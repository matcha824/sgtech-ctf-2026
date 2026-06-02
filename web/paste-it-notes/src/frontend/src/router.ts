import type { IncomingMessage, ServerResponse } from "http";
import { FileServer } from "./fileserver.js";

type Handler = (
  req: IncomingMessage,
  res: ServerResponse<IncomingMessage>,
) => Promise<void>;

export const METHODS = Object.freeze({
  GET: "GET",
  POST: "POST",
  PUT: "PUT",
  PATCH: "PATCH",
  DELETE: "DELETE",
  OPTIONS: "OPTIONS",
  HEAD: "HEAD",
});

type Method = (typeof METHODS)[keyof typeof METHODS];

type Route = {
  path: RegExp;
  methods: Method | Method[];
  handler: Handler;
};

class Router {
  routes: Route[] = [];
  errorHandlers: Record<number, Handler> = {};
  fileServer: FileServer = new FileServer("./static");

  get(path: RegExp, handler: Handler): void {
    this.route(path, METHODS.GET, handler);
  }

  post(path: RegExp, handler: Handler): void {
    this.route(path, METHODS.POST, handler);
  }

  put(path: RegExp, handler: Handler): void {
    this.route(path, METHODS.PUT, handler);
  }

  patch(path: RegExp, handler: Handler): void {
    this.route(path, METHODS.PATCH, handler);
  }

  delete(path: RegExp, handler: Handler): void {
    this.route(path, METHODS.DELETE, handler);
  }

  options(path: RegExp, handler: Handler): void {
    this.route(path, METHODS.OPTIONS, handler);
  }

  head(path: RegExp, handler: Handler): void {
    this.route(path, METHODS.HEAD, handler);
  }

  error(statusCode: number, handler: Handler): void {
    this.errorHandlers[statusCode] = handler;
  }

  route(path: RegExp, methods: Method | Method[], handler: Handler): void {
    this.routes.push({ path, methods, handler });
  }

  async getRouteHandler(
    path: string,
    method: string,
  ): Promise<Handler | undefined> {
    const route = this.routes.find(
      (r) =>
        r.path.test(path) &&
        (Array.isArray(r.methods)
          ? r.methods.includes(method as Method)
          : r.methods === method),
    );
    if (route) {
      return route.handler;
    }
    if (await this.fileServer.hasFile(path)) {
      return async (req, res) => {
        await this.getStaticFile(path, res);
      };
    }
    return undefined;
  }

  getErrorHandler(statusCode: number): Handler | undefined {
    return this.errorHandlers[statusCode];
  }

  isValidMethod(method: string): method is Method {
    return (Object.values(METHODS) as readonly string[]).includes(method);
  }

  serveStaticFile(path: RegExp, file: string): void {
    this.get(path, async (req, res) => {
      await this.getStaticFile(file, res);
    });
    this.head(path, async (req, res) => {
      await this.headStaticFile(file, res);
    });
  }

  private async getStaticFile(
    path: string,
    res: ServerResponse<IncomingMessage>,
  ): Promise<void> {
    try {
      const file = await this.fileServer.getFile(path);

      res.statusCode = 200;
      res.setHeader("Content-Type", file.details.contentType);
      res.setHeader("Content-Length", file.details.size);
      res.end(file.content);
    } catch (err) {
      res.statusCode = 404;
      res.end("File not found");
    }
  }

  private async headStaticFile(
    path: string,
    res: ServerResponse<IncomingMessage>,
  ): Promise<void> {
    try {
      const details = await this.fileServer.getFileDetails(path);
      res.statusCode = 200;
      res.setHeader("Content-Type", details.contentType);
      res.setHeader("Content-Length", details.size);
      res.end();
    } catch (err) {
      res.statusCode = 404;
      res.end();
    }
  }
}

export { Router };
