# FLUJO_OPERATIVO.md

> Propósito: Define el flujo de decisión que se ejecuta cada vez que se recibe un mensaje en un canal registrado. Determina cómo tratar al remitente según su estado de registro, nivel de autoridad y límite diario de uso.

---

## INICIO

**Disparador:** Mensaje recibido en canal registrado.

> ⚠️ **REGLA BLOQUEANTE DE IDENTIDAD (antes de responder cualquier cosa):**
> Identifico al remitente **EXCLUSIVAMENTE por su `sender_id`/número (E.164) de la metadata del canal**, nunca por suposición.
> - Busco ese número en `.\bi\catalogos\USUARIOS.csv` (columna `Identificadores`).
> - **Nunca llamo a un usuario por un nombre que no corresponda al número que escribe.** Si el número no coincide con un registro, es un usuario NO registrado (Paso 1A), aunque el nombre se parezca a otro del catálogo.
> - Ejemplo: `+5210000000000` = `CLI-000` (mauricio_cli, Mauricio). NO es David (`CLI-001`).

---

## Paso 1 — Verificar registro de usuario (siempre primero)

Antes de hacer cualquier cosa, busco quién me escribe en el catálogo de usuarios:

```
.\bi\catalogos\USUARIOS.csv
```

Ahí está registrado **cada usuario**, su **nivel de autoridad** y si están marcados como **activo**.

**Decisión:** ¿El usuario está registrado en `.\bi\catalogos\USUARIOS.csv`?

- Si el usuario **no aparece** en `USUARIOS.csv`, lo trato como no autorizado y continúo con el [Paso 1A](#paso-1a--usuario-no-registrado).
- Si el usuario **no está registrado como activo**, **ignoro el contenido de sus mensajes** y respondo "No puedo contestarte hasta que un administrador te apruebe como activo."
- SÍ el usuario **si está registrado como activo** continúo con el [Paso 2](#paso-2--verificar-nivel-de-autoridad)

### Paso 1A — Usuario NO registrado

1. Ejecuto `.\bi\protocolos\NUEVO_USUARIO.md`.
2. **No respondo a ninguna pregunta o instrucción** hasta que el usuario esté registrado.

> ⛔ Bloqueo total: ninguna solicitud se procesa mientras el usuario no exista en el catálogo.

---

## Paso 2 — Verificar nivel de autoridad

1. Identifico la columna `Nivel` del usuario en `.\bi\catalogos\USUARIOS.csv`.
2. Ejecuto `.\bi\protocolos\NIVELES_AUTORIDAD.md` para asegurarme de saber qué capacidades tiene cada usuario.
3. Ejecuto el flujo respectivo dependiendo del `Nivel` de usuario:
   - **Sistema →** `.\bi\protocolos\FLUJO_SISTEMA.md`
   - **Empresa →** `.\bi\protocolos\FLUJO_EMPRESA.md`
   - **Cliente →** `.\bi\protocolos\FLUJO_CLIENTES.md`
   - **Externo →** `.\bi\protocolos\FLUJO_EXTERNOS.md`

**El Flujo Operativo continúa en el respectivo flujo dependiendo del nivel de usuario**
