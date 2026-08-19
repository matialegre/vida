# Nocturno local — 2026-08-18-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (P0 — "terminarlo primero, antes del
trabajo Dreyfus").
**Branch:** `nocturno/local-2026-08-18-b-lector-campana` (pusheado, `63ad41a`).
**Sale de:** `nocturno/local-2026-08-17-cadena-bateria` (hay que mergear ese primero).

## TL;DR

**Tercera noche seguida de implementación en vez de auditoría.** Y esta vez lo
que apareció al escribir el código es que **dos auditorías distintas, con dos
meses de diferencia, habían encontrado el mismo defecto desde lados opuestos y
ninguna lo había visto como uno solo.**

- La **cadena de recuperación** (08-15), hallazgo **D1**: *"una vibración de
  66 Hz aparece en 0,066 Hz"*.
- La **cadena de la batería** (08-17), hallazgo **BAT-08**: *"la serie de
  batería de una campaña entera se carga como todos ceros"*.

Son el mismo bug:

> **`import_sd_csv` conocía dos formatos de CSV y el de CAMPAÑA no era ninguno
> de los dos.** Caía a la rama del sniffer, que asume tiempo en **segundos** y
> valores **ya en unidades físicas**. Un archivo de campaña tiene el tiempo en
> **milisegundos** y los valores en **cuentas int16**.

Tres síntomas independientes, un solo arreglo:

| se veía como | era |
|---|---|
| la batería de la campaña "no tiene muestras" | la columna se llama `vbat`, el lector buscaba `vb` |
| una vibración de 66 Hz aparecía en **0,066 Hz** | `t_ms` leído como segundos: `fs` y toda frecuencia /1000 |
| aceleraciones de **16.384 g** | cuentas crudas sin dividir por `ACC_LSB_G` |

Y el detalle que hace que esto importe hoy: **el formato de campaña es el que
produce el DoD.** *"Canal MPU + canal piezo logueando a SD sin gaps durante N
horas"* deja exactamente ese archivo. El único consumidor que lo leía bien era
el `/plot` que corre **en la placa** — o sea, el que no sirve cuando volvés con
la SD en el bolsillo.

## Tarea elegida y por qué

Por rotación el más viejo era **cosechador** (08-16). Lo descarté por la misma
razón que anoche y la dejo dicha de nuevo para no re-decidirla cada noche: es
**P2**, todo su `QUE_FALTA` está bloqueado por la compra, el repo **no tiene una
línea de código** (4 docs y 2 PDFs) y ya acumula **cuatro análisis** sobre el
mismo material. Un quinto sería cantidad, no calidad.

Fui a **datalogger**, que es **P0** ("terminarlo primero"), y adentro busqué lo
que dijeron los dos informes anteriores: la deuda del repo ya no es de
diagnóstico. Datalogger tiene **19 branches nocturnos sin mergear** y casi todos
son análisis.

El `check_battery_chain` del 08-17 dejó un orden de arreglo explícito y el
primero decía:

> *"**BAT-08** — agregar `"vbat"` a la lista de columnas de `import_sd_csv`.
> **Una línea**, y desbloquea la medición de autonomía sobre datos que ya
> existen."*

**Al escribirlo apareció que una línea no alcanzaba** — y ese es el hallazgo de
la noche. Agregar `"vbat"` a la lista hubiera hecho que la serie de batería
**existiera** pero con el eje de tiempo 1000× mal: la proyección de autonomía
habría contestado, con cara de respuesta correcta, una autonomía **mil veces**
equivocada. El arreglo de una línea era peor que el bug, porque el bug al menos
decía "pocas muestras".

## Qué hice

### `pc-sniffer/analysis.py` — el lector

El formato ya no se decide con un booleano (`raw_mode = "t_us" in header`) sino
con una tabla declarada:

```python
FORMATOS = {                 # columna de tiempo -> (factor a segundos, cuentas crudas)
    "t_us":   (1e-6, True),  # ráfaga eco en la SD
    "t_ms":   (1e-3, True),  # campaña clásica en la SD   <- el que faltaba
    "host_t": (1.0,  False), # export del propio sniffer
}
ALIAS = {..., "vb": "vb", "vbat": "vb", "tempC": "tc", ...}
```

