# Nocturno local — 2026-08-07

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (P1 — PLATA).
**Branch:** `nocturno/local-2026-08-07-revival-superficie-lan` (pusheado, commit `c5c492d`).

## Tarea elegida y por qué

Los últimos turnos fueron galgas (08-06), datalogger (08-06-b), frioseguro
(08-05). Por rotación tocaba frioseguro — y ahí me encontré con que **el trabajo
de día sin commitear que vengo reportando hace dos noches no es un archivo
suelto: es una operación de campo en curso.**

`REVIVAL_2026-08.md` + `firmware_revival/` + `kit_santacruz/`: @firmware preparó
un firmware nuevo (v2.1.0) para el ESP32 del reefer del **Campamento Parametican
Silver (Cerro Moro, Santa Cruz)**, que se flashea por USB vía Chrome Remote
Desktop para que de ahí en más se actualice **por WiFi**. Firmware compilado,
binarios con SHA, runbook, kit de herramientas, y hasta un `CLAUDE.md` para la
sesión que corre en la notebook de allá.

Elegí auditarlo. La razón, en una tabla:

| | |
|---|---|
| Distancia al equipo | **2000 km** |
| Quién está del otro lado | Andrés, operario **no técnico**, por WhatsApp |
| Recuperación si algo sale mal | **cable USB** — no hay otra |
| Lo que el REVIVAL agrega | tres endpoints que **reescriben el firmware** |
| Lo que el REVIVAL cambia | de qué red se cuelga el equipo |

Y ese último renglón es toda la tesis:

> **ANTES:** el ESP32 vivía en una LAN conocida. Su API REST sin autenticación
> era una decisión defendible: quien estaba en la red, ya estaba adentro.
>
> **AHORA:** `wifi_open.h` lo conecta a la **red ABIERTA de terceros con mayor
> RSSI** que encuentre en un campamento minero, y re-elige sola. Nadie sabe de
> antemano en qué LAN va a estar ni quién más está en ella.

Ninguna de las dos decisiones es mala por separado. **Juntas, sí**: el algoritmo
de redes abiertas es exactamente lo que le da valor de exploit a cada endpoint
sin credencial — y el REVIVAL sumó los endpoints que reescriben el firmware
justo en la versión que enciende ese algoritmo.

No pisa ningún branch previo de frioseguro: los 13 anteriores son resumen
mensual, vista de estabilidad, secretos, lint de provisioning y modelo de
alertas. Ninguno mira **qué puede hacer un tercero que esté en la misma WiFi**.

## Qué hice

1. **`tools/check_revival_surface.py`** (stdlib, solo lectura, sin red ni
   hardware). Lo que hizo falta resolver:
   - **Resolver los handlers registrados por referencia.** Nueve de los doce
     endpoints mutantes son `server.on("/api/relay", HTTP_POST, handleApiRelay)`:
     buscar el chequeo de credencial en el *registro* los daría a todos por
     inseguros aunque autenticaran. Hay que ir al cuerpo de la función. Y
     expandir **un solo nivel y solo lo referenciado** — con `or True` en ese
     filtro, 21 tests explotan (lo medí): cada endpoint hereda la auth de
     cualquier función del sketch y el checker se vuelve un absolvedor.
   - **Cortes balanceados que no se dejan engañar por literales.** Los handlers
     traen `server.send(200, "application/json", "{\"ok\":true}")`: contando
     paréntesis y llaves a ciegas, la llamada cierra donde no es.
   - **Sacar comentarios sin romper strings** (misma lección que la noche del
     contrato de la nube): `config.h` tiene `"https://xhdeacnw..."` y ese `//`
     no es un comentario.
   - **Anclar los chequeos de OTA a `ota_update.h`**: si alguien mueve el código
     a otro archivo, el chequeo tiene que dejar de decir que está todo bien en
     vez de callarse.

   Exit 0/1/2, `--json`, `--fail-on`, `--root`. Sirve de gate antes de flashear.

2. **`tools/test_check_revival_surface.py` — 69 tests en 7 capas:** parsers,
   cortes balanceados, resolución de handlers, enumeración de superficie, **un
   test por código de hallazgo con sketches sintéticos**, la **regresión sobre
   el sketch real** y el CLI. Los verifiqué con **mutación**: apagar el chequeo
   de `/update`, no expandir handlers, expandir sin filtrar, y aceptar 200 como
   internet — las cuatro hacen fallar la suite.

