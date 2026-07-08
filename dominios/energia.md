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
