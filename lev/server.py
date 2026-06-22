from __future__ import annotations

import argparse
import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from lev.assist import generate_assistance
from lev.models import AssistRequest, DocumentPayload
from lev.workspace import Workspace


ROOT = Path(__file__).resolve().parent.parent
WEB_ROOT = ROOT / "web"


def json_bytes(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


class LevRequestHandler(BaseHTTPRequestHandler):
    workspace: Workspace

    def log_message(self, format: str, *args: object) -> None:
        print(f"[Lev] {self.address_string()} - {format % args}")

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/documents":
            self.send_json([doc.to_dict() for doc in self.workspace.list_documents()])
            return

        if parsed.path == "/api/document":
            query = parse_qs(parsed.query)
            rel_path = query.get("path", [""])[0]
            try:
                content = self.workspace.read_document(rel_path)
            except Exception as exc:
                self.send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
                return
            self.send_json({"path": rel_path, "content": content})
            return

        self.serve_static(parsed.path)

    def do_HEAD(self) -> None:
        parsed = urlparse(self.path)
        self.serve_static(parsed.path, head_only=True)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            body = self.read_json_body()
        except ValueError as exc:
            self.send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
            return

        if parsed.path == "/api/document":
            try:
                payload = DocumentPayload.from_dict(body)
                self.workspace.write_document(payload.path, payload.content)
            except Exception as exc:
                self.send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
                return
            self.send_json({"ok": True})
            return

        if parsed.path == "/api/assist":
            try:
                request = AssistRequest.from_dict(body)
                response = generate_assistance(request)
            except Exception as exc:
                self.send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
                return
            self.send_json(response.to_dict())
            return

        self.send_error_json(HTTPStatus.NOT_FOUND, "Not found")

    def read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON") from exc
        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object")
        return payload

    def serve_static(self, request_path: str, head_only: bool = False) -> None:
        rel_path = request_path.lstrip("/") or "index.html"
        if rel_path == "":
            rel_path = "index.html"

        full_path = (WEB_ROOT / rel_path).resolve()
        if WEB_ROOT not in full_path.parents and full_path != WEB_ROOT:
            self.send_error_json(HTTPStatus.BAD_REQUEST, "Path escapes web root")
            return
        if not full_path.exists() or not full_path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content_type = mimetypes.guess_type(full_path.name)[0] or "application/octet-stream"
        data = full_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if not head_only:
            self.wfile.write(data)

    def send_json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_error_json(self, status: HTTPStatus, message: str) -> None:
        self.send_json({"error": message}, status=status)


def run_server(workspace_path: str, host: str, port: int) -> None:
    LevRequestHandler.workspace = Workspace(workspace_path)
    server = ThreadingHTTPServer((host, port), LevRequestHandler)
    url = f"http://{host}:{port}"
    print(f"[Lev] Workspace: {LevRequestHandler.workspace.root}")
    print(f"[Lev] Open: {url}")
    server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Lev human-centered agent MVP.")
    parser.add_argument(
        "workspace",
        nargs="?",
        default=".",
        help="Folder Lev should open as the project workspace.",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    run_server(args.workspace, args.host, args.port)


if __name__ == "__main__":
    main()
