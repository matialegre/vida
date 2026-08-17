# Nocturno local — 2026-08-17

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (P0 — "terminarlo primero, antes del
trabajo Dreyfus").
**Branch:** `nocturno/local-2026-08-17-cadena-bateria` (pusheado, `f615166`).

## TL;DR

El DoD del datalogger pide dos cosas que son la misma pregunta: *"N horas
logueando sin gaps"* y *"consumo **MEDIDO** con INA219, no estimado"*. Las dos
dependen de saber **cuánta batería le queda al nodo y quién se entera a tiempo**.
Un nodo que se apaga en la hora 5 de una campaña de 8 no tiene gaps: tiene un
archivo que termina.

Siete auditorías previas siguen el dato de vibración. Ninguna siguió el otro
número que viaja por los mismos cables: **`vbat`**.

**De los 9 eslabones: 1 OK, 2 con fricción, 6 ROTOS.** 14 hallazgos.

Tres números, sacados del propio código:

- **Un nombre de columna separa 8 horas de datos de la respuesta.** El nodo
  escribe `t_ms,seq,ax,…,tempC,vbat`. `import_sd_csv` busca
  `("ax","ay","az","gz","vb")` y **rellena con ceros lo que no encuentra**:
  `vbat` no está en esa lista. La serie de batería de una campaña entera se
  carga como todos ceros, `battery_projection` filtra `v>0.1`, se queda sin
  muestras y devuelve **"pocas muestras"**. Dos letras.
- **El ETA de autonomía sobrestima +836 % justo cuando importa.** Ajusta una
  recta sobre la última mitad de la ventana y extrapola hasta 3,00 V. Con una
  LiPo modelada descargando en 40 h, a las **32 h** proyecta **74,8 h
  restantes** contra **8 h** reales. El error crece cuanto más cerca del final
  se pregunta — que es cuando se pregunta.
- **El firmware de producción no distingue batería de USB.** `Battery.read_v()`
  lee VSYS y lo llama tensión de batería; con el USB enchufado VSYS es el riel
  del USB (~4,7 V), `pct` se satura en 100 % y `bat_low` nunca se enciende. Es
  la condición de **todo el banco** y de toda sesión de OTA: **el camino de
  batería baja no se puede haber probado nunca**. El repo ya tiene la detección
  escrita (`en_usb()`), en otro firmware.

Y el cierre de la cadena: **`bat_low` no dispara ninguna acción**. No viaja en el
frame RV1, no apaga nada, no avisa. El único aviso del sistema es un cartel en la
página web local del gateway, con un umbral distinto (3,30 vs 3,20). El único
corte por batería del repo está en **otro** firmware (`nodo-gimap/main.py:189`).

## Tarea elegida y por qué

Por rotación tocaba datalogger (los cinco turnos previos: cosechador 08-14,
frioseguro 08-14-b, datalogger 08-15, galgas 08-15-b, cosechador 08-16,
frioseguro 08-16-b — el más viejo era éste).

Los 🔴 del `QUE_FALTA` sin branch siguen siendo banco o hardware (#1 necesita
flashear, #2 es el front-end del piezo, #3 y #4 necesitan medir). Y los 18
branches previos cubren el **dato de vibración** en todos sus tramos:

| noche | qué audita | de qué número habla |
|---|---|---|
| 08-03 `registro-sd` | contabilidad de lo que se graba | aceleración |
| 08-04-b `contrato-rv1` | forma del frame LoRa | aceleración |
| 08-06-b `contrato-nube` | forma de lo que llega a la nube | aceleración |
| 08-08 `fidelidad-benchmark` | si el benchmark mide lo que dice | aceleración |
| 08-10 `cadena-vibracion` | qué significa el número | aceleración |
| 08-13 `cadena-puesta-en-marcha` | cómo arranca el nodo | — |
| 08-15 `cadena-recuperacion` | de la SD al informe | aceleración |

**`vbat` viaja por los mismos siete tramos y nunca fue auditado** — y es el
número del que dependen los dos ítems del DoD que siguen abiertos (#4 consumo
medido, #10 vista de batería en el dashboard).

## Qué hice

Un análisis + una herramienta ejecutable + tests. Mismo patrón que las noches
anteriores (`check_retrieval_chain`, `check_temperature_chain`).

| archivo | qué es |
|---|---|
| `tools/check_battery_chain.py` | el checker: lee el repo, cita `archivo:línea`, 14 hallazgos, 5 modos `--demo` |
| `tools/test_check_battery_chain.py` | **70 tests**, 7 capas |
| `docs/battery-chain.md` | el análisis escrito, los 9 eslabones, orden sugerido de arreglo |
| `QUE_FALTA.md` | sección nueva "Análisis offline hecho" |

**No toqué ni una línea de firmware, análisis ni dashboard.** Cero fixes
aplicados: esto es diagnóstico, y varios arreglos dependen de una medición en la
placa que no puedo hacer.

### Los 9 eslabones

| # | eslabón | estado |
|---|---|---|
| 1 | celda → riel VSYS | OK |
| 2 | VSYS → entrada del ADC | **ROTO** (BAT-02, BAT-13) |
| 3 | cuentas del ADC → volts | **ROTO** (BAT-01, BAT-04) |
| 4 | volts → volts estable | fricción (BAT-03) |
| 5 | volts → porcentaje | **ROTO** (BAT-05, BAT-06) |
| 6 | número → archivo / frame | **ROTO** (BAT-07, BAT-11) |
| 7 | número → nube | fricción (BAT-11) |
| 8 | serie → "cuánto le queda" | **ROTO** (BAT-08, BAT-09, BAT-10, BAT-14) |
| 9 | "queda poco" → alguien actúa | **ROTO** (BAT-12) |

### Los otros hallazgos que no entraron en el TL;DR

- **BAT-07** — el CSV de ráfaga (modo eco) **no tiene columna de batería**.
  `eco.py` lee la batería una vez por ráfaga y la manda **solo por WiFi**. Si la
  campaña fue sin cobertura —el caso que justifica tener SD— la tensión de esas
  horas no existe en ningún lado.
- **BAT-05/06** — **4 curvas** de porcentaje conviven en el repo, con **10
  puntos de spread** a 3,50 V (la misma celda vale 20/22/30/30 %), y **4
  tensiones distintas** significan "se acabó": 3,00 · 3,20 · 3,30 · 3,50. El
  nodo marca `bat_low` en 3,20, **debajo** del corte con el que
  `power-budget.md` calcula los mAh utilizables.
- **BAT-09** — la proyección de autonomía se calcula sobre el historial **en RAM
  del proceso sniffer**: solo se puede estimar de lo que se vio en vivo, que es
  lo que no pasa en una campaña desatendida.
- **BAT-11** — `last_vbat` arranca en `0.0` y no se refresca hasta el primer tick
  de 1 s. El gateway lo descarta dos veces y el análisis lo enmascara; **el
  persistidor de Supabase lo escribe como lectura real**. La curva de descarga
  en la nube arranca cada boot con un pico a 0 V.
- **BAT-02/13** — `nodo.py:94` maneja `WL_GPIO2` como **salida** de "VSYS sense
  enable", cuando el propio repo lo documenta dos veces como la **entrada** de
  VBUS-presente (y el control de modo de la fuente como `WL_GPIO1`). No es un
  descuido de una línea: está fijado como **doctrina** en `DECISIONS.md:125`
  (D-009), `AGENTS.md:151` y `docs/setup-completo.md:60` — y D-009 prohíbe
  explícitamente el pin que el propio `battery.py` del repo usa. Mientras la
  doctrina diga eso, la revisión confirma el código contra el doc en vez de
  contra la placa. **Este es el único que necesita hardware para resolverse.**

### Detalle de contexto que explica parte de todo esto

`firmwares/nodo-gimap/` está en tu árbol de trabajo pero **no está versionado**
(`git status` lo muestra como `??`). Es justo el driver que hace bien las tres
cosas que el de producción hace mal: detecta USB, fuerza el modo PWM de la
fuente antes de medir, y tiene `K_CAL` + una rutina `calibrar()` contra el
tester. Mientras no esté en el repo, nadie lo va a comparar contra `nodo.py`.
El checker degrada limpio sin él (hay un test que copia el repo sin esa carpeta
y verifica que no queden citas fantasma), pero pierde la mitad de la evidencia.
**Decidís vos si va al repo — no lo commiteé.**

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-17-cadena-bateria

# los 70 tests (tarda ~5 s, sin red ni hardware)
python -m unittest tools.test_check_battery_chain

# el informe completo con evidencia
python tools\check_battery_chain.py --detail

# los tres números del TL;DR, uno por comando:
python tools\check_battery_chain.py --demo-lectura      # la columna vbat que nadie lee
python tools\check_battery_chain.py --demo-proyeccion   # el ETA vs la verdad
python tools\check_battery_chain.py --demo-curvas       # las 4 curvas de %
python tools\check_battery_chain.py --demo-umbrales     # los 4 "vacío"
python tools\check_battery_chain.py --demo-cadena       # los 9 eslabones

# exit code: 3 (hay errores). Para CI:
python tools\check_battery_chain.py --json
```

Lo que verifiqué yo, corriendo: **70/70 tests OK**, `py_compile` de los dos
archivos nuevos, los 5 demos, exit code 3, JSON válido, y que **toda cita
`archivo:línea` de cada hallazgo apunta a una línea que existe** (es un test).

## Qué quedó sin verificar por hardware

- **BAT-02 (el pin).** Cuál de los dos es el correcto en tu Pico 2 W se
  resuelve con la placa: medir la batería con el tester y comparar contra lo que
  reporta cada variante. Hasta entonces el hallazgo dice que **el repo se
  contradice a sí mismo**, no cuál de las dos versiones tiene razón.
- **BAT-03 (rizado) y BAT-04 (calibración).** Necesitan osciloscopio y tester.
- **El modelo de descarga de la LiPo** (`lipo_v`) es **un modelo declarado** en
  el código, con puntos de curvas publicadas. Sirve para mostrar el signo y el
  orden de magnitud del error de extrapolar (BAT-10), **no para calibrar nada**.
  La curva real de tu celda sale de una descarga medida — que es, justamente, lo
  que BAT-08 hoy impide hacer con los datos que ya existen.
- No compilé ni flasheé nada. No hacía falta: es todo Python y lectura estática.

## Orden sugerido para arreglarlo (barato y verificable primero)

1. **BAT-08** — agregar `"vbat"` a la lista de columnas de `import_sd_csv`.
   **Una línea**, y desbloquea la medición de autonomía sobre datos que ya
   existen. Ya hay test que lo confirma como arreglo
   (`test_bat08_no_salta_si_el_lector_aprende_el_nombre`).
2. **BAT-07** — columna `vb` en el header de ráfaga de `eco.py`.
3. **BAT-01** — portar `en_usb()` al `Battery` de producción. Sin esto ninguna
   prueba de banco del camino de batería baja es válida.
4. **BAT-05/06** — una sola curva y un solo juego de umbrales, en un archivo,
   importado por todos.
5. **BAT-02/13** — resolver el pin contra la placa y recién ahí reescribir D-009.
6. **BAT-12** — decidir qué hace el nodo con `bat_low`.

Los 1–4 son software puro y se pueden hacer en cualquier momento; **el 1 es de
una línea y es el que más desbloquea** (toca el 🔴 #4 del QUE_FALTA).

## Estado del branch

`nocturno/local-2026-08-17-cadena-bateria` — 2 commits, pusheado a
github.com/matialegre/datalogger. **Pendiente de merge**, para que lo mire
@verificador. No modifica ningún archivo existente salvo `QUE_FALTA.md`.
