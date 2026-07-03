from __future__ import annotations

from ..context import Context


def install(ctx: Context, *, set_shell: bool = True) -> None:
    del set_shell
    if ctx.is_wsl:
        print("🪟 WSL detectado: módulo desktop ignorado")
        return
    print("🖥️ Módulo desktop")
    ctx.install_packages(
        ["alacritty", "papirus-icon-theme"],
        ["alacritty", "papirus-icon-theme"],
    )
    ctx.deploy(
        ctx.root / "setup/alacritty.toml",
        ctx.home / ".config/alacritty/alacritty.toml",
    )
