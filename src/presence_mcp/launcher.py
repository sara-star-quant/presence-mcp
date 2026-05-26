"""Launcher for the presence MCP server.

Locates a presence install on the local machine and runs its built-in MCP server (`lib/cli.py mcp`), forwarding stdio.
This package speaks no MCP itself; it exists so that the presence MCP server can be listed in the official MCP Registry, which requires an artifact on a supported package registry (PyPI here).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ENV_VAR = "PRESENCE_MCP_CLI"
ENV_PYTHON = "PRESENCE_MCP_PYTHON"
DEFAULT_RELATIVE = Path(".claude/plugins/presence/lib/cli.py")

_INSTALL_HINT = """\
presence-mcp: could not locate the presence MCP server.

Tried:
  - ${env_var} env var: (unset)
  - default: {default}

Install presence as a Claude Code plugin (https://github.com/sara-star-quant/presence),
or set {env_var} to the absolute path of presence's lib/cli.py.
"""


def _resolve_presence_cli() -> Path:
    """Return the path to presence's cli.py, or raise LookupError.

    Resolution order:
      1. $PRESENCE_MCP_CLI if set. If set but the file is missing, raise rather than falling back; an explicit override that points at a typo should surface, not be silently ignored.
      2. ~/.claude/plugins/presence/lib/cli.py.
    """
    env_val = os.environ.get(ENV_VAR)
    if env_val:
        candidate = Path(env_val).expanduser()
        if candidate.is_file():
            return candidate
        raise LookupError(f"{ENV_VAR}={env_val!r} is set but no file exists at that path.")

    default = Path.home() / DEFAULT_RELATIVE
    if default.is_file():
        return default

    raise LookupError(_INSTALL_HINT.format(env_var=ENV_VAR, default=default))


def main() -> None:
    try:
        cli_path = _resolve_presence_cli()
    except LookupError as exc:
        print(str(exc), file=sys.stderr, end="")
        sys.exit(1)

    python = os.environ.get(ENV_PYTHON) or sys.executable
    result = subprocess.run(
        [python, str(cli_path), "mcp"],
        check=False,
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