3. **`docs/revival-surface.md`** + ítem **#19** en `QUE_FALTA.md`.

## Hallazgos (con test que los demuestra — NO corregidos, generator ≠ evaluator)

Corrida real: **17 endpoints, 12 que cambian estado, 11 sin credencial →
14 error / 7 warn / 1 info.**

- **H1 (error ×2) — `POST /api/ota/url` y `POST /api/ota/check` no piden
  absolutamente nada.** Desde cualquier notebook en la misma WiFi abierta:
  seteás la URL del manifiesto a tu servidor, forzás el chequeo, y **el equipo
  se flashea con tu binario**. El SHA-256 no defiende nada: sale del mismo
  manifiesto que provee el atacante. `setInsecure()` tampoco importa — no hace
  falta interceptar nada cuando uno *es* el servidor. Y la URL **persiste en
  NVS**: sobrevive al reboot. Es ejecución de código arbitrario, sin credencial.

- **H2 (error) — `/update` responde `200 OK - rebooting` con el password
  equivocado, o sin password ni archivo.** Éste es el que más me gustó
  encontrar, porque el chequeo **existe y lee bien**: lo verifiqué contra el
  core que se usó para compilar (`WebServer/src/Parsing.cpp:241` parsea la query
  string *antes* de `_parseForm`, y `_currentArgs` no se destruye hasta la línea
  574 — o sea después del upload; `server.arg("pw")` funciona adentro del
  callback). Lo que falla es que **el veredicto no gobierna nada**: el rechazo
  hace `return` dentro del callback de upload, y el handler principal decide con
  `!Update.hasError()` — que es **false** cuando `Update` nunca arrancó. O sea
  "no hubo error" se confunde con "salió bien". Consecuencias:
  **`curl -X POST http://<IP>/update`** —sin nada— reinicia el equipo, y es
  repetible: un script en loop deja el sistema de alarma del reefer
  permanentemente reiniciándose. Además responde éxito: quien flashee con el
  password equivocado lee `OK - rebooting` y se va convencido. **Es la misma
  clase de bug que el H1/H3 de la nube del datalogger y el H3 de FrioSeguro —
  el sistema le informa éxito al operador por un camino que no verificó** — pero
  acá el operador está a 2000 km y no puede mirar.

- **H3 (warn) — el downgrade silencioso**, encadenado con H2.
  `otaSetPending(true)` queda puesto sobre el binario **que ya estaba
  corriendo**, sin que haya habido ningún OTA. Y `isCrashReset()` incluye
  **`ESP_RST_BROWNOUT`**: con el flag sucio, el próximo bajón de tensión —en un
  campamento minero, con un relé de sirena en la misma alimentación— manda el
  equipo a la partición anterior. Sin aviso, sin relación con ningún update.
  **Atenuante que verifiqué y dejo escrito:** `esp_ota_set_boot_partition()`
  valida la imagen antes de cambiar el arranque, así que mientras el otro slot
  esté vacío (justo después del flasheo por USB) el swap falla y bootea lo
  mismo. **El riesgo se enciende recién después del primer OTA exitoso**, o sea
  después de la fase F4 del plan de pruebas. Está leído de la doc de ESP-IDF,
  **no observado**.

- **H4 (error) — el chequeo de internet certifica justo lo que debería
  detectar.** `checkInternet()` (`.ino:734`) hace
  `internetAvailable = (code == 204 || code == 200)` contra
  `google.com/generate_204`. Esa URL existe **precisamente** para distinguir
  internet real (204, sin cuerpo) de **portal cautivo** (200 con el HTML del
  login). Aceptar el 200 convierte el único chequeo capaz de detectar el caso en
  el que lo **certifica como bueno**. En un sitio cuya conectividad son redes
  abiertas de terceros, el portal cautivo no es el caso raro: **es el
  esperable**. Y el efecto pega donde se cobra: `internetAvailable = true`
  habilita las ramas de Telegram y Supabase, que fallan contra el portal **sin
  que nadie mire el resultado**. El equipo se reporta sano, con internet, y las
  alertas no salen. **Fix: un carácter.**

