# Nocturno local — 2026-08-19

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-19-guard-self-trigger` (pusheado, `d8ada58`).
**Sale de:** `nocturno/local-2026-08-17-b-eventos-alerta` (hay que mergear ese primero).

## TL;DR

**Cuarta noche seguida de implementación.** Esta vez la tarea la eligió el
informe de anteanoche: el branch del 08-17-b terminó diciendo qué le faltaba, y
lo dejó escrito en el `QUE_FALTA`:

> *«el fix del `HOLD_SEC` del self-trigger, porque hoy un dropout espurio también
> escribe un `alert_start`».*

Ese branch hizo que los emisores **escriban en `events`**. O sea: desde el 08-17,
cada falso positivo del self-trigger dejó de ser una línea de log y pasó a ser
una fila `alert_start`, **severity `critical`**, en el feed que Dreyfus mira.

**Cuántos falsos positivos había, medido sobre las capturas reales de campo: 6.
Ahora: 0.** La rotura genuina sigue disparando.

Y el hallazgo de la noche, que cambia cómo se cuenta este bug:

> **El hold no faltaba. Estaba desconectado.** `Thresholds.hold_sec` se
> inicializa en 1,5 s (`shared/types.h`), se persiste en NVS
> (`NVS_KEY_HOLD_SEC`), se puede cambiar en caliente por `CMD_SET_THRESHOLDS`
> (`command_handler.cpp:99`)… y **ninguna decisión lo leía**. El `.ino` hacía
> `Thresholds th; nvsLoadThresholds(th);` y no usaba `th` para nada.

No fue "se perdió una constante en la migración a v3". Fue una perilla que
sobrevivió entera —con su persistencia y su comando remoto— y quedó sin cable.

## Tarea elegida y por qué

Por rotación tocaba `galgas` (el último fue 08-17-b; después vinieron frioseguro
y datalogger). Descarté `cosechador` por la misma razón de las últimas tres
noches, que dejo dicha para no re-decidirla: es **P2**, todo su `QUE_FALTA` está
bloqueado por la compra, el repo no tiene una línea de código y ya acumula cuatro
análisis sobre el mismo material.

Dentro de galgas había un candidato obvio y uno mejor:

- El obvio era otra auditoría. `galgas` tiene **11 branches nocturnos sin
  mergear** y casi todos son análisis.
- El mejor era **el agujero que abrió mi propio branch de anteanoche**. Emitir
  eventos de alerta sin arreglar el disparador es exactamente la secuencia
  equivocada: primero le diste voz al detector, después te fijás si grita solo.

Elegí el segundo. La evidencia ya estaba juntada del 07-29 (hallazgo 2 de
`docs/vpp-field-characterization.md`), así que esta noche era escribir el código
y medirlo, no volver a investigar.

## El defecto

El self-trigger v3 decidía con esto:

```c
v_pp = v_max - v_min;                       // 500 muestras @ 500 Hz = 1,0 s
self_alert = (v_pp > SELF_TRIGGER_VPP_V);   // 40 mV, UN burst, sin persistencia
```

Dos agujeros:

1. **Sin guard de rango.** El campo tiene dropouts: muestras en `0.0 V`. Como
   `v_pp` es max−min, **una sola** muestra en 0.0 V da `v_pp ≈ 1,55 V` = **37×**
   el umbral. En la captura de *motor ON* —operación normal— eso hacía que el
   **2,96 % de las ventanas de 1 s** cruzaran el ALERT.
2. **Sin hold.** El legacy exigía 1,5 s de permanencia; el informe de ensayos
   §9.2 pide 2–3 s. El v3 disparaba con un burst de 1 s.

## Qué hice

### 1. Guard de dropout (`adc_sampler.cpp`, A y B)

Las muestras fuera de `(0.30, 3.20) V` no son medidas: son dropouts. Se excluyen
de **todos** los agregados, no sólo de `v_pp` — una muestra en 0.0 V también
ensucia `v_mean`, `v_rms` y `sigma`.

Si **no sobrevive ninguna** muestra se publica el burst crudo: ése es el caso de
una entrada suelta oscilando entre rieles, donde el crudo tiene 3,3 V de spread y
tiene que disparar.

`r.n_samples` **sigue siendo el total del burst**, no el de válidas: es una
columna de `readings` y no le cambio el significado por atrás. Cuántas se
descartaron va en `metadata.adc_dropped`.

### 2. Hold (`esp_a_emisor.ino` / `esp_b_emisor.ino`)

El primer burst produce un **candidato**; se confirma con un **segundo burst de
`th.hold_sec` segundos, en el MISMO wake**.

La decisión que más conviene revisar es ésa: **la confirmación no es "dos wakes
consecutivos"**. Exigir dos wakes habría costado **un período entero** —600 s en
NORMAL— de latencia frente a una rotura real. Así cuesta 1,5 s de vigilia extra y
**sólo cuando hay candidato**, despreciable contra los segundos de WiFi+TLS de
cada wake. El ADC es ADC1 (GPIO34), que sigue disponible con la WiFi levantada.

Fail-open: si la confirmación no se puede hacer (burst incompleto, cero
muestras), se **acepta** el candidato. No poder confirmar es un problema del
sampler, y en una vía de seguridad la duda se resuelve avisando.

### 3. Trazabilidad en `metadata` de `readings`

`adc_dropped`, `adc_guard`, `adc_suspect`, y —cuando hubo candidato— `hold_s` +
`vpp_confirm`. Sin esto el guard sería invisible y **un front-end degradándose
pasaría por reposo prolijo**.

### 4. `tools/check_self_trigger.py` — el oráculo

Reproduce las **dos** decisiones (la vieja y la nueva) sobre las 12 capturas
Dreyfus reales y cuenta cuántas veces dispararía cada una. Las constantes no
están escritas en el script: **las lee de `config.h`**, y además falla si A y B
divergieron. Las capturas se abren read-only.

### 5. `tools/test_check_self_trigger.py` — 23 tests

Guard, hold, lectura de constantes del firmware, y tres tests `[CAMPO]` que fijan
el resultado sobre las capturas reales para que el arreglo no se pierda en un
merge.

## Lo que apareció al medir (y corrigió el diseño)

Vale la pena contarlo porque es el tipo de cosa que sólo aparece midiendo.

Mi primera versión del guard tenía una regla de más: *"si se descarta más del
25 % del burst, publicar crudo, porque eso es la señal yéndose a un riel y hay
que alertarlo"*. Sonaba bien. Con esa regla quedaban **3 alertas espurias**.

Fui a ver cuáles eran:

- Los 3 casos eran bloques de **190 a 405 muestras seguidas en exactamente
  0.0 V** — entre el 40 y el 80 % del burst.
- **El mismo artefacto aparece igual en la captura de la rotura real y en una de
  operación normal.** O sea: **no distingue nada**. Es una caída del pipeline de
  logging, no una señal.
- Y la rotura genuina se detecta por otro lado completamente: **5 ventanas sin un
  solo dropout, con `v_pp = 0,42 V`** — 10× el umbral.

Saqué la regla. El caso que la justificaba (señal entera en un riel) ya lo cubría
el camino de "no queda ninguna muestra válida". **Menos código y mejor
resultado** — la regla que agregué "por las dudas" era la que fabricaba las 3
alertas que quedaban.

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-19-guard-self-trigger

# 23 tests (~1 s, sin red ni hardware)
python tools\test_check_self_trigger.py

# la tabla sobre las capturas reales + veredicto (exit 0)
python tools\check_self_trigger.py
python tools\check_self_trigger.py --hold-sec 0    # cuánto aporta cada guarda

arduino-cli compile --fqbn esp32:esp32:esp32 firmware\esp_a_emisor
arduino-cli compile --fqbn esp32:esp32:esp32 firmware\esp_b_emisor
```

