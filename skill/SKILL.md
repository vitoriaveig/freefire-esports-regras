---
name: "freefire-esports-regras"
description: "Consulta e analisa regulamentos de esports de Free Fire (Garena: FFWS, ligas nacionais, EWC) em acervo curado com procedência, e os compara com Riot e Valve; use para dúvidas pontuais ou para dados e análises de pesquisa acadêmica."
---

# Regulamentos de esports de Free Fire (Garena) e comparação com Riot e Valve

Esta skill tem três modos. Escolha pelo pedido:

- **Consulta rápida**: pergunta pontual ("no FFWS MENA 2026, pode usar emulador?", "qual a punição por teaming na FFWS LATAM?"). Responda na conversa, curto e direto.
- **Análise para pesquisa**: dados, contagens, comparações entre regiões ou temporadas do Free Fire, tabelas, gráficos ou texto para artigo. Siga a seção 4.
- **Comparativo Free Fire × Riot × Valve**: o mesmo tema nas três empresas (idade mínima, dispositivos, conluio, apostas, penalidades, discricionariedade etc.). Siga a seção 5.

Responda sempre no idioma do usuário.

## 1. Obter as fontes (sempre)

Nunca responda de memória. O acervo fica no GitHub:

- Repositório: https://github.com/vitoriaveig/freefire-esports-regras
- Base para leitura: `https://raw.githubusercontent.com/vitoriaveig/freefire-esports-regras/main/`
- Arquivos: `catalogo/fontes.csv` (curadoria: competição, região, país, temporada, organizador, idioma, **procedência**, **acesso**, URL), `catalogo/catalogo.csv` (o mesmo, com o caminho do texto), `manifest.csv` (situação da coleta), `secoes.csv` (seções com página), `textos/<id>.md` (texto integral com `<!-- página N -->`), `comparativo/temas.csv` (livro de códigos), `scripts/buscar.py`, `scripts/comparar_versoes.py`, `scripts/comparar_corpora.py`.

```bash
B=https://raw.githubusercontent.com/vitoriaveig/freefire-esports-regras/main
mkdir -p ff && cd ff && for s in buscar comparar_versoes comparar_corpora; do curl -sSO $B/scripts/$s.py; done
mkdir -p comparativo && curl -sS -o comparativo/temas.csv $B/comparativo/temas.csv
python3 buscar.py --remoto vitoriaveig/freefire-esports-regras --listar
python3 buscar.py --remoto vitoriaveig/freefire-esports-regras --regex "emulat|emulador" --qualquer
```

Filtros do buscador: `--jogo`, `--competicao`, `--regiao`, `--temporada`, `--tipo`, `--procedencia`, `--ids`; `--regex`, `--qualquer`, `--contar`, `--max`.

Confira no `manifest.csv` se o texto está `ok`. `nao_coletado` indica documento só catalogado (Scribd, Studocu, site da Garena fora do ar etc.; o motivo está em `detalhe`). Se o usuário tiver o PDF, peça que anexe.

**Quando o usuário anexar um regulamento:** (1) calcule o SHA-256 e compare com `manifest.csv`; se já existir, só registre na `nota` que ele confirma a cópia; (2) se for novo, leia as primeiras páginas para identificar competição, temporada, versão, organizador e idioma; (3) acrescente a linha em `catalogo/fontes.csv` com `acesso` = "fornecido pela pesquisadora (texto extraído do PDF)", `procedencia` = "Cópia fornecida pela pesquisadora" e `url` = `arquivo-fornecido:<nome do arquivo>`; (4) num clone do repositório, rode `python scripts/gerar_catalogo.py && python scripts/incluir_arquivo_local.py <id> <arquivo>`; (5) envie ao GitHub `catalogo/fontes.csv`, `textos/<id>.md` e `manifest.csv` (pelo navegador, se não houver acesso por git). Nunca versione o PDF original. Registre na `nota` sinais de que o PDF não é o original (ex.: gerado por conversor em data posterior).

