# QUE_FALTA — galgas (sistema Dreyfus, parada de planta OCTUBRE 2026)

> Escrito por Claude Fable 2026-07-07 tras análisis completo. Fuente de verdad del estado: `act.md`. Este archivo se actualiza al completar cada ítem (mover a "Hecho" con fecha y evidencia). Repo: github.com/matialegre/galgas · Cuartel: github.com/matialegre/vida

## 🎯 Definición de "listo para octubre"
Los 3 ESP32 (A, B, RX) con galga física real y LiPo real, corriendo días sin intervención, reportando a Supabase con fallback local, con alertas visibles en el SCADA, OTA por device, e instalables en campo con checklist.

> ⚠️ **LEER ANTES DE TOCAR FIRMWARE: `docs/ESTADO_FIRMWARE.md`** (2026-07-17). El emisor de
> producción es **`firmware/ota_wm_pp/ota_wm_pp.ino` (3.6.5)**, NO `firmware/esp_a_emisor/`
> (0.8.1, **linaje retirado el 27-abr por el PLAN v5**). Varios ítems de acá abajo se
> escribieron contra el sketch retirado — corregidos abajo con 🔀.

## 🔴 Bloqueantes (sin esto no hay parada)
1. **RX completo** — hoy es heartbeat-only. Falta Task 08: subscriber Realtime + LCD I2C + buzzer + rol gateway HTTP del PLAN v5 (server :80 + PATCH `local_ip` cada 30s). [@firmware + @backend]
2. **Validación con GALGA FÍSICA + INA333** — todo corre con `DEV_SIMULATE_ADC`. Banco real, comparar contra `data/field_captures/` (ground truth, READ-ONLY). Revalidar umbral v_pp>40mV con señal real. [@muestreador]
    - 🔀 **EN BRANCH** `nocturno/local-2026-07-29-vpp-field-characterization` (pendiente de merge): **caracterización offline del v_pp real** en la ventana EXACTA del firmware (500 muestras = 1 s). `tools/analyze_vpp_field.py` (read-only sobre las capturas) + 9 tests + `docs/vpp-field-characterization.md`. Hallazgos: (1) v_pp real **≤14 mV mediana** en toda condición normal → ALERT 40 mV con margen enorme, valida el fix MONITOR=35 mV del 07-28-b; (2) **@firmware** — el self-trigger v3 (1 burst, sin hold) convierte dropouts de 0.0 V en ALERTAS espurias (3.0 % en motor ON, 0 % con guard); legacy tenía `HOLD_SEC=1.5s`. Fix candidato a confirmar en banco. [@muestreador + @firmware]