**Lo que verifiqué yo, corriendo:**

- **Alertas espurias en operación normal: 6 → 0.** La rotura real (CADENA B ROTA)
  sigue disparando en **5 ventanas**. Exit code 0.
- **23/23 tests OK.**
- **Mutación** — que los tests sean red y no decorado:

  | mutación | resultado |
  |---|---|
  | sacar el guard (no filtrar nunca) | **4 tests fallan** |
  | apagar el hold (confirmar siempre) | **1 test falla** |
  | guard que tape también el riel total | **1 test falla** |

  Restaurado → 23/23 OK. La tercera mutación **sobrevivió en el primer intento**:
  el test que la tenía que matar afirmaba algo que era verdad por accidente. Lo
  reescribí (y de paso me corrigió una creencia mía equivocada, abajo).
- **Compilan A y B** (esp32 core 3.3.8). Costo: **+1712 B de flash, +8 B de RAM**.

## Lo que quedó sin verificar (necesita banco / campo)

1. **Que el ADC v3 real produzca el mismo tipo de dropout.** Todo lo medido sale
   de capturas del pipeline **legacy**, donde el 0.0 V puede venir de la
   telemetría. El v3 muestrea local por ISR: hay que ver su patrón de dropout en
   banco, y si es distinto, revisar el rango `(0.30, 3.20) V`.
