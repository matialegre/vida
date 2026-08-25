# Nocturno local — 2026-08-25

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-25-promesa-del-gateway` (pusheado, `5838b60`).
**Sale de:** `nocturno/local-2026-08-22-b-una-medicion-una-fila` → **mergear ese
primero.** Usa su `reading_uid` y su migration `20260822000000`. No pisa nada de
los otros branches de galgas (`08-11` y `08-21` son `web/` y docs).

## TL;DR

> **El emisor guardaba la medición que no podía entregar. El gateway le contestaba
> 200 y después la tiraba.**

Anoche —la noche de galgas anterior, 08-22-b— se le dio al emisor una cola en RTC
para que ninguna medición se perdiera: sin WiFi, POST fallido o batería baja, la
guarda y la reintenta el wake siguiente. El branch de hoy encontró el agujero que
lo anulaba, y estaba una capa más arriba:

```c
#define FWD_MAX_RETRIES      3      // intentos antes de descartar
#define FWD_RETRY_BACKOFF_MS 2000   // espera entre reintentos
```

**El RX toleraba ~6 segundos de Supabase caído.** Después descartaba la medición.
Y como el 200 se lo había contestado al encolar, el emisor ya la había borrado de
su backlog y ya estaba durmiendo. Un deploy de Supabase, un reinicio del switch,
medio minuto de WiFi de planta: cualquiera de esos se llevaba datos de la parada,
sin dejar rastro más que un contador.

Lo más incómodo: **no estaba escondido.** El comentario del código lo decía con
todas las letras —*"Tradeoff: emisor cree haber entregado pero perdes el dato"*— y
el log también: `-- DATO PERDIDO`. Estaba **asumido**, no descubierto. Lo que
cambió fue el contexto: con el backlog del emisor adentro, el gateway pasó a ser
**el único eslabón que promete de más, y encima el que le da la orden de borrar al
que sí guardaba.**

## Tarea elegida y por qué

Por rotación tocaba galgas: las últimas cuatro noches fueron galgas (08-22-b),
frioseguro (08-23), cosechador (08-23-b) y datalogger (08-24), y galgas era la más
vieja.

Dentro del repo elegí **D1** —el hallazgo que la auditoría del 08-11 dejó anotado
en el bloqueante #1 y que nadie había tocado— por tres motivos:

1. **No está en ningún branch esperando merge.** El `08-11-cadena-entrega` lo
   *encontró* y lo describió; nadie lo implementó. Mismo patrón que funcionó el
   08-22-b con D2/D3: tomar un pendiente ya nombrado, con su evidencia escrita.
2. **Es la continuación directa de la noche anterior de galgas.** D2/D3 arreglaron
   el emisor; D1 es la capa que lo anulaba. Mergear el 08-22-b sin esto deja el
   backlog del emisor a medias: guarda, pero el gateway le miente y hace que lo
   borre.
3. **Los datos de octubre son el entregable.** Un hueco silencioso en la serie
   corrompe cualquier análisis que Dreyfus mire, y no hay forma de darse cuenta
   después.

## Qué hice

**La política de reintento salió del `.ino` y se volvió testeable.**
`firmware/shared/forward_queue.h` (nuevo) — cola circular estática de 8 × 768 B con
la máquina de estados adentro, **sin `Arduino.h`**, para poder correrla en la PC.
El `.ino` se quedó solo con el HTTP.

| resultado del POST | antes | ahora |
|---|---|---|
| 2xx | entregada | entregada |
| transporte (≤0), 5xx, 408, 429 | 3 intentos y **a la basura** | **reintento sin tope**, backoff 2→4→8→16→32→60 s |
| 4xx (que no sea 408/429) | 3 intentos y a la basura | **descarte inmediato**, contado aparte, log fuerte |
| cola llena | 503 (ya estaba, y estaba bien) | 503 |

Las cuatro filas son **un solo diseño** y ninguna se sostiene sola:

- **Reintentar sin tope** es lo que vuelve verdadero el 200. El RX vive en 220 V y
  no duerme: el recurso escaso es el slot, no la paciencia.
- **Descartar los 4xx** es su contracara **obligatoria**. Sin eso, un body que
  Supabase rechaza por cómo está escrito se queda en la cabeza de la cola para
  siempre y **congela el gateway entero**. Un cambio de schema mal desplegado
  dejaría de perder *una* medición para pasar a perderlas *todas*. Esta fila no es
  una concesión: es lo que hace segura la anterior.
- **El 503 con la cola llena** encadena las dos colas en vez de pisarlas: el
  emisor no recibe una promesa que el RX no puede cumplir, y se guarda el dato él.

**Y la pieza sin la cual todo lo anterior sería peor que el problema:**
`?on_conflict=reading_uid` + `Prefer: resolution=ignore-duplicates` en el POST del
worker, **solo si el body trae el uid**. El caso típico de un reintento es *"el
insert entró pero la respuesta se perdió"*: sin la clave de idempotencia,
"reintentar siempre" es una fábrica de duplicados. Es exactamente lo que el
08-22-b construyó para el emisor y que el gateway no estaba usando. Si el body
viene sin uid (emisor viejo), el POST va sin `on_conflict` y **el log lo dice**:
`(SIN uid: un reintento pudo duplicar)`. No se disimula.

**Dos cosas más que salieron del mismo tirón:**

- **El OTA se llevaba la cola puesta.** El drenado previo existía (3.5.4) con 30 s
  de tope, pero si no drenaba **seguía igual** — y la cola vive en RAM, así que el
  `ESP.restart()` del OTA borraba justo las mediciones que el emisor ya había dado
  por entregadas. Ahora **el OTA se aborta** y se reintenta en el próximo check
  (30 s). No hay riesgo de bloqueo: si Supabase estuviera caído, el firmware check
  no habría pasado y nunca se llega a esa línea.
- **El síntoma cambió de forma y había que poder verlo.** Con reintento sin tope,
  una nube caída **ya no se ve como `fwd_drop` subiendo**: se ve como la cola
  atrasada. `/health` y el heartbeat publican ahora `queue_oldest_s` / `fwd_old`
  (hace cuánto espera la más vieja), `queue_stale`, `queue_high_water`,
  `forwards_refused` y `forwards_retries`. **`forwards_dropped` mantiene el nombre
  por compatibilidad con el PLAN_v5 §4.2 pero cambió de significado**: antes
  mezclaba "la nube estuvo caída" con "el body está mal"; ahora solo es lo segundo,
  y si sube es un bug.

**Archivos:** `firmware/shared/forward_queue.h` (nuevo, 232), `firmware/esp_rx_receptor/esp_rx_receptor.ino`
(−80/+95), `firmware/esp_rx_receptor/config.h`, `tools/test_forward_queue.cpp` (nuevo),
`tools/mutantes_forward_queue.py` (nuevo), `tools/check_gateway_promise.py` (nuevo),
`tools/test_check_gateway_promise.py` (nuevo), `docs/gateway-promise.md` (nuevo),
`QUE_FALTA.md` (bloqueante #1), `.gitignore`.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-25-promesa-del-gateway

# 1. la POLITICA se corre de verdad, sin ESP32 -> 131 checks OK
g++ -std=c++17 -Wall -Wextra -O1 -o tools/test_forward_queue.exe tools/test_forward_queue.cpp
./tools/test_forward_queue.exe

# 2. los tests no son decorativos -> los 15 mutantes mueren
python tools/mutantes_forward_queue.py

# 3. el CABLEADO del .ino, que g++ no ve -> 9 checks, 0 fallando
python tools/check_gateway_promise.py
python tools/check_gateway_promise.py --demo-corte
python tools/check_gateway_promise.py --constantes
python -m unittest tools.test_check_gateway_promise     # 27 tests

# 4. el firmware compila con el core ESP32 real (~2 min)
arduino-cli compile --fqbn esp32:esp32:esp32 firmware/esp_rx_receptor

# 5. lo del 08-22-b sigue en pie
python tools/check_reading_idempotency.py               # 7/7
python -m unittest tools.test_check_reading_idempotency # 35 tests
```

