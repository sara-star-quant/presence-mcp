"""Assert that server.json's versions match presence_mcp.__version__.

The package version lives in src/presence_mcp/__init__.py and is exposed via hatch-version dynamic metadata.
server.json declares both a top-level `version` (the registry listing version) and a `packages[0].version` (the PyPI package version).
All three must agree at release time, or the registry will reject the publish or list the wrong artifact.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from presence_mcp import __version__ as pkg_version  # noqa: E402

server_json = json.loads((ROOT / "server.json").read_text())
server_version = server_json["version"]
package_version = server_json["packages"][0]["version"]

mismatches = []
if server_version != pkg_version:
    mismatches.append(f"server.json#version = {server_version!r}, expected {pkg_version!r}")
if package_version != pkg_version:
    mismatches.append(
        f"server.json#packages[0].version = {package_version!r}, expected {pkg_version!r}"
    )

if mismatches:
    print("Version mismatch:", file=sys.stderr)
    for m in mismatches:
        print(f"  {m}", file=sys.stderr)
    sys.exit(1)

print(f"OK: all versions agree on {pkg_version!r}")
