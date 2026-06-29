"""Utilidades compartidas por la skill procesar-documento."""
from __future__ import annotations

import datetime as dt
import hashlib
import re
import unicodedata
from pathlib import Path

STOPWORDS = set("""
de la que el en y a los del se las por un para con no una su al lo como mas pero
sus le ya o este si porque esta entre cuando muy sin sobre tambien me hasta hay
donde quien desde todo nos durante todos uno les ni contra otros ese eso ante
ellos e esto mi antes algunos que unos yo otro otras otra el tanto esa estos mucho
quienes nada muchos cual sea poco ella estar haber estas estaba estamos algunas
algo nosotros the of to and in is it for on with as are be this that at by an or
from
""".split())


def now_iso() -> str:
    """Marca de tiempo ISO sin microsegundos."""
    return dt.datetime.now().replace(microsecond=0).isoformat()


def today() -> str:
    return dt.date.today().isoformat()


def current_period() -> str:
    """Periodo trimestral actual, p. ej. 2026-Q2."""
    d = dt.date.today()
    return f"{d.year}-Q{(d.month - 1) // 3 + 1}"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def slugify(text: str, maxlen: int = 50) -> str:
    text = unicodedata.normalize("NFKD", str(text))
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return (text[:maxlen].rstrip("-")) or "doc"


def gen_id(filename: str, digest: str) -> str:
    """Id estable derivado del año y del hash del contenido."""
    return f"DOC-{dt.date.today().year}-{digest[:8]}"


def yaml_escape(value) -> str:
    """Devuelve un escalar YAML seguro en una sola linea."""
    if value is None:
        return '""'
    s = str(value).replace("\n", " ").replace("\r", " ").strip()
    s = re.sub(r"\s+", " ", s)
    if s == "" or re.search(r'[:#\[\]{}",&*!|>%@`]', s) or s[:1] in "-? ":
        return '"' + s.replace('"', '\\"') + '"'
    return s