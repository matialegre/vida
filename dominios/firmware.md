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

- 2026-07-08 [BRIEFING GIMAP] — leer ../BRIEFING_EQUIPO_GIMAP.md y los 4 docs (PARTE_GIMAP, PRESUPUESTO_ENERGIA, PROTOCOLO_CALIBRACION, INGENIERIA_NODO_1ANO). Para vos: emisores NO ESP32 (ATmega/STM32L bare-metal, sleep µA real); receptor SÍ ESP32; retomar TX = ventana RX Class A + reed/imán; VERIFICAR sleep con INA219.

- 2026-07-13 [FrioSeguro — COMPILADO para Supabase nuevo, NO flasheado] — arduino-cli 1.4.1, core esp32:esp32 3.3.8, FQBN `esp32:esp32:esp32` (partición default: app 1310720 B). 2 variantes, AMBAS SIN SIM (SIM800 descartado, commit 48ef83f): PLACA_NUM=1 → placa "sin SIM" (flash USB) y PLACA_NUM=2 → placa que porta el SIM800 físico (flash por aire). config.h: PLACA_NUM 4→2 final, DEVICE_NAME "SIM800"→"" (pisaba el nombre de ambos devices). Binarios en `C:\Proyectos\frioseguro\firmware_modular\build_out\` (gitignored): `placa1_nosim_usb/` y `placa2_exsim_ota/` (artefactos completos) + .bin sueltos nombrados. Tamaño: 1288696 B (98% flash — SIN margen, próxima feature no entra), RAM 16%. Verificado con strings: cada bin con su mDNS/versión, URL nueva cjdluhemschrynijzvap, cero rastro del proyecto viejo, Telegram intacto.
  HALLAZGO CRÍTICO (lección headers huérfanos): **ArduinoOTA NO EXISTE en el firmware** (nunca existió — git log -S lo confirma); `OTA_ENABLED/OTA_PORT/OTA_PASSWORD` son defines huérfanos, el doc ARQUITECTURA_2026-07-13.md §6 está equivocado. espota NO sirve ni contra el firmware viejo ni el nuevo. OTA real que SÍ está cableada: HTTP `POST /update` puerto 80 (web_api.h:417, multipart, sin auth) + OTA cloud Supabase (supabase.h:625). Flasheo por aire = `curl -F "update=@<bin>" http://<IP>/update`. Otros huérfanos: serial_api.h, current_sensor.h, power_monitor.h (nadie los incluye). Linter pre-flash: NO apta para CLIENTE por OTA abierta sin password (deuda ya registrada, para el banco OK). PENDIENTE: flashear (Matías/Director), agregar ArduinoOTA o auth al /update antes del primer cliente, resolver el 98% de flash (min_spiffs en placas con acceso USB).

- 2026-07-13 [gimap-ap v1.0.0 — COMPILADO, NO flasheado] — Firmware nuevo pedido por Lucas Oxarango (GIMAP): ESP32 como "router" para los 2 sensores comerciales WiFi/MQTT del labo. Repo nuevo `C:\Proyectos\gimap-ap\` (git init, commit 62dc360). SoftAP fijo `Gimap_Sensores`/`Gimap2218` (WPA2, canal 6, max 8, sin WiFiManager) + **broker MQTT embebido PicoMQTT 1.3.0 en 1883** (SI entro: lib en el index con soporte esp32; subclase de `ServerLocalSubscribe` con `subscribe("#")` -> buffer circular 20 msgs + hooks on_connected/on_disconnected) + pagina de estado en 192.168.4.1 (clientes MAC/IP/RSSI via `esp_wifi_ap_get_sta_list` + `esp_netif_dhcps_get_clients_by_mac`, uptime, ultimos topics) + watchdog task 30 s + heartbeat serial 60 s. Compila limpio: FQBN `esp32:esp32:esp32`, core 3.3.8 -> **963948 B flash (73%), 51016 B RAM (15%)**. Binarios versionados en `build_out/` (.bin/bootloader/partitions; elf/map/merged gitignored). Flasheo: `arduino-cli upload --fqbn esp32:esp32:esp32 --port COMx --input-dir build_out gimap_ap` (comando en README). PENDIENTE: Matias flashea la placa elegida + smoke test (banner serial, celular visible en la pagina, publish/subscribe con mosquitto o el script Python de Lucas) -> recien ahi anotar en la tabla de versiones.
