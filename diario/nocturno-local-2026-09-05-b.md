# Nocturno local — 2026-09-05-b

**Trabajador:** worker nocturno local (Matías durmiendo). **Segundo turno** de la
noche — el primero fue `nocturno-local-2026-09-05.md` (galgas, la potencia que
nadie cambió).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA — prioridad #1 de la
jerarquía**), zona `servidor/` únicamente.
**Branch:** `nocturno/local-2026-09-05-b-el-aviso-que-se-rinde`
(pusheado, `758560f`). **Sale de `main` (`2ac3a7d`) limpio.**
**No toca firmware, ni panel, ni `supabase/`, ni `hardware/`.**
**Migración append-only e idempotente** (sólo `ADD COLUMN IF NOT EXISTS` /
`CREATE INDEX IF NOT EXISTS`).

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_frioseguro`, ya
eliminado) porque el árbol de `frioseguro` tiene el KiCad de Matías sin commitear
(`hardware/mini`, `hardware/mini_lite`, los dos `.zip`) y un `checkout` lo habría
tocado. **Verificado al terminar: el árbol quedó idéntico**, en el branch
`nocturno/local-2026-09-04-b` donde estaba.

---

## TL;DR

> **La cola de avisos del servidor propio reintentaba sin esperar.** Cuando un
> envío fallaba, la fila volvía a la cola con el mismo `due_at` —ya en el
> pasado—, así que se reintentaba 30 s después contra el mismo error, y a los
> cinco intentos quedaba `failed`. **La vida entera de un aviso al cliente eran
> dos minutos.** Dos minutos de Telegram devolviendo 502, o del servidor sin
> salida a internet, y el aviso al comerciante moría para siempre, en silencio,
> mientras la cámara se calentaba. "Cinco intentos" sonaba a política de
> reintento; era una ráfaga.

## Por qué esta tarea

1. **Es PLATA y es el núcleo de lo que se cobra.** El abono se paga por *"el
   servicio avisa"*. Las últimas cuatro noches cerraron ese camino del lado del
   equipo (la sonda que se cae, la temperatura congelada, el aviso que no sale
   por Telegram). Éste es **el último tramo**, el del servidor propio, y era el
   único que quedaba sin mirar.
2. **Está libre.** Revisé los 34 branches abiertos de frioseguro: el único que
   toca `api/tareas.py` es el del 09-03-b, y lo hace agregando
   `_limpiar_sesiones()` al final del archivo. `_despachar_avisos()` no lo tocó
   nadie. (También descarté el ítem 18 del `QUE_FALTA` —el bug de defrost/
   cooldown en `alerts.h`— porque **ya está arreglado** en
   `nocturno/local-2026-08-18-fix-alert-delay-defrost`; el `QUE_FALTA` no lo
   dice y por poco lo hago dos veces.)
3. **Es 100 % software y se verifica sin base, sin Docker y sin hardware.**

## El agujero, y por qué nadie lo veía

```python
for n in pendientes:
    ok, detalle = canales.enviar(...)
    if ok:  ... status='sent' ...
    else:
        nuevo_estado = "failed" if n["intentos"] >= 4 else "queued"
