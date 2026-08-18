# Nocturno local — 2026-08-18

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la jerarquía).
**Branch:** `nocturno/local-2026-08-18-fix-alert-delay-defrost` (pusheado, `0ae4b27`).
**Sale de:** `nocturno/local-2026-07-18-alert-model` (hay que mergear ese primero).

## TL;DR

**Segunda noche seguida de implementación, no de auditoría.** El branch del
07-18 dejó escrito, con test que lo demostraba, un hallazgo que nadie cerró.
Esta noche lo cerré — y al escribirlo apareció que el hallazgo se quedaba corto.

El hallazgo de julio decía: *el acumulador no se reinicia al entrar en defrost.*
La causa real es más general:

> **`highTempSec` no medía tiempo observado por encima del crítico. Medía tiempo
> de reloj entre dos evaluaciones.** Cualquier hueco en la evaluación se le
> cobraba entero al contador que dispara la alerta.

Y hay **tres puertas** que abren ese hueco, no una. Las tres hacen `return`
temprano sin actualizar `lastAlertCheck`:

| puerta | qué la abre |
|---|---|
| `if (state.defrostMode)` | descongelamiento |
| `if (state.cooldownMode)` | espera post-descongelamiento |
| `if (!sensorData.valid)` | **sonda caída** — ésta no estaba en el hallazgo original |

**Con los defaults de producción el salto es total, no marginal.** El hallazgo de
julio lo llamó *«latente»*. No lo es:

- `defrostCooldownSec = 1800` (`storage.h:26`)
- `DEFAULT_ALERT_DELAY_SEC = 300` (`config.h:152`)

Al salir del cooldown entraban **1800 segundos de golpe** en un contador cuyo
umbral son 300. **Alerta en el primer tick, en cada ciclo de descongelamiento.**
Un freezer comercial descongela varias veces por día. El comerciante que paga el
abono recibía una alerta falsa por ciclo — sobre exactamente lo que se le cobra
(*«el servicio avisa»*, `PLATA.md`). Eso no es molestia: es churn.

Y había un segundo síntoma que hacía el bug invisible desde afuera: las ramas de
suspensión ponían a 0 `state.highTempElapsedSec` —**el espejo que ve el
dashboard**— pero no el acumulador real. **La pantalla mostraba 0 mientras el
firmware guardaba 1800.**

## Tarea elegida y por qué

Por rotación tocaba **cosechador** (los cinco turnos previos: frioseguro 08-16-b,
datalogger 08-17, galgas 08-17-b — el más viejo era cosechador, 08-16). **Lo
descarté a propósito y lo dejo dicho:**

- Cosechador es **P2** y todo su `QUE_FALTA` está bloqueado por la compra.
- El repo **no tiene una línea de código**: son 4 docs y 2 PDFs.
- Ya acumula **cuatro análisis** (07-18 energía, 08-11-b standby, 08-14 alarma,
  08-16 medición). Un quinto análisis sobre el mismo material sería cantidad, no
  calidad — que es justamente lo que la consigna prohíbe.

Fui a **FrioSeguro**, que es **PLATA = prioridad #1**, y adentro busqué lo que el
nocturno del 08-17-b dejó como diagnóstico del sistema entero:

> *«La deuda ya no es de diagnóstico.»*

FrioSeguro tiene **13 branches sin mergear**. El ítem 18 del `QUE_FALTA` —
*«cerrar hallazgo de la decisión de alerta (el core que se cobra)»* — tenía el
diagnóstico hecho, el oráculo escrito, el test que lo demuestra, y el fix
candidato descrito en dos líneas. **Le faltaba que alguien lo escribiera.**

Una aclaración honesta: el branch de julio escribió *«fix candidato (2 líneas, en
banco)»* y *«no lo toqué porque modificar firmware de producción sin banco es lo
que la doctrina prohíbe»*. **Revisé esa decisión y la cambié**, con este
criterio: lo que la doctrina prohíbe es *declarar hecho sin evidencia*, no
escribir código. Este fix es **lógica pura, sin hardware en el lazo**, y es
verificable de tres maneras sin tocar una placa (oráculo, compilación, mutación).
Lo que sí necesita banco —confirmar que un ciclo real de descongelamiento ya no
alerta— **queda marcado como pendiente y no lo declaro hecho**.

## Qué hice