- **H5 (warn) — «conectado pero sin internet» es un estado estable.**
  `wifiOpenLoop()` re-elige por **desconexión** o por **RSSI débil**, nunca por
  falta de internet (`internetAvailable` no aparece en `wifi_open.h`). El equipo
  puede pegarse a la abierta más fuerte —una impresora, un AP sin uplink, un
  portal cautivo— y **quedarse ahí para siempre** con señal excelente, mientras
  la abierta de al lado sí sale. **El algoritmo optimiza la variable
  equivocada:** elige *señal*, y lo que hace falta es *conectividad*. Con H4 se
  refuerzan: uno hace que no note que no tiene internet, el otro que no haga
  nada aunque lo notara.

- **H6 (warn) — la red del operador dura hasta la primera reconexión
  automática.** `wifi_open.h` promete que la red configurada por el operador «se
  prueba PRIMERO», pero la lee con `esp_wifi_get_config(WIFI_IF_STA)` — **el
  mismo slot que reescribe cada `WiFi.begin()`** del algoritmo automático. Basta
  que el equipo se conecte **una vez** a una abierta (porque la del operador no
  estaba visible en ese scan — el viento, que es la razón de ser del módulo)
  para que la red del operador pierda la prioridad **para siempre** y su clave
  deje de estar disponible. Recuperarlo es portal en sitio o serial: **USB, o
  sea Andrés y WhatsApp.**

- **H7 (warn) — la vuelta a la red anterior asume que era abierta**
  (`wifi_open.h:217`, `tryConnect(current, NULL, ...)`): si la actual era la WPA
  del operador, la vuelta falla y el equipo queda desconectado hasta el próximo
  ciclo.

- **H8 (error) — el SHA-256 del binario descargado es opcional.** La comparación
  corre solo `if (expectSha.length() == 64 && ...)`: un manifiesto sin ese campo
  **flashea sin verificar**. La propiedad de seguridad la decide el que sirve el
  manifiesto, que es justo quien no debería poder decidirla.

- **H9 (warn ×2) — TLS sin validar** (el SHA viaja en el mismo manifiesto por el
  mismo canal) y **sin downgrade por aire** (`if (cmp < 0)`): si una versión sale
  mala, republicar la anterior no la baja. Hay que publicar una versión *mayor*
  con el contenido viejo — acordarse el día que haga falta, que es el peor día
  para acordarse. (Mismo patrón que el hallazgo de `released_at` en galgas.)

- **H10 (warn) — `reefer1234`** es la única credencial que protege `/update`, y
  está publicada en el runbook, en el repo y en `config.h`. Ya inventariado en
  `SECURITY_AUDIT.md`; se anota por esa razón puntual.

**Lo que está BIEN y queda fijado por test** (tan importante: es lo que NO hay
que ir a revisar):

- **El kit que viaja lleva exactamente estas fuentes.** `firmware_revival/` y
  `kit_santacruz/firmware/firmware_revival/` son **idénticos byte a byte** (4/4
  archivos) y los cuatro binarios comparten SHA-256 con `SHA256SUMS.txt`. La
  auditoría es sobre el firmware que se flashea, no sobre una copia derivada.
- **`/update` es el único endpoint mutante que al menos pide credencial**, y la
  lee bien. Lo roto es la aplicación del veredicto, no la lectura.
- **La red de seguridad del rollback está cableada de verdad:**
  `otaCheckRollbackOnBoot()` es lo **primero** de `setup()` (`.ino:257`), antes
  del watchdog y de todo lo demás.
- **El binario de prueba de rollback es coherente con los tiempos**: `TEST_ROTO`
  cuelga el loop a los 60 s contra los 300 s de `OTA_VERIFY_UPTIME_MS`, así que
  el flag sigue puesto cuando llega el WDT y **la prueba F4b ejerce el camino
  que dice ejercer**. No es casualidad: está calculado.
- **El watchdog se desuscribe explícitamente durante el portal WiFiManager**
  (`.ino:272-274`), que bloquea 180 s > los 120 s del WDT. Sin eso, el portal de
  rescate se reiniciaría solo justo cuando alguien lo está configurando.
- **`compareSemver` es numérico**, heredado de galgas con sus 18 tests.
- **Los 5 GET son GET de verdad**: ninguno cambia estado.

