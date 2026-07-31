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
- 2026-07-13 (tarde) — **RECORDATORIO HOY MISMO: mandar el mensaje de la RÉPLICA DE LA PLACA DE LA FUENTE** (pedido de Matías en vivo — es PARA HOY, no dejar pasar).
- 2026-07-13 (tarde) — **Hardware Placa 1 (sin SIM), anotado por Matías**: (a) le FALTA LA TIERRA en el borne **TB A6** — necesaria para conectar relé o sensor de puerta → soldarla antes de usar esas funciones (dueño: Matías/@hardware); (b) para 3 sondas de temperatura YA ESTÁ lista. No mucho más pendiente en esa placa.
- 2026-07-13 — **PENDIENTES HUMANOS de Matías (anotados en vivo, no los hace ningún agente):**
  1. **Paco**: pasarle una forma de **reactivar él mismo la Supabase** (free tier se pausa por inactividad → opciones: acceso al dashboard con su cuenta como member, o instructivo de 2 pasos "entrar → Restore project". El Director puede preparar el instructivo; el contacto es de Matías).
  2. **Lucas (GIMAP)**: mandarle mensaje — después le lleva el **ESP en modo AP para el sensor que él tenía**; preguntarle si quiere **SSID y contraseña específicos** o le da igual cualquiera.
  3. **Taller Cassano**: hablarle — coordinar **cuándo le queda cómodo que Matías pase** y confirmar **la dirección/dónde hay que ir**.
