"""Limpieza lossless de texto y tablas.

El objetivo es quitar todo lo que NO es informacion (formato repetido, ruido de
paginacion, espacios, duplicados) sin alterar jamas los datos ni las cifras.
"""
from __future__ import annotations

import re
from collections import Counter

_PAGE_NUM_RE = re.compile(
    r"^\s*(p[aá]gina|page|pag\.?)?\s*\d{1,4}\s*(/\s*\d{1,4})?\s*$", re.I
)


def remove_repeated_headers_footers(pages):
    """Quita las lineas que se repiten como cabecera/pie en >50% de las paginas."""
    if len(pages) < 3:
        return pages
    edge = Counter()
    for p in pages:
        lines = [l.strip() for l in p.splitlines() if l.strip()]
        for l in lines[:2] + lines[-2:]:
            edge[l] += 1
    threshold = len(pages) * 0.5
    repeated = {l for l, c in edge.items() if c > threshold and len(l) < 120}
    if not repeated:
        return pages
    return ["\n".join(l for l in p.splitlines() if l.strip() not in repeated) for p in pages]


def clean_text(text: str) -> str:
    # Une palabras cortadas por guion al final de renglon: "docu-\nmento" -> "documento"
    text = re.sub(r"([A-Za-zÁÉÍÓÚáéíóúÑñ])-\n([a-záéíóúñ])", r"\1\2", text)
    # Elimina lineas que son solo numero de pagina
    out_lines = [l.rstrip() for l in text.splitlines() if not _PAGE_NUM_RE.match(l)]
    text = "\n".join(out_lines)
    # Colapsa saltos de linea y espacios redundantes
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    # Deduplica parrafos identicos conservando el orden
    seen, kept = set(), []
    for para in text.split("\n\n"):
        key = para.strip()
        if key and key in seen:
            continue
        seen.add(key)
        kept.append(para)
    return "\n\n".join(kept).strip()


def clean_table(rows):
    """Elimina filas y columnas COMPLETAMENTE vacias. Conserva columnas con nombre."""
    rows = [r for r in rows if any(str(c).strip() for c in r)]
    if not rows:
        return rows
    ncols = max(len(r) for r in rows)
    rows = [list(r) + [""] * (ncols - len(r)) for r in rows]
    keep = [j for j in range(ncols) if any(str(r[j]).strip() for r in rows)]
    return [[r[j] for j in keep] for r in rows]