**Verificado esta noche:**

- **La política se ejecutó de verdad, sin Pico ni ESP32.** `tools/test_forward_queue.cpp`
  incluye el header real (no una copia) y lo corre en g++ con un **reloj falso**:
  `now` es una variable, así que un corte de 5 minutos se simula en microsegundos.
  **131 checks OK.** El que importa es `test_corte_de_cinco_minutos`: 30+ mediciones
  ofrecidas durante un corte, `n_rejected == 0`, las 8 aceptadas siguen en la cola
  a los 5 minutos y se drenan **en orden** cuando la nube vuelve. Y
  `test_contabilidad_cierra`: sobre una secuencia mezclada de 60 rondas,
  `n_ok + n_rejected == aceptadas`. **No hay tercer destino: nada se evapora.**
- **Mutación: 15 mutantes de la política, los 15 caen.** Volver al tope de 3
  intentos (la política vieja, o sea D1 exactamente), 4xx transitorio, 5xx
  permanente, transporte contado como éxito, 408/429 sin caso especial, backoff sin
  techo, `ready()` comparando sin signo (se colgaría 49 días en el wrap de
  `millis()`), permanente que no libera el slot, `hasReadingUid` con falso positivo
  y con falso negativo, `oldestAgeMs` mirando el final de la cola, y cuatro más.
  El script queda en el repo (`tools/mutantes_forward_queue.py`) y trabaja sobre una
  **copia** del header en un temporal — no toca el repo.
  **Uno sobrevivió en la primera pasada** (el reset del backoff en `pop()`) y no lo
  tapé: es una invariante defensiva que hoy **no es alcanzable** desde el `.ino`
  porque el worker siempre pregunta `ready()` antes. Le escribí el test y le dejé
  el comentario diciendo eso, en vez de fingir que era una regresión real.
