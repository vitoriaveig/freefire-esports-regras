#!/usr/bin/env python3
"""Compara os regulamentos de Free Fire (Garena) com os da Riot Games e da Valve, tema a tema.

Corpora:
  ff     -> este repositório (vitoriaveig/freefire-esports-regras): textos/*.md com manifesto "ok"
  riot   -> vitoriaveig/riot-esports-regras: só regulamentos, políticas, códigos e índices de penalidades
  valve  -> ValveSoftware/counter-strike_rules_and_regs: requisitos de operação de torneios, exceções,
            regulamento suplementar dos Majors e diretrizes de itens

Para cada documento e cada tema do livro de códigos (comparativo/temas.csv) calcula: presença (sim/não),
ocorrências e ocorrências por 1.000 palavras. Gera:
  saida/comparativo_documentos.csv  (uma linha por documento × tema)
  saida/comparativo_resumo.csv      (corpus × tema: % de documentos com o tema e taxa mediana)
e imprime uma tabela-resumo em Markdown.

Exemplos:
  python scripts/comparar_corpora.py                       # tudo, lendo do GitHub
  python scripts/comparar_corpora.py --ff-local .          # FF a partir do clone local
  python scripts/comparar_corpora.py --trechos apostas --max-trechos 3   # trechos para leitura qualitativa
  python scripts/comparar_corpora.py --riot-jogo VALORANT --riot-temporada 2026

Leitura dos resultados: é uma medida de presença temática por dicionário de termos (en/pt/es/id), útil para
mapear e orientar a leitura; não substitui a codificação manual. Os corpora diferem em natureza (a Valve
regula organizadores terceiros; Riot e Garena regulam as próprias ligas), em tamanho e em idioma.
"""
import argparse, csv, io, re, statistics, sys, urllib.request
from pathlib import Path

REPO_FF = "vitoriaveig/freefire-esports-regras"
REPO_RIOT = "vitoriaveig/riot-esports-regras"
REPO_VALVE = "ValveSoftware/counter-strike_rules_and_regs"
VALVE_DOCS = [
    ("tournament-operation-requirements", "Tournament Operation Requirements", "Requisitos de operação de torneios"),
    ("tournament-operation-requirements-exceptions", "Tournament Operation Requirements – Exceptions", "Exceções concedidas"),
    ("major-supplemental-rulebook", "Major Supplemental Rulebook", "Regulamento suplementar (Majors)"),
    ("tournament-item-submission-guidelines", "Tournament Item Submission Guidelines", "Diretrizes de itens"),
]
TIPOS_RIOT = ("Regulamento", "Regras", "Política", "Código", "Índice de penalidades")
INVIS = re.compile("[­​-‏‪-‮⁠-⁩﻿]")
LIG = str.maketrans({"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl"})


def ler(repo, rel, cache, local=None):
    if local:
        return (Path(local) / rel).read_text(encoding="utf-8")
    alvo = cache / repo.replace("/", "__") / rel
    if not alvo.exists():
        url = f"https://raw.githubusercontent.com/{repo}/main/{rel}"
        with urllib.request.urlopen(url, timeout=90) as r:
            txt = r.read().decode("utf-8")
        alvo.parent.mkdir(parents=True, exist_ok=True); alvo.write_text(txt, encoding="utf-8")
    return alvo.read_text(encoding="utf-8")


def limpar(txt):
    corpo = txt.split("\n---\n", 1)[-1] if txt.startswith("---") else txt
    corpo = re.sub(r"<!-- página \d+ -->", " ", corpo)
    corpo = corpo.split("## Links presentes no documento")[0]
    return INVIS.sub("", corpo).translate(LIG)


