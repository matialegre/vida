# Nocturno local — 2026-08-17-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-17-b-eventos-alerta` (pusheado, `48870a3`).

## TL;DR

**Esta noche no es una auditoría: es la implementación de una.**

Diez branches nocturnos de galgas esperan merge y todos, salvo uno, son
análisis. El del 08-15-b (cadena de aviso) terminó con un hallazgo #1 que no
necesitaba más estudio, sólo código:

> *«Ningún firmware emite un evento de alerta. Ninguno. 24 llamadas a
> `emitEvent()` en todo el repo —OTA, boots, calibración, factory reset— y
> **cero** de alerta. La tabla `events`, el vocabulario que declara el schema
> (`alert_start`/`alert_end`), el índice parcial de alertas y el Realtime del
> dashboard **ya están**. Falta que alguien escriba la fila.»*

Escribí esa fila. Y encontré, al hacerlo, que **escribirla no alcanzaba**:

- **El SCADA no conoce el vocabulario que declara su propio schema.**
  `mapTag()` del `PlantaView` —el feed que mira la planta— conoce `alerta`,
  `alert`, `self_trigger`, `alert_clear`, `cleared`: nombres del mockup y del
  firmware monolítico. **No conoce `alert_start` ni `alert_end`**, que es lo que
  declara la migración inicial. Un `alert_start` caía al `return 'boot'` final
  de la función: **el feed de planta lo mostraba en gris, con icono de OK, como
  un arranque cualquiera.** Emitir el evento sin este fix habría producido filas
  correctas e invisibles — el peor resultado posible, porque se ve hecho.
- **Las dos vistas filtran por una severidad que la base no puede tener.**
  Comparan `severity === 'warn'`; el CHECK del schema permite `info`, `warning`,
  `error`, `critical`. `'warn'` a secas nunca matchea. Y no había color para
  `'critical'`, que es justamente la del `alert_start`: caía al gris de default.
- **El metadata del evento no entraba en el parser.** El patrón copiado de
  `supabasePostReading` re-parsea el JSON en un `StaticJsonDocument<256>`. Los 8
  campos del evento dan ~250 B: al borde. Con 256 el evento habría viajado **sin
  metadata y sin decir nada** (`deserializeJson` devuelve `NoMemory` y el
  `if (!e)` simplemente omite el campo). Va a 384 B y ahora loguea el fallo.

## Tarea elegida y por qué

Jerarquía: PLATA y UNIVERSIDAD primero, **octubre segundo**. Galgas es octubre y
es el repo que le tocaba por rotación (última vez 08-15-b). Pero el criterio
real fue otro: **de todo el `QUE_FALTA` de galgas, éste era el único ítem
bloqueante que se podía cerrar entero sin tocar hardware.** Los otros tres
piden galga física, LiPo real o un ESP32 en la mano.

Y había una razón de fondo para dejar de auditar por una noche: la definición de
«listo para octubre» del repo dice *«con alertas visibles en el SCADA»*. Ese
renglón estaba, literalmente, sin una sola línea de código que lo cumpliera.

## Qué hice

### Firmware — `firmware/shared/supabase_client.{h,cpp}`

`supabasePostEvent(device_id, event_type, severity, message, metadata_json)`.
Mismo patrón `HTTPClient` que el resto del cliente (la lección TLS ya pagada no
se toca). Dos detalles que no son cosméticos: `severity` vacía cae al DEFAULT
del schema en vez de mandar `""` —que rebotaría con 400 por el CHECK— y el doc
de parseo del metadata pasa a 384 B por lo de arriba.

### Firmware — `esp_a_emisor` y `esp_b_emisor` (byte-idénticos salvo `DEVICE_ID`)

| Transición | evento | severity | `metadata.reason` |
|---|---|---|---|
| `v_pp > SELF_TRIGGER_VPP_V` estando fuera de ALERTA | `alert_start` | `critical` | `n/a` |
| 10 wakes seguidos sin alerta (`ALERT_EXIT_CONSECUTIVE`) | `alert_end` | `info` | `streak` |
| cap de 1 h en ALERTA (`ALERT_MAX_DURATION_S`) | `alert_end` | `info` | `cap` |

**Uno por transición, no por lectura.** El emisor ya distinguía transición de
estado permanente (`if (current_mode != MODE_ALERTA)`); el evento cuelga de ese
mismo `if`. Un episodio de 6 h da 1 `alert_start` y 1 `alert_end`, no 390.

**El evento se encola en RTC slow memory y sobrevive el deep sleep.** Perder una
lectura cuesta una muestra de muchas; perder el `alert_start` borra el episodio
entero del timeline, porque es la única fila que lo declara. `queueAlertEvent()`
guarda el slot, `flushPendingAlertEvent()` postea donde ya hay TLS, y el slot
**sólo** se libera con un 2xx — hasta `ALERT_EVENT_MAX_RETRIES=10` wakes. A los
10 wakes sin red el nodo está incomunicado y el aviso ya no sirve para que nadie
actúe.

Tres decisiones que van con eso:

- `updateAlertState()` **sigue sin depender de la red**. Sólo encola: el
  self-trigger es local y la transición de modo no puede quedar atada a que
  salga un POST.
