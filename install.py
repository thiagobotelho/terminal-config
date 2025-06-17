#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path

HOME = Path.home()
SETUP_DIR = Path("setup")
FONTS_DIR = HOME / ".local/share/fonts"

def run(cmd: str):
    print(f"🔧 Executando: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def install_packages():
    print("📦 Instalando pacotes...")
    run("sudo dnf install -y zsh tmux git curl wget fontconfig")

def copy_configs():
    print("📁 Copiando arquivos de configuração...")
    shutil.copy(SETUP_DIR / "zshrc", HOME / ".zshrc")
    shutil.copy(SETUP_DIR / "p10k.zsh", HOME / ".p10k.zsh")
    shutil.copy(SETUP_DIR / "tmux.conf", HOME / ".tmux.conf")

def install_fonts():
    fonts_path = SETUP_DIR / "fonts"
    print("🔤 Instalando fontes SauceCodePro Nerd Font...")

    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    for font in fonts_path.glob("*.ttf"):
        shutil.copy(font, FONTS_DIR)
        print(f"✅ Fonte instalada: {font.name}")
    run("fc-cache -fv")

def install_tpm():
    print("🔌 Instalando TPM (Tmux Plugin Manager)...")
    tpm_dir = HOME / ".tmux/plugins/tpm"
    if not tpm_dir.exists():
        run(f"git clone https://github.com/tmux-plugins/tpm {tpm_dir}")
    run(f"{tpm_dir}/bin/install_plugins")

if __name__ == "__main__":
    install_packages()
    copy_configs()
    install_fonts()
    install_tpm()
    print("✅ Ambiente de terminal configurado com sucesso.")