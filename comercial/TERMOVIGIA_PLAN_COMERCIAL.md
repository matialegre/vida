# TERMOVIGÍA — Plan comercial de relanzamiento (3 socios, 5 equipos)

> @comercial · 2026-09-01. Doctrina: `PLATA.md` (Línea 1). Tarifa vigente: `C:\Proyectos\frioseguro\TERMOVIGIA.md` §3 (v4, ÷3 del 31-08).
> Métrica única: **abonos mensuales activos.** Todo lo que sigue se mide contra eso.
> **Todo lo de plata entre socios es PROPUESTA** para que Matías lo charle con Gonza y Sergio. Matías decide el número final.

Contexto en una línea: hay producto probado en la heladera de Matías y un reefer en Cerro Moro; hay un lead escrito (Venado Tuerto, folleto listo para el mié 2-sep); el pipeline de Bahía está **vacío** hace dos meses (`frioseguro_ESTADO_2026-08-31.md` §5); y ahora hay tres pares de manos. El cuello de botella ya no es armar equipos: es **poner equipos en cámaras ajenas con un abono firmado**.

---

## 1. Reparto de roles y de plata entre los 3 (PROPUESTA)

### 1.1 Quién hace qué por semana

| | Matías | Gonza | Sergio |
|---|---|---|---|
| **Rol** | Ingeniería, software, nube, precios, decisiones. Cierra por videollamada. | Producción: arma, prueba en banco y documenta cada equipo. | Calle: demos presenciales en Bahía, instalación, primera línea de soporte. (*Si el perfil real es al revés — Sergio arma y Gonza vende — se invierten las columnas; lo que no se invierte es que UNO solo hace la calle.*) |
| **Por semana** | **Máximo 4 h** hasta el 31-oct (parada Dreyfus + UTN): 1 h reunión de socios (lun), 2 h cierres/videollamadas, 1 h precios y pipeline. | 1 equipo terminado y probado por semana como mínimo (5 en 5 semanas). Checklist de banco firmado por equipo. | 3 demos presenciales por semana (mar/jue/sáb) + follow-up WhatsApp + instalaciones. |
| **Entrega semanal** | Pipeline actualizado, decisiones tomadas, firmware/nube que la demo necesita. | Equipo N en caja, con número de serie, foto y checklist. | 3 fichas de demo llenas (§2.3), fechas de instalación. |

### 1.2 Lo que Matías NO hace (proteger el tiempo)
- No arma placas ni suelda. No compra componentes (lista la hace Gonza; Matías aprueba por WhatsApp).
- No hace visitas frías en Bahía. Entra a un comercio solo para cerrar (segunda visita) o si el cliente lo pide por nombre.
- No instala en Bahía. Ninguna instalación fuera de Bahía (regla ya escrita: instalación remota, kit preconfigurado + electricista local + videollamada).
- No hace soporte de primer nivel ("no me llegó la alerta") — eso es Sergio con un guion; a Matías llega solo lo que Sergio no resolvió en 24 h.
- No escribe folletos, mensajes ni contratos: los agentes (@comercial, @diseno) los producen y Matías aprueba.

### 1.3 Los dos esquemas de plata (números con tarifa vigente)

**Unidad de cuenta** (se usa en todo el documento): *equipo típico* = 1 cámara + 2 sondas + 1 puerta.
- Estándar: 25.000 + 2×4.000 + 3.000 = **$36.000/mes**. Depósito $150.000. Instalación $50.000.
- Premium: lo mismo + base Premium 15.000 + sirena 3.000 = **$54.000/mes**. Depósitos $330.000. Instalación $50.000.
- Mezcla supuesta 70 % Estándar / 30 % Premium → **abono promedio $41.400/mes por equipo**; depósito promedio $204.000.

**Costos recurrentes de la operación (con fuente):**
- Nube: Supabase Pro **USD 25/mes** (precio de lista; la línea comercial hoy está en free tier, que se pausa por inactividad — no sirve para clientes que pagan). A $1.535 (BNA vendedor, 1-sep-2026) = **$38.375/mes**.
- Dominio termovigia.com.ar: **$8.500/año** (NIC.ar, tabla oficial) = $708/mes.
- SIM por base Premium: Movistar M2M "MICRO 100" 100 MB + 100 SMS **$5.000/mes** (el más chico, MICRO 10 ECO 10 MB + 100 SMS, $2.900/mes). Tomo **$5.000/mes por base Premium**. Ojo: la voz no está garantizada en planes M2M — ver §4 y §6.
- Netlify, Telegram, WhatsApp Business (app): $0.
- Hardware Estándar: $30.000–45.000 por kit en componentes (`PRECIOS_FRIOSEGURO.md` §2, julio; Gonza lo recotiza esta semana). Premium: **sin cotizar** — Gonza cotiza batería + cargador + módulo 4G; el depósito de $180.000 que pone el cliente es lo que lo financia.

Total fijo: **$39.083/mes** + $5.000 por base Premium activa.

**Ejemplo con 15 equipos activos** (escenario B, mes 6): abonos $621.000/mes · costos $59.083 · **neto operativo $561.917/mes**.

