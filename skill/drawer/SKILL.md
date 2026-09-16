---
name: drawer
description: >-
  Start or control the local Mermaid viewer (content-addressed SSOT with
  document meta id and version).
argument-hint: "[Mermaid source path or intent]"
---

# drawer

Drawer is a local loopback viewer for Mermaid.

| Mode | ID | Source | Renderer |
|---|---|---|---|
| Mermaid | MMD ID (`m_…`) | MMD Source | Mermaid |

Diagram themes are `default` / `classic` / `pastel` / `kami`.

## Script Macros

| Macro | CLI |
|---|---|
| `$DRAWER_CTL` | `python3 scripts/drawer_control.py` |

Build / fetch tooling lives in the **dev monorepo** (`scripts/*-build`, `fetch_*.py`), not in this installable skill.

## Commands

```bash
$DRAWER_CTL preview --file path/to/diagram.mmd
$DRAWER_CTL preview --id m_…
$DRAWER_CTL get-source --kind mermaid --id m_…
$DRAWER_CTL set-source --id m_…
$DRAWER_CTL mount
$DRAWER_CTL status
$DRAWER_CTL stop
```

| `--kind` | Live store | Preview |
|---|---|---|
| `mermaid` | `diagram.mmd` | `?mode=mermaid` |

| Concern | Value |
|---|---|
| Write-back | `preview`, not `set-source` |
| Mermaid source | MMD Source (`diagram.mmd`). |
| Stash | Omit on mint; do not change on update. |
| Records | First identity is MMD ID. Source is the body. `current` is the viewed pointer only. CLI: `--id` is that ID (required on `get-source`; omit on `preview` / `set-source` only to mint). History click retargets `current`. |

## Mermaid identity + current pointer

`history/mermaid/*.mmd` (+ `.json` sidecar) are editable records. **MMD ID** (`m_…`) is which diagram. **MMD Source** is the body. `diagram.meta.json` `current` points at the viewed record. UI edits write through `current` (no new record). Only `preview` / `set-source` creates a record and retargets. History click only switches `current`.

| Term | Meaning |
|---|---|
| MMD ID | Which diagram (`m_…`). First identity. |
| MMD Source | The `.mmd` body. |
| `current` | Viewed pointer, not identity |
| `title` | Human label (`%% title`, else diagram kind, else stem) |
| `version` | Document version in the stash `meta` line |

**Constraint:** before any Mermaid operation in Drawer, run `$DRAWER_CTL status`
and read MMD ID first (then `get-source --id` if you need the MMD Source).

```bash
$DRAWER_CTL status
$DRAWER_CTL get-source --kind mermaid --id m_…
```

On start, if `history/mermaid` has no `*.mmd`, Drawer seeds every packed
flat file under `../assets/templates/mermaid/*.mmd` (from repo `examples/mermaid-*`, no PNGs)
and points `current` at checkout when present.
`preview` with no file and no stdin body does not create a record. With a body,
omit `--id` to mint; pass `--id` (MMD ID) to update that record.
stdout `open` is `created` | `current`. JSON `id` is MMD ID.

`diagram.mmd` may be a convenience symlink to `current`; readers/writers must honor `meta.current`.
UI Source edits write through the current record and do **not** create records. History click
only retargets `current`. Source dock uses `/history.json` and `DELETE /api/history/<file>`.
