# Veredictos del verificador — branches de la noche (2026-07-08, madrugada)

> Auditorías adversariales de los 2 branches de firmware críticos, ANTES de flashear. Generator ≠ evaluator.
> ⚠️ Se tocó el LÍMITE DE SESIÓN a las ~4:40am aplicando los fixes → la deuda de ECO-LoRa quedó SIN aplicar. Retomar después del reset.

## 🏭 branch `rx/task08-completo` (galgas) → ⚠️ PASA CON DEUDA
**Flasheable a BANCO mañana, NO a producción.** El verificador RE-COMPILÓ (1.243.316 bytes / 63%, byte-idéntico a lo declarado), confirmó que NO toca shared/, que las 14 funciones nuevas se llaman (cero huérfanas), migración coherente con el constraint real, WDT balanceado en OTA, y docs honestas. Intentó romperlo (millis overflow, mute, hora sin sync) y RESISTIÓ.

**Deuda con dueño (antes de octubre, NO bloquea banco):**
- **M1 🟠 [@firmware]**: emisores "nunca vistos" no alarman jamás. Escenario parada: corte general → RX rebootea → emisores no vuelven → internet caída → panel queda en OK mostrando "sin datos" SIN beep, indefinidamente. Contradice el propósito del feature. Fix: escalar a SILENT si tras stale_s de uptime un emisor sigue !valid, o persistir last_seen_unix en NVS.
- **M2 🟠 [@firmware]**: WDT 120s puede cruzarse en el peor caso (WAN flaky: reconnect 18s + patch 10s + heartbeat 23s + fetch 5s + 4 acks×5s + refresh 26s ≈ 110-125s) → reboot espurio perdiendo la cola de forwards. Fix: esp_task_wdt_reset() al inicio de cada handler periódico (1 línea c/u).
- **M3 🟠 [@backend]**: migración `20260708000000_add_set_config_cmd.sql` con timestamp que sortea ANTES de las del branch `backend/ota-ab-bucket-firmado`. `db push` la rechaza out-of-order. Fix: renombrar a `2026070820xxxx` + coordinar con @backend antes de aplicar.
- B1-B4 🟡: falso SILENT transitorio tras reboot con reloj NVS viejo; validación laxa en handleSetConfig (stale_s negativo, mute_min="abc" des-mutea); mute_min no pisa pause infinito; cosméticos.

## ⚡ branch `nocturno/local-2026-07-07-ina219-ecolora` (datalogger) → ⚠️ PASA CON DEUDA
**Apto para banco (arrancar con eco_sleep=idle, protocolo §7-B), NO para campo.** py_compile OK en los 8 archivos. El verificador confirmó: bug de 7/8 campos real y el fix mejora el mesh, matemática INA219 correcta contra datasheet, defaults seguros, failsafe cae hacia alcanzable. 4 intentos de dejar nodo inalcanzable FALLARON salvo D2.

**Deuda SIN APLICAR (el fix agent murió por límite de sesión — RETOMAR):**
- **D1 🔴 ALTA [@firmware]**: con gateway sin parchear, nodo eco sano nunca "oye" al gateway → failsafe → despierto permanente → en campo consume MÁS que sin eco. Parche gateway ~10-15 líneas (diseño en docs/ECO_LORA_DISENO.md §3.1): ACK a frames eco=1 + disparar comandos pendientes al ver uplink. BLOQUEANTE para producción.
- **D2 🟠 [@firmware]**: config.py valida eco_button_gpio solo por rango → poner el botón en GPIO 17 (CS del LoRa) mata el radio. Fix: blacklist pines 4,5,15,16,17,18,19,20,21,23,24,25,29.
- **D3 🟠**: "oír gateway" = literal "GW" → si cambia el ID, todos los nodos al failsafe. Comparar contra cfg["mesh_dst"].
- **D4 🟠**: LoRaTx.poll() lee el SX127x con bus a 10MHz (modo SD) → for_lora() al inicio.
- **D5-D8 🟡**: clamp cal INA219 a 16 bits; restaurar profile al salir de eco; entrada CHANGELOG; sim_data en eco._sample.

## Retomar (después del reset 4:40am o próxima sesión)
1. Aplicar fixes D1-D8 al branch ECO-LoRa (el prompt exacto quedó en la orden del fix agent que se cortó). D1 es el importante.
2. Aplicar M1/M2/B* al branch RX. M3: renombrar la migración antes de tocar Supabase.
3. Recién entonces flashear a banco. Ninguno de los 2 branches se mergea a main hasta pasar hardware.
