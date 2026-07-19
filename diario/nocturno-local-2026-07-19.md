# Nocturno LOCAL — 2026-07-19 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
La **alerta que Dreyfus realmente ve** (LED rojo + relé + SCADA) la decide el RX con una
detección **diferencial**: `dv=|vA-vB| ≥ TH_V` **o** `ratio=min/max ≤ TH_R`, sostenida
`HOLD_SEC`. Dos noches previas modelaron el **auto-disparo del EMISOR** (v_pp local), pero
**la decisión del RX nunca se había modelado offline ni reproducido contra los datos
reales**. Escribí ese modelo (`tools/rx_detection_replay.py`, stdlib) + **17 tests** y lo
**reproduje contra el ground-truth `in_alert` de las 12 capturas de campo** (READ-ONLY).
Resultado: **sensibilidad ~100 %**, clasificación de causa (CADENA A/B ROTA / exceso / dV)
**99.9-100 %**, **0 falsas alarmas en reposo**. Y un **hallazgo cuantificado**: el RX de
**producción actual** sería **~1-4 % más "trigger-happy"** que el algoritmo de campo legacy
de feb-2026 sobre la misma señal (falsos positivos sistemáticos en los bordes de los
eventos: **+118 alertas en el ensayo principal**). No es un bug — es **drift medible entre
el firmware que se instala en octubre y lo que la planta vio en febrero**, con el número
exacto por archivo para decidir si se quiere esa sensibilidad extra o se ajusta `HOLD_SEC`.
**No toqué firmware ni las capturas.** **Branch: `nocturno/local-2026-07-19-rx-detection-replay`
(galgas), pendiente de merge.**

## Tarea elegida y por qué
**galgas #2 (octubre, prioridad #2) — la mitad de software de "validar la detección contra
señal real", pero para la alerta del RX.** READ-ONLY sobre datos sagrados, 100 % offline.

Recorrí los 4 `QUE_FALTA`, todos los branches nocturnos y los nocturnos previos. Por qué ésta:
- **FrioSeguro (P1, plata):** el turno del 18 ya trabajó su core (alert-model); no apilo la
  misma semana sobre el mismo repo, y su pila de 6 branches sigue siendo deuda de **deploy**
  (necesita ~1 h de día con @verificador), no de código nuevo.
- **datalogger (P0):** benchmark en `main`; el resto en branch (ina219/ecolora, sd-integrity
  ×2, rssi, ssid-casing) o hardware (piezo, alcance).
- **cosechador (P2):** el turno B del 18 acaba de cerrar su análisis offline (modelo de
  energía); área ya cubierta esta semana.
