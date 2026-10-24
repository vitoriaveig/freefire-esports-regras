# Regulamentos de esports de Free Fire: acervo curado para pesquisa

Acervo de pesquisa com o **catálogo**, a **procedência** e o **texto extraído** de regulamentos de esports
de Free Fire (Garena): Free Fire World Series (FFWS) e suas regiões, circuitos nacionais, Esports World Cup,
circuitos de terceiros e políticas da plataforma. Inclui uma **camada comparativa** com os corpora da
[Riot Games](https://github.com/vitoriaveig/riot-esports-regras) e da
[Valve](https://github.com/ValveSoftware/counter-strike_rules_and_regs).

Acompanha a skill `freefire-esports-regras` (cópia em [`skill/SKILL.md`](skill/SKILL.md)).

## Por que um acervo curado

Ao contrário da Riot, que mantém uma
[Biblioteca de Operações Competitivas](https://competitiveops.riotgames.com/pt-BR/library), e da Valve, que
publica as regras em um repositório no GitHub, **a Garena não mantém um acervo público centralizado** de
regulamentos. Os documentos circulam de forma dispersa: páginas de eventos, Google Docs, sites de
organizadores parceiros, cópias enviadas por usuários à Liquipedia e repositórios de terceiros. Por isso o
acervo foi montado documento a documento, registrando de onde veio cada um. Essa diferença de
transparência normativa entre as três empresas já é, em si, um dado de pesquisa.

## Procedência (coluna `procedencia`)

| Categoria | Significado |
|---|---|
| Oficial (site da Garena / documento publicado pela Garena) | Publicado pela própria desenvolvedora. |
| Oficial (site do organizador) | Publicado pelo organizador do evento (ex.: EWC, Google). |
| Cópia comunitária (Liquipedia Commons) | Enviado por usuários da Liquipedia, em geral sem fonte declarada. Usar com essa ressalva. |
| Cópia em repositório de terceiros | Scribd, Studocu etc. Catalogado, mas **não coletado** (acesso restrito). |
| Documento público de origem a verificar | Público, mas sem autoria clara. |

A coluna `acesso` diz se o documento foi coletado (`coletável`) ou não (restrito ou indisponível, com o motivo).

## Critérios de inclusão

Entram: circuitos oficiais da Garena (FFWS, ligas e campeonatos nacionais), eventos internacionais
multijogo com Free Fire (EWC), circuitos de terceiros licenciados ou patrocinados (Snapdragon Pro Series,
Google Play Games League) e políticas da plataforma que afetam competidores. Ficam de fora torneios amadores,
escolares e universitários, salvo se a pesquisa pedir.

## Conteúdo

| Caminho | O que é |
|---|---|
| `catalogo/fontes.csv` | Curadoria manual: um documento por linha, com competição, região, país, temporada, organizador, idioma, procedência, acesso e URL. **É o arquivo a editar para incluir documentos novos.** |
| `catalogo/catalogo.csv` / `.json` | Catálogo gerado (acrescenta chave do arquivo e caminho do texto). |
| `textos/<id>.md` | Texto integral extraído, com cabeçalho de metadados e marcas `<!-- página N -->`. |
| `manifest.csv` | Situação de cada documento: `ok`, `erro`, `nao_coletado`; SHA-256, páginas, palavras, idioma. |
| `secoes.csv` | Índice de seções e subseções (documento, número, título, página). |
| `comparativo/temas.csv` | Livro de códigos com 33 temas (idade mínima, residência, dispositivos, conluio, apostas, penalidades, discricionariedade, marcadores deônticos etc.) e expressões em inglês, português, espanhol e indonésio. |
| `scripts/` | Coleta, busca, comparação de versões e comparação entre corpora. |

## Como incluir um documento

1. Acrescente uma linha em `catalogo/fontes.csv` (pode editar direto no GitHub).
2. O commit dispara o workflow, que baixa o documento e extrai o texto.

## Uso

```bash
pip install -r requirements.txt     # e poppler-utils (pdftotext) no sistema
python scripts/gerar_catalogo.py && python scripts/baixar_e_extrair.py

python scripts/buscar.py --listar --procedencia Oficial
python scripts/buscar.py --regex "emulat|emulador" --qualquer --contar
python scripts/buscar.py --remoto vitoriaveig/freefire-esports-regras "teaming"

# Free Fire × Riot × Valve, tema a tema (lê os três corpora do GitHub)
python scripts/comparar_corpora.py
python scripts/comparar_corpora.py --trechos idade_minima --max-trechos 3
```

## Limitações (para a seção de método)

- O acervo é **incompleto por construção**: depende do que foi tornado público. A ausência de um documento não significa ausência de regra.
- Cópias comunitárias não têm garantia de serem a versão final; confira versão e data no texto.
- Os corpora comparados diferem em natureza: a Valve regula organizadores terceiros de torneios de CS2; Riot e Garena regulam as próprias ligas. Também diferem em tamanho e idioma.
- A comparação por dicionário mede presença temática e frequência de termos; serve para mapear e orientar a leitura, não substitui a codificação manual.

## Como citar

> GARENA. *Título do documento*. Versão X. [S. l.]: Garena, ano. Disponível em: URL. Acesso em: data.
> Acervo organizado em: SOBRENOME, Nome. *freefire-esports-regras*. GitHub, 2026. Disponível em: https://github.com/vitoriaveig/freefire-esports-regras (commit `<hash>`).

Scripts sob licença MIT. Os textos pertencem aos respectivos autores (Garena, organizadores).
