package main

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"log"
	"net"
	"net/http"
	"os"

	"github.com/matcha824/sgtech-ctf-2026/crypto/path-traversal/servers"
)

func main() {
	var (
		authPort     = "8000"
		resourcePort = "8001"
		flag         = os.Getenv("FLAG")
	)

	signingKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		log.Fatalf("generate signing key: %v", err)
	}

	auth := servers.NewAuthServer(signingKey)
	resource := servers.NewResourceServer(&signingKey.PublicKey, flag)

	errc := make(chan error, 2)

	go func() {
		addr := net.JoinHostPort("0.0.0.0", authPort)
		log.Printf("auth server listening on %s", addr)
		errc <- http.ListenAndServe(addr, auth.Handler())
	}()

	go func() {
		addr := net.JoinHostPort("0.0.0.0", resourcePort)
		log.Printf("resource server listening on %s", addr)
		errc <- http.ListenAndServe(addr, resource.Handler())
	}()

	log.Fatal(<-errc)
}
