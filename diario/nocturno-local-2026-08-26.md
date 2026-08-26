# Nocturno local — 2026-08-26

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la jerarquía).
**Branch:** `nocturno/local-2026-08-26-el-hueco-y-el-reloj` (pusheado, `a93ef03`).
**Sale de:** `main`. **No depende de ningún otro branch nocturno de frioseguro** —
crea dos headers nuevos y toca `supabase.h` / `web_api.h`, que ningún otro branch
abierto modifica.

## TL;DR

> **Cuando se cae el router, las lecturas no se demoran: se borran. Y el equipo no
> sabe qué hora es, así que ni siquiera podría volver a ponerlas en su lugar.**

El patrón que dispara todo está en `supabaseSync()`, y es de una línea:

```c
if (now - state.lastSupabaseSync >= INTERVAL_SUPABASE_SYNC_MS) {
  state.lastSupabaseSync = now;                 // <-- el reloj avanza IGUAL
  if (state.internetAvailable) supabaseSendReading();
}
```

El `lastSupabaseSync = now` está **arriba** del `if`. La lectura no se posterga:
**no existe**. A 10 s por lectura, un corte de router de 6 horas son **2160
lecturas** que nunca pasaron — y el hueco que dejan en `readings` es
indistinguible de *"no pasó nada"*, que es exactamente el escenario contra el que
se vende el abono.

**Y un segundo agujero en la misma línea, que la auditoría no había nombrado:**
`supabaseSendReading()` devuelve `bool` y **nadie lo mira**. Con internet
perfectamente disponible, un 500 de Supabase perdía la lectura con el mismo
silencio. El `if` no cubría el modo de falla más común, cubría el más obvio.

## Tarea elegida y por qué

Por rotación tocaba frioseguro: las últimas noches fueron datalogger (08-24) y
galgas (08-25), y frioseguro venía del 08-23 — el más viejo junto con cosechador.
La jerarquía manda **PLATA**, así que desempata solo.

Dentro del repo seguí el patrón que viene funcionando: **no abrir una auditoría
nueva, tomar un pendiente ya nombrado con su evidencia.** La auditoría
`08-14-b cadena-continuidad` dejó su lista de arreglos **en orden**, y ese orden
decide solo:

1. **R7 + R1** — hechos anoche de frioseguro (branch `08-23`).
2. **R5** (`#include "power_monitor.h"`) — **enciende hardware** (GPIO34/35 con
   optoacoplador). Es una línea que no se puede verificar de noche: meterla a
   ciegas en el firmware de un equipo que se actualiza por OTA es exactamente lo
   que no hay que hacer.
3. **R3 — el buffer offline.** ← ésta.

Además de que le tocaba por orden, R3 cambió de peso desde que se escribió. La
auditoría lo había puesto cuarto con este argumento: *"es el más caro y el que
menos urge: sin R7, los datos recuperados llegan a un sistema que igual no
avisó"*. **R7 ya está hecho** (branch `08-23`), así que esa condición se cumplió.

Y hay un tercer motivo que no estaba en la auditoría: **la instalación de Santa
Cruz** (`SESION_1_FRIOSEGURO_SANTACRUZ.md`, sin commitear) va sobre **redes WiFi
abiertas a 1500 km**, con portales cautivos. Eso no es "el router se cae de vez en
cuando": es el modo normal de operación de ese equipo. R3 es el hallazgo que más
directo le pega.

## Qué hice

**Lo que no se entrega, se guarda.** `firmware_modular/offline_buffer.h` (nuevo):
cola circular estática de **180 × 28 B = 5068 B**, **sin `Arduino.h`**, para poder
correrla en la PC.

```c
if (now - state.lastSupabaseSync >= INTERVAL_SUPABASE_SYNC_MS) {
  state.lastSupabaseSync = now;
  bool delivered = false;
  if (state.internetAvailable) delivered = supabaseSendReading();
  if (!delivered) supabaseCaptureOffline();
}
if (state.internetAvailable && !g_offlineBuffer.empty()) supabaseFlushOfflineBuffer();
```

