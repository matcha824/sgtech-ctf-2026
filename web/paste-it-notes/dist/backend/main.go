package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

type Paste struct {
	Contents string `json:"contents"`
	CreatedAt int64 `json:"created_at"`
	ID uint64 `json:"id"`
	Hidden bool `json:"hidden"`
}

type PasteStore struct {
	Pastes map[uint64]Paste
	current uint64
}

func NewPasteStore() *PasteStore {
	return &PasteStore{
		Pastes: make(map[uint64]Paste),
		current: 0,
	}
}

func (store *PasteStore) AddPaste(contents string, hidden bool) uint64 {
	store.current++
	id := store.current
	paste := Paste{
		Contents: contents,
		CreatedAt: time.Now().Unix(),
		ID: id,
		Hidden: hidden,
	}
	store.Pastes[id] = paste
	return id
}

func (store *PasteStore) GetPaste(id uint64) (*Paste, error) {
	paste, exists := store.Pastes[id]
	if !exists {
		return nil, fmt.Errorf("paste not found")
	}
	return &paste, nil
}

func (store *PasteStore) DeletePaste(id uint64) error {
	paste, err := store.GetPaste(id)
	if err != nil {
		return fmt.Errorf("paste not found")
	}
	paste.Hidden = true
	store.Pastes[id] = *paste
	return nil
}

func (store *PasteStore) SetPasteVisibility(id uint64, visible bool) error {
	paste, err := store.GetPaste(id)
	if err != nil {
		return fmt.Errorf("paste not found")
	}
	paste.Hidden = !visible
	store.Pastes[id] = *paste
	return nil
}

func handlePaste(store *PasteStore) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodPost:
			handlePostPaste(store)(w, r)
		case http.MethodGet:
			handleGetPaste(store)(w, r)
		case http.MethodDelete:
			handleDeletePaste(store)(w, r)
		default:
			writeJSON(w, http.StatusMethodNotAllowed, map[string]string{
				"error": "method not allowed",
			})
		}
	}
}

func handlePostPaste(store *PasteStore) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req struct {
			Contents string `json:"contents"`
		}
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{
				"error": "invalid request body",
			})
			return
		}

		id := store.AddPaste(req.Contents, false)
		writeJSON(w, http.StatusCreated, map[string]string{
			"message": "paste created",
			"id": fmt.Sprintf("%d", id),
		})
	}
}

func getId(r *http.Request) (uint64, error) {
	id := r.URL.Query().Get("id")
	if id == "" {
		return 0, fmt.Errorf("missing id parameter")
	}

	var pid uint64
	_, err := fmt.Sscanf(id, "%d", &pid)
	if err != nil {
		return 0, fmt.Errorf("invalid id parameter")
	}
	return pid, nil
}

func handleGetPaste(store *PasteStore) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		id, err := getId(r)
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{
				"error": err.Error(),
			})
			return
		}

		paste, err := store.GetPaste(id)

		if err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{
				"error": "paste not found",
			})
			return
		}

		if paste.Hidden {
			writeJSON(w, http.StatusNotFound, map[string]string{
				"error": "paste not found",
			})
			return
		}

		writeJSON(w, http.StatusOK, paste)
	}
}

func handleDeletePaste(store *PasteStore) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		id, err := getId(r)
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{
				"error": err.Error(),
			})
			return
		}

		if err := store.DeletePaste(id); err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{
				"error": "paste not found",
			})
			return
		}
		writeJSON(w, http.StatusOK, map[string]string{
			"message": "paste deleted",
			"id": fmt.Sprintf("%d", id),
		})
	}
}

func handlePasteVisibility(store *PasteStore, visible bool) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		id, err := getId(r)
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{
				"error": err.Error(),
			})
			return
		}

		if err := store.SetPasteVisibility(id, visible); err != nil {
			writeJSON(w, http.StatusNotFound, map[string]string{
				"error": "paste not found",
			})
			return
		}

		writeJSON(w, http.StatusOK, map[string]string{
			"message": "paste visibility updated",
			"id": fmt.Sprintf("%d", id),
		})
	}
}

func main() {
	port := os.Getenv("PORT")
	flag := os.Getenv("FLAG")

	if port == "" {
		port = "8000"
	}

	if flag == "" {
		log.Fatal("FLAG environment variable is not set")
	}

	store := NewPasteStore()
	store.AddPaste(flag, true)

	mux := http.NewServeMux()
	mux.HandleFunc("/api/paste", handlePaste(store))
	mux.HandleFunc("/internal/visible", handlePasteVisibility(store, true))
	mux.HandleFunc("/internal/hidden", handlePasteVisibility(store, false))

	server := &http.Server{
		Addr:              ":" + port,
		Handler:           loggingMiddleware(mux),
		ReadHeaderTimeout: 5 * time.Second,
	}

	shutdownSignals := make(chan os.Signal, 1)
	signal.Notify(shutdownSignals, os.Interrupt, syscall.SIGTERM)

	go func() {
		<-shutdownSignals

		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		if err := server.Shutdown(ctx); err != nil {
			log.Printf("graceful shutdown failed: %v", err)
		}
	}()

	log.Printf("listening on http://0.0.0.0:%s", port)
	if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("server failed: %v", err)
	}

	log.Println("server stopped")
}

func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		started := time.Now()
		next.ServeHTTP(w, r)
		log.Printf("%s %s %s", r.Method, r.URL.Path, time.Since(started))
	})
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)

	if err := json.NewEncoder(w).Encode(payload); err != nil {
		log.Printf("failed to write response: %v", err)
	}
}
