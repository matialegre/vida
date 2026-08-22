# Nocturno local — 2026-08-22

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (P0 — terminarlo antes del trabajo Dreyfus).
**Branch:** `nocturno/local-2026-08-22-una-sola-curva` (pusheado, `2a126b9`).
**Sale de:** `nocturno/local-2026-08-20-rafaga-bateria` → **mergear la cadena en orden**:
`08-17-cadena-bateria` → `08-18-b-lector-campana` → `08-20-rafaga-bateria` → este.

## TL;DR

> **El aviso de batería baja llegaba después del daño.**

El datalogger, las galgas y FrioSeguro comparten la misma pregunta: *¿cuánta
batería le queda al nodo y quién se entera a tiempo?* La auditoría del 08-17 la
dejó anotada como BAT-05 y BAT-06 y nadie la había tocado, porque no es un bug
de una línea: es que **el repo tenía cuatro opiniones distintas sobre la misma
celda**.

**Las curvas.** Cuatro conversiones volt→porcentaje, con **10 puntos de spread**
sobre la misma celda:

| curva | dónde | % a 3,50 V |
|---|---|---|
| tramos, 7 puntos | `battery.py` | 20 |
| lineal 3,30–4,20 | `nodo-gimap/bateria.py` | 22 |
| lineal `battery_low_v`–`battery_full_v` | `pico2w-node/nodo.py` | 30 |
| lineal `VEMPTY`–`VFULL` | gateway ESP32 | 30 |

El "queda 20 %" —el número con el que se decide ir a cambiar la batería— caía
entre 3,40 y 3,50 V según a quién le preguntaras. Y esa franja es justo el codo
de la LiPo, donde el tiempo restante cambia rápido.

**Los umbrales.** Cuatro tensiones significaban "se acabó": **3,00** (el 0 % de
`battery.py` y el `v_empty` del ETA) · **3,20** (`battery_low_v`, `VEMPTY`) ·
**3,30** (`V_CORTE`, `VLOW`, y el cutoff con el que `power-budget.md` calcula los
mAh utilizables) · **3,50** (`V_AVISO`).

Lo grave está en comparar dos de esos números: el nodo marcaba `bat_low` en
**3,20 V**, que es **por debajo** del corte de 3,30 V. Para cuando el sistema
avisaba, la celda ya estaba en la zona donde se arruina.

## Qué hice

**`celda.py`** en la raíz: la curva y los dos umbrales, y nada más.

| | valor | quién lo usa ahora |
|---|---|---|
| `V_LLENA` | 4,20 V | 100 % de la curva |
| `V_AVISO` | **3,50 V** | `bat_low` del nodo (default de `battery_low_v`, era 3,20) · `VLOW` del gateway |
| `V_CORTE` | **3,30 V** | 0 % de la curva · `VEMPTY` del gateway · `v_empty` del ETA (era 3,00) · cutoff de `power-budget.md` |
| `CURVA` | 7 tramos | los cuatro consumidores |

La curva elegida es la de tramos que ya estaba en `battery.py` (la **única
no-lineal**, que es lo que corresponde a una descarga con meseta), con el extremo
inferior re-anclado de 3,00 V a `V_CORTE`. Arriba de 3,40 V **da exactamente lo
mismo que antes** —3,50 V sigue siendo 20 %— y abajo del corte da 0 en vez de un
7 % que no se puede usar. Sigue siendo **un modelo declarado, no una
calibración**: calibrarlo pide una campaña de descarga real, que es justo lo que
los arreglos del 08-18-b y el 08-20 recién ahora dejan grabado en la SD.

**El problema que hacía difícil esto** (y por lo que no era un fix de una línea):
los cuatro consumidores están en **tres runtimes** y **ninguno puede importar** el
archivo. MicroPython flashea el contenido de UNA carpeta; el gateway calcula el
porcentaje en el JavaScript embebido en el `.ino`. Entonces:

- **`tools/sync_celda.py`** copia `celda.py` byte a byte a las carpetas de
  firmware y **genera** el bloque JS del gateway entre `/*CELDA-INI*/` y
  `/*CELDA-FIN*/`.
- `--check` no escribe nada y falla si algo quedó viejo.
- El checker de la cadena lo corre en **cada pasada** y lo reporta como
  **BAT-15**. Ése es el seguro: sin él, "una sola fuente de verdad" dura hasta el
  primer cambio.

De paso, `battery_full_v` **sale del schema de config**: existía sólo para
dibujar una recta que ya no existe. Queda un único ajuste por nodo,
`battery_low_v`, con default `V_AVISO`.

**Efecto lateral que conviene mirar:** el ETA ahora extrapola hasta 3,30 V en vez
de 3,00 V, así que **da menos horas** (en el test de campaña eco pasó de 7,2 h a
3,6 h). No es que el ETA haya empeorado — antes contaba como disponible una
franja en la que el nodo debería estar apagado. **BAT-10** (ajustar una recta
sobre una meseta) sigue abierto y es el error grande que queda ahí.

