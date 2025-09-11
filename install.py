#!/usr/bin/env python3

import shutil
import subprocess
import getpass
import os
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

    run("gsettings set org.gnome.desktop.interface gtk-theme 'catppuccin-mocha-blue-standard+default'")
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

def install_alacritty_theme_pack():
    """
    Baixa os temas oficiais do Alacritty (inclui gruvbox_dark.toml) no caminho:
    ~/.config/alacritty/themes/themes/<nome_do_tema>.toml
    """
    print("🎨 Baixando pack oficial de temas do Alacritty (gruvbox, etc.)...")
    themes_root = HOME / ".config/alacritty"
    repo_dir = themes_root / "themes"
    themes_root.mkdir(parents=True, exist_ok=True)

    if not repo_dir.exists():
        run(f"git clone https://github.com/alacritty/alacritty-theme {repo_dir}")
        print("✅ Pacote de temas clonado.")
    else:
        print("ℹ️ Repositório de temas já existe, atualizando (git pull)...")
        run(f"git -C {repo_dir} pull --ff-only")
        print("✅ Pacote de temas atualizado.")

def configure_alacritty():
    print("📁 Configurando Alacritty com tema e fonte...")
    ALACRITTY_CONF_DST.parent.mkdir(parents=True, exist_ok=True)

    if ALACRITTY_CONF_SRC.exists():
        content = ALACRITTY_CONF_SRC.read_text()

        if 'import =' in content and '[general]' not in content:
            print("🔧 Corrigindo sintaxe de 'import' no alacritty.toml...")
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('import'):
                    new_lines.append('[general]')
                new_lines.append(line)
            content = '\n'.join(new_lines)

        ALACRITTY_CONF_DST.write_text(content)
        print(f"✅ alacritty.toml copiado e ajustado para {ALACRITTY_CONF_DST}")

        # Checagem defensiva do(s) caminho(s) importado(s)
        try:
            from tomllib import loads as toml_loads  # Python 3.11+
        except Exception:
            toml_loads = None

        if toml_loads:
            try:
                cfg = toml_loads(content)
                imports = cfg.get("general", {}).get("import", [])
                if isinstance(imports, str):
                    imports = [imports]
                missing = []
                for i in imports:
                    p = Path(i.replace("~", str(HOME)))
                    if not p.exists():
                        missing.append(i)
                if missing:
                    print(f"⚠️ Atenção: os seguintes imports não foram encontrados: {missing}")
                    print("   Verifique se o pack de temas foi baixado corretamente.")
            except Exception:
                # Se parsing falhar, apenas segue.
                pass
    else:
        print("⚠️ alacritty.toml não encontrado no diretório setup.")

def install_nvim_and_plugins():
    print("📝 Instalando vim-plug e provisionando plugins do Neovim...")

    # Caminhos
    nvim_config = HOME / ".config" / "nvim"
    nvim_data = HOME / ".local" / "share" / "nvim"
    plug_vim = nvim_data / "site" / "autoload" / "plug.vim"
    init_vim_src = SETUP_DIR / "init.vim"
    init_vim_dst = nvim_config / "init.vim"

    # Cria pasta de configuração do Neovim
    nvim_config.mkdir(parents=True, exist_ok=True)

    # Instala vim-plug se não existir
    if not plug_vim.exists():
        run(
            "curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs "
            "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
        )
        print("✅ vim-plug instalado.")
    else:
        print("ℹ️ vim-plug já está presente.")

    # Copia init.vim do repositório (setup/)
    if init_vim_src.exists():
        shutil.copy(init_vim_src, init_vim_dst)
        print(f"✅ init.vim copiado de {init_vim_src} para {init_vim_dst}")
    else:
        print("⚠️ init.vim não encontrado na pasta setup.")

    # Instala pacotes de build necessários para Treesitter
    run("dnf install -y gcc gcc-c++ make unzip tar", sudo=True)

    # Executa PlugInstall + TSUpdate headless
    try:
        run("nvim --headless +PlugInstall +qall")
        run("nvim --headless +TSUpdate +qall")
        print("✅ Plugins do Neovim instalados e Treesitter atualizado.")
    except Exception:
        print("⚠️ Não consegui rodar PlugInstall/TSUpdate. Execute manualmente dentro do nvim.")

def set_default_shell():
    print("🖥️ Definindo ZSH como shell padrão (via sudo)...")
    zsh_path = shutil.which("zsh")
    if not zsh_path:
        print("❌ ZSH não encontrado no PATH.")
        return

    # Descobre o usuário-alvo de forma robusta (mesmo sob sudo)
    target_user = os.environ.get("SUDO_USER") or os.environ.get("USER") or getpass.getuser()

    # Garante que o shell está listado em /etc/shells (exigência do chsh)
    try:
        shells = subprocess.check_output("cat /etc/shells", shell=True).decode()
    except subprocess.CalledProcessError:
        shells = ""
    if zsh_path not in shells.splitlines():
        print(f"ℹ️  {zsh_path} não consta em /etc/shells. Registrando...")
        run(f"bash -lc \"echo '{zsh_path}' | sudo tee -a /etc/shells >/dev/null\"", sudo=False)

    # Aplica mudança para o usuário correto
    run(f"chsh -s {zsh_path} {target_user}", sudo=True)

    # Valida no /etc/passwd se consolidou
    entry = subprocess.check_output(f"getent passwd {target_user}", shell=True).decode().strip()
    new_shell = entry.split(":")[-1] if ":" in entry else ""
    if new_shell == zsh_path:
        print(f"✅ Shell padrão alterado para {zsh_path} para o usuário {target_user}.")
        print("ℹ️ Abra uma nova sessão (logout/login) ou um novo terminal para refletir em $SHELL.")
    else:
        print(f"⚠️ Shell não alterado. Atual: {new_shell or 'desconhecido'}. Verifique políticas PAM/SSSD.")

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
    install_alacritty_theme_pack() 
    configure_alacritty()
    install_nvim_and_plugins()
    set_default_shell()
    print("✅ Ambiente de terminal configurado com sucesso.")
