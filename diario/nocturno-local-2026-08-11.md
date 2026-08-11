# Nocturno local — 2026-08-11

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-11-cadena-entrega` (pusheado, `5413c8f`).

## Tarea elegida y por qué

Por rotación tocaba galgas: los dos turnos de ayer fueron datalogger y
frioseguro, y galgas no se toca desde el 08-09-b.

Repasé el `QUE_FALTA`. Los 🔴 sin branch siguen siendo hardware puro (#1 RX
completo necesita LCD+buzzer, #3 LiPo real, #4 reflashear B) y de los 🟡 el #5,
#6 y #8 ya los cubrió el contrato de schema. Los 19 branches previos cubren
vpp/umbrales, energía, alertas, linaje, OTA, readme-drift, contrato de comandos,
identidad de binarios, contrato de schema y —anteanoche— la cadena de medición.

**La cadena de medición del 08-09-b termina donde empieza el hueco**: sigue el
número desde el ADC hasta que existe y significa lo correcto **en la RAM del
emisor**. De ahí en adelante, nadie miró nada. La pregunta que elegí:

> el número que se midió bien, **¿llega? ¿llega una sola vez, y con qué hora?
> y si no llega, ¿alguien se entera?**

Elegí este tramo sobre cualquier otro por tres razones concretas:

1. Es la **precondición de los ítems #1 y #11** del QUE_FALTA, los dos sobre la
   topología de entrega ("rol gateway HTTP del PLAN v5", "validar el híbrido
   punta a punta"). El que ejecute el #1 se va a comer las trampas que encontré.
2. Es **la mitad del DoD de octubre que nadie chequeó nunca**: el DoD dice,
   textual, *"reportando a Supabase **con fallback local**"*. No existe.
3. El modo de falla de esta cadena **no es un crash ni un número raro: es
   silencio que se ve igual que salud**. Es exactamente el tipo de cosa que en
   planta se descubre tarde y caro.

## Qué hice

**`tools/check_delivery_chain.py`** (stdlib, solo lectura, sin nube ni hardware,
no compila nada, no entra a `data/field_captures`). Modela los cuatro tramos
—POST del emisor → [gateway RX | Supabase directo] → `readings` →
`last_seen_at` → presupuesto de silencio del SCADA— leyendo el código real de
las dos familias de emisor, el RX, las 15 migraciones y las **dos** vistas del
dashboard. Exit 0/1/2/3, `--json`, `--fail-on`, `--root`.

**Dos oráculos numéricos** que demuestran los hallazgos con números en vez de
afirmarlos:

- `--demo-queue` replica `fwdEnqueue`/`fwdWorkerTick` del RX con sus parámetros
  reales (8 slots, 3 reintentos, backoff 2 s, timeout 6 s): **un corte de 5 min
  de Supabase se lleva 12 lecturas que el emisor da por entregadas**. Detalle
  contraintuitivo: las 41 rechazadas con 503 son las *buenas* — el 503 es
  honesto, la cola es lo que produce la mentira.
- `--demo-silence` cruza el período de reporte de cada perfil contra los dos
  umbrales de "offline" del dashboard: **`palerta` tiene la ventana ciega más
  ancha (7.5× el período)**, justo el perfil que corre cuando hay una alerta.

**`tools/test_check_delivery_chain.py` — 69 tests en 7 capas:** utilidades de
texto, extractores sobre fuentes sintéticas, los dos oráculos con números
fijados a mano, un test por código de hallazgo con repos sintéticos armados en
disco, **control negativo** (un repo sano no enciende nada, y cada defecto
inyectado por separado enciende sólo su código), regresión sobre el repo real y
el CLI.

**`docs/delivery-chain.md`** — el análisis completo y el orden de arreglo por
costo-de-no-arreglarlo.

Lo que hubo que resolver:

- **De nuevo la rama muerta, y de nuevo en la dirección que absuelve.**
  `discoverGatewayUrl()` tiene el cuerpo real dentro de un `#else` que no
  compila (`#if 1 → return String();`). Leyendo el texto plano, el tool concluye
  "la familia modular usa gateway con mDNS" — exactamente al revés de la verdad.
  Es la misma lección del `#ifdef DEV_SIMULATE_ADC` del 08-09-b, así que esta
  vez la resolví en la utilidad (`active_preproc`) en vez de caso por caso.
- **El presupuesto de silencio no se juzga por su valor sino contra el período
  del que reporta.** `SILENCE_S.palerta = 30 s` es un número razonable… hasta que
  ves que el perfil reporta cada 10 s en un ciclo que tarda 5-8 s. La regla
  correcta es la razón umbral/período, no el umbral.
- **Al hallazgo de la cola no alcanzaba con afirmarlo.** "El RX puede perder
  datos" es una frase; "12 lecturas por corte de 5 minutos, y el emisor cree que
  las entregó" es una decisión de ingeniería. Por eso el oráculo — y por eso
  está declarado en el doc que **12 es cota superior** (el modelo no frena al
  WebServer durante el POST upstream; en el firmware real ese stall salva
  algunas por timeout del emisor).
- **Un contador que existe pero no viaja.** El RX ya cuenta `fwdDropped` y lo
  expone en `GET /health`… que vive en la LAN de planta. No lo consume nadie y
  no va en el PATCH del heartbeat, así que desde Bahía Blanca la pérdida es
  invisible. Es el arreglo más barato de toda la lista.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **4 error · 4 warn.**