| | **Esquema 1 — "Por equipo" (sin sociedad formal)** | **Esquema 2 — "Sociedad" (% fijo + sueldo de armado)** |
|---|---|---|
| Cómo funciona | Cada equipo tiene un "padrino" (quien lo armó e instaló). El padrino cobra **la instalación completa ($50.000)** y **25 % del abono** de ese equipo mientras esté activo; a cambio cubre reposición, visita técnica y soporte de primer nivel. Matías cobra el 75 % y paga nube, SIM, dominio, INPI. | Se cierra un porcentaje de utilidad: **Matías 50 % · Gonza 25 % · Sergio 25 %** (Matías aporta producto ya construido, nube, marca, capital; ellos manos y calle). Antes de repartir, el que arma e instala cobra un **sueldo de armado de $50.000 por equipo** (= la instalación, neutral para el pool). Costos salen del pool. |
| Con 15 equipos | Gonza + Sergio: 25 % × 621.000 = **$155.250/mes** entre los dos + $50.000 por cada equipo nuevo (2 en el mes 6 = $100.000). Matías: 75 % × 621.000 − 59.083 = **$406.667/mes**. | Utilidad $561.917 → Matías **$280.958** · Gonza **$140.479** · Sergio **$140.479**, más $50.000 por equipo a quien lo armó. |
| A favor | Simple, cada uno factura lo suyo (monotributo propio), incentiva a instalar rápido y a que el equipo no se caiga. Se arranca mañana. | Alinea a los tres con el total (a Sergio le conviene que Gonza arme, y viceversa). Escala mejor con vendedor externo. |
| En contra | Si Sergio vende y Gonza arma, hay que definir quién es "padrino" (propuesta: 15 % al que arma, 10 % al que instala/vende). Matías carga con todo el costo fijo. | Requiere sociedad (SAS) o un acuerdo escrito; contador; mayor fricción al arrancar. Con pocos equipos, 25 % de casi nada es nada. |
| **Recomendación** | **Arrancar con este** hasta 15 abonos activos. | Pasar a este cuando haya 15 abonos y la señal de vendedor externo (PLATA §"¿Cuándo necesito GENTE?"). |

Regla de oro (PLATA): nadie cobra sueldo fijo hasta que el recurrente lo cubra 2×. Ninguno de los dos esquemas tiene sueldo fijo.

---

## 2. Plan de los 5 equipos

### 2.1 Antes que nada: el maletín de demo (equipo 0)
Con **una de las 3 PCB WiFi que ya existen** (`hardware.md`), Gonza arma esta semana un **maletín de demo**: base en caja IP65, 1 sonda en cable de 1 m, 1 reed con imán suelto, fuente con ficha que se desenchufa a mano, vaso térmico. Es lo que Sergio lleva a cada comercio. La heladera de Matías queda como "el sitio que lleva meses andando" en el panel. Los 5 equipos nuevos van todos a clientes.

### 2.2 A quién va cada uno

| # | Perfil | Nivel | Condición | Por qué ese perfil | Candidato |
|---|---|---|---|---|---|
| **1** | Laboratorio / morgue / banco de sangre / vacunatorio con **auditoría** | **Premium** + registro | **Cobra desde el día 1** (regulado → paga fácil) | Cadena de frío regulatoria: no compra alertas, compra cumplimiento | **Venado Tuerto** si avanza; si no, laboratorio de análisis clínicos en Bahía |
| **2** | **Farmacia** (heladera de vacunas/insulina) | Estándar (+ WhatsApp $8.000) | Cobra desde el día 1, garantía 60 días | ANMAT/COFA piden registro diario; descartar un lote vale más que un año de abono | Del formulario §2.3 |
| **3** | **Carnicería / fiambrería / frigorífico chico** conocido y visible | Estándar + sirena | **EL ÚNICO PILOTO GRATIS**, 30 días, precio pactado antes ("después son $36.000/mes o lo retiro") | Referencia de calle: "lo tiene X a 3 cuadras, preguntale". Cámara con $3-10 M adentro | Del formulario §2.3 |
| **4** | **Distribuidora** (cámara grande, tiene grupo electrógeno) | **Premium** + transferencia a generador (a medida, se cotiza con relevamiento eléctrico) | Cobra desde el día 1 | Corte de luz = pérdida grande; único perfil donde el módulo de generador se vende solo | Del formulario §2.3 |
| **5** | **Restaurante / supermercado** | Estándar, 2 cámaras | Cobra desde el día 1 | Cierra a la 1, abre a las 10: 8 h de cámara muerta sin saberlo. Bromatología para habilitación | Del formulario §2.3 |

Regla: si Matías tiene "clientes para demo" que no calzan en estos 5 perfiles, se anotan igual — pero **los 5 equipos van primero a los que pagan desde el día 1**; el piloto gratis es uno y es estratégico (visible, referenciable), no "el que más insistió".

### 2.3 Formulario — Matías vuelca HOY sus "clientes para demo" (uno por fila; copiar y llenar)