Tres decisiones de diseño, que es lo único acá que conviene revisar:

- **El formato se decide por el nombre de la columna de tiempo, no mirando los
  datos.** Los tres headers del repo son distinguibles sin heurística. Una
  heurística sobre los valores ("¿esto es 1 g o son 16384 cuentas?") sería
  adivinar, y adivinar mal acá significa un informe con una unidad equivocada.
- **Un header desconocido no rompe**: se declara `formato: "desconocido"` en la
  salida y se supone lo de antes. Quien lea el informe ve qué se supuso, en vez
  de recibir un número sin procedencia.
- **Una fila con menos columnas que el header se descarta y se cuenta**
  (`descartadas`). Una campaña termina como terminan las campañas —se acaba la
  batería a mitad de línea— y esa línea cortada **volteaba el import entero**
  (numpy no arma un array ragged). Ocho horas de datos perdidas por los últimos
  12 bytes.

También `battery_projection`: `round(eta/3600, 2) if eta else None` →
`if eta is not None else None`. Con `vb == v_empty`, `eta` vale `0.0`, que es
*falsy*: **el instante más informativo de la serie salía como "no se pudo
estimar"** (BAT-14).

### `pc-sniffer/sniffer.py` + `page.py` — el camino hasta la respuesta

`/api/ds_battery?ds=<archivo>`: proyección de autonomía **sobre un CSV importado
de la SD**. Sin esto, arreglar BAT-08 no servía de nada: el `/api/battery_report`
sólo habla de lo que el sniffer escuchó **en vivo**, y una campaña desatendida
es exactamente el caso en que **no había nadie escuchando** (BAT-09). Diezma a
≤20.000 muestras porque la batería se lee 1 vez por segundo y el archivo puede
tener millones de filas de vibración; no cambia el ajuste y evita copiar 10 M de
floats. La página lo muestra al lado de la FFT del dataset.

### `tools/test_import_sd_csv.py` — 25 tests nuevos

Cinco capas: los tres formatos uno por uno, **no romper lo que ya andaba** (eco
y sniffer), archivos rotos, la cadena entera (de un archivo de 8 h de campaña a
*"le quedan N horas"*), y contra el repo real (que el `ALIAS` no se quede atrás
si el firmware cambia el header — hay un test que lee `nodo.py` y falla si el
header cambió).

### `tools/check_battery_chain.py` — el checker de anoche

`extraer_lector` ahora entiende **las dos formas** de escribir el lector (la
vieja tupla literal y la tabla nueva), así que los 70 tests de anoche siguen
detectando el defecto si alguien lo reintroduce con la forma vieja. Y **BAT-09
sólo salta si el ÚNICO camino es el historial vivo** — antes miraba nada más
que existiera ese camino.

De sus tests, **5 pinneaban el bug como conducta**; ahora pinnean el arreglo
(`[REGRESION]`), incluido uno nuevo que falla si BAT-08/09/14 vuelven a
encenderse en el repo real, o sea si el arreglo se pierde en un merge.

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-18-b-lector-campana

# los 97 tests (< 5 s, sin red ni hardware)
python -m unittest tools.test_import_sd_csv tools.test_check_battery_chain

