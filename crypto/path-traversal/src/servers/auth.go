package servers

import (
	"crypto/ecdsa"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"net/http"
	"sync"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

const grantedResourcePath = "/api/public"

// expires in
const accessTokenTTL = 10 * time.Minute

type AuthServer struct {
	signingKey *ecdsa.PrivateKey
	clients    sync.Map
	jtis       *jtiCache
}

func NewAuthServer(signingKey *ecdsa.PrivateKey) *AuthServer {
	return &AuthServer{
		signingKey: signingKey,
		jtis:       newJTICache(accessTokenTTL),
	}
}

func (s *AuthServer) Handler() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("/api/register-client", s.handleRegister)
	mux.HandleFunc("/api/token", s.handleToken)
	return mux
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func writeError(w http.ResponseWriter, status int, msg string) {
	writeJSON(w, status, map[string]string{"error": msg})
}

func (s *AuthServer) handleRegister(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeError(w, http.StatusMethodNotAllowed, "use POST")
		return
	}
	idBytes := make([]byte, 16)
	if _, err := rand.Read(idBytes); err != nil {
		writeError(w, http.StatusInternalServerError, "could not generate client_id")
		return
	}
	clientID := hex.EncodeToString(idBytes)
	s.clients.Store(clientID, struct{}{})

	writeJSON(w, http.StatusOK, map[string]any{
		"client_id":        clientID,
		"granted_scope":    grantedResourcePath,
		"spec":             "https://datatracker.ietf.org/doc/html/rfc9449",
		"how_to_get_token": "POST /api/token with form field client_id=<client_id> and a 'DPoP' header: a DPoP proof JWT signed by your EC P-256 key (ES256) with the public 'jwk' in the JWT header and claims htm=POST, htu=<this token endpoint's URL>, jti, iat.",
		"how_to_use_token": "Call the resource server with 'Authorization: DPoP <access_token>' plus a fresh 'DPoP' proof header whose claims are htm, htu (matching the request URL), jti, iat, and ath=base64url(sha256(access_token)).",
	})
}

func (s *AuthServer) handleToken(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeError(w, http.StatusMethodNotAllowed, "use POST")
		return
	}

	proof := r.Header.Get("DPoP")
	if proof == "" {
		writeError(w, http.StatusBadRequest, "missing DPoP proof header")
		return
	}
	jkt, claims, err := parseDPoPProof(proof)
	if err != nil {
		writeError(w, http.StatusUnauthorized, "invalid DPoP proof: "+err.Error())
		return
	}

	if htm, _ := claims["htm"].(string); htm != http.MethodPost {
		writeError(w, http.StatusUnauthorized, "DPoP htm mismatch")
		return
	}
	expectedHTU := "http://" + r.Host + r.URL.Path
	if htu, _ := claims["htu"].(string); htu != expectedHTU {
		writeError(w, http.StatusUnauthorized, "DPoP htu mismatch")
		return
	}
	if jti, _ := claims["jti"].(string); !s.jtis.useOnce(jti, time.Now()) {
		writeError(w, http.StatusUnauthorized, "DPoP proof replay detected")
		return
	}

	clientID := r.FormValue("client_id")
	if clientID == "" {
		writeError(w, http.StatusBadRequest, "missing client_id")
		return
	}
	if _, ok := s.clients.Load(clientID); !ok {
		writeError(w, http.StatusUnauthorized, "unknown client_id")
		return
	}

	now := time.Now()
	tokenClaims := jwt.MapClaims{
		"sub":      clientID,
		"resource": grantedResourcePath,
		"cnf":      map[string]string{"jkt": jkt},
		"iat":      now.Unix(),
		"exp":      now.Add(accessTokenTTL).Unix(),
	}
	signed, err := jwt.NewWithClaims(jwt.SigningMethodES256, tokenClaims).SignedString(s.signingKey)
	if err != nil {
		writeError(w, http.StatusInternalServerError, "could not issue token")
		return
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"access_token": signed,
		"token_type":   "DPoP",
		"expires_in":   int(accessTokenTTL.Seconds()),
	})
}
