# Nine Kings — Guia de Builds

Guia comunitário em português com builds para os nove reis de **Nine Kings**, descrições de cartas, sinergias e sugestões de posicionamento.

## Estrutura

```text
nine-kings-builds/
├── index.html        # Estrutura semântica e conteúdo inicial
├── css/
│   └── style.css     # Layout responsivo e temas claro/escuro
├── js/
│   └── main.js       # Dados das builds, pesquisa, filtros e visualização
└── README.md         # Documentação
```

## Como executar

Abra `index.html` em um navegador moderno. Não há dependências, build ou servidor obrigatório.

## Funcionalidades

- Nove builds com descrição dos efeitos e sinergias;
- imagens originais das cartas e reis armazenadas em `assets/cards/` e `assets/kings/`;
- pesquisa por rei ou carta e filtro de tipo;
- zoom das imagens e alternância de tema;
- layout responsivo.

## Publicação no GitHub Pages

Em **Settings → Pages**, selecione **Deploy from a branch** e configure `main` / `/(root)`.

Site: https://bruno-trindade85.github.io/nine-kings-builds/

## Fontes e observações

As imagens originais foram extraídas da Wiki oficial da Hooded Horse e são servidas localmente. A origem e a verificação de cada download estão em `assets/manifest.json`; o resumo está em `assets/REPORT.md`. Para atualizar, execute `python scripts/download_assets.py`. Os nomes e efeitos podem mudar com atualizações do jogo. O guia não é afiliado aos criadores de Nine Kings.

- [9 Kings Wiki](https://9kings.wiki.gg/)
- [Nine Kings na Steam](https://store.steampowered.com/app/2784470/9_Kings/)