**Restrições:** não tente contornar bloqueios de sites (robots, login, certificado inválido) nem baixar de Scribd/Studocu. Para incluir um documento novo, oriente o usuário a acrescentar uma linha em `catalogo/fontes.csv` no GitHub; o workflow coleta sozinho.

## 2. Como ler o acervo do Free Fire

**Não há biblioteca oficial.** A Garena não mantém acervo público centralizado de regulamentos (diferente da Riot e da Valve). O acervo é curado e **incompleto por construção**: a ausência de um documento não significa ausência de regra. Diga "não consta no acervo", nunca "não existe regra".

**Procedência importa.** Sempre informe a procedência do documento citado:

- *Oficial (site da Garena / documento publicado pela Garena / site do organizador)*: pode ser citado como fonte primária.
- *Cópia comunitária (Liquipedia Commons)*: enviada por usuários, em geral sem fonte declarada. Cite com a ressalva e confira versão e data no próprio texto.
- *Cópia fornecida pela pesquisadora*: PDF entregue pela usuária, sem link público; cite como "cópia em posse da autora" e indique a provável origem quando houver (coluna `fonte_original`).
- *Cópia em repositório de terceiros* e *origem a verificar*: só catalogadas ou com autoria a confirmar.

**Camadas normativas** (quando existirem): política da plataforma (Abuse Policy da Garena, para todos os jogadores) → regulamento do circuito (FFWS regional, liga nacional) → regras do evento ou da etapa (qualificatórias, finais) → regulamento do organizador terceiro quando o Free Fire está em evento multijogo (EWC: Global Rulebook + rulebook do Free Fire, em geral com cláusula de precedência). Procure a cláusula de precedência no texto.

**Particularidades do Free Fire** para a análise: jogo mobile (regras de aparelho oficial, emuladores, periféricos e versão do cliente), formato battle royale (pontuação por colocação e abate, critérios de desempate, conluio entre equipes, o *teaming*), público jovem (idade mínima e consentimento de responsáveis), circuitos regionais com regras próprias e documentos em vários idiomas (inglês, espanhol, português, indonésio). O Free Fire foi banido na Índia em 2022; o FFIC 2021 é anterior ao banimento e o Free Fire MAX voltou em 2025.

**Achados de estrutura úteis para a análise:** vários regulamentos da Garena (FFWS MENA, MEA, Africa, FFNS, FFMC, Clash Cup Nigeria) seguem um mesmo modelo global ("Overview / Definitions / Purpose & Position / Adjustment / Validity"), o que permite comparar regiões seção a seção; a FFWS LATAM usa outro modelo, em espanhol; a EWC Qualifier Open LATAM 2026 é operada por um terceiro (ProSur). Confirme no texto antes de afirmar.

**Glossário.** FFWS = Free Fire World Series (circuito oficial; regiões como Brasil, LATAM, SEA, MENA/MEA, África, EUA, Bangladesh; Global Finals). FFNS = Free Fire Nusantara Series (Indonésia). FFMC = Free Fire Malaysia Championship. FFIC = Free Fire India Championship. FFML = Free Fire Master League (Indonésia). LBFF = Liga Brasileira de Free Fire (séries A, B, C; substituída pela FFWS BR; a Série C de 2020 era operada pela Player1 com a Garena Brasil e a LnK). LAFF = Liga Ascensão de Free Fire (divisão de acesso à FFWS BR). Copa NFA = torneio independente da Liga NFA Entretenimento. COPA FF = copa brasileira da Garena. EWC = Esports World Cup. Booyah = vitória em uma queda.

## 3. Modo consulta rápida

1. Identifique competição, região e temporada.
2. Escolha o documento pelo catálogo e localize o trecho com `buscar.py` ou `secoes.csv`.
3. Responda em poucas linhas: a regra; seção e página; trecho original entre aspas com tradução; documento, versão e **procedência**; ressalvas.
4. Termine com o link do documento (coluna `url`) e o do texto no GitHub.

## 4. Modo análise para pesquisa (só Free Fire)

