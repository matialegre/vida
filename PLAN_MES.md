# PLAN MAESTRO — 7 julio → 18 agosto 2026 (v2, calendario UTN real)

> Del Director. WIP=1 por bloque. Si un día se cae, se corre el plan y se anota — no se apila.
> Fijo: oficina presencial 13:00–17:30 L-V (feriados nacionales = día completo libre). GIMAP a 5 cuadras. Herramental en casa y GIMAP.
> Calendario UTN: ver `CALENDARIO_UTN_2026.md`. Clases arrancan MAR 18-AGO. Finales: 3-7 ago y 10-14 ago.

## 🎯 Los 5 objetivos del período (reordenado 2026-07-07: DATALOGGER PRIMERO por orden de Matías)
1. **DATALOGGER (RuView) TERMINADO** — prioridad #1 de banco, antes del trabajo Dreyfus ("por las dudas"). **Alcance definido por Matías (2026-07-07): el datalogger lee MPU6050 + un canal PIEZOELÉCTRICO** (piezo como sensor de vibración, acondicionado con puente de diodos + capacitores — medición de envolvente/energía). Dreyfus se mide SOLO con galgas (sistema galgas-supabase, aparte). DoD: canal MPU + canal piezo logueando a SD sin gaps N horas + ECO-LoRa andando (duermen y siguen alcanzables) + consumo MEDIDO (INA219) + alcance/repetidor probado + decisión MicroPython vs C con benchmark. ⚠️ Front-end del piezo con protección: los piezos pican >20V (divisor/clamp + TVS — ver cosechador).
2. **TP SCI entregado** (cierre cátedra 1-ago) + TP EI cerrado — bloque liviano de las noches, no compite con el banco.
3. **UN FINAL rendido en agosto** (2° llamado 3-7 o 3° llamado 10-14) — materia a definir por Matías.
4. **galgas-supabase sin pendientes de software** + validado con galga y LiPo reales — arranca cuando el datalogger esté terminado (estimado: receso, semanas 3-4).
5. **FrioSeguro piloto real** (heladera de casa el feriado, un comercio después) — tareas cortas que no roban el bloque profundo.

**Regla de secuencia:** las MAÑANAS son del datalogger hasta cumplir su DoD; recién ahí entran las tareas de galgas (RX Task 08, galga física, LiPo). Los días de tabla siguen siendo válidos como lista ordenada de tareas — la prioridad de arriba manda sobre el día exacto. El sábado en GIMAP sirve a ambos (mismo banco, mismos instrumentos).

## 🕐 Día tipo (L-V laborable)
| Hora | Bloque | Qué |
|---|---|---|
| 08:00–08:20 | ☕ Director | Estado + LA tarea del día |
| 08:20–12:15 | 🔬 PROFUNDO | Banco/firmware (galgas → FrioSeguro) |
| 13:00–17:30 | 🏢 Oficina | Mundo Outdoor (intocable) |
| 17:30–18:15 | Corte real | Sin pantalla |
| 18:15–19:45 | 📄 LIVIANO | Uni: TPs → después ESTUDIO DEL FINAL |
| 19:45→ | Libre | Vida |

**Feriado/finde:** una sesión 09:00–13:00 y listo. Domingo: libre + 30 min de revisión con el Director (20:00).

## 📅 Semana 1 — 7 al 12 jul · "Feriados de oro"
| Día | Plan |
|---|---|
| Mar 7 | Hoy: sistema de agentes creado ✅. Noche: checklist TP SCI contra cuadernillo + **inscripción a las 5 materias del 2° semestre** (ya abrió) |
| Mié 8 | Mañana: galgas — leer `act.md`, levantar entorno, arrancar Task 08 RX (subscriber Realtime). Noche: completar huecos TP SCI |
| **Jue 9 🎉** | FERIADO — día completo: RX Task 08 entero (Realtime + LCD + buzzer). Evidencia: comando del dashboard mueve el RX |
| **Vie 10 🎉** | FERIADO — día completo: RX gateway HTTP local (server :80 + PATCH `local_ip`, PLAN v5) + TP SCI a plantilla docx |
| Sáb 11 | 🔬 GIMAP: **banco con GALGA FÍSICA + INA333** (adiós `DEV_SIMULATE_ADC`) vs `data/field_captures/` |
| Dom 12 | Libre. 20:00: revisión + **DECIDIR QUÉ FINAL se rinde en agosto** (con el Director) |
| Todos | ✉️ 10 min/noche: profesores — requisitos finales-por-proyecto (TC2/Medidas2/Tecnología) + consigna labo Sist. de Control + **confirmar acceso a GIMAP durante el receso (20-31 jul)** |

