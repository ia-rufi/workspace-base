---
name: procesar-documento
description: >
  Usa esta skill en el proceso nocturno (o cuando haya archivos en datos/entradas/)
  para convertir documentos pesados (PDF, Word, Excel, PowerPoint, CSV, TXT, MD e
  imágenes con OCR) en archivos MD/CSV pequeños, limpios sin perder datos y con un
  índice ligero. El trabajo pesado lo hacen scripts de Python; tú solo diriges el
  proceso y, opcionalmente, redactas un resumen corto.
---

# Skill: procesar-documento

Eres el responsable de curar los documentos que llegan a `datos/entradas/`. Tu
trabajo aquí es de **dirección, no de ejecución**: el script `scripts/pipeline.py`
extrae, limpia, particiona, convierte e indexa por su cuenta. Tú decides qué
documento procesar y con qué parámetros, lanzas el comando y revisas el resultado.

## Regla principal: trabaja lo mínimo

No leas el documento completo en tu contexto ni intentes transformarlo por tu
cuenta. Para eso está el pipeline. Tu intervención se limita a tres cosas: elegir
`tema` y `periodo`, ejecutar el comando y verificar la salida. Solo usa la API del
modelo (`--resumen llm`) cuando el resumen automático no baste; en ese caso el
script envía al modelo únicamente un fragmento ya reducido, nunca el documento
entero.

## Cuándo debes usarla

Debes ejecutarla cuando se dispare el proceso nocturno o cuando encuentres archivos
pendientes en `datos/entradas/`. Procesa **un documento a la vez**.

## Qué debes hacer, paso a paso

1. Lista los archivos en `datos/entradas/`.
2. Para cada archivo, determina su `tema` (ver más abajo) y el `periodo` que le
   corresponde (por ejemplo `2026-Q2`).
3. Ejecuta el pipeline:

   ```bash
   python scripts/pipeline.py \
     --in datos/entradas/<archivo> \
     --tema <tema> \
     --periodo <periodo> \
     --workspace . \
     --resumen extractivo
   ```

4. Lee la salida que imprime el script (ruta destino, número de trozos/tablas y %
   de reducción) y confírmala contra la sección de verificación.
5. No muevas ni borres nada a mano: el script ya mueve el original a
   `descartados/` y registra todo en `datos/logs/`.

## Cómo debes elegir el `tema`

Antes de asignar el tema, revisa los **tres archivos base** del agente —
`IDENTIDAD.md`, `INSTRUCCIONES.md` y `CONTEXTO.md` (en la raíz del workspace)— para
saber cuál es tu giro y qué áreas maneja la empresa. Asigna el tema que mejor
encaje. Si ningún tema encaja, el documento no debió llegar hasta aquí: no lo
proceses, déjalo donde está y repórtalo para revisión humana.

## Parámetros que debes pasar

| Argumento | Cuándo usarlo |
|-----------|---------------|
| `--in` | Ruta del documento. Obligatorio. |
| `--tema` | El tema que decidiste según los archivos base. |
| `--periodo` | El periodo del documento (p. ej. `2026-Q2`). |
| `--workspace` | La raíz del workspace (normalmente `.`). |
| `--resumen` | `extractivo` por defecto. Usa `llm` solo si el resumen extractivo queda pobre. `none` si no quieres resumen. |
| `--origen-canal` / `--origen-id` | Pásalos si conoces el remitente (canal e ID), para que queden en el front-matter. |
| `--keep-original` | Úsalo solo si quieres conservar el original en `entradas/`. |
| `--dry-run` | Úsalo para previsualizar sin escribir ni mover nada. |

## Qué hace el script por ti (no lo repliques)

El pipeline extrae el contenido según el formato; limpia sin perder datos (quita
encabezados/pies repetidos, números de página, une líneas cortadas, deduplica y
**nunca altera números**); parte el contenido en trozos por estructura o tamaño;
convierte tablas a CSV y prosa a MD con front-matter; genera el `_index.md` del
documento; agrega una fila a `datos/procesados/_catalogo.md`; escribe el log; y
mueve el original a `descartados/`. Tú no haces nada de esto a mano.

## Cuándo debes usar `--resumen llm`

Por defecto usa `extractivo` (sin API). Cambia a `llm` solo cuando el documento sea
denso o crítico y el resumen extractivo no capture bien la idea. El script enviará
al modelo solo el digest extractivo, no el documento. Si la API no está disponible,
hará *fallback* automático al extractivo.

## Después de ejecutar, debes verificar

Confirma que se creó la carpeta del documento con su `_index.md`, que `_catalogo.md`
tiene la fila nueva y que el original ya no está en `entradas/` (salvo que usaras
`--keep-original`). Si algo falla, **no muevas el original tú**: déjalo en
`entradas/` y registra el problema para revisión humana.

## Estructura de la skill

```
procesar_documento/
  SKILL.md
  requirements.txt
  scripts/
    pipeline.py            # orquestador: el único que ejecutas
    utils.py               # helpers compartidos (ids, hash, slugify, fechas)
    extract.py             # extrae contenido por formato
    clean.py               # limpieza lossless de texto y tablas
    partition.py           # parte en trozos manejables
    to_csv.py              # escribe tablas a CSV
    to_md.py               # escribe trozos y el _index.md
    index.py               # actualiza _catalogo.md y el log
    resumen_extractivo.py  # resumen sin API
    resumen_llm.py         # resumen con API (único módulo que la usa)
  referencias/
    formatos.md            # qué formato usa qué extractor y en qué se convierte
    esquemas.md            # front-matter, catálogo, nombres, log, USUARIOS.md
```

Las librerías de cada formato se importan de forma perezosa: si falta una, el
script solo falla para ese formato y lo reporta. TXT, MD y CSV no requieren nada
externo (ver `requirements.txt`).

Consulta `referencias/formatos.md` cuando necesites saber qué hace el pipeline con
un formato concreto, y `referencias/esquemas.md` para la forma exacta del
front-matter, el catálogo, los nombres de archivo y el log.