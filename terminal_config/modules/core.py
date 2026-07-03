from __future__ import annotations

import getpass
import os
import shutil

from ..context import Context


FEDORA_PACKAGES = [
    "zsh", "tmux", "git", "curl", "wget", "fontconfig", "fzf", "gawk",
    "jq", "ripgrep", "bat", "eza", "zoxide", "direnv", "age",
]
DEBIAN_PACKAGES = [
    "zsh", "tmux", "git", "curl", "wget", "fontconfig", "fzf", "gawk",
    "jq", "ripgrep", "bat", "zoxide", "direnv", "age",
]

ZSH_PLUGINS = {
    "zsh-autosuggestions": "zsh-autosuggestions",
    "zsh-syntax-highlighting": "zsh-syntax-highlighting",
    "zsh-history-substring-search": "zsh-history-substring-search",
    "zsh-fzf-history-search": "zsh-fzf-history-search",
}


def install(ctx: Context, *, set_shell: bool = True) -> None:
    print("📦 Módulo core")
    ctx.install_packages(FEDORA_PACKAGES, DEBIAN_PACKAGES)
    if ctx.package_manager == "apt":
        ctx.runner.run(["apt-get", "install", "-y", "eza"], sudo=True, check=False)
        batcat = shutil.which("batcat")
        bat = ctx.home / ".local/bin/bat"
        if batcat and not bat.exists() and not ctx.runner.dry_run:
            bat.parent.mkdir(parents=True, exist_ok=True)
            bat.symlink_to(batcat)

    omz = ctx.home / ".oh-my-zsh"
    ctx.clone_locked("oh-my-zsh", omz)
    ctx.clone_locked("powerlevel10k", omz / "custom/themes/powerlevel10k")
    for directory, lock_name in ZSH_PLUGINS.items():
        ctx.clone_locked(lock_name, omz / "custom/plugins" / directory)

    setup = ctx.root / "setup"
    for source_name, destination_name in (
        ("zshrc", ".zshrc"),
        ("p10k.zsh", ".p10k.zsh"),
        ("tmux.conf", ".tmux.conf"),
    ):
        ctx.deploy(setup / source_name, ctx.home / destination_name)

    modules = ctx.home / "custom_modules"
    for source in (setup / "custom_modules").glob("*.conf"):
        ctx.deploy(source, modules / source.name)

    tpm = ctx.home / ".local/share/tmux/plugins/tpm"
    ctx.clone_locked("tpm", tpm)
    env = os.environ.copy()
    native = f"{ctx.home}/.local/bin:{ctx.home}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    env["PATH"] = f"{native}:{env.get('PATH', '')}"
    if ctx.runner.dry_run:
        print(f"🔌 {tpm}/bin/install_plugins")
    else:
        import subprocess
        subprocess.run([str(tpm / "bin/install_plugins")], check=True, env=env)

    if set_shell and shutil.which("zsh"):
        user = os.environ.get("SUDO_USER") or os.environ.get("USER") or getpass.getuser()
        shell = shutil.which("zsh")
        ctx.runner.run(["chsh", "-s", shell, user], sudo=True)
