# PLAN MAESTRO — 7 julio → 18 agosto 2026 (v3, post-auditoría adversarial)

> Del Director. WIP=1 por bloque. Si un día se cae, se corre el plan y se anota — no se apila.
> Jerarquía oficial: **PLATA y UNIVERSIDAD primero**, octubre segundo (ver PORTFOLIO §👑).
> Calendario UTN: `CALENDARIO_UTN_2026.md` (única fuente de fechas). Clases: MAR 18-AGO. Finales: 3-7 y 10-14 ago.
> v3 aplica la auditoría 2026-07-07: track comercial con fecha única y temprana, hueco horario de venta, camino legal al cobro, checkpoint del TP, ERP = bloque oficina.

## 🎯 Los 5 objetivos del período (con metas VERIFICABLES)
1. 💰 **PLATA — FrioSeguro rodando:** piloto casero JUE 9-JUL · precio+pitch VIE 10-JUL · primera visita a comercio LUN 13-JUL · **meta realista: 1 piloto comercial instalado en julio, 1 abono COBRADO antes del 18-ago, 3 en pipeline** (la meta anterior "3 abonos antes del 18-ago" era aritméticamente imposible — auditoría #3).
2. 🎓 **UNI:** TP SCI ENTREGADO 14-jul (checkpoint duro 21-jul: si no está entregado, roba mañanas hasta que esté) · TP EI cerrado 17-jul · UN final rendido en agosto (llamados 3-7 / 10-14) · inscripción a las 5 materias ANTES del 14-ago.
3. 🔬 **Datalogger fase 1 (DoD acotado — auditoría #4):** benchmark MicroPython vs C + ECO-LoRa + INA219 = 2 semanas de mañanas. El front-end piezo y la prueba de alcance son fase 2 (receso). "Terminado" completo: ver `C:\Proyectos\datalogger\QUE_FALTA.md`.
4. 🏭 **Galgas rumbo octubre:** RX Task 08 + galga física + LiPo real — arranca cuando datalogger fase 1 cierre (~receso) o en huecos de banco.
5. 🏢 **ERP:** el bloque oficina (13-17:30) ES el ERP, punto — no se le suman horas nocturnas (auditoría #8). Norte: autonomía (soporte → agente IA).

## 🕐 Día tipo (L-V) — v3 con hueco de VENTA
| Hora | Bloque | Qué |
|---|---|---|
| 08:00–08:20 | ☕ Director | `git pull` + briefing (ya está en diario/) + LA tarea del día |
| 08:20–12:10 | 🔬 PROFUNDO | Banco: datalogger fase 1 → después galgas. **VIERNES: FrioSeguro/comercial** (2 mañanas equivalentes por semana para la plata) |
| **12:15–12:55** | 💰 **VENTA** | Camino a la oficina: UNA visita/gestión comercial (comercio, contador, ferretería). Lun y mié fijo; otros días si hay pendiente |
| 13:00–17:30 | 🏢 ERP | Mundo Outdoor — el bloque del ERP, completo acá |
| 17:30–18:15 | Corte real | Sin pantalla |
| 18:15–19:45 | 📄 LIVIANO **mono-tarea** | UNA sola cosa por noche: TP → después estudio del final. Mails a profesores: 10 min al final, no cuenta como tarea |
| 19:45→ | Libre | Vida. **A las 20:00 arranca el TURNO NOCHE de los agentes** (trabajan solos hasta las 7:00) |

**Sábado:** 09-13 banco (GIMAP) · tarde: slot de visita/instalación comercial si hay. **Domingo:** libre + 20:00 revisión semanal (30 min) con el reporte de tendencias.

## 🚨 ALERTA TP SCI (checklist 2026-07-07: `UNIVERSIDAD UTN\sistema de control industrial\CHECKLIST_ENTREGA_TP_SCI.md`)
El TP NO estaba casi listo: **~46h restantes** (9✅/20⚠️/17❌), con ~12h de LABORATORIO (faltan TODOS los archivos de proyecto reales: .dvp WPLSoft, .lsc LOGO!, MicroWin, RSLogix, CODESYS — lo "implementado" era pseudo-ladder en HTML) y el formato exige Word/plantilla (el HTML no vale como entrega; el cuadro de datos del alumno está VACÍO).
**Reajuste obligado (la UNI gana las mañanas — jerarquía PLATA+UNI):**
- **URGENTÍSIMO HOY/MAÑANA: mensaje a Conde para reservar laboratorio** — con receso 20-31 jul, el MAR 14-JUL puede ser el único día de lab antes del cierre 1-ago. Preguntar también si hay acceso en receso o primeros días de agosto.
- Los feriados 9-10 jul pasan a ser mayormente de TP SCI (WPLSoft .dvp + LOGO! .lsc + pasaje a Word con plantilla), no de banco. El piloto FrioSeguro casero (2h) se mantiene el jueves — es corto.
- Las mañanas de la semana 2 se reparten: TP SCI primero hasta bajar el riesgo, datalogger después. La entrega ya no es el 14-jul: **nueva meta de entrega: 28-31 jul** (checkpoint duro sigue 21-jul para medir avance).
- Riesgo de software: MicroWin/Designer 6 pueden no andar en Win11 → prever VM o PC del lab (resolver ANTES del martes de lab).

## 📅 Semana 1 — 7-12 jul · "Plata + RX + TP, todo arranca" (⚠️ leer ALERTA de arriba: los feriados son mayormente del TP)
| Día | Mañana/día | Mediodía 12:15 | Noche (mono-tarea) |
|---|---|---|---|
| Mar 7 | (hoy: sistema construido ✅) | — | Checklist TP SCI + **inscripción a las 5 materias** |
| Mié 8 | Datalogger: benchmark MicroPython vs C (arranque) | Comprar 2-3 **cajas estancas IP65** + prensacables | Completar huecos TP SCI |
| **Jue 9 🎉** | FERIADO doble: AM datalogger benchmark · PM **piloto FrioSeguro en TU heladera** (placa pelada, 2h) | — | TP SCI a plantilla docx |
| **Vie 10 🎉** | FERIADO: AM datalogger/galgas RX Task 08 · PM **PRECIO (3 escenarios, elegís uno) + pitch 5 renglones + borrador de contrato** con @comercial | — | Descanso o TP |
| Sáb 11 | 🔬 GIMAP: galga física + INA333 (banco galgas) | Tarde: identificar los 3 primeros comercios (caminando el barrio) | — |
| Dom 12 | libre | — | 20:00 revisión + decidir: **qué final rindo** + **CV/laburo remoto = pasivo** (matar scraper activo, auditoría #17) |

**DoD S1:** inscripto · piloto casero ANDANDO · precio fijado · pitch listo · TP SCI en docx · benchmark con veredicto.

## 📅 Semana 2 — 13-19 jul · "Primera visita + entregas + legal"
| Día | Mañana | Mediodía | Noche |
|---|---|---|---|
| Lun 13 | Datalogger: ECO-LoRa (diseño ventana RX) | 💰 **PRIMERA VISITA a comercio** (pitch + demo heladera en vivo) | **ENTREGAR TP SCI** ✅ |
| Mar 14 | Datalogger: ECO-LoRa implementación | Seguimiento visita / 2ª visita | TP EI: cierre |
| Mié 15 | Datalogger: driver INA219 + primera medición real | 💰 Visita 2/3 | TP EI: terminar |
| Jue 16 | Datalogger: consumo medido por estado (tabla) | Contador: **monotributo + facturación** (auditoría #7) | **ENTREGAR/CERRAR TP EI** ✅ |
| Vie 17 | 💰 FrioSeguro: flashear módulos nuevos en placa WiFi + checklist de instalación (se protocoliza acá) | Link de cobro de prueba (MercadoPago) | Arranca ESTUDIO DEL FINAL (diagnóstico) |
| Sáb 18 | 🔬 GIMAP: SIM800 con SIM real (antes del receso) | Tarde: **instalación del piloto comercial si hubo "sí"** | — |
| Dom 19 | libre | — | 20:00 revisión |

**DoD S2:** 2 TPs ENTREGADOS · ≥2 comercios visitados con precio dicho · monotributo en trámite + contrato borrador + link de cobro probado · datalogger fase 1 con ECO-LoRa e INA219 andando.

## 📅 Semanas 3-4 — 20-31 jul · RECESO · "Galgas + final + piloto convirtiendo"
- **Mañanas:** cierre datalogger fase 1 (prueba SD sin gaps N horas) → pasa a GALGAS: RX completo, LiPo real, prueba 24h con cortes, OTA A/B. Una tarea/día con evidencia. (⚠️ confirmar acceso GIMAP en receso — si cierra, banco en casa.)
- **Viernes + mediodías:** FrioSeguro comercial — visitas 4-6, seguimiento del piloto (¿el comerciante MIRA el dashboard? ¿le llegó una alerta?), ajustes de la vista mobile con @diseno/@frontend.
- **Noches:** ESTUDIO DEL FINAL 1h30 firmes (mono-tarea). **Checkpoint 21-jul:** TP SCI entregado sí o sí (si no → roba mañanas).
- **Sáb 25:** banco largo o instalación comercial 2.
- **Fin S4:** simulacro de final completo aprobado.

## 📅 Semana 5 — 3-9 ago · "EL FINAL"
- **RENDIR EL FINAL** (2° llamado; mañanas previas = repaso puro, banco pausado).
- Verificar cierre cuadernillo SCI (venció 1-ago) + notas AD 1° semestre (límite 10-ago).
- Mediodías: cobro del piloto → **conversión a ABONO** ("pasaron los 30 días: son $X/mes") + visitas si hay energía.
- Resto: galgas (lo que falte de QUE_FALTA).

## 📅 Semana 6 — 10-17 ago · "Colchón + pre-cuatri"
- 3° llamado si el final fue acá (o segundo final si el 1° salió bien y hay ganas).
- Tabla CONVERGENCIA con los programas REALES (`programas/RESUMEN_PROGRAMAS.md`): propuestas de 1 página para TC2 (¡su integrador es OBLIGATORIO y a consensuar!) y las electivas de Conde.
- Candidato a **Proyecto Final** elegido con GIMAP (el programa admite "desarrollos para empresas privadas" — el REDLER califica tal cual).
- Dom 17 (feriado lun): PLAN del régimen cursada (18-ago→octubre).
- **Mar 18-ago: arrancan las últimas 5.** 🎓

## 🌙 TURNO NOCHE (20:00–07:00 — los agentes laburan mientras Matías duerme)
Rutinas cloud (corren solas contra GitHub): **trabajador nocturno diario 02:00** (agarra la tarea de software más prioritaria de los QUE_FALTA, la implementa en un branch `nocturno/...`, deja el informe en diario/) · briefing Director 08:00 · investigación rotativa mié 18:00 · tendencias dom 18:00. A la mañana, el Director revisa el branch nocturno: lo que pasa por @verificador se mergea.

## ⚖️ Reglas v3
1. Mañana sagrada PERO el mediodía 12:15-12:55 es de la VENTA (lun/mié fijo) — la plata tiene hueco propio, ya no compite con el banco.
2. Una tarea de banco por mañana · una tarea por noche (mono-tarea, auditoría #8).
3. ERP = bloque oficina, completo ahí. Ni antes de las 12:15 ni después de las 18:15 salvo incendio.
4. Al arrancar CUALQUIER sesión: `git pull` (el turno noche y el briefing commitean solos — sin pull hay conflicto garantizado, auditoría #12).
5. Compañeros = manos en paralelo. Resultado de banco → bitácora el mismo día. Dos días caídos → replanificar con el Director, sin culpa.

## Bitácora del plan
- 2026-07-07 — v1 → v2 (calendario UTN real) → **v3 (cirugía post-auditoría adversarial de 20 hallazgos):** track comercial adelantado a semana 1 con fecha única, hueco de venta 12:15, camino legal al cobro en S2, meta de abonos realista, datalogger DoD acotado a fase 1, ERP = bloque oficina, noches mono-tarea, checkpoint TP 21-jul, turno noche de agentes.
