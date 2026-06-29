# Referencia: formatos soportados

Para cada formato, esta tabla indica qué librería usa el pipeline, qué extrae y en
qué se convierte. No necesitas memorizarla: el script decide solo según la
extensión. Consúltala si necesitas entender por qué un formato produjo cierta
salida o si falta una dependencia.

## Formatos admitidos

| Extensión | Librería | Qué extrae | Salida |
|-----------|----------|------------|--------|
| `txt`, `md` | nativo | Texto completo | MD por trozos |
| `csv` | nativo (`csv.Sniffer`) | Una tabla | CSV normalizado |
| `xlsx`, `xls` | openpyxl | Una tabla por hoja | CSV (uno por tabla) |
| `pdf` | pdfplumber | Texto por página + tablas | MD + CSV |
| `docx` | python-docx | Texto (detecta títulos) + tablas | MD + CSV |
| `pptx` | python-pptx | Texto por diapositiva + tablas | MD + CSV |
| `png`, `jpg`, `jpeg`, `tiff`, `bmp` | pytesseract + Pillow | Texto vía OCR (`spa+eng`) | MD |

## Reglas de conversión

- Datos tabulares (csv, xlsx, y las tablas dentro de pdf/docx/pptx) → **CSV**.
- Texto narrativo (txt, md, pdf, docx, pptx, OCR) → **MD** con front-matter.
- Un mismo documento puede producir **ambos**: trozos MD y varios CSV.

## Limpieza que se aplica al texto (lossless)

- Une palabras cortadas por guion al final de renglón (`docu-\nmento` → `documento`).
- Elimina líneas que son solo número de página.
- Quita encabezados/pies que se repiten en más del 50% de las páginas (pdf).
- Colapsa espacios y saltos de línea redundantes.
- Deduplica párrafos idénticos.
- **Nunca altera números ni datos.**

## Limpieza que se aplica a las tablas

- Elimina filas completamente vacías.
- Elimina columnas completamente vacías **y sin nombre**. Una columna con
  encabezado se conserva aunque venga sin datos (borrarla sería perder un campo).

## Formatos no soportados / bloqueados

- Si la extensión no está en la tabla, el pipeline termina con error
  `Formato no soportado` (código 1). En ese caso **debes mover el archivo a
  `cuarentena/`** y registrarlo.
- Los ejecutables (`exe`, `bat`, `sh`, `scr`, `msi`) y los archivos con macros sin
  verificar (`docm`, `xlsm`) **no deben llegar al pipeline**: la compuerta de
  seguridad del protocolo `DOCUMENTOS_RECIBIDOS.md` los manda a `cuarentena/` antes.

## Dependencias

Las librerías se importan de forma perezosa: si falta una, solo falla ese formato,
con un mensaje claro. Instálalas con `pip install -r requirements.txt`. El OCR
requiere además el binario `tesseract` instalado en el sistema. TXT, MD y CSV no
necesitan nada externo.