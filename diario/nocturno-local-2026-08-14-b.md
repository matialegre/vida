# Nocturno local — 2026-08-14-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**P1 — LA PALANCA DE PLATA**).
**Branch:** `nocturno/local-2026-08-14-b-cadena-continuidad` (pusheado, `6028370`).

## TL;DR

FrioSeguro se vende con una promesa de una línea: **"el servicio avisa"**. El
evento contra el que se vende es el corte de luz. Y el corte de luz **apaga la
heladera y apaga el monitor con la misma llave**.

Nadie había recorrido nunca esa cadena. Las seis auditorías offline previas del
repo empiezan todas con el equipo encendido y conectado.

**De los 8 eslabones: 0 ejecutables, 3 con fricción, 5 ROTOS.** Y los cinco
rotos comparten una sola causa: **el único que podría avisar de la falla es el
que falló.**

Tres números, sacados del propio código del repo:

- **`devices.is_online` se escribe 3 veces en TRUE y 0 en FALSE.** El único
  FALSE del sistema es el `DEFAULT` de la columna — o sea el estado *"nunca
  reportó"*. Un equipo que reportó una vez y después murió queda **verde para
  siempre**, y ningún cron mira `last_seen_at`. El contador de `offline` del
  panel admin, por construcción, solo puede contar equipos que nunca hablaron.
- **Un corte de 6 horas son 2160 lecturas que no existen y de las que no queda
  registro.** No hay buffer, y el timer de sync **se rearma antes de mirar si
  hay internet**: el dato de ese tick se cae y no se reintenta nunca. Al volver
  la luz, `last_seen_at` vuelve a `NOW()` con el primer POST y el hueco se borra
  del campo.
- **La detección del corte de luz está escrita entera y nunca corre.**
  `power_monitor.h` tiene debounce de 3 s, alerta por SMS y por Telegram. El
  campo `ac_power` viaja bajo `#ifdef POWER_MONITOR_H`, que es el include guard
  **del propio header** — y el sketch no lo incluye. El bloque se compila vacío.
  **Sin warning, sin error, sin TODO: compila limpio.**

## Tarea elegida y por qué

Por rotación tocaba frioseguro (los cuatro turnos previos: cosechador 08-11-b,
frioseguro 08-12, datalogger 08-13, galgas 08-13-b, cosechador 08-14 — el más
viejo era frioseguro). Y la jerarquía manda **PLATA**.

Dentro del repo, los 🔴 y 🟡 sin branch siguen siendo hardware (flashear, caja
estanca), nube, o decisiones de precio de Matías. Todo lo software-puro ya tenía
branch. Así que fui —como las noches anteriores en los otros repos— **al tramo
que ninguna auditoría había tocado**. Repasando qué está cubierto:

| noche | qué audita | dónde empieza |
|---|---|---|
| 07-18 `alert_model` | la **decisión** de alertar | equipo andando |
| 08-02 `telegram_gate_model` | la **entrega** del aviso | equipo andando |
| 08-03-b `check_schema_drift` | la **forma** de los datos | equipo andando |
| 08-09 `check_tenant_isolation` | el **aislamiento** entre clientes | equipo andando |
| 08-10-b `check_temperature_chain` | de qué sonda sale el **número** | equipo andando |
| 08-12 `check_install_chain` | **poner** el equipo a andar | antes de andar |

**Las seis suponen un equipo encendido y conectado.** La pregunta que elegí es la
que ninguna responde:

> **¿Quién avisa cuando el que tiene que avisar es el que se cayó?**

Tres razones para elegirla sobre cualquier otra cosa esta noche:

1. **Es el otro core que se cobra.** El 07-18 auditó *cuándo* se dispara la
   alerta. Esto audita si **hay alguien vivo para dispararla**.
2. **El fix más importante que salió no toca firmware ni hardware.** Es un cron
   de SQL. Es de las poquísimas cosas del repo que Matías puede cerrar **de día,
   solo, sin banco y sin comprar nada**.
3. **Faltan 4 días para el 18-ago** (meta: 3 abonos). Lo que sale de acá cambia
   qué se puede **prometer** en la venta — y encontró un documento que **no hay
   que usar como material comercial** hasta arreglarlo (ver R4).

## Qué hice

**`tools/check_continuity_chain.py`** (stdlib, solo lectura, sin red ni
hardware, no compila nada). **No inventa números: los LEE** de
`firmware_modular/`, `supabase/`, `web-dashboard/src/` y
`ESCENARIOS_CUBIERTOS.md`, y cita `archivo:línea` de cada afirmación. Exit
0/1/2/3, `--json`, `--detail`, `--fail-on`, `--root`.

