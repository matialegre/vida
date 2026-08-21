# Bitácora — @bibliotecario

Dueño de `C:\Proyectos\biblioteca` (repo git local): módulos probados y
reutilizables con FICHA (ORIGEN/PROBADO/USO/DEPENDE/GOTCHAS). Catálogo:
`C:\Proyectos\biblioteca\LEEME.md` — leerlo ANTES de escribir código nuevo.

## 2026-08-21 — Fundación + primera cosecha

Repo fundado (`git init`, 4 commits, estructura `micropython\ esp32\ pc\ protocolos\`).

### Qué entró (9 piezas)

**micropython\** (del nodo GIMAP, `C:\Proyectos\datalogger\firmwares\nodo-gimap\`, Pico 2 W):
- `ota.py` — OTA anti-ladrillo (temporal + sha256 + rename atómico). PROBADO en hardware: update 1.0.0→1.0.1 real.
- `bateria.py` — VSYS con guard `V_MIN_PLAUSIBLE`. El gotcha ADC29/VSYS-comparte-pin-con-CYW43 se REPRODUJO en hardware (leía ~0.011 V con WiFi activo, casi ladrillo); el guard está flasheado pero **la prueba en batería sigue pendiente**.
- `red.py` — WiFi con fallback a AP de provisioning. Probado en hardware; adaptación menor (título/AP parametrizados) solo sintaxis.
- `led.py` — patrones de estado no bloqueantes. Probado en hardware.

**pc\** (de `C:\Proyectos\datalogger\`):
- `visor_udp.py` — receptor UDP + web de gráficos en vivo. Recibió datos reales esta semana; parametrización solo sintaxis.
- `publicar_ota.py` — sha256 + version.json. Sirvió el update real.
- `flashear_pico.py` — autodetección COM (filtra Bluetooth fantasma) + mpremote + sha256. **Solo sintaxis.**
- `verificar_udp.py` — evidencia: paquetes contados, uptime creciente, en_usb. **Solo sintaxis.**

**protocolos\**
- `udp_broadcast.md` — contrato completo emisor+receptor: `FMT_CAB=">4sBIHH"`, tamaños SIEMPRE por `struct.calcsize` (bug real: un 20 a ojo cuando eran 16 bytes corría todas las muestras).

### Qué NO entró y por qué (→ "Se busca" en LEEME.md)

FrioSeguro v2.6.0 (`C:\Proyectos\frioseguro\firmware_revival\`): los 4 candidatos
(`ota_update.h` con rollback esp_ota_*, `wifi_open.h` selección de abiertas por
RSSI con veto, `checkInternet()` testigo dual en `firmware_revival.ino:819`,
cliente Supabase + `comandos_nube.h`) dependen todos de globals del `.ino`
(`state`, `wdtFeed()`, `server`, `logRemoto`) y `config.h` — no se forzó la
cosecha; quedaron anotados con ruta y función. El más valioso: el OTA con
rollback; `compareSemver()` (ota_update.h:49-59) es autocontenida y ya testeada.

Secretos: `secrets.py` del nodo NO entró; el SSID de la casa que aparecía en un
help string de `probar_bateria.py` se quitó de la versión de biblioteca.

Proyectos de origen: NO tocados (ni el comentario opcional — editar el main.py
del nodo cambiaría su sha256 vs. el OTA publicado).

### Próximo paso
1. Correr la prueba en batería del nodo GIMAP (`verificar_udp.py` sin USB) y
   actualizar las fichas de `bateria.py` y `verificar_udp.py` con la evidencia.
2. Correr `flashear_pico.py` contra un Pico real y actualizar su ficha.
3. Cuando FrioSeguro necesite un cambio de OTA/WiFi: modularizar ahí y cosechar
   a `esp32\` (definir la interfaz mínima: state, wdtFeed, logRemoto).
