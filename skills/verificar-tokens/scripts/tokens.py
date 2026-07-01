#!/usr/bin/env python3
"""
verificar-tokens — devuelve cuántos tokens ha gastado un usuario.

Busca al usuario por su CLAVE en USUARIOS.csv y lee su columna de tokens.
Salida (stdout), exactamente en el formato pedido:
    100 tokens

Estructura esperada de USUARIOS.csv:
    Clave,Identificadores,Usuario,Nombre Completo,Apodo,Nivel,Departamento,Estado, tokens_usados

(El encabezado " tokens_usados" puede traer espacios; se normalizan.)

Uso:
    python3 tokens.py <CLAVE>
    python3 tokens.py u-001
    python3 tokens.py u-001 --csv ../../bi/catalogos/USUARIOS.csv
"""
import argparse
import csv
import os
import sys

# nombres de columna aceptados (por si el encabezado varía).
# La búsqueda es por "Clave" (el ID único del usuario en USUARIOS.csv).
COL_ID = ["clave", "id", "identificadores", "identificador", "id_usuario", "user_id"]
COL_TOKENS = ["tokens_usados", "tokens", "tokens_gastados", "tokens_consumidos"]

# rutas donde intento encontrar el catálogo si no me pasan --csv
RUTAS_DEFECTO = [
    "bi/catalogos/USUARIOS.csv",
    "./bi/catalogos/USUARIOS.csv",
    "../bi/catalogos/USUARIOS.csv",
    "../../bi/catalogos/USUARIOS.csv",
    "../../../bi/catalogos/USUARIOS.csv",
]


def encontrar_csv(ruta_arg):
    if ruta_arg:
        return ruta_arg if os.path.exists(ruta_arg) else None
    for r in RUTAS_DEFECTO:
        if os.path.exists(r):
            return r
    return None


def col(fieldnames, candidatas):
    """Encuentra el nombre real de la columna (sin distinguir mayúsculas ni espacios)."""
    norm = {f.strip().lower(): f for f in fieldnames}
    for c in candidatas:
        if c in norm:
            return norm[c]
    return None


def main():
    ap = argparse.ArgumentParser(description="Tokens gastados por un usuario (por Clave).")
    ap.add_argument("clave", help="Clave del usuario en USUARIOS.csv (ej. u-001)")
    ap.add_argument("--csv", default=None, help="Ruta a USUARIOS.csv (opcional)")
    args = ap.parse_args()

    ruta = encontrar_csv(args.csv)
    if not ruta:
        print("Error: no encuentro USUARIOS.csv", file=sys.stderr)
        sys.exit(2)

    with open(ruta, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            print("Error: USUARIOS.csv vacío o sin encabezado", file=sys.stderr)
            sys.exit(2)
        c_id = col(reader.fieldnames, COL_ID)
        c_tok = col(reader.fieldnames, COL_TOKENS)
        if not c_id or not c_tok:
            print("Error: falta columna de Clave o de tokens en USUARIOS.csv", file=sys.stderr)
            sys.exit(2)

        objetivo = args.clave.strip().lower()
        for fila in reader:
            if (fila.get(c_id) or "").strip().lower() == objetivo:
                bruto = (fila.get(c_tok) or "").strip().replace(",", "")
                try:
                    tokens = int(float(bruto))
                except ValueError:
                    tokens = 0
                print(f"{tokens} tokens")
                return

    # no encontrado
    print("Usuario no encontrado", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
