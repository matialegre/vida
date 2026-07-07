# MAPA DE PROYECTOS — todas las rutas de lo que hizo Matías

> **PARA EL PRÓXIMO AGENTE (Opus 4.6 o quien venga):** este archivo es tu mapa del disco. Fue escrito por Claude Fable el 2026-07-07 tras analizar cada repo con subagentes. Leé primero `PORTFOLIO.md` (estado+plan), después esto (dónde está cada cosa). El sistema completo: `~/.claude/CLAUDE.md` (modo Director global) + `~/.claude/agents/` (7 agentes) + esta carpeta MATI-HQ (docs+bitácoras). ⚠️ La memoria persistente de Fable vive en `C:\Users\Pandemonium\.claude\projects\C--Users-Pandemonium-Documents-BACKUP-MATI-ERP\memory\` — solo se carga en sesiones abiertas en la carpeta del ERP; por eso TODO lo importante está duplicado acá.

## ⚡ MIGRACIÓN 2026-07-07 — RUTAS NUEVAS (las viejas quedaron como _ARCHIVO_*, nada borrado)
| Proyecto | Ruta NUEVA | GitHub (privados) | Pendientes |
|---|---|---|---|
| galgas | `C:\Proyectos\galgas` | github.com/matialegre/galgas | `QUE_FALTA.md` en el repo |
| datalogger | `C:\Proyectos\datalogger` | github.com/matialegre/datalogger | `QUE_FALTA.md` |
| frioseguro | `C:\Proyectos\frioseguro` | github.com/matialegre/frioseguro | `QUE_FALTA.md` |
| cosechador | `C:\Proyectos\cosechador` | github.com/matialegre/cosechador | `QUE_FALTA.md` |
| cuartel (este) | `C:\Users\Pandemonium\Documents\MATI-HQ` | github.com/matialegre/vida | — |

Archivos viejos: `Documents\_ARCHIVO_GALGAS_referencias` · `Desktop\_ARCHIVO_RASPBERRY_copias_viejas` · `Documents\_ARCHIVO_FRIOSEGURO_copia_vieja` · `Desktop\_ARCHIVO_AgenteBahia`. Rutinas cloud activas: briefing Director diario 8:00 · scout tendencias dom 18:00 · investigación rotativa mié 18:00 (todas Opus, corren contra el repo vida).

## 1. galgas — EL PROYECTO P0 (parada Dreyfus octubre)
- **Raíz:** `C:\Proyectos\galgas` (ex `GALGAS CON SUPABASE\galgas-supabase` — migrado, ahora sin espacios como exige el repo)
- **Fuente de verdad:** `act.md` (sesiones 1-8; las docs raíz/README están DESACTUALIZADAS)
- Clave: `firmware/` (3 sketches ESP32 + `shared/`; principal: `ota_wm_pp` v3.6.x) · `backend/supabase/` (migraciones append-only, NO editar viejas) · `web/` (dashboard React deployado: dreyfus-gimap.netlify.app) · `redler/` (mockup SCADA a integrar) · `tools/` (logger/sniffer/simulator Python) · `data/field_captures/` (CSVs reales Dreyfus feb-2026 — **READ-ONLY, no tocar jamás**) · `docs/` (PLAN_v5, ADRs 0001-0005, debug TLS) · `scripts/` (SETUP.ps1, sync_*.ps1) · `bins_*/` (binarios OTA)
- Supabase proyecto: `wtjjxhoyoqeicrydsppg` (sa-east-1). TLS: cert **GTS Root R4** + HTTPClient simple (NO reabrir ese debug, está resuelto).
- Reglas del repo: paths sin espacios, Arduino Core ESP32 3.3.1, secrets gitignored, rioplatense.
- En la misma carpeta padre hay copias de referencia: `FRIOSEGUROCLOUD-master` y el legacy `Galgas_GIMAP` + `ejemplo supabase/`.

## 2. Galgas legacy (referencia histórica)
- **Raíz:** `C:\Users\Pandemonium\Documents\Galgas_GIMAP-master\Galgas_GIMAP-master` (todo del 09/10/2025; hay también `Galgas_GIMAP-master.zip` al lado)
- 3×ESP32 UDP/AP local (`BELT_AP`, puertos 4210/4211, StatsPacket 25B). Sirve para: lógica de calibración 3 etapas + auto-offset, filtros IIR, simuladores `simulator_A/B.py` (vigentes; `simulador_emisores.py` y `test_simple.py` son OBSOLETOS).
- ⚠️ Lecciones: headers huérfanos nunca incluidos en .ino (`power_saving.h` etc.) · `analogRead()` en ISR (no repetir) · README describe protocolo viejo (mentira histórica).

## 3. RuView / datalogger (carpeta "RASPBERRY")
- **Raíz VÁLIDA (triple anidada):** `C:\Users\Pandemonium\Desktop\RASPBERRY\RASPBERRY\RASPBERRY` — las carpetas de afuera son copias viejas (lo advierte `QUE_HACER.md §2`). Hay un `RASPBERRY.rar` en Documents.
- **Fuente de verdad:** `QUE_HACER.md` (al 2026-06-19). Gobernanza: AGENTS.md, DECISIONS.md, PROGRESS.md, feature_list.json, verify.py.
- Clave: `firmwares/pico2w-node/` (nodo canónico MicroPython: `nodo.py`, `config.py`, `config.P1/P2/P3.json`, drivers, `flash_node.ps1`) · `firmwares/esp32s3-com11/esp32_dashboard/esp32_dashboard.ino` (gateway Arduino C ~62KB) · `vercel-dashboard/` (cloud: vercel-dashboard-indol-one.vercel.app, `api/index.js`, Supabase tabla `ruview_readings`) · `pc-sniffer/` · `recolector/` (harvesting LTC3588: specs PCB, plan, PDFs, compras) · `docs/power-budget.md`
- Reglas: JAMÁS mDNS (beacon UDP 50505 `RUVIEW`) · no mandar `eco on` a P1/P2 (quedan inalcanzables) · LoRa 433 SF7 frame `RV1|src|dst|pid|ttl|tipo|via|payload`.

## 4. FrioSeguro (Panamerican / SaaS Bahía) — palanca de plata
- **Raíz:** `C:\Users\Pandemonium\Desktop\AgenteBahia-master (1)\AgenteBahia-master (1)\AgenteBahia-master\FRIOSEGUROCLOUD-master\FRIOSEGUROCLOUD-master`
- **Spec maestra:** `FRIOSEGURO_MEGAPROMPT.md` en la carpeta padre (~27KB: 5 PCBs, pinout, schema, reglas de negocio)
- ⚠️ Existe OTRA copia en `C:\Users\Pandemonium\Documents\FRIOSEGUROCLOUD-master` — verificar cuál está más nueva antes de tocar.
- Clave: `firmware_modular/` (v4.0.0, headers por dominio, `config_SANTA_CRUZ.h`) · `web-dashboard/` (Netlify) · `android-app/` + `frioseguro-android/` (APK v17) · `supabase/` (schema_v2, ~15 migraciones) · `ALDI DISEÑO.kicad_*` (PCB) · `ESTADO_ACTUAL.md` (verdad al 09/03/2026)
- Estado: dashboard+app+cloud OK; SIM800/OTA/NTP sin validar en hardware; credenciales default sin cambiar.
- **Inventario físico en casa:** 5 PCBs fabricadas (2 SIM800 + 3 WiFi), 20 sondas DS18B20, 10 reed, 5 ESP32, relés.

## 5. Cosechador de energía (replicación paper)
- **Raíz:** `C:\Users\Pandemonium\Documents\COSECHADOR ENERGIA`
- Paper a replicar: `MEAS-D-25-07766.pdf` (Machado et al., Measurement — NO es de Matías). El otro PDF (`Implementacin_...Rotativo.pdf`) está marcado OBSOLETO (decisión D12).
- Clave: `AGENTS.md`, `PROGRESS.md`, `DECISIONS.md`, `docs\setup-completo.md`, `docs\architecture.md`. Estado ~10%: BOM ~$154.500 sin comprar, sin firmware, sin git.

## 6. Universidad UTN
- **Raíz:** `C:\Users\Pandemonium\Documents\UNIVERSIDAD UTN` (4 materias). Legajo 19074. Prof. industriales: Oscar Alfredo Conde.
- **SCI** (`sistema de control industrial\`): `TP_Sistema_Control_Industrial.html` (TP Integrador) · `cuadernillo-SCI.html` (fechas: cierre TP **1-AGO-2026**) · `Cuadernillos de TP ... 2026.pdf` (enunciado) · `UTxx.SCI Formato para los TP.docx` (plantilla entrega) · `BRIEFING-Claude-LOGO.md` + `Resolucion-Parcial1-SCI-2026.html`
- **Electrónica Industrial** (`electronica industrial\`): `Resolucion_Cuadernillo_TP_EI.md/.html/.pdf` (TP A-F completo) · `TP_Electronica_Industrial.html` (plantilla) · `Resolucion_Parcial1_EI_2026.pdf` · `P3_Esquemas_Neumaticos_Interactivo.html` (simulador ISO 1219 que le gustó al profe — ESTE FORMATO ES EL DIFERENCIAL, repetirlo) · manual Rosemount 3051 · fotos datos de cátedra `datos1.jpg`/`datos2.jpg`
- **Sistemas de Control** (`sistemas de control\`): apuntes 01-07, TP1-TP6 resueltos, `APUNTE_COMPLETO_TPs_1-6.html`, `cerradura.vhd.txt`, `Puente H · STM32F103.html`. **Exige proyecto de LABORATORIO a fin de año (cursada 2° cuatri).**
- **Electrónica de Potencia** (`electronica de potencia\`): `labo step down\Informe Laboratorio · Convertidor Step-Down · Grupo 2.pdf` + `UP\informe_boost.html` (PSIM) + `1ER PARICAL\`
- **FPGA:** `C:\Lab10_Booth` — multiplicador Booth VHDL (Quartus, DE2) + verificación SystemVerilog con clases (`booth_verif.sv`, `booth_pkg.sv`, `booth_multiplier_tb.sv`) + apuntes.
- Calendario oficial: `MATI-HQ\CALENDARIO_UTN_2026.md`.

## 7. ERP / Modulia (tiene equipo propio — NO gobernar desde acá)
- **Backup:** `C:\Users\Pandemonium\Documents\BACKUP MATI ERP\codigo` · **Original:** `D:\ERP MUNDO OUTDOOR`
- Su gobierno: `CLAUDE.md` + `AGENTS.md` + `.claude/` propio (37 agents con `@empresario` de CEO, commands, skills, docs). Backend FastAPI :8000, Postgres :2048, frontend React JSX.
- Doctrina reutilizada en todo el sistema: `.claude/docs/HARNESS_ENGINEERING.md` + `.claude/skills/karpathy-principles.md`.

## 8. CV y búsqueda laboral
- **Raíz:** `C:\Users\Pandemonium\Desktop\CV` — `CV_Matias_Alegre_v6.pdf/.html` + `_EN` · `buscar_empleos.py` (scraper corriendo, historial en `empleos_historial.json`, salida `empleos_remotos.html`) · `donde_mandar.py/html`

## 9. Sin código / pendientes de analizar
- Kiosco Ofiuco: `C:\Users\Pandemonium\Documents\KIOSCO OFIUCO PACO\kioscofiuco-master (1)` — SOLO README (el código no está; el README nació de la plantilla "SISTEMA MATI").
- **Carpetas en Documents AÚN NO ANALIZADAS** (preguntarle a Matías cuáles importan): `GALGAS POST DREY (2)` (¡suena a post-Dreyfus, puede ser relevante!), `GIMAP`, `Datalogger Acelerometro4`, `Refineria`, `CHUBON`, `TALLER EURO`, `Proyecto ERP`, `Proyecto Android SO`, `Arduino`, `jesustodomadera`, `maddenstreet`, `mattyaldi`, `cumple70vasco`.

## El sistema de agentes (construido 2026-07-07)
- `C:\Users\Pandemonium\.claude\CLAUDE.md` — MODO DIRECTOR global (se carga en toda sesión)
- `C:\Users\Pandemonium\.claude\agents\` — **9 agentes** (los VIVOS que carga Claude Code): `director` (opus, orquestador) · `energia` · `comms` · `muestreador` · `hardware` · `firmware` · `utn` · `comercial` (ventas/marketing, ejecuta PLATA.md) · `verificador` (calidad, generator≠evaluator, último gate)
- `C:\Users\Pandemonium\Documents\MATI-HQ\` — `PORTFOLIO.md` (maestro) · `PLAN_MES.md` (7-jul→18-ago, día por día) · `PLATA.md` · `CALENDARIO_UTN_2026.md` · `MAPA_PROYECTOS.md` (este archivo) · `CLAUDE.md` (modo comando: designación en paralelo) · `dominios\*.md` (7 bitácoras) · `agentes\` (BACKUP de los 9 agentes — los vivos son los de `~/.claude/agents/`; re-sincronizar el backup al editarlos)
- Repo remoto del cuartel: **github.com/matialegre/vida** (push al cerrar cada sesión)
