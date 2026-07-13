# PORTFOLIO — Cuartel General de Matías Alegre

> **Documento maestro.** El agente `@director` lo lee PRIMERO en cada sesión y lo actualiza al cerrar.
> Regla de oro: lo que no está acá (o en un doc linkeado) no existe. Cold-start test siempre.
> Creado 2026-07-07 por Claude (Fable) a partir del análisis completo de todos los repos.

## Quién es Matías (contexto mínimo)
Estudiante de último año de Ing. Electrónica (UTN Bahía Blanca, legajo 19074) + dev en Mundo Outdoor (autor de un ERP en producción, 23 usuarios) + investigador GIMAP (telemetría de galgas para Louis Dreyfus). En vacaciones de la uni hasta agosto 2026. Email dev: alegrematiasdev1@gmail.com.

## 👑 Jerarquía oficial de prioridades (Matías, 2026-07-07)
**1º PLATA y UNIVERSIDAD — empatados en la cima.** Plata = abonos FrioSeguro + ERP hacia autonomía (PLATA.md). Universidad = TPs, finales, cursada, proyecto final (recibirse).
**2º Octubre** (datalogger + galgas para la parada Dreyfus) — es también reputación/plata futura (servicios industriales).
**3º Todo lo demás.**
Regla de desempate diaria: si un día no alcanza para todo, sobrevive lo que tenga deadline más cercano de las categorías 1 y 2. La uni tiene fechas de cátedra (no se mueven); la plata tiene momentum (una semana sin acción comercial = pipeline muerto); el banco tiene octubre. En ese orden se sacrifica: 3º → banco (si octubre lo permite) → JAMÁS uni ni acción comercial de la semana.

## ⏰ Deadlines duros (ordenan TODO)

| Fecha | Qué | Proyecto |
|---|---|---|
| **2026-08-01** | Cierre de cuadernillos de TP de Sistemas de Control Industrial | UTN |
| **2026-08-18** | Inicio de clases 2° cuatrimestre — **LAS ÚLTIMAS 5 MATERIAS**: Sistemas de Control, Electrónica de Potencia, Economía, Inglés 2, Diseño y Manufactura de Circuitos Impresos. Finales: llamados 3-7 y 10-14 ago (fechas UTN: ver `CALENDARIO_UTN_2026.md`, única fuente) | UTN |
| Sin fecha de cátedra (los agenda Matías) | **Finales POR PROYECTO** de materias ya cursadas: TC2, Medidas Electrónicas 2, Tecnología, Sist. de Control Industrial, Electrónica Industrial | UTN |
| **Fin de año 2026** | **Proyecto de LABORATORIO de Sistemas de Control** (materia que cursa 2° cuatri) | UTN |
| 2026-2° cuatri | **Elegir el PROYECTO FINAL de carrera** (aún indefinido — decisión estratégica: alinearlo con datalogger GIMAP / harvesting / FrioSeguro) | UTN |
| **2026-10 (fecha exacta TBD)** | **PARADA DE PLANTA Louis Dreyfus** — el sistema de galgas tiene que estar validado e instalable | galgas-supabase |
| 2027 | Proyecto Final de carrera | UTN |

## 🗂️ Los proyectos (estado al 2026-07-07)

### P0 — galgas-supabase (LA PRIORIDAD TÉCNICA)
`C:\Proyectos\galgas` (repo: github.com/matialegre/galgas · pendientes: `QUE_FALTA.md`)
Reescritura cloud-first del sistema de galgas para Dreyfus (REDLER RPRB3). Fusión: física/DSP del GIMAP clásico + cliente Supabase de FrioSeguro. **Validado E2E en banco**: readings con deep sleep, provisioning, comandos con ack, OTA cloud (0.1.2→0.1.3), self-trigger alerta. Fuente de verdad del repo: `act.md` (las docs raíz están desactualizadas).
**Pendiente para octubre:** RX completo (hoy heartbeat-only; falta Realtime subscriber + LCD + buzzer + gateway HTTP del PLAN v5) · test con galga FÍSICA real (hoy `DEV_SIMULATE_ADC`) · test con LiPo real (hoy `DEV_BENCH_NO_BATTERY`) · re-flashear B · OTA que distinga A/B · bucket firmware con URL firmada · brownout USB · integrar mockup SCADA `redler/` al dashboard.
TLS: cert **GTS Root R4** + HTTPClient simple (lección aprendida, no repetir el debug).

