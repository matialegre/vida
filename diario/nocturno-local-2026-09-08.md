# Nocturno local — 2026-09-08

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA — prioridad #1 de la
jerarquía**), zona `firmware_modular/` + `tools/` + `docs/`.
**Branch:** `nocturno/local-2026-09-08-el-compresor-que-no-se-cuenta`
(pusheado, `0d8a6be`).
**Sale de `main` (`2ac3a7d`) limpio**, sin ningún otro branch mergeado adentro.
**No toca** `alerts.h`, `sensors.h`, `door_sensors.h`, `power_monitor.h`,
`supabase.h`, el panel, el servidor, SQL ni `hardware/`.

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_frio_0908`, ya
eliminado) porque el árbol de `frioseguro` tiene el KiCad de Matías sin
commitear (TermoVigía Mini/Lite) y un `checkout` lo habría tocado. **Verificado
al terminar: el árbol quedó idéntico**, en el branch `09-04-b` donde estaba, con
los mismos 9 archivos modificados/sin trackear.

---

## TL;DR

> **El canal que mide el compresor nunca compiló, y sus dos números centrales
> eran imposibles.** `current_sensor.h` tenía 255 líneas de lógica completa que
> el `.ino` no incluía. Adentro: una **alerta de sobrecorriente en 20 A sobre
> una cadena que satura en 5,2 A** —inalcanzable por aritmética, no por
> calibración— y un **horómetro que sumaba `runMinutes / 60.0` a un
> `unsigned long`**, o sea que **contaba 0 horas para cualquier ciclo de menos
> de una hora**: todos. El mantenimiento preventivo que se vende medía cero, y
> la alerta que se vende no podía dispararse.

## Por qué esta tarea

1. **La dejó marcada el turno anterior.** El informe del 09-07-b dice textual:
   *"`current_sensor.h` (255 líneas) tampoco lo incluye el `.ino` … Si tiene un
   fantasma como éste, no se va a saber hasta que alguien lo incluya. Candidato
   para una próxima noche."* Lo tenía.
2. **Es PLATA, la prioridad #1**, y está cotizado: `PLAN_TERMOVIGIA_3.md` lista
   *"consumo del compresor + predictivo **$8k/mes** por local"* como upsell sobre
   hardware que el equipo ya tiene.
3. **El plan ya había escrito qué hacer.** `PLAN_V3.1_TERMOVIGIA.md` línea 52 lo
   marca **HUÉRFANO** con el diagnóstico exacto (*"matemática de ACS712 con
   offset 2,5 V; redefine `PIN_CURRENT_SENSOR 36` contra el 32 de `config.h`"*)
   y pide la *"reescritura chica"* de su §1.6. Esta noche no hubo que inventar
   el diseño: había que ejecutarlo.
4. **Se hace entera sin hardware**, y no colisiona con nada abierto salvo dos
   conflictos textuales de tres líneas.

## Lo que encontré, en orden de gravedad

### 1. La alerta de sobrecorriente era imposible — y la cadena rompía la placa

El archivo asumía **ACS712 alimentado con 5 V**: reposo en 2,5 V, 100 mV/A,
leído por un ADC de 3,3 V. Desde 2,5 V hasta el techo del ADC quedan 800 mV
(740 con margen de recorte) ⇒ **5,2 A RMS** antes de que la senoidal pegue
contra el riel. El umbral era `CURRENT_OVERCURRENT 20.0`.

> No estaba mal calibrado. **No podía dispararse nunca.** Y
> `CURRENT_COMPRESSOR_MAX 15.0`, que lo desarmaba, tampoco.

Y peor que el número: 20 A × 100 mV/A son 2 V de pico **sobre** los 2,5 V de
reposo = **4,5 V en un GPIO** cuyo máximo absoluto es VDD+0,3 = 3,6 V. Esa
cadena no medía mal: quemaba el ESP32. Por eso el producto ya había elegido otra
cosa (`PLAN_TERMOVIGIA_3`, decisión 4: *"SCT-013 al ADC directo (nada de 220 V
en la placa); ACS712 descartado"*) — sólo que el código nunca se enteró.

**La barrera que le faltaba, y ahora existe:** el rango representable ya no es
un dato suelto, sale de las mismas constantes que la sensibilidad, y un
**`static_assert` rompe la compilación** si el umbral de alerta cae afuera. Es
la misma doctrina que el largo de trama de galgas de anteanoche: dos cosas que
se pueden desincronizar en silencio, se sincronizan por construcción.

### 2. El horómetro contaba cero para siempre

```c
unsigned long compressorTotalHours;
unsigned long runMinutes = (millis() - onTime) / 60000;
currentState.compressorTotalHours += runMinutes / 60.0;   // ← float a entero
```

Un ciclo de heladera dura 10-40 minutos ⇒ `runMinutes / 60.0` da 0,17…0,67 ⇒
**truncado a 0**. Sólo habría contado ciclos de más de una hora, y una heladera
que corre una hora seguida ya es la falla, no la operación. Encima
`currentSensorInit()` lo ponía en 0 con un `// TODO: Cargar de Preferences` al
lado: **como el número siempre era 0, el TODO nunca se iba a notar**.