**El trabajo de @firmware está bien hecho en lo que se propuso** (rollback,
watchdog, tres vías de OTA, kit completo con runbook). Lo que falta es la
consecuencia de segundo orden de su propia decisión de conectividad.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-07-revival-superficie-lan
python tools/check_revival_surface.py                  # -> 14 error / 7 warn / 1 info, exit 1
python tools/check_revival_surface.py --json
python tools/check_revival_surface.py --fail-on warn
python -m unittest tools.test_check_revival_surface    # -> Ran 69 tests, OK
```

Gate antes de flashear:
`python tools/check_revival_surface.py && python kit_santacruz/herramientas/flashear.py --port COMx`

H2 se comprueba sin la herramienta, leyendo dos bloques de `ota_update.h`
(`:150` y `:163`) y preguntándose **qué mira el `if (ok)`**.

Los tests de `TestRepoReal` **fijan los 22 hallazgos de hoy**: si alguien
arregla uno, el test falla y obliga a actualizar `docs/revival-surface.md` en el
mismo commit.

## Qué quedó sin verificar (hardware / sitio — trabajo de día)

Todo está **leído del código, no observado**. Con el módulo **en USB** y el
backup ya hecho, en orden de valor:

1. **El bypass, en un comando:** `curl -i -X POST "http://<IP>/update"` (sin
   `?pw=`, sin archivo). Si responde `200 OK - rebooting` y el serial muestra el
   banner de arranque, H2 está confirmado en vivo.
2. **El flag después de ese POST:** `GET /api/ota/url` devuelve
   `pending_verify`. Si quedó en `true` sin haber flasheado nada, H3 deja de ser
   hipótesis.
3. **El portal cautivo:** engancharse a una abierta del sitio y mirar `STATUS`
   por serial. Si dice `Internet: SI` pero `POST /api/telegram/test` no llega,
   es H4.
4. **La red guardada:** cargar una WPA por serial, forzar conexión a una
   abierta, y ver si la WPA sigue teniendo prioridad al reconectar (H6).

- **No compilé nada.** La auditoría es estática y el kit ya trae los binarios
  compilados y verificados por SHA el 2026-08-05. **No bajé toolchains** (regla
  de disciplina de tiempo).
- **No corrí `npm run build`**: no toqué `dashboard/`.
- **No toqué el trabajo de día** (`firmware_revival/`, `kit_santacruz/`,
  `REVIVAL_2026-08.md`, el `.zip`): no lo commiteé ni lo modifiqué. Solo lo leí.
- **Los fixes son de firmware** → se aplican y se prueban en banco. **Ninguno
  aplicado.**

## Estado

- Branch `nocturno/local-2026-08-07-revival-superficie-lan` pusheado (1 commit,
  `c5c492d`: 4 archivos). frioseguro volvió a `main` limpio.
- `QUE_FALTA.md` de frioseguro: ítem **#19** (en el branch).
- ⚠️ **El objetivo auditado NO está versionado.** `firmware_revival/` y
  `kit_santacruz/` son trabajo de día sin commitear (tercera noche que lo
  reporto). La herramienta y los tests **sí** están versionados y son
  autocontenidos: sobre un checkout limpio la corrida sale **exit 3 con mensaje
  claro** en vez de fingir que está todo bien, y `TestRepoReal` se saltea.
  **Matías: commiteá el kit** — es un firmware que va a producción y hoy vive
  solo en este disco. (El `.zip` probablemente no quiera versionarse.)
- ℹ️ **`C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-07-18-modelo-energia`, no en `main`** (estado previo, no
  lo hice yo). **No lo cambié.**
- ⚠️ **Queda el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota`**
  en galgas (0 commits; su contenido ya está adentro del branch del 08-06).
  `git branch -d` cuando Matías quiera.
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las ocho
  noches anteriores: `agentes/{esquematico,pcb}.md`,
  `dominios/{comms,diseno,esquematico,firmware,hardware,logo_acceso_remoto,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`, + sin trackear `agentes/diseno3d.md`,
  `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html`,
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- La cola de merge suma **45 branches** en origin (galgas 16, datalogger 14,
  frioseguro 14, cosechador 1). El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo
  y sin usar: falta la sesión humana.
  **Nota de prioridad:** de los 14 de frioseguro, éste es el único que toca un
  equipo **que está por salir a producción a 2000 km esta semana**. H2 y H4 son
  fixes de pocas líneas que conviene aplicar **antes** de que el módulo vuelva
  al zócalo — después, cada corrección cuesta una ventana de OTA por una red
  abierta que puede no estar.
