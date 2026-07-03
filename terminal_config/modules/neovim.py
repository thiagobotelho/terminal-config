from __future__ import annotations

from ..context import Context


def install(ctx: Context, *, set_shell: bool = True) -> None:
    del set_shell
    print("📝 Módulo neovim")
    ctx.install_packages(["neovim", "gcc", "gcc-c++", "make"], ["neovim", "gcc", "g++", "make"])
    ctx.deploy(ctx.root / "setup/init.vim", ctx.home / ".config/nvim/init.vim")
