# Nocturno LOCAL — 2026-07-16 (worker de la PC, Matías durmiendo)

## Tarea elegida y por qué
**galgas #2/#3 — replay del HOLD/debounce de la alerta del emisor contra señal real
+ destape de un BUG LATENTE de config.** Octubre (prioridad #2), READ-ONLY sobre
datos sagrados, verificable 100 % offline, aditivo.

Recorrí los 4 `QUE_FALTA`, los nocturnos previos (07-10→07-15) y el estado real de
**todas** las branches. Lo que ordenó la decisión:
- **Todos los bloqueantes "obvios" ya tienen branch, en los 4 repos.** galgas: RX
  (`rx/task08-completo`), SCADA redler (`web/scada-redler`), OTA A/B bucket
  (`backend/ota-ab-bucket-firmado`), energy-budget (07-15), vpp-audit (07-11).
  datalogger: ina219/ecolora (07-07/08), sd-integrity (07-09 y 07-15), rssi (07-10).
  FrioSeguro: 5 branches sin mergear (deuda de **deploy**, no de código — avisado ya
  7 noches). cosechador: P2, todo gated por compra (nada de software esta noche).
  ⇒ No había fruta baja sin tocar; **había que encontrar algo nuevo de verdad**.
- Leyendo el firmware real para el vpp/energy encontré un **hueco que nadie modeló**:
  el emisor v3 **carga** `th_v/th_r/hold_sec` de NVS y los deja setear por comando
  cloud, pero **la alerta usa una constante de compilación e ignora `th` entero, y
  no aplica ningún hold temporal**. El informe de campo (§9.2) pide `HOLD 2-3 s` en
  producción y eso **nunca se validó contra los datos reales**.
- Elegí esto porque: (1) es un **bloqueante de octubre** (config de alerta correcta
  antes de la parada), (2) es la **dimensión temporal** que le faltaba al vpp-audit
  del 07-11 — complementa, no duplica, (3) destapa un **bug de correctness** real
  (comando cloud que es no-op), (4) converge con **Medidas 2** y **SCI** (uni = #1).

Encaja con "UNA tarea bien hecha por noche" y no estaba en ningún branch.

## El bug latente (correctness, para octubre) — evidencia con file:línea
| Evidencia | Qué |
|---|---|
| `firmware/shared/types.h:98` | `thresholdsDefault` → `th_v=0.040, th_r=0.60, hold_sec=1.5` |
| `firmware/esp_a_emisor/esp_a_emisor.ino:220` | `Thresholds th; nvsLoadThresholds(th);` — se **carga** de NVS |
| `firmware/esp_a_emisor/command_handler.cpp:94` | `CMD_SET_THRESHOLDS` — el comando cloud **persiste** th |
| `firmware/esp_a_emisor/esp_a_emisor.ino:259` | `self_alert = (r.v_pp > SELF_TRIGGER_VPP_V)` — decide con **constante**, NO con `th` |

⇒ Setear thresholds desde la nube con `set_thresholds` **no tiene efecto** (la alerta
sigue clavada en `SELF_TRIGGER_VPP_V=0.040`), y **no hay hold** (`hold_sec` no se usa).

## Qué hice — branch `nocturno/local-2026-07-16-alert-hold-replay`
Sale de `main`. Software **aditivo** (2 archivos nuevos + 1 doc + 1 nota en
QUE_FALTA). No toqué firmware, ni datos, ni schema, ni `data/field_captures/`
(sagrado; lo **leí** en read-only, nunca lo modifiqué).

| Archivo | Qué |
|---|---|
| `tools/alert_hold_replay.py` | Replaya cada captura real como secuencia de bursts (una fila ≈ un burst de ~50 muestras), recalcula `v_pp=max−min` como el firmware, y compara la política **actual** (`v_pp>umbral`, sin hold, N=1) contra un **HOLD de N bursts consecutivos**. Reporta por archivo/canal: bursts, over, alerts, latencia (1er ALERTA en bursts), racha máxima. `--th-v/--hold-bursts/--channel/--baseline/--sweep-hold/--json`; exit 0/1/2 (gate de CI: baseline que no debe alertar). **Reusa** los 2 helpers ya probados del vpp-audit del 07-11 (`extract_first_json`, `block_vpp`). Stdlib puro. |
| `tools/test_alert_hold_replay.py` | **30 tests** unittest sobre bursts sintéticos: parseo (raw_json sin comillas, llaves en strings), `v_pp`, política de hold (aislado vs sostenido, hueco de datos que corta racha, `>` estricto, monotonía "más hold nunca más alertas"), I/O de CSV sintético, reporte, exit codes, JSON. **No toca las capturas reales.** |
| `docs/alert-hold-replay.md` | El bug con file:línea, qué hace, uso, los 4 hallazgos, recomendación para octubre, qué NO modela (cadencia de wake de v3), convergencia UTN. |
| `QUE_FALTA.md` (galgas) | #2 → nota del bug + branch con el resumen. |

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-16-alert-hold-replay
python -m unittest tools.test_alert_hold_replay -v      # -> Ran 30 tests ... OK
python tools/alert_hold_replay.py data/field_captures/                    # política actual
python tools/alert_hold_replay.py data/field_captures/ --hold-bursts 3    # con hold
python tools/alert_hold_replay.py data/field_captures/ --channel both --sweep-hold 1,2,3,5,10,30 \
    --baseline "galgas_20260213_131538.csv" --baseline "galgas_20260213_131637.csv" \
    --baseline "galgas_20260213_132005.csv" --baseline "galgas_20260213_132130.csv"
```
**Resultado obtenido esta noche** (Python 3.14.3): `unittest` → **30/30 OK** (0.04 s).
CLI coherente y verificable a mano (un test replica: racha de 4 con hold=3 → 2 alertas,
1er en el 3er burst). Corrida real sobre las 12 capturas del REDLER, ver hallazgos.

## Hallazgos que salen de los datos reales (para @firmware / @muestreador)
1. **En reposo puro, 0 espurias incluso sin hold.** Las 4 verificaciones post-offset
   + los 2 monitoreos finales → 0 alertas en ambos canales, hold 1..30. El umbral de
   40 mV es seguro en reposo; **el hold no es lo que protege el reposo.**
2. **El falso positivo de motor del canal B es SOSTENIDO, no aislado.** `133045`
   ("motor estable", 0 roturas) dispara B **50 veces en una racha de 30 bursts**. Un
   hold de 3 sólo saca 4 (50→46); hay que llegar a hold≈30 para bajarlo a 1. ⇒ **La
   recomendación §9.2 de "2-3 s de hold" es necesaria pero NO suficiente para B**: el
   debounce es la palanca equivocada para un sesgo sostenido; hace falta el fix de
   umbral/front-end de B que ya identificó el vpp-audit del 07-11.
3. **Un hold modesto es seguro barato y casi no toca la rotura real.** En `reposo_1`
   (evento real **CADENA B ROTA** a las 13:02), hold=3 conserva 93-94 de 97-98 alertas
   y la latencia sólo pasa de burst 81 → 83 (+2 bursts). Poner hold=2-3 no pierde nada
   en eventos reales; simplemente no resuelve el problema de B.
4. **v_pp ≠ alerta diferencial del RX.** El ensayo principal `134127` (1 cadena
   desconectada) dispara sólo en B por v_pp (A=0): una desconexión no siempre da pico
   de v_pp. Cruce informativo, no la spec del RX (`dV=|vA−vB|`/`TH_R`) — igual que el 07-11.

**Recomendación octubre:** (a) cablear `th.th_v` + `th.hold_sec` en `esp_a/b_emisor.ino:259`
para cerrar el no-op del comando cloud; (b) sumar un hold chico (2-3 bursts) como seguro
barato; (c) NO esperar que el hold solo arregle B → combinar con el fix de umbral/front-end
de B del 07-11.

## Qué quedó SIN verificar (necesita banco/hardware)
- **Cadencia de wake de v3.** Un "burst" del replay = una fila del CSV (logging
  continuo del RX legacy). El hold en v3 se aplica sobre **wakes de deep sleep**
  (60 s VIGILADO / 10 s ALERTA), no sobre filas de 500 Hz. El replay da el eje
  temporal **relativo** (aislado vs sostenido), no el hold en segundos — mapear
  `hold_bursts`→`hold_sec` necesita la cadencia real.
- **Aplicar el fix en firmware** (cablear th_v+hold_sec en :259) y re-verificar en
  banco: eso lo hace @firmware con hardware. Esta noche es el marco + la evidencia,
  no el cambio de firmware (riesgoso sin banco).
- **Señal de galga física nueva** (QUE_FALTA #2): las capturas son de feb-2026; el
  banco real puede mover la estadística de v_pp.

## Reglas respetadas
Nada borrado. No toqué firmware, ni schema, ni datos, ni `data/field_captures/`
(READ-ONLY sagrado — sólo lectura, nunca escritura), ni migraciones. No mDNS (no
aplica). No hay secretos en el código. No stageé `__pycache__/` (gitignored).
Verificación instantánea (Python puro, 0.04 s) — sin compilación pesada, sin
timeouts. El branch **no se mergea** hasta @verificador; es aditivo, READ-ONLY sobre
lo sagrado, y los 30 tests pasan.

## Branch
`nocturno/local-2026-07-16-alert-hold-replay` (pusheado a origin, 1 commit `2ee6552`;
sale de `main`).

## Notas para el @director / @verificador / @firmware / @muestreador / @cronista
- **Patrón sostenido, hallazgo nuevo:** 4ª herramienta de análisis stdlib de la serie
  (rssi 07-10, vpp 07-11, energy 07-15, hold 07-16) — pero esta **destapa un bug de
  correctness** (config cloud muerta), no sólo caracteriza. Todas READ-ONLY sobre lo
  sagrado, todas convergen con la uni.
- **Encadenamiento con el 07-11 y el 07-15:** el vpp-audit dio el *valor* del umbral,
  este dio el *eje temporal*, el energy-budget dio el *costo en batería* de cada
  alerta. Los tres apuntan a la misma acción de banco: fijar la config de alerta de B
  (umbral asimétrico + hold + medir su costo energético) antes de octubre.
- **Sigue en pie la sugerencia repetida (8ª noche):** agrupar un **bloque de día de
  ~1 h para bajar la pila de FrioSeguro** (5 branches) — es deploy/merge, no código.
  El worker no lo toca de noche a propósito.