### `firmware_modular/alerts.h` — el fix (+20 bytes de flash)

**Dos reglas distintas, porque los dos huecos significan cosas distintas.** Esto
es lo único de diseño que hay acá y es lo que conviene revisar:

**1. Suspensión deliberada** (defrost, cooldown) → **el episodio termina.**

```c
state.tempOverCritical = false;
state.highTempElapsedSec = 0;
highTempSec = 0;     // el acumulador REAL, no solo su espejo en state
lastAlertCheck = 0;  // re-ancla el reloj: el 1er tick post-suspensión no acumula
return;
```

`lastAlertCheck = 0` no es un valor mágico: es **el mismo centinela «no hay
muestra previa» que el código ya usaba** al arrancar (`if (lastAlertCheck > 0)`).
Al salir de la suspensión, el `alert_delay_sec` se exige **entero de nuevo** —
que es lo que el cliente configuró para tolerar los picos post-defrost.

**2. Pérdida accidental de muestras** (sonda inválida, loop bloqueado por
HTTPS/OTA, WiFi reconectando) → **se descarta el hueco, no el episodio.**

```c
unsigned long deltaMs = now - lastAlertCheck;  // unsigned: sobrevive el rollover de millis()
if (deltaMs <= ALERT_MAX_SAMPLE_GAP_MS) {
  highTempSec += deltaMs / 1000;
}
```

Un parpadeo de la sonda **no tiene por qué regalarle 300 s de gracia a una cámara
que se está calentando**. Por eso acá no se reinicia el conteo, sólo no se cobra
el hueco. Es la diferencia deliberada con el caso 1, y hay un test para cada lado.

`ALERT_MAX_SAMPLE_GAP_MS = 15000` no es un número inventado: `checkAlerts()`
corre cada **1000 ms** y las sondas se leen cada `INTERVAL_SENSOR_READ_MS =
2000` (`config.h:159`). **15 s son 7,5× el productor más lento** — hay un test
que verifica esa relación para que nadie baje el tope sin darse cuenta.

### `tools/alert_model.py` — el oráculo, actualizado en el mismo commit

Es un espejo 1:1 del firmware; si el firmware cambia y el modelo no, el oráculo
miente. Le agregué además un **historial de fidelidad** (qué versión del firmware
espeja y desde cuándo), porque este módulo ya cambió de significado una vez.

Re-anclé también las **17 citas `alerts.h:NN`** de los tres archivos, que el fix
había desplazado. Cada una apunta hoy a la línea que dice.

### `tools/test_alert_model.py` — 12 → 20 tests

Los dos tests que **pinneaban el bug como conducta** (`[CARACTERIZACION]`) ahora
pinnean el arreglo (`[REGRESION-H1]`). Los nuevos:

| test | qué fija |
|---|---|
| `test_post_defrost_no_alerta_al_instante` | el caso exacto del hallazgo, invertido |
| `test_post_defrost_exige_el_delay_completo_de_nuevo` | a los 290 s no, a los 300 s sí |
| `test_defrost_reinicia_el_acumulador_real_no_solo_el_espejo` | la divergencia espejo/real |
| `test_cooldown_tambien_reancla` | la segunda puerta |
| `test_escenario_produccion_defrost_mas_cooldown_de_30_min` | **defaults reales**, tick de 1 s, 2500 ticks |
| `test_sonda_caida_10_min_no_dispara_al_volver` | la tercera puerta |
| `test_el_hueco_no_borra_el_episodio_en_curso` | que el caso 2 no se pase de generoso |
| `test_borde_exacto_del_hueco_maximo` | `== MAX` acumula, `MAX+1` descarta |
| `test_la_cadencia_normal_del_firmware_no_se_descarta` | que el tope no rompa la operación normal |

### `docs/alert-model.md` y `QUE_FALTA.md`

H1 documentado como cerrado, con las tres puertas, el porqué de las dos reglas y
el costo medido. **El hallazgo original de julio queda textual**, marcado como
histórico, para que se pueda auditar el camino del hallazgo al fix.

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-18-fix-alert-delay-defrost

# los 20 tests (< 1 s, sin red ni hardware)
python -m unittest tools.test_alert_model