**Las dos decisiones que definen la cola, y por qué esas:**

| | decisión | por qué |
|---|---|---|
| cadencia offline | **60 s**, no 10 | a 10 s la cobertura cae a **30 minutos** en los mismos 5 KB. Una heladera no cambia de historia en 10 segundos: lo que el cliente necesita ver de un corte es **la curva**, y a 1 minuto la curva está entera. 180 × 60 s = **3 h**. |
| cola llena | **diezma**, no tira | descartar el más viejo se come justo **el principio del corte**, que es el dato que contesta *"¿cuándo empezó a subir?"*. Tirar una de cada dos **y duplicar el período** dobla la cobertura y parte la resolución al medio: 3 h → 6 h → 12 h → 24 h … hasta 192 h en el techo. **Los dos extremos sobreviven siempre.** |

Duplicar el período junto con el diezmado no es cosmético: sin eso la cola se
vuelve a llenar en el mismo tiempo y **diezma en cascada**. Y recién en el techo
(6 diezmados) se empieza a descartar el más viejo — contado en `discarded`, no en
silencio.

**Y la pieza sin la cual todo lo anterior sería PEOR que el problema:**

> **El firmware no tiene reloj.** No hay NTP —el `QUE_FALTA #9` dice *"validar
> NTP"*, pero **no está escrito**: no hay un solo `configTime()` en el repo— ni
> RTC. `millis()` sabe cuánto hace que arrancó, no qué hora es.

Mientras todo se manda en el momento no importa: `readings.created_at` tiene
`DEFAULT NOW()` y el que pone la hora es Postgres. **En el momento en que una
lectura se guarda para mandarla después, deja de alcanzar.** Un buffer que
reenvía sin `created_at` mete las 180 lecturas de un corte de 3 horas **todas en
el mismo minuto**: una pared vertical de datos falsos donde antes había un hueco
honesto. Eso es peor que no hacer nada.

**La hora ya estaba llegando cada 10 segundos y se tiraba.** Toda respuesta HTTP
de Supabase trae `Date: Wed, 26 Aug 2026 03:14:07 GMT`.
`firmware_modular/device_clock.h` (nuevo) ancla `(epoch_del_servidor, millis())`
en cada POST exitoso y reconstruye la hora de cualquier instante pasado con una
resta. **Sin NTP, sin RTC y sin una sola request nueva.**

- **Sin reloj válido el buffer NO se drena.** Espera. Como el ancla se pone con el
  primer POST exitoso posterior a la reconexión, esa espera dura a lo sumo un
  ciclo de sync. Prefiero que el dato espere un minuto a que entre con hora falsa.
- Ancla de más de 24 h → el reloj se declara inválido (y de paso queda muy por
  debajo del wrap de `millis()` a los 49,7 días).
- `Date` corrupto o fuera de la banda 2026–2100 → se rechaza y **no pisa el ancla
  buena**.

**Dos cosas más del mismo tirón:**

- **Las filas recuperadas se marcan: `system_state = "buffered"`.** La columna
  **ya existe** en el esquema y no la usaba nadie: **cero migración**. Sin la
  marca, el panel muestra un tramo con `wifi_rssi` / `ping_ms` / `free_heap`
  vacíos y parece un bug. (Esas columnas no se guardan a propósito: la salud del
  enlace en un instante sin enlace no dice nada.)
- **El corte tiene que poder verse mientras pasa.** `/api/status` publica ahora un
  bloque `buffer` con `pending`, `oldest_sec`, `period_sec`, `decimations`,
  `captured` / `flushed` / `discarded`, `high_water`, `clock_valid` y
  `clock_syncs`. **Un corte ya no se ve como lecturas que faltan: se ve como una
  cola que crece.** Sin publicarlo, el corte volvería a ser invisible desde
  afuera — sólo que ahora encima con los datos adentro del equipo.

