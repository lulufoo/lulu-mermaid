"""Legacy envelope backfill (called from pointer models)."""
from __future__ import annotations

from document_meta import ID_RE, correct_envelope
from drawer_ctl import paths
from drawer_ctl import util
from drawer_ctl import document
from drawer_ctl import mermaid

def lift_nested_mermaid_history() -> int:
    """Move history/mermaid/* up to history/ and rewrite meta.current."""
    dest = paths.history_root()
    nested = dest / "mermaid"
    if not nested.is_dir():
        return 0
    moved = 0
    for src in nested.iterdir():
        if not src.is_file():
            continue
        target = dest / src.name
        if target.exists():
            continue
        src.replace(target)
        moved += 1
    meta = mermaid.read_meta_raw()
    cur = str(meta.get("current") or meta.get("archive") or "")
    prefix = "history/mermaid/"
    if cur.startswith(prefix):
        meta["current"] = "history/" + cur[len(prefix) :]
        mermaid.write_meta(meta)
        mermaid.refresh_diagram_mmd_alias(mermaid.mermaid_record_path_from_meta(meta))
    try:
        next(nested.iterdir())
    except StopIteration:
        nested.rmdir()
    except OSError:
        pass
    return moved


def migrate_document_envelopes() -> dict:
    """One-shot: canonicalize envelope tokens; mint when a record has none."""
    lift_nested_mermaid_history()
    n_mermaid = 0
    for mmd in paths.mermaid_history_records():
        try:
            too_big = mmd.stat().st_size > paths.HISTORY_SOURCE_READ_CAP
        except OSError:
            continue
        if too_big:
            mermaid.ensure_history_entry_meta(mmd)
            continue
        raw = util.read_text_capped(mmd)
        if not raw:
            continue
        side = mermaid._read_history_sidecar(mmd)
        sid = str(side.get("id") or "").strip()
        if not ID_RE["mermaid"].match(sid):
            sid = util.new_diagram_id()
        out, changed = correct_envelope(raw, "mermaid", sid)
        if changed:
            util.write_text_atomic(mmd, out)
            n_mermaid += 1
        mermaid.ensure_history_entry_meta(mmd)
    mermaid_meta = mermaid.read_meta_raw()
    mrec = mermaid.mermaid_record_path_from_meta(mermaid_meta)
    if mrec is not None:
        live = document.envelope_live_fields(mrec, "mermaid")
        if live:
            mermaid_meta["id"] = live["id"]
            mermaid_meta["version"] = live["version"]
            mermaid_meta["rev"] = live["version"]
            mermaid.write_meta(mermaid_meta)
    return {"ok": True, "mermaid": n_mermaid}