# el firmware compila
arduino-cli compile --fqbn esp32:esp32:esp32 firmware_modular
```

**Lo que verifiqué yo, corriendo:**

- **20/20 tests OK** (eran 12) + `py_compile` de los dos archivos.
- **`arduino-cli compile` OK.** Costo medido contra el baseline compilado antes
  de tocar nada: **+20 bytes de flash** (1288696 → 1288716) y **0 bytes de RAM**.
- **Mutación** — que los tests sirvan de red, no de decorado: revertí cada mitad
  del fix en el oráculo y corrí la suite.
  - Revertir el reset de las suspensiones → **3 tests fallan**.
  - Revertir el clamp del hueco → **3 tests fallan**.
  - Restaurado → 20/20 OK.
- Las 17 citas `alerts.h:NN` re-ancladas y comprobadas contra el archivo nuevo.

## Qué quedó sin verificar por hardware

1. **Que un ciclo real de descongelamiento ya no genere la alerta falsa.** Es el
   punto entero. Se cierra flasheando una placa WiFi y forzando defrost
   (`serial_api.h` ya tiene el comando, y `web_api.h:221` lo togglea desde la
   página local). Esperar el cooldown y confirmar que **no** sale nada.
2. **Que una alerta legítima post-defrost sí salga**, a los `alert_delay_sec` de
   terminado el cooldown. Sin esta mitad, el fix podría haber roto la alerta en
   vez de arreglarla — el oráculo dice que no, el hardware lo confirma.
3. **La tercera puerta en la vida real**: desconectar la DS18B20 en caliente y ver
   que al reconectarla no dispara.

Nada de esto necesita nube ni cliente: es una placa, una sonda y el monitor serie.

## Lo que este branch NO hace (a propósito)

- **No toca el umbral, ni `alert_delay_sec`, ni ninguna config.** El fix no
  cambia *cuándo debería* alertar el sistema; hace que alerte cuando dice que
  alerta.
- **No arregla la truncación.** `highTempSec += deltaMs / 1000` pierde el resto
  en cada tick: con la cadencia real (~1010 ms) son ~10 ms por tick, ~3 s sobre
  un delay de 300 (~1 %). Va en la dirección **segura** (alerta tarde, no
  temprano) y arreglarlo bien pide acumular en ms. **Queda escrito como deuda en
  el doc, no mezclado con este commit.**
- **No toca el resto del firmware**, ni el dashboard, ni Supabase, ni nada de
  los otros 12 branches.

## Nota para el Director

Dos cosas que no son de esta tarea pero se ven desde acá:

**1. `firmware_modular` compila al 98 % de la partición por defecto**
(1288716 / 1310720 B). No es de este branch —ya estaba— pero **quedan ~22 kB**.
La próxima feature de firmware que alguien agregue no entra, y el error de
compilación va a aparecer en un momento peor que ahora. Es cambiar el
`PartitionScheme` a `min_spiffs` (galgas ya lo usa) o empezar a podar. Vale
anotarlo antes de que sea urgente.

**2. FrioSeguro tiene 13 branches nocturnos sin mergear** y es el proyecto de
**PLATA**. Dos de ellos —`07-11-b-resumen-mensual` y su continuación
`07-13-resumen-mensual-fixes`— ya pasaron por @verificador con veredicto
**MERGE-CON-FIXES** y los fixes están aplicados: **están listos y esperando**. La
cadena de esta noche es igual: `07-18-alert-model` → `08-18-fix-alert-delay-defrost`.

El patrón se repite en los cuatro repos y ya lo dijo el informe del 08-17-b: el
cuello de botella dejó de ser encontrar cosas. **Una sesión de día pasando
branches por @verificador y mergeando vale más, hoy, que otra noche de análisis.**

**Próximo paso concreto:** mergear `07-18-alert-model` y después éste; flashear
una placa WiFi y forzar un ciclo de defrost. Es media hora de banco y cierra el
ítem 18 del `QUE_FALTA` — el core que se cobra.

---

**Higiene del cuartel:** MATI-HQ seguía con cambios sin commitear al arrancar la
noche (los mismos 16 modificados + 4 sin trackear del informe anterior). **No los
toqué ni los commiteé**: son trabajo tuyo en curso. Este commit sólo agrega este
informe. En `frioseguro` tampoco toqué lo que está sin trackear
(`REVIVAL_2026-08.md`, `firmware_revival/`, `kit_santacruz/`,
`FRIOSEGURO_SANTACRUZ_KIT.zip`) — el commit lista los 5 archivos uno por uno.
