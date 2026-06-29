"""Escritura de tablas a CSV normalizado."""
from __future__ import annotations

import csv
import io
from pathlib import Path


def write_table_csv(folder: Path, idx: int, table: dict):
    """Escribe una tabla (con filas ya limpias) a CSV.

    Devuelve (nombre_archivo, bytes_escritos, esquema).
    """
    rows = table["rows"]
    name = f"tabla-{idx:02d}.csv"
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    data = buf.getvalue()
    (folder / name).write_text(data, encoding="utf-8")
    schema = {
        "nombre": name,
        "titulo": table["title"],
        "columnas": rows[0] if rows else [],
        "filas": max(len(rows) - 1, 0),
    }
    return name, len(data.encode("utf-8")), schema