def docs_repo(repo, cache, local, filtro):
    cat = list(csv.DictReader(io.StringIO(ler(repo, "catalogo/catalogo.csv", cache, local))))
    man = {r["texto_id"]: r for r in csv.DictReader(io.StringIO(ler(repo, "manifest.csv", cache, local)))}
    vistos, out = set(), []
    for d in cat:
        tid = Path(d["texto"]).stem
        if tid in vistos or man.get(tid, {}).get("status") != "ok" or not filtro(d):
            continue
        vistos.add(tid)
        try:
            out.append((d, limpar(ler(repo, d["texto"], cache, local)), man[tid]))
        except Exception as e:
            print(f"# sem texto {repo}:{tid}: {e}", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--temas", default=str(Path(__file__).resolve().parent.parent / "comparativo" / "temas.csv"))
    ap.add_argument("--corpora", default="ff,riot,valve")
    ap.add_argument("--ff-local", help="pasta do clone local do repositório Free Fire (padrão: GitHub)")
    ap.add_argument("--riot-jogo"); ap.add_argument("--riot-temporada")
    ap.add_argument("--riot-incluir-arquivados", action="store_true")
    ap.add_argument("--ff-procedencia", help="filtra FF pela procedência (ex.: Oficial)")
    ap.add_argument("--min-palavras", type=int, default=300, help="ignora documentos muito curtos (formulários, capas)")
    ap.add_argument("--saida", default="saida_comparativo")
    ap.add_argument("--cache", default=".cache_corpus")
    ap.add_argument("--trechos", help="tema para imprimir trechos de exemplo por corpus")
    ap.add_argument("--max-trechos", type=int, default=3)
    a = ap.parse_args()
    cache, saida = Path(a.cache), Path(a.saida); saida.mkdir(exist_ok=True)
    temas = list(csv.DictReader(open(a.temas, encoding="utf-8")))
    rx = {t["tema"]: re.compile(t["regex"], re.I) for t in temas}
    corpora = a.corpora.split(",")

    docs = []  # (corpus, id, titulo, jogo, competicao, temporada, tipo, texto, idioma)
    if "ff" in corpora:
        f = lambda d: (not a.ff_procedencia or a.ff_procedencia.lower() in d.get("procedencia", "").lower())
        for d, t, m in docs_repo(REPO_FF, cache, a.ff_local, f):
            docs.append(("Free Fire (Garena e outros)", d["id"], d["titulo"], d["jogo"], d["competicao"], d["temporada"],
                         d["tipo_documento"], t, m.get("idioma", ""), d.get("procedencia", "")))
    if "riot" in corpora:
        def f(d):
            if not d["tipo_documento"].startswith(TIPOS_RIOT): return False
            if not a.riot_incluir_arquivados and d["status_biblioteca"] == "Arquivado": return False
            if a.riot_jogo and d["jogo"] != a.riot_jogo: return False
            if a.riot_temporada and d["temporada"] != a.riot_temporada: return False
            return True
        for d, t, m in docs_repo(REPO_RIOT, cache, None, f):
            docs.append(("Riot Games", d["id"], d["titulo"], d["jogo"], d["competicao"], d["temporada"],
                         d["tipo_documento"], t, m.get("idioma", ""), "Oficial (Biblioteca da Riot)"))
    if "valve" in corpora:
        for nome, titulo, tipo in VALVE_DOCS:
            try:
                t = limpar(ler(REPO_VALVE, nome + ".md", cache))
                docs.append(("Valve (CS2)", nome, titulo, "Counter-Strike 2", "Torneios de CS2 (terceiros)", "vigente",
                             tipo, t, "en", "Oficial (repositório da Valve)"))
            except Exception as e:
                print(f"# sem texto valve:{nome}: {e}", file=sys.stderr)

    linhas = []
    for c, did, tit, jogo, comp, temp, tipo, txt, idioma, proc in docs:
        n = len(re.findall(r"\w+", txt))
        if n < a.min_palavras: continue
        for t in temas:
            k = len(rx[t["tema"]].findall(txt))
            linhas.append({"corpus": c, "id": did, "titulo": tit, "jogo": jogo, "competicao": comp, "temporada": temp,
                           "tipo_documento": tipo, "idioma": idioma, "procedencia": proc, "palavras": n,
                           "tema": t["tema"], "presente": int(k > 0), "ocorrencias": k,
                           "por_mil_palavras": round(1000 * k / n, 3)})
    if not linhas:
        print("Nenhum documento encontrado."); return
    with open(saida / "comparativo_documentos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)

    corpus_nomes = sorted({l["corpus"] for l in linhas})
    resumo = []
    for t in temas:
        reg = {"tema": t["tema"], "rotulo": t["rotulo"]}
        for c in corpus_nomes:
            sel = [l for l in linhas if l["corpus"] == c and l["tema"] == t["tema"]]
            reg[f"{c} | % docs"] = round(100 * sum(l["presente"] for l in sel) / len(sel), 1)
            reg[f"{c} | mediana/1000"] = round(statistics.median(l["por_mil_palavras"] for l in sel), 3)
        resumo.append(reg)
    with open(saida / "comparativo_resumo.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(resumo[0])); w.writeheader(); w.writerows(resumo)

    ndocs = {c: len({l["id"] for l in linhas if l["corpus"] == c}) for c in corpus_nomes}
    print("Documentos analisados: " + "; ".join(f"{c}: {n}" for c, n in ndocs.items()))
    print("\n| Tema | " + " | ".join(f"{c} (% docs)" for c in corpus_nomes) + " |")
    print("|---|" + "---|" * len(corpus_nomes))
    for r in resumo:
        print(f"| {r['rotulo']} | " + " | ".join(f"{r[f'{c} | % docs']}" for c in corpus_nomes) + " |")
    print(f"\nArquivos: {saida/'comparativo_documentos.csv'}, {saida/'comparativo_resumo.csv'}")

    if a.trechos:
        r = rx[a.trechos]
        for c in corpus_nomes:
            print(f"\n### {c} — trechos para '{a.trechos}'")
            k = 0
            for d in docs:
                if d[0] != c: continue
                for m in r.finditer(d[7]):
                    ini, fim = max(0, m.start() - 220), min(len(d[7]), m.end() + 220)
                    print(f"- [{d[1]}] …{' '.join(d[7][ini:fim].split())}…")
                    k += 1; break
                if k >= a.max_trechos: break


if __name__ == "__main__":
    main()