```
CLIENTE PARA DEMO #__
1. Nombre del comercio y del dueño/decisor:
2. Rubro (carnicería / farmacia / veterinaria / laboratorio / distribuidora / restaurante / super / otro):
3. Ciudad y dirección:
4. Cuántas cámaras/heladeras y de qué tamaño (y si tiene freezer -18):
5. ¿Tiene WiFi estable en el local? ¿Cortes de luz frecuentes? ¿Grupo electrógeno?:
6. ¿Quién decide y quién paga? (dueño / encargado / socio / contador):
7. Urgencia (1 = "algún día", 5 = "ya perdí mercadería / me cayó bromatología"):
8. Relación con vos (1 = no me conoce, 5 = amigo/familia/cliente actual) y cómo lo contactás:
```

Con las respuestas, @comercial asigna equipo (1-5), nivel, precio y fecha de demo en la tabla de leads. **Un lead sin próximo paso fechado es un lead muerto.**

Leads cruzados que YA existen en el portfolio y tienen frío (a confirmar por Matías): **Kiosco Ofiuco (Paco)** — heladeras de bebidas/lácteos, cliente actual; **Mundo Outdoor** — no tiene frío, pero tiene 13 locales y conoce a medio Bahía: pedir 3 nombres; **Cassano / TallerEuro / Montagne** — clientes Modulia, pedir un nombre a cada uno.

---

## 3. Guion de demo de 15 minutos (equipo físico + celular)

> Lo hace Sergio (o quien haga la calle). Antes de entrar: maletín cargado, celular con el panel abierto y logueado, la heladera de Matías reportando (verificarlo en la vereda), hoja de mostrador con el WhatsApp comercial impreso, contrato en la mochila.
> **Regla dura:** ningún paso se muestra hasta que @verificador lo haya dado por andando en el maletín (columna "Gate"). Lo que no pasó el gate NO se demuestra y NO se promete — se anota como señal de producto.

| Min | Qué pasa | Qué se dice (corto) | Gate |
|---|---|---|---|
| 0-1 | Apertura, una frase y silencio | Carnicería: *"¿Cuánta plata tenés en la cámara ahora, y si se corta un sábado a la noche, cuándo te enterás?"* Farmacia: *"¿Quién mira la heladera de las vacunas el domingo?"* | — |
| 1-3 | **El vivo**: panel en el celu, heladera de Matías | *"Esta es una heladera en Bahía, ahora. Lleva meses reportando, cada minuto, también a las 3 de la mañana."* Dar el celular EN LA MANO. | Panel comercial online con historial |
| 3-6 | **Sonda al vaso con hielo** | Sacar la sonda del maletín, meterla en el vaso con hielo del comercio: *"Miren cómo baja."* Y a los < 2 min: alerta en el celu del dueño (se lo agrega como contacto antes de entrar o se usa el de Sergio). *"Ese mensaje llega a USTED, no a mí."* | Alerta E2E < 2 min con umbral de demo (p.ej. < 10 °C) |
| 6-8 | **Puerta abierta** | Separar el imán del reed: *"Quedó la puerta abierta"* → alerta a los N s. Si hay sirena en el maletín, suena. | Reed + alerta puerta; sirena opcional |
| 8-11 | **Corte de luz** — desenchufar la fuente a mano | Estándar: *"Se apagó. En unos minutos la nube avisa que el equipo dejó de reportar — sabés que pasó algo, no qué."* **Premium** (solo si el maletín es Premium): *"Se cortó la luz y el equipo sigue vivo con batería: te manda SMS / te llama."* | Estándar: alerta "equipo mudo" (`cron-device-alerts`). Premium: batería + 4G + SMS/llamada — **HOY NO EXISTE** (`TERMOVIGIA.md` §6). Hasta que exista, se dice: *"El Premium lleva batería y línea 4G y avisa por SMS; lo tengo para instalar en la segunda tanda"* y NO se demuestra. |
| 11-13 | **El papel** | Abrir el historial/exportación: *"Esto es lo que le mostrás a bromatología. Se hace solo."* | Exportación CSV/PDF del panel. Si el PDF con hash no existe, mostrar la curva + CSV y no decir "certificado". |
| 13-15 | **El número y el cierre** | *"El equipo no lo comprás: dejás un depósito de $150.000 que te vuelve cuando lo devolvés, la instalación son $50.000, y el abono $36.000 por mes — $1.200 por día. Vos sabés qué tenés adentro de la cámara."* Silencio. Luego: *"¿Te lo instalamos el jueves a la mañana o el sábado?"* | — |

Cierre según posición en la cola: **equipo 3 (único piloto)**: *"30 días gratis; el [fecha] o queda en $36.000/mes o lo retiro."* **Todos los demás**: *"Pagás desde el día uno; si en 60 días no te sirvió, te devuelvo todo y lo retiro."* Salir siempre con fecha y con el WhatsApp del dueño.

### Las 5 objeciones

