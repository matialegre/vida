# Nocturno local — 2026-09-01-b

**Trabajador:** worker nocturno local (Matías durmiendo). Segundo turno de la noche
(el primero fue `nocturno-local-2026-09-01.md`, galgas).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la jerarquía).
**Branch:** `nocturno/local-2026-09-01-b-el-aviso-que-no-sale` (pusheado, `f13e2fe`).
**Sale de:** `main` (`4b632fa`). **No depende de ningún otro branch nocturno.**
Toca `firmware_modular/telegram.h`, `alerts.h`, `door_sensors.h`, `power_monitor.h`,
`current_sensor.h`, `config.h` y el `.ino`. Colisión menor con `08-21-b` (uptime) y
`08-27` (net_witness), que también tocan `config.h` y el `.ino` — en bloques
distintos, se mergea en cualquier orden. **Ninguno de los 26 branches abiertos toca
`telegram.h`.**

---

## TL;DR

> **El aviso que el comerciante paga por recibir se descartaba en silencio, y el
> firmware anotaba que lo había mandado.**

FrioSeguro se cobra por una sola promesa: *el servicio avisa*. La **decisión** de
alertar tiene modelo offline desde el branch `07-18` y fix desde el `08-18`. La
**entrega** —el último metro hasta el celular— no tenía ninguno.

Las cuatro fuentes de alerta (temperatura, puerta, corte de luz, sobrecorriente)
desembocaban en tres líneas de `telegram.h`:

```c
if (millis() - state.lastTelegramAlert < 300000) return;   // (1) un gate global
int code = http.POST(body);                                 // (2) solo se imprimia
state.lastTelegramAlert = millis();                         // (3) avanzaba siempre
```

El branch `08-02` ya había dejado esto documentado con 18 tests, bajo el título
correcto: *"Generator != evaluator: NADA de esto se corrigió de noche."* Los cuatro
hallazgos seguían ahí, un mes después, con fix candidato escrito y sin aplicar:

| | Qué causaba |
|---|---|
| **H1** | `state` es global → `lastTelegramAlert` arranca en 0, y `millis()` también. La línea (1) es verdadera durante los **primeros 300 s de vida del nodo**. No es un caso raro: es la ventana posterior a un corte de luz, a un reset por watchdog y a un OTA. |
| **H2** | El gate no distinguía fuente ni severidad. Un aviso de puerta abierta silenciaba 5 min a la temperatura crítica que viniera atrás, **y la descartada no se difería: se perdía**. |
| **H3** | (3) corre después de (2) sin mirarlo. Un 429, un 500 o un `-1` por TLS caído consumían la ventana igual. |
| **H4** | Los call-sites marcaban su flag (`door->alertSent`, `powerState.alertSent`) **fuera** del `if (state.internetAvailable && ...)`. Sin internet el evento quedaba marcado como avisado y no se reintentaba nunca. |

El escenario que las junta a las cuatro es el más común del negocio: **se corta la
luz.** El nodo arranca con batería, detecta el corte a los ~3 s (H1: mudo), el router
del comercio todavía no volvió (H4: marcado sin entregar), y cuando media hora después
sube la temperatura ya no queda nadie escuchando.

H3 es la **cuarta** aparición del mismo patrón en este repo: `lastSupabaseSync = now`
arriba del `if` (branch `08-26`), `faultAlerted1 = true` arriba del envío (branch
`08-29`), y ahora `lastTelegramAlert = millis()` arriba del código de respuesta.
**El reloj avanza aunque la acción no ocurra.**

## Por qué esta tarea y no otra

1. **Jerarquía + rotación.** El turno anterior de esta misma noche fue galgas (P0
   octubre); frioseguro es PLATA, prioridad #1, y venía del `08-29`. **Datalogger sigue
   bloqueado**: su árbol quedó sucio y con un branch sin commits desde el 31-ago (ver
   abajo). Cosechador sigue esperando la compra. Frioseguro desempata solo.
2. **No estaba en ningún branch.** Repasé los 26 branches nocturnos abiertos de
   frioseguro: **ninguno toca `telegram.h`**. El `08-02` produjo el *modelo* y los
   hallazgos, no el fix — y lo dice explícitamente.
3. **Hay precedente exacto de esta jugada**: el branch `08-18-fix-alert-delay-defrost`
   tomó un hallazgo del modelo `07-18` y lo corrigió en firmware. Esto es lo mismo,
   sobre el otro modelo que quedó sin cobrar.
4. **Es el core de lo que se cobra.** El item #19 (`08-29`) hizo que el aviso de sonda
   caída *se genere*. Este hace que *salga*. Sin este, aquel manda su `sensor_fault` a
   Telegram por un caño que lo puede tirar.
5. **Software puro**, verificable sin banco hasta el último metro.

## Qué hice

`firmware_modular/telegram_gate.h` (nuevo) — header **puro**: sin Arduino, sin
HTTPClient, sin `String`. Enteros, flags y `char[]`. No es un espejo en otro lenguaje
(el riesgo que el propio `alert_model.py` señala): **es el mismo archivo que se
flashea**, y por eso se compila con `g++` en la PC y se testea sin hardware. Mismo
criterio que `sensor_fault_model.h` (`08-29`) y `offline_buffer.h` (`08-26`).