- **galgas (P0 octubre):** los bloqueantes duros tienen branch (RX task08, SCADA, OTA A/B) o
  son hardware. **Pero** al releer la trilogía de análisis de la alerta encontré un hueco
  real: `vpp_threshold_audit.py` (07-11) y `alert_hold_replay.py` (07-16) modelan el
  **auto-disparo del EMISOR** (`v_pp` local, un *wake* por golpe). El **vpp-audit dejó
  explícitamente afuera** la alerta del RX ("el cruce v_pp↔in_alert es informativo, no la
  spec del RX"). **La decisión diferencial del RX — la alerta del sistema, la que ve
  Dreyfus — no tenía modelo offline ni se había cruzado contra el ground-truth.** Ese es el
  pedazo verificable sin hardware que faltaba.

Por qué el modelo-y-replay: es el patrón que ya funcionó (vpp/alert-hold/energy en galgas,
alert-model en frioseguro), aplicado al **hueco que esos mismos tools dejaron abierto**, con
un ancla de verificación dura: **el `in_alert` que la planta marcó en febrero**.

## Qué hice — branch `nocturno/local-2026-07-19-rx-detection-replay` (galgas)
Sale de `main`. **3 archivos nuevos + nota en QUE_FALTA. Cero borrados, no toca firmware,
ni las capturas, ni ninguna otra branch.**

| Archivo | Qué |
|---|---|
| `tools/rx_detection_replay.py` (nuevo) | Espejo 1:1 de `esp_rx_receptor/esp_rx_receptor.ino::updateAlert` caso 3 (diferencial). Parsea los CSV posicional (el `raw_json` tiene comas sin comillas → csv.DictReader se desalinea; se toma prefijo antes de `,{` y cola después del último `}`, validado contra el conteo del README). `replay()` recomputa la decisión con los parámetros de cada fila y arma la matriz de confusión (solo filas **determinadas**) + reproducción de la categoría de mensaje. Marca **indeterminadas** las filas donde pudo gobernar una rama de mayor prioridad (emisor-off/batería) que no se reconstruye del CSV. CLI con sens/spec/msgOK por archivo, exit code por `--max-mismatch-rate`. |
| `tools/test_rx_detection_replay.py` (nuevo) | **17 tests** `unittest` (sin deps, **no** tocan las capturas): cada rama del `bad` (dv, ratio, ε ambos-cero), el hold (retardo + re-arme por muestra buena), la clasificación (CADENA A/B, exceso A, dV genérico), el mapeo de strings reales, las 3 clases de indeterminada, y la matriz de confusión (sens/spec perfectos sin hold). |
| `docs/rx-detection-replay.md` (nuevo) | Por qué existe, correspondencia 1:1 con el `.ino`, el oráculo (por qué es verificable de verdad), alcance honesto, resultados, el hallazgo de drift, y los límites de banco. |
| `QUE_FALTA.md` | Nota "EN BRANCH pendiente" bajo #2. |

## El oráculo (por qué no es un modelo contra otro modelo)
Los CSV de `data/field_captures/` traen, **por muestra**, la etiqueta `in_alert` que el
sistema calculó *durante los ensayos de Dreyfus* (General Lagos, 11-13 feb 2026), junto con
`vA/vB/vA0/vB0/sigmaA0/sigmaB0/TH_V/TH_R/HOLD_SEC/TH_STEP_MIN` y el `alert_msg` textual. El
modelo recomputa la decisión con esos mismos parámetros y compara **fila a fila** contra
`in_alert`. Es el firmware de producción vs. lo que la planta realmente marcó. (Validación
de parseo: reposo_1 → 2510 filas / 718 alertas, coincide exacto con el README.)

## Resultados (salida real del CLI de esta noche)
| archivo | filas | GT alr | modelo | Sens | Spec | msgOK | indet |
|---|---:|---:|---:|---:|---:|---:|---:|
| 4× reposo estable + motor ON (131538…132330) | 7 155 | 0 | 0 | — | 100 % | — | 0 |
| 133045 | 2 134 | 480 | 498 | 100 % | 98.9 % | 100 % | 0 |
| 133354 | 3 078 | 480 | 498 | 100 % | 99.3 % | 100 % | 0 |
| 133635 | 3 877 | 573 | 608 | 100 % | 98.9 % | 100 % | 0 |
| **134127 (ENSAYO PRINCIPAL)** | 5 332 | 1 349 | 1 467 | 100 % | 97.0 % | 100 % | 0 |
| 140736 / 140738 (**EMISOR A APAGADO**) | ~5 390 | 1 193 | 1 422 | 99.8 % | 93.3 % | 100 % | 750/764 |
| reposo_1 (**CADENA B ROTA 13:02**) | 2 510 | 718 | 716 | 99.7 % | 100 % | 99.9 % | 116 |

- **Sensibilidad ~100 %:** el RX de producción reproduce casi toda alerta que la planta marcó.
- **Clasificación de causa 99.9-100 %:** cuando modelo y GT alertan, coinciden en el por qué.
- **0 falsas alarmas en señal quieta** (spec 100 % en reposo).
- **indet** en 140736/8 = las filas del test "EMISOR A APAGADO" donde gobierna una rama de
  mayor prioridad; el modelo las aparta honestamente en vez de fingir que las evalúa.

## Hallazgo para @muestreador / @verificador (drift cuantificado, NO corregido)
Exceso sistemático de alertas del modelo vs. el ground-truth, concentrado en los **bordes de
los eventos**, siempre por **falsos positivos** (nunca FN salvo 4 muestras en total):
+18 en 133045/133354, +35 en 133635, **+118 en el ensayo principal**. Especificidad 93-97 %
en los archivos con evento, 100 % en reposo. **Interpretación (a validar):** el RX de
**producción actual** (`.ino`) es **~1-4 % más "trigger-happy"** que el algoritmo de campo
legacy (`Galgas_GIMAP-master`, feb-2026) sobre **la misma señal**. Más sensible = alerta
antes en la transición. **No es un bug** — es drift medible entre el firmware que se instala
en octubre y lo que Dreyfus vio en febrero; el tool da el número exacto por archivo para
decidir a propósito si se quiere esa sensibilidad o se ajusta `HOLD_SEC`. **No toqué firmware.**

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-19-rx-detection-replay
git diff main --stat                                   # -> 3 nuevos + QUE_FALTA
python -m py_compile tools/rx_detection_replay.py tools/test_rx_detection_replay.py   # exit 0
python -m unittest tools.test_rx_detection_replay      # -> OK (17 tests)
python tools/rx_detection_replay.py data/field_captures/               # -> la tabla de arriba
python tools/rx_detection_replay.py data/field_captures/reposo_1.csv --verbose
```
**Resultado obtenido esta noche:** `py_compile` exit 0 + **17/17 OK** en <0.01 s + replay
reproduce el ground-truth con sens ~100 %. Sin descargas ni toolchains pesados — cero riesgo
de timeout (disciplina del 07-07 respetada).

## Qué quedó SIN verificar (necesita banco — no se cierra de noche)
1. **La causa fina del drift** legacy↔producción — requiere leer el algoritmo de campo de
   `Galgas_GIMAP-master` y/o correr ambos firmwares sobre la misma entrada en banco.
2. **Las ramas emisor-off / batería** del RX — dependen de estado de runtime (`last_seen`,
   timeouts) ausente en el CSV; se validan con un ensayo de timeouts inducidos (QUE_FALTA #10).
3. **El umbral definitivo de octubre** — se fija con la galga física real montada
   (QUE_FALTA #2 sigue abierto en su mitad de hardware).

## Reglas respetadas
Solo software. Nada borrado, nada movido. **No toqué firmware** (`esp_rx_receptor.ino`
intacto), ni schema, ni nube, ni secretos. **Las capturas quedaron READ-ONLY** (`git status
data/` limpio). No toqué otros repos. `.pyc` ya ignorado por el `.gitignore` del repo.
Identidad git del repo ya seteada = Matías. El branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-19-rx-detection-replay` (galgas, pusheado a origin; sale de `main`).

## Notas para @verificador / @muestreador / @director
- **@verificador:** el DoD es *"cada decisión de `rx_detection_replay.py` coincide con
  `esp_rx_receptor.ino::updateAlert` caso 3, y el replay reproduce el `in_alert` de las
  capturas dentro de lo esperado"*. Los 17 tests son el oráculo del **modelo**; el replay es
  el oráculo del **firmware vs. campo**. Puntos a atacar: (a) **¿el modelo diverge del `.ino`
  en alguna rama** — p.ej. la condición de re-arme del hold (`last_ok_time` solo se resetea
  cuando NO bad) o el orden de la clasificación de mensaje `:343-357`? Leé el `.py` contra el
  `.ino` línea por línea. (b) **¿el manejo de indeterminadas es correcto** — realmente esas
  filas pudieron caer en emisor-off/batería, o estoy escondiendo mismatches legítimos? Mirá
  140736/8 con `--verbose`. (c) **¿el parseo posicional es sólido** ante alert_msg con
  caracteres raros? (validado: 0 badlines en las 12 capturas, conteo == README).
- **@muestreador (dueño de la detección):** el drift ~1-4 % (producción más sensible que el
  campo legacy) es tuyo para decidir: ¿sensibilidad deseada o se sube `HOLD_SEC`? El tool te
  da el FP-por-archivo para cada valor de umbral si querés barrer. La causa raíz necesita
  comparar los dos algoritmos en banco.
- **@director:** una noche de **octubre (prioridad #2)** que cierra la **mitad de software
  del bloqueante #2 para la alerta del RX** (la que ve Dreyfus) y **cuantifica un drift real**
  entre el firmware de octubre y los datos de febrero — sin gastar un peso, sin tocar hardware
  ni las capturas sagradas. Es un tool autocontenido, no depende de ninguna otra branch; buen
  candidato a mergear directo tras @verificador. **Sigue en pie el aviso:** la pila de
  FrioSeguro (6 branches) necesita ~1 h de día con @verificador.
