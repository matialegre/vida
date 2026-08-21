# Nocturno local — 2026-08-20

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (RuView — prioridad #1 de banco).
**Branch:** `nocturno/local-2026-08-20-rafaga-bateria` (pusheado, `ff2ae28`).
**Sale de:** `nocturno/local-2026-08-18-b-lector-campana` (**mergear ese primero**).

## TL;DR

Anteanoche el laboratorio aprendió a **leer** la batería de una campaña. Esta
noche la campaña aprendió a **escribirla**, que era el único modo en que el dato
directamente no existía.

> `eco.py` leía la batería una vez por ráfaga y la mandaba **sólo por WiFi**. El
> archivo que queda en la SD no la llevaba. Si la campaña fue sin cobertura —el
> caso que justifica la SD— la tensión de esas horas **no existía en ningún
> lado**.

Y un segundo defecto, que apareció al mirar el **nombre** del archivo y no el
contenido:

> El archivo se llama `e%03d_%d.csv` = índice + uptime. **Los dos arrancan en
> cero en cada arranque**, así que dos arranques producen los **mismos nombres**
> (`e001_12.csv`) y el segundo abre `"w"` sobre el primero. **Una campaña que se
> reiniciaba se borraba sola.** No es una carrera: el ciclo eco es periódico, es
> determinista.

## Tarea elegida y por qué

Por rotación tocaba `datalogger` (las dos noches anteriores fueron galgas y
frioseguro; el último datalogger fue el 08-18-b). Descarté `cosechador` por la
misma razón de las últimas cinco noches, que dejo dicha para no re-decidirla: es
P2, todo su `QUE_FALTA` está bloqueado por la compra y ya acumula cuatro
análisis sobre el mismo material.

Dentro del repo **no busqué**: la auditoría del 08-17 dejó un orden sugerido y
BAT-07 es el punto 2, escrito así:

> *«**BAT-07** — agregar la columna `vb` al header de ráfaga de `eco.py`.»*

Tercera noche seguida en que la tarea la elige un pendiente ya nombrado por un
informe anterior. Y es el complemento exacto del 08-18-b: sin esto, el lector
que aprendió a leer la batería de una campaña **no tiene nada que leer** en el
modo eco, que es el modo de las campañas largas.

## La decisión que no seguí (y por qué)

La auditoría pedía una **columna**. No la hice, y la razón es medible:

La ráfaga muestrea a **~1 kHz** y el `f.write` de cada fila está **adentro del
lazo crítico**. Una columna constante son **decenas de miles de formateos de
float por archivo**, por un dato que **no cambia dentro de la ráfaga**. Se paga
jitter de muestreo —que es el número que el DoD de este repo mide, el bloqueante
🔴 #1— para no ganar ninguna información.

La batería es **un valor por ráfaga**. Va en la metadata del archivo:

```
# eco rafaga hz_obj=1000  accel_LSB_per_g=16384 gyro_LSB_per_dps=131 up_s=612 vb_ini=4.021
t_us,ax,ay,az,gx,gy,gz
... decenas de miles de filas ...
# fin vb_fin=3.998 n=9987
```

Tres decisiones que van con eso, todas fijadas con test:

- **`vb_ini` se mide ANTES de la ráfaga y va en el header.** Una campaña termina
  porque se acaba la batería, y el último archivo es justamente el que queda
  cortado a la mitad. El dato más informativo de toda la campaña es el que se
  perdería si estuviera sólo al final.
- **`up_s`** (segundos desde el arranque) es lo único que ordena los archivos en
  el tiempo: `t_us` vuelve a cero en cada ráfaga.
- **La serie usa `vb_ini`, nunca mezclada con `vb_fin`.** Son dos condiciones de
  carga distintas; alternarlas metería en la pendiente un serrucho que no es
  descarga.

## Qué hice

### 1. Firmware — `eco.py`, las **dos** copias

`firmwares/pico2w-node/` y `firmwares/pico2w-eco-com14/` son el mismo firmware
duplicado (el `LEEME_GIMAP` apunta al segundo como el nodo eco de GIMAP). Los dos
tenían el defecto idéntico y los dos están arreglados: `vb_ini`/`up_s` en el
header, `vb_fin`/`n` en la línea de cierre, y `_mount_sd()` retomando la
numeración con un `os.listdir("/sd/eco")` por montaje.

### 2. Laboratorio — `pc-sniffer/analysis.py`

- **`read_eco_meta(path)`** lee la metadata **sin parsear las filas** (header +
  últimos 256 bytes). Una campaña son cientos de archivos de decenas de miles de
  filas: abrirlos enteros por dos números sería leer gigabytes. Hay un test que
  lo prueba de la única forma que no miente: las filas del archivo son **basura
  ilegible** y la metadata igual sale.
- **`eco_battery_series(paths)`** arma la curva de la campaña.
- `import_sd_csv` también devuelve la metadata (y la línea de cierre **no** entra
  como fila fantasma — hay test).

### 3. `/api/eco_battery?dir=<carpeta>`

`/api/ds_battery` (el del 08-18-b) contesta sobre **un archivo**, y un archivo de
ráfaga dura **segundos**: no hay descarga que ver adentro. La campaña eco es la
**carpeta** entera. Este es el camino desde esa carpeta hasta "cuánto le queda".

### 4. Cuando el nodo se reinicia, la serie se **corta**

`up_s` vuelve a cero y **nadie sabe cuánto estuvo apagado**. Pegar los dos tramos
sería inventar ese hueco: `eco_battery_series` devuelve **segmentos** y dice
cuántos hubo (`segmentos > 1` en la respuesta = el nodo se reinició durante la
campaña). Los archivos sin metadata —firmware viejo, archivo cortado antes del
header— se **listan por nombre** en vez de entrar como cero: un cero se
confundiría con una celda muerta (mismo criterio que BAT-11).

### 5. El checker y el doc

`check_battery_chain.py` ahora audita que el dato **exista** en la SD, no en qué
formato: BAT-07 desaparece y el eslabón 6 baja de **ROTO a fricción**. La
auditoría (`docs/battery-chain.md`) tiene la sección de cierre con el "por qué no
es una columna".

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-20-rafaga-bateria

python tools\test_eco_battery.py             # 26 tests, ~0,3 s
python tools\test_import_sd_csv.py           # 25 tests (sin cambios)
python tools\test_check_battery_chain.py     # 73 tests (eran 72)

python tools\check_battery_chain.py          # BAT-07 ya no aparece: 10 hallazgos
python tools\check_battery_chain.py --demo-lectura
```

**Lo que verifiqué yo, corriendo:**

- **124/124 tests OK** (26 nuevos + 73 + 25). Sin red, sin hardware, ~6 s.
- **La cadena bajó de 5 eslabones ROTOS a 4**, y de 11 hallazgos a **10**.
- **El endpoint, punta a punta** con el test client de Flask sobre una campaña
  sintética de 13 ráfagas (4,10 → 3,60 V en 6 h):
  `{"eta_h":7.2,"slope_v_per_h":-0.0833,"span_h":6.0,"segmentos":1,"sin_meta":0}`.
  Los tres caminos de error (carpeta que no existe, carpeta vacía, firmware
  viejo) devuelven su mensaje y no revientan.
- **Mutación** — que los tests sean red y no decorado:

  | mutación | resultado |
  |---|---|
  | no cortar el segmento al reiniciar el nodo | **1 falla** |
  | mezclar `vb_fin` en la serie | **3 fallan** |
  | aceptar `vb_ini=0` como medición | **1 falla** |
  | no leer la cola del archivo (sin `vb_fin`) | **2 fallan** |
  | sacar la guarda de basura del parseo | **1 falla** |
  | que el firmware deje de escribir `vb_ini` | **1 falla + reaparece BAT-07** |
  | sacar el `listdir` de la numeración | **1 falla** |

  Restaurado → 124/124. **Ninguna sobrevivió.**

## Lo que quedó sin verificar (necesita hardware)

1. **Que un Pico 2 W real escriba estos archivos.** Todo lo de arriba corre sobre
   archivos sintéticos y sobre el **texto** del firmware. Es de @tester con el
   nodo eco y una SD: 15 minutos, `eco_cycle_s=20` y mirar `/sd/eco`.
2. **Que `time.time()` en MicroPython devuelva segundos desde el boot** en esta
   build. Es lo esperable sin RTC seteado, pero **no lo verifiqué en la placa**.
   Si devolviera 0 siempre, `eco_battery_series` armaría un segmento por archivo
   y lo diría (`segmentos` = N) — falla ruidosa, no silenciosa, pero hay que
   mirarlo.
3. **El costo del `listdir` por montaje** con cientos de archivos en `/sd/eco`
   (@energia/@muestreador). Es una vez por montaje, no por ráfaga; estimado
   despreciable, **no medido**.
4. **`vb_ini` en banco va a decir ~4,7 V** con el USB enchufado: hereda BAT-01
   (el firmware no distingue batería de USB). Está dicho en el doc y en el
   informe del branch; **no es regresión de esta noche**, es el hallazgo abierto.

## Lo que este branch NO toca

- **Ningún umbral, ninguna curva de porcentaje, ningún `v_empty`.** BAT-05 y
  BAT-06 siguen abiertos: son una decisión de qué significa "vacío" (@energia),
  no un bug.
- **No toca `nodo.py`** (el modo campaña clásico ya grababa la columna `vbat`),
  ni LoRa, ni el frame RV1, ni el gateway ESP32, ni la nube.
- **`bat_low` sigue sin disparar nada** (BAT-12) y el modelo de autonomía sigue
  siendo una recta (BAT-10).
- **Nada de mDNS** (regla dura del repo).
- **No toqué el trabajo sin commitear de Matías** (ver higiene).

## Nota para el Director

Lo que agrega esta noche al patrón de las tres anteriores: **la auditoría dijo
cómo arreglarlo y el arreglo no le hizo caso, con evidencia.** Pedía una columna;
una columna habría metido decenas de miles de formateos de float en un lazo de
1 kHz — o sea, habría degradado el número que el bloqueante #1 del DoD mide, para
guardar un dato que no cambia dentro de la ráfaga. El hallazgo (*el dato no
existe*) era correcto; la implementación sugerida, no. Vale anotarlo: los
informes nocturnos nombran bien **el problema**, y la solución se vuelve a
decidir en el momento de escribirla.

Segundo: **el defecto más grave de la noche no estaba en ninguna auditoría.**
Que una campaña se borre sola al reiniciarse el nodo no lo vio ni la cadena de la
batería, ni la de recuperación de la SD (08-15), ni la de puesta en marcha
(08-13) — tres auditorías que miraron ese mismo directorio. Apareció al leer el
`%` del nombre del archivo mientras escribía otra cosa. Es un argumento a favor
de seguir haciendo **implementación** y no sólo auditoría: se toca código que la
auditoría sólo lee.

**Estado de la cola de merge:** `datalogger` tiene **22 branches sin mergear a
`main`**. La cadena de la batería ya son tres eslabones encadenados
(08-17 auditar → 08-18-b leer → 08-20 escribir) y **el último no sirve solo**.

**Próximo paso concreto:** mergear en orden `08-17-cadena-bateria` →
`08-18-b-lector-campana` → `08-20-rafaga-bateria`. Los tres son software puro,
sin hardware, y entre los tres bajan la cadena de **6 eslabones rotos a 4** y
desbloquean el 🔴 #4 (medir consumo real) y el 🟡 #10 (vista de batería).

---

**Higiene del cuartel:**

- ⚠️ **MATI-HQ sigue con los mismos 16 modificados + los sin trackear** de los
  informes anteriores (`comercial/`, `DREYFUS_ESQUEMATICO.*`, `backups/`,
  `propuestas/MAIL_SAE_PPS.md`, `agentes/diseno3d.md`…). **No los toqué ni los
  commiteé.** Este commit sólo agrega este informe.
- ⚠️ **`C:\Proyectos\datalogger` tiene trabajo de día SIN COMMITEAR del 08-10**:
  `firmwares/nodo-gimap/`, `tools/rx_gimap.py`, `tools/test_protocolo_gimap.py`,
  `tools/test_red_gimap.py`, `docs/ARMADO_NODO_GIMAP.html` y un `.gitignore`
  modificado. **No los toqué** — commiteé sólo mis 9 archivos, uno por uno.
  Detalle que importa: `firmwares/nodo-gimap/` es la **evidencia de BAT-01 y
  BAT-02** (el driver que sí detecta USB), y **no está versionado**: en un clone
  limpio el checker pierde la mitad de esa evidencia. Hay un test que lo cubre,
  pero la solución de verdad es commitearlo.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío. El latido de DESKTOP-RK8DH7C
  sigue parado desde el **2026-08-07** (13 días).
