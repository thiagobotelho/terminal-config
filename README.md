# 🧰 terminal-config

Automação completa para configurar seu terminal Linux (Fedora) com ZSH, TMUX, Nerd Font e plugins essenciais.

> 📌 Ideal para pós-instalação, formatação ou padronização de ambientes DevOps.

---

## 📄 Descrição

Repositório de automação para configurar rapidamente o ambiente de terminal no **Fedora Linux**, utilizando:

- **ZSH** com tema **Powerlevel10k**
- **TMUX** com **TPM (Tmux Plugin Manager)**
- **Fontes Nerd Font** compatíveis com o terminal
- **Scripts em Python 3** para instalação automatizada de dependências e cópia dos dotfiles

---

## ⚙️ Recursos

✅ Instalação automatizada via `install.py`  
✅ Suporte a Powerlevel10k e TPM  
✅ Fontes personalizadas para terminais compatíveis  
✅ Reutilização rápida do ambiente em novos setups  

---

## 🚀 Instalação

```bash
sudo dnf install git python3 -y
git clone https://github.com/thiagobotelho/terminal-config.git
cd terminal-config
python3 install.py
