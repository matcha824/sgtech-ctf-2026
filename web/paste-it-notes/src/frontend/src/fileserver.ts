import { NodeCache } from "@cacheable/node-cache";
import { readFile, stat } from "fs/promises";
import path from "path";

type FileDetails = {
  contentType: string;
  size: number;
};

export type StaticFile = {
  content: Buffer;
  details: FileDetails;
};

const CONTENT_TYPES: Record<string, string> = {
  ".css": "text/css; charset=utf-8",
  ".gif": "image/gif",
  ".html": "text/html; charset=utf-8",
  ".ico": "image/x-icon",
  ".jpeg": "image/jpeg",
  ".jpg": "image/jpeg",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".webp": "image/webp",
};

class CachedFile {
  content: Buffer;
  details: FileDetails;

  constructor(content: Buffer, details: FileDetails) {
    this.content = content;
    this.details = details;
  }
}

export class FileServer {
  private readonly rootPath: string;
  private readonly cache: NodeCache<CachedFile> = new NodeCache({
    stdTTL: 60,
    checkperiod: 120,
    deleteOnExpire: true,
  });

  constructor(basePath: string) {
    this.rootPath = path.resolve(basePath);
  }

  async hasFile(file: string): Promise<boolean> {
    try {
      await this.getCachedFile(file);
      return true;
    } catch {
      return false;
    }
  }

  async getFileContent(file: string): Promise<Buffer> {
    return (await this.getCachedFile(file)).content;
  }

  async getFileDetails(file: string): Promise<FileDetails> {
    return (await this.getCachedFile(file)).details;
  }

  async getFile(file: string): Promise<StaticFile> {
    const cachedFile = await this.getCachedFile(file);

    return {
      content: cachedFile.content,
      details: cachedFile.details,
    };
  }

  private async getCachedFile(file: string): Promise<CachedFile> {
    const filePath = this.getFilePath(file);
    const cachedFile = this.cache.get(filePath);

    if (cachedFile) {
      return cachedFile;
    }

    const [content, fileStats] = await Promise.all([
      readFile(filePath),
      stat(filePath),
    ]);
    const extension = path.extname(filePath).toLowerCase();

    const nextFile = new CachedFile(content, {
      contentType: CONTENT_TYPES[extension] ?? "application/octet-stream",
      size: fileStats.size,
    });

    this.cache.set(filePath, nextFile);
    return nextFile;
  }

  private getFilePath(file: string): string {
    const requestedPath = path.resolve(this.rootPath, `.${path.sep}${file}`);
    const relativePath = path.relative(this.rootPath, requestedPath);

    if (relativePath.startsWith("..") || path.isAbsolute(relativePath)) {
      throw new Error("invalid file path");
    }

    return requestedPath;
  }
}
