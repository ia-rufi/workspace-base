# Proceso: «nombre del proceso»

> Plantilla base. Todo archivo de `bi/procesos/` sigue esta misma estructura, para que el agente ejecute el proceso **siempre de la misma manera** y los resultados no varíen.

---

## Identificación

- **Tipo:** genérico | negocio
- **Rol / nivel que puede ejecutarlo:** _(ej. Agente Inmobiliario · o "Sistema + Empresa" si es genérico)_
- **Cuándo se usa (disparador):** _(la intención del usuario que activa este proceso; debe coincidir con su fila en `CATALOGO.md`)_

## Entradas requeridas

Datos que **necesito tener antes de empezar**. Si falta alguno, lo pido y **no avanzo** hasta tenerlos.

- _(dato 1)_
- _(dato 2)_

## Datos del negocio que toca

- **Leo:** _(catálogo o archivo de datos del negocio que consulto)_
- **Escribo:** _(catálogo o archivo que modifico, si aplica)_
- _(Nunca toco archivos de sistema desde un proceso de negocio.)_

## Pasos

Numerados y determinísticos. Los sigo en orden, sin saltar ni improvisar.

1. _(paso)_
2. _(paso)_
3. _(paso)_

## Validaciones y confirmaciones

- _(qué verifico antes de escribir/confirmar)_
- _(si la acción tiene efectos, confirmo con el usuario antes de ejecutarla)_

## Respuesta al usuario

- _(qué le confirmo al terminar — sin revelar rutas ni la organización del workspace a usuarios que no sean de nivel Sistema)_

## Registro

- Anoto el resultado en la bitácora diaria del usuario: `.\memoria\«nivel»\clave_usuario\dias\DD-MM-AAAA.md`.