```

La fila vuelve a `queued` **sin tocar `due_at`**, y la consulta es
`WHERE status='queued' AND due_at <= NOW()`. O sea que el "reintento" es la
pasada siguiente del bucle, 30 s después. Cinco pasadas = 2 min de vida.

Tres disfraces, y ninguno es un descuido:

1. **En el banco no falla nunca.** Con internet y el token bien puesto, el
   primer intento sale y los cinco reintentos no se ejercitan jamás. El código
   que se rompe es el que sólo corre el día que algo anda mal.
2. **El número 5 no tenía unidad.** Nadie escribió "cinco intentos son dos
   minutos". Escrito así se ve solo; escrito como `intentos >= 4`, no.
3. **El canal que siempre falla juraba que no perdía nada.**
   `canales.enviar('push', ...)` devolvía `False` con el comentario *"la fila
   queda en la cola, no se pierde"*, y `servidor/SEGURIDAD.md` §4.5 lo repetía
   palabra por palabra. Las dos capas leídas por separado están bien; el
   despachador, dos archivos más allá, las contradecía. **Una organización cuyas
   reglas sean sólo `push` estaba pagando y no recibiendo nada, nunca, y nadie
   se enteraba.** Es el mismo patrón que la sonda caída y la temperatura
   congelada: dos módulos correctos, el agujero justo en el medio.

## Lo que salió al arreglarlo (y no estaba en el plan)

**1. Con más de un cliente, uno roto tapaba a todos.** La consulta es
`ORDER BY due_at LIMIT 50`, y una fila trabada nunca se movía al futuro:
**50 avisos rotos de UNA organización bloqueaban la cola de las otras cuatro.**
En un servicio multi-tenant, un `chat_id` mal cargado en un cliente dejaba sin
avisos a los demás. El aislamiento sale gratis del mismo cambio — al postergar
la fila, deja de ocupar lugar en el `LIMIT`.

**2. Un problema de Telegram se convertía en un problema de ingesta.** Los
envíos estaban **adentro** del `with pool().connection()`. Cada uno puede tardar
hasta 10 s y la tanda es de 50: una sola pasada podía retener una conexión más
de 8 minutos, sobre un pool de `max_size=5` (chico a propósito, dice `base.py`)
que comparten las cinco tareas de fondo y el api por el que los equipos publican
sus lecturas.

**3. Un reinicio a mitad de tanda mandaba todo de nuevo.** Con una sola
transacción al final, si el contenedor se reiniciaba en el medio se perdía el
registro de lo ya enviado: en el arranque siguiente el cliente recibía la misma
alerta **dos veces**. Ahora cada resultado se escribe apenas se conoce, en su
propia transacción, y el peor caso es un aviso repetido.

## Qué se entregó

`servidor/api/logica/reintentos.py` — **puro** (sin base, sin red, sin reloj
propio, sólo stdlib), mismo criterio que `logica/silencio.py`. Cuatro reglas:

| # | Regla | Por qué |
|---|---|---|
| 1 | **El reintento espera**: backoff 1, 2, 5, 10, 20, 30 min, en la columna nueva `proximo_intento_at` | Reintentar 30 s después contra el mismo error no es reintentar |
| 2 | **Se abandona por el primero de DOS topes**: 12 intentos o **6 h desde que el aviso vencía** | Un aviso de "la cámara está a −2 °C" entregado medio día tarde no es un aviso, es una molestia. El tope de intentos solo no alcanzaba; la ventana sola tampoco |
| 3 | **Tres clases de falla y sólo una se reintenta**: `transitorio` (timeout, 5xx, 429) · `permanente` (400 = chat_id inexistente, **403 = el cliente bloqueó al bot**, 401 = token revocado) · `no_entregable` (canal sin implementar o sin configurar) | Reintentar un 403 doce veces no desbloquea al bot; lo que hace falta es llamar al cliente |
| 4 | **Lo que se abandona se avisa**, en UN solo mensaje por pasada | Si se cae el token del bot mueren de golpe los avisos de todas las orgs: 40 WhatsApps se silencian igual de rápido que ninguno |

**`due_at` NO se pisa**, a propósito: es el paso del escalado ("a los 15 minutos,
llamar"). Sobreescribirlo con la hora del próximo reintento borraría a qué hora
correspondía avisar, que es justo lo que uno quiere leer después de un
incidente. Por eso `proximo_intento_at` es columna nueva y la consulta usa
`COALESCE(proximo_intento_at, due_at)`.

**La clase se decide en `canales.py`**, donde todavía se tiene el código HTTP y
el tipo de excepción. Adivinarla más arriba parseando el string del error sería
frágil justo en el camino del que depende que el cliente se entere.

Columna nueva `falla_clase` (`error` ya guardaba el detalle, pero un texto libre
no se agrupa), para que esto sea una consulta y no una arqueología:

```sql
SELECT org_id, falla_clase, COUNT(*)
  FROM notifications WHERE status='failed' GROUP BY 1,2 ORDER BY 3 DESC;
```

Y corregí la mentira donde estaba escrita: `canales.py` y `SEGURIDAD.md` §4.5.

## Cómo verificarlo (comandos exactos, sin hardware, sin base, sin Docker)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-09-05-b-el-aviso-que-se-rinde

cd servidor/api && python -m unittest discover -s tests -t .
```

**Resultados obtenidos esta noche:**

- **57 tests OK, 0 fallos.** Baseline de `main` medido antes de tocar nada:
  **42**. O sea **15 nuevos**, todos del trabajo de esta noche.
