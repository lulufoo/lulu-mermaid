<p align="center">
  <img src="docs/readme/logo.png" width="160" alt="Lulu Mermaid" />
</p>

<h1 align="center">Lulu Mermaid</h1>

<p align="center"><b>One text protocol. AI agent writes it. Lulu Mermaid draws it. You work on the canvas.</b></p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License"></a>
</p>

---

Mermaid diagrams in a local Drawer loop: the agent writes MMD, Lulu Mermaid renders it, you edit on the canvas or in Source.

| Mode | Product | Source ID |
|---|---|---|
| Mermaid | **Lulu Mermaid** | MMD (`m_…`) |

## Quick start

Install **only** the [`skill/`](./skill/) folder, then in chat:

```text
/mermaid
```

or:

```text
/mermaid Draw a checkout state diagram for me.
```

## Examples

### Mermaid

Rendering depends on [mermaid](https://github.com/mermaid-js/mermaid) and [elkjs](https://github.com/kieler/elkjs) (via `@mermaid-js/layout-elk`).

- [checkout.mmd](./examples/mermaid-state/checkout.mmd) — checkout state
- [ship-a-feature.mmd](./examples/mermaid-mindmap/ship-a-feature.mmd) — mindmap

## Install

Ship **`skill/`** only:

```text
skill/
  SKILL.md                 # agent entry
  mermaid/ drawer/         # mode skills
  assets/                  # viewer + History templates
  scripts/                 # drawer_control CLI
```

## Develop

From the repo root:

```bash
node scripts/drawer-app-build/build.mjs
node scripts/mermaid-ext-build/build.mjs
node scripts/examples-templates-build/build.mjs
```

Default cache is `~/.cache/mermaid`. ✅ Verified (`skill/scripts/drawer_ctl/paths.py` `STATE_DIR`).  
Default port is `49868`. ✅ Verified (`skill/scripts/drawer_ctl/paths.py` `DEFAULT_PORT`).

## License

- Project: [MIT](./LICENSE)
- Vendored Mermaid: [THIRD_PARTY.md](./THIRD_PARTY.md)
