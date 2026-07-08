# PRECIOS FrioSeguro — investigación de competidores + 3 escenarios

> Producido por @comercial · 2026-07-07 (adelantado del vie 10-jul) · Precios en ARS de julio 2026.
> Decisión final: Matías con el Director. Esto es el menú con números justificados.

---

## ⚠️ ALERTA PREVIA: el nombre "FrioSeguro" YA EXISTE como empresa en Argentina

**"Frio Seguro Monitoreo del Frio S.R.L."** (CUIT 30-71874481-0) opera en CABA y Zona Norte con **exactamente el mismo modelo**: instalación de dataloggers + abono mensual de monitoreo + alertas por WhatsApp/SMS/email. Tienen web ([frioseguro.com](https://www.frioseguro.com/)), app en Google Play ("FrioSeguro") y perfil societario registrado ([Dateas](https://www.dateas.com/es/empresa/frio-seguro-monitoreo-del-frio-srl-30718744810)).

- **Riesgo marcario:** si tienen (o registran) la marca en INPI, usar el mismo nombre es un problema legal y de confusión. **Acción sugerida antes de imprimir nada:** buscar "frio seguro" en el portal de INPI (https://portaltramites.inpi.gob.ar) y decidir: (a) renombrar (barato hoy, carísimo después), o (b) verificar que la clase/marca esté libre y registrarla YA.
- **Lo bueno:** valida el modelo de negocio al 100% (alguien ya vive de esto en CABA) y NO operan en Bahía Blanca → el terreno local está libre. No publican precios (cotizan por visita) — típico de servicio, y lo que nos conviene también.

---

## 1) Qué cobra la competencia (investigado julio 2026)

### A. Termógrafos / dataloggers USB (lo que hoy compra un comercio "cumplidor")
| Producto | Precio | Qué hace / qué NO hace |
|---|---|---|
| Datalogger termógrafo USB multiuso (SimpleTech, rep. Sensitech en LatAm) | **$34.000 – $70.000** (pago único) | Registra; NO avisa. Hay que ir, enchufarlo a la PC y bajar el PDF. Si la cámara se cortó el sábado, te enterás el lunes con la mercadería podrida. [simpletech.ar](https://www.simpletech.ar/MLA-1310588851-datalogger-termografo-digital-sensor-temperatura-multiuso-_JM) / [otro modelo $50.000](https://www.simpletech.ar/MLA-1711947612-datalogger-termografo-sensor-temperatura-digital-usb-_JM) |
| Sensitech TempTale 4 USB (descartable, cadena de frío en tránsito) | ~$34.000–$70.000 c/u, **de un solo uso** | Para envíos, no para monitoreo permanente. [MercadoLibre](https://articulo.mercadolibre.com.ar/MLA-1421554923-monitor-sensitech-temptale-4-usb-cadena-de-frio-registrador-_JM) / [sensitech.com](https://www.sensitech.com/es/productos/monitores/) |

### B. Sensores WiFi "hágalo usted mismo" (la objeción barata)
| Producto | Precio | Qué NO trae |
|---|---|---|
| Sensor WiFi Tuya/SmartLife con sonda DS18B20 y alarma | **$133.650** (pago único) | Sin instalación, sin soporte, cloud china (si Tuya te banea o cambia la app, perdiste todo), sin registro presentable para bromatología, una sola sonda. [misctechnologies/ML](https://www.misctechnologies.com/MLA-1170345809-sensor-temperatura-wifi-alarma-y-bateria-tuya-smartlife-_JM) |
| Sensor WiFi p/heladera con pantalla (Demasled) | **$30.300** | Ambiente/heladera hogareña; no apto cámara, sin sonda cableada seria, mismas limitaciones de arriba. [elektrom.com.ar](https://www.elektrom.com.ar/sensor-de-temperatura-y-humedad-para-heladera-con-pantalla-wifi-smart-life-demasled/p/MLA46072701) |

### C. testo Saveris 2 (el estándar profesional — nuestro techo de precio)
- Logger WiFi Saveris 2-T2 (sonda externa + contacto de puerta — el equivalente exacto a nuestro kit): se vende en Argentina vía distribuidores ([testo.com.ar](https://www.testo.com/es-AR/productos/saveris-2), [Actylab](https://actylab.com/instrumentos-testo/233-0200572-2032.html), [Dtisa](https://dtisa.com/producto/data-logger-wifi-testo-saveris-2-t2-data-logger-de-temperatura-con-conexiones-para-sonda-ntc-externa-y-contacto-puerta/)). Precio internacional de referencia: **USD 300–500 por logger** → en Argentina, con impuestos y margen de importador, **$500.000 – $900.000 por punto de frío**, cotización solo a pedido.
- Y encima la nube con alertas SMS **se paga aparte**: licencia Advanced ~**EUR 38 por logger por año** ([testo](https://www.testo.com/en-US/testo-saveris-2-advanced-cloud-licence-for-12-months/p/0526-0735)); la nube gratis NO manda SMS.
- Nadie te lo instala, nadie te lo mira: es una herramienta, no un servicio.

### D. Servicios de monitoreo con abono (el comparable real)
- **Frío Seguro SRL (CABA/Zona Norte):** instalación de dataloggers + abono mensual + alertas WhatsApp/SMS/email + reportes automáticos. Sin precio público (cotizan en visita). [frioseguro.com](https://www.frioseguro.com/) / [ficha](https://frio-seguro.laguia.online/)
- **USS (seguridad, nacional):** monitoreo de temperatura como extensión de su central de alarmas — mismo formato de abono. [uss.com.ar](https://uss.com.ar/soluciones-de-monitoreo-de-temperatura/)
- En Bahía Blanca: **no se encontró ningún prestador local de monitoreo de frío con abono**. Mercado libre (en el buen sentido).

### Conclusión competitiva
El comercio de Bahía hoy elige entre: (a) termómetro pincho + planilla a mano ($15.000 y mentira piadosa ante bromatología), (b) datalogger USB que no avisa ($34–70k), (c) juguete Tuya sin respaldo ($130k), o (d) testo a $700k+ por punto sin servicio. **Nadie le ofrece el servicio completo con alguien local que responde.** Ese es el hueco.

---

## 2) Tres escenarios de pricing (por local; "punto de frío" = 1 heladera/cámara con su sonda)

**Costo real nuestro por punto:** kit ESP32 + DS18B20 + reed + PCB propia ≈ **$30.000–$45.000 en componentes — y los primeros 5 kits YA están pagados**. Instalación: media jornada de Matías + viáticos Bahía. Cloud: ya corre (IP fija propia / infra existente); costo marginal ≈ $0. O sea: **desde el kit 1, el abono es margen casi puro** — lo que se cobra es el servicio y la espalda, no el hardware.

**Valor para el cliente (contra qué se justifica el número):**
- Una cámara de carnicería tiene **$3–10 millones** de mercadería. Un solo corte de fin de semana no avisado = pérdida total. El abono anual entero (~$540k en el recomendado) es menos que UNA góndola salvada.
- El registro de temperatura es **obligación legal** (ver sección 4): el sistema genera solo la planilla que hoy truchean a mano.
- En farmacia, perder la cadena de frío de vacunas/insulina no es plata: es descarte obligatorio + problema regulatorio.

| | 🥉 ECONÓMICO (penetración) | 🥈 **RECOMENDADO** ⭐ | 🥇 PREMIUM (farmacias/cadenas) |
|---|---|---|---|
| **Instalación** (una vez, por local) | $35.000 | **$70.000** | $120.000 |
| **Abono mensual — 1er punto de frío** | $25.000 | **$45.000** | $70.000 |
| **Abono — cada punto adicional (mismo local)** | $15.000 | **$25.000** | $40.000 |
| Incluye | Alertas Telegram/push, dashboard, historial | Todo lo anterior + registro mensual PDF para bromatología + soporte con respuesta en 48 h + reposición de hardware sin cargo | Todo + SLA 24 h + sirena local + contacto de puerta con alerta inmediata + informe mensual firmado + visita semestral de verificación |

### Justificación de cada escenario

**🥉 Económico — instalación $35.000 / abono $25.000.**
La instalación apenas repone el costo de componentes del kit; el abono es "precio de no pensarlo" (≈ $830/día). Sirve solo si el objetivo fuera llenar 5 kits en 2 semanas a cualquier costo. **Contras:** posiciona el servicio como gadget y no como seguro; a 10 locales junta ~$300k/mes (lejos de la meta de PLATA de que 10 locales paguen >1 sueldo junior); no deja margen para el día que haya que pagar un instalador por visita. Subir precios después es una guerra; bajar es un regalo. **No recomendado salvo emergencia de caja.**

**🥈 RECOMENDADO — instalación $70.000 / abono $45.000 + $25.000 por punto adicional.** ⭐
- **Instalación $70.000:** repone el kit (~$40k) + paga la media jornada + viáticos, y queda por debajo del precio psicológico de $100k. Contra testo: entrar con Saveris 2 cuesta **10 veces más** por punto y sin nadie que responda. Frase de venta: *"la instalación sale menos que un datalogger USB de los que no avisan… bah, que dos"*.
- **Abono $45.000/mes:** = **$1.500 por día**, menos de medio kilo de vacío por semana, ≈ 0,5–1,5% del valor de la mercadería que cuida por mes. Incluye el registro para bromatología, que hecho a mano cuesta 10 minutos diarios de un empleado (eso solo ya vale más de $45k/mes). Contra la alternativa Tuya ($133k una vez): en 3 meses de abono el cliente "pagó lo mismo", pero recibió instalación, soporte, reposición y papel válido — y a nosotros nos deja LTV, que es la métrica que manda (PLATA: abonos activos).
- **Aritmética de la meta:** 10 locales × (1,6 puntos promedio) ≈ **$610.000/mes recurrente** + $700k de instalaciones one-shot. No llega solo a "1 sueldo junior con 10 locales" pero con 15–18 locales sí — y el escenario recomendado es el único que permite pagar comisión a un vendedor (20% del primer año) sin fundirse, que es la señal de contratación definida en PLATA.
- **Piloto (política ya definida, no ablandar):** 1 solo piloto gratis 30 días con precio pactado ANTES ("después son $45.000/mes o lo retiro"). Cliente 2 en adelante paga desde el día 1 con garantía 60 días.

**🥇 Premium — instalación $120.000 / abono $70.000.**
Para farmacias (obligación ANMAT/COFA, el descarte de un lote de vacunas supera el abono anual), veterinarias con biológicos y cadenas/supermercados con varias cámaras. El SLA de 24 h y el informe firmado justifican el salto: acá el cliente no compra alertas, compra **cumplimiento regulatorio con respaldo**. No abrir con esto; es el upsell natural cuando preguntan "¿y me lo firmás para la inspección?".

### Reglas comunes (van al contrato)
- Hardware en **comodato**: sigue siendo nuestro; se corta el abono → se retira el equipo. (Protege el modelo: nadie "compra y chau".)
- Cobro por transferencia/débito, mes adelantado, del 1 al 10.
- **Ajuste trimestral por IPC (INDEC)** escrito en el contrato desde el día 1 — en Argentina un abono sin cláusula de ajuste es un abono que se derrite.
- Upsell en la misma visita (PLATA Línea 4): sirena / puerta abierta / control remoto simple = +$10.000–15.000/mes por relé.

---

## 3) Escenario elegido

**⭐ RECOMENDADO: instalación $70.000 + abono $45.000/mes (1er punto) / $25.000 (adicional).**
Motivos: cubre costos desde el minuto uno, sostiene la promesa de servicio (soporte + reposición), es 10× más barato que la única alternativa profesional (testo), resiste la comparación con el juguete Tuya por servicio y no por precio, y es el único de los tres que deja margen para comisionar un vendedor cuando llegue la señal de los 5 abonos.

---

## 4) NORMATIVA — el argumento de venta (todo con fuente)

> La frase para el mostrador: **"El registro de temperatura no es un favor que le hacés a bromatología: es obligación. Esto te lo hace solo, todos los días, y te lo imprime."**

### 4.1 Alimentos — Código Alimentario Argentino (Ley 18.284)
- **CAA, Capítulo III, Artículo 178** — la cita de oro, textual: *"Todas las cámaras frigoríficas deberán poseer instrumentos apropiados para el control y **registro** de temperatura y humedad relativa."* → No alcanza el termómetro: pide REGISTRO. Fuente oficial: [CAA Cap. III — De los productos alimenticios (alimentosargentinos.magyp.gob.ar)](https://alimentosargentinos.magyp.gob.ar/contenido/marco/CAA/Capitulo_03.htm)
- **CAA, Capítulo II (Condiciones de fábricas y comercios), art. 4.1.4.2.3 (BPM):** los locales refrigerados requieren *"un termómetro de máxima y de mínima o dispositivos de registro de la temperatura, para asegurar la uniformidad de la temperatura para la conservación de materias primas, productos y procesos"*. Fuentes: [CAA Cap. II (alimentosargentinos)](https://alimentosargentinos.magyp.gob.ar/contenido/marco/CAA/Capitulo_02.htm) · [PDF oficial ANMAT actualizado](https://www.argentina.gob.ar/sites/default/files/anmat_caa_capitulo_ii_establecactualiz_2021-03.pdf)
- **Manual BPM (Secretaría de Agroindustria):** el control de temperatura es punto crítico de las Buenas Prácticas de Manufactura exigibles a todo elaborador. [PDF oficial](https://alimentosargentinos.magyp.gob.ar/contenido/publicaciones/calidad/BPM/BPM_conceptos_2002.pdf)

### 4.2 Carnes — SENASA
- **Decreto 4238/68 (Reglamento de Inspección de Productos de Origen Animal):** rige todo establecimiento con cámaras que maneje carne y derivados; fija condiciones de frío y control por cámara. Fuentes: [SENASA](http://www.senasa.gob.ar/decreto-423868) · [texto en InfoLEG](https://servicios.infoleg.gob.ar/infolegInternet/anexos/20000-24999/24788/dn4238-1968cap1.htm) · [Digesto SENASA](https://digesto.senasa.gob.ar/items/show/789)

### 4.3 Farmacia / vacunas — ANMAT, Ministerio de Salud, COFA
- **Norma COFA para aplicación de vacunas en farmacia:** heladera exclusiva con **"cartilla de registro de temperatura… en la puerta de la heladera, para luego ser archivada"**, control **como mínimo una vez por día**, termómetro en el centro de la heladera. [cofa.org.ar](https://www.cofa.org.ar/?p=1243)
- **Manual de almacenamiento de vacunas — nivel operativo (Ministerio de Salud, 2022):** registro de temperatura de heladeras de vacunas como rutina obligatoria del vacunatorio (planilla diaria). [PDF oficial argentina.gob.ar](https://www.argentina.gob.ar/sites/default/files/bancos/2022-12/manual-almacenamiento-vacunas-nivel-operativo.pdf)
- **Resolución 498/2008 (Normas Nacionales de Vacunación)** — marco nacional de cadena de frío. [argentina.gob.ar/normativa](https://www.argentina.gob.ar/normativa/nacional/141074/texto)
- Refuerzo ANMAT (cadena de frío en establecimientos): [Disposición 2241/17 (PDF)](https://boletin.anmat.gob.ar/marzo_2017/Dispo_2241-17.pdf)

### 4.4 Bahía Blanca — bromatología municipal
- La habilitación y fiscalización de comercios de alimentos en Bahía pasa por **Bromatología municipal**, con requisitos técnicos de conservación para locales que elaboran/venden alimentos: [bahia.gob.ar/tramites/bromatologia](https://www.bahia.gob.ar/tramites/bromatologia/) · [Requisitos mínimos locales de alimentos](https://www.bahia.gob.ar/tramites/habilitaciones/comerciales/requisitos-minimos-para-locales-donde-elaboren-alimentos/) · [Bromatología y Protección de la Salud](https://www.bahia.gob.ar/salud/bromatologia/)
- **Pendiente (visita/llamado, no está online):** confirmar con Bromatología BB si en inspección piden planilla de temperatura y con qué frecuencia. Si la respuesta es "sí" (casi seguro, aplican CAA), cada inspector que pasa por un comercio nos hace marketing gratis.

### Los 3 links más fuertes para llevar impresos
1. **CAA Art. 178** (registro obligatorio en TODA cámara): https://alimentosargentinos.magyp.gob.ar/contenido/marco/CAA/Capitulo_03.htm
2. **Norma COFA** (registro diario en heladera de vacunas de farmacia): https://www.cofa.org.ar/?p=1243
3. **Manual de vacunas del Ministerio de Salud** (planilla diaria, nivel operativo): https://www.argentina.gob.ar/sites/default/files/bancos/2022-12/manual-almacenamiento-vacunas-nivel-operativo.pdf

---

## Bitácora
- 2026-07-07 — Documento creado por @comercial. Investigación con fuentes de julio 2026. Pendientes: (1) chequeo INPI del nombre "FrioSeguro" ⚠️, (2) llamado a Bromatología BB, (3) Matías valida escenario con el Director antes de la primera visita (13-jul).
