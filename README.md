# presence-mcp

<!-- mcp-name: io.github.sara-star-quant/presence-mcp -->

Launcher for the [presence](https://github.com/sara-star-quant/presence) MCP server. `presence` is a Claude Code plugin that already exposes its living project model and outcome telemetry as MCP resources; this package is the PyPI-distributed shim that bridges that MCP server into the official [MCP Registry](https://github.com/mcp) so any MCP-aware client (Claude Desktop, Cursor, Continue, custom JSON-RPC clients, ...) can connect.

The launcher itself speaks no MCP. It locates a local presence install and runs `python lib/cli.py mcp`, forwarding stdio. See `docs/mcp.md` in the presence repo for the protocol details and resource schema.

## Install

1. Install [presence](https://github.com/sara-star-quant/presence) as a Claude Code plugin first. This launcher is a frontend, not a replacement.
2. `pip install presence-mcp` (or `pipx install presence-mcp`, or `uv tool install presence-mcp`). Requires Python 3.12+.
3. Verify: `presence-mcp` should accept JSON-RPC on stdin. Pasting `{"jsonrpc":"2.0","id":1,"method":"initialize"}` and pressing Enter should yield an `initialize` response from the presence MCP server.

You can also invoke it as `python -m presence_mcp` if a console script isn't convenient.

## Environment variables

| Variable | Purpose |
|---|---|
| `PRESENCE_MCP_CLI` | Absolute path to presence's `lib/cli.py`. Overrides the default `~/.claude/plugins/presence/lib/cli.py` lookup. |
| `PRESENCE_MCP_PYTHON` | Python interpreter to run presence with. Defaults to `sys.executable` of the launcher itself. Useful when presence is installed under a different Python (for example, a project venv). |

If `presence-mcp` reports it could not locate presence, install presence at the standard Claude Code plugin path, or set `PRESENCE_MCP_CLI`.

## Per-client configuration

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

## Working-directory caveat

presence's MCP server resolves the current repo from the launcher's working directory via `git rev-parse --show-toplevel` (see [presence's `docs/mcp.md`](https://github.com/sara-star-quant/presence/blob/main/docs/mcp.md)). MCP clients that launch the server from a fixed directory will only see one repo. To switch repos, either launch a separate instance per project (set `cwd` in the client's per-server config), or restart the server from the target project root.

## Disambiguation

presence's MCP server advertises `serverInfo.name = "presence-mcp"` in its `initialize` response (see presence `docs/mcp.md`). That's the server's MCP identity. This package is the PyPI launcher. The names match by intent.

## Versioning and support

- This launcher is protocol-agnostic. It does **not** rev when presence ships new MCP resources; it only revs when its own resolution logic, CLI surface, or `server.json` content changes.
- Tested with presence >= 0.6.0. Older presence versions may still work (the entrypoint `lib/cli.py mcp` has existed since v0.4.1) but are not exercised by CI.
- File launcher-only bugs (path detection, install errors, CLI argument forwarding) on this repo's [issues](https://github.com/sara-star-quant/presence-mcp/issues). File resource-content bugs (what `presence://*/model` returns, telemetry schema, etc.) on the [presence](https://github.com/sara-star-quant/presence/issues) repo.
- Windows: untested in v0.1.0. The launcher uses `subprocess.run` which is cross-platform, but the default presence install path (`~/.claude/plugins/presence/lib/cli.py`) needs a real Windows install to confirm. Report issues if you try it.

## License

MIT. See [LICENSE](./LICENSE).