| Objeción | Respuesta |
|---|---|
| **"Es caro"** | No bajar precio, bajar alcance: *"Arrancás con la cámara crítica, una sonda y la puerta: $32.000. Sumás después sin tocar nada de lo instalado."* Y la cuenta: *"$1.100 por día contra lo que tenés adentro de la cámara."* Comparación real: sensor WiFi de MercadoLibre ~$130.000 sin instalación, sin soporte, sin planilla válida; importado > $700.000 por cámara más licencia. |
| **"¿Y si se corta internet?"** | *"El corte ES una alarma: si el equipo deja de reportar te llega el aviso. No te deja ciego. Y si querés que avise aunque no haya luz ni internet, para eso está el Premium con batería y 4G."* (Solo prometer el Premium cuando exista.) |
| **"Ya tengo termómetro / anoto en planilla"** | *"El termómetro sirve cuando hay alguien mirándolo. ¿Quién lo mira el sábado a la noche? Esto es el mismo termómetro que te llama, y que llena la planilla solo. Bromatología no pide termómetro, pide REGISTRO (CAA art. 178, te lo dejo impreso)."* |
| **"¿Qué pasa si falla?"** | *"El equipo es nuestro, no lo compraste: si falla lo reponemos sin cargo, estamos en Bahía. Y el servicio avisa: si el equipo se calla, la nube te lo dice."* Nunca decir "no falla". |
| **"¿Y si me lo quiero comprar?"** | *"No se vende, y te conviene que no: si lo comprás, el día que cambia la app o se rompe, quedaste solo. Con el comodato, todo lo que se rompe es problema nuestro y el depósito te vuelve."* Si insiste: *"Podés quedarte el equipo imputando el depósito, pero el servicio sigue siendo por abono — sin nube no hay alerta."* |

Y la sexta, siempre: **"¿Dónde lo tenés andando?"** → ya lo vio (heladera en vivo) → *"desarrollado para un campamento minero de Panamerican en Santa Cruz — hay un equipo instalado allá, monitoreado desde Bahía"* (cierto desde el 21-ago) → *"equipos míos corren en Louis Dreyfus con la UTN"* → desde el cliente 2: *"lo tiene X, preguntale"*.

---

## 4. Catálogo comercial de upsells ("más sistemas y web")

Todo sobre la misma base, el mismo panel y el mismo contrato: se agrega una línea al abono, no se vende otro producto. Precios coherentes con la tarifa v4 (una boca = $4.000, un canal = $8.000, un módulo = $15.000). **Estado** dice si se puede vender hoy.

| # | Nombre vendible | Dolor que resuelve | Abono sugerido | Rubro | Estado técnico |
|---|---|---|---|---|---|
| 1 | **Puerta abierta + sirena** | Puerta de cámara que queda abierta de noche | $3.000 + $3.000/mes (tarifa vigente) | Todos | Existe (reed + relé) |
| 2 | **Aviso por WhatsApp** | "No uso Telegram" | $8.000/mes por sitio (vigente) | Todos | Existe como línea de precio; canal a verificar |
| 3 | **Llamada de alerta** (la nube llama a 2-3 contactos en escalada hasta que alguien atiende) | La alerta que nadie leyó a las 3 AM | $6.000/mes por sitio | Farmacia, distribuidora, laboratorio | **No existe**. Nota: sale de la nube (API de voz), no de la SIM — así el Premium no depende de que el plan M2M tenga voz |
| 4 | **Vigía de energía (Premium)** | Corte de luz sin aviso | $15.000/mes por base (vigente) + depósitos | Distribuidora, frigorífico, laboratorio | **No existe** (batería + 4G, `TERMOVIGIA.md` §6) |
| 5 | **Transferencia automática a grupo electrógeno** | Nadie va a arrancar el grupo un domingo | Desarrollo a medida + **$10.000/mes** de supervisión (estado del grupo, arranques, fallas) | Distribuidora, frigorífico, super | **No existe**; fuerza la cotiza un electricista |
| 6 | **Registro certificado** (PDF/CSV mensual con código de verificación, listo para inspección) | Planilla trucha con letra del empleado; auditoría | $6.000/mes por sitio | Farmacia, laboratorio, morgue, frigorífico | **No existe** (hoy va dentro del "desarrollo a medida" $300k+; como abono se vende más fácil) |
| 7 | **Salud del compresor** (corriente del motor: arranca demasiado / no arranca / se está muriendo) | El compresor avisa 2 semanas antes de morirse | $6.000/mes por cámara | Carnicería, frigorífico, super | `current_sensor.h` existe en el firmware pero NO está incluido (R5, banco) |
| 8 | **Humedad** (cámaras de maduración, panaderías, depósitos) | Producto que se seca o se moja | $4.000/mes por boca | Panadería, fiambrería, depósito | **No existe** (sensor nuevo) |
| 9 | **Puerta del local fuera de horario** | Entraron a las 4 AM y nadie supo | $3.000/mes por puerta | Todos | Existe (mismo reed) — solo software de horarios |
| 10 | **Control remoto** (prender/apagar deshielo, luces, bomba desde el celu) | Ir al local para apretar un botón | $5.000/mes por salida | Restaurante, super, distribuidora | Módulos relé existen (10); lógica a verificar |
| 11 | **Panel multi-sucursal** (usuarios con roles, vista consolidada, resumen por local) | Dueño de 3 locales que no sabe cuál está mal | $10.000/mes por cuenta (+ cámaras adicionales a $15.000) | Cadenas, franquicias | **No existe** (roles = deuda §6) |
| 12 | **Resumen mensual automático** ("este mes: 2 alertas, 0 pérdidas") | Que el cliente VEA el valor y renueve | **Incluido** — es retención, no upsell | Todos | Función escrita, deploy pendiente (`ESTADO` §3.4) |
| 13 | **Pantalla de estado en el local** (TV/tablet en cocina o depósito: cámaras en verde/rojo) | El encargado no mira el celular; la pantalla la ve todo el turno | $5.000/mes por pantalla | Restaurante, super, distribuidora | **No existe** — 4 h (@backend 4.1) |
| 14 | **Registro HACCP digital** (planilla diaria firmada por el encargado + checklist + no conformidades, exportable SENASA/bromatología) | La planilla HACCP de papel que nadie completa | $10.000/mes por local | Frigorífico, elaboradores, cadenas | **No existe** — 16 h (@backend 4.3); es el escalón arriba del ítem 6 |
| 15 | **Integración con Modulia (ERP)** — lote marcado si la cámara tuvo excursión, merma imputada a evento | Saber QUÉ mercadería estaba adentro cuando falló | $15.000/mes — o **incluido** para clientes de Modulia como gancho cruzado | Clientes Modulia con frío | **No existe** — 10 h de este lado (@backend 4.5) |