**DoD:** inscripto a las 5 · RX dejó de ser heartbeat-only · TP SCI en docx · galga real medida · final elegido.

## 📅 Semana 2 — 13 al 19 jul · "Entregar + hardware real"
| Día | Mañana | Noche |
|---|---|---|
| Lun 13 | Galgas: validar pipeline con galga real (umbral v_pp real vs 40mV) | Últimos retoques TP SCI |
| Mar 14 | Galgas: test **LiPo real** + presupuesto de energía medido | **ENTREGAR TP SCI** ✅ |
| Mié 15 | Galgas: re-flash ESP-B + OTA A/B diferenciada | TP EI: cierre |
| Jue 16 | Galgas: arrancar prueba de resistencia 24h (cortes inducidos) | TP EI: terminar |
| Vie 17 | FrioSeguro: compilar + flashear módulos nuevos (1 placa WiFi) | **ENTREGAR/CERRAR TP EI** ✅ + arranca ESTUDIO DEL FINAL (1° sesión: diagnóstico de qué sé) |
| Sáb 18 | 🔬 GIMAP: SIM800 con SIM real (aprovechar ANTES del receso por si cierra el lab) | — |
| Dom 19 | Libre | 20:00 revisión |

**DoD:** 2 TPs entregados · galgas con hardware real 24h estable · SIM800 probado con evidencia · plan de estudio del final armado.

## 📅 Semanas 3-4 — 20 al 31 jul · RECESO DE INVIERNO · "Galgas cerradas + final estudiado"
Régimen igual (la oficina no para por el receso de la uni). GIMAP: según lo que confirmen; si cierra, el trabajo de banco es en casa.
- **Mañanas (una por día, con evidencia):** galgas — migración SQL columnas nuevas · bucket firmware URL firmada · fix brownout USB · SCADA `redler/` integrado al dashboard · checklist de instalación de campo para octubre.
- **Noches:** ESTUDIO DEL FINAL (1,5h firmes). Con Claude: resúmenes, parciales viejos, simulacros.
- **Sáb 25:** 🔬 casa: **piloto FrioSeguro en tu heladera** — sonda + reed + dashboard + alerta Telegram, andando de punta a punta.
- **Dom 26 y week 4:** subir intensidad de estudio si el final es el 3-7 ago (simulacro completo el sáb 1-ago).

**DoD:** galgas-supabase sin pendientes de software · FrioSeguro piloto casero corriendo · final: simulacro aprobado antes del llamado.

## 📅 Semana 5 — 3 al 9 ago · "EL FINAL (2° llamado) + verificación SCI"
- **RENDIR EL FINAL** (día del llamado que corresponda; mañanas previas = repaso, se pausa el banco).
- Verificar cierre formal del cuadernillo SCI (venció 1-ago) y notas AD del 1° semestre (límite 10-ago).
- Resto de mañanas: RuView/datalogger — benchmark MicroPython vs C (decisión con evidencia) + driver INA219.
- Noches: FrioSeguro comercial — lista de 10 comercios, pitch de 1 página, precio. Contactar UNO para piloto (gratis 1 mes → abono).

## 📅 Semana 6 — 10 al 17 ago · "Colchón + pre-cuatri"
- Si el final fue al 3° llamado (10-14 ago): rendirlo acá. Si ya se rindió: segunda materia posible o banco.
- Consolidar respuestas de profesores → tabla CONVERGENCIA con requisitos reales → elegir candidato a **Proyecto Final** con GIMAP.
- Dom 17 (feriado lun): escribir el PLAN de régimen cursada (18-ago → octubre) con el Director: dónde entran galgas/parada cuando se cursa de nuevo.
- **Mar 18-ago: arrancan las últimas 5 materias.** 🎓

## ⚖️ Reglas
1. Mañana sagrada: ni mails, ni ERP, ni redes antes de 12:15. El ERP vive en la oficina salvo incendio.
2. Una tarea de banco por mañana. Termina antes → se adelanta la siguiente, no se abren dos.
3. El estudio del final desplaza al bloque liviano desde el 17-jul — los TPs ya van a estar entregados.
4. Compañeros = manos en paralelo (uno arma circuito mientras vos calibrás), no dirección.
5. Resultado de banco → bitácora del dominio el mismo día (5 min).
6. Dos días seguidos sin cumplir la mañana → avisarle al Director; se replanifica sin culpa.

## Bitácora del plan
- 2026-07-07 — v1 creada; v2 corregida con calendario UTN real (feriados 9-10 jul, receso 20-31 jul, finales 3-7 y 10-14 ago, clases 18-ago). Falta que Matías defina QUÉ final rinde en agosto.
