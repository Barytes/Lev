from dataclasses import asdict, dataclass


@dataclass
class DocumentInfo:
    path: str
    name: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DocumentPayload:
    path: str
    content: str

    @classmethod
    def from_dict(cls, payload: dict) -> "DocumentPayload":
        return cls(path=str(payload.get("path", "")), content=str(payload.get("content", "")))


@dataclass
class AssistRequest:
    path: str
    content: str
    previous_content: str = ""
    cursor: int = 0
    selection_start: int = 0
    selection_end: int = 0

    @classmethod
    def from_dict(cls, payload: dict) -> "AssistRequest":
        return cls(
            path=str(payload.get("path", "")),
            content=str(payload.get("content", "")),
            previous_content=str(payload.get("previous_content", "")),
            cursor=int(payload.get("cursor", 0) or 0),
            selection_start=int(payload.get("selection_start", 0) or 0),
            selection_end=int(payload.get("selection_end", 0) or 0),
        )


@dataclass
class AssistResponse:
    assistance: str
    intent: str = "unknown"
    source: str = "agent"

    def to_dict(self) -> dict:
        return asdict(self)