- El flush va **antes de commands/OTA**: el OTA puede terminar en `ESP.restart()`
  y llevarse el evento sin mandar.
- El `metadata` lleva `boot_count` y `retries`. **El emisor no tiene reloj** y
  `events.ts` lo pone Postgres; sin esos dos campos, un `alert_start` reintentado
  seis wakes después es indistinguible de uno recién ocurrido. (Es el mismo
  problema que el nocturno del 08-16-b encontró en FrioSeguro; acá al menos
  queda declarado en la fila.)
- `alert_streak` del `alert_end` es **cuántos wakes duró el episodio**: se
  captura al encolar, porque las dos ramas de salida lo resetean a 0 acto
  seguido. Leerlo en el flush daba 0 siempre.

`FW_VERSION` → `0.9.0-{A,B}-eventos`.

### Dashboard — `web/src/views/PlantaView.jsx` y `web/src/App.jsx`

`mapTag()` aprende el vocabulario del schema (`alert_start`, `alert_end`,
`sensor_fault`) manteniendo los legacy. Un `sevColor()` único reemplaza las dos
tablas de color que discrepaban entre sí y con la base.

## Cómo verificarlo

Hecho en este branch, sin hardware:

```bash
cd C:\Proyectos\galgas
arduino-cli compile --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs firmware/esp_a_emisor
arduino-cli compile --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs firmware/esp_b_emisor
arduino-cli compile --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs firmware/esp_rx_receptor
cd web && npm run build
```

Los tres sketches compilan con esp32 core 3.3.8 (ya instalado, no hubo que bajar
nada). **Costo medido contra el baseline compilado antes de tocar nada:
+2976 bytes de flash** (1235392 → 1238368, 62 % de la partición) y **0 bytes de
RAM dinámica** — los 6 slots nuevos viven en RTC slow memory (14 bytes), que no
entra en ese número. El RX se compiló para confirmar que el cambio en la
`shared` no lo rompe: sigue igual.

`web/ npm run build` → 394 módulos, OK en 5,4 s.

## Qué quedó sin verificar (necesita hardware)

1. **Que la fila llegue.** El POST a `/rest/v1/events` con la anon key: la policy
   `insert_events_anon` existe en la migración, pero nunca se ejerció desde un
   emisor. Comprobación: disparar alerta y
   `select event_type, severity, message, metadata from events where device_id='A' order by ts desc limit 5;`
   → **exactamente una** fila `alert_start` por episodio.
2. **El reintento.** Cortar el WiFi antes del POST del evento y dejar pasar
   wakes: el serie debe decir `reintento 1/10`, `2/10`… y al volver la red, un
   solo `alert_start` con `retries > 0` en el metadata.
3. **El feed.** Que la pestaña Planta muestre tag rojo `alert` y después verde
   `cleared` — no gris `boot`.
4. **El falso positivo.** El branch `nocturno/local-2026-07-29-vpp-field-characterization`
   documentó que el self-trigger v3 sin `HOLD_SEC` convierte dropouts de 0,0 V en
   alertas espurias (3 % con motor ON). **Ahora esos dropouts también escriben un
   `alert_start`.** El fix del hold es previo a poner esto en planta: si no, el
   feed de Dreyfus se llena de alertas de mentira y nadie lo mira más.

## Lo que este branch NO hace (a propósito)

- **El RX no emite estos eventos.** Tiene su propio `emitEvent()` y su propio
  `anyAlert()` derivado de lo que le llega de A y B; hacerlo emitir también
  duplicaría cada episodio. La fuente de verdad de una galga es su emisor.
- **No hay notificación.** Mail, Telegram, sirena: nada. Esto deja la fila
  escrita y visible en pantalla. El aviso que sale *de* la pantalla sigue siendo
  el hallazgo abierto de la cadena de aviso del 08-15-b.
- **No se tocó el umbral, ni `data/field_captures/`, ni el RX, ni nada de red
  del PLAN v5.**

## Nota para el Director

Galgas tiene ahora **once branches nocturnos sin mergear**, diez de los cuales
son análisis. La deuda ya no es de diagnóstico. Este branch es el primero que
convierte un hallazgo en código y, al hacerlo, apareció algo que ninguna
auditoría había visto: **el dashboard no habla el idioma de su propio schema.**
Ese tipo de drift sólo se cae cuando alguien intenta usar las dos puntas juntas.

Vale la pena una sesión de día para pasar los branches por `@verificador` y
mergear los que corresponda. Cada auditoría que espera es una que la próxima
puede estar repitiendo sin saberlo.

**Próximo paso concreto:** flashear A con `0.9.0-A-eventos`, forzar una alerta
en banco, y mirar `events` + el feed de Planta. Es media hora con el ESP32 en la
mano.

---

**Higiene del cuartel:** MATI-HQ tenía cambios sin commitear al arrancar la
noche (16 archivos modificados en `agentes/`, `dominios/`, `enlace/` y 4 sin
trackear, entre ellos `propuestas/MAIL_SAE_PPS.md` y `dominios/diseno3d.md`).
**No los toqué ni los commiteé**: son trabajo tuyo en curso, no mío. Este commit
sólo agrega este informe. El branch de galgas sí quedó pusheado y limpio.
