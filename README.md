# Descrição
Repositório de automação para configurar rapidamente o ambiente de terminal no Fedora Linux com ZSH, TMUX e fontes Nerd Font, incluindo temas e plugins.  Utiliza um script em Python 3 para instalação automática de dependências, cópia dos dotfiles e configuração do ambiente. Ideal para pós-instalação, formatação ou padronização de máquinas DevOps.

# ⚙️ terminal-config

Repositório de automação para configurar rapidamente o terminal com:

- ZSH (com Powerlevel10k)
- TMUX (com TPM)
- Fontes Nerd Font
- Scripts automatizados em Python

## 🚀 Instalação

```bash
sudo dnf install git python3 -y
git clone https://github.com/thiagobotelho/terminal-config.git
cd terminal-config
python3 install.py
