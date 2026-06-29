"""Resumen abstractive OPCIONAL. Unico modulo que usa la API del modelo.

Recibe un digest YA reducido (el resumen extractivo o un recorte corto), nunca el
documento completo, para mantener el costo al minimo. Si la API no esta disponible
o falla, devuelve None y el pipeline cae automaticamente al resumen extractivo.
La clave se lee de la variable de entorno ANTHROPIC_API_KEY.
"""
from __future__ import annotations

import os
import sys


def summarize_llm(digest: str, model: str):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        import anthropic
    except ImportError:
        return None
    try:
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model=model,
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": (
                    "Resume en 1-2 frases, en espanol, conservando datos y cifras "
                    "clave. Devuelve solo el resumen, sin preambulo:\n\n" + digest
                ),
            }],
        )
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text").strip()
    except Exception as exc:  # noqa: BLE001
        print(f"  [aviso] resumen LLM fallo ({exc}); uso extractivo.", file=sys.stderr)
        return None