**Archivos:** `firmware_modular/offline_buffer.h` (nuevo, 221),
`firmware_modular/device_clock.h` (nuevo, 211), `firmware_modular/supabase.h`
(+163/-1), `firmware_modular/web_api.h` (+25/-4), `tools/test_offline_buffer.cpp`
(nuevo), `tools/mutantes_offline_buffer.py` (nuevo),
`tools/check_offline_buffer_wiring.py` (nuevo),
`tools/test_check_offline_buffer_wiring.py` (nuevo), `docs/offline-buffer.md`
(nuevo), `QUE_FALTA.md` (#20), `.gitignore`.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-26-el-hueco-y-el-reloj

# 1. la POLITICA se corre de verdad, sin ESP32 -> 1332 checks OK
g++ -std=c++17 -Wall -Wextra -O1 -o tools/test_offline_buffer.exe tools/test_offline_buffer.cpp
./tools/test_offline_buffer.exe

# 2. los tests no son decorativos -> los 27 mutantes mueren
python tools/mutantes_offline_buffer.py
python tools/mutantes_offline_buffer.py --lista

# 3. el CABLEADO del .ino, que g++ no ve -> 33/33
python tools/check_offline_buffer_wiring.py
python tools/check_offline_buffer_wiring.py --json
python -m unittest tools.test_check_offline_buffer_wiring     # 21 tests

# 4. el firmware compila con el core ESP32 real (~2 min la 1a vez)
arduino-cli compile --fqbn esp32:esp32:esp32 firmware_modular
```

**Verificado esta noche:**

- **La política se ejecutó de verdad, sin ESP32.** `tools/test_offline_buffer.cpp`
  incluye los **headers reales** (no una copia) y los corre en g++ con un **reloj
  falso**: `millis()` es una variable, así que un corte de 6 horas se simula en
  microsegundos. **1332 checks, 0 fallando.**
  Los que importan: `test_corte_de_seis_horas` — 2160 lecturas ofrecidas durante
  el corte, la cola guarda 180 diezmando a 2 min, **el primero y el último de la
  serie sobreviven**, cada uno se re-fecha correctamente al reconectar
  (`2026-08-26T03:14:07Z` … `09:12:07Z`) y se drenan **en orden en 6 requests**.
  Y `test_contabilidad_cierra`: sobre 3000 rondas con reconexiones esporádicas,
  `captured == flushed + discarded + size`. **No hay tercer destino: nada se
  evapora.**
- **Mutación: 27 mutantes, los 27 caen.** Cadencia offline igual a la online,
  primera muestra rechazada, tirar el más viejo en vez de diezmar, diezmar sin
  duplicar el período, quedarse con las impares, **compactar desde el índice 0
  (que pisa el buffer circular cuando `head != 0`)**, diezmado sin techo, descarte
  sin contar, `popFront` que saca de más, lote sin tope, `offer` que no sella el
  instante, y 12 del reloj (zona horaria ignorada, banda de cordura, epoch pisado
  al fallar, ancla que nunca vence, `epochAtMillis` que ignora la antigüedad —o
  que suma en vez de restar—, calendario sin bisiestos, ISO sin la `Z`…).
  El script trabaja sobre una **copia** en un temporal: no toca el repo.
- **El sketch compila con el core ESP32 real** (`arduino-cli`, no sólo sintaxis).
  Comparé contra `main` compilando los dos: **flash 1 288 696 → 1 294 204 B
  (+5508 B, +0,42 %)** y **RAM 53 784 → 58 872 B (+5088 B)**, que son exactamente
  los 5068 B de la cola más los 20 del reloj.
- **El checker estático, 33/33**, con **21 tests** que rompen un hecho por vez y
  verifican que **falle el check correcto y sólo ése**. Vigila lo que g++ no
  puede ver: que el patrón viejo de R3 no vuelva, que se mire el **resultado** del
  POST y no sólo si hay internet, que el `Date` se pida antes del request y se lea
  **antes de `http.end()`**, que sin reloj no se drene, que `popFront` sólo se
  llame con un 2xx en la mano, y que `offline_buffer.h` / `device_clock.h` **no
  ganen un `#include <Arduino.h>`** — el día que lo ganen, la única verificación
  que existe deja de compilar.

**Dos cosas que arreglé del propio harness, y que valen más que un test más:**

- **Un mutante colgaba la corrida entera.** Sin tope, `mutantes_offline_buffer.py`
  se quedaba esperando para siempre a un mutante que deja los tests en un lazo
  infinito. Ahora corre con timeout de 60 s y eso se reporta como `CUELGA`
  (también es "el test se dio cuenta", pero acotado). Y les puse tope a los tres
  `while` del test que podían no terminar: una política rota tiene que **hacer
  fallar** el test, no colgarlo.
- **Un mutante sobrevivió y estaba bien que sobreviviera.** El primer intento de
  romper la cadencia fue cambiar la resta `uint32_t` de `due()` por una
  comparación con signo. **Sobrevive**: en complemento a dos las dos formas dan lo
  mismo en los dos bordes (el de `0xFFFFFFFF` y el de `0x80000000`), y la
  diferencia real es *undefined behavior*, no comportamiento observable. **No le
  inventé un test que no puede existir**: reemplacé ese mutante por uno que sí se
  distingue (`>` en lugar de `>=`) y lo dejé escrito en el doc.

## Lo que quedó SIN verificar (y por qué)

- **Nada corrió en hardware.** Ni un corte real, ni un drenaje real, ni un POST
  real.
- **Que `HTTPClient` del core ESP32 devuelva el header `Date`.** Se usa
  `collectHeaders()` + `header("Date")`, que es la API documentada, y Supabase
  manda `Date` en toda respuesta (es obligatorio en HTTP/1.1). **Pero nadie lo
  ejecutó.** Es la suposición de la que cuelga todo el reloj. Si fallara, el
  buffer **no drena** (no drena mal: no drena) y `buffer.clock_syncs` se queda en
  0 — por eso ese contador está publicado en `/api/status`. **Es lo primero que
  hay que mirar en el banco.**
- **Que PostgREST acepte el insert de un array de 30 filas** con `Prefer:
  return=minimal`. Está en la doc y es el uso normal, pero el firmware nunca
  mandó un array hasta ahora.
- **Que `created_at` explícito no choque con nada.** Es una columna con `DEFAULT
  NOW()`, sin trigger que la pise en `readings` (el trigger
  `update_device_last_seen` toca `devices`, no `readings`). Verificado leyendo el
  esquema, no ejecutando.
- ⚠️ **El sketch quedó en 98,7 % de flash (1 294 204 / 1 310 720 B).** `main` ya
  estaba en 98,3 %, así que **no es este branch** — pero quedan **16 516 bytes** y
  lo próximo que se agregue no va a entrar. Hay partition schemes con más app en el
  mismo módulo (`min_spiffs` da 1,9 MB). **Es una decisión de despliegue y es
  tuya**, pero conviene tomarla antes de la próxima feature, no cuando el compile
  falle.
- **Las alertas y los eventos de puerta siguen perdiéndose durante el corte.**
  `supabaseSendAlert()` y `door_events` mantienen su `if (!internetAvailable)
  return`. La cola guarda **lecturas**; el estado de alerta viaja adentro de cada
  lectura recuperada, así que el histórico muestra que la alerta estuvo activa,
  **pero la fila de `alerts` de ese momento no existe.** Es el próximo escalón y
  es más chico ahora que la infraestructura está.
- **Sigue abierto R2** (el firmware no recalcula `state.wifiConnected`;
  `reconnectWiFi()` sigue sin un solo call site) y **R5** (`ac_power` sin el
  `#include`). El buffer funciona igual porque se dispara con
  `internetAvailable`, que sí se recalcula cada 30 s en `checkInternet()`.
- **Lo escribí y lo verifiqué yo.** El checker compara contra `config.h` y el
  esquema —que son referencia, no algo mío— pero **una lectura de @firmware antes
  del banco vale**: lo que hay que buscar es si `supabaseCaptureOffline()` omite
  algo que el POST en vivo sí manda y que el histórico vaya a necesitar.

## Próximo paso (para Matías, de día)

1. **Mergear.** Sale de `main` y no depende de nadie. Con el `08-23` (R1+R7) son
   complementarios y no se pisan: **el `08-23` cubre el corte de LUZ** (equipo
   muerto, avisa la nube) y **éste el corte de RED** (equipo vivo y mudo, guarda
   el equipo). Mergean en cualquier orden.
2. **En el banco, el test barato que cierra R3** (está en `docs/offline-buffer.md`):
   cortar el **internet, no el WiFi** (bloquear el dominio de Supabase en el
   router, o desenchufar el uplink dejando el AP prendido — con el WiFi caído
   entra en juego R2 y ensucia la prueba). Esperar 15 min mirando
   `http://<ip>/api/status`: `buffer.pending` tiene que subir de a uno por minuto
   y `clock_syncs` tiene que ser > 0. Restaurar. Después, en Supabase:
   `select created_at, temp_avg, system_state from readings where device_id='<mac>'
   order by created_at` → tienen que aparecer **~15 filas `buffered` separadas por
   un minuto cubriendo el corte**, **no** apiladas en el minuto de la reconexión.
   **Ese es el check que separa "hay buffer" de "hay buffer que sirve".**
3. **Decidir el partition scheme** antes de la próxima feature de firmware (98,7 %
   de flash).
4. **Santa Cruz:** el equipo de allá corre `firmware_revival/`, que es **otro
   sketch** y está **sin commitear** (ver abajo). Este branch **no lo toca**. Si
   ese nodo va a quedar en redes abiertas con portal cautivo, tiene el mismo
   agujero R3 y vale portarle los dos headers — son dos archivos sin dependencias
   de Arduino.

## Estado de los otros repos (no los toqué)

- ⚠️ **`C:\Proyectos\frioseguro` sigue con trabajo de día SIN COMMITEAR**, y esta
  noche **creció**: además de `kit_santacruz/`, `firmware_revival/`,
  `backup_supabase/`, `supabase/BOOTSTRAP_2026-08-19.sql`, `REVIVAL_2026-08.md` y
  los dos `.zip`, aparecieron **`apk-panel/`, `panel-web/`, `.build_revival/` y
  `supabase/migration_device_logs.sql`**, más cambios sin commitear en las dos
  apps Android. **`BOOTSTRAP_2026-08-19.sql` sigue siendo el esquema de verdad y
  vive sólo en este disco.** Van muchas noches reportándolo; ahora hay además un
  **firmware entero** (`firmware_revival/`) fuera de git, que es el que se está
  usando en una instalación real a 1500 km. **No lo toqué ni lo commiteé**: el
  `git add` de esta noche fue archivo por archivo.
- ⚠️ **MATI-HQ sigue con trabajo de día sin commitear**: `scripts/turno_noche_log.txt`
  modificado y sin trackear `SESION_1_FRIOSEGURO_SANTACRUZ.md`,
  `SESION_2_DATALOGGER_PIEZO.md`, `SESION_3_PID_TORNO_UTN.md`. **Los leí pero no
  los toqué** — el `SESION_1` es el que explica la puesta en marcha de Santa Cruz
  y es el que hizo que R3 pesara más que su lugar en la lista.
- La cola de merge de frioseguro son **23 branches**. Los que tocan la cadena de
  la continuidad son el `08-14-b` (que la auditó), el `08-23` (R1+R7) y éste (R3).
