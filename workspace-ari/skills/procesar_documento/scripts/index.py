"""Mantenimiento del catalogo global y del log de ingesta."""
from __future__ import annotations

import csv
import datetime as dt
from pathlib import Path

from utils import now_iso

CATALOGO_HEADER = (
    "| id | ruta | tema | periodo | tipo | fecha_doc | origen | resumen | estado |\n"
    "|----|------|------|---------|------|-----------|--------|---------|--------|\n"
)


def update_catalogo(procesados_root: Path, fm: dict, index_rel: str, resumen: str):
    cat = procesados_root / "_catalogo.md"
    if not cat.exists():
        cat.write_text("# Catalogo de documentos procesados\n\n" + CATALOGO_HEADER, encoding="utf-8")
    corto = (resumen[:90] + "…") if len(resumen) > 90 else resumen
    corto = corto.replace("|", "/").replace("\n", " ")
    origen = f"{fm.get('origen_canal', '')}:{fm.get('origen_id', '')}"
    row = (
        f"| {fm['id']} | {index_rel} | {fm['tema']} | {fm['periodo']} | {fm['tipo']} "
        f"| {fm.get('fecha_documento', '')} | {origen} | {corto} | {fm['estado']} |\n"
    )
    with open(cat, "a", encoding="utf-8") as fh:
        fh.write(row)


def append_log(logs_dir: Path, fm: dict, archivo: str, destino: str, decision: str, motivo: str):
    logs_dir.mkdir(parents=True, exist_ok=True)
    log = logs_dir / f"ingesta-{dt.date.today():%Y-%m}.csv"
    new = not log.exists()
    with open(log, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["timestamp", "canal", "id_remitente", "archivo", "hash",
                        "decision", "destino", "motivo", "agente"])
        w.writerow([now_iso(), fm.get("origen_canal", ""), fm.get("origen_id", ""),
                    archivo, fm.get("hash_original", ""), decision, destino, motivo, "pipeline"])