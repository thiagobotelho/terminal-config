# terminal-config

Configuração modular e reproduzível de terminal para Fedora, Ubuntu/Debian e
WSL 2.

## Recursos

- Zsh, Oh My Zsh, Powerlevel10k e plugins fixados por commit
- tmux, TPM, Catppuccin, resurrect/continuum, sessionx e módulos de status
- `fzf`, `jq`, `ripgrep`, `bat`, `eza`, `zoxide`, `direnv` e `age`
- Nerd Font baixada de release fixa e validada por SHA256
- módulos opcionais para Alacritty/desktop e Neovim
- backup dos dotfiles antes de substituição
- execução segura de subprocessos, sem `shell=True`

## Requisitos e plataformas

- Python 3.10+
- Fedora com `dnf` ou Ubuntu/Debian com `apt-get`
- Linux nativo ou WSL 2
- Git, HTTPS e `sudo`

Consulte [SUPPORT.md](SUPPORT.md) para a matriz completa.

## Instalação

```bash
git clone https://github.com/thiagobotelho/terminal-config.git
cd terminal-config

# Instalação mínima e compatível com WSL
python3 install.py --profile wsl

# Linux desktop com fonte e Alacritty
python3 install.py --profile desktop

# Desktop, fonte, Alacritty e Neovim
python3 install.py --profile full
```

O padrão é `--profile core`, equivalente ao perfil WSL.

### Perfis e módulos

| Perfil | Módulos | Uso recomendado |
|---|---|---|
| `core` | `core` | servidor, container ou instalação mínima |
| `wsl` | `core` | WSL com Windows Terminal |
| `desktop` | `core`, `fonts`, `desktop` | Linux com interface gráfica |
| `full` | `core`, `fonts`, `desktop`, `neovim` | workstation completa |

| Módulo | Responsabilidade |
|---|---|
| `core` | Zsh, tmux, plugins, dotfiles e utilitários |
| `fonts` | download e instalação verificada da Nerd Font |
| `desktop` | Alacritty e configuração gráfica; ignorado no WSL |
| `neovim` | Neovim, compiladores e `init.vim` |

### Módulos específicos

```bash
python3 install.py --modules core fonts
python3 install.py --list-modules
python3 install.py --profile full --no-set-shell
```

### Dry-run

```bash
python3 install.py --profile full --dry-run
```

O dry-run não instala pacotes, não baixa artefatos e não altera dotfiles.

## Pós-instalação

Abra um terminal novo ou execute:

```bash
exec zsh
```

Verificações rápidas:

```bash
echo "$SHELL"
tmux list-sessions
zoxide --version
direnv version
```

Arquivos existentes recebem backup com sufixo
`.bak-AAAAMMDD-HHMMSS` antes de serem substituídos.

## Reprodutibilidade e fontes

`versions.lock.json` fixa os commits dos projetos Git e a versão/checksum da
fonte. Arquivos TTF/OTF não são armazenados neste repositório. A fonte mantém
sua licença original do projeto Nerd Fonts, indicada no próprio lockfile.

No WSL, configure no Windows Terminal uma Nerd Font Mono, por exemplo
`CaskaydiaCove Nerd Font Mono`.

Para atualizar uma dependência, altere sua versão/commit e checksum em
`versions.lock.json`, execute os testes e revise o dry-run antes da instalação.

## tmux automático

O Zsh abre ou anexa a sessão `main` em terminais reais e ignora o terminal
integrado do VS Code. Para desativar:

```bash
export TERMINAL_CONFIG_AUTO_TMUX=0
```

## Validação

```bash
python3 -m unittest discover -s tests -v
zsh -n setup/zshrc setup/p10k.zsh
```

Releases seguem tags semânticas (`v1.0.0`, `v1.1.0`, ...). Consulte
[CHANGELOG.md](CHANGELOG.md).

## Atualização

```bash
git pull --ff-only
python3 install.py --profile wsl --dry-run
python3 install.py --profile wsl
```

O instalador é idempotente e pode ser reexecutado.

## Solução de problemas

- Não iniciar tmux automaticamente:
  `export TERMINAL_CONFIG_AUTO_TMUX=0`.
- Testar sem trocar o shell padrão: use `--no-set-shell`.
- Listar módulos disponíveis: `python3 install.py --list-modules`.
- Ícones quebrados no WSL: confirme a fonte Nerd Font **Mono** no perfil do
  Windows Terminal e abra uma nova aba.
- Restaurar um dotfile: copie o backup desejado sobre `~/.zshrc`,
  `~/.tmux.conf` ou `~/.p10k.zsh`.

## Remoção

Não há remoção automática para evitar apagar personalizações. Revise e remova
manualmente os dotfiles, `~/custom_modules`, `~/.oh-my-zsh` e
`~/.local/share/tmux/plugins`. Pacotes do sistema devem ser removidos pelo
gerenciador da distribuição.

## Projeto

- Mudanças: [CHANGELOG.md](CHANGELOG.md)
- Contribuição: [CONTRIBUTING.md](CONTRIBUTING.md)
- Plataformas: [SUPPORT.md](SUPPORT.md)
- Licença: [LICENSE](LICENSE)
