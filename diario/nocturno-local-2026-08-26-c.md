# Nocturno local — 2026-08-26 (tercera pasada, "-c")

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (**P0** — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-26-c-topologia-del-gateway` (pusheado, `e44d52f`).
**Sale de:** `nocturno/local-2026-08-25-promesa-del-gateway`, que a su vez sale de
`08-22-b`. **Orden de merge: `08-22-b` → `08-25` → éste.**

## TL;DR

> **Anoche se le arregló la promesa a un gateway que la familia de octubre no
> usa — y no podía usar.**

El branch `08-25` (primera parte de esta misma noche fue frioseguro, la segunda
datalogger; el `08-25` es de anoche) le construyó al RX una política de reintento
seria para que su `200` fuera una promesa de verdad. Buen trabajo, y **inalcanzable
desde `esp_a_emisor` / `esp_b_emisor`**, que es la familia que se flashea. Tres
motivos independientes, y con uno solo alcanzaba:

1. **El descubrimiento estaba clavado en "no".** `discoverGatewayUrl()` era
   `return String();` adentro de un `#if 1`, así que `gw_url` era **siempre** `""`
   y todo el bloque de fallback del `.ino` era código muerto. Y el cuerpo que
   estaba del otro lado del `#else` era **mDNS** — la lección que el propio
   `QUE_FALTA` da por descartada.

2. **Los dos caminos hablaban protocolos distintos.** Si alguien apagaba ese
   `#if 1`, la URL del RX se le pasaba a `supabaseInit()`, o sea que el emisor
   posteaba a `http://<rx>/rest/v1/readings`. **El RX no sirve ese path**: levanta
   exactamente dos rutas, `POST /reading` y `GET /health`, y todo lo demás cae en
   `onNotFound` → **404**. La familia monolítica (`ota_wm_pp`) siempre lo hizo
   bien; la modular tenía escrita la suposición del relay transparente, que es lo
   que hace `gateway_relay.h` — un header que **ningún sketch incluye**.
   Y hay un daño colateral que no es del POST: cambiar el `base_url` vía
   `supabaseInit()` desviaba también el `GET commands` y el `firmwareCheck` **del
   mismo wake**.

3. **El 404 no estaba en la lista.** El fallback enumeraba `<=0, 502, 503, 504`.
   El RX contesta, por sí mismo, `400` (body inválido), `413` (no entra) y `503`
   (cola llena), más el `404`. **Tres de esos cuatro no estaban.** Un 404 mandaba
   la medición al backlog sin reintento — y como el path estaba mal
   *estructuralmente*, el wake siguiente daba 404 otra vez. Los 12 slots del
   backlog RTC que el `08-22-b` construyó para no perder nada se llenaban de
   mediciones que **nunca iban a salir**, y a partir de ahí cada medición nueva
   pisaba una vieja.

## Tarea elegida y por qué

Por rotación quedaban galgas (08-25) y cosechador (08-23-b). **Cosechador es P2 y
todo lo que le queda está bloqueado por la compra** — sus branches ya agotaron el
análisis offline y ahí sólo se puede inventar trabajo. Galgas es **P0 con fecha**.

Dentro del repo seguí el patrón que viene funcionando: **no abrir una auditoría
nueva, tomar un pendiente ya nombrado con su evidencia.** D9 estaba esperando
desde el `08-11`, descrito y sin implementar, y subió de peso solo: es la capa que
anulaba lo que se hizo anoche. Mismo movimiento que el `08-25` respecto del
`08-22-b`.

## Qué hice

### 1. La topología, en un solo archivo que corre en la PC

`firmware/shared/gateway_route.h` (nuevo, **sin `Arduino.h`**): path y puerto del
contrato con el RX, la decisión por código HTTP, la frescura de la IP, validación
de la IP y los dos parsers de fecha.

**La regla de decisión dejó de ser una lista:**

| | resultado |
|---|---|
| gateway + 2xx | entregada |
| gateway + **cualquier** no-2xx | **reintento directo** |
| directo + 2xx | entregada |
| directo + no-2xx | backlog |

Una lista es una apuesta a que conocés todos los códigos que el otro lado puede
inventar. Esta regla no enumera: un no-2xx del gateway significa *"el RX no se hizo
cargo"* y nunca *"Supabase la rechazó"* — el RX contesta por sí mismo y sólo
promete cuando encola. Reintentar directo es gratis en corrección porque el
`reading_uid` + `ON CONFLICT DO NOTHING` del `08-22-b` hacen que la segunda fila no
exista.

### 2. El descubrimiento por `devices.local_ip` (PLAN v5), sin mDNS

El cuerpo mDNS **no quedó comentado**: está en el historial de git, que es donde va
el código muerto. En un `#else` se veía como una opción, y no lo es.

**Y la pieza sin la cual nada de esto funcionaba: el emisor no tiene reloj.** No
hay un solo `configTime()` en toda la familia modular; `nowDeviceMs()` es uptime
acumulado, no hora. Y la frescura de `local_ip_at` es una comparación contra
"ahora".

> **No hace falta que sepa la hora.** `local_ip_at` lo escribió Postgres y el
> header `Date` viene en **esa misma respuesta HTTP**. Los dos instantes son del
> servidor: el emisor resta dos números ajenos. Sin NTP, sin RTC y sin una sola
> request nueva. (Es la misma jugada que usé anoche en frioseguro, y acá salió del
> mismo problema.)

**Eso destapó un bug de la familia monolítica que no estaba anotado en ningún
lado.** `ota_wm_pp` compara contra su reloj local:

```c
uint32_t age_s = (now > at_unix) ? (uint32_t)(now - at_unix) : 0;
```

Con el reloj sin sincronizar (`now` ≈ 1970) eso da `age_s = 0` — o sea
**"perfectamente fresca"** — y el nodo le manda la única copia de una medición a
una IP que puede ser de la semana pasada. Por eso `gwRouteFreshness` devuelve
**tres** estados y no dos: `UNKNOWN` **no es** `FRESH`. Un reloj roto no puede
significar "la IP está perfecta"; significa "no sé", y "no sé" es que no.

### 3. La caché, que es lo que hace que el gateway ahorre algo

Descubrir por Supabase cuesta **exactamente el handshake TLS que el gateway existe
para evitar**. Sin caché, el camino "gateway" sería más caro que el directo. Por
eso hay dos constantes y no una: `GW_ROUTE_IP_FRESH_S` (600 s, *"¿esta IP todavía
sirve?"*, la juzga el servidor) y `GW_CACHE_RENEW_S` (3000 s, *"¿cada cuánto pago
un GET para enterarme?"*). En `MODE_NORMAL` eso es **1 wake de cada 5** pagando
TLS y 4 yendo al RX sin TLS. Vive en RTC slow memory, igual que el backlog.

### 4. El interruptor, y por qué queda apagado

`#define EN_GATEWAY 0` en los dos `config.h`. **Con 0 el comportamiento es el de
hoy, byte por byte**: `discoverGatewayUrl()` devuelve `""`, cero requests extra,
POST directo. Se puede mergear sin decidir nada.

Queda en 0 porque **hay una contradicción abierta entre documentos y la decidís
vos, no este branch**:

| | dice |
|---|---|
| `PLAN_v3 §1.1` | *"El RX no está físicamente cerca de los emisores. **No puede actuar de gateway local**"* |
| `PLAN_v5 §4` | el RX publica `devices.local_ip` cada 30 s y sirve `POST /reading` **justamente para esto** |

Lo que cambia este branch es que la respuesta sea **un 0/1 y no una reescritura**,
y que el camino esté testeado *antes* de que alguien lo necesite en planta.

**Archivos:** `firmware/shared/gateway_route.h` (nuevo, 236), `gateway_discovery.h`
(reescrito), `gateway_relay.h` (banner de código muerto), `supabase_client.h/.cpp`
(+`supabaseBuildReadingBody` y `supabasePostReadingVia`), los dos `.ino` y los dos
`config.h`, `tools/test_gateway_route.cpp` (nuevo), `tools/mutantes_gateway_route.py`
(nuevo), `tools/check_gateway_topology.py` (nuevo),
`tools/test_check_gateway_topology.py` (nuevo), `docs/gateway-topology.md` (nuevo),
`QUE_FALTA.md`.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-26-c-topologia-del-gateway

# 1. la POLITICA se corre de verdad, sin ESP32 -> 26290 checks OK
g++ -std=c++17 -Wall -Wextra -O1 -o tools/test_gateway_route.exe tools/test_gateway_route.cpp
./tools/test_gateway_route.exe

# 2. los tests no son decorativos -> los 26 mutantes mueren
python tools/mutantes_gateway_route.py
python tools/mutantes_gateway_route.py --lista

# 3. el CABLEADO, que g++ no ve -> 35/35
python tools/check_gateway_topology.py
python tools/check_gateway_topology.py --constantes
python -m unittest tools.test_check_gateway_topology      # 24 tests

# 4. compila con el core ESP32 real, por los DOS caminos (~2 min c/u)
arduino-cli compile --fqbn esp32:esp32:esp32 firmware/esp_a_emisor
arduino-cli compile --fqbn esp32:esp32:esp32 firmware/esp_b_emisor
arduino-cli compile --fqbn esp32:esp32:esp32 \
  --build-property "compiler.cpp.extra_flags=-DEN_GATEWAY=1" firmware/esp_a_emisor

# 5. lo de las noches anteriores de galgas sigue en pie
./tools/test_forward_queue.exe
python tools/check_gateway_promise.py
python tools/check_reading_idempotency.py
```

**Verificado esta noche:**

- **La política se ejecutó de verdad, sin ESP32.** `tools/test_gateway_route.cpp`
  incluye el header **real** (no una copia) y lo corre en g++: **26290 checks, 0
  fallando.** El que importa es `test_wake_completo`, que reproduce la secuencia
  del `.ino` sin red sobre **12 288 combinaciones** de (IP, `local_ip_at`, `Date`,
  código del RX, código de Supabase) y verifica en todas la invariante:
  **una medición o se entrega o se encola. No hay tercer destino.** Con nombre
  propio: el 503 de cola llena, el 404 del path equivocado (el caso que motiva el
  branch), el `Date` que no vino, el RX caído hace media hora, y el peor caso —
  gateway roto **y** Supabase caído — que tiene que terminar en el backlog.
- **Mutación: 26 mutantes, los 26 caen.** Volver a la lista vieja tal cual, el 2xx
  sin techo y sin piso, `UNKNOWN` colapsado en `FRESH` (que es exactamente el bug
  del monolítico), aceptar cualquier fecha futura, la resta al revés, el path
  transparente, la URL truncada, IP con ceros a la izquierda (octal encubierto),
  octetos > 255, `0.0.0.0`, bisiesto sin la regla del siglo, el offset de zona
  ignorado y sumado al revés, el mes del header `Date` matcheando a mitad de camino
  (`"nFe"`), y seis más. El script trabaja sobre una **copia** en un temporal y
  tiene tope de 60 s por mutante (`CUELGA` también cuenta como muerto, pero
  acotado — la lección del worker que quedó clavado).
- **El checker estático, 35/35**, con **24 tests** que rompen un hecho por vez y
  verifican que **falle el check correcto y sólo ése** (incluido un test de que
  *mencionar* mDNS en un comentario **no** dispare un falso positivo).
  **El checker encontró algo mientras lo escribía**: quedaba un **segundo** lugar
  con la regla del 2xx escrita a mano — el guard del drenaje del backlog. También
  pasó a `gwRouteDecide()`. Es exactamente para lo que sirve el auditor separado.
- **Compilan los tres caminos con el core ESP32 real** (`arduino-cli`, 3.3.8, no
  sólo sintaxis), comparando contra el branch base en un worktree limpio:

  | | flash | RAM |
  |---|---|---|
  | base (`08-25`) | 1 237 556 B (94 %) | 61 456 B |
  | **éste, `EN_GATEWAY=0`** | **1 211 840 B (92 %)** | **59 376 B** |
  | éste, `EN_GATEWAY=1` | 1 232 968 B (94 %) | 59 376 B |

  **Sacar el mDNS bajó 25 716 B de flash y 2 080 B de RAM** aunque la query ya
  estaba deshabilitada: `<ESPmDNS.h>` se seguía linkeando igual. Con el sketch del
  RX en 94 % y el Task 08 debiendo LCD + buzzer + subscriber Realtime, **25 KB no
  es cosmético** — es el margen que hacía falta.

## Lo que quedó SIN verificar (y por qué)

- **Nada corrió en hardware.** Ni un POST al RX, ni un descubrimiento real.
- **Que `HTTPClient` entregue el header `Date`** en el GET de `devices`. Se usa
  `collectHeaders()` + `header("Date")`, que es la API documentada, y `Date` es
  obligatorio en HTTP/1.1 — pero nadie lo ejecutó. **Es la suposición de la que
  cuelga toda la frescura.** Lo bueno: si fallara, `gwRouteFreshness` devuelve
  `UNKNOWN`, el gateway **no se usa** (no se usa mal: no se usa) y todo va directo.
  El modo de falla es el comportamiento de hoy.
- **El formato exacto de `local_ip_at`** que devuelve PostgREST. El parser acepta
  `Z`, `+00:00`, `-03:00` y fracción; se probó contra los tres, pero contra strings
  escritos a mano, no contra una respuesta real.
- **La familia monolítica NO se tocó.** `ota_wm_pp` sigue con su parser que muta la
  TZ del proceso y con el bug del reloj sin sincronizar que describí arriba. Anda
  hoy y no había forma de verificar el cambio sin banco; meterle mano a ciegas a un
  firmware que funciona es lo que no hay que hacer de noche.
  **`check_gateway_topology.py --constantes` muestra las constantes de las dos
  familias lado a lado** para el día que se unifiquen.
- **`gateway_relay.h` sigue existiendo** con su `MDNS.begin()` adentro: es el último
  mDNS del repo. No llega a ningún binario porque ningún sketch lo incluye, y eso
  **ahora lo vigila el checker**. Le puse un banner de código muerto en vez de
  borrarlo (borrar archivos no es trabajo de noche).
- **Lo escribí y lo verifiqué yo.** El checker compara contra el `config.h` del RX y
  contra las rutas reales de su `.ino` —que son referencia, no algo mío— pero **una
  lectura de @firmware antes del banco vale**: lo que hay que buscar es si
  `supabasePostReadingVia()` omite algo que el POST directo sí manda.
- ⚠️ **Sigue abierto R2 del lado de frioseguro y el Task 08 del lado de galgas.**
  Este branch no toca el RX.

## Próximo paso (para Matías, de día)

1. **Mergear en orden: `08-22-b` → `08-25` → éste.** Cada uno sale del anterior.
   Y **la migration `20260822000000` va ANTES de flashear** (sigue valiendo la
   advertencia de las dos noches anteriores).
2. **Decidir la topología, que es lo único que este branch no puede decidir.**
   `PLAN_v3 §1.1` dice que el RX no está cerca de los emisores; `PLAN_v5 §4` lo
   construye como gateway. Es una pregunta **física** sobre dónde va a estar cada
   caja en la planta, no una de código. Los números para decidir están en
   `docs/gateway-topology.md` §3.
3. **Si la respuesta es "sí, gateway": el test de banco** está escrito en
   `docs/gateway-topology.md` §6 y es barato — flashear A con `-DEN_GATEWAY=1`,
   ver el 200 por el gateway, **apagar el RX** y verificar que la medición aparece
   igual en `readings` y que **el backlog queda en 0**. Ése es el caso que antes se
   comía la medición.
4. **Si la respuesta es "no, directo":** el branch se mergea igual y no cambia
   nada, pero se lleva puestos los 25 KB de mDNS y deja el 404 tapado por si algún
   día se prende.

## Estado de los otros repos (no los toqué)

- ⚠️ **`C:\Proyectos\frioseguro` sigue con trabajo de día SIN COMMITEAR**, y hoy
  creció (ver el informe de la primera pasada de esta noche): `kit_santacruz/`,
  `firmware_revival/`, `apk-panel/`, `panel-web/`, `backup_supabase/`,
  `BOOTSTRAP_2026-08-19.sql`, `supabase/migration_device_logs.sql`, dos `.zip`.
  **`BOOTSTRAP_2026-08-19.sql` sigue siendo el esquema de verdad y vive sólo en
  este disco**, y `firmware_revival/` es un firmware entero fuera de git corriendo
  en una instalación real a 1500 km.
- ℹ️ **`galgas` tiene `hardware/` sin trackear** (trabajo de día). No lo toqué ni lo
  commiteé: el `git add` de esta noche fue archivo por archivo.
- ⚠️ **MATI-HQ sigue con trabajo de día sin commitear**: `scripts/turno_noche_log.txt`
  modificado y sin trackear `SESION_1_FRIOSEGURO_SANTACRUZ.md`,
  `SESION_2_DATALOGGER_PIEZO.md`, `SESION_3_PID_TORNO_UTN.md`. Los leí, no los toqué.
- La cola de merge de galgas son **29 branches**. Los tres que forman la cadena de
  la entrega y que se mergean en orden son `08-22-b` (el emisor no pierde),
  `08-25` (el RX no miente) y éste (los dos hablan el mismo idioma).

**Documento largo con todo el detalle:** `docs/gateway-topology.md` (en el branch).
