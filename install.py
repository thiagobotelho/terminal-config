#!/usr/bin/env python3

import shutil
import subprocess
from pathlib import Path

HOME = Path.home()
SETUP_DIR = Path("setup")
FONTS_DIR = HOME / ".local/share/fonts"
CUSTOM_MODULES_SRC = SETUP_DIR / "custom_modules"
CUSTOM_MODULES_DST = HOME / "custom_modules"
ALACRITTY_CONF_SRC = SETUP_DIR / "alacritty.toml"
ALACRITTY_CONF_DST = HOME / ".config/alacritty/alacritty.toml"

def run(cmd: str, sudo: bool = False, **kwargs):
    print(f"🔧 Executando: {cmd}")
    if sudo:
        cmd = f"sudo {cmd}"
    subprocess.run(cmd, shell=True, check=True, **kwargs)

def is_gnome_terminal_available():
    try:
        output = subprocess.check_output(["gsettings", "list-schemas"]).decode()
        return "org.gnome.Terminal.Legacy.Profile" in output
    except Exception:
        return False

def set_gnome_terminal_font(font_name="SauceCodePro Nerd Font Mono 11"):
    print(f"🕋️ Definindo fonte '{font_name}' no GNOME Terminal...")

    try:
        default_profile = subprocess.check_output([
            "gsettings", "get", "org.gnome.Terminal.ProfilesList", "default"
        ]).decode().strip().strip("'")

        profile_path = f"/org/gnome/terminal/legacy/profiles:/:{default_profile}/"

        subprocess.run([
            "gsettings", "set",
            f"org.gnome.Terminal.Legacy.Profile:{profile_path}",
            "use-system-font", "false"
        ], check=True)

        subprocess.run([
            "gsettings", "set",
            f"org.gnome.Terminal.Legacy.Profile:{profile_path}",
            "font", font_name
        ], check=True)

        print("✅ Fonte aplicada com sucesso no GNOME Terminal.")

    except subprocess.CalledProcessError:
        print("❌ Erro ao aplicar a fonte no GNOME Terminal.")

def install_packages():
    print("📦 Instalando pacotes base (dnf)...")
    run("dnf install -y zsh tmux git curl wget fontconfig fzf alacritty papirus-icon-theme python3-pip", sudo=True)

def install_catppuccin_alacritty_themes():
    print("🎨 Instalando temas Catppuccin para Alacritty...")
    theme_dir = HOME / ".config/alacritty"
    theme_dir.mkdir(parents=True, exist_ok=True)

    themes = [
        "catppuccin-latte.toml",
        "catppuccin-frappe.toml",
        "catppuccin-macchiato.toml",
        "catppuccin-mocha.toml"
    ]

    base_url = "https://github.com/catppuccin/alacritty/raw/main/"

    for theme in themes:
        dest_file = theme_dir / theme
        if not dest_file.exists():
            run(f"curl -LO --output-dir {theme_dir} {base_url}{theme}")
            print(f"✅ Tema baixado: {theme}")
        else:
            print(f"ℹ️ Tema já existe: {theme}")

def install_catppuccin_theme():
    print("🎨 Instalando Catppuccin GTK Theme via install.py...")
    theme_repo = HOME / "catppuccin-gtk"
    theme_variant = "catppuccin-mocha-blue-standard+default"
    theme_dest = HOME / ".local/share/themes" / theme_variant

    if not theme_repo.exists():
        run(f"git clone https://github.com/catppuccin/gtk.git {theme_repo}")

    run(f"pip3 install --user -r {theme_repo}/requirements.txt")
    run("rm -f ~/.config/gtk-4.0/gtk.css")
    run("rm -rf ~/.config/gtk-4.0/assets")

    run(f"python3 {theme_repo}/install.py mocha blue")

    if not theme_dest.exists():
        print(f"❌ Tema compilado não encontrado em: {theme_dest}")
        return

    run("gsettings set org.gnome.desktop.interface gtk-theme 'catppuccin-mocha-blue-standard+dark'")
    run("gsettings set org.gnome.desktop.interface icon-theme 'Papirus-Dark'")

