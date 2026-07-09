# Nocturno LOCAL — 2026-07-08 (worker de la PC, Matías durmiendo)

## Tarea elegida y por qué
**Aplicar la deuda del @verificador D1-D8 al ECO-LoRa del datalogger.**

La madrugada del 8-jul el verificador auditó los 2 branches de firmware y dejó una lista
explícita de "Retomar" (ver `diario/2026-07-08-veredictos-verificador.md`). El fix agent del
branch ECO-LoRa **murió por límite de sesión y dejó D1-D8 SIN APLICAR**, con **D1 🔴 marcado
BLOQUEANTE para producción**. No es una tarea "hecha esperando merge": es deuda pendiente y
documentada, sobre el datalogger, que es **PRIORIDAD #1 de banco** (PLAN_MES obj. #3) y
verificable sin hardware. Encaja con "UNA tarea bien hecha por noche".

## Qué hice (branch `nocturno/local-2026-07-08-ecolora-fixes`, arranca del branch `...ina219-ecolora`)

| # | Sev | Archivo | Fix |
|---|-----|---------|-----|
| **D1** | 🔴 bloqueante | `esp32s3-com11/.../esp32_dashboard.ino` | El gateway ahora responde a los frames `eco=1`: (a) ACK de vida `RV1\|GW\|<id>\|<seq>\|1\|A\|\|<seq> eco` → el nodo resetea el failsafe y **sigue durmiendo**; (b) dispara los comandos pendientes de ese nodo en la ventana RX → entrega garantizada con cualquier ciclo. Diseño §3.1. |
| D2 | 🟠 | `config.py` | `eco_button_gpio` rechaza pines de LoRa/SD/I2C/VSYS/WiFi (`_RESERVED_GPIO = 4,5,15,16,17,18,19,20,21,23,24,25,29`). Antes el botón en GP17 (CS LoRa) mataba la radio. |
| D3 | 🟠 | `nodo.py:poll()` | Gateway reconocido por `cfg["mesh_dst"]` (con `"GW"` de fallback), no por literal → renombrar el gateway ya no tira todos los nodos al failsafe. |
| D4 | 🟠 | `nodo.py:poll()` | `bus.for_lora()` al inicio; el SPI podía quedar a 10 MHz (modo SD) y la radio se lee a 5 MHz. |
| D5 | 🟡 | `ina219.py` | Clamp de `cal` a 16 bits (+ sube `current_lsb` para mantener la lectura correcta); con shunt+max_a chicos el cal ideal se pasaba de 0xFFFF y `_w16` lo truncaba en silencio. |
| D6 | 🟡 | `eco.py:run()` | Restaura el perfil de CPU configurado al salir de ECO (run/awake forzaban 48 MHz). |
| D8 | 🟡 | `eco.py:_sample()` | Si no hay MPU y `sim_data` (default), balanceo simulado → el frame eco deja de salir plano (az=1) en el banco. |
| D7 | 🟡 | `CHANGELOG.md` | Entrada de changelog. |

También sincronicé `docs/ECO_LORA_DISENO.md §3.1` (el parche del gateway pasó de "pendiente" a "APLICADO — falta banco") y `QUE_FALTA.md`.

## Cómo verificarlo (comandos exactos)
```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-07-08-ecolora-fixes

# 1) Python (nodo): sintaxis de los 4 archivos tocados
python -m py_compile firmwares/pico2w-node/eco.py firmwares/pico2w-node/config.py \
  firmwares/pico2w-node/ina219.py firmwares/pico2w-node/nodo.py     # -> sin salida = OK

# 2) Lógica del validador de gpio (default 22 pasa, pines reservados rechazan)
cd firmwares/pico2w-node
python -c "import config; v=config.SCHEMA['eco_button_gpio'][2]; \
  print(v(22), v(-1), not v(17), not v(25), v(2))"                  # -> True True True True True

# 3) Gateway (D1): compila con el core esp32
cd C:\Proyectos\datalogger\firmwares\esp32s3-com11\esp32_dashboard
arduino-cli compile --fqbn "esp32:esp32:esp32s3:USBMode=hwcdc,CDCOnBoot=cdc,FlashSize=16M,PSRAM=opi,PartitionScheme=custom" .
```
Resultados obtenidos esta noche: py_compile **OK** en los 4; validador **OK**; matemática del clamp INA
**consistente** (recomputar cal desde el lsb topado da el mismo 0xFFFF); gateway **compila** —
`1.164.127 bytes (6%)`, globals 90.848 (27%), con `arduino-cli` + core `esp32:esp32 3.3.8`.

## Qué quedó SIN verificar (necesita hardware — protocolo §7 del diseño)
- **Prueba de banco del ciclo ECO real** (lightsleep, USB que muere, wake por IRQ del botón).
- **D1 en vivo**: con el gateway parcheado, mandar `profile low` a P1 y confirmar **5/5** con cualquier
  ciclo (antes solo entraba con perfil `banco`); ver que el nodo NO cae al failsafe estando el gateway
  encendido y sin comandos; y que al apagar el gateway el failsafe dispara y luego **retoma solo**.
- **INA219 real**: cablear el módulo y correr `power bench 3` (Parte A del protocolo).
- No pude probar el `.ino` corriendo: compila, pero flashear/observar es de día con el ESP32-S3 en mano.

## Reglas respetadas
Nada borrado, nada de field_captures (es de galgas), sin mDNS, migraciones intactas. Trabajo solo
software en un branch nuevo. Los 2 branches previos (`...ina219-ecolora` y `rx/task08-completo`) siguen
esperando su banco; este branch NO se mergea a main hasta pasar hardware.

## Branch
`nocturno/local-2026-07-08-ecolora-fixes` (pusheado a origin, 2 commits). Arranca del branch
`nocturno/local-2026-07-07-ina219-ecolora`.

## Sigue pendiente para el @firmware (de la lista del verificador, NO tocado esta noche)
- **M1/M2/B* del branch `rx/task08-completo` (galgas)** — deuda del RX, no se aplicó (elegí UNA tarea).
  M3: renombrar la migración `20260708000000_add_set_config_cmd.sql` antes de tocar Supabase.
