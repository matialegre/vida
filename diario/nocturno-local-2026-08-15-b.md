# Nocturno local — 2026-08-15-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-15-b-cadena-aviso` (pusheado, `d354f7b`).

## TL;DR

El sistema de galgas no existe para medir. Existe para que **alguien haga algo**
antes de que se rompa el redler. Todas las auditorías previas del repo —siete—
terminan en la pantalla. Ninguna sigue el tramo que **arranca donde termina la
pantalla**: el aviso.

**De los 8 eslabones: 2 ejecutables, 1 con fricción, 5 ROTOS.** Los dos sanos son
justo los dos que el repo ya auditó (medir, entregar). Todo lo que pasa después
de que el número llega a la nube está roto.

Tres números, sacados del propio código:

- **Ningún firmware emite un evento de alerta. Ninguno.** 24 llamadas a
  `emitEvent()` en todo el repo —OTA, boots, calibración, factory reset— y
  **cero** de alerta. Los dos emisores modulares (la familia de octubre) no
  emiten **ningún** evento de ningún tipo. La tabla `events`, el vocabulario que
  declara el schema (`alert_start`/`alert_end`), el índice parcial de alertas y
  el Realtime del dashboard **ya están**. Falta que alguien escriba la fila.
- **El único aviso físico de la planta está escrito, compila, y no recibe
  datos.** El LCD, el LED rojo y el buzzer del RX se actualizan en un solo lugar:
  el handler del POST de la lectura. El RX no consulta `readings` ni se suscribe
  a nada. Y el emisor modular pide la URL del gateway a `discoverGatewayUrl()`,
  cortocircuitada en un `#if 1`. Con la familia monolítica el panel funciona; con
  la modular, dice "esperando..." con la nube en rojo.
- **De una alerta de 6 horas quedan 0 filas de `events`.** La única evidencia son
  390 filas de `readings` con `in_alert=true`, y **ninguna consulta del dashboard
  filtra por esa columna** — aunque el índice para hacerlo existe desde la
  primera migración.

## Tarea elegida y por qué

Por rotación tocaba galgas (los cuatro turnos previos: galgas 08-13-b,
cosechador 08-14, frioseguro 08-14-b, datalogger 08-15 — el más viejo era éste).

