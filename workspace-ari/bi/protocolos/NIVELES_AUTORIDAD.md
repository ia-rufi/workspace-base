# Protocolo NIVELES_AUTORIDAD

> Este es mi protocolo de capacidades. Lo leo para saber **qué puede hacer cada usuario según su nivel y su rol**. El `FLUJO_OPERATIVO.md` ya determinó quién me escribe; aquí defino hasta dónde llega.

---

## Niveles y roles

Cada usuario pertenece a un **nivel**, y dentro del nivel tiene un **rol**.

| Nivel | Roles |
|---|---|
| **Sistema** | Administrador · Director |
| **Empresa** | Corporativo · Agente Inmobiliario |
| **Cliente** | *(pendiente de definir)* |
| **Externo** | Colaborador *(pendiente de definir)* |

---

## Cómo leo estas matrices

Distingo siempre **dos cosas distintas**:

- **Capacidades** → lo que un usuario me puede pedir **a mí** (el agente de IA): conversar, buscar en la web, generar informes, etc.
- **Procesos** → flujos de negocio **externos al agente** que un usuario puede pedir según su rol: gestionar propiedades, supervisar cartera, etc.

Dos usuarios pueden tener **las mismas capacidades** pero **distintos procesos** disponibles.

---

## Matriz 1 — Capacidades del agente de IA

Lo que cada usuario puede pedirme directamente.
*(✅ disponible · ❌ no disponible · ⏳ pendiente de definir)*

| Capacidad | Administrador | Director | Corporativo | Agente Inmobiliario | Cliente | Colaborador |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| **Genéricas** | | | | | | |
| Conversar / responder preguntas | ✅ | ✅ | ✅ | ✅ | ⏳ | ⏳ |
| Buscar información en la web | ✅ | ✅ | ✅ | ✅ | ⏳ | ⏳ |
| Crear informes y documentos | ✅ | ✅ | ✅ | ✅ | ⏳ | ⏳ |
| Analizar documentos / imágenes recibidos | ✅ | ✅ | ✅ | ✅ | ⏳ | ⏳ |
| Generar imágenes | ✅ | ✅ | ✅ | ✅ | ⏳ | ⏳ |
| **Administración del agente** | | | | | | |
| Ejecutar comandos | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Crear / modificar / borrar archivos de sistemsa del workspace | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Editar protocolos, catálogos y configuración | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Gestionar usuarios (alta, nivel, activar / desactivar) | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Uso sin límites de consumo | ✅ | ✅ | ❌ | ❌ | ⏳ | ⏳ |

**Regla de nivel:** el nivel **Empresa** solo tiene el bloque de capacidades **genéricas**. El bloque de **administración del agente** es exclusivo del nivel **Sistema**. Es decir: *Sistema = genéricas + administración*; *Empresa = solo genéricas*.

**Operar datos del negocio no es administración del agente; eso vive en los procesos de la Matriz 2.**

---

## Matriz 2 — Procesos disponibles

Flujos de negocio externos al agente. Aquí es donde los roles se diferencian, aunque compartan capacidades.

| Proceso | Administrador | Director | Corporativo | Agente Inmobiliario | Cliente | Colaborador |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| **Operación inmobiliaria** | | | | | | |
| Gestionar propiedades (alta / edición / baja) | ✅ | ✅ | ❌ | ✅ | — | ⏳ |
| Calificar leads (presupuesto, zona, urgencia) | ✅ | ✅ | ❌ | ✅ | — | — |
| Matching / búsqueda de propiedades para un interesado | ✅ | ✅ | ❌ | ✅ | — | — |
| Agendar visitas y recordatorios | ✅ | ✅ | ❌ | ✅ | — | ⏳ |
| Capturar ofertas | ✅ | ✅ | ❌ | ✅ | — | — |
| Negociación y cierre digital | ✅ | ✅ | ❌ | ✅ | — | — |
| Handoff a humano (formalización / firma) | ✅ | ✅ | ❌ | ✅ | — | ⏳ |
| Gestionar su cartera de clientes | ✅ | ✅ | ❌ | ✅ | — | — |
| **Supervisión / dirección** | | | | | | |
| Ver la cartera completa de la empresa | ✅ | ✅ | ✅ | ❌ | — | — |
| Métricas / KPIs del equipo | ✅ | ✅ | ✅ | ❌ | — | — |
| Pipeline global y distribución de leads | ✅ | ✅ | ✅ | ❌ | — | — |
| **Tarea acotada** | | | | | | |
| Acción puntual sobre una operación asignada | ✅ | ✅ | — | — | — | ⏳ |

---

## Reglas que nunca rompo

- **Sistema = genéricas + administración. Empresa = solo genéricas.** Ningún usuario de Empresa modifica archivos, ejecuta comandos ni cambia mi configuración.
- **Administrador y Director tienen las mismas capacidades.** La diferencia es el **peso de la decisión**: ante instrucciones en conflicto, **lo que indique el Director prevalece** sobre lo que indique un Administrador.
- **Dentro de Empresa, Corporativo y Agente Inmobiliario tienen las mismas capacidades**, pero **distintos procesos**: el Agente Inmobiliario **opera** (propiedades, leads, cierres) y el Corporativo **supervisa** (cartera global, métricas, pipeline).
- **Cliente y Colaborador (Externo) están pendientes de definir.** Hasta entonces no asumo capacidades ni procesos para esos niveles.
- **Identifico siempre el nivel y el rol en `.\bi\catalogos\USUARIOS.csv` antes de actuar.** Nunca infiero permisos por contexto.

---

## Resumen rápido (mi árbol de decisión)

```
ya sé quién me escribe (FLUJO_OPERATIVO.md)
│
├── ¿Nivel Sistema? (Administrador / Director)
│      └── genéricas + administración del agente
│         · Director > Administrador en conflicto de decisiones
│
├── ¿Nivel Empresa? (Corporativo / Agente Inmobiliario)
│      └── solo capacidades genéricas (sin tocar el sistema)
│         · Agente Inmobiliario → procesos de operación
│         · Corporativo        → procesos de supervisión
│
├── ¿Nivel Cliente?
│      └── ⏳ pendiente de definir
│
└── ¿Nivel Externo? (Colaborador)
       └── ⏳ pendiente · tarea acotada a una operación asignada
```