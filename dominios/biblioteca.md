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

## 2026-09-01 — Segunda cosecha: KiCad por código + primer .scad

Pedido del Director: cosechar el toolchain de @esquematico (Termovigía base v2)
y la lib OpenSCAD de @diseno3d. Repo biblioteca: commit `f601b61`.

### Qué entró

**pc\kicad_gen\** (carpeta nueva, con `README.md`):
- `kicad_gen.py` — framework de esquemáticos KiCad 10 por código (Sheet/Part con
  `.pin(n)`, wire/junction, rail/gnd/pwr_flag, hojas jerárquicas, `modulo_symbol`,
  `chequear_geometria`, `chequear_referencias`, `write_sheet/write_custom_lib/write_project`).
- `symlib.py` — extractor de símbolos de las libs oficiales (resuelve `extends`) + pines.
- `chequear_solapes_sch.py` — QA de texto (copia idéntica a laser-pcb y Termovigía; solo se agregó ficha).
- `verificar.py` — pipeline ERC + solapes + PDF + netlist + BOM + PNG, parametrizado
  (raíz por argumento, hojas hijas descubiertas del archivo).
- `ejemplo\generar_ejemplo.py` — 3 componentes (bornera → R → LED → GND).

**Linaje verificado en los repos** (no de palabra): laser-pcb
(`ejemplo_kicad/tools/gen_sch.py` + `esquematico/kicad/generar_interfaz.py`,
erc.rpt 2026-07-30 0/0) → galgas (`hardware/kicad/generar_nodo_galga.py`,
erc.rpt 2026-08-20 0/0) → Termovigía (`hardware/v2/termovigia_base`, erc.txt
2026-09-01 0/0, 6 hojas). `ALDI DISEÑO.kicad_sch` NO cuenta: es a mano en
eeschema 9. `hardware/generar_kicad_sch.py` (KiCad 9, sin symlib) es ancestro
conceptual, no de código.

**Evidencia de la copia**: `python ejemplo\generar_ejemplo.py` + `python
verificar.py ejemplo\ejemplo.kicad_sch` → `ERC messages: 0 Errors 0 Warnings 0`,
0 solapes, PDF/NET/BOM OK, PNG mirado (J1→+5V→R1→D1→GND correcto). Quedan
`ejemplo\ejemplo.kicad_sch` y `salida\p1.png` commiteados como evidencia.
Gotcha nuevo cazado con el ejemplo: el ERC de KiCad 10 valida que la huella
exista en las libs instaladas (`footprint_link_issues` = warning = falla).

Adaptaciones respecto del original (en ficha como probadas SOLO por el ejemplo):
`configurar()` en vez de `PROJECT[0]`/`CUSTOM_LIB` hardcodeado, `Sheet(madre=...)`
genera sus uuids, `sheet_symbol(hija, ...)`, `write_sheet` sin `root_uuid`.
El descubrimiento de hojas hijas en `verificar.py` no se probó con un proyecto
jerárquico: **solo sintaxis**.

**3d\** (sección nueva en LEEME):
- `lib_gabinete.scad` — de `frioseguro\hardware\v2\gabinete\lib_termovigia.scad`.
  Módulos: tabla PG + `pg_distribuir`/`pg_extremo` (los agregó @diseno3d
  mientras yo cosechaba; incluidos), gota truncada, `agujero_pared`, standoff,
  columna_tapa, oreja_pared, ranura_precinto, guia_luz, oblongo, caja_r.
  Afuera: el isotipo de marca (`iso_*`, `isotipo`) — es Termovigía, no gabinete.
- `test_lib_gabinete.scad` — instancia todo; `openscad.exe -o x.stl` →
  Volumes 10, sin warnings, echos de la tabla PG correctos. `*.stl` gitignoreado.
  **NO impreso**: la ficha lo dice.

### Proyectos de origen
NO tocados (ni el comentario de "versión canónica"): Termovigía sigue con
`include <lib_termovigia.scad>` y con sus `kicad_gen.py`/`symlib.py` locales.

### Próximo paso
1. Próximo esquemático de @esquematico: usar `biblioteca\pc\kicad_gen` en vez
   de copiar de Termovigía; si es jerárquico, marcar en la ficha de
   `verificar.py` que el descubrimiento de hojas anduvo.
2. Cuando @diseno3d imprima el gabinete: actualizar PROBADO de `lib_gabinete.scad`
   con lo medido (agujero PG7, standoff M3).
3. Siguen pendientes los del 08-21 (batería del nodo, flashear_pico, OTA ESP32).
