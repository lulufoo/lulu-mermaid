# Viewer

Local loopback viewer for Mermaid. Loaded from `/mermaid` only. Not a slash skill.

Use `$DRAWER_CTL` from the mermaid entry. Extra verbs: `mount`, `status`, `stop`.
Subcommand contract: `$DRAWER_CTL --help`.

Write-back is `preview`, not `set-source`. `--id` is MMD ID. Required on
`get-source`. Omit on `preview` / `set-source` only to mint.

`history/*.mmd` (+ `.json` sidecar) are the record list. `current` is the viewed
pointer, not identity. History click retargets `current`. UI Source writes
through `current` and does not create records.

On start, if `history` has no `*.mmd`, the viewer seeds packed templates under
`../assets/templates/mermaid/*.mmd` and points `current` at checkout when present.

`preview` with no file and no stdin does not create a record.
stdout `open` is `created` | `current`.