Ahora la cuenta va en **segundos enteros**, sin coma flotante en el camino, y se
persiste en NVS en su propio namespace (`current`, nunca `prefs.clear()`, como
pide §1.8 del plan), escribiendo una vez por hora para no gastar la flash.

### 3, 4, 5 y 6

- **La corriente chica se truncaba a 0.** `long sum` acumulando amperes al
  cuadrado + `sqrt(sum / samples)` con **división entera**: por debajo de 1 A el
  sensor leía **0,00 A**, y por arriba sólo podía dar la raíz de un entero
  (0 · 1,00 · 1,41 · 1,73 · 2,00 · 2,24 …). Justo alrededor del umbral de
  "compresor andando" (2,0 A) la resolución era de ~0,25 A.
- **La ventana de medida no era de un ciclo.** 100 muestras × 200 µs son 20 ms
  *si `analogRead()` fuera gratis*; cuesta ~100 µs, así que la ventana real era
  ~1,5 ciclos de 50 Hz — y el RMS de un número no entero de ciclos **depende de
  la fase en que arrancó**: dos lecturas idénticas dan números distintos. Ahora
  la ventana se mide **en tiempo** (`while (micros() - t0 < 20000)`).
- **Una falsa alarma por arranque.** Un compresor pide corriente de rotor
  bloqueado (5-8× la nominal) en **cada** arranque, y el código declaraba
  sobrecorriente con **una sola muestra**. Una heladera arranca ~50 veces por
  día: el canal que se vende como *"te avisamos antes de que se rompa"* habría
  mandado decenas de falsas alarmas diarias hasta que el comerciante silencie el
  bot. Ahora: ventana ciega de 3 s desde el arranque + 3 muestras sostenidas.
- **Y el aviso se consumía antes de mandarse** (`overcurrentAlert = true` arriba
  del `if (state.internetAvailable)`). **Cuarto branch consecutivo con este
  patrón** — 08-29, 09-06-b, 09-07-b. Acá el escenario correlacionado es de
  manual: **un compresor trabado tomando corriente de rotor bloqueado hace
  saltar la térmica, y de esa térmica cuelga el router.**
- **"Verificar termostato" clavado para siempre.** `startCount > 100` con un
  contador que no baja nunca ⇒ a las 48 h el mensaje queda pegado al estado de
  un equipo sano. El síntoma que importa no es cuántos arranques lleva en su
  vida sino el **ritmo**: ahora es una ventana móvil de una hora (arma en 12,
  desarma en 8) y `startCount` queda como diagnóstico que **no genera avisos**.

## Qué se entregó

`firmware_modular/current_model.h` — **puro** (sin Arduino, sin HTTP, sin
`analogRead`) e **incluido** por `current_sensor.h`: no es un espejo, lo que se
testea es lo que se flashea. Mismo criterio que `sensor_fault_model.h` (08-29),
`temp_report_model.h` (09-04-b), `door_alert_model.h` (09-06-b),
`power_alert_model.h` (09-07-b) y `trama_revd.h` (galgas).

`current_sensor.h` reescrito sobre el front-end que el producto sí eligió
(SCT-013-030 con bias 1,65 V en **GPIO32, el de `config.h`** — el archivo viejo
lo pisaba con 36), más `config.h`, el `.ino`, la suite y el doc.

**Tres estados, no dos:** si la ventana recortó contra un riel, si el bias medido
se alejó del nominal o si no entraron muestras suficientes, la lectura es
**inválida** — `current_amps` viaja como `null` y **el modelo no decide nada**:
no cuenta arranques, no acumula horas, no dispara ni limpia alertas. Un canal
roto no puede declarar que el compresor está parado; eso es la temperatura
congelada del 09-04-b con otra unidad.