def install_oh_my_zsh():
    print("🌀 Instalando Oh-My-Zsh (modo silencioso)...")
    zsh_dir = HOME / ".oh-my-zsh"

    if not zsh_dir.exists():
        run(f"git clone https://github.com/ohmyzsh/ohmyzsh.git {zsh_dir}")
        run(f"cp {zsh_dir}/templates/zshrc.zsh-template {HOME}/.zshrc")
        print("✅ Oh-My-Zsh instalado e .zshrc aplicado.")

    ssh_dir = HOME / ".ssh"
    if not ssh_dir.exists():
        ssh_dir.mkdir(mode=0o700)
        print("✅ Diretório ~/.ssh criado com permissão 700 (para o ssh-agent).")
    else:
        print("ℹ️ Diretório ~/.ssh já existe.")

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

def install_fonts():
    print("🌤 Instalando fontes Nerd Font...")
    fonts_path = SETUP_DIR / "fonts"
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    for font in fonts_path.glob("*.ttf"):
        shutil.copy(font, FONTS_DIR)
        print(f"✅ Fonte instalada: {font.name}")
    run("fc-cache -fv")

    if is_gnome_terminal_available():
        set_gnome_terminal_font("SauceCodePro Nerd Font Mono 11")
    else:
        print("⚠️ GNOME Terminal não disponível ou sessão gráfica ausente. Fonte não aplicada.")

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
        
def install_tpm():
    print("🔧 Instalando TPM (Tmux Plugin Manager)...")
    tpm_dir = HOME / ".tmux/plugins/tpm"

    if not tpm_dir.exists():
        subprocess.run(f"git clone https://github.com/tmux-plugins/tpm {tpm_dir}", shell=True, check=True)

    tmux_conf = HOME / ".tmux.conf"
    if not tmux_conf.exists():
        print("❌ Arquivo ~/.tmux.conf não encontrado. Abortando configuração do TPM.")
        return

    print("📂 Aplicando configuração do tmux.conf em sessão temporária...")
    subprocess.run("tmux new-session -d -s temp-tpm-session", shell=True, check=True)
    subprocess.run("tmux source-file ~/.tmux.conf", shell=True, check=True)
    subprocess.run("tmux kill-session -t temp-tpm-session", shell=True, check=True)

    print("🔌 Instalando plugins do TPM...")
    subprocess.run(f"{tpm_dir}/bin/install_plugins", shell=True, check=True)

def configure_alacritty():
    print("📁 Configurando Alacritty com tema e fonte...")
    ALACRITTY_CONF_DST.parent.mkdir(parents=True, exist_ok=True)

    if ALACRITTY_CONF_SRC.exists():
        # Leitura do conteúdo original
        content = ALACRITTY_CONF_SRC.read_text()

        if 'import =' in content and '[general]' not in content:
            print("🔧 Corrigindo sintaxe de 'import' no alacritty.toml...")
            lines = content.splitlines()
            new_lines = []
            inside_header = False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('import'):
                    new_lines.append('[general]')
                new_lines.append(line)
            content = '\n'.join(new_lines)

        ALACRITTY_CONF_DST.write_text(content)
        print(f"✅ alacritty.toml copiado e ajustado para {ALACRITTY_CONF_DST}")
    else:
        print("⚠️ alacritty.toml não encontrado no diretório setup.")

def set_default_shell():
    print("🖥️ Definindo ZSH como shell padrão (via sudo)...")
    zsh_path = shutil.which("zsh")
    if zsh_path:
        run(f"chsh -s {zsh_path} $(whoami)", sudo=True)
    else:
        print("❌ ZSH não encontrado no PATH.")

if __name__ == "__main__":
    install_packages()
    install_catppuccin_alacritty_themes()
    install_catppuccin_theme()
    install_oh_my_zsh()
    install_oh_my_zsh_plugins()
    install_powerlevel10k()
    copy_configs()
    install_fonts()
    install_tpm()
    configure_alacritty()
    set_default_shell()
    print("✅ Ambiente de terminal configurado com sucesso.")
