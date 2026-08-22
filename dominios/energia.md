# Dominio: ENERGÍA (agente @energia)

Doc de dominio + bitácora. El agente lo lee al arrancar y lo actualiza al cerrar.

## Estado del dominio (nacimiento, 2026-07-07)
- galgas-supabase: deep sleep entre ráfagas OK en banco; falta test con LiPo real (`DEV_BENCH_NO_BATTERY` activo) y presupuesto medido del ciclo wake→POST→sleep.
- RuView: nodos Pico 2 W SIN sleep (ECO-LoRa no implementado; no mandar `eco on` a P1/P2). Falta driver INA219. `docs/power-budget.md` existe en el repo — revisarlo.
- Cosechador: objetivo sleep <5µA (paper: 0.75µA); nada construido.
- Instrumento de medición de consumo: definir (INA219 propio / multímetro de GIMAP / Nordic PPK2 — evaluar compra, GIMAP banca).

## Presupuestos de energía (tabla viva)
| Nodo | Estado | Medido/Estimado | Consumo | Autonomía | Fecha |
|---|---|---|---|---|---|
| (vacío — completar con mediciones reales) | | | | | |

## Bitácora
- 2026-07-07 — Agente creado por Claude Fable con herencia de los 4 proyectos. Próximo paso: definir instrumento de medición y presupuesto del ciclo completo de ESP-A en galgas-supabase.

- 2026-07-08 [BRIEFING GIMAP] — leer ../BRIEFING_EQUIPO_GIMAP.md y los 4 docs (PARTE_GIMAP, PRESUPUESTO_ENERGIA, PROTOCOLO_CALIBRACION, INGENIERIA_NODO_1ANO). Para vos: 8800mAh murió en 1 día (ESP32+WiFi+boost=367mA). Medir sleep PRIMERO. LiSOCl2+supercap+LDO bajo Iq, NUNCA boost. Presupuesto en INGENIERIA_NODO_1ANO/PRESUPUESTO_ENERGIA.

- 2026-08-22 [NOCTURNO] — **RuView/datalogger: una sola curva de batería.** Branch `nocturno/local-2026-08-22-una-sola-curva` (sale de `08-20-rafaga-bateria`; mergear la cadena en orden desde `08-17-cadena-bateria`). Cierra **BAT-05 y BAT-06** de `docs/battery-chain.md`: había 4 conversiones volt→% con **10 puntos de spread** y 4 tensiones de "se acabó" (3,00 / 3,20 / 3,30 / 3,50). Lo concreto para este dominio: **el nodo marcaba `bat_low` en 3,20 V, por debajo del corte de 3,30 V con el que `power-budget.md` cuenta los mAh utilizables** — el aviso llegaba después del daño, y la autonomía del doc y el ETA de la herramienta contestaban preguntas distintas. Ahora `celda.py` es la única fuente: `V_LLENA=4,20` · `V_AVISO=3,50` (avisar) · `V_CORTE=3,30` (0 % y cortar, **el mismo cutoff de `power-budget.md`**) + curva de 7 tramos (no lineal, con meseta). Propagación por `tools/sync_celda.py` (el firmware no puede importar de otra carpeta y el gateway calcula en JS) con drift detectado como **BAT-15**. **Ojo con las autonomías que ya calculaste:** el ETA extrapola hasta 3,30 V y no 3,00 V, así que da menos horas (7,2 → 3,6 h en el test de campaña eco) — es más honesto, no peor. Sigue abierto **BAT-10** (recta sobre una meseta: el error de modelo grande) y **BAT-01** (el firmware no distingue batería de USB, así que en banco lee ~4,7 V y el camino de batería baja nunca se probó). Detalle: `diario/nocturno-local-2026-08-22.md`.