## Cómo verificarlo (comandos exactos, sin hardware, ~6 minutos)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-09-08-el-compresor-que-no-se-cuenta

# 1) la decisión, contra el header que se flashea
g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_current_model.exe tools/test_current_model.cpp
./tools/test_current_model.exe

# 2) que los tests sirvan: reimplantar los defectos y ver que mueran
python tools/mutantes_current_model.py

# 3) que compile como se flashea HOY (módulo apagado)
arduino-cli compile --fqbn "esp32:esp32:esp32:PartitionScheme=min_spiffs" firmware_modular

# 4) que compile con el módulo PRENDIDO  <- esto prueba que ya linkea
arduino-cli compile --clean --fqbn "esp32:esp32:esp32:PartitionScheme=min_spiffs" \
  --build-property "compiler.cpp.extra_flags=-DCURRENT_SENSOR_ENABLED=1" firmware_modular
```

**Resultados obtenidos esta noche:**

- `test_current_model.exe` → **97 checks, 0 fallos, sin warnings**. Seis bloques
  están escritos como **regresión** (fallan contra la lógica vieja).
- `mutantes_current_model.py` → **10/10 mutantes muertos**, header restaurado y
  suite re-corrida en verde después.

  | mutante | qué reimplanta | checks que fallan |
  |---|---|---|
  | 1 | RMS acumulado en entero (la corriente chica se trunca a 0) | 6 |
  | 2 | no se detecta el recorte contra los rieles | 3 |
  | 3 | el bias se asume en vez de medirse | 4 |
  | 4 | el horómetro vuelve a la división entera (0 h para siempre) | 5 |
  | 5 | sin ventana ciega: el pico de arranque dispara la alerta | 2 |
  | 6 | el aviso se consume aunque no se haya entregado | 2 |
  | 7 | el ciclado corto se mide por arranques de toda la vida | 1 |
  | 8 | una lectura inválida decide igual (canal roto = compresor parado) | 5 |
  | 9 | debounce simétrico: una muestra alta declara el arranque | 6 |
  | 10 | la zona muerta cuenta como parada (un bajón apaga el compresor) | 2 |

- **Compilación apagado** → exit 0, **1.288.712 B flash (65 %) / 53.784 B RAM
  (16 %)** — **idéntico byte a byte al de `main`**: el gate cuesta cero.
- **Compilación PRENDIDO** → exit 0, **1.300.872 B / 54.528 B** (+12.160 B flash,
  +744 B RAM), **0 warnings**. Ésta es la verificación que importa: **el módulo
  linkea por primera vez desde que existe**.

## Sigue APAGADO, y es a propósito

`CURRENT_SENSOR_ENABLED 0` en `config.h`; el `.ino` incluye, inicializa y corre
el módulo **sólo bajo ese `#if`**. Ninguna placa del parque tiene la pinza ni el
divisor de bias, y sin ese circuito la entrada del ADC no mide corriente: mide
lo que haya. El gate es de **compilación** a propósito — una placa sin el
front-end ni siquiera lleva el código. (Está con `#ifndef` para poder compilarlo
prendido desde la línea de comandos sin editar el archivo.)

## Qué quedó SIN verificar (pide banco y pinza)

1. **⚠️ Ningún umbral está medido sobre una heladera real.** `CUR_RUN_ON_A 1.5`,
   `CUR_RUN_OFF_A 0.8`, `CUR_OVERCURRENT_A 18.0` y los 12 arranques/hora son
   puntos de partida razonables para un compresor de comercio, **no datos**. El
   ensayo que los fija: pinza sobre el vivo del compresor y registro de 24 h — de
   ahí salen la corriente de régimen, el pico de arranque real, su duración y el
   ritmo normal. Toda la lógica de arriba decide bien sobre umbrales que nadie
   midió. [@hardware + @muestreador]
2. **El bias real y su deriva.** `CUR_BIAS_TOL_MV 300` supone resistores al 5 %.
   Si el bias se mueve más que eso con la temperatura, el equipo se va a declarar
   inválido a sí mismo.
3. **Que 20 ms de ventana alcancen**: confirmar con una carga conocida (una
   estufa de 1000 W son 4,5 A a 220 V) y una pinza de mano como testigo.