### P0 — UTN: cierre de TPs integradores (deadline 1-ago)
`C:\Users\Pandemonium\Documents\UNIVERSIDAD UTN`
- **SCI**: TP Integrador 2026 desarrollado (WPLSoft, LOGO!, TSX Micro, S7-200, SLC500, CODESYS). **Cierra 1-ago.** Verificar completitud contra el cuadernillo, pasar a plantilla `UTxx.SCI Formato para los TP.docx`, entregar. Ojo: hay "temas de final" aparte (foro).
- **Electrónica Industrial**: TP Integrador A–F resuelto completo (mod. 6-jul). Falta verificación final + formato de entrega.
- **TC2 / Medidas Electrónicas 2 / Tecnología**: Matías debe un proyecto por materia. **NO HAY MATERIAL EN DISCO** — primera acción: bajar consignas del aula virtual.

### P1 — FrioSeguro (LA PALANCA DE PLATA)
`C:\Proyectos\frioseguro` (megaprompt en `docs\` · repo: github.com/matialegre/frioseguro · pendientes: `QUE_FALTA.md`)
Monitoreo de frío/puertas. Origen: Panamerican Cerro Moro (7 reefers). Destino comercial: SaaS para comercios de Bahía. **Inventario listo para vender: 5 PCBs, 20 sondas DS18B20, 10 reed switches, 5 ESP32, relés, IP fija propia.**
**Pendiente:** validar SIM800/OTA/NTP en hardware · flashear módulos nuevos · migración SQL columnas nuevas · credenciales de producción · circuito físico SIM800 · retención de datos. Dashboard Netlify y APK v17 ya operativos.

### P0 — RuView / datalogger — **TERMINARLO PRIMERO, antes del trabajo Dreyfus (orden de Matías 2026-07-07, "por las dudas")**
`C:\Proyectos\datalogger` (repo: github.com/matialegre/datalogger · pendientes: `QUE_FALTA.md` · desanidado, la copia vieja quedó en `Desktop\_ARCHIVO_RASPBERRY_copias_viejas`)
Red de vibración: Pico 2 W (MPU6050 50Hz→SD+FFT) → LoRa 433 mesh "RV1" → ESP32-S3 gateway → Vercel → Supabase. Visión: **datalogger fino alineado con las galgas**, perfil de energía "el mejor del planeta".
**Pendiente:** ECO-LoRa (sleep clase A) NO implementado — no mandar `eco on` a P1/P2 · driver INA219 para consumo real · prueba de alcance + salto repetidor · calibrar RSSI-distancia · decisión MicroPython vs C/C++ en nodos para low-power/muestreo determinista.

### P2 — Cosechador de energía (investigación)
`C:\Proyectos\cosechador` (repo: github.com/matialegre/cosechador · pendientes: `QUE_FALTA.md`)
Replicación del paper MEAS-D-25-07766 (harvesting piezo → LTC3588 → supercaps → detector de incendios sin batería). ~10%: BOM completo (~$154.500), nada comprado, sin firmware. 6 fases planificadas. Se cruza con `recolector/` de RuView (mismo LTC3588+supercaps).

### P0 permanente — ERP / Modulia (5hs diarias garantizadas — NUNCA olvidarlo)
`C:\Users\Pandemonium\Documents\BACKUP MATI ERP\codigo` (original en `D:\ERP MUNDO OUTDOOR`)
En producción (Mundo Outdoor, Montagne, TallerEuro, Cassano) + SaaS multi-rubro en curso. Se gobierna con SU `.claude` (37 agents, @empresario como CEO) — el Director no lo microgestiona, pero lo tiene SIEMPRE en el mapa porque:
- **Matías le dedica mínimo 5hs/día** (el bloque 13:00-17:30 ES el ERP + horas remotas) — es su frente diario más grande, no un proyecto lateral.
- **Objetivo declarado (2026-07-07): que quede ANDANDO SOLO** — soporte cubierto por un agente de IA (o pagado), onboarding y cobros automatizados. Cada sesión de ERP debería acercar eso: menos dependencia de Matías, no más features.
- **Es el mejor activo de venta**: "cadena de 13 locales lo usa hace 2 años" — se vende solo con referencia.
- **Es infraestructura para todo lo demás**: servidor físico + IP fija + dominios de Mundo Outdoor pueden hostear servicios del resto del portfolio. Regla Ponytail: lo que ya anda en Supabase/Netlify/Vercel NO se migra; el server propio es capacidad libre para lo NUEVO/pesado (video, MQTT, workers, backups pesados).

### P3 — Otros
- CV/búsqueda laboral: `C:\Users\Pandemonium\Desktop\CV` (CV v6 ES/EN + `buscar_empleos.py` corriendo).
- Kiosco Ofiuco: solo README (sin código en disco). Congelado salvo que aparezca el repo.
- Carpetas aún NO analizadas en Documents: `GALGAS POST DREY (2)`, `GIMAP`, `Datalogger Acelerometro4`, `Refineria`, `CHUBON`, `TALLER EURO`, `Proyecto Android SO` — pedirle a Matías cuáles importan.

## ⚠️ DECISIÓN URGENTE DE MARCA (detectada 2026-07-07 por @comercial)
**"FrioSeguro" ya existe como empresa** (*Frío Seguro Monitoreo del Frío S.R.L.*, CUIT 30-71874481-0, frioseguro.com, app en Play Store) con el MISMO modelo en CABA/Zona Norte. Valida el negocio, pero es riesgo marcario: **Matías debe elegir nombre nuevo para el producto comercial ANTES del primer folleto/contrato** (chequear INPI). El código/repos pueden seguir llamándose frioseguro internamente. Detalle en `comercial\PRECIOS_FRIOSEGURO.md`.

## 💪 Recursos (NO son cuello de botella)
- **Sistemas (vía Mundo Outdoor):** servidor físico disponible, dominios, PCs, compras de infra — lo que haga falta.
- **Hardware (vía GIMAP):** stock enorme ya en mano (mucho más que lo listado en FrioSeguro) + capacidad de compra de lo que falte.
- **Infra propia:** IP fija + router → self-hosting posible.
- **Mano de obra:** decisión de Matías — el equipo son SUS AGENTES DE IA (este sistema), no gente designada. El cuello de botella real es el TIEMPO de Matías y su foco → por eso WIP=1 y este portfolio.
- **Capital:** ~$300.000 ARS/mes propios para invertir.
- **Red humana de refuerzo:** compañeros de la uni con ganas, técnicos/ingenieros accesibles, profesores y contactos. Se usan para lo que un agente no puede hacer: instalar en campo, mediciones presenciales, avales académicos, cerrar ventas.

## 🧭 Jugada estratégica: LA CONVERGENCIA
Matías tiene **5 finales que puede rendir POR PROYECTO** (TC2, Medidas 2, Tecnología, SCI, Electrónica Industrial) + el **Proyecto Final 2027** (sin definir) + los proyectos reales (datalogger GIMAP, galgas, harvesting, FrioSeguro). La jugada correcta NO es hacer 6+ proyectos independientes: es **hacer que cada final-por-proyecto y el Proyecto Final SEAN piezas de los proyectos reales**. Un solo esfuerzo, crédito doble o triple: la uni convalida lo que Dreyfus/GIMAP/FrioSeguro ya necesitan. Ejemplos de mapeo candidato (a validar con cada profesor — Matías tiene los contactos):
- **Medidas Electrónicas 2** → caracterización y calibración del datalogger de vibración/galgas (incertidumbre, trazabilidad, fs real, ruido).
- **Teoría de Circuitos 2** → análisis del front-end analógico (INA333, puente de Wheatstone, filtros) o del harvesting piezo (LTC3588, supercaps, transferencia).
- **Tecnología** → la PCB del datalogger o de FrioSeguro: materiales, procesos, DFM.
- **SCI** → integración SCADA/alertas del sistema de galgas (ya casi lo tiene con el dashboard redler).
- **Electrónica Industrial** → instrumentación del REDLER: lazo 4-20mA/HART equivalente, P&ID de la instalación.
- **Proyecto Final 2027** → candidatos naturales: el datalogger inalámbrico de vibración/deformación completo (con aval GIMAP y cliente real Dreyfus) o el sistema de harvesting piezo aplicado.
El `@utn` consigue los requisitos de cada final-por-proyecto con los profesores y el Director asigna cada pieza al especialista que corresponda.

## 🎯 Plan Julio → Octubre (v1, 2026-07-07)

**Julio (vacaciones = ventana de oro):**
1. Semana 1-2: cerrar y ENTREGAR los 2 TPs integradores (SCI antes del 1-ago con margen). En paralelo, banco de pruebas galgas: galga física + LiPo real.
2. Semana 3-4: RX completo de galgas-supabase + OTA A/B. FrioSeguro: validar SIM800/OTA en hardware con el stock que ya hay.
3. Continuo: conseguir consignas de TC2/Medidas2/Tecnología ANTES de que arranque el cuatri.

**Agosto:** arranca cursado → régimen mixto. Galgas: pruebas de robustez (WiFi industrial, reconexión, NVS tras cortes). FrioSeguro: primera instalación comercial en un comercio de Bahía (carnicería/farmacia) con las 5 placas.

**Septiembre:** pre-parada: ensayo general del sistema completo de galgas + SCADA redler integrado + checklist de instalación en campo. RuView/datalogger si suma a la parada, sino post-octubre.

**Octubre:** PARADA DE PLANTA. Todo lo demás se congela esa semana.

**Reglas del plan:** WIP=1 por dominio · nada se declara "hecho" sin evidencia verificable · cada sesión deja bitácora actualizada · el Director re-prioriza cada semana, no cada hora.

## 🕳️ Huecos conocidos del sistema (auditoría 2026-07-07 — el Director los persigue hasta cerrarlos)
1. **GIT + BACKUP OFFSITE — el riesgo más grande de todos.** Cosechador sin git, repos con copias triple-anidadas y ZIPs como "versionado", todo en UN disco local. Si el disco muere, se pierden años. Fix barato: GitHub privado (gratis) para galgas-supabase, RuView, FrioSeguro, cosechador y MATI-HQ + `git push` como hábito de cierre de sesión. UNA mañana lo deja resuelto.
2. **El sistema de agentes está SIN PROBAR (cold-start).** Nadie verificó aún que una sesión nueva en otra carpeta cargue el modo Director y encuentre todo. Test: abrir Claude en el Escritorio y decir "¿qué hacemos hoy?". Si algo falla, arreglar el harness.
3. **Fecha y logística de la parada de OCTUBRE.** No hay fecha exacta, ni lugar confirmado (¿General Lagos como en febrero? = viaje a Santa Fe), ni definición de quién va de GIMAP. Sin esto, "octubre" no es un plan, es una intención. Preguntar YA en GIMAP.
4. **Consignas reales pendientes.** El plan académico se apoya en supuestos hasta que los profesores respondan: requisitos de los 5 finales-por-proyecto, consigna del labo de Control, y el REGLAMENTO del Proyecto Final (alcance, tutores, si acepta trabajo con empresa/GIMAP).
5. **Lado legal de cobrar:** monotributo/facturación para los abonos, y un **contrato simple de FrioSeguro con límite de responsabilidad** ("el servicio avisa, no garantiza la mercadería") — SIN eso, un freezer perdido puede convertirse en un reclamo contra Matías. Redactar antes del primer abono cobrado.
6. **Seguridad antes de vender:** credenciales hardcodeadas en repos (Supabase anon en RuView, `CREDENCIALES.txt`, defaults de FrioSeguro), bucket firmware público. Barrida de higiene antes del primer cliente pago.
7. **Decisión CV/trabajo:** `buscar_empleos.py` sigue corriendo — ¿el objetivo 2026 es conseguir laburo remoto o construir ingreso propio? Son estrategias distintas que compiten por las mismas mañanas. Matías debe elegir el default (el otro pasa a oportunista).
8. **Carpetas sin analizar** (posible material valioso): `GALGAS POST DREY (2)`, `GIMAP`, `Datalogger Acelerometro4`, `Refineria`, `CHUBON`, `TALLER EURO`, `Proyecto Android SO`.

## 📚 Documentos del cuartel (leer según necesidad)
- `MAPA_PROYECTOS.md` — TODAS las rutas del disco: cada repo, sus archivos clave, sus reglas y trampas. **El próximo agente empieza por acá si no conoce el terreno.**
- `PLAN_MES.md` — plan día por día 7-jul → 18-ago (v2 con calendario UTN real).
- `CALENDARIO_UTN_2026.md` — fechas oficiales UTN (llamados, feriados, inicio clases 18-ago).
- `PLATA.md` — plan de monetización: FrioSeguro como abono (línea 1), Modulia, servicios industriales post-octubre. Métrica única: abonos activos.
- `dominios\*.md` — bitácoras de los 6 especialistas.

## 📓 Bitácora del Director
Formato: `fecha — qué pasó / qué se decidió / próximo paso`

- 2026-07-07 — Sistema creado. Análisis completo de 8 repos hecho por Claude Fable (detalle en dominios/*.md). Deadline crítico detectado: SCI 1-ago. Próximo paso sugerido: sesión de cierre de TP SCI + pedir a Matías las consignas de TC2/Medidas2/Tecnología y la fecha exacta de la parada de octubre.
- 2026-07-13 — **SESIÓN GRANDE: FrioSeguro renació en nube nueva y las 2 placas quedaron E2E online.** (1) Mergeados 2/3 branches nocturnos (secret-scan #6, linter #4) tras veredicto @verificador; resumen-mensual #11 quedó MERGE-CON-FIXES (falta RLS + mensaje cobertura 0%). (2) El Supabase viejo fue ELIMINADO por Matías → se bootstrapeó proyecto nuevo **MATIAS (cjdluhemschrynijzvap)** vía Management API con SETUP_COMPLETO + OTA + 3 fixes de schema descubiertos con hardware real (`migration_fixes_2026-07-13.sql`). (3) Dashboard deployado en **frioseguro-dashboard.vercel.app** (admin+cliente; user admin = alegrematiasdev1@gmail.com). (4) **Placa 1 flasheada por USB, Placa 2 flasheada POR AIRE** (portal cautivo + POST /update — sin cable, tenía el USB bloqueado por el SIM800); ambas registradas y online con lecturas cada 10 s. Arquitectura completa en `frioseguro/docs/ARQUITECTURA_2026-07-13.md`. **Deudas nuevas**: rotar bot Telegram, password al /update, firmware sube wifi_password (sacar), flash al 98%, sondas sin soldar, decidir si desoldar SIM800 de Placa 2. La decisión de marca (nombre ≠ FrioSeguro) sigue pendiente.
- 2026-07-13 — **PENDIENTES HUMANOS de Matías (anotados en vivo, no los hace ningún agente):**
  1. **Paco**: pasarle una forma de **reactivar él mismo la Supabase** (free tier se pausa por inactividad → opciones: acceso al dashboard con su cuenta como member, o instructivo de 2 pasos "entrar → Restore project". El Director puede preparar el instructivo; el contacto es de Matías).
  2. **Lucas (GIMAP)**: mandarle mensaje — después le lleva el **ESP en modo AP para el sensor que él tenía**; preguntarle si quiere **SSID y contraseña específicos** o le da igual cualquiera.
  3. **Taller Cassano**: hablarle — coordinar **cuándo le queda cómodo que Matías pase** y confirmar **la dirección/dónde hay que ir**.
- 2026-07-07 (cierre de sesión Fable) — Sistema COMPLETO entregado: modo Director global (`~/.claude/CLAUDE.md`), 7 agentes, MATI-HQ con PORTFOLIO/PLAN_MES v2/CALENDARIO/MAPA/PLATA/6 dominios. Calendario UTN real incorporado (feriados 9-10 jul; receso 20-31 jul; finales 3-7 y 10-14 ago; clases 18-ago). Inventario completo registrado (26 MCUs, 10 relés, analizador lógico). Matías sigue con Opus 4.6. **DECISIONES PENDIENTES DE MATÍAS: (1) qué final rinde en agosto, (2) precios FrioSeguro, (3) fecha exacta de la parada de octubre, (4) qué hay en las carpetas no analizadas (GALGAS POST DREY (2), GIMAP, Datalogger Acelerometro4, Refineria, CHUBON).** Primera acción del plan: esta noche checklist TP SCI + inscripción a las 5 materias.
