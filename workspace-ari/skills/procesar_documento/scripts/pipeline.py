#!/usr/bin/env python3
"""pipeline.py — orquestador de la skill procesar-documento.

Encadena los modulos (extract, clean, partition, to_csv, to_md, index, resumen_*)
para convertir un documento de datos/entradas/ en una version curada dentro de
datos/procesados/<tema>/<periodo>/. Todo el trabajo pesado es determinista y sin
API; el resumen LLM es opcional y solo recibe un digest reducido.

Uso:
    python pipeline.py --in datos/entradas/reporte.pdf --tema finanzas \
        --periodo 2026-Q2 --workspace . --resumen extractivo
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

import utils
from extract import extract
from clean import clean_table
from partition import partition_blocks
from resumen_extractivo import summarize_extractive
from resumen_llm import summarize_llm
from to_csv import write_table_csv
from to_md import write_chunk_md, build_index_md
from index import update_catalogo, append_log


def process(args) -> int:
    src = Path(args.input).expanduser().resolve()
    if not src.exists():
        print(f"[error] no existe el archivo: {src}", file=sys.stderr)
        return 2

    ws = Path(args.workspace).expanduser().resolve()
    procesados_root = ws / "datos" / "procesados"
    descartados = ws / "datos" / "descartados"
    logs_dir = ws / "datos" / "logs"

    digest_hash = utils.sha256_of(src)
    in_size = src.stat().st_size
    doc_id = utils.gen_id(src.name, digest_hash)
    print(f"-> Procesando {src.name}  ({in_size / 1024:.1f} KB)")

    # 1) Extraer + 2) limpiar/particionar (sin API)
    text_blocks, tables, fmt = extract(src)
    chunks = partition_blocks(text_blocks, args.max_chunk_chars)
    clean_tables = [{"title": t["title"], "rows": clean_table(t["rows"])} for t in tables]
    clean_tables = [t for t in clean_tables if t["rows"]]
    full_text = "\n\n".join(c["text"] for c in chunks)

    # 3) Resumen (extractivo por defecto; llm opcional sobre un digest reducido)
    if args.resumen == "none":
        resumen = ""
    else:
        resumen = summarize_extractive(full_text) if full_text else ""
        if args.resumen == "llm":
            llm = summarize_llm(resumen or full_text[:1500], args.llm_model)
            if llm:
                resumen = llm
    if not resumen and clean_tables:
        resumen = f"Documento con {len(clean_tables)} tabla(s) de datos."

    tipo = "csv" if (clean_tables and not chunks) else "md"
    fm = {
        "id": doc_id,
        "origen_canal": args.origen_canal,
        "origen_id": args.origen_id,
        "fecha_recepcion": utils.today(),
        "fecha_documento": "",
        "tema": args.tema,
        "periodo": args.periodo,
        "tipo": tipo,
        "formato_original": fmt,
        "hash_original": digest_hash,
        "version": 1,
        "resumen": resumen,
        "estado": "vigente",
        "n_trozos": len(chunks),
        "n_tablas": len(clean_tables),
        "palabras": len(full_text.split()),
    }

    doc_folder = procesados_root / args.tema / args.periodo / f"{doc_id}-{utils.slugify(src.stem)}"

    if args.dry_run:
        print(f"   [dry-run] {len(chunks)} trozo(s), {len(clean_tables)} tabla(s)")
        print(f"   [dry-run] destino: {doc_folder}")
        print(f"   [dry-run] resumen: {resumen[:120]}")
        return 0

    # 4) Escribir trozos, tablas e indice
    doc_folder.mkdir(parents=True, exist_ok=True)
    out_size = 0
    chunk_files = []
    for chunk in chunks:
        name, sz = write_chunk_md(doc_folder, chunk)
        chunk_files.append((chunk["title"], name))
        out_size += sz
    table_schemas = []
    for i, table in enumerate(clean_tables, 1):
        name, sz, schema = write_table_csv(doc_folder, i, table)
        table_schemas.append(schema)
        out_size += sz
    out_size += build_index_md(doc_folder, fm, chunk_files, table_schemas, resumen or "(sin resumen)")

    # 5) Catalogo global
    index_rel = os.path.relpath(doc_folder / "_index.md", procesados_root)
    update_catalogo(procesados_root, fm, index_rel, resumen)

    # 6) Mover original a descartados (salvo --keep-original)
    if args.keep_original:
        motivo = "original conservado en entradas"
    else:
        descartados.mkdir(parents=True, exist_ok=True)
        target = descartados / src.name
        if target.exists():
            target = descartados / f"{src.stem}-{digest_hash[:8]}{src.suffix}"
        shutil.move(str(src), str(target))
        motivo = f"original movido a {target}"

    # 7) Log
    append_log(logs_dir, fm, src.name, str(doc_folder), "procesado", motivo)

    reduccion = (1 - out_size / in_size) * 100 if in_size else 0
    print(f"   OK -> {doc_folder}")
    print(f"   {len(chunks)} trozo(s), {len(clean_tables)} tabla(s); "
          f"salida {out_size / 1024:.1f} KB; reduccion {reduccion:.0f}%")
    print(f"   {motivo}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Procesa un documento a MD/CSV curados.")
    p.add_argument("--in", dest="input", required=True, help="Documento a procesar")
    p.add_argument("--tema", default="general")
    p.add_argument("--periodo", default=utils.current_period())
    p.add_argument("--workspace", default=".")
    p.add_argument("--resumen", choices=["none", "extractivo", "llm"], default="extractivo")
    p.add_argument("--max-chunk-chars", type=int, default=6000)
    p.add_argument("--origen-canal", default="desconocido")
    p.add_argument("--origen-id", default="desconocido")
    p.add_argument("--keep-original", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--llm-model", default="claude-haiku-4-5-20251001")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return process(args)
    except (ValueError, RuntimeError) as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())