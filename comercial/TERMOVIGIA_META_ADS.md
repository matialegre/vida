# TERMOVIGÍA — ¿Meta Ads para conseguir demos? Análisis, costos y plan

> @comercial · 2026-09-02. Pregunta de Matías: *"¿se puede usar Meta Ads para promocionar Termovigía? Para dar demos y eso. ¿Cuánto sale? ¿Cómo será el plan?"*
> Contexto que manda: `TERMOVIGIA_PLAN_COMERCIAL.md` (5 equipos · Gonza 1 equipo/semana · Sergio 3 demos/semana · Matías 4 h/semana hasta el 31-oct) · `PLATA.md` Línea 1 (métrica = **abonos activos**) · sitio vivo https://termovigia.vercel.app/ (CTA a WhatsApp +54 9 2920 591019, sin precios).
> Todo precio de acá abajo lleva fuente y fecha. Lo que no se pudo verificar está rotulado **no verificado**.

---

## RESPUESTA CORTA PARA MATÍAS

1. **Sí se puede, y es fácil de montar (1 día de trabajo), pero HOY no lo prendas.** El cuello de botella no son los interesados: son 5 equipos, 1 armado por semana y 3 demos/semana. La publicidad compra el recurso que ya te sobra y no compra el que te falta.
2. Con impuestos, **$100.000 de pauta se te debitan como ~$153.000** (IVA 21 % + percepción 30 % + IIBB ~2 %) y te compran, con supuestos conservadores para B2B local, **unas 40-65 conversaciones, de las cuales 8-20 son gente real** y 4-6 aceptan demo. Sergio ya puede generar 12 demos/mes caminando, gratis.
3. **Prendelo recién cuando pasen las 5 condiciones del §6.0** (el vaso con hielo grabado en video, los 5 equipos colocados o el pipeline de calle agotado, segunda tanda de kits comprada, una referencia con nombre y el contrato visto por el contador).
4. Cuando se prenda: **$60.000/mes de pauta neta (~$92.000 con impuestos), una sola campaña de clic a WhatsApp, 14 días.** Sigue solo si el **costo por conversación CALIFICADA** (dueño con cámara, en zona) queda **≤ $25.000**. Arriba de $50.000, se apaga.
5. Antes de gastar un peso: **Google Business Profile (gratis, 30 min)**, la **Corporación del Comercio y el Centro de Farmacéuticos de Bahía**, y **dos distribuidoras / un service de refrigeración** como referidores. Rinden más que la pauta y no tienen impuestos.

---

## 1. ¿Conviene o no? — No todavía, y por una razón aritmética

La publicidad sirve para **generar demanda cuando la oferta puede absorberla**. Hoy la oferta es:

| Recurso | Capacidad real | Techo mensual |
|---|---|---|
| Equipos en stock | 5, más 1/semana que arma Gonza | ~4 instalaciones nuevas/mes, y solo 5 clientes hasta comprar la segunda tanda |
| Demos presenciales | Sergio, 3/semana, solo Bahía | 12 demos/mes |
| Atención de WhatsApp | Sergio, sin herramienta, sin guion de chat probado | ~5-10 conversaciones nuevas/día antes de que se le caiga alguna |
| Matías | 4 h/semana hasta el 31-oct | Cierres por videollamada, nada más |

Con esos techos, **el máximo teórico de la tanda entera son 5 abonos**. Ya hay pipeline identificado para más de 5 (los "clientes para demo" de Matías, Kiosco Ofiuco, los nombres a pedir a Mundo Outdoor y a los clientes de Modulia, más Venado Tuerto y Cerro Moro). **No falta demanda: falta ejecución.** Doscientas consultas serían un problema operativo, no un éxito: cada consulta sin responder en 24 h es marca quemada, y la marca todavía no tiene ni una referencia con nombre que la sostenga.

Y hay un problema más duro: **todavía no hubo ninguna demo ni ningún abono cobrado**. La regla vigente es que el viernes 4 tiene que haber un equipo disparando una alerta real desde un vaso con hielo o la semana siguiente no se agenda nada. **Publicitar un producto cuya propia demo el equipo no verificó es la forma más cara de descubrir que algo no anda**: el que atiende ese anuncio es un desconocido que no te va a perdonar nada, mientras que el primer cliente que consigue Sergio caminando sí te perdona una falla porque te conoce la cara.

**La alternativa de no gastar un peso todavía es la recomendada, y no es "no hacer nada":** es hacer §7 (Google Business Profile, cámaras, distribuidoras, referidos, calle), que cuesta tiempo y cero pesos, y que además **produce el activo que la publicidad va a necesitar después**: el video del hielo, una foto de equipo instalado y un cliente con nombre.

**El costo de oportunidad puntual:** $153.000 debitados de la tarjeta son casi 4 kits Estándar de BOM ($30-45k cada uno, `PRECIOS_FRIOSEGURO.md` §2, a recotizar). Con esa plata comprás capacidad de facturar $36.000/mes × 4. Con pauta comprás visitas al sitio.

**Lo que sí conviene hacer ya (costo $0):** dejar la infraestructura publicitaria armada y en pausa — página de Facebook, Business Manager, cuenta publicitaria, número vinculado, píxel en la landing. Cero gasto, y el día que se prenda no se pierden dos semanas de trámites ni se estrena una cuenta nueva (las cuentas recién creadas son las que Meta más bloquea).

---

## 2. Qué se puede hacer con Meta, exactamente

### 2.1 Los tres formatos que aplican a este caso

