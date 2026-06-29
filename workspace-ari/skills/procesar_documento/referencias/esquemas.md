# Referencia: esquemas y convenciones

Define la forma exacta de los archivos que produce y consume el pipeline, para que
sepas qué leer primero y dónde está cada dato.

## Jerarquía de consulta (de lo ligero a lo pesado)

Para no saturar tu contexto, consulta siempre en este orden y detente en cuanto
tengas lo que necesitas:

1. `datos/procesados/_catalogo.md` — índice global. **Léelo primero.**
2. `<carpeta-doc>/_index.md` — índice del documento (front-matter + resumen + TOC).
3. Trozos `NN-*.md` o tablas `tabla-NN.csv` — abre **solo** el que necesites.

## Estructura de salida

```
datos/procesados/<tema>/<periodo>/<id>-<slug>/
    _index.md          # front-matter + resumen + tabla de contenidos
    01-<seccion>.md    # trozos de texto limpios
    02-<seccion>.md
    tabla-01.csv       # tablas normalizadas
```

## Convención de nombres

- Id del documento: `DOC-<año>-<hash8>` (`hash8` = primeros 8 caracteres del sha256
  del contenido; estable y sirve para detectar duplicados).
- Carpeta del documento: `<id>-<slug-del-nombre>`.
- Trozos de texto: `NN-<slug-del-título>.md` (`NN` = orden: 01, 02, …).
- Tablas: `tabla-NN.csv`.
- Índice del documento: `_index.md`.

## Front-matter de `_index.md`

```yaml
---
id: DOC-2026-xxxxxxxx
origen_canal: whatsapp
origen_id: "+5215555555555"
fecha_recepcion: 2026-05-26
fecha_documento: ""        # se completa si se conoce la fecha del documento
tema: finanzas
periodo: 2026-Q2
tipo: md                   # md | csv
formato_original: pdf
hash_original: <sha256>
version: 1
resumen: "..."
estado: vigente            # vigente | superado
n_trozos: 3
n_tablas: 0
palabras: 49
---
```

## Catálogo global `datos/procesados/_catalogo.md`

Tabla con una fila por documento:

```
| id | ruta | tema | periodo | tipo | fecha_doc | origen | resumen | estado |
```

`ruta` apunta al `_index.md` relativo a `procesados/`; `origen` es `canal:id`;
`resumen` viene recortado a ~90 caracteres.

## Log de ingesta `datos/logs/ingesta-AAAA-MM.csv`

```
timestamp,canal,id_remitente,archivo,hash,decision,destino,motivo,agente
```

`decision` ∈ { `procesado`, `cuarentena`, `descartado`, `superado`,
`ignorado_remitente_no_registrado` }.

## Catálogo de remitentes `bi/catalogos/USUARIOS.md`

Tabla con los remitentes autorizados:

```
| id | nombre | canal | estado | notas |
```

`estado` ∈ { `Activo`, `Inactivo` }. El pipeline **no** valida esto: lo validas
**tú** según el protocolo `DOCUMENTOS_RECIBIDOS.md` antes de procesar (recuperas el
ID del remitente del canal y confirmas que exista y esté `Activo`).