Lo que NO entra en el catálogo: páginas web genéricas, ERP como producto (es Modulia — se pasa el lead), electrónica a medida suelta. "Web" acá significa **el panel del cliente**, no hacer sitios.

### Cruce con @backend (`C:\Proyectos\frioseguro\PLAN_PLATAFORMA_TERMOVIGIA.md`, 2026-09-01 21:13)

El plan técnico existe y usa la misma tarifa v4. Donde los dos documentos difieren, la propuesta comercial es la de esta columna; **Matías decide** (es lo que @backend le pide en su §5: "decidir precios de los upsells y si el Premium queda en $15.000").

| Ítem | @comercial propuso | @backend propuso | Propuesta final para Matías |
|---|---|---|---|
| Puerta fuera de horario (9 ↔ 4.2) | $3.000/puerta | $5.000/cámara (incluye conteo de aperturas por turno) | **$5.000/cámara** — hay más que una alerta, hay un informe |
| Salud del compresor (7 ↔ 4.4) | $6.000/cámara | $8.000/cámara (SCT-013 en placa + predictivo) | **$8.000/cámara** — lleva sensor extra y evita un compresor de $1 M |
| Registro certificado (6 ↔ (c)) | $6.000/sitio | Módulo (c), 20 h, parte del "desarrollo a medida" | **$6.000/mes como línea de abono** para el que no paga desarrollo; el que paga desarrollo lo tiene incluido |
| Llamada de alerta (3 ↔ (a) paso 3) | $6.000/sitio, desde la nube | Premium: `ATD` desde el A7670 ($0) · Estándar: Twilio Voice, precio **no verificado** | **$6.000/sitio en Estándar** (Twilio); **incluido en Premium** (lo hace el módulo) |
| SMS de "equipo mudo" en Estándar | no lo tenía | Twilio: USD 0,1034/SMS + USD 1,15/mes el número; 2-5 SMS/mes por cliente → < USD 1/mes | **Incluido en el abono** (costo < $1.600/mes por cliente, no se cobra aparte) |
| Base Premium | $15.000 (no bajar) | pregunta si queda en $15.000; presupuesta SIM $10-15k | **Queda en $15.000.** La SIM real cuesta $2.900-5.000 (§1.3): deja $10.000 de margen por base — es el mejor producto de la lista |
| Pantalla de estado (4.1) | no lo tenía | $5.000/pantalla, 4 h | **Entra** (ítem 13) |
| HACCP digital (4.3) | no lo tenía | $10.000/local, 16 h | **Entra** (ítem 14), se vende después del ítem 6 |
| Integración Modulia (4.5) | "pasar el lead" | $15.000/mes o incluido para clientes Modulia | **Incluido para clientes de Modulia** — es el gancho cruzado de PLATA Línea 2 |

Combo que @backend puede construir en una semana sin hardware nuevo: **13 + 9 + 1 = $13.000/mes más por local** (pantalla + puerta fuera de horario + sirena con lógica). Es el upsell de la segunda visita.

**Calendario técnico que la venta tiene que respetar** (roadmap de @backend §5): Sprint 1 (2-15 sep) "que no dé vergüenza en la demo" → las demos de la semana del 8-sep se hacen con lo del Sprint 1, **con los gates del §3**. Sprint 2 (16-29 sep) = lo que compra Venado Tuerto (reporte con hash, umbrales, roles). Sprint 3 (30 sep - 13 oct) = Matías en Dreyfus, **no se promete nada nuevo a ningún cliente en esas dos semanas**. Prioridad comercial que le pido a @backend, en este orden: **Premium (SMS por el propio equipo) → vigía de equipo mudo con escalado → reporte con hash → resumen mensual → compresor**.