2. **El rango del guard contra el acondicionamiento real** (INA333 + offset). Hoy
   sale de la base ~1,55 V de las capturas.
3. **Disparar una alerta real y contar las filas de `events`** — que el hold no
   haya roto la emisión del 08-17. Con `DEV_SIM_PERIOD_S 1` los dos bursts cruzan
   el umbral y el camino completo se ejercita en banco. Es de @tester, 10 min.
4. **El costo de batería del burst de confirmación** (@energia). Estimado
   despreciable; **no medido**.

## Dos cosas que encontré y NO arreglé (a propósito)

1. **Un riel plano es invisible para el detector.** Si la señal se va entera a
   masa y se queda quieta, `v_pp = max−min = 0` y **no dispara — ni la versión
   vieja ni la nueva**, porque el detector es pico-a-pico. No es una regresión de
   este branch: es el detector. Lo único que hoy delata el caso es
   `adc_dropped`/`adc_suspect`. El que faltaría es un detector sobre **`v_mean`
   fuera de banda**, y eso es una decisión de umbral de @muestreador, no un bug
   que se arregle de noche. Queda fijado con test.

   (Esto me corrigió: cuando diseñé el guard di por sentado que el camino de "no
   quedan muestras válidas" cubría el riel total. Cubre el riel *ruidoso*. El
   riel *plano* no lo veía nadie, ni antes.)

2. **Flash al 94 %.** 1.240.048 de 1.310.720 B; quedan **70.672 B**. No es de este
   branch —la base ya estaba en 94 %— pero **hay que mirarlo antes de octubre**: a
   este ritmo el binario deja de entrar, y la OTA es la vía de actualización en
   planta. Es un ítem para el `QUE_FALTA`, no para esta noche.

## Lo que este branch NO toca

- **No toca `data/field_captures/`** (sagrado, read-only — el oráculo sólo lee).
- **No toca el umbral de 40 mV**, ni `TH_VPP_MONITOR` del SCADA, ni el RX, ni el
  backend, ni el schema. El fix del `mapTag()` y el de los eventos son del branch
  del que éste sale.
- **No agrega ningún tipo de evento nuevo.** Escalar "burst sospechoso" a un
  evento de falla necesita decidir vocabulario y tocar el CHECK del schema: es
  una decisión, no una implementación.
- **No toqué nada del provisioning, OTA ni deep sleep.**

## Nota para el Director

Anoche escribí que dos auditorías habían encontrado el mismo defecto sin
enterarse una de la otra. Esta noche pasó lo opuesto y conviene anotarlo como
señal de que algo empezó a funcionar: **el branch del 08-17-b dejó escrito
exactamente qué le faltaba, y ese renglón fue el que eligió la tarea de hoy.** No
hubo que buscar: había un pendiente nombrado, con su evidencia ya medida del
07-29. La cadena 07-29 (medir) → 08-17-b (implementar) → 08-19 (cerrar el agujero
que abrió) es la primera vez que tres noches se encadenan a propósito.

Lo que no cambió: **`galgas` tiene ahora 12 branches nocturnos sin mergear**, y
éste depende del 08-17-b, que depende de nada pero espera desde hace dos días.
`datalogger` tiene 20, `frioseguro` 13.

**Próximo paso concreto:** mergear `08-17-b-eventos-alerta` y después éste — en
ese orden, porque el segundo arregla el disparador del primero. Si se mergea sólo
el 08-17-b, quedan emitiéndose `alert_start` críticos con el detector que grita
solo, que es el peor de los tres estados posibles.

---

**Higiene del cuartel:** MATI-HQ seguía con los mismos 16 modificados + 4 sin
trackear de los informes anteriores. **No los toqué ni los commiteé**: es trabajo
tuyo en curso. Este commit sólo agrega este informe y la entrada del `QUE_FALTA`.
En `galgas` no había nada sin trackear antes de empezar; el commit del branch
lista los 11 archivos uno por uno.
