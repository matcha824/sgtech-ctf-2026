FROM golang:1.26.3-alpine3.23 AS go-build

WORKDIR /build/backend

COPY backend/go.mod backend/go.sum ./
RUN go mod download

COPY backend/ ./
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /out/backend .

FROM node:26-alpine3.23 AS node-build

WORKDIR /build/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npx tsc && npm prune --omit=dev

FROM node:26-alpine3.23 AS final

WORKDIR /app

COPY --from=go-build /out/backend /app/backend/backend
COPY --from=node-build /build/frontend/dist /app/frontend/dist
COPY --from=node-build /build/frontend/static /app/frontend/static
COPY --from=node-build /build/frontend/node_modules /app/frontend/node_modules
COPY --from=node-build /build/frontend/package.json /app/frontend/package.json

ENV FLAG=sgctf{wh0_s41d_y0u_c0u1d_r34d_my_p3r50n41_n0735}

EXPOSE 3000

CMD ["sh", "-c", "cd /app/backend && ./backend & cd /app/frontend && exec node dist/index.js"]
