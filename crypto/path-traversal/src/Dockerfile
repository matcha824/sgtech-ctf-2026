FROM golang:1.26.3 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/pathtrav .

FROM gcr.io/distroless/static-debian12
COPY --from=build /out/pathtrav /pathtrav
ENV AUTH_PORT=8000 RESOURCE_PORT=8001 RESOURCE_HOST=localhost
ENV FLAG=sgtech{dpop_htu_not_sanitized}
EXPOSE 8000 8001
ENTRYPOINT ["/pathtrav"]