- **Cinco están escritos como regresión, y comprobé que fallan contra la
  política vieja**: reimplanté la lógica de "5 intentos sin backoff" en un
  script descartable y le corrí encima esos cinco tests → **5 failures**. Son
  `test_una_caida_transitoria_no_mata_el_aviso`,
  `test_el_reintento_se_posterga_no_es_inmediato`,
  `test_al_vencer_la_ventana_aunque_queden_intentos`,
  `test_rechazo_permanente_no_se_reintenta_nunca` y
  `test_canal_sin_implementar_no_consume_reintentos`.
- `python -m compileall -q servidor/api` → **OK** (los `__pycache__` se
  borraron; no entraron al commit).

## Qué quedó SIN verificar (pide la base andando — de día)

Cinco escenarios, detalle en `docs/notification-retry.md`:

1. Aplicar `servidor/sql/072_reintento_avisos.sql` — lo hace solo el corredor de
   migraciones de `base.py` al arrancar — y confirmar las 2 columnas y 2 índices.
2. Encolar un aviso a un `chat_id` inexistente → `failed` con
   `falla_clase='permanente'` **en el primer intento**, y que llegue el mensaje
   de infraestructura.
3. Encolar uno con el bot apagado / sin red → `queued` con `proximo_intento_at`
   ~1 min adelante, y ver crecer las esperas 1, 2, 5, 10…
4. Una regla `push` activa → `failed` con `falla_clase='no_entregable'`.
5. Resolver la alerta a mitad del backoff → el trigger `cancelar_avisos()` la
   deja en `cancelled` y el despachador no vuelve a tomarla.

## Nota de merge

Sale de `main` (`2ac3a7d`) limpio. **Colisión posible con un solo branch**:
`nocturno/local-2026-09-03-b-el-aviso-que-se-da-por-dado`, y sólo en
`api/tareas.py` — él agrega `_limpiar_sesiones()` al final del archivo, yo
reescribo `_despachar_avisos()` que está mucho más arriba, más una línea de
`import` y una en `arrancar()`. Es añadido contra añadido: **se resuelve
quedándose con los dos lados**. Con el resto (incluido el 09-04-b de anoche, que
sólo toca `servidor/sql/070_validez_temperatura.sql`), ninguna.

**Numeré la migración 072 a propósito.** Hay **dos** `070_*` pendientes en
branches distintos: `070_cuentas_personas.sql` (09-03-b) y
`070_validez_temperatura.sql` (09-04-b). Como los nombres difieren, conviven y
el corredor los aplica los dos en orden alfabético — no es un choque, pero
conviene saberlo antes de mergear, y por eso me salteé el 071.

## Anotado y NO tocado

- **Drift en el `QUE_FALTA.md` de frioseguro**: el ítem 18 ("cerrar hallazgo de
  la decisión de alerta") sigue pidiendo un fix que **ya está hecho** en
  `nocturno/local-2026-08-18-fix-alert-delay-defrost` — el branch corrige
  `alerts.h` (reinicia `highTempSec` y re-ancla `lastAlertCheck` al salir de
  defrost/cooldown, y clampea el hueco con `ALERT_MAX_SAMPLE_GAP_MS`). Casi lo
  hago dos veces. No lo corregí para no generar conflicto con ese mismo branch;
  se resuelve al mergearlo. [@cronista]
- **El resumen mensual va a decir que avisó.** El "este mes: 2 alertas, 0
  pérdidas" (ítem 11) cuenta **alertas**, no **entregas**. Con `falla_clase` ya
  se puede distinguir "alerta abierta" de "cliente enterado"; hacerlo toca ese
  entregable y es de @backend.
- **`notifications` no tiene índice por `alert_id`**, y `cancelar_avisos()`
  filtra por ahí en cada resolución. Con volumen chico no se nota.
- **`notificar_matias` sigue sin reintentar.** Si el aviso de infraestructura no
  sale, queda en el log del contenedor y lo levanta el vigía externo. Era una
  decisión ya tomada en `canales.py`; no la cambié.
- **El truncamiento de `deltaMs / 1000` en `alerts.h`** (firmware) hace que el
  reloj del retardo de alerta corra **siempre lento, nunca rápido**: pierde el
  resto en cada tick. Está adentro del branch del 08-18, así que no lo toqué —
  pero vale mirarlo cuando ese branch se mergee. [@firmware]

## Estado del repo

`C:\Proyectos\frioseguro` quedó **exactamente como estaba** (el KiCad sin
commitear de Matías, intacto, en el branch del 09-04-b). El worktree temporal
`C:\Proyectos\_noche_frioseguro` se eliminó. El branch está pusheado y el
`QUE_FALTA.md` actualizado (ítem 21).
