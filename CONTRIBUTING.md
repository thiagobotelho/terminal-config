# Contribuindo

1. Crie uma branch a partir de `main`.
2. Mantenha instalação idempotente e compatibilidade Python 3.10+.
3. Não adicione binários, fontes ou segredos ao Git.
4. Atualize `versions.lock.json` somente com origem e checksum verificáveis.
5. Execute:

```bash
python3 -m unittest discover -s tests -v
zsh -n setup/zshrc setup/p10k.zsh
python3 install.py --profile wsl --dry-run
```

Descreva no pull request as distribuições testadas e qualquer alteração em
arquivos do usuário.
