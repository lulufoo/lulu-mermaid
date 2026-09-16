"""Shared paths and mutable STATE_DIR."""
from __future__ import annotations

from pathlib import Path

STATE_DIR = Path.home() / ".cache" / "mermaid"
DEFAULT_PORT = 49868  # fixed loopback; CLI --port 0 means "use this"
SERVER_FILE = "server.json"
SOURCE_FILE = "diagram.mmd"
META_FILE = "diagram.meta.json"
VIEWER_FILE = "drawer.html"
HISTORY_DIR_NAME = "history"
EXPORT_DIR_NAME = "export"
HISTORY_SOURCE_READ_CAP = 256_000


def skill_root() -> Path:
    """Install root: skill/ (parent of this scripts/ dir)."""
    return Path(__file__).resolve().parents[2]


def asset_path() -> Path:
    return skill_root() / "assets" / VIEWER_FILE


def server_path() -> Path:
    return STATE_DIR / SERVER_FILE


def source_path():
    return STATE_DIR / SOURCE_FILE


def read_text_capped(path: Path, cap: int = HISTORY_SOURCE_READ_CAP) -> str:
    """Read a history source without pulling a runaway file into memory."""
    try:
        with path.open("rb") as fh:
            raw = fh.read(max(1, int(cap)))
        return raw.decode("utf-8", errors="replace")
    except OSError:
        return ""


def mermaid_history_records() -> list[Path]:
    return sorted(
        (path for path in history_dir().glob("*.mmd") if path.is_file()),
        key=lambda path: path.name,
        reverse=True,
    )


def history_root() -> Path:
    d = STATE_DIR / HISTORY_DIR_NAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def history_dir() -> Path:
    return history_root()


def meta_path() -> Path:
    return STATE_DIR / META_FILE


def export_dir() -> Path:
    d = STATE_DIR / EXPORT_DIR_NAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def mermaid_example_template_dir() -> Path:
    return skill_root() / "assets" / "templates" / "mermaid"


def mermaid_example_template_sources() -> list[Path]:
    root = mermaid_example_template_dir()
    if not root.is_dir():
        return []
    return sorted(p for p in root.glob("*.mmd") if p.is_file())
