package servers

import (
	"crypto/ecdsa"
	"crypto/subtle"
	"net/http"
	"net/url"
	"path"
	"strings"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

type ResourceServer struct {
	authPubKey *ecdsa.PublicKey
	routes     map[string]string
	jtis       *jtiCache
}

func NewResourceServer(authPubKey *ecdsa.PublicKey, flag string) *ResourceServer {
	return &ResourceServer{
		authPubKey: authPubKey,
		routes: map[string]string{
			"/api/public":       `{"message":"hello world","hint":"token only grants access to /api/public"}`,
			"/api/public/info":  `{"message":"public info: nothing secret here"}`,
			"/api/private/flag": flag,
		},
		jtis: newJTICache(accessTokenTTL),
	}
}

func (s *ResourceServer) Handler() http.Handler {
	return http.HandlerFunc(s.serve)
}

func (s *ResourceServer) serve(w http.ResponseWriter, r *http.Request) {
	authz := r.Header.Get("Authorization")
	rawToken, ok := strings.CutPrefix(authz, "DPoP ")
	if !ok || rawToken == "" {
		writeError(w, http.StatusUnauthorized, "missing 'Authorization: DPoP <token>' header")
		return
	}
	tokenClaims := jwt.MapClaims{}
	_, err := jwt.NewParser(jwt.WithValidMethods([]string{"ES256"})).
		ParseWithClaims(rawToken, tokenClaims, func(*jwt.Token) (any, error) {
			return s.authPubKey, nil
		})
	if err != nil {
		writeError(w, http.StatusUnauthorized, "invalid access token: "+err.Error())
		return
	}

	proof := r.Header.Get("DPoP")
	if proof == "" {
		writeError(w, http.StatusUnauthorized, "missing DPoP proof header")
		return
	}
	jkt, proofClaims, err := parseDPoPProof(proof)
	if err != nil {
		writeError(w, http.StatusUnauthorized, "invalid DPoP proof: "+err.Error())
		return
	}

	cnf, _ := tokenClaims["cnf"].(map[string]any)
	boundJKT, _ := cnf["jkt"].(string)
	if boundJKT == "" || subtle.ConstantTimeCompare([]byte(boundJKT), []byte(jkt)) != 1 {
		writeError(w, http.StatusUnauthorized, "access token is not bound to this DPoP key")
		return
	}

	if ath, _ := proofClaims["ath"].(string); ath != athHash(rawToken) {
		writeError(w, http.StatusUnauthorized, "DPoP ath mismatch")
		return
	}

	if htm, _ := proofClaims["htm"].(string); htm != r.Method {
		writeError(w, http.StatusUnauthorized, "DPoP htm mismatch")
		return
	}
	if jti, _ := proofClaims["jti"].(string); !s.jtis.useOnce(jti, time.Now()) {
		writeError(w, http.StatusUnauthorized, "DPoP proof replay detected")
		return
	}

	htu, _ := proofClaims["htu"].(string)
	htuURL, err := url.Parse(htu)
	if err != nil {
		writeError(w, http.StatusUnauthorized, "DPoP htu is not a valid URL")
		return
	}
	if htuURL.Host != r.Host || htuURL.Path != r.URL.Path {
		writeError(w, http.StatusUnauthorized, "DPoP htu does not match the request")
		return
	}

	grantedScope, _ := tokenClaims["resource"].(string)
	if !strings.HasPrefix(htuURL.Path, grantedScope) {
		writeError(w, http.StatusForbidden, "request is outside the granted scope")
		return
	}
	// oops vulnerability: ../
	resolved := path.Clean(htuURL.Path)

	body, ok := s.routes[resolved]
	if !ok {
		writeError(w, http.StatusNotFound, "no such resource")
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte(body))
}
