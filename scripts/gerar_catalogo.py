#!/usr/bin/env python3
"""Gera catalogo/catalogo.csv e .json a partir de catalogo/fontes.csv (curadoria manual).

Diferente da Riot, o Free Fire não tem uma biblioteca oficial centralizada: o acervo é montado à mão,
documento por documento, registrando a procedência de cada um (coluna `procedencia`) e se ele pode ser
coletado (coluna `acesso`). Este script só valida os campos e acrescenta as colunas técnicas usadas
pelos demais scripts (chave do arquivo e caminho do texto).

Uso: python scripts/gerar_catalogo.py [--raiz .]
"""
import argparse, csv, hashlib, json, re, sys
from collections import Counter
from datetime import date
from pathlib import Path

OBRIGATORIOS = ["id", "titulo", "jogo", "competicao", "temporada", "organizador", "tipo_documento", "procedencia", "acesso", "url"]


def chave(url):
    m = re.search(r"/d/(?:e/)?([\w-]{20,})", url)
    if m: return "g-" + m.group(1)[:16]
    return hashlib.sha1(url.encode()).hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--raiz", default=".")
    raiz = Path(ap.parse_args().raiz)
    linhas = list(csv.DictReader(open(raiz / "catalogo" / "fontes.csv", encoding="utf-8")))
    erros = []
    ids = Counter(l["id"] for l in linhas)
    for l in linhas:
        for c in OBRIGATORIOS:
            if not l.get(c, "").strip(): erros.append(f"{l.get('id')}: campo vazio '{c}'")
        if ids[l["id"]] > 1: erros.append(f"id repetido: {l['id']}")
    if erros:
        print("\n".join(erros)); sys.exit(1)
    por_url = {}
    for l in linhas:
        k = chave(l["url"]); l["chave_arquivo"] = k
        por_url.setdefault(k, []).append(l["id"])
    for l in linhas:
        l["mesmo_arquivo_que"] = ";".join(i for i in por_url[l["chave_arquivo"]] if i != l["id"])
        l["texto"] = f"textos/{por_url[l['chave_arquivo']][0]}.md"
        l["status_biblioteca"] = l["acesso"]  # compatibilidade com os scripts do corpus da Riot
    campos = list(linhas[0].keys())
    with open(raiz / "catalogo" / "catalogo.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(linhas)
    meta = {"descricao": "Acervo curado de regulamentos de esports de Free Fire (Garena), com procedência",
            "catalogo_gerado_em": date.today().isoformat(), "n_documentos": len(linhas),
            "n_coletaveis": sum(l["acesso"].startswith("coletável") for l in linhas), "documentos": linhas}
    (raiz / "catalogo" / "catalogo.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(linhas)} documentos; {meta['n_coletaveis']} coletáveis")


if __name__ == "__main__":
    main()