Los 🔴 del `QUE_FALTA` sin branch siguen siendo banco o hardware (#2 necesita
galga física, #3 LiPo real, #4 flashear). Y las siete auditorías previas de este
repo cubren, todas, **el sistema por adentro**:

| noche | qué audita | dónde termina |
|---|---|---|
| 07-29 `vpp-field-characterization` | qué significa el v_pp | el número |
| 08-04 `contrato-comandos` | la forma de los comandos | el nodo |
| 08-06 `identidad-ota` | quién es cada nodo para el OTA | el nodo |
| 08-07-b `contrato-schema` | la forma de lo que entra a la DB | la tabla |
| 08-09-b `cadena-medicion` | ADC crudo → número | el número |
| 08-11 `cadena-entrega` | número → card del SCADA | **la pantalla** |
| 08-13-b `puesta-en-marcha-campo` | caja cerrada → nodo andando | el nodo |

La pregunta que elegí es la que ninguna contesta:

> La galga se sale de rango a las 3 de la mañana.
> **¿Quién se entera, cuándo, y qué queda de eso mañana?**

Tres razones para elegirla sobre cualquier otra cosa esta noche:

1. **Es el otro extremo del 08-11.** Esa noche auditó que el número llegara a
   pintar la card. Ésta pregunta qué pasa **cuando la card se pinta de rojo y no
   hay nadie mirando** — que en una planta con turno de noche es el caso normal,
   no el raro.
2. **Es literalmente por lo que paga Dreyfus.** El sistema se vende como
   detección temprana de falla en el redler. Si la detección no llega a un
   humano, es un protector de pantalla caro.
3. **El fix más importante son dos líneas de firmware.** A1 es llamar
   `emitEvent()` en la transición de alerta, con los nombres **que el schema ya
   declara**. No toca el lazo de muestreo, ni el POST, ni el OTA: nada de lo que
   auditaron el 08-09-b y el 08-11.

## Qué hice

**`tools/check_alert_chain.py`** (stdlib, solo lectura, sin red ni hardware, no
compila nada). **No inventa números: los LEE** de `firmware/`, `web/src/`,
`backend/supabase/migrations/` y los directorios de Edge Functions, y cita
`archivo:línea` de cada afirmación. Exit 0/1/2/3, `--json`, `--detail`,
`--fail-on`, `--root`.

**Cuatro oráculos** que demuestran los hallazgos en vez de afirmarlos:

- `--demo-aviso` recorre los **8 eslabones** como quien vive la alerta y marca
  cada uno *ejecutable / fricción / ROTO*. Resultado: **2 / 1 / 5**, primer
  eslabón roto: el **4** (que suene algo en la planta).
- `--demo-vocabulario` pone las **tres escrituras** del nombre del evento de
  alerta una al lado de la otra —lo que la base declara, lo que la pantalla
  entiende, lo que el firmware emite— y cuenta cuántos nombres comparten:
  **uno** (`low_battery`), y el firmware no emite ninguno.
- `--demo-latencia` calcula, perfil por perfil, cuánto tarda el aviso en llegar a
  cada superficie. El panel de la planta y "un humano" salen **nunca** en las
  cinco filas.
- `--demo-silencio --horas 6` cuantifica una alerta larga: 390 lecturas, 0
  eventos, 1 beep del SCADA, 6 h de buzzer con una familia y 0 con la otra, y
  qué queda como evidencia al día siguiente.

**`tools/test_check_alert_chain.py` — 128 tests en 7 capas:** utilidades de
texto, extractores sobre fuentes sintéticas, los cuatro oráculos con números
fijados, **control negativo** (un repo sintético sano no enciende nada), un
defecto inyectado por vez que enciende **exactamente** su conjunto de códigos, la
capa "no salta cuando no corresponde", y regresión sobre el repo real + CLI.

**`docs/alert-chain.md`** — el análisis completo y el orden de arreglo.

### Lo que hubo que resolver

- **El comentario de cabecera de un archivo puede robarle el nombre a la
  función.** `gateway_discovery.h` empieza con *"Cada emisor llama
  `discoverGatewayUrl()` después de wifiBoot"*, y mi buscador de cuerpos de
  función matcheaba **esa** mención: el hallazgo salía bien pero **citaba la
  línea 7 en vez de la 50**. Un hallazgo con la cita equivocada es un hallazgo
  que el que lo va a arreglar no encuentra. Ahora la búsqueda corre sobre el
  texto sin comentarios (que conserva los números de línea). Hay test.
- **El RX arma la URL de `readings` para EMPUJAR, no para TRAER.** Mi primera
  versión buscaba el path suelto y concluía que el RX sí consultaba la nube — lo
  que **apagaba A2 entero**. La distinción real es el query string: un GET lleva
  `?select=...`; el forward del gateway no. Con el matcheo laxo, el hallazgo más
  importante de la noche desaparecía en silencio.
- **A3 no podía disparar sobre un directorio que no existe.** Mi primera versión
  encendía "no hay Edge Functions" en cualquier carpeta del disco, incluida una
  vacía. Un repo donde el directorio ni existe no es "no tiene funciones": es
  otro repo. Ahora exige que **los directorios existan y estén vacíos**. Lo cazó
  un test de la CLI con un `--root` inexistente.
- **El buzzer del RX no beepea una vez por intervalo.** `BUZZER_INTERVAL_MS` es
  el **toggle**: un beep completo son dos intervalos. Mi primera cuenta daba el
  doble. Y el tramo activo tampoco es todo el tiempo: depende de si el emisor
  duerme más que la ventana de stale (A7), así que el oráculo lo calcula tramo
  por tramo en vez de multiplicar.
- **A4 tenía que separar lo que es hecho del código de lo que es política del
  navegador.** Que el `AudioContext` arranque `suspended` sin gesto previo es
  comportamiento del navegador (verificable, pero fuera del repo). Que **no haya
  `resume()` en ningún lado** y que el disparo sea **por flanco** son hechos del
  código. El hallazgo dispara por los segundos, y el primero está declarado como
  premisa externa.
- **Un `case CMD_SILENCE` en cualquier switch no silencia ningún buzzer.** El
  extractor de comandos mira el cuerpo de `processRxCommands()`, no el archivo
  entero. Esa la encontró la prueba de mutación, no yo.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **5 error · 3 warn · 3 info.**

| código | sev | dueño | qué |
|---|---|---|---|
| **A1** | error | @firmware | **Ningún firmware emite un evento de alerta.** `ota_wm_pp.ino`: 22 `emitEvent()`, 0 de alerta. `esp_rx_receptor.ino`: 2 (heartbeat y boot), 0 de alerta — **ni siquiera registra cuándo enciende el buzzer**. `esp_a/b_emisor`: **0 eventos de cualquier tipo**. Y el schema (`initial_schema.sql:116`) declara el vocabulario en el comentario de la columna. |
| **A2** | error | @firmware | **El aviso físico está desconectado en la familia de octubre.** `esp_rx_receptor.ino:849` es la única escritura del estado del panel, adentro del handler del POST; 0 suscripciones Realtime y 0 GET a `readings`. `gateway_discovery.h:50` devuelve vacío bajo `#if 1` (decisión documentada: PLAN_v3 §1.1) y `esp_a_emisor.ino:286` igual le pregunta. La **monolítica** sí alimenta el panel (`ota_wm_pp.ino:34`, `EN_GATEWAY 1`). |
| **A3** | error | @backend | **No hay ningún camino de aviso fuera del navegador.** `backend/functions/` y `backend/supabase/functions/` existen y tienen solo `.gitkeep`. Cero push, mail o webhook. **FrioSeguro ya tiene el push desplegado**; el proyecto que va a una planta con turno de noche, no. |
| **A4** | error | @frontend | **El único sonido del SCADA depende de un gesto previo y suena una vez.** `PlantaView.jsx:60`: el `AudioContext` se crea adentro de `play()`, sin `resume()` en ningún lado, con `catch (e) {}` vacío — y el contexto mudo **queda cacheado** para toda la vida de la página. `:124`: disparo por flanco. |
| **A5** | error | @frontend | **El ACK no sale del navegador.** `PlantaView.jsx:105`, `useState({})`: no persiste un refresh, no viaja, no queda quién ni cuándo. Y el botón sólo existe mientras la card está en ALERT. |
| **A6** | warn | @firmware | **A la hora, la alerta se desescala sola.** `esp_a_emisor.ino:168` + `config.h:124`: cumplido `ALERT_MAX_DURATION_S` vuelve a NORMAL **aunque la falla siga** ("puede ser falso positivo", dice el comentario). Avisa cada 10 s la primera hora y cada 10 min después: **más lento cuanto más vieja la falla**. |
| **A7** | warn | @firmware | **El panel declara OFFLINE antes de que llegue la próxima lectura.** `STALE_READING_S = 1800` contra un `AHORRO_MAX` que duerme **3600 s**: `anyAlert()` se apaga sola entre lectura y lectura y el buzzer se calla con la alerta puesta. |
| **A8** | warn | @frontend | **OFFLINE tapa a ALERT.** `computeStage()` devuelve OFFLINE antes de mirar `in_alert`: el nodo que alerta y después se queda sin batería / sin WiFi / se cuelga termina **en gris, no en rojo** — y OFFLINE no hace sonar nada. |
| **A9** | info | @frontend | **Tres vocabularios que casi no se cruzan.** base: `alert_start, alert_end, low_battery, sensor_fault`; UI: `alert, alert_clear, alerta, battery_low, low_battery`; firmware: nada. Comparten **uno**. `alert_start` caería al ícono `'boot'`. |
| **A10** | info | @backend | **El índice parcial de alertas no tiene consumidor.** `readings_alert_idx ... where in_alert = true` está desde la primera migración; ninguna consulta del cliente filtra por `in_alert`. Es el camino más barato al informe de octubre. |
| **A11** | info | @firmware | **El buzzer no se puede callar.** `processRxCommands()` implementa reboot, identify, ota y factory_reset: ninguno silencia, y no hay pulsador. 6 h de beep en el escenario del demo. Termina con el operario desenchufando el panel — y ahí el sistema queda mudo sin registro (A1). |

**Orden sugerido:**

1. **A1 — emitir el evento. Es la pieza más barata y la que más cambia.** Dos
   `emitEvent()` en la transición de `updateAlertState()`, con los nombres que el
   schema ya declara (y de paso se arregla medio A9). *Sin esto no se puede
   verificar nada en campo, no hay informe para Dreyfus, y ningún otro arreglo
   deja rastro.*
2. **A3** — con A1 hecho, es un webhook sobre `events`. El patrón ya está escrito
   y desplegado **en el otro repo**.
3. **A2** — decisión de arquitectura, no bug: o el modular vuelve al gateway por
   `devices.local_ip` (**no** por mDNS, lección pagada), o el RX se suscribe a
   Realtime como promete su propio comentario. Lo que no puede quedar es el panel
   escrito y sin fuente.
4. **A4 + A8** — frontend, media tarde.
5. **A5** — necesita decidir *quién* ackea (hoy no hay auth).
6. **A6 + A7** — dos parámetros que hay que decidir juntos.
7. **A10 + A9** — salen casi gratis después de A1.
8. **A11** — decisión de producto.

## Lo que está BIEN (fijado por test, para no ir a revisarlo)

- **El self-trigger está bien planteado**: 40 mV de v_pp, el mismo número que
  pinta la card. Una sola verdad para las dos puntas.
- **El panel del RX está escrito completo**: LCD 20×4 con las dos galgas, LED,
  buzzer intermitente, línea `[** ALERTA **]`, manejo de stale. A2 es una
  conexión que falta, no un desarrollo.
- **La familia monolítica sí alimenta el panel**: la mitad buena de A2 ya existe.
- **La base tiene todo lo necesario para el registro**: `events` con `severity`,
  vocabulario declarado, índice parcial y Realtime suscripto. Falta la fila.
- **El dashboard ya sabe mostrar un evento de alerta**: `mapTag` tiene íconos y
  colores para alert / cleared / battery / fault.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-15-b-cadena-aviso

python tools/check_alert_chain.py                      # informe; exit 3
python tools/check_alert_chain.py --detail             # + evidencia archivo:linea
python tools/check_alert_chain.py --demo-aviso         # los 8 eslabones
python tools/check_alert_chain.py --demo-vocabulario   # los tres nombres del mismo evento
python tools/check_alert_chain.py --demo-latencia
python tools/check_alert_chain.py --demo-silencio --horas 6
python tools/check_alert_chain.py --json

cd tools && python -m unittest test_check_alert_chain  # -> Ran 128 tests, OK
```

Cinco hallazgos se comprueban **sin la herramienta**:

```bash
grep -rn "emitEvent(\"" firmware/ | grep -i alert          # A1: cero hits
grep -rn "emitEvent" firmware/esp_a_emisor firmware/esp_b_emisor   # A1: cero hits
grep -n "in_alert" firmware/esp_rx_receptor/esp_rx_receptor.ino    # A2: una escritura
grep -n "#if 1" firmware/shared/gateway_discovery.h                # A2
ls backend/functions backend/supabase/functions                    # A3: solo .gitkeep
grep -n "resume()" web/src/views/PlantaView.jsx                    # A4: cero hits
```

**Verificado en esta máquina:**

- `py_compile` de los dos archivos.
- **128 tests en verde** (4,3 s). Sin descargas ni toolchains: cero riesgo de
  timeout.
- **Control negativo real:** un repo sintético sano no enciende **nada** (exit 0,
  los 8 eslabones ejecutables), y cada defecto inyectado por separado enciende
  **exactamente** el conjunto esperado. Los once tienen además su test "no salta
  cuando no corresponde".
- **Verificado por mutación — 16 mutaciones, las 16 hacen fallar la suite:**
  `func_body` sin sacar comentarios · el forward contado como pull · el corte
  naíf en `//` · `emitEvent` contando la definición · `is_alert_event` sin
  `sensor_fault`/`low_battery` · exit code con la severidad menos grave · el
  buzzer ignorando la ventana de stale · A3 disparando sin que el directorio
  exista · gateway-disabled sin mirar dónde cae el `#else` · el ACK dándose por
  persistido · A4 sin exigir que falte el `resume` · el orden de `computeStage`
  invertido · la cadena ignorando la severidad · el índice de alertas sin exigir
  el `WHERE` · `define_number` sin resolver la multiplicación · los comandos
  leídos de todo el archivo en vez del handler.
  *(La primera pasada dejó **tres vivas**: una era una mutación inerte (mi
  mutación caía en una rama inalcanzable — la reescribí como el corte naíf) y
  **dos eran tests flojos**: no había ningún caso con un índice llamado "alert"
  sin `WHERE`, ni con un `case CMD_*` fuera del handler. Los dos tests nuevos
  prueban el contrato declarado, no la mutación. El andamio fue descartable, en
  el temp: **no se commiteó**. Borré el `__pycache__` antes de cada corrida y
  restauré el archivo al final; `git status` quedó igual que antes.)*
- **No se tocó firmware, ni el dashboard, ni SQL, ni `data/field_captures/`.** El
  branch agrega 3 archivos y edita `QUE_FALTA.md`.

## Qué quedó sin verificar

- **Todo sale de leer el repo, no de disparar una alerta.** No hay galga en banco
  ni nodo flasheado al que hacerle subir el v_pp de noche.
- **A2 supone que la familia modular es la que va a octubre.** Sale del
  `QUE_FALTA` y del branch del 08-11, no de una decisión escrita en el repo. **Si
  para octubre va la monolítica, A2 se cae** — y esa ambigüedad es un hallazgo en
  sí: hoy no está escrito en ningún lado cuál de las dos se instala.
- **A4 se apoya en la política de autoplay del navegador** (un `AudioContext`
  creado sin gesto previo arranca `suspended`). Se confirma en un minuto: abrir
  el dashboard, esperar una alerta sin tocar la página. **La otra mitad —que
  suena una sola vez— es un hecho del código.**
- **Las latencias del `--demo-latencia` mezclan datos y supuestos**: los períodos
  de sueño salen de `PP_PROFILES`; el POST (5 s) y el Realtime (2 s) son
  supuestos declarados, no medidos.
- **El `--demo-silencio` supone que la falla no se arregla sola.** Las cuentas
  salen de los períodos reales; el escenario es una hipótesis.
- **La verificación de mayor valor es barata y de día:** abrir el dashboard y
  preguntarle a la tabla `events` cuántas filas de alerta tiene. Si es 0 —y va a
  ser 0— A1 queda cerrado sin discusión.
- **Ningún fix aplicado** — generator ≠ evaluator. Ni siquiera A1, que son dos
  líneas: el que agrega el evento tiene que poder verlo llegar a la tabla.

## Estado

- Branch `nocturno/local-2026-08-15-b-cadena-aviso` pusheado (`d354f7b`), sale de
  `main` (`e9cd4bc`). **galgas volvió a `main` limpio.**
- `QUE_FALTA.md` de galgas: ítem **#18** nuevo + un sub-bullet en el **#1**
  (donde vive la Task 08 del RX, que es exactamente A2), **dentro del branch**.
  Numeré 18 a propósito: los branches del 08-04 y del 08-07-b agregan un `#16` y
  el del 08-09-b un `#17`. Va a haber conflicto trivial de contexto en el ítem #1
  con el branch del 08-11.
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Decimoséptima noche que lo reporto**: es firmware que va a un equipo a 2000
  km y vive **sólo en este disco**. **No lo toqué.**
- ⚠️ **`C:\Proyectos\datalogger` sigue con trabajo de día SIN COMMITEAR**
  (`firmwares/nodo-gimap/`, `tools/rx_gimap.py`, los dos tests del nodo GIMAP,
  `docs/ARMADO_NODO_GIMAP.html`, `.gitignore`). **No lo toqué.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las
  veintidós noches anteriores: `agentes/`, `dominios/`, `enlace/`, más
  `agentes/diseno3d.md`, `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html` y
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- ⚠️ Sigue el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando quieras.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío (sólo el `.gitkeep`). El único
  `enlace\maquinas\*.estado.json` (DESKTOP-RK8DH7C) sigue con `ultima_vez_viva`
  del **2026-08-07**: el latido está parado hace **8 días**. **No lo toqué** (los
  scripts de ENLACE son trabajo de día sin commitear).
- La cola de merge suma **60 branches** en origin (galgas **21**, datalogger 18,
  frioseguro 18, cosechador 3).

## Para @firmware / @backend / @frontend / @comercial / @cronista / @verificador

- **@firmware: A1 es tuyo y es la noche entera.** Dos `emitEvent()` en la
  transición de `updateAlertState()` —una a la entrada, una a la salida— con los
  nombres que el schema **ya declara**. No toca el lazo de muestreo, ni el POST,
  ni el OTA: no hay riesgo de reabrir lo que auditaron el 08-09-b y el 08-11. Es
  el mejor ratio esfuerzo/resultado del repo hoy: convierte la peor noche del
  sistema en algo que se puede consultar. Después **A2**, que es una decisión de
  arquitectura, y ojo: **los emisores modulares no emiten un solo evento de
  ningún tipo**, así que hoy no hay ni `boot` de ellos.
- **@backend: A3.** Con A1 hecho, es un webhook sobre `events` — y el patrón está
  escrito y desplegado en FrioSeguro (`cron-device-alerts`). Después **A10**: la
  consulta de historial de alertas, que es **el esqueleto del informe de
  octubre** y tiene el índice hecho esperándola.
- **@frontend: A4, A8 y A5.** Las dos primeras son media tarde: `resume()` del
  contexto en el primer gesto, repetir el beep mientras dure la alerta, y mover
  el `return 'ALERT'` arriba del `'OFFLINE'`. A5 necesita decidir quién ackea.
- **@comercial: esto cambia qué se puede prometer.** Hoy el sistema **no avisa**:
  muestra. Si alguien pregunta "¿y si pasa algo a la madrugada?", la respuesta
  honesta es "queda registrado en las lecturas" — y ni eso es cómodo de mirar
  (A10). No prometer aviso hasta que A1+A3 estén cerrados.
- **@cronista: el `QUE_FALTA` #1 dice que el RX "hoy es heartbeat-only" y eso ya
  no es cierto.** `esp_rx_receptor.ino` es `3.6.7-RX-palways`, con panel de
  alerta completo, gateway HTTP con cola asíncrona, OTA y comandos. Lo que falta
  de la Task 08 no es el LCD ni el buzzer: es **de dónde saca los datos** (A2).
  Conviene reescribir ese ítem con el fix, no antes.
- **@verificador:** el DoD es *"cada eslabón del aviso tiene un hecho del repo
  que lo confirma o lo desmiente"*. Los 128 tests son el oráculo y `TestRepoReal`
  fija los 11 hallazgos. **Puntos a atacar, en orden:**
  1. **A1 es el más sólido y el más fácil de cerrar de verdad**: consultá
     `events` en el Supabase real. Si hay una sola fila de alerta, el hallazgo se
     cae; si hay cero —y va a haber cero— queda cerrado sin discusión.
  2. **A2 es el más valioso y el que más depende de una premisa**: cuál familia
     va a octubre. Empezá por conseguir esa respuesta por escrito; sin ella el
     hallazgo es condicional.
  3. **A4 tiene dos mitades**: la política del navegador (fuera del repo,
     verificable en un minuto) y el disparo por flanco (hecho del código).
  4. **A6 y A7 son decisiones, no bugs**, y están en warn por eso: lo auditable
     es que **nadie las cruzó** — el cap de una hora y la ventana de stale se
     eligieron por separado.
  5. **A9 y A11 son los más discutibles** y están en info: uno no molesta hasta
     que alguien emita, el otro es una decisión de producto.
