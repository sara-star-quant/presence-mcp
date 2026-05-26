# Changelog

All notable changes to `presence-mcp` are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0]

Initial release. Thin launcher that locates a local [presence](https://github.com/sara-star-quant/presence) install and forwards stdio to `python lib/cli.py mcp`, so the presence MCP server can be listed in the official MCP Registry at https://github.com/mcp.

### Added

- `presence-mcp` console script and `python -m presence_mcp` entry point.
- Resolver looks up `$PRESENCE_MCP_CLI`, then falls back to `~/.claude/plugins/presence/lib/cli.py`.
- `$PRESENCE_MCP_PYTHON` override for the interpreter (defaults to `sys.executable`).
- Clear stderr install-hint when presence is not found.
- MIT licensed.
- CI on Python 3.12 / 3.13 / 3.14 across Linux and macOS.

### Known limitations

- Windows is untested.
- Tested against presence >= 0.6.0.
