from __future__ import annotations

import argparse
import importlib
from pathlib import Path

from .context import load_context
from .modules import MODULES


PROFILES = {
    "core": ("core",),
    "wsl": ("core",),
    "desktop": ("core", "fonts", "desktop"),
    "full": ("core", "fonts", "desktop", "neovim"),
}


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description="Configura terminal Linux/WSL")
    command.add_argument("--profile", choices=PROFILES, default="core")
    command.add_argument("--modules", nargs="+", choices=MODULES)
    command.add_argument("--dry-run", action="store_true")
    command.add_argument("--no-set-shell", action="store_true")
    command.add_argument("--list-modules", action="store_true")
    return command


def main(argv: list[str] | None = None) -> None:
    args = parser().parse_args(argv)
    if args.list_modules:
        print("\n".join(MODULES))
        return

    root = Path(__file__).resolve().parents[1]
    ctx = load_context(root, args.dry_run)
    selected = tuple(args.modules or PROFILES[args.profile])
    for name in selected:
        module = importlib.import_module(f"terminal_config.modules.{name}")
        module.install(ctx, set_shell=not args.no_set_shell)
    print(f"✅ Módulos concluídos: {', '.join(selected)}")