4. **La persistencia del horómetro**: cortar la luz con el compresor andando y
   ver que al volver las horas siguen ahí. El ciclo en curso al momento del corte
   se pierde (hasta 1 h, que es el intervalo de guardado).
5. **Que el panel no se rompa** con los campos nuevos del JSON (`current_valid`,
   `starts_last_hour`, `short_cycle_alert`). Hoy nadie los consume; cuando se
   prenda hay que sumarlos a `readings` con migración append-only.
   [@backend + @frontend]

## Lo que NO hice, a propósito

**El aviso "el compresor no arranca con la temperatura subiendo"** — que el plan
§1.6 llama *"la diferencia entre 'se abrió la puerta' y 'se rompió el equipo'"*
y que es **lo que más vale del upsell** — **no está implementado**. El
`undercurrentAlert` del archivo viejo se declaraba, no se escribía nunca, y
tenía al lado el comentario honesto: *"esto requiere lógica adicional basada en
temperatura"*.

Sigue siendo cierto, y por eso no lo hice: necesita una señal que **hoy no
existe** (*"la temperatura de esta cámara viene subiendo de forma sostenida"*), y
esa señal depende de los **umbrales por cámara de §1.1**, que tampoco existen.
Escribirlo esta noche era inventar dos números y un contrato. El contrato que
haría falta quedó escrito en `docs/current-model.md` §7 para cuando §1.1 esté.
[@firmware]

## Colisiones al mergear

- **`config.h` y `firmware_modular.ino`**: conflicto textual chico con
  `nocturno/local-2026-09-07-b-el-corte-que-nadie-avisa`, que agrega
  `POWER_MONITOR_ENABLED` y su propio bloque `#if` en los mismos dos lugares.
  Son bloques independientes: **se conservan los dos**, en cualquier orden.
- **`currentTelegramWindowOpen()` duplica `powerTelegramWindowOpen()`** de ese
  branch (las dos puertas de `sendTelegramMessage()`: token y ventana de 5 min,
  que descarta en silencio porque es `void`). Al mergear los dos, colapsarlas en
  un helper — o, mejor, hacer que ambas entreguen por la cola de transporte de
  `nocturno/local-2026-09-01-b-el-aviso-que-no-sale`, que es donde esto tiene que
  vivir. Mientras tanto la duplicación es correcta y no rompe nada.
- Los tres archivos nuevos (`current_model.h`, `tools/test_current_model.cpp`,
  `tools/mutantes_current_model.py`) no colisionan con nada.

## Anotado y NO tocado

- **La numeración de `QUE_FALTA.md` sigue pisada**: el 09-05-b, el 09-06-b y el
  09-07-b usaron todos el ítem **21**. Éste entró como **22** para no sumar al
  problema, con el aviso escrito al lado. Renumerar al mergear. [@cronista]
- **`main` tiene cuatro `.exe` de test commiteados** en `tools/`
  (`test_net_witness.exe`, `test_offline_buffer.exe`, `test_sensor_fault.exe`,
  `test_telegram_gate.exe`). El de esta noche **no** viaja en el commit (se
  regenera con g++). Sacar los otros del repo es una limpieza de un minuto que no
  hice para no mezclarla con esto. [@bibliotecario]
- **Los umbrales del módulo no son configurables desde la web ni desde Supabase.**
  Cuando se prenda en un cliente van a tener que serlo (es la lección del
  09-06-b con `config.doorEnabled`). Toca `types.h`, `storage.h`, `web_api.h`,
  `html_ui.h` y el pull de config: es su propio branch, y hoy no tiene sentido
  porque no hay ni una pinza puesta. [@firmware]

## Estado al cerrar

- Branch pusheado: `nocturno/local-2026-09-08-el-compresor-que-no-se-cuenta`
  (`0d8a6be`).
- `QUE_FALTA.md` de frioseguro actualizado (ítem 22).
- Worktree `C:\Proyectos\_noche_frio_0908` eliminado; el árbol de `frioseguro`
  quedó **idéntico**, en el branch `09-04-b`, con el KiCad de TermoVigía sin
  commitear como estaba.
- El `.exe` del test no viaja en el commit.
- En MATI-HQ quedaron **sin commitear, tal como los encontré**,
  `dominios/pcb.md` y `scripts/turno_noche_log.txt`: son de otro trabajo (la
  rev G de la PCB de galgas) y no me corresponde firmarlos.
- Nada corriendo, nada abierto.