- 2026-07-30 (nocturno-local-b, 2do turno) — **Auditoría (evaluador) de las auto-resoluciones del 1er turno: 3 de 8 duplicaban un bullet — arreglado en el harness.** Pase adversarial sobre la salida del generador de las 07-30 (generator≠evaluator). El reporte del 1er turno verificó "0 marcadores de conflicto" pero **no 0 duplicados** — hueco clásico del `merge --union`. Hallado: en 3 resoluciones (galgas `07-29`, frioseguro `07-11-b` y `07-13`) el bullet `EN BRANCH \`X\`` quedaba **repetido**, porque `main` ya documentaba ese branch (con otra redacción, vía sync posterior) y la union sumaba ambas anotaciones — sin marcador, invisible al chequeo de anoche; un humano drenando a ciegas commiteaba la bitácora con el bullet doble (P0 galgas / P1 frioseguro). **Fix en `tools/resolve_doc_conflicts.py`** (harness engineering, no parche a mano): funciones puras `en_branch_refs` + `dedup_en_branch` que descartan la anotación repetida y **conservan la de main**; cableadas a `union_merge_file`/`build_plan`/reporte. **Verificado (git real):** 8 resoluciones regeneradas → **0 duplicados** + **0 marcadores**; las 3 subsumidas quedan **idénticas a main** (`diff` 07-29 = vacío) — su cambio de docs ya vivía ahí, el valor real del branch (código/tests) entra igual merge-a-limpio aparte; 4 repos intactos (read-only). Tests: `test_resolve_doc_conflicts` **13→20 OK**, `test_merge_queue_status` 23/23 (reuse intacto). Reporte `COLA_MERGE_RESOLUCIONES.md` regenerado con notas 🧹; banner 07-30-b en `COLA_MERGE_NOCTURNOS.md`. Sin branch (tooling del cuartel). Detalle: `diario/nocturno-local-2026-07-30-b.md`.
- 2026-07-30 (nocturno-local) — **Los 8 conflictos-docs de la cola YA vienen pre-resueltos: el drenaje de día quedó mecánico de punta a punta (ataca el cuello #1, sin sumar branch).** Paso siguiente al *clasificar* (07-29-b): *resolver* de antemano. Escrito `tools/resolve_doc_conflicts.py` (MATI-HQ main, stdlib, reutiliza los helpers de `merge_queue_status.py`): para cada branch `nocturno/*` que da **CONFLICTO 100% en docs** (los 8 de la cola: 6 galgas + 2 frioseguro, todos por `QUE_FALTA.md`), reconstruye ours/base/theirs y los funde con **`git merge-file --union`** (toma ambos lados, sin marcadores) → deja el `.md` fusionado en `COLA_MERGE_RESOLUCIONES/<repo>/<branch>/` + los comandos exactos de drenaje. Si un branch chocara en código lo **SALTEA** (jamás auto-resuelve código; hoy 0 salteados). **Verificado (git real):** 8 resoluciones, **0 marcadores de conflicto**, cada una conserva **tanto** el avance de main (bullets 07-28-b/07-29) **como** la línea nueva del branch → no revierte nada; los 4 repos intactos (read-only, no mergea). Tests: `python -m unittest tools.test_resolve_doc_conflicts` **13/13 OK** + `test_merge_queue_status` 23/23 (el reuse no rompió nada). Con esto los 8 "conflictos" pasan de merge-a-mano a **revisar-y-copiar**; sumado a 9 LIMPIO-ADITIVO + 10 stale-docs, el único trabajo humano real que queda son los ~3 branches que tocan código. Reporte: `COLA_MERGE_RESOLUCIONES.md` + banner 07-30 en `COLA_MERGE_NOCTURNOS.md`. Sin branch (tooling del cuartel). Detalle: `diario/nocturno-local-2026-07-30.md`.
- 2026-07-29 (nocturno-local-b, 2do turno) — **Cola de merge hecha DRENABLE: el tool ahora dice qué conflicto es trivial y cuál es real (ataca el cuello #1 sin sumar branch).** Con los 4 repos saturados de análisis offline (34 branches nocturnos sin mergear; galgas 6 noches seguidas; PLATA comercial completo), la jugada de mayor palanca no era un branch #35 sino **drenar**. Corregí+extendí `tools/merge_queue_status.py` (MATI-HQ main, como el 07-27-b): (1) **bug de conteo** — reportaba "3 archivos en conflicto" donde había 1 (metía las líneas informativas `Auto-merging`/`CONFLICT` de git como archivos); ahora corta en la línea en blanco; (2) **clasificación doc-vs-código** (`is_doc`/`collision_kind`, puras+testeadas) → cada conflicto/colisión etiquetada `[SOLO docs]`/`[codigo]`/`[doc+codigo]`; (3) rollup accionable + salida ASCII-safe. **Hallazgo que des-asusta la cola (git real):** de 34 branches, **8 CONFLICTO y los 8 son SOLO `QUE_FALTA.md`** (0 tocan firmware); 14 REVISAR-STALE, 10 solo-docs; 9 LIMPIO-ADITIVO. El atasco de galgas es **bitácora, no código** → se resuelve tomando ambos lados del `.md`. Orden de drenaje escrito en `COLA_MERGE_NOCTURNOS.md` (banner 07-29). Verificado: `python -m unittest tools.test_merge_queue_status` **23/23 OK** (+11 nuevos) + corrida en vivo. Reporte fresco: `COLA_MERGE_STATUS_2026-07-29.md`. Sin branch (es tooling del cuartel). Detalle: `diario/nocturno-local-2026-07-29-b.md`.
- 2026-07-29 (nocturno-local) — **Umbrales de v_pp de galgas revalidados contra la señal REAL de campo (P0-octubre, #2).** Hasta hoy el v_pp se calibraba contra un comentario del simulador (`config.h:108`), no contra el terreno. Escrito `tools/analyze_vpp_field.py` (galgas, stdlib, **read-only** sobre las capturas Dreyfus sagradas) que reconstruye la ventana EXACTA del firmware (500 muestras = 1 s, `BURST_SAMPLES_NORMAL`) y mide el v_pp real; + 9 tests + `docs/vpp-field-characterization.md`. **Dos hallazgos:** (1) el v_pp real es **≤14 mV mediana en toda condición normal** → el ALERT de 40 mV tiene margen enorme y el fix MONITOR=35 mV del 07-28-b queda **validado, hasta conservador** (el "30 mV" era pesimista); (2) **cry-wolf latente en el firmware v3 [@firmware]** — el self-trigger (`v_pp>40mV`, 1 burst, **sin hold**) convierte los dropouts de 0.0 V (1.2 % de las muestras con motor ON) en **ALERTAS espurias** (3.0 % de los segundos; 0 % con un guard de rango). El legacy tenía `HOLD_SEC=1.5s`, el informe §9.2 pide 2–3 s. **No aplicado de noche** (generator≠evaluator): fix candidato documentado (guard de outliers y/o restaurar hold) para confirmar en banco. **Branch `nocturno/local-2026-07-29-vpp-field-characterization`** (galgas, commit `877390b`) + puntero en `main` (commit `b717127`). Detalle en `diario/nocturno-local-2026-07-29.md`.
- 2026-07-28 (nocturno-local-b, 2do turno) — **Cry-wolf del SCADA de galgas corregido (P0 octubre, "la cara que Dreyfus ve").** La vista Planta (`PlantaView.jsx`) clasificaba las cards con `TH_VPP_MONITOR=20mV`, por DEBAJO del vpp de reposo documentado (~30mV, `config.h:108`) → **ámbar "MONITOREO" permanente en operación normal** = desensibiliza al operario. Corregido a 35mV (30mV reposo + 1σ ruido 5mV, 5mV bajo el ALERT de 40mV que NO se toca) → imposible causar alerta perdida. De paso cerré el **drift del item #9** de `QUE_FALTA.md` (decía "integrar SCADA — pendiente" cuando ya vive integrado en PlantaView). Verificado offline: `web/ npm run build` OK. **Branch `nocturno/local-2026-07-28-b-scada-monitor-threshold`** (galgas) + puntero en `main` (commit `bbe095f`). Falta (campo): validar el borde exacto contra `field_captures` con señal real [@muestreador+@diseno]. Detalle en `diario/nocturno-local-2026-07-28-b.md`.
- 2026-07-27 (nocturno-local-b, 2do turno) — **Tool que regenera la cola de merge en vivo + hallazgo que corrige la COLA_MERGE del 07-24.** Escrito `tools/merge_queue_status.py` (MATI-HQ, stdlib, solo lectura): mide cada branch `nocturno/*` con la **métrica correcta de merge** (3-way real `merge-tree --write-tree` → diff vs main), no el `git diff main..branch` (two-dot) que engaña. Corriéndolo se desmintió la alarma central del doc a mano: los 8 branches STALE de datalogger **NO borran `misiones/`** — **0 de 32 branches borra un solo archivo** (verificado con git). Estado real: 19 LIMPIO-ADITIVO, 8 REVISAR-STALE, 2 CONFLICTO (frioseguro resumen-mensual), 1 BINARIOS (galgas 07-09), 1 SUBSUMIDO, 1 YA-EN-MAIN (galgas 07-21-b = rama huérfana en el tip de main). 12 tests de `classify()` OK. Reporte: `COLA_MERGE_STATUS_2026-07-27.md`; banner de corrección en `COLA_MERGE_NOCTURNOS.md`. **Ataca el cuello #1 (drenaje humano): 27/32 mergeables sin drama → una sesión con @verificador baja la cola fuerte.** Detalle en `diario/nocturno-local-2026-07-27-b.md`.
- 2026-07-27 (nocturno-local) — **Drift del README de galgas corregido (item #14, P0 octubre).** Con datalogger 100% triado y el provisioning de FrioSeguro completo, el valor nocturno de producir modelos/tests está agotado (el cuello es merge humano). Tomé el fallback documentado: el `README.md` de galgas mentía ("scaffolding esperando contexto", ruta muerta `GALGAS CON SUPABASE`, pointer roto `PLAN_v2_DEFINITIVO.md`) cuando el sistema está validado E2E en banco → reescrito reflejando el estado real (A 0.1.3/B 0.1.1/RX heartbeat), designando `act.md` fuente de verdad; 14/14 pointers verificados. **Branch `nocturno/local-2026-07-27-readme-drift`** (galgas, solo docs, el más barato de drenar). Detalle en `diario/nocturno-local-2026-07-27.md`.
- 2026-07-24 (nocturno-c) — **COLA DE MERGE creada: `COLA_MERGE_NOCTURNOS.md`.** Hay **26 branches nocturnos sin mergear** (galgas 10, datalogger 8, frioseguro 7, cosechador 1), casi ninguno en main — el cuello de botella que los informes venían marcando, ahora cuantificado con git real. Hallazgos: datalogger 🔴 STALE (8 branches 6-8 commits atrás, nunca rebaseados → merge naïve revierte firmware); 2 pares redundantes (frioseguro 07-11-b⊂07-13; datalogger 07-09≈07-15 sd-integrity); galgas 07-09 arrastra binarios de build. galgas+cosechador sanos (drenaje mecánico). **Próximo paso: sesión de drenaje con @verificador siguiendo el orden del doc (PLATA/octubre primero).** Detalle en `diario/nocturno-local-2026-07-24-c.md`.
- 2026-07-07 (cierre de sesión Fable) — Sistema COMPLETO entregado: modo Director global (`~/.claude/CLAUDE.md`), 7 agentes, MATI-HQ con PORTFOLIO/PLAN_MES v2/CALENDARIO/MAPA/PLATA/6 dominios. Calendario UTN real incorporado (feriados 9-10 jul; receso 20-31 jul; finales 3-7 y 10-14 ago; clases 18-ago). Inventario completo registrado (26 MCUs, 10 relés, analizador lógico). Matías sigue con Opus 4.6. **DECISIONES PENDIENTES DE MATÍAS: (1) qué final rinde en agosto, (2) precios FrioSeguro, (3) fecha exacta de la parada de octubre, (4) qué hay en las carpetas no analizadas (GALGAS POST DREY (2), GIMAP, Datalogger Acelerometro4, Refineria, CHUBON).** Primera acción del plan: esta noche checklist TP SCI + inscripción a las 5 materias.
