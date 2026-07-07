# PLATA — plan de monetización

> Del Director. Principio rector (heredado del @empresario del ERP): **la plata está en VENDER lo construido, no en construir más.** Todo acá abajo usa activos que YA existen.

## Los activos monetizables (hoy, sin construir nada)
1. **FrioSeguro**: 5 PCBs fabricadas + 20 sondas + 10 reed + cloud/dashboard/APK andando.
2. **ERP/Modulia**: en producción con 4 empresas, ~1.700 leads, 14 demos de rubro, equipo de agentes propio.
3. **Capacidad instalada**: 10 ESP32 + 5 Picos + 10 módulos relé + analizador lógico + IP fija + herramental completo.
4. **Credibilidad industrial**: GIMAP + instalación real en Dreyfus + sistema en Bunge/TBB + +40 equipos reparados.
5. **Marca personal**: CV v6, docente, "el pibe que hace de todo" en Bahía.

## 💰 Línea 1 — FrioSeguro como ABONO MENSUAL (plata más rápida y recurrente)
**Qué se vende:** "Monitoreo de frío 24/7 con alertas al celular" para comercios con heladeras/cámaras: carnicerías, panaderías, farmacias, veterinarias (vacunas), restaurantes, supermercados chinos, distribuidoras.
**El dolor real:** una cámara que se corta un fin de semana = cientos de miles de pesos en mercadería. Además bromatología exige registros de temperatura → **el sistema genera el registro solo** (argumento de venta demoledor para farmacias/alimentos).
**Modelo:** instalación (cubre hardware + 1 visita) + abono mensual por local (incluye alertas, dashboard, historial, soporte). Precios exactos los define Matías con el Director — referencia inicial a validar: instalación que recupere el costo del kit, abono que a 10 locales pague >1 sueldo junior.
**Capacidad actual:** 5 kits listos = 5 clientes ya, sin comprar NADA. Con 10 ESP32 + sondas de repuesto se arma la segunda tanda.
**Pasos (ya calzados en PLAN_MES):** piloto en heladera de casa (sáb 25-jul) → lista de 10 comercios + pitch de 1 página (sem 4) → 1 piloto real gratis 30 días → convertir a abono → repetir.
**Regla:** el primer cliente NO es el objetivo; el objetivo es el ABONO — contrato simple, débito/transferencia mensual, sin excepciones.

**Política de prueba gratis (definida 2026-07-07, NO ablandar):**
- **UN solo piloto gratis** (máximo 2), de **30 días** — 30 y no 14, porque necesita atravesar al menos un susto/evento real (una puerta abierta, un corte) para que el cliente SIENTA el valor. Las alertas van al celular DEL CLIENTE desde el día 1.
- Al instalar se pacta el precio: "gratis 30 días, después son $X/mes o lo retiro" — el número se dice ANTES, no al final.
- **Del cliente 2 en adelante SE COBRA desde el día 1**, con garantía "si en 60 días no te sirvió, te devuelvo todo". El piloto gratis fue para tener la referencia; dos gratis es regalar el producto.
- El piloto se elige estratégico: comercio conocido, visible, que dé referencia ("lo tiene la carnicería X, preguntale").

**Manejo de la objeción "¿dónde lo tenés andando?" (3 capas, todas verdaderas):**
1. Demo en vivo: MI heladera en el dashboard, desde el celu, ahora.
2. "El sistema lo desarrollé para un campamento minero de Panamerican en Santa Cruz" (origen real — decir *desarrollado para*, no "instalado" hasta que sea cierto).
3. "Instalo sistemas industriales — equipos míos corren en Louis Dreyfus con la UTN (GIMAP)."
Desde el cliente 2: capa 4 = "lo tiene [piloto] acá a N cuadras, preguntale".

## 💰 Línea 2 — ERP/Modulia (la máquina grande, ya tiene equipo)
No se gobierna desde acá (equipo propio + @empresario). Lo que el Director vigila: que cada semana haya AL MENOS una acción comercial de Modulia (outreach, demo, cobro) — porque técnica ya sobra y venta es lo que falta. TallerEuro y Cassano demuestran que se vende. El ERP además es escaparate: cada cliente de FrioSeguro es lead potencial de Modulia (y viceversa — misma visita, dos productos).

**El MISMO playbook que FrioSeguro aplica acá (2026-07-07):**
- Objeción "¿dónde anda?": acá es todavía más fuerte — *"lo usa todos los días una cadena de retail de 13 locales con 23 usuarios hace 2 años, más un taller (TallerEuro), Montagne y Cassano"*. Con permiso de los dueños, esa referencia con nombre vale oro.
- Trial: demo del rubro + **30 días de prueba con precio pactado ANTES** ("después son $X/mes o se da de baja"). Nada de trials eternos: trial sin fecha de conversión = cliente gratis para siempre.
- Un solo "gratis extendido" por rubro nuevo (para tener LA referencia del rubro); del segundo cliente del rubro en adelante, se cobra desde el arranque con garantía de devolución.
- La métrica es la misma: **abonos activos**, no demos creadas ni features nuevas.

