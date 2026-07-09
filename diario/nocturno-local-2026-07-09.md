# Nocturno LOCAL — 2026-07-09 (worker de la PC, Matías durmiendo)

## Tarea elegida y por qué
**Pagar la deuda del @verificador sobre el branch RX de galgas (M1/M2/M3/B2/B3).**

La madrugada del 8-jul el verificador auditó los 2 branches de firmware y dejó
"Retomar" con dos ítems (`diario/2026-07-08-veredictos-verificador.md`):
1. Deuda ECO-LoRa D1-D8 (datalogger) → **ya la pagó el nocturno del 8-jul**.
2. Deuda RX M1/M2/B* (galgas) + M3 (migración) → **NO se había aplicado**
   ("elegí UNA tarea" dijo el worker anterior). Es deuda documentada y presente.

Por qué esta y no otra, con la jerarquía **PLATA y UNIVERSIDAD primero, octubre
segundo**:
- **FrioSeguro (PLATA)** tiene su branch nocturno `...frioseguro-particion-ota`
  **vacío** (sin commits propios) y sus ítems de software (#11 resumen mensual,
  #12 retención) son *para cuando ya haya abonos* — hoy hay **cero**, así que
  construirlos ahora es prematuro (anti-sobre-ingeniería). Los bloqueantes
  reales de PLATA (#1-6) son hardware/comercial: flashear, piloto casero,
  precio, caja estanca — nada de eso es software nocturno.
- **UNI** vive en `UNIVERSIDAD UTN\`, fuera de los 4 repos del worker.
- En cambio la **M1 del RX es un bug de seguridad presente** sobre P0 (galgas,
  parada de octubre): en un corte general el panel de alerta quedaba **mudo**
  mostrando "sin datos" indefinidamente — justo cuando más importa. Quirúrgico,
  documentado por el verificador, verificable por recompilación. Es el
  "Retomar #2" explícito. Encaja con "UNA tarea bien hecha por noche".

## Qué hice (branch `nocturno/local-2026-07-09-rx-deuda-verificador`, sale de `rx/task08-completo`)

FW `3.7.0-RX-palways` → **`3.7.1-RX-palways`**.

| # | Sev | Archivo | Fix |
|---|-----|---------|-----|
| **M1** | 🟠 ALTA oct | `esp_rx_receptor.ino` + `config.h` | `last_seen_unix` de A/B se **persiste en NVS `rx_seen`** y se restaura en el boot (`seenLoadOnBoot`), con anti-wear (`seenPersistTick` en el heartbeat, `SEEN_PERSIST_MIN_DELTA_S=300`). Un emisor visto **alguna vez** se recuerda cruzando el power-cycle → escala a `SILENT` tras la gracia de 180 s; uno **nunca** visto (banco 1 emisor / B sin instalar) sigue sin alarmar. `doFactoryReset` limpia `rx_seen`. |
| **M2** | 🟠 | `esp_rx_receptor.ino` | `esp_task_wdt_reset()` al inicio de cada handler bloqueante: `doHeartbeatAndLocalIp`, `processRxCommands` (+ por cada ack del `for`), `cloudRefreshOne` (cada GET), `doOtaCheck` (firmware-check previo al `wdt_delete`), y el bloque de reconexión WiFi de `loop()`. Cada segmento queda << WDT 120 s aunque varios handlers caigan en la misma iteración con WAN flaky. |
| **M3** | 🟠 | migración | `git mv 20260708000000_add_set_config_cmd.sql → 20260708200000_...` para ordenar **después** de las del branch `backend/ota-ab-bucket-firmado` (`...150000`/`...151000`). Nunca aplicada al cloud → rename seguro. 4 refs en docs actualizadas (RX_TASK08_NOTAS ×3, README ×1, QUE_FALTA ×1). |
| **B2** | 🟡 | `esp_rx_receptor.ino` | Helper `cfgReadU32` en `handleSetConfig`: rechaza no-números/negativos. Antes `stale_s:-5` envolvía a ~4.29e9 (clampeaba a MAX) y `mute_min:"abc"` daba 0 → **des-muteaba sin querer**. |
| **B3** | 🟡 | `esp_rx_receptor.ino` | `mute_min:N>0` ahora **pisa un `pause` infinito previo** (`g_mute_forever=false`). |

También sincronicé `docs/RX_TASK08_NOTAS.md` (sección "3.7.1 — deuda aplicada" con
checklist de banco) y `QUE_FALTA.md` (ítem 1 → deuda aplicada en el branch).

## Cómo verificarlo (comandos exactos)
```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-09-rx-deuda-verificador

# Recompilar (core esp32 3.3.8 ya instalado en esta maquina)
/c/Tools/arduino-cli/arduino-cli compile \
  --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs \
  --output-dir build/esp_rx_371 firmware/esp_rx_receptor

# Ver los 3 puntos clave del diff:
git diff rx/task08-completo -- firmware/esp_rx_receptor/esp_rx_receptor.ino \
  | grep -E "seenLoadOnBoot|seenPersistTick|esp_task_wdt_reset|cfgReadU32|g_mute_forever"
```
**Resultado obtenido esta noche:** compila **OK** — `1.244.032 bytes (63%)`,
globals `61.880 (18%)`, arduino-cli 1.4.1 + core esp32 3.3.8, `min_spiffs`.
Delta vs 3.7.0 (1.243.316) = **+716 bytes**. Revisión de tipos: `cfgReadU32`
rechaza string/float/negativo; NVS `rx_seen` usa `uint64` epoch con umbral
`>1735689600`; `esp_task_wdt_reset()` sólo se llama desde el `loopTask`
(suscrito al WDT en setup).

## Qué quedó SIN verificar (necesita el ESP32-RX en mano)
- **M1 en vivo:** con A+B vistos, cortar todo (emisores + RX + WAN), rebootear el
  RX **sin internet** → tras la gracia de 180 s debe pasar a `SILENT` con beep
  (antes quedaba mudo). Y en banco con **un solo** emisor confirmar que B (nunca
  visto) NO alarma. Ver en Serial `[SEEN] restaurado de NVS`.
- **M2:** RX 2+ h con WAN degradada → cero `[WDT]`/panic espurio (RIESGO #1 del
  banco, ya listado en RX_TASK08_NOTAS).
- **B2/B3:** mandar `set_config {"stale_s":-5}`, `{"mute_min":"abc"}`,
  `{"mute_min":0}`, y `pause`→`{"mute_min":5}`; verificar los acks.
- **M3:** aplicar la migración renombrada (`supabase db push`) coordinando el
  orden con el branch `backend/ota-ab-bucket-firmado` (deuda de @backend).

## Reglas respetadas
Nada borrado (salvo `git mv` de una migración nunca aplicada, pedido explícito
del verificador). NO se tocó `data/field_captures/` (sagrado), ni `shared/`, ni
mDNS, ni migraciones ya aplicadas (append-only intacto). Sólo software, branch
nuevo. **El branch NO se mergea a main hasta pasar banco/hardware.**

## Branch
`nocturno/local-2026-07-09-rx-deuda-verificador` (pusheado a origin, 1 commit).
Sale de `rx/task08-completo`.

## Sigue pendiente (NO tocado esta noche)
- **Banco/hardware de los 3 branches RX/datalogger** que esperan flasheo:
  `rx/task08-completo` (+ estos fixes), `backend/ota-ab-bucket-firmado`, y los 2
  del datalogger. Todos "PASA CON DEUDA / apto banco", ninguno mergeado.
- FrioSeguro: los bloqueantes de PLATA son hardware/comercial (no nocturnos).