---

## 5. Proyección a 6 meses (sep-2026 → feb-2027)

Supuestos (todos arriba): abono promedio **$41.400**/equipo; instalación **$50.000** (ingreso); depósito promedio **$204.000** (**caja, NO ingreso** — se devuelve); costo fijo **$39.083/mes** + **$5.000** por base Premium (30 % de los activos); BOM Estándar **$45.000** (capital, lo financia el depósito). Piloto gratis: 1 (paga desde el mes 2). Churn supuesto 0 en 6 meses — la meta es < 5 %/mes; una baja se ve enseguida en la métrica.

### A — 5 equipos activos (los 5 de esta tanda, nada más)
| Mes | Activos | Pagan | Nuevos | Abonos | Instalaciones | **Ingreso** | Costos | **Margen op.** | Depósitos (caja) |
|---|---|---|---|---|---|---|---|---|---|
| sep | 1 | 0 | 1 | 0 | 50.000 | 50.000 | 39.083 | 10.917 | 204.000 |
| oct | 2 | 2 | 1 | 82.800 | 50.000 | 132.800 | 44.083 | 88.717 | 204.000 |
| nov | 3 | 3 | 1 | 124.200 | 50.000 | 174.200 | 44.083 | 130.117 | 204.000 |
| dic | 4 | 4 | 1 | 165.600 | 50.000 | 215.600 | 44.083 | 171.517 | 204.000 |
| ene | 5 | 5 | 1 | 207.000 | 50.000 | 257.000 | 49.083 | 207.917 | 204.000 |
| feb | 5 | 5 | 0 | 207.000 | 0 | 207.000 | 49.083 | 157.917 | 0 |
| **6 m** | | | | | | **1.036.600** | | **767.100** | 1.020.000 |

MRR al mes 6: **$207.000**. Reparto E1 con 5: G+S ~$52.000/mes + instalaciones; Matías ~$106.000/mes. **Esto no es "hacerse ricos": es la prueba de que el pitch cierra.** Qué tiene que pasar: 1 demo/semana, 1 cierre/mes, 0 bajas.

### B — 15 equipos activos (la segunda tanda entra en noviembre)
| Mes | Activos | Pagan | Nuevos | Abonos | Instalaciones | **Ingreso** | Costos | **Margen op.** | Depósitos (caja) |
|---|---|---|---|---|---|---|---|---|---|
| sep | 2 | 1 | 2 | 41.400 | 100.000 | 141.400 | 44.083 | 97.317 | 408.000 |
| oct | 4 | 4 | 2 | 165.600 | 100.000 | 265.600 | 44.083 | 221.517 | 408.000 |
| nov | 7 | 7 | 3 | 289.800 | 150.000 | 439.800 | 49.083 | 390.717 | 612.000 |
| dic | 10 | 10 | 3 | 414.000 | 150.000 | 564.000 | 54.083 | 509.917 | 612.000 |
| ene | 13 | 13 | 3 | 538.200 | 150.000 | 688.200 | 59.083 | 629.117 | 612.000 |
| feb | 15 | 15 | 2 | 621.000 | 100.000 | 721.000 | 59.083 | 661.917 | 408.000 |
| **6 m** | | | | | | **2.820.000** | | **2.510.500** | 3.060.000 |

MRR al mes 6: **$621.000**. Qué tiene que pasar cada mes: **3 demos/semana (12/mes), 1 cierre cada 4 demos** (25 %), Gonza arma 3/mes desde noviembre (necesita comprar 10 kits más en octubre: ~$450.000, que los depósitos de sep-oct cubren), churn < 1 baja. En diciembre aparece la señal de PLATA para vendedor a comisión (5+ abonos, pitch probado, leads que Sergio no llega a visitar).

### C — 40 equipos activos (Bahía + 2 ciudades por instalación remota + vendedor a comisión desde noviembre)
| Mes | Activos | Pagan | Nuevos | Abonos | Instalaciones | **Ingreso** | Costos | **Margen op.** | Depósitos (caja) |
|---|---|---|---|---|---|---|---|---|---|
| sep | 3 | 2 | 3 | 82.800 | 150.000 | 232.800 | 44.083 | 188.717 | 612.000 |
| oct | 7 | 7 | 4 | 289.800 | 200.000 | 489.800 | 49.083 | 440.717 | 816.000 |
| nov | 13 | 13 | 6 | 538.200 | 300.000 | 838.200 | 59.083 | 779.117 | 1.224.000 |
| dic | 21 | 21 | 8 | 869.400 | 400.000 | 1.269.400 | 69.083 | 1.200.317 | 1.632.000 |
| ene | 30 | 30 | 9 | 1.242.000 | 450.000 | 1.692.000 | 84.083 | 1.607.917 | 1.836.000 |
| feb | 40 | 40 | 10 | 1.656.000 | 500.000 | 2.156.000 | 99.083 | 2.056.917 | 2.040.000 |
| **6 m** | | | | | | **6.678.200** | | **6.273.700** | 8.160.000 |

