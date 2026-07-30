# QUE_FALTA — galgas (sistema Dreyfus, parada de planta OCTUBRE 2026)

> Escrito por Claude Fable 2026-07-07 tras análisis completo. Fuente de verdad del estado: `act.md`. Este archivo se actualiza al completar cada ítem (mover a "Hecho" con fecha y evidencia). Repo: github.com/matialegre/galgas · Cuartel: github.com/matialegre/vida

## 🎯 Definición de "listo para octubre"
Los 3 ESP32 (A, B, RX) con galga física real y LiPo real, corriendo días sin intervención, reportando a Supabase con fallback local, con alertas visibles en el SCADA, OTA por device, e instalables en campo con checklist.

## 🔴 Bloqueantes (sin esto no hay parada)
1. **RX completo** — hoy es heartbeat-only. Falta Task 08: subscriber Realtime + LCD I2C + buzzer + rol gateway HTTP del PLAN v5 (server :80 + PATCH `local_ip` cada 30s). [@firmware + @backend]
2. **Validación con GALGA FÍSICA + INA333** — todo corre con `DEV_SIMULATE_ADC`. Banco real, comparar contra `data/field_captures/` (ground truth, READ-ONLY). Revalidar umbral v_pp>40mV con señal real. [@muestreador]
    - 🔀 **EN BRANCH** `nocturno/local-2026-07-29-vpp-field-characterization` (pendiente de merge): **caracterización offline del v_pp real** en la ventana EXACTA del firmware (500 muestras = 1 s). `tools/analyze_vpp_field.py` (read-only sobre las capturas) + 9 tests + `docs/vpp-field-characterization.md`. Hallazgos: (1) v_pp real **≤14 mV mediana** en toda condición normal → ALERT 40 mV con margen enorme, valida el fix MONITOR=35 mV del 07-28-b; (2) **@firmware** — el self-trigger v3 (1 burst, sin hold) convierte dropouts de 0.0 V en ALERTAS espurias (3.0 % en motor ON, 0 % con guard); legacy tenía `HOLD_SEC=1.5s`. Fix candidato a confirmar en banco. [@muestreador + @firmware]
   - 🐛 **BUG LATENTE detectado (2026-07-16, branch `nocturno/local-2026-07-16-alert-hold-replay`):** el firmware **carga** thresholds de NVS (`esp_a_emisor.ino:220`) y los deja setear por comando cloud (`CMD_SET_THRESHOLDS`), pero la decisión de alerta usa la **constante de compilación** `SELF_TRIGGER_VPP_V=0.040` (`esp_a_emisor.ino:259`) e **ignora `th` entero + no aplica ningún hold** → `set_thresholds` desde la nube es un **no-op** y `hold_sec` (recomendado 2-3 s por el informe §9.2) no existe. [@firmware wire th_v+hold_sec en :259]
   - 🔀 **EN BRANCH** `nocturno/local-2026-07-16-alert-hold-replay` (pendiente de merge): `tools/alert_hold_replay.py` (stdlib, READ-ONLY) replaya las 12 capturas reales agregando la **dimensión temporal** (hold de N bursts) — complementa el vpp-audit del 07-11 (que barre el valor del umbral). **Hallazgos:** reposo puro = 0 espurias sin hold (40mV seguro); el falso positivo de motor del canal B es **sostenido** (racha 30) → el hold 2-3s del §9.2 es **necesario pero NO suficiente** para B (hace falta el fix de umbral/front-end de B del 07-11); un hold=3 casi no toca la rotura real (reposo_1: 93/97 alertas, +2 bursts de latencia). `tools/test_alert_hold_replay.py` = **30 tests OK**. Doc: `docs/alert-hold-replay.md`. Ver `MATI-HQ/diario/nocturno-local-2026-07-16.md`.
3. **Test con LiPo REAL** — sacar `DEV_BENCH_NO_BATTERY` (hoy finge 4.0V). Presupuesto de energía medido del ciclo completo wake→muestreo→POST→sleep. [@energia]
4. **Re-flashear ESP-B** con el cliente nuevo (A ya está en 0.1.3 vía OTA; B quedó atrás). [@firmware]

## 🟡 Importantes (hacen la diferencia en campo)
5. OTA que distinga A/B en `firmware_versions` (hoy comparten target `emisor`). [@backend + @firmware]
6. Bucket `firmware` con URL firmada + TTL (hoy PÚBLICO — hueco de seguridad). [@backend]
7. Fix brownout en boot por USB underpower. [@hardware]
8. Migración SQL de columnas nuevas pendiente de correr. [@backend]
9. **Integrar mockup SCADA `redler/`** al dashboard `web/` — la cara que Dreyfus ve. [@frontend + @diseno]
    - ⚠️ **DRIFT: la integración YA ESTÁ HECHA** — `web/src/views/PlantaView.jsx` ("copia fiel del mockup, conectado a Supabase real") montado en `App.jsx` (pestaña Planta) con `redler.css`. Lo que faltaba era un afinado.
    - 🔀 **EN BRANCH** `nocturno/local-2026-07-28-b-scada-monitor-threshold` (pendiente de merge): corrige un **cry-wolf** del SCADA — `TH_VPP_MONITOR` estaba en 20mV, por DEBAJO del vpp de reposo documentado (~30mV, `config.h`) → cards en ámbar "MONITOREO" permanente en operación normal. Subido a 35mV (30mV reposo + 1σ ruido, 5mV bajo el ALERT de 40mV); la lógica de ALERTA no se toca. Verificado offline: `web/ npm run build` OK. **Falta (campo):** validar el borde exacto contra `data/field_captures/` con señal real de galga. [@muestreador + @diseno]
10. Prueba de resistencia 24-48h con cortes de WiFi/energía inducidos; verificar NVS conserva calibración tras power-cycle. [@verificador]
11. Robustez WiFi de planta: reconexión, canal, comportamiento con AP caído → fallback directo a Supabase (validar el híbrido PLAN v5 punta a punta). [@comms]

## 🟢 Para cerrar prolijo
12. Montaje de campo: enclosures/fijación al equipo, prensacables, checklist de instalación con fotos. [@hardware]
13. `CONTEXTO_USO_REAL.md` completarlo (bloquea features de UX según el CLAUDE.md del repo).
14. Docs raíz desactualizadas vs act.md — sincronizar (el README miente sobre el estado). [@cronista]
15. Definir con GIMAP/Dreyfus: FECHA exacta de la parada, lugar, quién va. [MATÍAS]

## Lecciones ya pagadas (no repetir)
- TLS: cert **GTS Root R4** + HTTPClient simple. NO reabrir (debug completo en docs/).
- mDNS descartado por flakey. Migraciones append-only. Paths sin espacios (por eso vivís en C:\Proyectos\galgas).

## Hecho
- 2026-07-07 — Migrado a C:\Proyectos\galgas + GitHub privado (1007 archivos, field_captures con backup por primera vez).