| código | sev | qué |
|---|---|---|
| **D1** | error | el RX responde `200 {"queued":true}` y **después** forwardea: el emisor cree que entregó y se va a deep sleep. Tras 3 reintentos el item se descarta (el propio firmware lo loguea como `DATO PERDIDO`) y la cola son 8 slots de RAM: un reboot del RX se lleva 8 lecturas ya reconocidas. **12 por corte de 5 min** (oráculo). |
| **D2** | error | ninguna familia persiste la lectura que no pudo entregar (buscado: RTC array, NVS, LittleFS, SPIFFS, SD). POST fallido → `goSleep()` → la RAM se borra. **El DoD promete "fallback local".** Agrava en la modular: con el gateway apagado hay **un solo intento por wake**. |
| **D3** | error | las dos familias re-postean el **mismo body** por otra ruta. `readings` no tiene UNIQUE ni índice único, el body no lleva clave de idempotencia ni `Prefer: resolution=merge-duplicates` → un timeout post-commit inserta la fila dos veces. Y como `v_pp` **es** la alerta, un burst duplicado en el borde del umbral pesa doble. |
| **D5** | error | el presupuesto de silencio está escrito **tres veces** (período del firmware, fórmula de `App.jsx`, tabla `SILENCE_S` de `PlantaView`) y las dos vistas **discrepan en los 5 perfiles**. La misma card puede estar `warn` en una pantalla y `OFFLINE` en la otra, con los mismos datos y en el mismo instante. PlantaView es la que ve Dreyfus. |
| **D7** | error | `FW_VERSION` de los emisores modulares es `"0.8.1-A-otatest"`; el regex de perfil de las dos vistas (`/-(p[a-z]+)$/`) no matchea → ambas caen al fallback (300 s y 600 s), pero los modos modulares reportan cada 600 s y 3600 s. **Un emisor modular sano se ve permanentemente OFFLINE** — y es la familia que se flashea para octubre (#1 y #4). Cry-wolf del 07-28-b, ahora en el eje del tiempo. |
| **D4** | warn | `readings.ts` es `default now()` y nadie manda `ts`: la hora de la fila es la de **llegada**. Un forward reintentado llega hasta 24 s tarde con esa hora. Para el informe de Dreyfus importa: correlacionar A contra B en el tiempo *es* el análisis. |
| **D8** | warn | `fwdNextTry` es variable de archivo, no campo del item: la cabeza que falla frena la cola entera. Con A fallando, las lecturas **sanas** de B se atrasan 2 s por intento ajeno. |
| **D9** | warn | las dos familias no acuerdan la topología: modular con gateway **apagado** (decisión del 26-04, contradice PLAN_v3 §1.1), monolítico con `EN_GATEWAY 1` por `devices.local_ip`. Además la rama de fallback modular es **código muerto**, y si se reactiva sólo cubre `<=0` y `502`: un 500/503/504 del relay **no** dispara el reintento. Trampa puesta para el que ejecute el #1. |
| **D10** | warn | `firmware/shared/gateway_relay.h` no lo incluye nadie pero sigue ahí, con `MDNS.begin()` y proxy transparente de cualquier path (incluido `/storage/`). mDNS está descartado por doctrina. Un `#include` distraído reabre la puerta. |

**Orden de arreglo sugerido** (por costo de no arreglarlo antes de octubre, no
por dificultad): D7 y D5 primero — son de hoy, sin hardware, y hasta arreglarlos
cualquier prueba de campo arranca con el SCADA mintiendo. Después D2+D3 juntos
(si se va a reintentar, primero hay que poder reintentar sin duplicar). Después
D1/D8 como decisión de diseño. D4 es barato. D9/D10 es limpieza que el #1 va a
necesitar igual. Detalle completo en `docs/delivery-chain.md`.

## Cómo verificarlo

```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-11-cadena-entrega

python tools/test_check_delivery_chain.py     # 69 tests -> OK
python tools/check_delivery_chain.py          # informe; exit 2 (hay errores)
python tools/check_delivery_chain.py --demo-queue     # la tabla de perdida
python tools/check_delivery_chain.py --demo-silence   # la ventana ciega
python tools/check_delivery_chain.py --json | python -m json.tool | head -40
```

Verificado en esta máquina: `py_compile` de los dos archivos, los 69 tests en
verde (2.9 s), el auditor devolviendo exit 2 sobre el repo real y los dos
oráculos imprimiendo sus tablas. **No se tocó una sola línea de firmware, de
`web/` ni de SQL** — el branch agrega tres archivos y nada más, así que no hay
build de dashboard que correr.

## Qué quedó sin verificar (necesita hardware o red)

- **Los 12 de la cola son de un modelo, no de un RX midiendo.** Se validan con
  un corte de WiFi inducido en la prueba de resistencia del ítem #10.
- **La duplicación (D3) es *posible* según el código; falta ver una fila
  duplicada real.** Forma barata de verla: cortar el upstream a mitad de un POST
  y contar filas por `(device_id, boot_count)` en `metadata`.
- **Nada de red real:** el auditor no abrió una conexión ni consultó Supabase.

## Estado

Branch pusheado, `QUE_FALTA.md` de galgas actualizado con la marca EN BRANCH en
los ítems #1 y #11. Nada pendiente de esta máquina.