**Tres oráculos** que demuestran los hallazgos en vez de afirmarlos:

- `--demo-apagon` recorre los **8 eslabones** como quien vive el corte y marca
  cada uno *ejecutable / fricción / ROTO*. Resultado: **0 / 3 / 5**, primer
  eslabón roto: el **2** (la detección del corte).
- `--demo-latch` lista **todas** las escrituras de `is_online` y de
  `state.wifiConnected`, con dirección y `archivo:línea`, y después dice quién
  podría apagarlas y si existe.
- `--demo-hueco` cuantifica un corte de N horas: cuántas lecturas se pierden,
  cuántas quedan, y **qué reporta cada superficie al volver la luz**.

**`tools/test_check_continuity_chain.py` — 103 tests en 7 capas:** utilidades de
texto, extractores sobre fuentes sintéticas, los tres oráculos con números
fijados, **control negativo** (un repo sintético sano no enciende nada), un
defecto inyectado por vez que enciende **exactamente** su conjunto de códigos,
la capa "no salta cuando no corresponde", y regresión sobre el repo real + CLI.

**`docs/continuity-chain.md`** — el análisis completo y el orden de arreglo.

### Lo que hubo que resolver

- **Un checker que hardcodea las dos mitades de una contradicción no sirve.**
  Casi todo hallazgo acá es una contradicción **interna**. Por eso **parsea**:
  corregida la fuente, el hallazgo se apaga solo. Hay test de eso para los nueve.
- **El `#ifdef` sobre un include guard fue el hallazgo más silencioso de la
  noche, y casi se me pasa.** `#ifdef POWER_MONITOR_H` parece un feature flag; es
  el guard del header. La regla que lo caza —sacar el guard del propio archivo y
  cruzarlo contra los `#include` del sketch— vale para cualquier módulo opcional
  del repo, no solo para éste.
- **Las citas del documento de cobertura traen el rango de líneas adentro del
  backtick.** `` `connectivity_manager.h:201-205` ``. Mi primera versión pedía la
  extensión pegada al backtick de cierre y **perdía la mitad de la tabla en
  silencio** — incluyendo los dos archivos que sostienen todo el bloque de
  CONECTIVIDAD. Lo cazó un test. La mutación que lo revierte ahora falla.
- **`esp_ota_ops.h` no es del repo.** Contar los headers del SDK como "archivos
  faltantes" inflaba R4 con un falso positivo. Hay lista de exclusión.
- **R6 no podía dispararse por las etiquetas de causa.** Que la nube tenga
  `power_loss` en su diccionario no es un defecto — es evidencia de para qué fue
  escrita. El disparador quedó en lo verificable: **la nube espera un
  `alert_type` que el firmware nunca emite**.
- **R2 tuve que achicarlo para que fuera cierto.** Mi primera redacción decía que
  el equipo no reconecta. Falso: el stack de Arduino reconecta solo. Lo que sí es
  verificable —y es lo que rompe la cadena— es que **el firmware no se entera**:
  el loop no llama `WiFi.status()` ni una vez y `reconnectWiFi()` no tiene un
  solo call site.
- **R1 y R9 son el mismo defecto visto en dos superficies** (la base y la
  pantalla), así que el test del control negativo los espera **juntos** en vez de
  fingir que son independientes. Todo el resto es un código por defecto.
- **Los defaults `out=sys.stdout` se evalúan al importar.** Los tests de CLI
  capturaban stdout y el informe salía igual por la consola real. Se resuelve
  adentro de la función.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **5 error · 2 warn · 2 info.**

