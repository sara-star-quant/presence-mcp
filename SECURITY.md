# Security policy

## Reporting

Report suspected vulnerabilities privately via GitHub's Security Advisories on this repository ("Report a vulnerability" tab), not in public issues.

## Scope

This package is a thin process launcher: it locates a local presence install and spawns `python lib/cli.py mcp`. It performs no network I/O, holds no secrets, and writes no files.

In scope:

- Path-handling bugs in the resolver (`_resolve_presence_cli`) that could cause execution of an unintended binary.
- Argument-forwarding bugs that could let a caller influence what runs.
- Logic that could let the launcher run when presence is absent and silently do something unexpected.

Out of scope (report to [presence](https://github.com/sara-star-quant/presence)):

- Anything about what the presence MCP server itself returns.
- Bugs in resource content, telemetry, encryption, or the underlying daemon.

## Supported versions

Only the latest released version receives security fixes.
