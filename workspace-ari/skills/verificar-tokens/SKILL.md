---
name: verificar-tokens
description: Consulta cuántos tokens ha gastado un usuario registrado en USUARIOS.csv y responde en el formato "100 tokens". Úsala siempre que alguien pregunte por el consumo o gasto de tokens de un usuario, diga cosas como "cuántos tokens gastó X", "tokens de X", "consumo de X", o use el comando \tokens. La búsqueda es por la Clave del usuario.
---

# verificar-tokens

Devuelvo cuántos tokens ha gastado un usuario, leyendo el catálogo de usuarios. No calculo ni estimo el número a ojo: **siempre ejecuto el script**, que lee el dato exacto del CSV.

## Cuándo la uso

- "¿Cuántos tokens ha gastado u-001?"
- "tokens de u-003"
- "consumo de tokens del usuario u-007"
- comando `\tokens u-001`

## Fuente de datos

`.\bi\catalogos\USUARIOS.csv` — la búsqueda es **por `Clave`** (el ID único del usuario). Estructura del catálogo:

```
Clave,Identificadores,Usuario,Nombre Completo,Apodo,Nivel,Departamento,Estado, tokens_usados
u-001,rufi.devops@gmail.com,rufi,Rufi Pérez,Rufi,administrador,DevOps,activo,1240
```

- Busco la fila por `Clave`.
- Leo la columna **`tokens_usados`** (su encabezado puede traer un espacio inicial; el script lo normaliza).
- El orden de las columnas no importa: el script las ubica por nombre de encabezado, no por posición.

## Cómo la ejecuto

```bash
python3 scripts/tokens.py <CLAVE>
# ejemplo:
python3 scripts/tokens.py u-001
```

Opcional, si el catálogo está en otra ruta:

```bash
python3 scripts/tokens.py u-001 --csv ./bi/catalogos/USUARIOS.csv
```

## Qué respondo

- **Usuario encontrado** → repito tal cual la salida del script, p. ej.:

  ```
  100 tokens
  ```

- **Usuario no encontrado** (la Clave no está en el CSV) → lo digo claramente: `Usuario no encontrado`. No invento un número.

## Reglas

- Nunca adivino el número de tokens; siempre lo saco del script.
- Respondo en el formato exacto `<N> tokens`.
- Respeto `NIVELES_AUTORIDAD.md`: esta consulta es para **Administrador** o **Corporativo**. Si quien pregunta es Cliente, no la ejecuto.