- **El sketch compila con el core ESP32 real** (`arduino-cli`, no solo sintaxis).
  Comparé contra el branch base compilando los dos: **+1504 B de flash (+0,11 %) y
  +24 B de RAM.** La cola ya ocupaba esos 6 KB estáticos antes.
- **El checker estático, 9/9**, con 27 tests que rompen un hecho por vez y verifican
  que **falle el check correcto y solo ése**. Vigila cosas que g++ no puede ver: que
  el `.ino` use la cola compartida y no se escriba otra propia, que no vuelva ningún
  tope de intentos (ni por `#define` ni por un `if (failures >= N)` a mano), que el
  `on_conflict` esté y que la migration exista, que el OTA aborte, y que
  `forward_queue.h` **no gane un `#include <Arduino.h>`** — el día que lo gane, la
  única verificación que existe deja de compilar.

## Lo que quedó SIN verificar (y por qué)

- **Nada corrió en hardware.** Ni un forward real, ni un corte real, ni un OTA real.
- **Que Supabase acepte el `Prefer` doble del RX.** El worker manda
  `return=minimal,resolution=ignore-duplicates` (los dos tokens juntos). Está en la
  doc de PostgREST; nadie lo ejecutó. El emisor usa solo el segundo, así que este
  caso es nuevo.
- ⚠️ **ORDEN DE DESPLIEGUE, y ahora importa más que antes: primero la migration
  `20260822000000`, después el firmware.** Al revés PostgREST contesta 400 a todos
  los POST — y con la política nueva **un 400 se descarta**. Un 400 masivo por
  schema es hoy el peor caso posible del sistema. Es la misma advertencia del
  08-22-b, pero ahí el costo era un POST fallido y acá es un descarte.
- **Que abortar el OTA no lo bloquee.** El check es `!fwdQ.empty()` tras 30 s. Si
  algo dejara la cola permanentemente no vacía, el RX no se actualizaría más. Vale
  mirarlo en el primer OTA de banco.