| código | sev | dueño | qué |
|---|---|---|---|
| **R1** | error | @backend | **`devices.is_online` es un latch.** 3 escrituras a TRUE (INSERT de primer boot, heartbeat, y el trigger `update_device_last_seen` que corre con **cada** lectura), 0 a FALSE. No hay camino de vuelta. |
| **R2** | error | @firmware | **El mismo latch adentro del ESP32.** `state.wifiConnected` no se recalcula nunca: el loop **no llama `WiFi.status()`**, y `reconnectWiFi()` (`wifi_utils.h:106`) **no tiene un solo call site**. El equipo no queda desconectado para siempre — queda **sin saber** que se desconectó. |
| **R3** | error | @firmware | **No hay buffer offline.** `if (now - X >= INTERVAL) { X = now; if (internetAvailable) enviar(); }` — el reloj avanza igual. **16 puntos** del firmware donde un `if (!state.internetAvailable) return` deja caer el dato. El hueco es indistinguible de *"no pasó nada"*. |
| **R4** | error | @cronista | **`ESCENARIOS_CUBIERTOS.md` describe otro sistema.** Declara **34/34 ✅**, su "Firmware base" es `firmware_v2/src/` —que no existe— y faltan **8 de los 14** archivos que cita. Los **7 escenarios de CONECTIVIDAD**, justo los que responden esta pregunta, se apoyan en `connectivity_manager.h` y `offline_buffer.h`. |
| **R5** | error | @firmware | **`ac_power` nunca se envía** (ver TL;DR). La base tiene la columna, `v_devices_status` la selecciona, la lógica está escrita completa. **Falta el `#include`.** |
| **R6** | warn | @backend | **El único camino de push es reactivo.** `cron-device-alerts` se llama cron pero es un webhook sobre `alerts`: necesita una fila. Un equipo sin luz no inserta filas. Y sus `REBOOT_CAUSE_LABELS` ya traducen `power_loss` y `brownout` — **la mitad de la nube está escrita esperando un mensaje que la mitad del firmware no emite**. |
| **R7** | warn | @backend | **Ningún cron mira `last_seen_at`.** Los 3 registrados son vencimiento de abono y dos limpiezas. **La cuenta ya está hecha**: `v_devices_status` expone `seconds_since_seen`. Nadie la consulta. |
| **R8** | info | @firmware | **Sin watchdog propio en el sketch.** Un cuelgue es el modo de falla que más se parece a "todo bien": sigue alimentado, sigue asociado, y `last_seen_at` deja de avanzar sin que nadie mire. |
| **R9** | info | @frontend | **Dos verdades contradictorias en la misma pantalla.** La frescura (`hace X`) se calcula bien desde el `created_at` — **es el único eslabón de la cadena que funciona**. Al lado se pinta el `is_online` que no puede apagarse. |

**Orden sugerido:**

1. **R7 — el cron que vigila el silencio. Es la pieza más barata de toda la
   cadena y la que más cambia.** Un cron cada 15 min que haga `INSERT` en
   `alerts` cuando `seconds_since_seen` pase un umbral **reusa el push que ya
   está desplegado** y **no toca una línea de firmware**. Convierte cinco modos
   de falla mudos en un mensaje al celular. *Sin esto, arreglar los otros no se
   puede verificar en el campo.*
2. **R1** — el mismo cron lo apaga. Van juntos.
3. **R5** — una línea (`#include "power_monitor.h"`), pero enciende hardware
   (GPIO34/35 + optoacoplador): **verificar en banco antes de flashear a un
   cliente**.
4. **R3** — el buffer. El más caro y el que menos urge: sin R7, los datos
   recuperados llegan a un sistema que igual no avisó.
5. **R2 + R8** — que el firmware sepa que se cayó, y que vuelva si se cuelga.
6. **R9** — frontend puro, media hora.
7. **R4** — reescribir el documento **después** de los fixes, no antes.

## Lo que está BIEN (fijado por test, para no ir a revisarlo)

- **El dashboard calcula la frescura correctamente**, con tres niveles
  (`fresh` / `stale` / `very-stale`). Único eslabón sano de la cadena.
- **`v_devices_status` ya expone `seconds_since_seen`.** La aritmética de R7 está
  hecha; falta el consumidor.
- **`power_monitor.h` está escrito completo**, no esbozado. R5 es un `#include`,
  no un desarrollo.
- **`cron-device-alerts` maneja bien las suscripciones push**: limpia las
  expiradas (404/410) y vibra distinto para los eventos de sistema.
- **El heartbeat manda datos de salud reales** (`uptime_sec`, `free_heap`,
  `wifi_rssi`). El problema no es que no reporte: es que **su ausencia no dispara
  nada**.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-14-b-cadena-continuidad

python tools/check_continuity_chain.py                     # informe; exit 3
python tools/check_continuity_chain.py --detail            # + evidencia archivo:linea
python tools/check_continuity_chain.py --demo-apagon       # los 8 eslabones
python tools/check_continuity_chain.py --demo-latch        # todas las escrituras
python tools/check_continuity_chain.py --demo-hueco --horas 6
python tools/check_continuity_chain.py --json

