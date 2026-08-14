# Nocturno local — 2026-08-13-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-13-b-puesta-en-marcha-campo` (pusheado, `b4de791`).

## TL;DR

**El RX ya resolvió la puesta en marcha en campo. A y B no heredaron nada.**

El RX parpadea el LED mientras el portal está abierto (*"así el operario
distingue AP esperando config de device dormido"*, dice su propio comentario),
abre el portal si le mantenés BOOT 2 s, y trae la red de Dreyfus hardcodeada con
self-learn a NVS. Los emisores no tienen **ninguna** de las tres — y son los
emisores los que van atornillados al eje, no el RX, que vive en el tablero.

`docs/DEPLOYMENT_DREYFUS.md` —la hoja que además ve el cliente— describe con
bastante fidelidad **el comportamiento del RX** y lo presenta como el de los
tres. De ahí sale casi todo lo demás.

De los 8 pasos del procedimiento de provisioning, **5 son ejecutables, 2 tienen
fricción y 1 está BLOQUEADO**, y el bloqueo es el **paso 2**: *"esperar 15-25 s
mirando el LED"*. En A/B ese LED no parpadea nunca, y el AP ni siquiera existe a
los 15-25 s (antes hay dos intentos de conexión de 15 s).

Y los dos remedios que la hoja le da al instalador **hacen lo contrario de lo
que dicen, en silencio**: `factory_reset` conserva el WiFi que prometía borrar y
borra la calibración de la galga que no prometía tocar; "Cambiar perfil →
AHORRO_MAX" deja el nodo despertando cada 60 s sin corte por batería, con ack
verde en el dashboard.

## Tarea elegida y por qué

Por rotación tocaba galgas (los cuatro turnos previos fueron cosechador,
frioseguro, datalogger ×2; la última noche de galgas fue el 08-11).

Los 🔴 del `QUE_FALTA` sin branch siguen siendo banco o hardware. Y las seis
auditorías previas de este repo empiezan, todas, con **el nodo ya andando**:

| noche | qué audita | dónde empieza |
|---|---|---|
| 07-29 `vpp-field-characterization` | qué significa el v_pp | nodo corriendo |
| 08-04 `contrato-comandos` | forma de los comandos | nodo corriendo |
| 08-06 `identidad-ota` | quién es cada nodo para el OTA | nodo corriendo |
| 08-07-b `contrato-schema` | forma de lo que entra a la DB | nodo corriendo |
| 08-09-b `cadena-medicion` | galga → número | nodo corriendo |
| 08-11 `cadena-entrega` | número → card del SCADA | nodo corriendo |

**Nadie audita cómo el nodo llega a estar andando.** Y ese tramo importa ahora:
en octubre hay que instalar tres equipos en una parada de planta con ventana
fija, y el documento con el que se va a hacer nunca se cruzó contra el firmware.
La pregunta que elegí:

> el instalador llega con los 3 equipos y un celular, sigue la hoja paso por
> paso. **¿Cada paso es ejecutable? ¿Los remedios que la hoja le da cuando algo
> sale mal, hacen lo que dicen?**

Elegí este ítem sobre cualquier otro porque **F3+F4 valen antes de la próxima
salida a campo, no después** (hoy el remedio del manual destruye la calibración
de una galga instalada), y porque **F7 toca el ítem #6 del QUE_FALTA**: hay que
mover las credenciales de desarrollo **antes** de cerrar el bucket público, no
después.

## Qué hice

**`tools/check_field_commissioning.py`** (stdlib, solo lectura, sin red ni
hardware, no compila nada). Cruza `wifi_provisioning.h`, `nvs_config.h`,
`protocol.h`, `gateway_discovery.h`, los `config.h` y el `command_handler.cpp`
de A y B, el `.ino` del RX **como implementación de referencia**, la hoja de
entrega y el dashboard. Exit 0/1/2/3, `--json`, `--detail`, `--fail-on`,
`--root`.

**Dos oráculos** que demuestran los hallazgos en vez de afirmarlos:

- `--demo-campo` recorre los **8 pasos** de la sección 2 como quien instala un
  emisor por primera vez y marca cada uno *ejecutable / fricción / BLOQUEADO*.
  Resultado: **5 / 2 / 1**, primer freno en el PASO 2.
- `--demo-remedios` toma los **tres remedios** que la hoja le ofrece al
  instalador y deduce, efecto por efecto, qué le pasa realmente al nodo.

**`tools/test_check_field_commissioning.py` — 79 tests en 7 capas:** utilidades
de texto, extractores sobre fuentes sintéticas, los dos oráculos con números
fijados, un test por código de hallazgo sobre un **repo sintético sano al que se
le inyecta un solo defecto** (control negativo + delta), la capa "no salta
cuando no corresponde", regresión sobre el repo real y CLI.

**`docs/field-commissioning.md`** — el análisis completo y el orden de arreglo.

### Lo que hubo que resolver

- **`pinMode(LED_PIN, ...)` no es una señal.** Mi primer detector de F1 daba por
  buena cualquier mención de `LED_PIN` en el archivo del portal — y así un
  `pinMode()` suelto alcanzaba para declarar que el operario tiene aviso. Ahora
  exige una **escritura** al pin (`digitalWrite`/`ledcWrite`/`analogWrite`); la
  mutación que afloja eso hace fallar 4 tests.
- **Leer un `case` sin comerse el siguiente.** Si el corte del `switch` es
  flojo, `CMD_FACTORY_RESET` hereda el `wifiResetCreds()` de un case vecino y
  **F3 se disuelve**. El corte quedó deliberadamente agresivo (quedarse corto
  sólo pierde evidencia; pasarse inventa que el bug no existe), y hay un test
  que pone el `wifiResetCreds()` en el case de al lado y exige que F3 igual
  salte.
- **F5 no es "el nombre no existe", es "el ack miente".** Escrito como
  comparación de vocabularios, el hallazgo se arreglaba renombrando el
  documento. El defecto real es el **fallback silencioso con `return 0`**: hay
  un test donde el firmware rechaza el profile desconocido y F5 **no** salta,
  aunque el documento siga diciendo `AHORRO_MAX`.
- **F1 tampoco podía ser "el LED no está en `wifi_provisioning.h`".** El portal
  se podría señalizar desde el `.ino`. La condición exige que **todos** los usos
  del LED en el emisor estén dentro de `identify`; hay test con el parpadeo
  puesto en el `.ino` que verifica que no salte.
- **Los `.bin` sólo cuentan si tienen SSID *y* clave.** Con `any` en vez de
  `all`, un bin que casualmente contenga la palabra del SSID entraba como fuga.
  Hay test con dos bins sintéticos, uno con cada cosa.
- **F10 no podía depender sólo de los flags de banco.** Los flags son un
  pendiente ya conocido (QUE_FALTA #2/#3). El hallazgo es la **combinación** con
  lo que el documento de entrega le promete al cliente; el repo sintético sano
  ya trae la promesa y no enciende nada.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **5 error · 5 warn · 3 info.**

| código | sev | qué |
|---|---|---|
| **F1** | error | **el LED que el instructivo manda mirar no existe en A ni en B.** `LED_PIN=2` se escribe únicamente dentro del `case CMD_IDENTIFY` de `command_handler.cpp`; `wifi_provisioning.h` —donde vive **todo** el portal del emisor— no lo toca ni una vez. El instalador busca la red `GALGAS_A` a ciegas. El RX **sí** parpadea 1 Hz mientras el portal está abierto. |
| **F2** | error | **el portal dura 60 s, no los 5 min que promete la hoja.** `AP_PORTAL_TIMEOUT_S=60`; la extensión a `AP_PORTAL_EXTEND_S=300` ocurre **cuando un cliente ya se conectó**. Los 5 minutos son para tipear la clave, no para llegar. Sumado a F1: ~1 minuto para adivinar que el AP se abrió. |
| **F3** | error | **`factory_reset` es el remedio documentado para borrar el WiFi y es lo único que no borra.** Llama sólo a `nvsFactoryReset()` (namespace `galgas`); las credenciales viven en el NVS del stack (`WiFi.persistent(true)`) + el de WiFiManager. La función que sí las borra —`wifiResetCreds()`— existe, está citada en el comentario de `nvsFactoryReset()`… y **no la llama nadie**. Código muerto. En campo: el nodo quedó con la red equivocada, el instalador manda el remedio del manual, y el nodo se reconecta a la misma red equivocada. |
| **F4** | error | **`factory_reset` borra la calibración de la galga y deja el nodo en perfil de banco.** `p.clear()` se lleva las 15 keys, incluidas `cal_k`/`cal_offset`, los thresholds y el flag `first_boot`; sin ese flag el boot siguiente re-siembra `POWER_USB_BENCH` ⇒ `period_s=60` y `batt_check_enabled=false`. El remedio para un problema de **red** deja el nodo despertando cada minuto, **sin corte por batería**, midiendo con k=1.0/offset=0.0 — y ningún campo del reading dice que perdió la calibración. La hoja no advierte nada. |
| **F5** | error | **el vocabulario de perfiles de la hoja no existe en el firmware modular y cae al peor default.** La hoja opera con `AHORRO_MAX`/`ALWAYS_ON`/`NORMAL` (son los perfiles de la familia **legacy** `ota_wm_pp`); `powerProfileFromStr()` conoce `usb_bench`/`bat_normal`/`bat_low` y devuelve `POWER_USB_BENCH` ante cualquier desconocido, con `return 0` (ack de éxito). Pedís *"1 h de sleep, ~6 meses de batería"* y obtenés 60 s sin cutoff, en verde. |
| **F6** | warn | **el dashboard dice que `set_power_profile` no se aplica — en A/B sí se aplica.** `App.jsx`: *"(LEGACY) … ota_wm_pp lo ackea pero NO lo aplica"*, con payload default `usb_bench`. Cierto para la familia legacy, peligroso para la modular: el dashboard es uno solo para las dos. |
| **F7** | warn | **credenciales WiFi personales versionadas y dentro de los `.bin`.** `DEV_WIFI_SSID`/`DEV_WIFI_PASS` están literales en `wifi_provisioning.h` (versionado), no en el `secrets.h` gitignoreado donde vive el resto — el propio comentario dice *"ROTAR antes de entregar al cliente"*. Están dentro de **los 15 `.bin` versionados**, que son los que se suben al bucket `firmware` de Storage, **hoy público** (QUE_FALTA #6). Las del cliente (`DREYFUS_*`) sí están bien guardadas. |
| **F8** | warn | **se le pide a IT de Dreyfus una excepción de mDNS que el sistema no usa.** `gateway_discovery.h` está deshabilitado por decisión explícita y `wifi_provisioning.h` aclara *"sin mDNS"*; la doctrina del repo lo tiene descartado por flakey. |
| **F9** | warn | **el AP de provisioning es abierto** (`AP_PASSWORD ""`) y la hoja no lo menciona. Acotado (sólo vive mientras dura el portal) ⇒ warn. |
| **F10** | warn | **la hoja promete indicadores que hoy son constantes de banco.** `DEV_BENCH_NO_BATTERY` (Vbat fijo 4.0 V) y `DEV_SIMULATE_ADC` siguen definidos en A y B, mientras la hoja describe umbrales de 3.50/3.30 V "en tiempo real". |
| **F11** | info | la tabla de puertos pide **DNS por TCP** (`TCP \| 53 / 853`). Una whitelist escrita literal deja a los nodos sin resolver, y el síntoma va a parecer "no hay internet". |
| **F12** | info | el timeout del portal **no depende del profile** (la hoja dice que sí); y con `AP_FALLBACK_THRESHOLD=1` cada wake sin red abre un AP de un minuto — el propio header estima ~23 días de autonomía en vez de ~12 meses. |
| **F13** | info | el RX tiene botón que fuerza el portal; en A/B el mismo pin está declarado con `// long press = reset wifi creds (TODO)`. |

**Orden sugerido:**

1. **F3 + F4, un solo commit.** El más barato y el más peligroso. Las dos mitades:
   que `CMD_FACTORY_RESET` llame también a `wifiResetCreds()` **y** que preserve
   `cal_*`. Más un comando `reset_wifi` separado, que es lo que el instalador
   quiere el 90 % de las veces.
2. **F5** — sacar el fallback silencioso: error ante profile desconocido. Diez
   líneas, y convierte un modo de falla mudo en un mensaje rojo.
3. **F1 + F13 — bajar del RX a los emisores** lo que el RX ya tiene probado:
   parpadeo en el lazo del portal (cinco líneas; el lazo ya existe y ya hace
   `delay(50)`) y el botón que fuerza el portal. Sin esto ningún arreglo de la
   hoja alcanza.
4. **F2 + F12** — reescribir la sección 2 con los números reales, **o** subir
   `AP_PORTAL_TIMEOUT_S` a 300 y dejar la hoja. Es una decisión de energía.
5. **F7 — antes de cerrar el bucket público** (#6), no después.
6. **F6, F8, F9, F10, F11** — higiene.

## Lo que está BIEN (fijado por test, para no ir a revisarlo)

- **El portal del emisor es no bloqueante y bien hecho**:
  `setConfigPortalBlocking(false)` + `wm.process()` en el lazo, extensión al
  conectarse un cliente y gracia de 60 s si el cliente se va. La lógica de
  ventana es correcta; lo que falta es la señal.
- **Las credenciales sobreviven al OTA y al reflasheo de la app** (viven fuera
  del namespace `galgas`). Es justamente lo que hace que F3 muerda.
- **El AP se llama `GALGAS_<id>`**: cada nodo se distingue del de al lado.
- **El scan del RX es sólo para log, no filtra**, con el comentario que explica
  el bug que eso causó. Es la clase de decisión que hay que copiar a los emisores.
- **Los secretos del cliente están bien**: `DREYFUS_SSID`/`DREYFUS_PASSWORD` en
  `secrets.h`, gitignoreado.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-13-b-puesta-en-marcha-campo

python tools/check_field_commissioning.py                  # informe; exit 3
python tools/check_field_commissioning.py --detail         # + evidencia y hechos
python tools/check_field_commissioning.py --demo-campo     # los 8 pasos, uno por uno
python tools/check_field_commissioning.py --demo-remedios  # qué hace cada remedio
python tools/check_field_commissioning.py --json

python -m unittest tools.test_check_field_commissioning    # -> Ran 79 tests, OK
```

Cuatro hallazgos se comprueban **sin la herramienta**:

- `grep -n "digitalWrite" firmware/shared/wifi_provisioning.h` → **cero hits** (F1)
- `grep -rn "wifiResetCreds" firmware/ --include=*.cpp --include=*.ino` → **cero llamadores** (F3)
- `grep -n "AHORRO_MAX" firmware/shared/protocol.h` → **cero hits** (F5)
- `strings bins_ota_0.8.1/esp_a_emisor_0.8.1-A-otatest.bin | grep -i pazos` (F7)

**Verificado en esta máquina:**

- `py_compile` de los dos archivos.
- **79 tests en verde** (1,9 s). Sin descargas ni toolchains: cero riesgo de
  timeout.
- **Control negativo real:** un repo sintético sano no enciende **nada**, y cada
  defecto inyectado por separado enciende **uno y sólo un** código. Ocho
  hallazgos tienen además su test "no salta cuando no corresponde".
- **Verificado por mutación — las 9 hacen fallar la suite:** aflojar el detector
  del LED a cualquier mención de `LED_PIN`, no cortar el `case` del switch,
  contar la definición de `wifiResetCreds()` como llamador, `any` en vez de
  `all` en el escaneo de los `.bin`, comparar `!=` en vez de `>` en el timeout
  del portal, invertir la prioridad de severidades del exit code, sacarle a F5
  la exigencia del ack, sacarle a F1 la exigencia de que el LED sea sólo de
  `identify`, y sacarle a F4 la exigencia del seed de banco.
  *(El andamio de mutación fue descartable: no se commiteó. Borré el
  `__pycache__` antes de cada corrida y restauré el archivo al final.)*
- **No se tocó una sola línea de firmware, ni de `web/`, ni de `backend/`, ni
  `data/field_captures/`.** El branch agrega 3 archivos y edita `QUE_FALTA.md`.
  No corrí `npm run build` porque no toqué `web/`.

## Qué quedó sin verificar

- **Todo sale de leer el repo, no de mirar una instalación.** Los oráculos
  demuestran el efecto de lo que dice el código; no que la placa lo haga.
- **F3 se apoya en dónde viven las credenciales de WiFiManager** (namespace
  propio, fuera de `galgas`). Es lo que el propio repo afirma en dos comentarios
  y lo que documenta WiFiManager, pero **conviene confirmarlo con la placa**:
  provisionar por el portal, mandar `factory_reset` y ver si el boot siguiente
  abre el AP o se reconecta solo. **Un minuto, sin instrumental.** Es la
  verificación de mayor valor de toda la noche. Si cayera, F3 se cae entero —
  **F4 no depende de ella**.
- **F5 no se probó punta a punta**: la caída a `usb_bench` está deducida del
  `return POWER_USB_BENCH` del fallback, no observada. Se ve en un minuto
  mandando `set_power_profile {"profile":"AHORRO_MAX"}` con el Serial abierto.
- **F1 se puede confirmar en 20 segundos**: alimentar un emisor sin red conocida
  al alcance y mirar si el LED hace algo mientras aparece `GALGAS_A`.
- **Ningún fix aplicado** — generator ≠ evaluator.

## Estado

- Branch `nocturno/local-2026-08-13-b-puesta-en-marcha-campo` pusheado
  (`b4de791`), sale de `main` (`e9cd4bc`). galgas volvió a `main` limpio.
- `QUE_FALTA.md` de galgas: punteros nuevos en **#10**, **#12** y **#14**, dentro
  del branch. ⚠️ No agregué ítems numerados nuevos a propósito, para no pelearme
  el número con los otros branches en cola; los tres punteros son bloques
  añadidos bajo ítems existentes, así que el merge es trivial.
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\datalogger` sigue con trabajo de día SIN COMMITEAR**
  (`firmwares/nodo-gimap/`, `tools/rx_gimap.py`, los dos tests del nodo GIMAP,
  `docs/ARMADO_NODO_GIMAP.html`, `.gitignore`). **No lo toqué.**
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Decimotercera noche que lo reporto:** es firmware que va a un equipo a
  2000 km y vive **sólo en este disco**. **No lo toqué.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las
  dieciocho noches anteriores: `agentes/`, `dominios/`, `enlace/`, más
  `agentes/diseno3d.md`, `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html` y
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- ℹ️ `C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-08-11-b-presupuesto-standby`. **No lo cambié.**
- ⚠️ Sigue el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando quieras.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío (sólo el `.gitkeep`). El único
  `enlace\maquinas\*.estado.json` (DESKTOP-RK8DH7C) tiene `ultima_vez_viva` del
  **2026-08-07**: el latido está parado hace 6 días. **No lo toqué** (los
  scripts de ENLACE son trabajo de día sin commitear).
- La cola de merge suma **56 branches** en origin (galgas **20**, datalogger 17,
  frioseguro 17, cosechador 2).

## Para @firmware / @hardware / @energia / @cronista / @verificador

- **@firmware:** **F3+F4 son tuyos y son un solo commit chico.** Hoy el remedio
  del manual borra la calibración de una galga instalada y deja el nodo sin
  corte por batería: es el peor par de la lista. Después **F5** (diez líneas:
  que el profile desconocido devuelva error) y **F1+F13**, que no es diseñar
  nada — es **copiar del RX** tres cosas que ya están escritas y probadas.
- **@hardware:** el checklist de instalación (#12) **no se puede escribir todavía**
  contra el firmware actual: el paso 2 del procedimiento está bloqueado. Corré
  `--demo-campo` antes de redactarlo; con F1+F13 arreglados el checklist queda
  de cinco líneas y sin fricción.
- **@energia:** **F12 y F4 son tuyos.** `AP_FALLBACK_THRESHOLD=1` significa que
  cada wake sin red enciende un AP de 60 s — el propio header estima ~23 días de
  autonomía en vez de ~12 meses. Y F4 hace que un `factory_reset` deje el nodo en
  `usb_bench` (60 s de período, sin cutoff): esos dos caminos hay que meterlos en
  el presupuesto de energía del ítem #3, porque son los que se comen la batería
  en campo, no el ciclo normal.
- **@cronista:** `docs/DEPLOYMENT_DREYFUS.md` es **el doc que ve el cliente** y
  hoy describe la familia legacy (`ota_wm_pp`) mientras se desarrolla la
  modular. Entra en el ítem #14, y es el de mayor costo si queda desincronizado:
  las secciones 2 (procedimiento), 3 (firewall) y 5 (LED, batería) hay que
  reescribirlas junto con los arreglos, no antes.
- **@verificador:** el DoD es *"cada paso del procedimiento de puesta en marcha
  tiene un hecho del repo que lo confirma o lo desmiente"*. Los 79 tests son el
  oráculo y `TestRepoReal` fija los 13 hallazgos. **Puntos a atacar, en orden:**
  (1) **F3 es el único hallazgo con una premisa fuera del repo** —dónde persiste
  WiFiManager sus credenciales—; si cayera, F3 se cae entero (F4 no depende de
  ella) y es el más barato de confirmar: un `factory_reset` con el Serial
  abierto. (2) **F5 está deducido del camino de código**, no observado. (3)
  **F9 es el más discutible**: el AP sólo existe mientras dura el portal, así
  que la exposición es física y acotada — está en warn por eso.
