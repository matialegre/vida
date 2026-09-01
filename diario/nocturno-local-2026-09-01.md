# Nocturno local — 2026-09-01

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (**P0** — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-09-01-el-rescate-desarmado` (pusheado, `567aeef`).
**Sale de:** `main` (`e9cd4bc`). **No depende de ningún otro branch nocturno.**
Toca `firmware/shared/supabase_client.cpp` (3 líneas, adiciones) y `esp_rx_receptor.ino`,
que también toca `08-11-cadena-entrega` — pero ése vive en la lógica de gateway/forward
y éste en el bloque de rescate y el `setup()`. Se mergean en cualquier orden.

---

## TL;DR

> **El rollback post-OTA estaba escrito, comentado, llamado desde `setup()`… y la
> bandera que lo enciende no la prendía nadie.**

`esp_rx_receptor.ino` tenía la máquina completa:

```c
RTC_DATA_ATTR bool     ota_pending_verify = false;   // se declara
static void checkOtaRollback(esp_reset_reason_t rr) {
  if (!ota_pending_verify) return;                   // se chequea
  ...
  ota_pending_verify = false;                        // se limpia
}
```

Se declara, se chequea, se limpia. **`grep -rn "ota_pending_verify" firmware/shared/`
devolvía cero líneas.** Y arriba de `doOtaCheck()` había un comentario que explicaba
por qué no estaba ahí:

```c
// ota_pending_verify lo maneja supabase_client.cpp internamente (no lo seteamos
// aca para evitar el bug del 3.5.3 ...)
```

La mitad de arriba era cierta —el bug 3.5.3 existió y el razonamiento es correcto—;
la mitad de abajo describía un cableado que nunca se hizo. Se movió la descarga al
módulo compartido, se movió el comentario, y **el armado se quedó en el camino**.

Estado real de las tres familias:

| Firmware | Máquina de rollback | ¿Se arma? |
|---|---|---|
| `ota_wm_pp` (monolítico, legacy) | completa | **sí** — línea 1275, después de `Update.end(true)` |
| `esp_rx_receptor` | completa, copiada | **no** |
| `esp_a_emisor` | no existe | — |
| `esp_b_emisor` | no existe | — |

Las tres modulares —**las que se flashean para octubre**— flasheaban OTA sin red.
Un bin que no arranca se recupera con cable USB sobre una caja atornillada a un
REDLER en marcha.

Es el mismo patrón que el `08-28` de anteanoche ("la calibración se escribía en NVS
y no la leía nadie"): **drift entre la familia monolítica y la modular, donde lo que
se perdió no fue el código sino el cable.**

## Por qué esta tarea y no otra

1. **Rotación + jerarquía.** El `08-29` fue frioseguro; el `08-28` galgas y el
   `08-28-b` datalogger. Anoche y anteanoche (30 y 31 de agosto) **no hubo informe
   nocturno** — ver "hallazgo colateral" abajo. Entre los repos desbloqueados, galgas
   es P0 con fecha inamovible.
2. **No estaba en ningún branch.** Repasé los 30 branches nocturnos abiertos de
   galgas. Los de OTA (`07-20-b-ota-decision-model`, `07-31-ota-versioning-tests`,
   `08-05-b`/`08-06-identidad-ota`) cubren **qué bin se elige y cómo se etiqueta**.
   Ninguno toca **qué pasa después de flashearlo**.
3. **Es la regla que Matías dejó escrita**: *OTA nunca ladrillo — ningún nodo puede
   perderse por una reprogramación fallida.* Estaba declarada y no implementada en la
   familia de octubre.
4. **Habilita los otros ítems del OTA.** El `#5` (OTA que distinga A/B) empuja
   binarios distintos a dos equipos en planta. Sin rollback, un push mal targeteado
   no tiene vuelta atrás remota.
5. **Es software puro**, verificable sin banco hasta el último tramo.

Descarté el `#6` (bucket `firmware` público → URL firmada): toca el camino de
descarga de **siete** familias de firmware a la vez, y meter mano ahí a ciegas, sin
banco y sin red de rollback, es exactamente lo contrario de lo que pide esa regla.
Con el rescate mergeado y probado, ese ítem se vuelve mucho más barato de hacer.

## Qué hice

`firmware/shared/ota_rescue.h` (nuevo, header-only sobre NVS) + el cableado:

1. **Armado, una sola línea, en el downloader compartido.** `supabaseDownloadFirmware()`
   llama `otaRescueArm()` **después** de `Update.end(true)` OK y **antes** del
   `ESP.restart()`. Como es el módulo compartido, **cubre RX + A + B de una**.
   Nunca antes de la descarga: eso era el bug 3.5.3 (un crash bajando el `.bin`
   mandaría a rollback al bin viejo, que es el que anda).
2. **Verificación al bootear**, en los tres `setup()`, antes de la radio y del ADC.
   Crash (`PANIC`/`INT_WDT`/`TASK_WDT`/`WDT`/`BROWNOUT`) con verificación pendiente →
   rollback. Tres boots sin crash → confirmado. Con período NORMAL, la ventana dura
   ~20 min.
3. **El RX pierde su copia muerta** y su `config.h` deja de definir la cuota por su
   cuenta (una sola fuente: `OTA_RESCUE_VERIFY_BOOTS`).
4. **Telemetría**: los emisores publican `metadata.ota_rescue` (`verifying` /
   `confirmed` / `aborted`) en `readings` mientras dura. Un equipo en verificación
   todavía puede volver atrás y quien mira el dashboard tiene que saberlo.

**Dos cosas se hicieron distinto del original monolítico**, y las dos son defectos
reales del original:

- **El estado pasa de RTC memory a NVS.** La RTC memory se pierde con el corte de
  energía… que es justo lo que provoca un bin malo que dispara brownout: el equipo se
  apaga, la bandera se borra sola y el rescate nunca corre. **La red desaparecía
  precisamente en el caso para el que existía.** Y el layout de `.rtc.data` lo decide
  el linker de cada bin — y el bin que lee la bandera no es el que la escribió, que es
  literalmente el punto del OTA.
- **Se chequea el retorno de `esp_ota_set_boot_partition()`.** El original lo ignoraba.
  Si el otro slot está vacío (equipo flasheado por cable una sola vez), apuntar el
  arranque ahí convierte un equipo que anda en uno que no arranca: **el rescate
  fabricando el ladrillo que vino a evitar.** Ahora, si no valida, no reinicia:
  aborta, limpia y sigue con el bin actual.

## Cómo verificarlo (comandos exactos, sin hardware)

```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-09-01-el-rescate-desarmado

# 1. la máquina de decisión, sobre el header REAL (shims de host en tools/fakes/)
g++ -std=c++17 -I tools/fakes -o tools/test_ota_rescue.exe tools/test_ota_rescue.cpp
./tools/test_ota_rescue.exe
#    -> OK -- 62 checks, 0 fallas

# 2. el CABLEADO sobre firmware/, + 9 mutantes del módulo
python tools/check_ota_rescue_wiring.py --mutants
#    -> 50 checks, 0 fallas; los 9 mutantes mueren

# 3. la prueba de que el checker sirve: contra main tiene que REPROBAR
git worktree add /tmp/galgas-main main
python tools/check_ota_rescue_wiring.py --root /tmp/galgas-main
#    -> 27 fallas, rc=1
git worktree remove /tmp/galgas-main

# 4. compilación real de las tres familias
arduino-cli compile --fqbn esp32:esp32:esp32 firmware/esp_a_emisor
arduino-cli compile --fqbn esp32:esp32:esp32 firmware/esp_b_emisor
arduino-cli compile --fqbn esp32:esp32:esp32 firmware/esp_rx_receptor
```

Los cuatro corrieron esta noche y dieron eso. Costo en flash, medido contra `main`
con el mismo core (esp32 3.3.8) — importa porque el sketch está al 94 % y eso ya es
el ítem #9b del `QUE_FALTA`:

| Sketch | main | branch | delta | margen que queda |
|---|---|---|---|---|
| `esp_a_emisor` / `esp_b_emisor` | 1 235 360 B | 1 236 988 B | **+1 628 B** | 73 732 B |
| `esp_rx_receptor` | 1 234 676 B | 1 235 828 B | **+1 152 B** | 74 892 B |

RAM global sin cambios en las tres.

El punto 3 es el que le da valor al resto: un checker que no reprueba el bug que dice
cazar no vale nada. Y los mutantes (no armar nunca, que el panic no cuente como crash,
confirmar al primer boot, reiniciar sin validar el otro slot, …) existen porque un test
verde sobre un módulo que no se puede romper tampoco prueba nada.

## Qué quedó SIN verificar (necesita banco)

1. **Que el rollback ocurra de verdad.** Todo lo de arriba prueba la *decisión*, no el
   *efecto*: nadie verificó todavía que `esp_ota_set_boot_partition()` mueva el arranque
   de un ESP32 real. Procedimiento: flashear un bin que panica a propósito en `setup()`
   (después del `otaRescueCheckOnBoot()`), subirlo como versión nueva, y mirar por serie
   `[RESCUE] el bin en verificacion crasheo` y el equipo volviendo solo.
2. **Confirmación real**: un OTA normal, tres wakes, `[RESCUE] bin nuevo CONFIRMADO`,
   con `metadata.ota_rescue` pasando por `verifying` en `readings`.
3. **Slot vacío**: equipo recién flasheado por cable, forzar crash con verificación
   pendiente, confirmar que dice `ABORTADO` y **no** reinicia.
4. **`factory_reset`** con una verificación en curso.

## Lo que este branch NO cierra (a propósito)

**La otra mitad de Task 09: el watchdog.** Un bin que se **cuelga** sin resetear no
genera ningún `reset_reason`, así que el rollback no lo ve: el equipo queda colgado con
la verificación pendiente. No lo hice esta noche por una razón concreta, no por falta de
tiempo: la API de `esp_task_wdt` cambió entre arduino-esp32 2.x y 3.x, y el timeout tiene
que ser más largo que un wake **con OTA adentro** (~110 s en el peor caso: 3 intentos de
30 s). Elegir mal ese número **reinicia nodos sanos a mitad de una descarga** — o sea,
convierte la red de seguridad en la falla. Eso se elige en banco, con un cronómetro.
Queda anotado en `QUE_FALTA` #1 y en `docs/ota-rescue.md` §4.

**Cosecha a biblioteca:** `ota_rescue.h` es candidato claro (es genérico a cualquier
ESP32 con OTA — FrioSeguro lo querría igual), pero **no se cosecha todavía**: la regla
del `@bibliotecario` es que ningún módulo entra sin decir dónde se probó, y esto todavía
no vio un rollback real. Cuando pase el punto 1 del banco, va.

## Hallazgo colateral — dos cosas que Matías debería mirar

1. **`C:\Proyectos\datalogger` quedó con el árbol sucio y un branch sin commits.**
   Existe `nocturno/local-2026-08-31-el-csv-que-no-avisa` (local, **sin pushear**),
   está checkouteado, su `git log` no tiene nada arriba de `b8df100`, y hay cambios sin
   commitear en 6 archivos (`misiones/*.py`, `nodo.py`, `registro.py`,
   `tools/test_misiones.py`) más `firmwares/nodo-gimap/`, `tools/check_sd_integrity.py`
   y `tools/test_integridad_sd.py` sin trackear. Parece un nocturno del 31-ago
   **abortado a mitad**: no hay informe en `diario/` ni del 30 ni del 31.
   **No lo toqué** — es trabajo de alguien y no es mío decidir si se commitea o se tira.
   Por eso además trabajé en galgas y no en datalogger: para no pisarlo.
2. **`MATI-HQ` viene con cambios sin commitear desde antes de esta sesión**: `PLATA.md`,
   4 bitácoras de dominios, y los 4 archivos de `cv suegro/` **borrados** pero sin
   commitear el borrado. Tampoco los toqué. Si el borrado de `cv suegro/` fue a
   propósito, hay que commitearlo; si no, `git checkout -- "cv suegro/"` los devuelve.

---

## Estado del branch

`nocturno/local-2026-09-01-el-rescate-desarmado` → `567aeef`, pusheado a
`origin`. `QUE_FALTA.md` de galgas actualizado (#1 y #5). Los README de A y B dejaron
de decir que Task 09 está entero pendiente. Documento largo:
`C:\Proyectos\galgas\docs\ota-rescue.md`.