1. Monte a base em Python com `catalogo.csv` + `manifest.csv` (um texto por arquivo; ignore `nao_coletado`).
2. Compare regiões e temporadas sobre um tema (`buscar.py --contar` com expressões em vários idiomas) e versões entre si (`comparar_versoes.py <id_antigo> <id_novo>`, ex.: FFWS MENA 2026 Spring × Fall; FFNS 2025 Fall × 2026 Spring; FFWS LATAM 2025 × 2026).
3. A cobertura do acervo é um achado: quantos documentos são oficiais, quantos são cópias, quais regiões não têm regulamento público. Calcule em código a partir de `fontes.csv`.
4. Classificações do catálogo (circuito, tipo, procedência) são do pesquisador; confira as que entrarem como variável.

## 5. Modo comparativo Free Fire × Riot × Valve

```bash
python3 comparar_corpora.py                      # lê os três corpora do GitHub; gera CSVs e tabela-resumo
python3 comparar_corpora.py --trechos conluio --max-trechos 3
python3 comparar_corpora.py --riot-jogo VALORANT --riot-temporada 2026 --ff-procedencia Oficial
```

- Corpora: Free Fire (este acervo); Riot (https://github.com/vitoriaveig/riot-esports-regras, só regulamentos, políticas, códigos e índices de penalidades ativos, por padrão); Valve (https://github.com/ValveSoftware/counter-strike_rules_and_regs: requisitos de operação de torneios, exceções, regulamento suplementar dos Majors e diretrizes de itens).
- Saídas: `comparativo_documentos.csv` (documento × tema: presença, ocorrências, por 1.000 palavras) e `comparativo_resumo.csv` (corpus × tema: % de documentos e taxa mediana).
- O livro de códigos (`comparativo/temas.csv`) tem 30 temas e 3 marcadores deônticos (obrigação, proibição, permissão), com expressões em inglês, português, espanhol e indonésio. Para um tema novo, acrescente uma linha com a expressão regular.
- **Interprete com cuidado** e diga isso no texto: (1) a Valve regula organizadores terceiros, enquanto Riot e Garena regulam as próprias ligas; (2) os corpora têm tamanhos muito diferentes (em out/2026: Riot 70 documentos normativos ativos, Valve 4, Free Fire 19 com texto de 32 catalogados); (3) idiomas diferentes afetam a contagem por dicionário; (4) presença de termo não é presença de regra. Use os números para mapear e escolher o que ler, e confirme com os trechos (`--trechos`) e a leitura integral.
- Eixos analíticos sugeridos: transparência normativa (acesso público aos regulamentos), centralização do poder (cláusulas de discricionariedade, recursos e arbitragem), proteção de menores, integridade (apostas, manipulação, órgãos externos como ESIC), especificidades mobile e battle royale, e densidade deôntica.

## 6. Rigor e entrega

- Todos os números saem de código. Toda afirmação sobre regra cita documento, seção, página e procedência.
- Base codificada como planilha (artifact do tipo Sheets, se disponível; .xlsx só se o usuário pedir); gráficos em código.
- Nota metodológica pronta para o artigo: critérios de inclusão do acervo, categorias de procedência, data de acesso, hash do commit de cada repositório (`git ls-remote https://github.com/<repo> HEAD`), livro de códigos e limitações acima. Sugira dupla codificação e kappa de Cohen se o artigo exigir.
- Referência no estilo que o usuário indicar (ABNT, APA etc.); se não indicar, pergunte. Modelo ABNT: GARENA. *Título do documento*. Versão X. [S. l.]: Garena, ano. Disponível em: URL. Acesso em: data. Para cópias da Liquipedia, indique a procedência na nota.
- Texto acadêmico: registro adequado a periódicos internacionais de alto impacto; melhore ortografia, coesão e fluidez preservando a forma de escrita da autora. Não acrescente afirmações que o acervo não sustente.
- Skills relacionadas: `riot-esports-regras` (consultas aprofundadas no corpus da Riot) e `cs2-regras-torneios` (regras e exceções da Valve).
