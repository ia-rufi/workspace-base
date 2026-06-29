"""Particion de bloques de texto en trozos manejables.

Si el texto tiene encabezados markdown, parte por ellos; si no, acumula parrafos
hasta un tamaño maximo. Cada trozo lleva titulo y numero de orden.
"""
from __future__ import annotations

import re

from clean import clean_text


def partition_blocks(text_blocks, max_chars: int):
    chunks = []
    for block in text_blocks:
        text = clean_text(block["text"])
        if not text:
            continue
        if re.search(r"(?m)^#{1,6}\s", text):
            chunks.extend(_by_headings(text))
        else:
            chunks.extend(_by_size(text, block["title"], max_chars))
    for n, c in enumerate(chunks, 1):
        c["n"] = n
        if not c.get("title"):
            c["title"] = f"Seccion {n}"
    return chunks


def _by_headings(text):
    parts, current = [], {"title": None, "lines": []}
    for line in text.splitlines():
        m = re.match(r"^#{1,6}\s+(.*)", line)
        if m:
            if current["lines"] or current["title"]:
                parts.append(current)
            current = {"title": m.group(1).strip(), "lines": []}
        else:
            current["lines"].append(line)
    if current["lines"] or current["title"]:
        parts.append(current)
    result = []
    for p in parts:
        body = "\n".join(p["lines"]).strip()
        if body or p["title"]:
            result.append({"title": p["title"], "text": body})
    return result


def _by_size(text, title, max_chars):
    paras = [p for p in text.split("\n\n") if p.strip()]
    chunks, buf, size = [], [], 0
    for para in paras:
        if size + len(para) > max_chars and buf:
            chunks.append({"title": title, "text": "\n\n".join(buf)})
            buf, size = [], 0
        buf.append(para)
        size += len(para) + 2
    if buf:
        chunks.append({"title": title, "text": "\n\n".join(buf)})
    return chunks