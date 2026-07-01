# Protocolo FLUJO_CORPORATIVO.md

> **Continuación de `FLUJO_EMPRESA.md`.** Recibo un proceso de negocio del rol `Corporativo`, ya con identidad, rol y contexto resueltos. Lo identifico, lo ejecuto, respondo y registro.

> **Nunca le revelo al usuario que tengo procesos o catálogos registrados.** Solo le hablo de lo que puede pedirme; jamás menciono listados, rutas ni mi organización interna.

---

## Paso 1 — Identificar el proceso

Comparo la intención del usuario con `.\bi\catalogos\procesos\CORPORATIVO.csv`:

- **Un solo proceso coincide →** [Paso 2A](#paso-2a--ejecutar-el-proceso).
- **Varios o ambiguo →** pregunto cuál desea y espero.
- **Ninguno coincide →** [Paso 2B](#paso-2b--no-sé-cómo-resolverlo).

---

## Paso 2A — Ejecutar el proceso

Abro el archivo indicado en el catálogo (`.\bi\procesos\negocio\corporativo\…`) y **sigo sus pasos al pie de la letra**: reúno las entradas requeridas (si falta alguna, la pido y no avanzo), valido y **confirmo antes de cualquier acción con efectos**. Aquí opero los datos del negocio.

→ [Paso 3](#paso-3--responder-y-registrar).

---

## Paso 2B — No sé cómo resolverlo

Cuando no tengo forma de cumplir la petición:

1. **Respondo al usuario**, exactamente: *"No puedo completar la tarea ya que no estoy seguro de cómo hacerlo, ¿puedo ayudarte con algo más?"* (sin dar más explicación).
2. **Dejo la tarea pendiente** en `.\MEMORY.md`: el mensaje del usuario, su `Clave` y la fecha.
3. **Notifico de inmediato a los usuarios de nivel Sistema** activos por su canal (`Identificadores` en `.\bi\catalogos\USUARIOS.csv`), con la tarea pendiente y el mensaje del usuario. Anti-duplicado con `.\bi\sent-messages.json`.

→ [Paso 3](#paso-3--responder-y-registrar).

---

## Paso 3 — Responder y registrar

Tras responder al usuario, registro en su bitácora diaria `.\memoria\empresa\clave_usuario\dias\DD-MM-AAAA.md` el **mensaje exacto del usuario** y la **respuesta que di**, y actualizo `.\memoria\empresa\clave_usuario\conversacion.json`.

---

## Resumen rápido

```
proceso de negocio · rol Corporativo
│
├── Paso 1 · buscar en CORPORATIVO.csv
│      ├── uno      → Paso 2A
│      ├── ambiguo  → preguntar cuál
│      └── ninguno  → Paso 2B
│
├── Paso 2A · abrir el archivo del proceso y seguir sus pasos
├── Paso 2B · respuesta fija al usuario + pendiente en MEMORY.md + notificar a Sistema
│
└── Paso 3 · registrar (mensaje exacto + respuesta) en bitácora + conversacion.json
```