- **En `MODE_ALERTA` las dos colas cubren ~1 minuto, y eso sigue siendo poco.**
  `--demo-corte` lo pone en números con las constantes reales:

  | modo | corte | ofrecidas | ANTES | AHORA |
  |---|---|---|---|---|
  | NORMAL (600 s) | 2 h | 24 | 24 | **0** |
  | VIGILADO (60 s) | 5 min | 10 | 10 | **0** |
  | VIGILADO (60 s) | 30 min | 60 | 60 | 28 |
  | ALERTA (10 s) | 1 min | 12 | 12 | **0** |
  | ALERTA (10 s) | 5 min | 60 | 60 | 28 |

  **La columna AHORA no es cero para siempre y no lo escondí.** Agrandar la cola del
  RX cuesta RAM, agrandar el backlog del emisor cuesta RTC memory: es una decisión
  tuya, no de este branch. Lo que sí cambió de raíz es **quién sabe**: hoy la
  pérdida ocurre con un 503 que al emisor le llega, no con un descarte silencioso
  que no le llegaba a nadie.
- **Cuánto tarda un forward de verdad** con el WiFi de planta. Drenar 8 a ~2,5 s
  cada uno son ~20 s en los que el WebServer no atiende.
- **Lo escribí y lo verifiqué yo.** El checker compara contra `config.h`,
  `protocol.h` y la migration —que son referencia, no algo mío— pero **una lectura
  de @firmware antes del banco vale**: lo que hay que buscar es si el worker paga
  algo que la `Queue` de host no modela.
- ⚠️ **El sketch del RX está en 94 % de flash** (1.236.244 / 1.310.720 B). No es
  culpa de este branch (sumó 0,11 %), pero quedan ~74 KB y el Task 08 todavía debe
  meter el subscriber Realtime + LCD + buzzer. **Conviene saberlo antes**, no
  cuando no entre.

## Próximo paso (para Matías, de día)

1. **Mergear `08-22-b` y después éste.** Éste sale de aquél.
2. **Correr la migration `20260822000000` ANTES de flashear.** Los dos branches lo
   piden y acá el costo de equivocarse subió.
3. **En el banco, el test barato que cierra D1:** con el RX andando, cortar el
   upstream a Supabase (bloquear el dominio en el router o apagar el uplink) 5
   minutos, dejar A y B empujando, restaurar, y contar filas por
   `(device_id, boot_count)`. Tiene que dar **una fila por medición** y ninguna
   faltando. `GET /health` durante el corte debería mostrar `queue_len` subiendo y
   `queue_oldest_s` creciendo.
4. **Decisión que sigue siendo tuya:** los 8 slots de la cola del RX y los 12 del
   backlog del emisor son la cobertura real. En `ALERTA` eso es un minuto. ¿Alcanza
   para la parada, o hay que gastar RAM?

## Estado de los otros repos (no los toqué)

- ⚠️ **`C:\Proyectos\frioseguro` sigue con trabajo de día SIN COMMITEAR** —
  `kit_santacruz/`, `firmware_revival/`, `backup_supabase/`,
  `BOOTSTRAP_2026-08-19.sql`, dos `.zip`. **Van muchas noches reportándolo.**
  `BOOTSTRAP_2026-08-19.sql` es hoy el esquema de verdad y vive **sólo en este
  disco.**
- ℹ️ `galgas` tiene `hardware/` sin trackear (trabajo de día). No lo toqué ni lo
  commiteé: el `git add` fue archivo por archivo.
- ⚠️ **MATI-HQ sigue con trabajo de día sin commitear**: `dominios/muestreador.md`
  modificado y sin trackear `SESION_1_FRIOSEGURO_SANTACRUZ.md`,
  `SESION_2_DATALOGGER_PIEZO.md`, `SESION_3_PID_TORNO_UTN.md`. No los toqué.
- La cola de merge de galgas son 6 branches. Los dos que tocan el bloqueante #1 son
  el `08-11` (que lo auditó) y éste (que lo arregla).