MRR al mes 6: **$1.656.000**. Qué tiene que pasar: **6-8 demos/semana desde noviembre** (imposible con una sola persona en la calle → vendedor a comisión, 20 % del primer año como ya está escrito en `PRECIOS_FRIOSEGURO.md`), Gonza arma 8-10/mes (necesita ayuda o preensamblado de PCB: es un segundo cuello), **Premium terminado y verificado antes de noviembre** (sin Premium no hay distribuidoras ni laboratorios), soporte que ya interrumpe (señal de PLATA para atención). Este escenario **choca de frente con octubre (Dreyfus)**: solo es posible si Matías se mantiene en las 4 h/semana y el resto lo absorben Gonza, Sergio y los agentes.

**Lo que los tres escenarios tienen en común:** el margen operativo es alto porque el costo marginal de un equipo es $5.000/mes (Premium) o $0 (Estándar). El negocio no es el hardware, es la cantidad de abonos y que no se caigan. Los depósitos son caja que **no se toca** salvo para armar el equipo que la generó (reponer el pasivo con un activo en comodato).

**Capital que hace falta poner (antes de que entre el primer depósito):** 5 kits Estándar ~$225.000 + maletín de demo (placa existente) + INPI 3 clases $121.707 + dominio $8.500 + Supabase Pro $38.375 = **~$393.600** entre los tres. El resto lo financian los depósitos.

---

## 6. Legales pendientes — orden, costo, responsable