cd tools && python -m unittest test_check_continuity_chain  # -> Ran 103 tests, OK
```

Cuatro hallazgos se comprueban **sin la herramienta**:

```bash
grep -rn "is_online" supabase/SETUP_COMPLETO.sql firmware_modular/supabase.h   # R1
grep -rn "reconnectWiFi\|WiFi.status()" firmware_modular/*.h firmware_modular/*.ino  # R2
grep -n "#include" firmware_modular/firmware_modular.ino | grep power_monitor   # R5
grep -n "cron.schedule" supabase/SETUP_CRON_JOBS.sql                            # R7
```

**Verificado en esta máquina:**

- `py_compile` de los dos archivos.
- **103 tests en verde** (8,6 s). Sin descargas ni toolchains: cero riesgo de
  timeout.
- **Control negativo real:** un repo sintético sano no enciende **nada** (exit 0,
  cadena sin ningún eslabón roto), y cada defecto inyectado por separado enciende
  **exactamente** el conjunto esperado. Los nueve tienen además su test "no salta
  cuando no corresponde".
- **Verificado por mutación — 15 mutaciones, las 15 hacen fallar la suite:**
  latch sin exigir cero FALSE · R2 sin mirar si el loop consulta `WiFi.status()`
  · R3 sin exigir ausencia de buffer · R4 sin umbral · R5 sin exigir que el
  header no esté incluido · R6 disparando por las etiquetas de causa solas ·
  refs sin el sufijo de líneas · cron-staleness sin marcadores · call sites
  contando la definición como llamada · sync-timers sin exigir que el reloj se
  rearme primero · `strip_line_comments` sin respetar strings · exit code con la
  severidad menos grave · R9 sin exigir el latch · fuentes de firmware sin filtro
  de extensión · `find_anywhere` sin excluir `node_modules`/`build`.
  *(La primera pasada dejó **tres mutaciones vivas**: en las tres el guard era
  correcto y **el test era flojo**. R3: el repo sano nunca ejercitaba el guard
  del buffer porque tampoco tenía gates pelados — agregué el caso realista
  (buffer + un gate suelto en otro camino). Las otras dos: los filtros de
  extensión y de `node_modules` no tenían ningún test directo. Los tres tests
  nuevos prueban el contrato declarado, no la mutación. El andamio fue
  descartable, en `/tmp`: **no se commiteó**. Borré el `__pycache__` antes de
  cada corrida y restauré el archivo al final.)*
- **No se tocó firmware, ni SQL, ni el dashboard, ni ninguna decisión de compra.**
  El branch agrega 3 archivos y edita `QUE_FALTA.md`.

## Qué quedó sin verificar

- **Todo sale de leer el código, no de correr un sistema.** No hay equipo
  flasheado ni proyecto Supabase al que consultar de noche.
- **R1 y R7 se apoyan en el SQL canónico (`SETUP_COMPLETO.sql`).** Si en el
  Supabase real alguien agregó a mano un cron o un trigger que apaga `is_online`,
  los dos se caen. **Se verifica en un minuto de día:**
  `SELECT jobname, schedule FROM cron.job;`. Es la misma clase de hueco que
  encontró la noche del 08-09 con `migration_fixes_2026-07-13.sql`.
- **R4 cuenta como "presente" a `ota_update.h`, que hoy sólo existe en
  `firmware_revival/` — trabajo de día SIN COMMITEAR.** En un clone limpio
  faltarían **9 de 14**, no 8. Y el checker sólo verifica que el archivo exista
  *en alguna parte*: **ninguno de los 6 "presentes" está en el directorio que el
  documento declara**.
- **R5 supone que enchufar `power_monitor.h` funciona.** Pide GPIO34/35 y un
  optoacoplador que **no está en el BOM comercial**. El `#include` es una línea;
  que el número signifique algo es hardware.
- **R8 no dice que falte watchdog en el binario** (el core arma el suyo): dice
  que el sketch no configura ninguno propio ni reporta la causa del reset.
- **El eslabón 1 no lo puede contestar el software.** *"¿El kit lleva respaldo de
  energía?"* no está escrito en el repo, y de esa respuesta dependen los otros
  siete. **Aunque la respuesta sea "no", hay que escribirla** — cambia lo que el
  producto puede prometer.
- **Ningún fix aplicado** — generator ≠ evaluator. Ni siquiera R5, que es una
  línea: el que decide encender el monitor de corte tiene que ser el que puede
  probarlo en banco.

## Estado

- Branch `nocturno/local-2026-08-14-b-cadena-continuidad` pusheado (`6028370`),
  sale de `main` (`ddf5134`). **frioseguro quedó en `main` limpio.**
- `QUE_FALTA.md` actualizado **dentro del branch** (ítem 19 nuevo, al final de
  los 🟡). No pisa las secciones de los otros 17 branches: es un ítem propio.
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Decimoquinta noche que lo reporto**, y esta noche además **le pegó al
  análisis**: `ota_update.h` sólo existe ahí, así que R4 cuenta 8 faltantes en
  vez de 9. Es firmware que va a un equipo a 2000 km y vive **sólo en este
  disco**. **No lo toqué.**
- ⚠️ **`C:\Proyectos\datalogger` sigue con trabajo de día SIN COMMITEAR**
  (`firmwares/nodo-gimap/`, `tools/rx_gimap.py`, los dos tests del nodo GIMAP,
  `docs/ARMADO_NODO_GIMAP.html`, `.gitignore`). **No lo toqué.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las
  veinte noches anteriores: `agentes/`, `dominios/`, `enlace/`, más
  `agentes/diseno3d.md`, `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html` y
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- ⚠️ Sigue el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando quieras.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío (sólo el `.gitkeep`). El único
  `enlace\maquinas\*.estado.json` (DESKTOP-RK8DH7C) sigue con `ultima_vez_viva`
  del **2026-08-07**: el latido está parado hace **7 días**. **No lo toqué** (los
  scripts de ENLACE son trabajo de día sin commitear).
- La cola de merge suma **58 branches** en origin (galgas 20, datalogger 17,
  frioseguro **18**, cosechador 3).

## Para @backend / @firmware / @frontend / @hardware / @comercial / @cronista / @verificador

- **@backend: R7 y R1 son tuyos, y son la noche entera.** El cron de silencio es
  una función SQL de seis líneas más un `cron.schedule`. Reusa
  `seconds_since_seen`, que **ya está calculado en `v_devices_status`**, y el
  push, que **ya está desplegado**. Es el mejor ratio esfuerzo/resultado de todo
  el repo hoy: convierte cinco modos de falla mudos en un mensaje al celular, sin
  tocar firmware. Después **R6**: definir el `alert_type` de "equipo en silencio"
  y el de "volvió", que hoy no existen.
- **@firmware: R5 primero** — una línea, pero verificala en banco antes de que
  vaya a un cliente. Después **R2** y **R8**. Y ojo con **R3**: el patrón del
  `X = now` antes de saber si hay red está en **cinco timers** de
  `supabaseSync()` — si tocás uno, tocá los cinco.
- **@frontend: R9.** El dato correcto ya lo tenés en la misma función: derivá el
  color del mismo `created_at` con el que ya calculás el "hace X". Media hora, y
  saca una etiqueta verde que hoy miente.
- **@hardware: el eslabón 1 es tuyo y no lo puede resolver el software.**
  *"¿El kit lleva respaldo de energía?"* — de esa respuesta dependen los otros
  siete eslabones. Y si R5 se va a encender, el optoacoplador para GPIO34 **no
  está en el BOM comercial**.
- **@comercial: cuidado con `ESCENARIOS_CUBIERTOS.md` (R4).** Es el documento que
  uno le mostraría a un cliente que pregunta *"¿y si se corta la luz?"*, y hoy
  dice **34/34 ✅** sobre un firmware que no está en el repo. **No lo uses como
  material de venta hasta que R4 esté cerrado.** Y el límite de responsabilidad
  del ítem 6 del QUE_FALTA ("el servicio avisa, no garantiza la mercadería")
  conviene redactarlo **sabiendo esto**.
- **@cronista:** `ESCENARIOS_CUBIERTOS.md` no es drift chico: **describe otro
  árbol de firmware**. Conviene reescribirlo contra `firmware_modular/` junto con
  los fixes, no antes — si se reescribe ahora, queda un documento honesto que
  dice "no cubierto" en 7 de 7 escenarios de conectividad, y eso también hay que
  decidirlo.
- **@verificador:** el DoD es *"cada eslabón de la cadena del apagón tiene un
  hecho del repo que lo confirma o lo desmiente"*. Los 103 tests son el oráculo y
  `TestRepoReal` fija los 9 hallazgos. **Puntos a atacar, en orden:**
  1. **R1 y R7 son los más sólidos** (aritmética y conteo) pero los más
     dependientes de que el Supabase real coincida con el SQL del repo. Empezá
     por ahí: una consulta y quedan cerrados o caídos.
  2. **R4 es el que más cambia según qué hay en el working tree** (el
     `ota_update.h` sin commitear). Corrélo sobre un clone limpio.
  3. **R2 es el más fácil de leer de más**: no dice que el WiFi no vuelva.
  4. **R5 es el más filoso y el más barato de confirmar**: `grep #include`.
  5. **R8 y R9 están en info porque son los más discutibles**, y R6 en warn
     porque "reactivo" es una decisión de diseño defendible **si existe R7**.
