
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
    run("sudo dnf install -y zsh tmux git curl wget fontconfig")

def install_oh_my_zsh():
    print("🌀 Instalando Oh-My-Zsh...")
    zsh_path = HOME / ".oh-my-zsh"
    if not zsh_path.exists():
        run("sh -c \"$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\"")

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
    shutil.copy(SETUP_DIR / "zshrc", HOME / ".zshrc")
    shutil.copy(SETUP_DIR / "p10k.zsh", HOME / ".p10k.zsh")
    shutil.copy(SETUP_DIR / "tmux.conf", HOME / ".tmux.conf")
    
    print("📁 Copiando módulos customizados do tmux...")
    CUSTOM_MODULES_DST.mkdir(parents=True, exist_ok=True)
    for file in CUSTOM_MODULES_SRC.glob("*.conf"):
        shutil.copy(file, CUSTOM_MODULES_DST)
        print(f"✅ Copiado: {file.name}")

def set_default_shell():
    print("🖥️ Definindo ZSH como shell padrão...")
    zsh_path = shutil.which("zsh")
    if zsh_path:
        run(f"chsh -s {zsh_path}")

if __name__ == "__main__":
    install_packages()
    install_oh_my_zsh()
    install_powerlevel10k()
    copy_configs()
    install_fonts()
    install_tpm()
    set_default_shell()
    print("✅ Ambiente de terminal configurado com sucesso.")