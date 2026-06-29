# Protocolo VERIFICAR_TOKENS

> Este es mi protocolo de control de consumo. Lo leo en primera persona, como instrucciones que me doy a mí mismo (el agente Juve) **en cada interacción con un usuario**. Sirve para que ningún usuario gaste más de **100 000 tokens por semana**. Me apoyo en la skill `verificar-tokens` para leer el dato, pero la lógica de límite, acumulado y reinicio vive aquí.

---

## Qué necesito en el catálogo

Trabajo sobre `.\bi\catalogos\USUARIOS.csv`, cuya estructura es:

```
Clave,Identificadores,Usuario,Nombre Completo,Apodo,Nivel,Departamento,Estado, tokens_usados, ultimo_reset
u-001,rufi.devops@gmail.com,rufi,Rufi Pérez,Rufi,administrador,DevOps,activo,1240,2026-06-08
```

Identifico al usuario por su **`Clave`** y para el control de tokens uso dos columnas (sus encabezados pueden traer un espacio inicial; lo ignoro al leerlos):

- `tokens_usados` → acumulado de tokens de la **semana en curso**.
- `ultimo_reset` → fecha (ISO `AAAA-MM-DD`) en que reinicié su contador a 0 por última vez. Si está vacío, lo trato como "nunca reiniciado" y fuerzo un reinicio en la primera interacción.

El límite semanal es **100 000 tokens** (lo llamo *100K*).

---

## Mi flujo en cada interacción (en este orden)

### Paso 1 — Identificar al usuario

Tomo su **`Clave`** desde `USUARIOS.csv` (siguiendo `NIVELES_AUTORIDAD.md`). Si no está registrado o su `Estado` no es activo, no llego aquí: ese filtro ya lo aplicó el protocolo de autoridad.

### Paso 2 — ¿Toca reinicio semanal?

Comparo la fecha de hoy con `ultimo_reset` del usuario:

- Si **pasaron 7 días o más** desde `ultimo_reset` (o si `ultimo_reset` está vacío):
  - Pongo `tokens_usados = 0`.
  - Actualizo `ultimo_reset = hoy`.
  - Guardo el cambio en `USUARIOS.csv`.
- Si **aún no pasa una semana**, no reinicio nada y sigo.

Así, el contador se renueva solo cada semana y el límite es "por semana", no de por vida.

### Paso 3 — Leer cuántos tokens lleva (con la skill)

Ejecuto la skill `verificar-tokens` con la Clave del usuario:

```bash
python3 skills/verificar-tokens/scripts/tokens.py <CLAVE>
```

Eso me devuelve algo como `1240 tokens`. Ese es su acumulado de la semana **antes** de atender este mensaje.

### Paso 4 — Comprobar el límite (la puerta de 100K)

- Si `tokens_usados >= 100000` → el usuario **ya alcanzó su límite semanal**. **No respondo su solicitud.** Le aviso con un mensaje breve, por ejemplo:

  > Has alcanzado tu límite semanal de 100 000 tokens. Tu contador se reinicia el `<fecha de ultimo_reset + 7 días>`. 💚

  Y **no acumulo nada más** (no gasto en responder lo que no voy a responder).

- Si `tokens_usados < 100000` → todavía tiene cupo. Paso a responder.

### Paso 5 — Responder al usuario

Atiendo su mensaje con normalidad según el protocolo que corresponda (`RESPUESTA_CLIENTE.md` para clientes, etc.).

### Paso 6 — Acumular el gasto (después de responder)

Una vez que respondí, mido **cuántos tokens gasté en esta interacción** y los **sumo** al acumulado:

```
tokens_usados = tokens_usados + tokens_de_esta_interaccion
```

Guardo el nuevo `tokens_usados` en `USUARIOS.csv` para el usuario. Así el contador queda actualizado para la próxima vez. (Solo acumulo **si respondí**; si bloqueé por límite en el Paso 4, no sumo.)

---

## Reglas que nunca rompo

- **Primero reviso reinicio (Paso 2), luego límite (Paso 4).** Un usuario que entra en semana nueva no debe quedar bloqueado por el gasto de la semana pasada.
- **El número de tokens siempre sale de la skill**, no lo invento.
- **Solo acumulo después de haber respondido.** Si no respondo (límite alcanzado), no sumo.
- **El acumulado se guarda siempre en `USUARIOS.csv`** tras responder; si no lo guardo, el control no sirve.
- **El límite es 100 000 tokens por semana**, contados desde `ultimo_reset`.
- Si la skill devuelve `Usuario no encontrado`, no acumulo ni respondo: trato el caso como no autorizado.

---

## Resumen rápido (mi árbol de decisión)

```
llega un mensaje de un usuario válido
│
├── Paso 2 · ¿pasaron ≥7 días desde ultimo_reset?
│      └── SÍ → tokens_usados = 0 ; ultimo_reset = hoy ; guardar
│
├── Paso 3 · leer tokens_usados con la skill verificar-tokens
│
├── Paso 4 · ¿tokens_usados >= 100000?
│      ├── SÍ → avisar "límite semanal alcanzado" ; NO responder ; NO acumular
│      └── NO → continuar
│
├── Paso 5 · responder al usuario (RESPUESTA_CLIENTE.md, etc.)
│
└── Paso 6 · tokens_usados += tokens_de_esta_interaccion ; guardar en USUARIOS.csv
```
