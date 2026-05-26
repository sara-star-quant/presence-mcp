# presence-mcp

<!-- mcp-name: io.github.sara-star-quant/presence-mcp -->

[![PyPI](https://img.shields.io/pypi/v/presence-mcp.svg)](https://pypi.org/project/presence-mcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/presence-mcp.svg)](https://pypi.org/project/presence-mcp/)
[![License: MIT](https://img.shields.io/pypi/l/presence-mcp.svg)](./LICENSE)
[![CI](https://github.com/sara-star-quant/presence-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/sara-star-quant/presence-mcp/actions/workflows/ci.yml)
[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-active-2ea44f)](https://registry.modelcontextprotocol.io/v0/servers?search=presence-mcp)

> PyPI launcher that exposes [presence](https://github.com/sara-star-quant/presence)'s living project model and outcome telemetry as MCP resources for Claude Desktop, Cursor, Continue, and other MCP-aware clients.

`presence` is a Claude Code plugin. It already ships a stdio MCP server at `lib/cli.py mcp` and exposes two read-only resources per repository (see [What you get](#what-you-get)). This package is the PyPI shim that lets that server be listed in the official [MCP Registry](https://github.com/mcp) and invoked with a single command name in every per-client config, instead of an absolute path that varies per machine.

The launcher itself speaks no MCP. It locates a local presence install and forwards stdio to `python lib/cli.py mcp`. About 40 lines of Python, stdlib only.

## Quick start

```bash
pip install presence-mcp
```

Then point any MCP client at the `presence-mcp` command. For Claude Desktop, that's:

```json
{
  "mcpServers": {
    "presence": {
      "command": "presence-mcp"
    }
  }
}
```

Full per-client config for [Cursor](#cursor) and [Continue](#continue) below. Requires Python 3.12+ and a local [presence](https://github.com/sara-star-quant/presence) install.

## What you get

Two read-only MCP resources, one per repository you've worked on:

| URI | Content | MIME type |
|---|---|---|
| `presence://<repo_id>/model` | Living `model.md` (Markdown) | `text/markdown` |
| `presence://<repo_id>/telemetry` | Recent commit / revert / verification claims (JSON array) | `application/json` |

`<repo_id>` is a 12-char SHA-256 prefix of the repo. The server resolves the current repo from the launcher's working directory; see [Working-directory caveat](#working-directory-caveat). Resource schema and protocol details: [presence's `docs/mcp.md`](https://github.com/sara-star-quant/presence/blob/main/docs/mcp.md).

## Per-client configuration

The same `presence-mcp` command works in every client.

### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS), or the equivalent on Windows / Linux:

```json
{
  "mcpServers": {
    "presence": {
      "command": "presence-mcp"
    }
  }
}
```

### Cursor

`.cursor/mcp.json` in the project root, or the global Cursor MCP settings:

```json
{
  "mcpServers": {
    "presence": {
      "command": "presence-mcp"
    }
  }
}
```

### Continue

`~/.continue/config.json`:

```json
{
  "mcpServers": [
    {
      "name": "presence",
      "command": "presence-mcp"
    }
  ]
}
```

### Verify the install

The launcher accepts JSON-RPC on stdin. Pasting `{"jsonrpc":"2.0","id":1,"method":"initialize"}` and pressing Enter should yield an `initialize` response. You can also invoke it as `python -m presence_mcp` if a console script isn't convenient.

## Environment variables

| Variable | Purpose |
|---|---|
| `PRESENCE_MCP_CLI` | Absolute path to presence's `lib/cli.py`. Overrides the default `~/.claude/plugins/presence/lib/cli.py` lookup. If set but the path is missing, the launcher errors out instead of falling back, so typos surface. |
| `PRESENCE_MCP_PYTHON` | Python interpreter to run presence with. Defaults to `sys.executable` of the launcher itself. Useful when presence is installed under a different Python (for example, a project venv). |

If `presence-mcp` reports it could not locate presence, install presence at the standard Claude Code plugin path, or set `PRESENCE_MCP_CLI`.

## Working-directory caveat

presence's MCP server resolves the current repo from the launcher's working directory via `git rev-parse --show-toplevel`. MCP clients that launch the server from a fixed directory will only see one repo. To switch repos, either launch a separate instance per project (set `cwd` in the client's per-server config), or restart the server from the target project root.

## Compatibility

- **Python:** 3.12 or newer. CI matrix covers 3.12 / 3.13 / 3.14.
- **presence:** tested with `>= 0.6.0`. Older versions back to v0.4.1 (where the MCP server first shipped) may still work but are not exercised by CI.
- **Platforms:** Linux and macOS exercised in CI. Windows is untested in v0.1.0. The launcher uses `subprocess.run` which is cross-platform, but the default presence install path (`~/.claude/plugins/presence/lib/cli.py`) needs a real Windows install to confirm. Report issues if you try it.

This launcher is protocol-agnostic: it does **not** rev when presence ships new MCP resources. It only revs when its own resolution logic, CLI surface, or `server.json` content changes.

## Where to file issues

- **Launcher bugs** (path detection, install errors, CLI argument forwarding): [issues on this repo](https://github.com/sara-star-quant/presence-mcp/issues).
- **Resource-content bugs** (what `presence://*/model` returns, telemetry schema, working-directory behavior, anything about the protocol itself): [issues on the presence repo](https://github.com/sara-star-quant/presence/issues).

## Disambiguation

presence's MCP server advertises `serverInfo.name = "presence-mcp"` in its `initialize` response. That's the server's MCP identity. This package is the PyPI launcher. The names match by intent.

## Links

- PyPI: https://pypi.org/project/presence-mcp/
- MCP Registry: https://registry.modelcontextprotocol.io/v0/servers?search=presence-mcp (`io.github.sara-star-quant/presence-mcp`)
- Upstream (presence): https://github.com/sara-star-quant/presence

## License

MIT. See [LICENSE](./LICENSE).
