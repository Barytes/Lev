from pathlib import Path
from typing import Union

from lev.models import DocumentInfo


IGNORED_DIRS = {".git", ".venv", "__pycache__", "node_modules", "web"}
SUPPORTED_SUFFIXES = {".md", ".txt"}


class Workspace:
    def __init__(self, root: Union[str, Path]):
        self.root = Path(root).expanduser().resolve()
        if not self.root.exists():
            raise FileNotFoundError(f"Workspace does not exist: {self.root}")
        if not self.root.is_dir():
            raise NotADirectoryError(f"Workspace is not a directory: {self.root}")

    def list_documents(self) -> list[DocumentInfo]:
        documents: list[DocumentInfo] = []
        for path in sorted(self.root.rglob("*")):
            if not path.is_file():
                continue
            if any(part in IGNORED_DIRS for part in path.relative_to(self.root).parts):
                continue
            if path.suffix.lower() not in SUPPORTED_SUFFIXES:
                continue
            rel = path.relative_to(self.root).as_posix()
            documents.append(DocumentInfo(path=rel, name=path.name))
        return documents

    def resolve_document(self, rel_path: str) -> Path:
        if not rel_path:
            raise ValueError("path cannot be empty")

        full_path = (self.root / rel_path).resolve()
        if self.root not in full_path.parents and full_path != self.root:
            raise ValueError("path escapes workspace")
        if full_path.suffix.lower() not in SUPPORTED_SUFFIXES:
            raise ValueError("unsupported document type")
        return full_path

    def read_document(self, rel_path: str) -> str:
        path = self.resolve_document(rel_path)
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")

    def write_document(self, rel_path: str, content: str) -> None:
        path = self.resolve_document(rel_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
