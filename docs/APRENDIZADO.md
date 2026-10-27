# Terminal reproduzível

## O que observar

Leia versões fixadas, módulos e execução segura. Antes de aplicar, use o modo de simulação; confira backups .bak-* gerados ao substituir dotfiles. Para restaurar, compare o backup e recoloque apenas o arquivo escolhido, preservando mudanças locais. Teste Bash/Zsh, Fedora e WSL em ambientes descartáveis; um runner Ubuntu não prova integração em todos os sistemas.

## Roteiro de leitura e validação

1. Leia o README e identifique o componente que recebe a configuração.
2. Confira namespaces, seletores, portas, identidades e dependências nos exemplos.
3. Ajuste apenas os campos necessários em um ambiente isolado; não use credenciais de produção.
4. Valide sintaxe e contratos locais antes de aplicar. Registre o resultado real separado deste guia.
5. Execute um caso permitido e um caso negado, conferindo a causa da resposta.
6. Defina reversão por recurso/arquivo e preserve dados persistentes antes de mudanças.

Os comentários dos manifests explicam escolhas; não comprovam disponibilidade do componente. Exemplos fora de entradas Kustomize não são implantados automaticamente.