3. **Test con LiPo REAL** — sacar `DEV_BENCH_NO_BATTERY` (hoy finge 4.0V). Presupuesto de energía medido del ciclo completo wake→muestreo→POST→sleep. [@energia]
4. **Re-flashear ESP-B** con el cliente nuevo (A ya está en 0.1.3 vía OTA; B quedó atrás). [@firmware]
1. **RX completo** — ~~hoy es heartbeat-only~~ **DESACTUALIZADO**: el RX de `main` ya está en `3.6.7-RX-palways` con LCD, buzzer, WebServer gateway y OTA per-device; la **Task 08 está completa en el branch `rx/task08-completo` (3.7.0)** + deuda del @verificador pagada en `nocturno/local-2026-07-09-rx-deuda-verificador` (3.7.1, compila). **Lo que falta es BANCO, no código**: mergear y validar E2E. [@firmware + @verificador]
2. **Validación con GALGA FÍSICA + INA333** — todo corre con `DEV_SIMULATE_ADC`. Banco real, comparar contra `data/field_captures/` (ground truth, READ-ONLY). ~~Revalidar umbral v_pp>40mV~~ 🔀 **ese umbral vive en el linaje retirado**; en el vigente **no hay umbral** (ver #16). [@muestreador]
3. **Test con LiPo REAL** — sacar `DEV_BENCH_NO_BATTERY` (hoy finge 4.0V). Presupuesto de energía medido del ciclo completo wake→muestreo→POST→sleep. 🔀 Ojo: `DEV_BENCH_NO_BATTERY` es del linaje retirado — verificar el equivalente en `ota_wm_pp.ino` (tiene 5 perfiles de energía). [@energia]
4. 🔀 **Re-flashear ESP-B** — ~~con el cliente nuevo (A ya está en 0.1.3 vía OTA; B quedó atrás)~~. **CORREGIDO 2026-07-17: seguir esa instrucción flashearía B con el linaje RETIRADO** (downgrade `3.6.5`→`0.1.x`/`0.8.1`, perdiendo perfiles + gateway del PLAN v5). El `0.1.3` sale de `act.md` sesión 8 (26-abr) — el doc **termina ahí** y no registra el corte de linaje del 27-abr. **Lo correcto:** flashear B con `firmware/ota_wm_pp/` `-DDEVICE_TARGET_B` en **3.6.5**, perfil a definir. **Antes de flashear**: confirmar contra el device/`firmware_versions` qué corre hoy (el repo no lo sabe). Ver `docs/ESTADO_FIRMWARE.md`. [@firmware]

16. 🔴 **NUEVO (2026-07-17) — el lazo de alerta no está cerrado en el firmware vigente.** En `ota_wm_pp.ino` el flag `in_alert` **no se calcula de la señal**: es el perfil de compilación (`:1411`, `:1900` → `strcmp(PROFILE_NAME,"ALERTA")`). No hay `th_v`, ni `SELF_TRIGGER`, ni `hold_sec`, ni comando `set_thresholds` (grep → cero). Y el RX **sólo consume** el flag (`esp_rx_receptor.ino:849`), no calcula umbral. ⇒ **hoy el sistema no entra en alerta solo — lo decide un humano recompilando/OTAeando el perfil.** Insumos de diseño ya listos: `vpp-audit` (branch 07-11) + `alert-hold-replay` (branch 07-16) — reapuntados a este sketch. Ver `docs/ESTADO_FIRMWARE.md` §4. [@firmware + @muestreador]

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
    - 🔀 **EN BRANCH** `nocturno/local-2026-07-16-b-docs-entrada` (pendiente de merge): arreglados los 3 docs de ENTRADA (README/INDEX/CLAUDE) — el README declaraba "scaffolding, esperando contexto" y frenaba en seco a cualquier agente cold-start. Ver `MATI-HQ/diario/nocturno-local-2026-07-16-b.md`.
    - 🔀 **EN BRANCH** `nocturno/local-2026-07-17-linaje-firmware` (pendiente de merge): arreglados los docs de **ESTADO**. `act.md` se declara fuente de verdad pero **su última entrada es la sesión 8 (26-abr)** y no registra el corte de linaje del 27-abr (PLAN v5) → de ahí salieron el `0.1.3` de #4 y el "heartbeat-only" de #1. Nuevo `docs/ESTADO_FIRMWARE.md` con el timeline reconstruido y evidencia. **Pendiente (sólo Matías/@cronista):** escribir las sesiones 9+ de `act.md` (27-abr→jul) — no lo inventé.
15. Definir con GIMAP/Dreyfus: FECHA exacta de la parada, lugar, quién va. [MATÍAS]
17. 🟡 **NUEVO (2026-07-17) — decidir el destino de `firmware/esp_a_emisor/`, `esp_b_emisor/` y `shared/`** (linaje retirado): marcarlos legacy (como `firmwares/_legacy/` en el repo `datalogger`) o borrarlos. Hoy son una **trampa activa**: es el sketch de nombre más obvio y ya hizo caer a **dos noches de análisis** (07-15 energy-budget, 07-16 alert-hold) que leyeron el archivo muerto. **No se movió ni borró nada** — es decisión de Matías. [MATÍAS + @firmware]

## Lecciones ya pagadas (no repetir)
- TLS: cert **GTS Root R4** + HTTPClient simple. NO reabrir (debug completo en docs/).
- mDNS descartado por flakey. Migraciones append-only. Paths sin espacios (por eso vivís en C:\Proyectos\galgas).

## Hecho
- 2026-07-07 — Migrado a C:\Proyectos\galgas + GitHub privado (1007 archivos, field_captures con backup por primera vez).
