import pkg from "http-proxy";
const { createProxyServer } = pkg;
import * as http from "http";
import { Router, METHODS } from "./src/router.js";

const PORT = 3000;

const proxy = createProxyServer();
const router = new Router();

router.serveStaticFile(/^\/$/, "index.html");

router.route(
  /^\/api\//,
  [METHODS.GET, METHODS.POST, METHODS.DELETE],
  async (req, res) => {
    proxy.web(req, res, { target: "http://localhost:8000" }, (e: Error) => {
      console.log(e);
    });
  },
);

router.serveStaticFile(/^\/paste\/[^/]+$/, "paste.html");

const server = http.createServer(
  async (
    req: http.IncomingMessage,
    res: http.ServerResponse<http.IncomingMessage>,
  ) => {
    const date = new Date().toISOString();
    console.log(`[${date}] ${req.method} ${req.url}`);

    if (!req.method || !router.isValidMethod(req.method)) {
      res.statusCode = 405;
      res.end("Method Not Allowed");
      return;
    }

    const url = new URL(req.url ?? "", `http://${req.headers.host}`);
    const handler = await router.getRouteHandler(url.pathname, req.method);

    if (!handler) {
      res.statusCode = 404;
      res.end("Not Found");
      return;
    }
    await handler(req, res);
  },
);

server.on("clientError", (err, socket) => {
  socket.end("HTTP/1.1 400 Bad Request\r\n\r\n");
});

server.on("close", () => {
  console.log("Server has successfully shut down.");
});

server.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