Una **ranura pendiente por fuente** (`TG_SRC_TEMP` / `DOOR` / `POWER` / `CURRENT`) y
un invariante: **un aviso pendiente no se descarta hasta que se entrega.** Sin
internet queda pendiente y se reintenta cada 60 s hasta que sale.

```c
if (g.pendingCritical[src]) return true;      // H2: lo critico no espera
if (!g.everDelivered[src])  return true;      // H1: nunca entrego -> no hay ventana
return tgElapsed(now, g.lastDeliveredMs[src]) >= minIntervalMs;
```

```c
if (result == TG_DELIVERED) { g.lastDeliveredMs[src] = now; ... }   // H3
```

**H4 desaparece de los call-sites sin tocar su semántica**: pueden seguir marcando
`alertSent = true`, porque la responsabilidad de la entrega quedó adentro del módulo.
`telegramRetryPending()` barre los pendientes desde `loop()`.

**Clasificación del código HTTP**, que es lo que hace que el reintento no sea una
trampa: 2xx entregado; **429 reintentar** (es el rate limit de la propia API de
Telegram, es temporal); **4xx descartar** (token inválido, chat bloqueado, Markdown
roto: reintentar no lo arregla, y sin esto taparía a su fuente para siempre); 5xx / 0 /
-1 reintentar. Un descarte **no** marca la fuente como entregada: el aviso siguiente no
paga los 5 minutos por culpa del que se perdió.

**Tres cosas más, que aparecieron al mirar de cerca:**

- **`StaticJsonDocument<512>` → `DynamicJsonDocument(len + 256)`.** Con el mensaje más
  largo (sobrecorriente + decorado) el documento estático desbordaba, salía JSON
  truncado y Telegram devolvía 400. Otro camino de pérdida silenciosa **dentro de la
  misma función**, que no se notaba justamente porque nadie miraba el código de
  respuesta.
- **`testTelegram()` devuelve el resultado real.** El botón "📲 Probar Telegram" del
  panel local devolvía `true` siempre: el instalador veía **"✅ Mensaje enviado"**
  aunque no hubiera salido nada. Es la herramienta con la que se valida una
  instalación en el comercio.
- **El decorado ya no adjunta la temperatura si `sensorData.valid == false`** (dice
  `sin dato (sonda)`). Con la sonda caída `tempAvg` conserva el último valor bueno;
  mandarlo como si fuera actual convierte al aviso en desinformación. Es la
  mitad-Telegram de la deuda anotada en el `08-29`; la otra mitad (lo que se publica en
  `readings`) sigue abierta porque toca el contrato con el panel y con la app.

## Cómo verificarlo (comandos exactos, sin hardware)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-09-01-b-el-aviso-que-no-sale

# 1. la maquina de entrega, sobre el header REAL
g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_telegram_gate.exe tools/test_telegram_gate.cpp
./tools/test_telegram_gate.exe
#    -> OK -- 66 checks, 0 fallas

# 2. el CABLEADO sobre firmware_modular/, + 9 mutantes del modulo
python tools/check_telegram_wiring.py --mutants
#    -> OK -- 92 checks, 0 fallas

# 3. la prueba de que el checker sirve: contra main tiene que REPROBAR
git worktree add /tmp/fs-main main
python tools/check_telegram_wiring.py --root /tmp/fs-main
#    -> FALLO -- 53 checks, 46 fallas
git worktree remove /tmp/fs-main

