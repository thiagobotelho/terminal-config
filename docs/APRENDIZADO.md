# Terminal reproduzível


Leia versões fixadas, módulos e execução segura. Antes de aplicar, use o modo de simulação; confira backups .bak-* gerados ao substituir dotfiles. Para restaurar, compare o backup e recoloque apenas o arquivo escolhido, preservando mudanças locais. Teste Bash/Zsh, Fedora e WSL em ambientes descartáveis; um runner Ubuntu não prova integração em todos os sistemas.

## Responsabilidade dos componentes

Os módulos alteram arquivos do usuário e ferramentas do terminal. Login, contexto Kubernetes e permissões do cluster pertencem ao oc e ao servidor. Para comparar comportamento entre terminal nativo, WSL e ambiente isolado, confira PATH e executável resolvido antes de reinstalar pacotes ou substituir dotfiles.