# el lector ahora resuelve las dos columnas
python tools\check_battery_chain.py --demo-lectura
python tools\check_battery_chain.py            # 11 hallazgos (eran 14), exit 3
```

**Lo que verifiqué yo, corriendo:**

- **97/97 tests OK** (25 nuevos + 72 del checker, que eran 70).
- `py_compile` de los 6 archivos tocados.
- **Mutación** — que los tests sean red y no decorado. Revertí cada mitad del
  arreglo por separado:

  | mutación | resultado |
  |---|---|
  | sacar el alias `vbat` → `vb` | **4 tests fallan** |
  | volver a tratar `t_ms` como segundos | **3 tests fallan** |
  | volver al `if eta` | **1 test falla** |
  | sacar la guarda de fila corta | **1 test revienta** |

  Restaurado → 97/97 OK.
- El checker: **14 → 11 hallazgos**, eslabones **6 → 5 ROTOS** (el 8, *"serie →
  cuánto le queda"*, baja a fricción: le queda BAT-10, que es `warn`).
- Exit code 3 y `--json` válido, como antes.

## Qué quedó sin verificar (necesita hardware / una campaña real)

1. **Que un CSV de campaña REAL se lea bien.** Todos los archivos de prueba los
   generé yo con el header que dice `nodo.py`. Un archivo de verdad puede traer
   cosas que no modelé: `ticks_ms` envolviéndose a los 12,4 días (D3 del 08-15),
   líneas mezcladas de dos arranques (D2), una misión Dreyfus que **reusa las
   columnas `ax,ay,az` para otra magnitud** (D5). El test que más vale es
   apuntar el laboratorio a un archivo que salga de una SD.
2. **La página.** El `/api/ds_battery` está probado como código, no abierto en
   un navegador: `python pc-sniffer\sniffer.py`, importar un CSV y mirar que
   aparezca la línea de batería al lado de la FFT. Es de @tester, 5 minutos.
3. **Que la autonomía que da sea creíble.** El modelo sigue siendo una recta
   (BAT-10). Ahora **recibe datos**; que el número sea correcto es otra
   discusión, y recién ahora se puede tener con una campaña real de por medio.

## Lo que este branch NO hace (a propósito)

- **No toca ningún umbral, ninguna curva de porcentaje, ningún `v_empty`.**
  BAT-05 y BAT-06 (4 curvas con 10 puntos de spread, 4 tensiones distintas de
  "vacío") siguen abiertos: son una decisión de qué significa *vacío*, no un bug
  del lector, y esa decisión es tuya.
- **No toca ningún firmware.** BAT-07 (la ráfaga eco no graba batería en la SD)
  sigue abierto; hay un test que lo fija como conducta conocida para que el
  archivo de ráfaga devuelva ceros **sin romper nada**.
- **Siguen abiertos** BAT-01, BAT-02, BAT-05, BAT-06, BAT-07, BAT-10, BAT-11,
  BAT-12, BAT-13. Los que quedan de software puro y baratos son, en orden:
  BAT-07 (columna de batería en la ráfaga), BAT-01 (portar `en_usb()` — sin eso
  **ninguna prueba de banco del camino de batería baja es válida**, porque con
  el USB enchufado VSYS es el riel del USB) y BAT-05/06 (una sola fuente de
  verdad de curva y umbrales).
- **No toqué `data/`, ni el frame RV1, ni nada de mDNS.**

## Nota para el Director

Lo de esta noche es un caso concreto de algo que ya dijeron los tres informes
anteriores, y ahora tiene evidencia:

**Dos auditorías encontraron el mismo defecto y ninguna se enteró de la otra.**
D1 (08-15) y BAT-08 (08-17) están escritos en dos documentos distintos, con dos
códigos distintos, como si fueran dos problemas. Son una función de 20 líneas.
El costo de la deuda de merge no es sólo que los arreglos esperen: es que **los
análisis se repiten sin saberlo**, y cada repetición gasta una noche.

`datalogger` tiene **19 branches nocturnos sin mergear**. `galgas`, 11.
`frioseguro`, 13.

**Próximo paso concreto:** mergear `08-17-cadena-bateria` y después éste. Y si
hay media hora de día, apuntar el laboratorio a un CSV real de la SD — eso cierra
el punto 1 de arriba y es la primera vez que el repo va a poder contestar
*"¿cuánto le quedaba de batería en la hora 6?"* sobre datos que ya existen.

---

**Higiene del cuartel:** MATI-HQ seguía con cambios sin commitear al arrancar
(los mismos 16 modificados + 4 sin trackear de los informes anteriores). **No los
toqué ni los commiteé**: son trabajo tuyo en curso. Este commit sólo agrega este
informe y la entrada del `QUE_FALTA`. En `datalogger` tampoco toqué lo que está
sin trackear (`firmwares/nodo-gimap/`, `tools/rx_gimap.py`,
`tools/test_protocolo_gimap.py`, `tools/test_red_gimap.py`,
`docs/ARMADO_NODO_GIMAP.html`) ni el `.gitignore` modificado — el commit lista
los 8 archivos uno por uno.