# 4. compilacion real (~4 min; el core esp32 3.3.8 ya estaba instalado)
arduino-cli compile --fqbn "esp32:esp32:esp32:PartitionScheme=min_spiffs" firmware_modular
#    -> exit 0
#    -> 1289020 bytes (65 %) de flash; 55376 bytes (16 %) de RAM; sin warnings
```

Los cuatro corrieron esta noche y dieron eso.

El punto 3 es el que le da valor al resto. Y los mutantes existen porque un test verde
sobre un módulo que no se puede romper tampoco prueba nada: desarmar H1, H2, H3 y H4 uno
por uno; tratar el 429 como definitivo; reintentar los 4xx para siempre; sacar el
truncado de `tgGateQueue`; un off-by-one en `tgSrcValid`; sacar el throttle de
reintento. Los nueve mueren.

> **El mutante de H2 sobrevivió en la primera pasada** y encontró un agujero real *del
> test*: mi caso de "lo crítico no espera" usaba una fuente que todavía no había
> entregado nada, así que pasaba por la regla de H1 y **el bypass crítico nunca se
> ejercitaba**. Se agregaron 4 checks con la fuente ya entregando. El test no lo
> encontré yo; lo encontró el mutante.

## Qué quedó SIN verificar (necesita banco)

Todo lo de arriba prueba la **decisión** y el **cableado**, no el **efecto**: nadie
verificó un POST real contra la API de Telegram por esta ruta.

1. **Reintento real**: disparar una alerta con el router apagado, confirmar por serie
   `queda PENDIENTE`, prender el router y confirmar que el mensaje **llega** — y una
   sola vez. Éste es el bug principal.
2. **H1 en el equipo**: resetear el nodo con la puerta ya abierta; el aviso tiene que
   salir a los 120 s (antes: silencio).
3. **H2 en el equipo**: aviso de puerta y temperatura crítica a los 60 s; tienen que
   **llegar los dos**.
4. **`TG_DROP`**: un `TELEGRAM_CHAT_IDS` inexistente tiene que producir un
   `Aviso DESCARTADO` por serie y **no** dejar la fuente trabada.
5. **Costo del `DynamicJsonDocument`** sobre el heap real con TLS abierto. El sketch
   está en 16 % de RAM, pero la fragmentación del heap de un ESP32 se mide, no se
   supone.

**Delta de flash contra `main`: verificación pendiente.** La compilación del branch dio
1 289 020 B / 55 376 B; la de `main` en un worktree limpio seguía corriendo cuando cerré
el turno (no hay caché en un worktree nuevo: son ~4 min más) y no la esperé, por la
disciplina de tiempo. Para medirla:
`cd /tmp/fs-main && arduino-cli compile --fqbn "esp32:esp32:esp32:PartitionScheme=min_spiffs" firmware_modular`.
Cota superior conocida: el gate agrega 4 × 384 B de buffers estáticos ≈ **1,5 kB de
RAM**, sobre 272 kB libres. No es un riesgo, pero está sin medir.

## Limitaciones declaradas (no son omisiones)

- **`power_monitor.h` y `current_sensor.h` no los incluye el `.ino`.** Son código
  muerto en el firmware que se flashea hoy — ambos lo dicen en su encabezado ("NO está
  integrado aún"). Los cableé igual, porque el cambio de firma de `sendTelegramAlert`
  los habría dejado rotos para el día que se integren, pero **su edición no pasó por el
  compilador**. De las cuatro fuentes de H2, **las vivas hoy son dos**: temperatura y
  puerta. Es un hallazgo colateral que vale la pena mirar de día: el upsell de relés
  (#15) y la alerta de corte de luz asumen módulos que no están compilados.
- **Corte y restauración de luz comparten fuente.** Un corte de menos de 5 min hace que
  la restauración espere el intervalo — pero ya **no se pierde**, y su texto cuenta la
  historia entera ("hubo corte, duró N minutos, ya volvió"). Está fijado como test.
- **El escapado de Markdown no se toca.** Un `g_device_name` con `_` o `*` produce un
  400. Antes se perdía en silencio; ahora se ve por serie y se cuenta en
  `droppedCount`. El fix toca el texto de todos los mensajes y merece su propia pasada.
- **Al mergear con el branch `08-02`**: sus `test_h*` van a **fallar a propósito** —
  fijan el comportamiento viejo, y el propio doc lo anticipa ("cuando @firmware aplique
  un fix, el test correspondiente falla, y ese fallo es la evidencia"). Hay que
  actualizar `tools/telegram_gate_model.py` o retirarlo en favor de
  `test_telegram_gate.cpp`, que testea el header real en vez de un espejo en Python.

**Cosecha a biblioteca:** `telegram_gate.h` es candidato (cualquier nodo que avise por
un canal poco confiable lo quiere), pero **no se cosecha todavía**: la regla del
`@bibliotecario` es que ningún módulo entra sin decir dónde se probó, y esto todavía no
vio un POST real.

## Hallazgo colateral — sigue igual que anoche

`C:\Proyectos\datalogger` **sigue con el árbol sucio** y el branch
`nocturno/local-2026-08-31-el-csv-que-no-avisa` **sin un solo commit y sin pushear**
(6 archivos modificados en `firmwares/pico2w-node/`, más `firmwares/nodo-gimap/`,
`tools/check_sd_integrity.py` y `tools/test_integridad_sd.py` sin trackear). Es lo
mismo que reportó el turno anterior. **No lo toqué** — no es mío decidir si eso se
commitea o se tira — pero **es lo que está bloqueando a datalogger dos noches
seguidas**. Vale un minuto de Matías: o se commitea en su branch, o se descarta.

`MATI-HQ` también sigue con cambios sin commitear de antes de esta sesión
(`comercial/TERMOVIGIA_PLAN_COMERCIAL.md` sin trackear y 4 bitácoras de dominios
modificadas); frioseguro tiene los suyos (`android-app/`, `frioseguro-android/`, y las
carpetas del revival de Santa Cruz). Tampoco los toqué: el commit de este branch stagea
**solo** los 13 archivos del trabajo de esta noche.

---

## Estado del branch

`nocturno/local-2026-09-01-b-el-aviso-que-no-sale` → `f13e2fe`, pusheado a `origin`.
`QUE_FALTA.md` de frioseguro actualizado (ítem **#20**). Documento largo:
`C:\Proyectos\frioseguro\docs\telegram-delivery.md`.