**Resultado en el checker:** de 10 hallazgos a **8**; el eslabón 5
(*volts → porcentaje*) pasa de **ROTO a OK**. Quedan 3 eslabones rotos (eran 4).

## Cómo verificarlo (sin hardware, todo en 10 s)

```
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-22-una-sola-curva

python tools/test_celda.py                  # 14 tests nuevos: la curva y su propagacion
python tools/test_check_battery_chain.py    # 76 (eran 73)
python tools/test_eco_battery.py            # 26
python tools/test_import_sd_csv.py          # 25

python tools/sync_celda.py --check          # exit 0 = las copias estan al dia
python tools/check_battery_chain.py --demo-curvas    # las 5 curvas, y quien delega
python tools/check_battery_chain.py --demo-umbrales  # [aviso] TODOS 3.50 / [corte] TODOS 3.30
```

Para ver el seguro funcionando: agregá una línea a
`firmwares/pico2w-node/celda.py`, corré el checker (aparece **BAT-15**, el
eslabón 5 vuelve a ROTO), y arreglalo con `python tools/sync_celda.py`.

El JS del gateway lo verifiqué evaluándolo con node contra la curva de Python
(quedó también como test en `test_celda.py`).

## Qué quedó sin verificar

- **Nada en este cambio requiere hardware** — es todo modelo y propagación. Pero
  lo que el cambio *habilita* sí: el número que la placa mide sigue sin
  distinguir batería de USB (**BAT-01**, abierto), así que en banco lee ~4,7 V y
  satura en 100 %. Mientras eso siga, el camino de batería baja no se puede
  probar de verdad.
- **El sketch del ESP32 no se compiló** (no hay toolchain Arduino/ESP32 acá y
  bajarlo era clavar la noche — lección del 07-07). El cambio está **dentro del
  `<script>` del HTML embebido**, o sea es una string literal para el compilador:
  ningún símbolo C++ cambió (verificado con grep — `VLOW`/`VEMPTY`/`VFULL`/`pct`
  se usan sólo entre las líneas 627 y 856, que son el `<script>`). Comando para
  confirmarlo de día:
  `arduino-cli compile --fqbn esp32:esp32:esp32s3 firmwares/esp32s3-com11/esp32_dashboard`
- ⚠️ **`firmwares/nodo-gimap/bateria.py` NO viaja en el branch.** Esa carpeta no
  está versionada (tiene `secrets.py`). El cambio está aplicado **en el disco de
  esta PC**; si alguna vez versionás la carpeta —o si flasheás ese nodo desde
  otra máquina— acordate de llevar también `firmwares/nodo-gimap/celda.py`.
- Las carpetas `firmwares/pico2-lora-com10`, `pico2w-wifi-com13`,
  `pico2w-eco-com14` y `pico/` son snapshots viejos por puerto COM y **siguen con
  la curva lineal vieja**. No las toqué (no son las que se flashean hoy), pero
  `sync_celda.py` las **lista en cada corrida** para que ese drift sea visible en
  vez de silencioso.

## Decisión que quedó escrita

`DECISIONS.md` → **D-018 — Una sola celda**. Incluye el "por qué no un paquete
importable" (tres runtimes, cero imports posibles entre ellos) para que la
próxima sesión no intente rehacerlo de otra forma y descubra el mismo muro.

## Lo que sigue en esta cadena

Del orden sugerido en `docs/battery-chain.md`, quedan:

1. **BAT-01** — portar `en_usb()` al `Battery` de producción. Es el que desbloquea
   *probar* el camino de batería baja. Software puro, se puede hacer de noche,
   pero **no se puede verificar sin placa**.
2. **BAT-12** — decidir qué hace el nodo con `bat_low` (hoy: nada). Es una
   decisión tuya, no del worker: ¿se apaga, avisa por RV1, o las dos?
3. **BAT-02 / BAT-13** — el pin. Necesita hardware y reescribir la doctrina D-009.

## Archivos

Nuevos: `celda.py` · `firmwares/pico2w-node/celda.py` (copia) · `tools/sync_celda.py` · `tools/test_celda.py`

Tocados: `battery.py` · `firmwares/pico2w-node/nodo.py` · `firmwares/pico2w-node/config.py` · `firmwares/esp32s3-com11/esp32_dashboard/esp32_dashboard.ino` · `pc-sniffer/analysis.py` · `tools/check_battery_chain.py` · `tools/test_check_battery_chain.py` · `tools/test_eco_battery.py` · `docs/battery-chain.md` · `DECISIONS.md` · `README.md` · `QUE_FALTA.md`

Fuera del branch (no versionado): `firmwares/nodo-gimap/bateria.py` + `celda.py`
