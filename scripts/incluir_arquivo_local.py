#!/usr/bin/env python3
"""Inclui no corpus um PDF/DOCX entregue pela pesquisadora (sem URL pública de download).

Extrai o texto com o mesmo método da coleta automática (pdftotext + OCR quando o PDF é imagem),
grava textos/<id>.md com o cabeçalho de metadados e atualiza a linha correspondente em manifest.csv.
O documento precisa estar em catalogo/fontes.csv com `acesso` começando por "fornecido" e o
catálogo precisa ter sido gerado (scripts/gerar_catalogo.py). O arquivo original não é versionado.

Uso: python scripts/incluir_arquivo_local.py <id> <caminho_do_arquivo> [<id> <arquivo> ...]
"""
import csv, hashlib, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import baixar_e_extrair as bx  # noqa: E402

raiz = Path(__file__).resolve().parent.parent
docs = {d["id"]: d for d in csv.DictReader(open(raiz / "catalogo" / "catalogo.csv", encoding="utf-8"))}
mpath = raiz / "manifest.csv"
manifest = {r["texto_id"]: r for r in csv.DictReader(open(mpath, encoding="utf-8"))} if mpath.exists() else {}
args = sys.argv[1:]
if not args or len(args) % 2:
    sys.exit(__doc__)
for did, arq in zip(args[::2], args[1::2]):
    d = docs[did]
    if not d["acesso"].startswith("fornecido"):
        sys.exit(f"{did}: o campo 'acesso' em fontes.csv deve começar por 'fornecido'")
    tid = Path(d["texto"]).stem
    dados = Path(arq).read_bytes()
    reg = {k: "" for k in bx.CAMPOS_MANIFEST}
    reg.update(texto_id=tid, chave_arquivo=d["chave_arquivo"], titulo=d["titulo"], url=d["url"], status="ok",
               detalhe=f"arquivo fornecido pela pesquisadora ({Path(arq).name})", sha256=hashlib.sha256(dados).hexdigest(),
               bytes=len(dados), baixado_em=bx.agora(), arquivo_texto=f"textos/{tid}.md")
    paginas, corpo = [], ""
    if dados[:4] == b"%PDF":
        paginas = bx.pdf_para_paginas(dados)
        if paginas and len(re.findall(r"\w+", "\n".join(paginas))) < 10 * len(paginas):
            com_ocr = bx.ocr(dados)
            if com_ocr:
                paginas = bx.pdf_para_paginas(com_ocr); reg["detalhe"] += "; texto obtido por OCR (conferir)"
        corpo = "\n".join(f"\n<!-- página {i} -->\n{pg.rstrip()}" for i, pg in enumerate(paginas, 1))
        links = bx.links_pdf(dados)
        if links:
            corpo += "\n\n## Links presentes no documento\n\n" + "\n".join(f"- {u}" for u in links)
    else:
        corpo = bx.normalizar(bx.docx_para_texto(dados))
    plano = "\n".join(paginas) if paginas else corpo
    reg.update(paginas=len(paginas) or "", palavras=len(re.findall(r"\w+", plano)), idioma=bx.detectar_idioma(plano))
    (raiz / "textos").mkdir(exist_ok=True)
    (raiz / "textos" / f"{tid}.md").write_text(bx.cabecalho(d, reg) + corpo.strip() + "\n", encoding="utf-8")
    manifest[tid] = reg
    print(f"[ok] {tid}: {reg['paginas']} páginas, {reg['palavras']} palavras, idioma {reg['idioma']}")
validos = {Path(d["texto"]).stem for d in docs.values()}
manifest = {k: v for k, v in manifest.items() if k in validos}
with open(mpath, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=bx.CAMPOS_MANIFEST); w.writeheader()
    for k in sorted(manifest): w.writerow({c: manifest[k].get(c, "") for c in bx.CAMPOS_MANIFEST})
