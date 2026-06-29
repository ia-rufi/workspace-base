"""Resumen extractivo SIN API.

Puntua cada frase por la frecuencia (normalizada) de sus palabras significativas y
selecciona las mejores hasta un presupuesto de caracteres, conservando el orden
original. No usa el modelo: es la opcion por defecto.
"""
from __future__ import annotations

import re

from utils import STOPWORDS


def summarize_extractive(full_text: str, max_chars: int = 400) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", full_text.replace("\n", " "))
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    if not sentences:
        return full_text[:max_chars].strip()

    freq = {}
    for w in re.findall(r"\b[\wáéíóúñ]+\b", full_text.lower()):
        if w not in STOPWORDS and len(w) > 2:
            freq[w] = freq.get(w, 0) + 1
    if not freq:
        return " ".join(sentences)[:max_chars].strip()

    maxf = max(freq.values())
    scored = []
    for idx, s in enumerate(sentences):
        words = re.findall(r"\b[\wáéíóúñ]+\b", s.lower())
        score = sum(freq.get(w, 0) for w in words) / (len(words) or 1) / maxf
        scored.append((score, idx, s))
    scored.sort(reverse=True)

    chosen, total = [], 0
    for _, idx, s in scored:
        if total + len(s) > max_chars and chosen:
            break
        chosen.append((idx, s))
        total += len(s)
    chosen.sort()
    return " ".join(s for _, s in chosen).strip()