| Formato | Qué hace | Qué requiere | Para qué sirve acá |
|---|---|---|---|
| **Clic a WhatsApp (CTWA)** ⭐ | El anuncio en Facebook/Instagram tiene botón "Enviar mensaje": abre el chat con un mensaje pre-cargado | Página de Facebook + número de WhatsApp Business **vinculado a la página** + cuenta publicitaria con medio de pago | **El más directo para este caso.** El interesado no llena nada, escribe. Y el chat abre una ventana de 72 h en la que responder es gratis si contestás dentro de las primeras 24 h ([Zenvia, 2026](https://zenvia.com/blog/como-usar-anuncios-click-to-whatsapp-no-seu-negocio/)) |
| **Tráfico al sitio** | Manda a termovigia.vercel.app | Lo mismo + el sitio (ya existe) | Sirve sobre todo para **construir el público de retargeting** y medir interés. Como generador de consultas es peor: agrega un clic más antes del contacto |
| **Formularios nativos (Instant Forms)** | El usuario deja nombre/teléfono sin salir de Facebook | Lo mismo + política de privacidad publicada en el sitio (**hoy no está — hay que escribirla**) | Barato por lead y **lleno de basura**: la gente lo completa sin pensar. Solo sirve si alguien llama en menos de 5 minutos. Con Sergio en la calle, no |

**Recomendación: CTWA único.** Un formato, una campaña, un público. Nada de repartir $60.000 en tres cosas.

### 2.2 Qué hay que tener (y qué NO hace falta)

- **Página de Facebook** de Termovigía. Obligatoria — la cuenta publicitaria anuncia "en nombre de" una página.
- **Cuenta de Meta Business (Business Manager) + cuenta publicitaria** con medio de pago.
- **Número de WhatsApp Business vinculado a la página.** Acá hay ruido: varias guías (todas de empresas que venden API) dicen que hace falta la WhatsApp Business API ([Woztell](https://woztell.com/guide-click-to-whatsapp-ads/)). **No es cierto para el caso simple**: Meta tiene página de ayuda propia titulada "Crear anuncios de clic a WhatsApp **desde la app de WhatsApp Business**" (facebook.com/business/help/199357208512411) y las guías 2026 confirman que sirve la app o la API, y que **la API solo hace falta para automatizar** ([Zenvia](https://zenvia.com/blog/como-usar-anuncios-click-to-whatsapp-no-seu-negocio/), [AdLibrary 2026](https://adlibrary.com/posts/meta-click-to-whatsapp-ads-guide)). Con el volumen esperado acá (menos de 3 conversaciones por día), **la app alcanza y sobra**, y coincide con lo ya decidido en PLATA: *"escalar a WhatsApp Business API recién con 10+ abonos"*. Igual: confirmarlo en pantalla el día de la configuración, es un checkbox.
- **Verificación**: Meta puede pedir verificación de identidad de la cuenta publicitaria (foto de DNI) y, en algunos casos, verificación del negocio. Con gasto bajo normalmente no la pide al arrancar, pero la puede pedir en cualquier momento y **congela el gasto hasta resolverla**. Típico 24-48 h, puede irse a semanas. *No verificado el criterio exacto con el que Meta la dispara — no lo publica.*
- **NO hace falta**: WhatsApp Business API, agencia, sitio nuevo, ni catálogo.

### 2.3 Cuánto tarda ponerlo en marcha

| Paso | Tiempo |
|---|---|
| Crear página de Facebook + foto de perfil (ya existe el PNG de marca) y datos | 1 h |
| Business Manager + cuenta publicitaria + medio de pago | 1 h |
| Vincular el número comercial de WhatsApp Business a la página (verificación por SMS) | 30 min |
| Píxel de Meta en la landing (Vercel, una etiqueta) | 30 min — @frontend |
| Cargar campaña + 2 creatividades + públicos | 2 h |
| **Revisión de los anuncios por Meta** | Normalmente < 24 h; puede ser 48 h |
| Verificación de identidad si Meta la pide | 1-5 días hábiles |

**Realista: un día de trabajo + 24-48 h de espera.** No es el cuello de botella; el cuello es tener algo que mostrar.

---

## 3. Cuánto sale (2026, en pesos, con fuente)

### 3.1 Cómo factura Meta en Argentina y qué impuestos se suman

Meta es **servicio digital del exterior**. Sobre lo que gastás en pauta se aplica, cobrado por el emisor de la tarjeta / medio de pago como agente de percepción:

| Concepto | % | Norma / fuente | ¿Se recupera? |
|---|---|---|---|
| **IVA** | **21 %** | Decreto 813/2018, percibido por el intermediario de pago ([Estudio Piacentini, 31-oct-2025](https://www.estudiopiacentini.com.ar/impuestos-que-se-pagan-sobre-los-servicios-digitales-del-exterior/)) | **Responsable inscripto: sí**, crédito fiscal. **Monotributista: NO** — es costo puro |
| **Percepción a cuenta de Ganancias / Bienes Personales** | **30 %** | **RG 5617/2024** (ARCA), vigente desde el 23-dic-2024, reemplazó al régimen de la RG 4815 cuando venció el Impuesto PAÍS ([Boletín Oficial 19-12-2024](https://www.boletinoficial.gob.ar/detalleAviso/primera/318447/20241219) · [Bruchou & Funes de Rioja](https://bruchoufunes.com/nuevo-regimen-de-percepcion-que-reemplaza-el-impuesto-pais/) · [Banco Patagonia, FAQ](https://www.bancopatagonia.com.ar/preguntas-frecuentes/tarjetas/credito/percepcion.php)) | Es **pago a cuenta**, no impuesto nuevo. Quien tributa Ganancias/BP lo computa. **El monotributista no es sujeto de Ganancias → tiene que pedir la devolución a ARCA** (trámite anual). **A confirmar con el contador** |
| **Ingresos Brutos** | **~2 % (Prov. de Buenos Aires)** | Piacentini (31-oct-2025) dice 2 % PBA; una guía de agencia dice 3 % genérico ([Anunzi](https://ayuda.anunzi.net/paid-media/impuestos/impuestos-en-facebook-ads-argentina), ene-2025). **Tomo 2 %, con margen de error de 1 punto** | No |
| ~~Impuesto PAÍS~~ | — | **Derogado el 23-dic-2024**, ya no se cobra ([abogados.com.ar](https://abogados.com.ar/index.php/el-impuesto-pais-desaparece-pero-se-mantiene-la-percepcion-del-30-en-impuesto-a-las-ganancias-y-bienes-personales/36182)) | — |

**Recargo total ≈ 53 %** sobre la pauta neta (21 + 30 + 2). Coincide con lo que reportan las guías locales: *"IVA 21 % + 30 % de percepción... suman 54 %"* ([Anunzi](https://ayuda.anunzi.net/paid-media/impuestos/impuestos-en-facebook-ads-argentina) · [DoubleTick, 2026](https://www.doubletick.com.ar/como-financiar-pauta-meta-ads-argentina/) · [Tributo Simple](https://tributosimple.com/como-conviene-pagar-meta-ads-en-argentina-tarjeta-vs-linea-de-credito-local/)).

> **Regla práctica: lo que Matías pone de pauta, multiplicalo por 1,53 para saber lo que le va a debitar la tarjeta.** De ese recargo, **30 puntos son recuperables** (con contador y trámite), **23 puntos son costo hundido** para un monotributista.

**Medios de pago**: tarjeta de crédito/débito argentina cargada en la cuenta publicitaria (lo normal, con todos los impuestos de arriba). Existen alternativas — prepagas en dólares, líneas de crédito locales de agencias que facturan en pesos con solo IVA — que las guías 2026 comparan ([DoubleTick](https://www.doubletick.com.ar/como-financiar-pauta-meta-ads-argentina/), [Upway](https://upwaydigitalsolutions.com/blog/marketing/como-pagar-campanas-de-meta-en-pesos-sin-el-65percent-de-impuestos-en-argentina)). **No las recomiendo**: son intermediarios, el ahorro no compensa el riesgo de que la cuenta quede a nombre de un tercero, y el monto en juego es chico. Tarjeta de Matías, punto.

### 3.2 Precios de la pauta (rangos con fuente y margen de error)

Cotización usada: **dólar BNA vendedor $1.535 al 2-sep-2026** ([Cronista](https://www.cronista.com/finanzas-mercados/dolar-hoy-a-cuanto-cotiza-el-oficial-en-los-bancos-de-la-city-este-miercoles-2-de-septiembre/)).

| Métrica | Valor con fuente | En pesos (neto, sin impuestos) |
|---|---|---|
| **CPM Argentina (mediana real)** | **USD 3,62**, mediana sep-2025 → jul-2026, sobre >USD 3.000 M de gasto agregado ([Superads](https://www.superads.ai/facebook-ads-costs/cpm-cost-per-mille/argentina)). Rango observado USD 0,20 – 16,79: **Argentina es de los mercados más volátiles del mundo** (el mes a mes se mueve USD 2,61 promedio) | **$5.557 por 1.000 impresiones** |
| CPM por objetivo | Alcance USD 2-5 · Facebook feed USD 4-12 · Reels USD 2-5 (el más barato) ([SODI, 14-abr-2026](https://www.sodi.com.ar/blog/cuanto-cuesta-publicidad-facebook-instagram-argentina)) | $3.000 – $18.400 |
| **CPC (tráfico)** | **USD 0,30 – 1,00** ([SODI, abr-2026](https://www.sodi.com.ar/blog/cuanto-cuesta-publicidad-facebook-instagram-argentina)); segunda fuente independiente: **$400 – $1.500 ARS por clic** ([Basework, 2026](https://www.basework.com.ar/blog/whatsapp-marketing-argentina-2026)) | **$460 – $1.535** — las dos fuentes coinciden |
| **Costo por conversación iniciada (CTWA)** | LatAm **EUR 0,20 – 0,80** en campañas sanas; los que lo hacen mal pagan EUR 2,50+ ([Kanal, benchmarks 2026](https://getkanal.com/blog/click-to-whatsapp-ads-benchmarks-2026)) | ≈ **$350 – $1.400**, y **$4.400+** si sale mal |
| CTR sano | 1,5-2,5 %; top 3,5-5 %; **video vertical tipo Reel: 2-5 % y el costo por conversación más bajo** (Kanal 2026) | — |
| Costo de mensajería de Meta por conversación | USD 0,005 – 0,16 según país; **Argentina en el techo, cerca de 2 centavos** ([Patagon AI](https://www.patagon.ai/blog-posts/whatsapp-business-api-pricing)) | ~$30 — **irrelevante, y $0 si se usa la app y no la API** |
| Mínimo con sentido para negocio local | **$50.000 – $100.000 ARS/mes**, comprometido por 3 meses (SODI, abr-2026) | — |

**Margen de error: alto, y hay que decirlo.** Los benchmarks son promedios de todos los rubros (mayormente e-commerce B2C, que es lo que domina Meta en Argentina). **Un público B2B chico y geolocalizado en una ciudad de 300.000 habitantes paga bastante más caro que la mediana**, porque el algoritmo tiene poca gente donde optimizar. Para el plan uso el **techo del rango, ×2**: $1.500 por conversación iniciada como supuesto de trabajo, no $350.

### 3.3 La traducción: "con $X/mes esperás Y conversaciones, de las que Z son reales"

Supuestos, todos explícitos y conservadores:
- Costo por conversación iniciada: **$1.500** (techo LatAm ×2, por público B2B chico).
- **20 % de las conversaciones son "reales"**: dueño o encargado de un comercio con frío, en Bahía o en zona con electricista, que responde más de un mensaje. El otro 80 % son curiosos, gente de otra provincia, alguien que quiere un termómetro de $20.000 para la casa, y clics accidentales (en móvil son muchos).
- **30 % de los reales aceptan demo presencial.**
- **1 de cada 4 demos cierra abono** (mismo supuesto del §5 del plan comercial).

| Pauta neta | Debitado con impuestos (×1,53) | Conversaciones | **Reales (20 %)** | Demos (30 %) | Abonos esperados | **Costo por abono** |
|---|---|---|---|---|---|---|
| $30.000 | $45.900 | 20 | **4** | 1,2 | 0,3 | $153.000 |
| **$60.000** | **$91.800** | **40** | **8** | **2,4** | **0,6** | **$153.000** |
| $100.000 | $153.000 | 66 | **13** | 4,0 | 1,0 | $153.000 |
| $300.000 | $459.000 | 200 | **40** | 12 (satura a Sergio) | 3,0 | $153.000 |

**Cómo leerlo:** un abono cuesta ~$153.000 de publicidad = **4,3 meses del abono Estándar de $36.000**. No es un desastre (un CAC de 4 meses con churn bajo es sano), pero **es plata que compra algo que Sergio produce gratis**: 12 demos/mes caminando. La pauta empieza a tener sentido cuando esas 12 demos/mes ya no alcanzan.

Y ojo con la última fila: **$300.000 de pauta rompe la operación.** 200 conversaciones a atender por una sola persona que además está en la calle = respuestas tardías = marca quemada, y encima solo hay 5 equipos para colocar.

---

## 4. Segmentación: lo que se puede y lo que no

### 4.1 Geografía

| Anillo | Localidades | Por qué |
|---|---|---|
| **Núcleo (donde se hace demo presencial)** | Bahía Blanca + radio de 25 km: Punta Alta, General Daniel Cerri, Cabildo, Grünbein | Es donde Sergio puede ir. Radio de 25 km, no 50: una demo a 60 km le come la tarde |
| **Segundo anillo (instalación remota, cierre por videollamada)** | Coronel Suárez, Tres Arroyos, Pigüé, Coronel Dorrego, Monte Hermoso, Médanos, Villalonga | Ciudades chicas con comercio de alimentos, a las que llega el kit por encomienda y donde hay electricista local |
| **Tercer anillo (solo si sobra presupuesto)** | Carmen de Patagones / Viedma | El número comercial es 2920 = zona Viedma/Patagones: escribirle a un número local baja la fricción |
| **Nunca** | AMBA, todo el país | Ahí se compite con importadores con presupuesto real y no hay ninguna ventaja de cercanía. El lead de Venado Tuerto llegó solo, sin pauta |

**Regla operativa: no abrir el segundo anillo hasta que el núcleo haya dado 2 abonos.** Un cliente remoto que falla, a 300 km, cuesta cinco veces más de atender.

### 4.2 A quién se puede apuntar (y por qué es difícil)

Lo que Meta ofrece y algo sirve:
- **Intereses de negocio**: "Pequeña empresa", "Emprendimiento", "Propietario de empresa", "Restaurantes", "Supermercado", "Refrigeración", "Seguridad alimentaria". Son intereses de **consumo**, no de rubro: al que le gusta "Restaurantes" es el que sale a comer, no el que tiene uno.
- **Comportamiento "administradores de página de Facebook"** — históricamente el mejor proxy B2B de Meta, con subcategorías por tipo de página (comida/bebida, retail, salud). **Meta viene recortando opciones de segmentación año a año: hay que verificar en pantalla qué queda disponible el día que se arme la campaña. No verificado.**
- **Retargeting de interacción con el video** (gente que vio ≥ 15 s del video del hielo): **este es el mejor público de todos** y no existe hasta que el video haya corrido. Razón adicional para arrancar con el video.
- **Advantage+ / público amplio 25-65 en Bahía**, dejando que la creatividad filtre: contraintuitivo, pero con audiencias chicas suele ganarle a la segmentación fina, porque el algoritmo aprende de quién frena el scroll.

**Lo que NO se puede** (decirlo antes de que Matías lo espere):
- **Meta no deja apuntar por rubro comercial.** No existe "dueños de carnicería de Bahía Blanca". Ese dato lo tienen LinkedIn (vacío en comercio chico argentino) y las cámaras de comercio (que sí lo tienen — §7).
- **No hay públicos similares (lookalike)** sin lista de clientes, y hoy hay cero clientes. Con 5-10 tampoco alcanza: Meta pide del orden de 100 registros para una semilla decente.
- No se puede segmentar por "tiene una cámara de frío", "está habilitado por bromatología" ni "lo inspeccionaron el mes pasado" — que es exactamente lo que define al comprador.
- **El universo real es chico**: en Bahía habrá algunos cientos de comercios con cámara; Meta necesita decenas de miles de personas para optimizar. Vas a pagar por mostrarle el anuncio a mucha gente que nunca va a comprar. **Eso ya está en el precio y no se arregla con mejor segmentación: se arregla con mejor creatividad.**

---

## 5. Los anuncios: 3 propuestas

**Reglas duras para los tres**, no negociables:
- **Sin precios.** El precio se dice en la demo, después del hielo (guion §3 del plan). El sitio tampoco los publica: coherente.
- **Nada de 4G, SMS ni llamada**: no existen. Ningún anuncio los nombra.
- **"Desarrollado para"**, nunca "instalado en", salvo lo que sea literalmente cierto.
- **Nunca "te garantizamos que no perdés la mercadería"**: contradice el contrato (límite de responsabilidad — *el servicio avisa, no garantiza la mercadería*) y es el tipo de promesa que Meta rechaza.
- **Escribir en tercera persona, no en segunda.** La política de atributos personales de Meta rechaza anuncios que afirman o insinúan algo sobre el usuario. *"¿Perdiste mercadería?"* es candidato a rechazo; *"Una cámara que se corta un sábado a la noche se descubre el lunes"* pasa. Es la causa de rechazo evitable número uno.

### Anuncio A — "El vaso con hielo" (video vertical 20 s) ⭐

**Este es el mejor activo publicitario que Termovigía va a tener, y por lejos.** Es un producto invisible — una caja que manda mensajes — y el video del hielo lo vuelve visible en 20 segundos sin explicar nada. Los benchmarks 2026 dicen que el video vertical nativo tipo Reel tiene el CTR más alto (2-5 %) y el costo por conversación más bajo del inventario ([Kanal](https://getkanal.com/blog/click-to-whatsapp-ads-benchmarks-2026)). **Grabarlo el sábado 5, en el ensayo de la demo, con el celular en vertical y buena luz. Un solo plano, sin cortes, sin música, sin logo animado: la gracia es que parezca real, porque lo es.**

Guion: mano metiendo la sonda en el vaso con hielo → corte a la pantalla del celular donde el número baja → llega la notificación → mano levantando el celular con la alerta. Texto quemado en pantalla: *"Sonda al hielo"* → *"1 minuto 40"* → *"Alerta"*.

Copy:
```
Una cámara que se corta un sábado a la noche se descubre el lunes a la mañana.
Termovigía mide la temperatura cada minuto y avisa al celular cuando se sale de rango.
El sistema se desarrolló para un campamento minero en Santa Cruz. Ahora está en Bahía.
Equipo en comodato, servicio por abono, instalación a cargo nuestro.
Escribinos y te mostramos cómo funciona, sin compromiso.
```
CTA: **Enviar mensaje.** Mensaje precargado: *"Hola, tengo una cámara/heladera y quiero saber cómo funciona Termovigía."*

### Anuncio B — "La planilla que se llena sola" (imagen: la tira del registrador)

Usa lo que **ya existe en el sitio**: la tira de registrador con la curva de temperatura. Recortar un fin de semana real de la heladera de Matías, con un bajón marcado en rojo y la hora al lado. Cero stock, cero ilustración.

Copy:
```
Bromatología no pide un termómetro. Pide el registro.
Termovigía guarda la temperatura de cada cámara, minuto a minuto, y arma la planilla sola.
Cuando algo se sale de rango, el aviso llega al celular en el momento, no al otro día.
Servicio mensual para comercios de Bahía Blanca y la zona. El equipo lo ponemos nosotros.
Escribinos y te mostramos el panel andando.
```
Público separado del A: **farmacias, veterinarias, laboratorios**. Es el segmento que compra cumplimiento, no ahorro, y paga más fácil.

### Anuncio C — "El equipo, de verdad" (foto real, cuando exista)

Foto del primer equipo instalado en una cámara real: caja IP65 en la pared, el cable de la sonda entrando, y al lado la pantalla del celular con la lectura. **Sin retoque, con la pared fea de fondo.** No sale hasta que haya un equipo instalado — y ahí sirve doble, porque en ese momento ya se puede nombrar la referencia con permiso del cliente.

Copy:
```
Así queda instalado: una caja, una sonda dentro de la cámara y un imán en la puerta.
No hay que cambiar el equipo de frío ni romper nada; se instala en una mañana.
El equipo no se compra: queda en comodato y el servicio se paga por mes.
Estamos en Bahía Blanca. Si falla algo, vamos.
Escribinos y coordinamos una demostración en tu local.
```

**Presupuesto de producción de los tres: $0.** El video lo graba Sergio con el celular, la tira ya está en el sitio y la foto sale de la primera instalación.

---

## 6. Plan por etapas, con presupuesto y criterio de corte

### 6.0 Etapa 0 — Las 5 condiciones para prender (hoy no se cumple ninguna del todo)

| # | Condición | Cómo se verifica | Estado hoy |
|---|---|---|---|
| 1 | **El vaso con hielo dispara una alerta real, y está grabado en video** | Ensayo del sáb 5-sep con @verificador + el archivo de video | Pendiente (regla del vie 4-sep) |
| 2 | **Los 5 equipos colocados, o el pipeline de calle agotado** (Sergio hizo 2 semanas de visitas y se le acabaron los nombres) | Pipeline de `dominios/comercial.md`, estado por lead | El formulario §2.3 ni siquiera está lleno |
| 3 | **Segunda tanda de kits comprada** (capacidad ≥ 3 instalaciones/mes sostenida) | Factura de componentes + Gonza confirmando ritmo | BOM sin recotizar |
| 4 | **Una referencia con nombre y permiso** ("lo tiene X, preguntale") | Cliente 1 andando 30 días + su OK por escrito | Cero clientes |
| 5 | **Contrato visto por contador/abogado + facturación resuelta** | `CONTRATO_TERMOVIGIA_v4.md` con las respuestas del contador | Borrador sin revisar |

**Mientras tanto, gasto = $0**, y se deja armada la infraestructura (§2.3) en pausa. El píxel se instala desde ya: empieza a juntar visitantes del sitio para el retargeting futuro, sin costar nada.

### 6.1 Etapa 1 — Prueba chica: **$60.000 de pauta neta, 14 días**

- Debitado real: **~$91.800** (×1,53). **Ese es el número que Matías tiene que aprobar, no el $60.000.**
- **$2.000/día**, una sola campaña, objetivo **Mensajes → WhatsApp**.
- **Dos anuncios**: A (video del hielo) y B (la tira), mismo público núcleo (Bahía + 25 km, 25-65). Nada de 6 variantes: con este presupuesto no hay volumen para aprender de 6.
- **Ubicaciones automáticas**, con Reels prioritario (CPM 20-40 % más barato que el feed, Kanal 2026).
- **No tocar nada los primeros 7 días.** Apagar y prender campañas resetea el aprendizaje; es el error más caro y más común.

**La métrica que decide es el costo por conversación CALIFICADA.** Calificada = alguien que (a) tiene cámara o heladera comercial, (b) está en el núcleo o en el segundo anillo y (c) contestó al menos dos mensajes. **No** el costo por clic, **no** el costo por conversación iniciada: esos dos números se ven lindos y no significan nada.

| Costo por conversación calificada a los 14 días | Decisión |
|---|---|
| **≤ $25.000** | **Sigue.** Está por debajo del valor de una demo. Se pasa a Etapa 2 |
| $25.000 – $50.000 | **Una vuelta más de 14 días**, cambiando creatividad (no público). Si no baja, se apaga |
| **> $50.000** | **Se apaga.** Y no es fracaso: es la respuesta a la pregunta, comprada por $91.800 |
| **0 conversaciones calificadas en 7 días con el presupuesto entregándose completo** | **Se apaga a los 7, no a los 14.** No hay nada que optimizar |

### 6.2 Etapa 2 — Escalar (solo con capacidad libre)

Duplicar a **$120.000/mes de pauta** (~$183.600 debitados) **solo si se cumplen las tres a la vez**:
1. La Etapa 1 dio costo por conversación calificada ≤ $25.000.
2. **Hay ≥ 2 equipos en stock sin asignar** y Gonza sostiene 1/semana.
3. Sergio tiene **al menos 1 slot de demo libre por semana** (o sea: la calle no lo está saturando).

Si falta cualquiera de las tres, **la plata va a comprar kits, no impresiones.** Escalar de a poco: +50 % cada 14 días, nunca duplicar de golpe (el algoritmo se re-aprende y el costo se dispara).

### 6.3 Quién atiende, y en cuánto tiempo

**Sergio, con esta regla escrita:** respuesta en **menos de 15 minutos** en horario comercial (9-13 y 16-20) y a primera hora de la mañana para lo que entra de noche. Si no puede garantizarlo, **la campaña no se prende**: pagar por una conversación y contestarla al otro día es tirar la plata dos veces (se pierde el lead y se pierde la ventana gratuita de 72 h).

Herramientas, todas gratis y ya decididas en PLATA:
- **Mensaje de bienvenida** y **mensaje de ausencia** configurados en WhatsApp Business.
- **Etiquetas = pipeline** (Nuevo · Calificado · Demo agendada · Piloto · Abono · Descartado) — ya está escrito en `comercial/plantillas_whatsapp.md`.
- **Guion de calificación de 3 preguntas**: *"¿Qué tenés que cuidar: cámara, heladera o freezer?"* · *"¿En qué localidad?"* · *"¿Sos el dueño o el encargado?"*. Con eso se decide en 2 minutos si va a la agenda o a "Descartado".
- **Descartado no es basura**: se le deja el sitio y se anota con fecha. Un "hoy no" de septiembre es un "vení" de marzo.

---

## 7. Lo que rinde más que la pauta (y va primero)

| # | Canal | Costo real | Qué produce | Comparado con Meta |
|---|---|---|---|---|
| **1º** | **La calle (ya está en el plan)**: Sergio, 3 comercios por día, con el maletín | $0 en efectivo. ~9 h/semana de Sergio | **12 demos/mes** con la persona parada adelante y el hielo en la mano | Meta con $153.000 debitados da **4 demos**. La calle da 12 por cero pesos. **Mientras esto no esté saturado, pautar es absurdo** |
| **2º** | **Cámaras y colegios**: Corporación del Comercio, Industria y Servicios de Bahía Blanca · Centro/Colegio de Farmacéuticos · Colegio de Veterinarios · cámara de la carne | Cuota societaria, o $0 por una charla / un mail a socios | **La lista de comercios por rubro que Meta no te vende.** Una charla de 20 min ante 30 farmacéuticos = 30 leads calificados | Es *exactamente* la segmentación que Meta no ofrece (§4.2), gratis. **Lo primero después de la calle** |
| **3º** | **Distribuidoras y services de refrigeración**: quien repara las cámaras de medio Bahía ya conoce a los 40 comercios que las tienen | Comisión por referido (propuesta: **1 abono, $36.000, por cliente que cierra**) o 10 % del abono el primer año | Referidos con confianza prestada y con el dolor ya identificado | Un técnico de refrigeración vale más que $500.000 de pauta. **Alto retorno, cero riesgo de cuenta bloqueada** |
| **4º** | **Referidos del piloto** (la carnicería del equipo 3) | $0 o 1 abono de premio | La conversión más alta de todas: *"lo tiene X a 3 cuadras, preguntale"* | Es la capa 4 del manejo de objeciones de PLATA. **No existe hasta tener el cliente 1** |
| **5º** | **Google Business Profile** (ficha de empresa en Google/Maps) | **$0**, ~30 min + verificación (postal o video) | Aparece cuando alguien busca "monitoreo de temperatura Bahía Blanca" o "control de cámara frigorífica". Volumen bajísimo, **intención altísima**: el que busca eso tiene el problema hoy | Meta interrumpe a gente que no busca nada; Google atiende al que ya busca. **Hacerlo esta semana igual, no cuesta nada** |
| **6º** | **Grupos de Facebook y Marketplace locales** (compra-venta Bahía, gastronómicos, comerciantes) | $0 | Alcance local real | Riesgo: baneo por spam y quemar el perfil. **Una publicación con el video, en 3 grupos, sin repetir.** No es un canal, es un empujón |
| **7º** | **Meta Ads** | $91.800 el mes de prueba | 8 conversaciones reales, 2-3 demos | **Último.** Se prende cuando los canales 1 a 4 no dan abasto |

**Cuál pondría primero: la calle y las cámaras de comercio.** El Centro de Farmacéuticos es el mejor lead de todos los que aparecen en este documento: cien farmacias, todas con heladera de vacunas, todas con obligación de registro, todas en la misma lista de mails. Ese contacto lo puede hacer Matías en 20 minutos de sus 4 horas semanales, y no cuesta un peso.

---

## 8. Riesgos

| Riesgo | Probabilidad | Cómo se mitiga |
|---|---|---|
| **Anuncio rechazado** | **Alta** al principio | La causa evitable número uno es la política de **atributos personales** (hablarle al usuario de su situación: *"¿perdiste mercadería?"*). Escribir en tercera persona (§5). Si rechazan, se edita y se vuelve a mandar; no se crea un anuncio nuevo ni otra cuenta |
| **Cuenta publicitaria bloqueada** | **Media-alta — pasa seguido**, sobre todo en cuentas nuevas, con tarjeta nueva y gasto que arranca de golpe | Cuenta a nombre de Matías con su identidad real · **2FA activado** · tarjeta a su nombre · arrancar con $2.000/día y subir de a poco · **nunca crear una segunda cuenta para esquivar un bloqueo** (es la forma más rápida de perder también la página). Si se bloquea: apelar desde el Centro de Calidad de la Cuenta y esperar. **El daño real no es la plata: es que la página y el número comercial queden marcados** |
| **Gastar sin poder atender** | **Alta — es LA que importa acá** | El tope de $2.000/día está calculado para que no entren más de 1-2 conversaciones por día. **Si Sergio tiene 3 conversaciones sin responder por más de 6 h, se pausa la campaña ese mismo día**, sin discutir |
| **Quemar la marca antes de la primera referencia** | **Alta** | Un desconocido que llega por un anuncio no perdona una demo que falla ni un "te aviso la semana que viene". Por eso el orden correcto es: primero los que te conocen (calle, referidos, cámaras), después los extraños. **Termovigía tiene una sola oportunidad de primera impresión en una ciudad chica** |
| **Anunciar sin contrato validado ni factura** | **Media, con consecuencia legal real** | La ley 24.240 (art. 8) establece que **las precisiones de la publicidad obligan al oferente e integran el contrato**. Si el anuncio dice "te avisamos" y un día la nube no avisó, eso es lo que se reclama. Por eso: nada de garantías de resultado en el copy, el límite de responsabilidad tiene que estar en el contrato firmado (`CONTRATO_TERMOVIGIA_v4.md`, ya escrito, **falta contador/abogado**), y **la landing necesita política de privacidad publicada** si alguna vez se usan formularios nativos (ley 25.326). Y para cobrar hace falta la facturación resuelta: **no se publicita un servicio que todavía no se puede facturar** |
| **La percepción del 30 % queda como costo hundido** | Media (depende de la figura fiscal) | Un monotributista no computa la percepción contra Ganancias; hay que **pedir la devolución a ARCA**. Sumarlo a la lista de preguntas del contador que ya está en el encabezado del contrato |
| **El CPM argentino se dispara** | Media | Argentina es de los mercados más volátiles del mundo: mediana USD 3,62 pero rango observado USD 0,20 – 16,79 ([Superads](https://www.superads.ai/facebook-ads-costs/cpm-cost-per-mille/argentina)). **Presupuesto diario tope siempre puesto**, nunca campaña sin límite |

---

## 9. Qué hacer esta semana (nada de esto cuesta plata)

| Cuándo | Acción | Dueño |
|---|---|---|
| **Vie 4-sep** | Que el equipo dispare la alerta real del vaso con hielo (regla ya vigente) | @firmware / @backend |
| **Sáb 5-sep** | En el ensayo de la demo: **grabar el video vertical de 20 s del hielo**. Un plano, celular en vertical, buena luz. Es el activo publicitario más valioso del proyecto | **Sergio + Gonza** |
| **Sáb 5-sep** | Crear la **ficha de Google Business Profile** de Termovigía (gratis, 30 min) e iniciar la verificación | **Matías o Sergio** |
| **Lun 7-sep** | En la reunión de socios: decidir **quién atiende el WhatsApp y con qué tiempo de respuesta** (es condición para cualquier pauta futura) | Los 3 |
| **Lun 7-sep** | Página de Facebook + Business Manager + cuenta publicitaria + número vinculado, **todo en pausa, gasto $0** | **Sergio** |
| **Lun 7-sep** | **Píxel de Meta en la landing** (empieza a juntar público de retargeting desde hoy, gratis) | @frontend |
| **Sem. 8-sep** | Mail/llamado a **Corporación del Comercio** y **Centro de Farmacéuticos** de Bahía pidiendo una charla o una comunicación a socios | **Matías** (20 min de sus 4 h) |
| **Sem. 15-sep** | Hablar con **2 distribuidoras / 1 service de refrigeración** y ofrecerles el esquema de referido | **Sergio** |
| **Cuando se cumplan las 5 de §6.0** | Recién ahí: prender la Etapa 1 con $60.000 de pauta | **Matías decide el número final** |

---

## Fuentes consultadas (todas verificadas el 2-sep-2026)

- **CPM Argentina USD 3,62 mediana (sep-2025 → jul-2026, sobre >USD 3.000 M de gasto agregado)**: https://www.superads.ai/facebook-ads-costs/cpm-cost-per-mille/argentina
- **CPC/CPM Argentina por objetivo y mínimos de inversión (art. del 14-abr-2026)**: https://www.sodi.com.ar/blog/cuanto-cuesta-publicidad-facebook-instagram-argentina
- **CPC $400-1.500 ARS y costo de mensajería en pesos (2026)**: https://www.basework.com.ar/blog/whatsapp-marketing-argentina-2026
- **Benchmarks CTWA 2026 (costo por conversación LatAm EUR 0,20-0,80, CTR, ventaja de Reels)**: https://getkanal.com/blog/click-to-whatsapp-ads-benchmarks-2026
- **Precio de conversación de Meta por país, Argentina en el techo (~2 centavos)**: https://www.patagon.ai/blog-posts/whatsapp-business-api-pricing
- **Impuestos a servicios digitales del exterior: IVA 21 % (Dec. 813/2018), percepción RG 5617 30 %, IIBB PBA 2 % (art. del 31-oct-2025)**: https://www.estudiopiacentini.com.ar/impuestos-que-se-pagan-sobre-los-servicios-digitales-del-exterior/
- **RG 5617/2024, texto oficial (Boletín Oficial, 19-dic-2024)**: https://www.boletinoficial.gob.ar/detalleAviso/primera/318447/20241219 · análisis: https://bruchoufunes.com/nuevo-regimen-de-percepcion-que-reemplaza-el-impuesto-pais/
- **Impuesto PAÍS derogado el 23-dic-2024; la percepción del 30 % continúa**: https://abogados.com.ar/index.php/el-impuesto-pais-desaparece-pero-se-mantiene-la-percepcion-del-30-en-impuesto-a-las-ganancias-y-bienes-personales/36182
- **Cómo se identifica la percepción en el resumen de tarjeta**: https://www.bancopatagonia.com.ar/preguntas-frecuentes/tarjetas/credito/percepcion.php
- **"IVA 21 + Ganancias 30 + IIBB 3 = 54 %" (guía de agencia, ene-2025)**: https://ayuda.anunzi.net/paid-media/impuestos/impuestos-en-facebook-ads-argentina
- **Medios de pago de Meta Ads en Argentina 2026 (tarjeta vs. líneas locales)**: https://www.doubletick.com.ar/como-financiar-pauta-meta-ads-argentina/ · https://tributosimple.com/como-conviene-pagar-meta-ads-en-argentina-tarjeta-vs-linea-de-credito-local/ · https://upwaydigitalsolutions.com/blog/marketing/como-pagar-campanas-de-meta-en-pesos-sin-el-65percent-de-impuestos-en-argentina
- **Requisitos de anuncios de clic a WhatsApp y ventana gratuita de 72 h**: https://zenvia.com/blog/como-usar-anuncios-click-to-whatsapp-no-seu-negocio/ · https://adlibrary.com/posts/meta-click-to-whatsapp-ads-guide · Meta oficial: facebook.com/business/help/199357208512411 ("Crear anuncios de clic a WhatsApp **desde la app de WhatsApp Business**") y facebook.com/business/help/1874973492831043
- **Postura contraria (afirma que hace falta la API)**, de una empresa que vende API: https://woztell.com/guide-click-to-whatsapp-ads/
- **Dólar BNA vendedor $1.535 al 2-sep-2026**: https://www.cronista.com/finanzas-mercados/dolar-hoy-a-cuanto-cotiza-el-oficial-en-los-bancos-de-la-city-este-miercoles-2-de-septiembre/

**No verificado (y cómo averiguarlo):**
- Criterio exacto con el que Meta dispara la verificación de identidad/negocio → Meta no lo publica; se descubre al crear la cuenta.
- Alícuota exacta de IIBB para servicios digitales en Prov. de Buenos Aires (2 % vs. 3 %) → lo confirma el contador, o el resumen de la tarjeta con el primer débito real.
- Devolución de la percepción RG 5617 para un monotributista → **pregunta para el contador**; sumarla a las 5 que ya tiene en el encabezado de `CONTRATO_TERMOVIGIA_v4.md`.
- Qué opciones de segmentación por comportamiento ("administradores de página") siguen disponibles en 2026 → se ve en pantalla al armar el público, no antes.
- Costo por conversación real para B2B local en Bahía → **no existe benchmark; se compra con los $91.800 de la Etapa 1.** Ese es, literalmente, el producto de esa prueba.
