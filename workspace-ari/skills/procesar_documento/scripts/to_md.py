"""Escritura de trozos de texto a MD y del indice ligero del documento."""
from __future__ import annotations

from pathlib import Path

from utils import slugify, yaml_escape


def write_chunk_md(folder: Path, chunk: dict):
    name = f"{chunk['n']:02d}-{slugify(chunk['title'])}.md"
    body = f"# {chunk['title']}\n\n{chunk['text']}\n"
    (folder / name).write_text(body, encoding="utf-8")
    return name, len(body.encode("utf-8"))


def build_index_md(folder: Path, fm: dict, chunk_files, table_schemas, resumen: str):
    """Genera _index.md: front-matter + resumen + tabla de contenidos."""
    lines = ["---"]
    for k, v in fm.items():
        lines.append(f"{k}: {yaml_escape(v)}")
    lines.append("---\n")
    lines.append("## Resumen\n")
    lines.append(resumen + "\n")
    lines.append("## Contenido\n")
    if chunk_files:
        lines.append("### Trozos de texto\n")
        for title, name in chunk_files:
            lines.append(f"- [{title}]({name})")
        lines.append("")
    if table_schemas:
        lines.append("### Tablas (CSV)\n")
        for s in table_schemas:
            cols = ", ".join(str(c) for c in s["columnas"][:12])
            lines.append(f"- [{s['titulo']}]({s['nombre']}) — {s['filas']} filas; columnas: {cols}")
        lines.append("")
    content = "\n".join(lines)
    (folder / "_index.md").write_text(content, encoding="utf-8")
    return len(content.encode("utf-8"))