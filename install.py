#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path

HOME = Path.home()
SETUP_DIR = Path("setup")
FONTS_DIR = HOME / ".local/share/fonts"
CUSTOM_MODULES_SRC = SETUP_DIR / "custom_modules"
CUSTOM_MODULES_DST = HOME / "custom_modules"

def run(cmd: str):
    print(f"🔧 Executando: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def install_packages():
    print("📦 Instalando pacotes base (dnf)...")
    run("sudo dnf install -y zsh tmux git curl wget fontconfig fzf alacritty papirus-icon-theme")

def install_catppuccin_theme():
    print("🎨 Instalando Catppuccin GTK Theme manualmente...")
    theme_repo = HOME / "catppuccin-gtk"
    theme_dest = HOME / ".themes"
    theme_name = "Catppuccin-Mocha-Standard-Blue-Dark"

    if not theme_repo.exists():
        run(f"git clone https://github.com/catppuccin/gtk.git {theme_repo}")

    src_theme_path = theme_repo / "themes" / theme_name
    dest_theme_path = theme_dest / theme_name

    if not src_theme_path.exists():
        print(f"❌ Tema não encontrado em: {src_theme_path}")
        return

    theme_dest.mkdir(parents=True, exist_ok=True)
    if not dest_theme_path.exists():
        shutil.copytree(src_theme_path, dest_theme_path)
        print(f"✅ Tema copiado: {theme_name}")

    print("🎨 Aplicando tema Catppuccin + ícones Papirus...")
    run(f"gsettings set org.gnome.desktop.interface gtk-theme '{theme_name}'")
    run("gsettings set org.gnome.desktop.interface icon-theme 'Papirus-Dark'")

def install_oh_my_zsh():
    print("🌀 Instalando Oh-My-Zsh (modo silencioso)...")
    zsh_dir = HOME / ".oh-my-zsh"
    if not zsh_dir.exists():
        run(f"git clone https://github.com/ohmyzsh/ohmyzsh.git {zsh_dir}")
        run(f"cp {zsh_dir}/templates/zshrc.zsh-template {HOME}/.zshrc")

def install_oh_my_zsh_plugins():
    print("🔌 Instalando plugins do Oh-My-Zsh...")
    custom_plugins = HOME / ".oh-my-zsh/custom/plugins"
    plugins = {
        "zsh-autosuggestions": "https://github.com/zsh-users/zsh-autosuggestions.git",
        "zsh-syntax-highlighting": "https://github.com/zsh-users/zsh-syntax-highlighting.git",
        "zsh-history-substring-search": "https://github.com/zsh-users/zsh-history-substring-search.git",
        "zsh-fzf-history-search": "https://github.com/joshskidmore/zsh-fzf-history-search.git"
    }
    for name, repo in plugins.items():
        dest = custom_plugins / name
        if not dest.exists():
            run(f"git clone {repo} {dest}")

def install_powerlevel10k():
    print("🎨 Instalando tema Powerlevel10k...")
    theme_path = HOME / ".oh-my-zsh/custom/themes/powerlevel10k"
    if not theme_path.exists():
        run(f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git {theme_path}")

def install_tpm():
    print("🔌 Instalando TPM (Tmux Plugin Manager)...")
    tpm_dir = HOME / ".tmux/plugins/tpm"
    if not tpm_dir.exists():
        run(f"git clone https://github.com/tmux-plugins/tpm {tpm_dir}")
    run(f"{tpm_dir}/bin/install_plugins")

def install_fonts():
    print("🔤 Instalando fontes Nerd Font...")
    fonts_path = SETUP_DIR / "fonts"
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    for font in fonts_path.glob("*.ttf"):
        shutil.copy(font, FONTS_DIR)
        print(f"✅ Fonte instalada: {font.name}")
    run("fc-cache -fv")

def copy_configs():
    print("📁 Copiando arquivos de configuração...")
    for file_name in ["zshrc", "p10k.zsh", "tmux.conf"]:
        src = SETUP_DIR / file_name
        dest = HOME / f".{file_name}"
        if src.exists():
            shutil.copy(src, dest)
        else:
            print(f"⚠️ Arquivo não encontrado: {file_name}")

    print("📁 Copiando módulos customizados do tmux...")
    if CUSTOM_MODULES_SRC.exists():
        CUSTOM_MODULES_DST.mkdir(parents=True, exist_ok=True)
        for file in CUSTOM_MODULES_SRC.glob("*.conf"):
            shutil.copy(file, CUSTOM_MODULES_DST)
            print(f"✅ Copiado: {file.name}")
    else:
        print("⚠️ Diretório de módulos customizados não encontrado.")

def set_default_shell():
    print("🖥️ Definindo ZSH como shell padrão (via sudo)...")
    zsh_path = shutil.which("zsh")
    if zsh_path:
        run(f"sudo chsh -s {zsh_path} $(whoami)")
    else:
        print("❌ ZSH não encontrado no PATH.")

def configure_alacritty():
    print("📁 Configurando Alacritty com tema e fonte...")
    config_dir = HOME / ".config" / "alacritty"
    config_dir.mkdir(parents=True, exist_ok=True)

    source_toml = SETUP_DIR / "alacritty.toml"
    target_toml = config_dir / "alacritty.toml"

    if source_toml.exists():
        shutil.copy(source_toml, target_toml)
        print(f"✅ alacritty.toml copiado para {target_toml}")
    else:
        print("❌ Arquivo setup/alacritty.toml não encontrado!")

if __name__ == "__main__":
    install_packages()
    install_catppuccin_theme()
    install_oh_my_zsh()
    install_oh_my_zsh_plugins()
    install_powerlevel10k()
    copy_configs()
    install_fonts()
    install_tpm()
    set_default_shell()
    configure_alacritty()
    print("✅ Ambiente de terminal configurado com sucesso.")
