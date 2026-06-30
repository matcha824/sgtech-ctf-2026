// DPoP helpers
package servers

import (
	"crypto"
	"crypto/ecdsa"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"sync"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/lestrrat-go/jwx/v2/jwk"
)

const dpopMaxSkew = 300 * time.Second

func athHash(accessToken string) string {
	sum := sha256.Sum256([]byte(accessToken))
	return base64.RawURLEncoding.EncodeToString(sum[:])
}

func parseDPoPProof(proof string) (jkt string, claims jwt.MapClaims, err error) {
	claims = jwt.MapClaims{}
	var thumbprint string

	parser := jwt.NewParser(
		jwt.WithValidMethods([]string{"ES256"}),
		jwt.WithIssuedAt(),
	)

	_, err = parser.ParseWithClaims(proof, claims, func(t *jwt.Token) (any, error) {
		if typ, _ := t.Header["typ"].(string); typ != "dpop+jwt" {
			return nil, fmt.Errorf("unexpected typ header: %v", t.Header["typ"])
		}
		raw, ok := t.Header["jwk"]
		if !ok {
			return nil, fmt.Errorf("missing jwk header")
		}
		b, err := json.Marshal(raw)
		if err != nil {
			return nil, fmt.Errorf("bad jwk header: %w", err)
		}
		key, err := jwk.ParseKey(b)
		if err != nil {
			return nil, fmt.Errorf("bad jwk header: %w", err)
		}
		tp, err := key.Thumbprint(crypto.SHA256)
		if err != nil {
			return nil, fmt.Errorf("thumbprint: %w", err)
		}
		thumbprint = base64.RawURLEncoding.EncodeToString(tp)

		var pub ecdsa.PublicKey
		if err := key.Raw(&pub); err != nil {
			return nil, fmt.Errorf("jwk is not an EC public key: %w", err)
		}
		return &pub, nil
	})
	if err != nil {
		return "", nil, err
	}

	iat, err := claims.GetIssuedAt()
	if err != nil || iat == nil {
		return "", nil, fmt.Errorf("missing iat")
	}
	if d := time.Since(iat.Time); d > dpopMaxSkew || d < -dpopMaxSkew {
		return "", nil, fmt.Errorf("proof iat outside acceptable window")
	}

	return thumbprint, claims, nil
}

type jtiCache struct {
	seen sync.Map
	ttl  time.Duration
}

func newJTICache(ttl time.Duration) *jtiCache {
	return &jtiCache{ttl: ttl}
}

func (c *jtiCache) useOnce(jti string, now time.Time) bool {
	if jti == "" {
		return true
	}
	c.seen.Range(func(k, v any) bool {
		if now.Sub(v.(time.Time)) > c.ttl {
			c.seen.Delete(k)
		}
		return true
	})
	_, loaded := c.seen.LoadOrStore(jti, now)
	return !loaded
}
