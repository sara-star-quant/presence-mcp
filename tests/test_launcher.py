from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from presence_mcp import launcher


def _make_fake_presence(root: Path) -> Path:
    cli = root / ".claude" / "plugins" / "presence" / "lib" / "cli.py"
    cli.parent.mkdir(parents=True)
    cli.write_text("# fake presence cli for tests\n")
    return cli


def test_env_var_takes_precedence_over_default(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    default_cli = _make_fake_presence(home)

    override_cli = tmp_path / "elsewhere" / "cli.py"
    override_cli.parent.mkdir()
    override_cli.write_text("# override\n")

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("PRESENCE_MCP_CLI", str(override_cli))

    resolved = launcher._resolve_presence_cli()
    assert resolved == override_cli
    assert resolved != default_cli


def test_default_path_used_when_env_unset(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    expected = _make_fake_presence(home)

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("PRESENCE_MCP_CLI", raising=False)

    assert launcher._resolve_presence_cli() == expected


def test_missing_presence_raises_with_install_hint(tmp_path, monkeypatch, capsys):
    home = tmp_path / "home"
    home.mkdir()  # no presence install inside

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("PRESENCE_MCP_CLI", raising=False)

    with pytest.raises(LookupError) as exc_info:
        launcher._resolve_presence_cli()
    assert "plugin" in str(exc_info.value).lower()

    monkeypatch.setattr(sys, "argv", ["presence-mcp"])
    with pytest.raises(SystemExit) as sysexit:
        launcher.main()
    assert sysexit.value.code == 1
    captured = capsys.readouterr()
    assert "plugin" in captured.err.lower()


def test_env_var_pointing_at_missing_file_raises(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    _make_fake_presence(home)  # default exists, to prove we do NOT fall back

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("PRESENCE_MCP_CLI", str(tmp_path / "does-not-exist.py"))

    with pytest.raises(LookupError, match="is set but no file exists"):
        launcher._resolve_presence_cli()


def test_main_spawns_subprocess_with_correct_args(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    cli = _make_fake_presence(home)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("PRESENCE_MCP_CLI", raising=False)

    calls: list[list[str]] = []

    def fake_run(cmd, check):
        calls.append(list(cmd))
        return subprocess.CompletedProcess(args=cmd, returncode=0)

    monkeypatch.setattr(launcher.subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["presence-mcp"])

    with pytest.raises(SystemExit) as sysexit:
        launcher.main()

    assert sysexit.value.code == 0
    assert calls == [[sys.executable, str(cli), "mcp"]]


def test_python_override_env_var(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    cli = _make_fake_presence(home)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("PRESENCE_MCP_CLI", raising=False)
    monkeypatch.setenv("PRESENCE_MCP_PYTHON", "/custom/python3")

    calls: list[list[str]] = []

    def fake_run(cmd, check):
        calls.append(list(cmd))
        return subprocess.CompletedProcess(args=cmd, returncode=0)

    monkeypatch.setattr(launcher.subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["presence-mcp"])

    with pytest.raises(SystemExit):
        launcher.main()

    assert calls == [["/custom/python3", str(cli), "mcp"]]


def test_main_forwards_nonzero_exit_code(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    _make_fake_presence(home)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("PRESENCE_MCP_CLI", raising=False)

    def fake_run(cmd, check):
        return subprocess.CompletedProcess(args=cmd, returncode=7)

    monkeypatch.setattr(launcher.subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["presence-mcp"])

    with pytest.raises(SystemExit) as sysexit:
        launcher.main()

    assert sysexit.value.code == 7