| Orden | Trámite | Qué se hace y cuánto cuesta (fuente) | Responsable | Cuándo |
|---|---|---|---|---|
| 1 | **Dominio termovigia.com.ar** | NIC.ar, tabla oficial: **$8.500/año** (alta, renovación y transferencia, mismo precio). Se registra en nic.ar con usuario de Trámites a Distancia (AFIP). | **Matías** (usuario TAD) | **Mié 2-sep** — es lo único que se pierde por esperar |
| 2 | **Búsqueda de antecedentes INPI** (clases 9, 38, 42) | **Gratis**, online en el portal del INPI (portaltramites.inpi.gob.ar → consulta de marcas). Buscar "termovigia", "termo vigia", "termovigía", fonéticos ("termovijia") en las 3 clases. Si aparece algo parecido en la clase 9 o 42, cambiar a un candidato de reserva (Termotraza, Criovista, Vigifrío, Criolink). | @comercial prepara el listado de búsquedas; **Matías** ejecuta (o Sergio) | Jue 3-sep |
| 3 | **Solicitud de marca INPI** | Arancel por clase: **100 UMAPI**; UMAPI desde el 1-sep-2026 = **$405,69** → **$40.569 por clase**, **$121.707 las 3 clases** (agosto era $39.735). Se puede presentar sin agente; honorarios de agente de referencia $200.000-300.000 por clase (no hace falta para arrancar). El arancel no se devuelve si hay oposición. Titular propuesto: **Matías** a título personal (después se licencia o transfiere a la sociedad). | **Matías** (titular) | Semana del 8-sep, después de la búsqueda |
| 4 | **Monotributo / factura** | Propuesta: **factura Matías** (una sola cara ante el cliente: contrato, factura y cobro a nombre de quien es titular de la marca y del equipo en comodato). Gonza y Sergio facturan a Matías sus servicios de armado/instalación con su propio monotributo (Esquema 1). Categoría la define el contador con la proyección del §5 (escenario B). Cuando se pase al Esquema 2, SAS. | **Matías + contador** | Antes del primer cobro (meta: piloto instalado en septiembre → primer cobro en octubre) |
| 5 | **Contrato servicio + comodato** | Existe borrador en `C:\Users\Pandemonium\Documents\MATI-HQ\comercial\CONTRATO_BORRADOR.md` (2026-07-07; el que la tarea nombra en `frioseguro\comercial\` NO existe). Sirve la estructura (objeto, **límite de responsabilidad "notifica y registra, no garantiza la mercadería"**, comodato, IPC trimestral, baja 30 días, datos, jurisdicción BB). **Falta actualizarlo al modelo v3/v4:** marca Termovigía · **depósito de garantía** (reintegro a 30 días de devuelto, ajustado por IPC, envío de vuelta a nuestro cargo, opción de imputarlo a compra) · Anexo I con **valores de reposición pieza por pieza** · niveles Estándar/Premium · "dependencia de terceros" que incluya red celular · cláusula transitoria del piloto gratis con precio escrito. Después: **contador + abogado** (IPC post-prohibición de indexación, tope de responsabilidad, figura del comodato). | @comercial actualiza el texto (jue 4-sep); **Matías** lo lleva al contador/abogado | Antes de la primera firma |
| 6 | **Seguro / responsabilidad** | El límite contractual (3 abonos) es la primera defensa. Consultar a un productor de seguros por **RC profesional/operaciones** con la proyección del §5; probablemente no haga falta hasta 15 abonos, pero que lo diga el productor, no nosotros. | **Sergio** pide 2 cotizaciones | Octubre |
| 7 | **SIM M2M con SMS y voz** | Movistar M2M MICRO 100: $5.000/mes (100 MB + 100 SMS). Voz **no garantizada** en planes M2M: confirmar con Movistar Empresas / Claro Connect si hay plan con voz, o resolver la llamada desde la nube (§4 ítem 3). | **Gonza** (compra 1 chip de prueba) + @backend | Semana del 8-sep |

---

## 7. Los próximos 7 días (mar 1-sep → lun 7-sep)

| Día | Acción | Dueño |
|---|---|---|
| **Mar 1** | Leer este plan. Llenar el **formulario §2.3** por cada "cliente para demo" (mínimo 5) y mandarlo. Definir quién hace la calle: Gonza o Sergio. | **Matías** |
| **Mar 1** | Mandar a Gonza la lista de lo que hay (5 PCB, 20 DS18B20, 10 reed, 10 relé, 3 cajas IP65) y pedirle recotización del BOM Estándar + cotización Premium (batería, cargador, módulo 4G). | Matías → **Gonza** |
| **Mié 2** | **Mandar el folleto a Venado Tuerto** (`FOLLETO_TERMOVIGIA.pdf` + `MENSAJE_WHATSAPP.md`). Registrar termovigia.com.ar ($8.500). | **Matías** |
| **Mié 2** | Arrancar el **maletín de demo** (equipo 0) con una PCB WiFi existente: caja, sonda 1 m, reed + imán, fuente desenchufable. | **Gonza** |
| **Jue 3** | Búsqueda de antecedentes INPI (gratis) con el listado de variantes. Resultado por WhatsApp al grupo de socios. | **Matías o Sergio** |
| **Jue 3** | @comercial: tabla de leads con los 5+ del formulario (equipo asignado, nivel, precio, fecha de demo) + contrato actualizado al modelo v4 (§6.5) + hoja de mostrador con marca Termovigía y WhatsApp comercial. | **@comercial / @diseno** |
| **Vie 4** | Mergear cola nocturna + flashear la placa del maletín con `firmware_modular` + claves reales (`QUE_FALTA` #1/#4/#8). Deploy `cron-monthly-summary`. | **@firmware / @backend** (Matías aprueba, no ejecuta) |
| **Sáb 5** | **Ensayo de la demo completa** (§3) en la casa de Matías con el maletín: hielo, puerta, desenchufar. Cronómetro en cada paso. Lo que no pasa el gate, se saca del guion. | **Sergio + Gonza**, @verificador con la evidencia |
| **Dom 6** | Nada. (Regla: si el sábado falló algo, el domingo se arregla en banco — Gonza — no se agenda demo.) | — |
| **Lun 7** | **Reunión de socios de 1 h**: elegir Esquema 1 o 2 (§1.3), aprobar tabla de leads, fijar las **3 primeras demos** (mar 8, jue 10, sáb 12). Matías define el número final de cada cotización. | **Matías, Gonza, Sergio** |
| **Lun 7** | Actualizar pipeline en `dominios\comercial.md` con las 3 demos fechadas. | **@comercial** |

Regla de la semana: **el viernes 4 tiene que haber un equipo que dispara una alerta real desde un vaso con hielo.** Si eso no pasa, la semana siguiente no se agenda ninguna demo, y el problema es de producto, no comercial.

---

## Fuentes consultadas (2026-09-01)
- Tarifa, depósitos, modelo: `C:\Proyectos\frioseguro\TERMOVIGIA.md` §3 · `PLATA.md` Línea 1.
- NIC.ar aranceles .com.ar $8.500/año: https://nic.ar/es/dominios/aranceles
- INPI: UMAPI $405,69 desde 1-sep-2026, 100 UMAPI por clase = $40.569; búsqueda de antecedentes gratuita: https://unamarca.com.ar/aranceles-inpi/ · https://1mark.ar/knowledge/costo-registro-marca-2026 (presentación sin agente posible; honorarios de agente $200-300k de referencia).
- SIM M2M Movistar (MICRO 10 ECO $2.900 · MICRO 100 $5.000 · MICRO 500 $10.000, con SMS): https://articulo.mercadolibre.com.ar/MLA-751384840-chip-m2m-25mb-10-sms-base-movistar-_JM · Claro M2M gestionado / Claro Connect: https://sucursales.claro.com.ar/empresas/servicios/iot/m2m-gestionado/ · precio chip M2M $2.000/mes (Pixel.AR, ene-2026): https://pixelargps.com/blog/guia-completa-chips-m2m-iot
- Supabase Pro USD 25/mes: https://www.nocode.mba/articles/supabase-pricing
- Dólar BNA 1-sep-2026 $1.485/$1.535: https://www.cronista.com/finanzas-mercados/dolar-oficial-hoy-asi-cerro-la-cotizacion-de-este-martes-1-de-septiembre/
- BOM kit $30-45k: `MATI-HQ\comercial\PRECIOS_FRIOSEGURO.md` §2 (jul-2026, a recotizar).
