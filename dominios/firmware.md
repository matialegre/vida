# Dominio: FIRMWARE (agente @firmware)

Doc de dominio + bitácora. El agente lo lee al arrancar y lo actualiza al cerrar.

## Estado del dominio (nacimiento, 2026-07-07)
- galgas-supabase: `ota_wm_pp` v3.6.x, OTA cloud validada (A 0.1.2→0.1.3). PENDIENTE: RX completo (Realtime+LCD+buzzer+gateway HTTP), re-flash B, OTA distinguir A/B.
- RuView: gateway .ino 62KB monolítico (candidato modularizar); nodos MicroPython; benchmark MicroPython vs C/PIO pendiente (decisión datalogger).
- FrioSeguro: v4.0.0 modular (referencia de arquitectura); flasheo de módulos nuevos + SIM800/OTA/NTP en hardware pendiente.
- Lección fundacional: headers huérfanos del legacy — verificar SIEMPRE que el código esté incluido y ejecutándose.

## Versiones flasheadas (tabla viva)
| Placa | Proyecto | Versión | Fecha | Nota |
|---|---|---|---|---|
| ESP-A | galgas-supabase | 0.1.3 (OTA) | pre-2026-07 | cliente nuevo |
| ESP-B | galgas-supabase | vieja | — | RE-FLASHEAR |
| ESP-RX | galgas-supabase | heartbeat-only | — | completar Task 08 |

## Bitácora
- 2026-07-07 — Agente creado por Claude Fable. Próximo paso sugerido: Task 08 del RX (es el bloqueante más grande para octubre).