## 💰 Línea 3 — Servicios industriales vía GIMAP (ticket alto, ciclo lento)
**Qué se vende:** monitoreo de vibración/deformación como servicio (datalogging + informe) para plantas: exactamente lo que ya hace para Dreyfus. Con el datalogger RuView terminado, un "estudio de vibraciones de N días con informe" es un servicio empaquetable de ticket alto.
**Cuándo:** DESPUÉS de octubre — la parada es la credencial de venta ("sistema probado en parada de planta de Louis Dreyfus"). No perseguir esto antes.

## 💰 Línea 4 — Relés + reed switches = automatización simple de comercios (oportunista)
Con 10 módulos de relé: control remoto de bombas/luces/portones/hornos + "alerta puerta de cámara abierta". NO como producto propio nuevo (sería dispersión) sino como **upsell en la misma visita de FrioSeguro**: "¿querés que la sirena también te avise si quedó la puerta abierta? ¿prender/apagar X desde el celu?" — mismo firmware, mismo dashboard, abono levemente mayor.

## ❌ Qué NO hacer por plata (dispersión disfrazada de ingreso)
- Trabajos one-off de electrónica a medida baratos (riego, dimmers sueltos): consumen las mañanas de oro y no dejan abono. Solo si pagan MUY bien o suman al portfolio.
- Reventa de componentes / armado de kits: margen bajo, tiempo alto.
- Construir un producto NUEVO antes de que FrioSeguro tenga 5 abonos activos.

## 🥇 Métrica única de esta línea de trabajo
**Abonos mensuales activos** (FrioSeguro + Modulia). Todo lo demás es vanidad. Metas (corregidas por auditoría 2026-07-07 — las anteriores eran aritméticamente imposibles con el trial de 30 días): **1 piloto comercial instalado en julio · 1 abono COBRADO antes del 18-ago · 3 en pipeline al 18-ago · 3-5 abonos activos antes de octubre.** Fechas de largada (únicas, alineadas con PLAN_MES v3): piloto casero 9-jul · precio+pitch 10-jul · primera visita 13-jul.

## Canal WhatsApp (decisión 2026-07-07)
**1 celu + 1 chip comercial dedicado con WhatsApp Business** (gratis; perfil de empresa, catálogo, etiquetas). El personal queda personal. NADA de 5 chips ni emuladores (ban de Meta casi seguro + problema que no existe: el cuello es tener abonos, no mandar mensajes). La venta de FrioSeguro es presencial; WhatsApp = follow-up. El outreach de Modulia ya lo hace el número secundario del ERP (OpenClaw, @whatsapp-comms) — no duplicar. Escalar a WhatsApp Business API (oficial, paga) recién con 10+ abonos.

## 👥 ¿Cuándo necesito GENTE? (pedido de Matías 2026-07-07 — el Director DEBE evaluar esto en cada hito)
Principio: **los agentes de IA hacen todo lo que no requiera cuerpo o confianza humana cara a cara.** Se contrata gente solo cuando aparece una señal medible, nunca "por las dudas". El Director revisa esta sección al llegar a cada hito de abonos (5 → 15 → 30) y después de octubre.

**Señales de que SÍ hace falta una persona (y qué persona):**
- **Vendedor** (primero a COMISIÓN pura, sin sueldo fijo): cuando haya pitch probado + 5 abonos + lista de leads que Matías no llega a visitar. Un vendedor sin producto probado quema leads; un vendedor con casos reales imprime. El ERP ya contempla esto (@empresario habla de "Agus / vendedor a sumar") — puede ser LA MISMA persona vendiendo Modulia + FrioSeguro en la misma visita.
- **Técnico instalador** (por instalación, no sueldo): cuando las instalaciones de FrioSeguro superen ~2/semana o haya que instalar fuera de Bahía. Candidatos naturales: compañeros de la uni (ya identificados como recurso). La instalación se protocoliza ANTES (checklist + fotos) para que no dependa de Matías.
- **Soporte/atención**: recién cuando los reclamos interrumpan las mañanas de oro más de 2 veces/semana. Antes de contratar: automatizar con agente + WhatsApp Business.
- **NUNCA contratar para**: desarrollo de software/firmware (eso es de los agentes + Matías), diseño, marketing genérico, "ayuda general".

**Regla de oro:** cada contratación se paga sola con ingresos EXISTENTES (comisión % de venta, monto fijo por instalación) — cero sueldos fijos hasta que el recurrente los cubra 2×. Matías decide siempre; el Director solo presenta la señal, los números y un recomendado.

## Bitácora
- 2026-07-07 — Documento creado. Próxima acción de plata: piloto casero FrioSeguro (sáb 25-jul según PLAN_MES) y lista de 10 comercios (sem 4). Matías define precios con el Director antes del primer contacto.
