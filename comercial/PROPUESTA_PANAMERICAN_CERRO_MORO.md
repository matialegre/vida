# PROPUESTA — Monitoreo de cadena de frío de reefers · Pan American Silver, Cerro Moro

> @comercial · 2026-09-03 · **para revisión de Matías antes del vie 5-sep**
> Contacto en sitio: **Andrés Leiva Chavez**. Pedido textual del 3-sep-2026 (audio): *"andá pensando en cómo vas a hacer con el tema de la parte económica"*.
> **Matías decide el número final, siempre.** Todo monto de acá abajo es propuesta con la cuenta a la vista.
> Doctrina: `PLATA.md` (Línea 1 — el objetivo es el ABONO). Base técnica honesta: `C:\Proyectos\frioseguro\entrega_scz\docs\ESTADO_HONESTO.md`.

---

## PARTE 1 — La página que se manda (WhatsApp / mail)

> Copiar de acá hasta la línea de corte. Nada más. El resto del documento es interno.

**Termovigía — Monitoreo de cadena de frío para los reefers de Cerro Moro**

Hoy, mientras leen esto, hay un equipo nuestro instalado en el campamento midiendo y reportando a la nube. Se puso el 21 de agosto, Andrés lo reconectó el 3 de septiembre y desde entonces manda una lectura cada pocos segundos, que se ve desde Bahía Blanca en tiempo real. Todavía mide el aire del pasillo: apenas Andrés meta las sondas adentro, mide el reefer.

Ese equipo resolvió lo difícil de este sitio: **se conecta solo a la red del campamento que realmente da internet**, no a la que tiene más señal. Lo probamos 128 veces seguidas: la red más potente el 95 % del tiempo no dio internet ni una sola vez. Un equipo comprado en catálogo, que se configura con una red y una clave, ahí adentro se queda mudo el primer día.

**Lo que proponemos** es llevar eso de un equipo suelto a un servicio sobre los **5 reefers en operación** (+ el que hoy está fuera de servicio, previsto): **2 sondas por reefer**, alerta al celular cuando la temperatura se sale del rango durante más tiempo del acordado, aviso cuando un equipo deja de reportar, e **informe mensual de cadena de frío por reefer**, que es el papel que sirve cuando alguien pregunta.

**Quién hace qué:** los equipos van preconfigurados y probados en banco desde Bahía; **el montaje lo hace Andrés en sitio**, guiado por videollamada. Eso ahorra el viaje y los días de un ingeniero a 1.500 km, y por eso esta propuesta **no tiene línea de instalación**.

**La inversión, en tres líneas:**

| | **Recomendada — un equipo por reefer** | Alternativa — 3 equipos, compartiendo de a dos |
|---|---|---|
| Desarrollo y puesta en servicio industrial (pago único) | **USD 2.950** | USD 2.950 |
| Equipos, repuestos en sitio y materiales (pago único) | **USD 1.400** | USD 1.180 |
| **Servicio mensual** (5 reefers) | **USD 200/mes** | USD 200/mes |
| **Inversión inicial** | **USD 4.350** | USD 4.130 |

Facturación en dólares estadounidenses. De abonarse en pesos, se toma el tipo de cambio vendedor del Banco de la Nación Argentina de la fecha de pago.

*Referencia al 3-sep-2026 (BNA vendedor $ 1.535): la inversión inicial recomendada equivale a $ 6.677.000 y el servicio mensual a $ 307.000.*

**Recomendamos un equipo por reefer, y conviene explicar por qué**, porque la otra opción es más barata y sería fácil venderla. Compartir un equipo entre dos reefers obliga a llevar el cable de las sondas de un contenedor al otro, y ese cable es la parte frágil de todo el sistema: el fabricante del sensor (Maxim/Analog, nota de aplicación 148) le asigna a un circuito como el nuestro un alcance del orden de **3 metros**, y los 200 metros que se citan habitualmente corresponden a equipos con un chip de línea dedicado. Con nuestras propias mediciones llegamos bastante más lejos que esos 3 m, pero **en línea recta y con el cable adecuado**, no repartiendo ramas hacia varios lados.

Y hay algo más importante que la distancia: **cada reefer es un contenedor metálico con su propia puesta a tierra**. Un cable de sondas entre dos reefers ata esas dos tierras por un hilo fino, y la temperatura se mide justamente contra esa referencia: la diferencia de potencial entre tableros entra sumada a la lectura. Eso no se puede verificar desde Bahía Blanca — solo aparece en el sitio.

De ahí sale la frase que resume toda la ingeniería de esta decisión:

> **Si igual hay que tirar un cable hasta el otro reefer, es mucho más seguro tirar 220 V y poner un equipo ahí, que tirar el cable de las sondas.** Llevar energía cincuenta metros es un problema resuelto; llevar el bus de sensores cincuenta metros es un problema intermitente. Y este servicio se vende porque avisa: **un sistema que anda "casi siempre" es peor que no tener nada, porque enseña al operador a ignorar las alarmas.**

La diferencia entre las dos opciones es **USD 220 por única vez — poco más de un mes de abono**. La alternativa de 3 equipos sigue en pie y la cotizamos con gusto **si las distancias medidas dan cortas** (hasta unos 15 metros por sonda, en línea, sin ramas divergentes). Pero es una opción que **depende de una medición que todavía nadie hizo**, y la recomendada no depende de nada.

Para poner los números en escala: **una sola pérdida parcial de 3 toneladas de mercadería congelada, valuada al precio más conservador posible, son más de $ 12.500.000** — más de tres años de este servicio.

**Lo que todavía no prometemos.** En agosto hicimos auditar el sistema por cinco revisores independientes y el veredicto fue: *prototipo que funciona de punta a punta, pero que hay que endurecer antes de venderlo a una minera*. No lo escondemos: está en el precio. El desarrollo que cotizamos **es exactamente ese endurecimiento**, en cuatro etapas con fecha, con aceptación de ustedes en cada una, y **el servicio mensual se cobra a mitad de tarifa hasta que la última etapa esté aceptada** (19-dic-2026). Se paga el valor entregado, no la promesa.

**Lo que necesitamos para cotizar en firme:** las distancias medidas, el rango de temperatura de cada reefer, quién firma la orden de compra y los requisitos de alta como proveedor.

*Matías Alegre · Termovigía · Bahía Blanca · 2920 59-1019 · alegrematias08@gmail.com*

— — — — — — — — — — corte: lo de abajo NO se manda — — — — — — — — — —

---

## PARTE 2 — Alcance

### 2.1 Qué hay hoy, verificado (3-sep-2026)

| Hecho | Evidencia |
|---|---|
| 1 equipo instalado en el campamento, `REEFER_01_SCZ`, firmware `firmware_revival` 2.6.21 | Puesto el 21-ago; reconectado por Andrés el 3-sep |
| Reportando cada ~5 s, última lectura 9,56 °C | Consulta a la base de Santa Cruz, 3-sep |
| **1 sola sonda y está FUERA del reefer** — mide ambiente | Idem. Andrés espera confirmación de Matías para meterlas |
| Elección de red abierta con internet real: probada 128 ciclos | `ESTADO_HONESTO.md` |
| Rollback de OTA verificado al reloj (4 s / 6 min) | `ESTADO_HONESTO.md` |
| **Sin contrato y sin un peso cobrado** | `PLATA.md` L74 |

Traducción comercial: **el activo más valioso que tenemos con este cliente no es el equipo, es que ya está adentro y funcionando.** Toda la propuesta se apoya en eso y no en una promesa.

### 2.2 El parque

- **6 reefers**, **1 fuera de servicio** → **5 activos** es lo que se cotiza.
- **2 están separados** del resto.
- **A todos les llega internet** (redes abiertas del campamento). Esto es determinante: no hace falta 4G, no hace falta tender red. Es el escenario más barato posible.
- El sexto reefer, cuando vuelva a servicio, entra con una línea de precio ya escrita (§4.6). No se rediscute nada.

### 2.3 Cuántas sondas y por qué dos por reefer

Un reefer no tiene "una" temperatura: tiene un gradiente. La sonda del propio equipo mide el **retorno de aire**, que es lo que la máquina necesita ver para regular — no lo que la carga siente. Con **dos sondas** (una cerca de la puerta / carga, otra en el fondo o en impulsión) se pueden distinguir tres cosas distintas que hoy se confunden en una sola:

1. **La máquina falló** (suben las dos juntas).
2. **La puerta quedó abierta o hubo carga/descarga larga** (sube la de la puerta y la del fondo no).
3. **Una sonda se soltó o se rompió** (una sola se va a un valor absurdo).

Con una sonda sola, cualquiera de las tres se ve igual y no se puede decidir a quién llamar. Dos por reefer es el mínimo con el que el informe mensual sirve como prueba. **10 sondas** para los 5 activos.

### 2.4 Cuántas bases — el veredicto técnico ya está, y cambia la recomendación

Andrés propone **3 módulos, 2 reefers cada uno**. Matías había pensado 1 cada 2-3 reefers con sondas largas. **La distancia nunca se midió**, así que `@muestreador` resolvió la pregunta por análisis: `C:\Proyectos\frioseguro\hardware\ALCANCE_1WIRE.md` (3-sep-2026). **El veredicto invierte la recomendación anterior de este documento: se cotiza como recomendada una base por reefer** (escenario B), y las 3 bases quedan como alternativa condicionada.

**Los cinco fundamentos, todos del documento de `@muestreador`:**

1. **El máster que usa nuestro producto es el peor de la tabla de AN148.** La nota de aplicación 148 de Maxim/Analog clasifica los másters, y "pin de micro pelado + pull-up" —que es exactamente FrioSeguro— está catalogado en **≈ 3 m de radio y 3 m de peso**. Los **200 m** que se citan en todos lados corresponden a másters con driver dedicado (FET con control de slew rate, DS2480B con filtro) o con pull-up activo (500 m). **Citar los 200 m para nuestro circuito es citar la fila equivocada de la tabla.**
2. **Y encima AN148 declara alcance a 5 V; nosotros corremos el bus a 3,3 V.** La propia nota avisa que las redes grandes *"often have too much loss to perform well under low voltage conditions"*. O sea: estamos fuera de su alcance declarado y hay que **derratear** sus números, no copiarlos.
3. **La cuenta propia por tiempo de subida** (el máster tiene que muestrear dentro de los 15 µs del flanco): con CAT5, **4k7 → 30 m · 2k2 → 64 m · 1 kΩ → 143 m**, y **1 kΩ es el piso absoluto a 3,3 V** (por debajo, la sonda tendría que hundir más corriente de la que especifica su hoja de datos). El "~15 m con 4k7" que ya estaba escrito en `CABLEADO.md` tiene 2× de margen sobre el límite físico: está bien puesto.
4. **Esos metros valen SOLO en línea.** AN148 desaconseja la estrella no conmutada **dos veces en el mismo párrafo** y dice explícitamente que *no da garantías a ninguna distancia* en esa topología, porque en estrella **los rebotes recorren el peso total del cableado, no la rama más larga**: tres ramas de 25 m se comportan como 75 m. Y "una base con sondas largas saliendo hacia varios reefers" es, literalmente, la definición de estrella no conmutada.
5. **El riesgo dominante no está en ninguna nota de aplicación: son las tierras.** Cada reefer es un contenedor metálico con su propia puesta a tierra, alimentado desde un tablero de campamento con generador. Un cable de sonda del reefer A al B ata el GND de la sonda de B al GND del ESP32 que está en A; y como **el dato se mide contra ese mismo GND**, la diferencia de potencial entre tierras **entra sumada a la lectura**. No la filtra el trenzado, porque no es modo común. **Esto solo se ve en el sitio: no se puede probar en Bahía.**

**Y el argumento que cierra la discusión, que va también en la página que se manda al cliente:**

> Si igual hay que tirar cable hasta el reefer lejano, **es mucho más seguro tirar 220 V y poner una base ahí que tirar el bus de sondas**. Llevar energía 80 m es un problema resuelto y perdonador (se calcula la caída y listo); llevar 1-Wire 80 m entre dos contenedores con tierras distintas es un problema **marginal e intermitente**. Y el producto se vende porque avisa: **un bus que anda "casi siempre" es peor que no tener nada, porque enseña al operador a ignorar las alarmas.**

| | **Escenario B — RECOMENDADO** | Escenario A — alternativa condicionada | (Escenario descartado) |
|---|---|---|---|
| Bases | **5** (una por reefer activo) | 3 (2 + 2 + 1) | 1 para los seis |
| Topología | Lineal, ≤ 5 m, 2 sondas — *"sin discusión"* en la tabla de `@muestreador` | Mini-estrella de 2 ramas por base | Estrella grande |
| Cable CAT5 | **~30 m en total** (el que menos cable usa) | 60-150 m | 150-400 m |
| Riesgo de bus intermitente | **Nulo** | Bajo si cada rama ≤ 15 m · medio 15-25 m · alto arriba de 25 m | **Alto** |
| Tierras cruzadas entre contenedores | **Ninguna** | Sí | Seis |
| Si falla, quedan ciegos | **1 reefer, y el sistema lo sabe** (deja de reportar y el panel lo marca) | 2 reefers | 6 reefers |
| ¿Depende de una medición que nadie hizo? | **No** | **Sí — bloqueante** | Sí |
| Equipos | USD 1.400 | USD 1.180 | **No se cotiza** |

**Por qué el escenario de una sola base ni siquiera se ofrece:** además del análisis de bus, **no entra en el firmware**. `entrega_scz/firmware/sondas.h` define `SONDAS_MAX 4`; doce sondas en un bus no caben en el producto actual **ni con el bus perfecto**. Sostener ese escenario sería rediseño de firmware, no una decisión de cableado. Y es el escenario que más barato cotiza y el que puede costar el cliente entero.

**Regla de decisión, si Andrés trae las distancias y son cortas:** el escenario A vuelve a estar sobre la mesa **solo si cada rama es ≤ 15 m, los dos reefers de cada par son contiguos, la base va en el medio y las dos ramas son de largo parecido** (una de 3 m y otra de 40 m es el peor caso de rebotes). Entre 15 y 25 m se puede, con pull-up de 1 kΩ y prueba de banco aprobada antes de despachar. **Arriba de 25 m por rama, no se discute: va una base por reefer.** Y ojo con el tercer módulo del plan de Andrés: si pretende cubrir con un cable largo los dos reefers que están separados, **ese módulo es el escenario descartado en chiquito** y hay que romperlo en dos — pueden ser 4 equipos, no 3.

### 2.4-bis La línea de firmware que va a Cerro Moro (no es un detalle)

**A Cerro Moro va la línea `entrega_scz`, no `firmware_modular`.** Hay que escribirlo en la orden de armado y en el runbook, porque las dos compilan y las dos "andan":

- `entrega_scz/firmware/sondas.h` **identifica cada sonda por su ROM de 64 bits**, persistida en NVS. Es lo que hace posible tener más de una sonda por equipo sin que se crucen las lecturas.
- `firmware_modular/sensors.h` **lee por índice** (`getTempCByIndex(0)` y `(1)`) y fija el conteo una sola vez al arrancar. Con dos sondas, si se cae la del índice 0, **la que sobrevive pasa a reportarse con el nombre de la otra sin que nada avise**, mientras la "Sonda 2" alerta desconexión. O sea: el número que llega al panel es de la otra sonda física.

En una propuesta que se vende como **trazabilidad para auditoría**, un dato correcto atribuido al sensor equivocado no es un bug menor: es la propia prueba invalidada. Aceptable con una sonda; **inaceptable con dos**, y letal con cuatro.

### 2.5 Qué se instala y quién lo instala

Por base: caja estanca, fuente, prensacables, sondas DS18B20 estancas con su cable, y el paso de cable al reefer.

**Lo instala Andrés, en sitio, con el kit preconfigurado y probado en banco en Bahía + puesta en marcha por videollamada.** Esto no es una limitación disfrazada: es la única forma sensata a 1.500 km, y **hay que valorizarlo en voz alta**. Dos pasajes a Santa Cruz, alojamiento, traslados internos, inducción de seguridad y 5 días de un ingeniero fuera de su trabajo están en el orden de **$ 2.500.000**, y además **Matías no puede viajar en octubre** (parada de planta de Louis Dreyfus, fecha inamovible). Que Andrés esté adentro convierte un proyecto imposible en uno de esta semana.

Por eso esta propuesta **no tiene línea de instalación**, y así hay que decirlo: no es un descuento, es un costo que no existe porque ellos ponen las manos.

### 2.6 Lo opcional, que no entra en la primera orden de compra

- **Sensor de puerta por reefer** (reed + imán): la causa más común de pérdida en un campamento es una puerta que quedó abierta. $ 25.000 por sensor + $ 10.000/mes por reefer. **Se ofrece después de que las sondas estén andando**, no antes: la primera orden de compra tiene que ser simple.
- **Sirena local** en el pasillo de reefers: $ 60.000 + $ 10.000/mes.

---

## PARTE 3 — Modelo comercial

### 3.1 La decisión: venta de equipos + desarrollo + abono. NO comodato.

Con comercios de Bahía el modelo es **comodato con depósito de garantía reintegrable** (`PLATA.md` L15). **Acá no.** Razones, en orden:

1. **Una minera no deja un "depósito de garantía".** Su sistema de compras emite órdenes de compra contra bienes y servicios; un depósito reintegrable es una cuenta a cobrar que a ellos les complica el asiento y a nosotros nos obliga a devolverlo algún día.
2. **A 1.500 km no queremos el equipo de vuelta.** El comodato existe para poder retirar el equipo si el cliente deja de pagar. Retirar tres cajas de Cerro Moro cuesta más que las cajas.
3. **El equipo es barato y el servicio es lo que vale.** El costo de materiales de una base está en el orden de USD 30-45 (`docs/LISTA_MATERIALES.md`). Regalar la discusión del fierro y pelear por el abono es la jugada correcta: **la métrica es abonos activos**, no venta de hardware.
4. **Vender el equipo mata la objeción "¿y si desaparecen?"** El fierro queda de ellos. Lo que se contrata mes a mes es el servicio — y si un día lo dan de baja, se quedan con equipos que sin nube no alertan (eso también hay que decirlo, va en la cláusula de límite de responsabilidad).

**Estructura propuesta, tres líneas separadas y facturables por separado** (a una minera esto le importa: son tres partidas presupuestarias distintas):

| Línea | Naturaleza | Cuándo se factura |
|---|---|---|
| **Desarrollo y puesta en servicio industrial** | Servicio, pago único, por etapas | 40 % a la OC · 30 % a la aceptación de E2+E3 · 30 % a la aceptación de E4 |
| **Equipos, repuestos y materiales** | Bienes, pago único | 100 % contra entrega en sitio (o 50/50 si lo piden) |
| **Servicio mensual de monitoreo** | Servicio recurrente | Mensual adelantado |

### 3.2 Lo que hay que averiguar antes de emitir una cotización en firme

Esto **no se adivina**: se pregunta, y cuanto antes mejor, porque puede cambiar el número.

| Qué | Por qué importa | A quién se pregunta |
|---|---|---|
| **Alta como proveedor**: qué exige el sistema de compras de PAAS Argentina (legajo, constancia de inscripción, referencias, firma del Código de Conducta de Proveedores) | Sin alta no hay orden de compra, y el alta puede tardar semanas. Es el camino crítico administrativo, no el técnico | Andrés → Compras / Abastecimiento |
| **¿Aceptan monotributista o exigen Responsable Inscripto?** | Muy probablemente exijan RI (quieren crédito fiscal). Si es así, hay que resolverlo con el contador **antes** de cotizar, y el precio cambia (IVA) | Compras + contador de Matías |
| **Condición de pago: 30 / 60 / 90 días fecha de factura** | A 60 días hay que financiar dos meses de servicio con plata propia. Con estos montos se banca; conviene saberlo igual | Compras |
| **Seguros: ¿piden póliza de RC? ¿ART?** | **Si el montaje lo hace Andrés (personal de la mina), no hay nadie nuestro pisando el sitio y no corresponde ART nuestra.** Hay que dejarlo escrito así, porque es lo que evita todo el legajo de contratista | Andrés + HSE |
| **¿Orden de compra por proyecto o contrato marco de servicio?** | Un contrato marco con renovación automática protege el abono mucho mejor que una OC que se agota | Compras |
| **Moneda y ajuste** | Ver §4.7 | Compras |
| **Quién firma y hasta qué monto** | Saber si Andrés puede firmar $ 6 M o hay que subir. Define a quién hay que mostrarle el sistema | Andrés |

### 3.3 Un punto de integridad que hay que cuidar (importante)

Andrés es **el origen del lead de Venado Tuerto** y ofreció presentar clientes en Bahía. Es un aliado, y hay que tratarlo como tal. **Pero:**

> **No se le paga ni se le ofrece a Andrés ninguna comisión, incentivo ni beneficio ligado a que Pan American compre.** Nada. Ni "un porcentaje", ni "algo por la gestión", ni un equipo de regalo mientras la compra esté en discusión.

Pan American Silver tiene un **Código de Conducta de Proveedores** público que exige cumplimiento de las leyes aplicables, y toda minera grande tiene política anticorrupción. Un pago a un empleado que influye en una compra es exactamente lo que esas políticas persiguen: nos quema el cliente, lo quema a él y quema la marca. **El costo de un "gracias" mal puesto es infinitamente mayor que el negocio.**

Lo que **sí** se puede y se debe hacer: agradecer por escrito, darle un sistema que lo haga quedar bien adentro (que es lo que él está buscando: *"la gente de acá no lo vio, no saben ni cómo entrar"*), y tratar **por separado y con otra lógica** los referidos de Bahía y Venado Tuerto, que no tienen nada que ver con la compra de Panamerican. Si alguna vez se formaliza un esquema de referidos, se hace con clientes que no sean su empleador y se pone por escrito.

---

## PARTE 4 — Los números, desglosados

**DECIDIDO POR MATÍAS (3-sep-2026): se cotiza en DÓLARES y se acepta el pago en pesos.** Todo importe de esta parte está en dólares, con el equivalente en pesos al lado al **tipo de cambio de referencia BNA vendedor $ 1.535 (3-sep-2026, verificado ese día)**. Los precios se redondearon a números comerciales limpios (ver §4.1 y §4.3): son precios, no divisiones.

> **La línea que va en la cotización, textual:** *"Facturación en dólares estadounidenses. De abonarse en pesos, se toma el tipo de cambio vendedor del Banco de la Nación Argentina de la fecha de pago."*
> Va como **propuesta**, no como condición: en una minera las condiciones de pago las fija compras en la orden de compra. **En el PDF del cliente no va ninguna validez de la cotización** (§4.7).

### 4.1 Desarrollo — cómo se arma el número

Valor hora usado: **USD 25/h** (≈ $ 38.375 al cambio de referencia). Es **la mitad del piso de la banda mid-level de LATAM** (USD 35-55/h; senior USD 65-85/h, LATAM Developer Hourly Rates citado por Teclab, 2026), y se justifica porque no hay overhead de agencia ni intermediario. No es un precio inflado: es un precio de ingeniero que factura directo.

| Bloque | Horas | Qué incluye | ¿Se cobra? |
|---|---|---|---|
| **Específico de Cerro Moro** | | | |
| Puesta en servicio de sondas, rangos y umbrales por reefer, calibración | 16 | Hoy el umbral está en 50 °C (ambiente) y **nunca alertó por temperatura real** | Sí, 100 % |
| Registro auditable exportable con código de verificación | 20 | Es lo que compra una minera: la prueba, no la alerta | Sí, 100 % |
| Panel multi-equipo + usuarios de PAAS con rol de lectura | 16 | *"no saben ni cómo entrar"* — hoy no hay roles ni multiusuario | Sí, 100 % |
| Puesta en marcha remota, pruebas de campo con Andrés, documentación y capacitación | 20 | Videollamadas, runbook, guía de 1 página para el turno | Sí, 100 % |
| **Salud de bus**: distinguir "sonda desconectada" de "bus con ruido", + histéresis de 3 barridos antes de alertar | 8 | Hoy los dos casos devuelven el mismo −127 y **la evidencia que los separa se descarta**; y se alerta con **un solo** barrido fallido → del orden de **una falsa alarma por día**. Ver §5 | Sí, 100 % |
| **Subtotal específico** | **80 h** | | **USD 2.000** ≈ $ 3.070.000 |
| **Plataforma (se reusa en todos los clientes)** | | | |
| Seguridad: RLS cerrada, credencial por equipo, secretos fuera del binario, revocar claves quemadas | 40 | Hoy la clave anon del `.bin` público es **llave maestra de escritura**: con ella cualquiera desde internet falsifica el historial o apaga el equipo | Sí, **50 %** |
| Buffer offline: lecturas y alertas encoladas | 16 | Hoy se pierden datos durante los cortes; `offlineQueue[50]` está declarada y sin usar | Sí, **50 %** |
| Vigía de equipo mudo con escalado (aviso 5 min / alarma 30 min) | 12 | **Un equipo muerto no puede avisar que está muerto** | Sí, **50 %** |
| OTA con manifiesto inmutable + `OTA_URL` | 12 | De noche, con uplink degradado, entró **1 de 4 intentos**; las últimas versiones se flashearon por cable | Sí, **50 %** |
| **Subtotal plataforma** | **80 h** | Se cobra la mitad | **USD 1.000** ≈ $ 1.535.000 |
| **TOTAL DESARROLLO** | **160 h** | | **USD 3.000 → se propone USD 2.950** ≈ $ 4.528.000 |

**Por qué la plataforma se cobra al 50 % y no al 100 %:** ese trabajo también sirve para Venado Tuerto y para cada comercio de Bahía. Cobrárselo entero a Panamerican sería cobrarle a un cliente el producto de todos. Cobrarlo a cero sería regalar 80 horas porque el que apura es él. **La mitad es la respuesta honesta, y decirlo así construye confianza en vez de gastarla.** Esta línea es negociable a la baja solo si a cambio entra el sexto reefer o los sensores de puerta; nunca "porque sí".

### 4.2 Sobre el número que Matías recordaba

Matías mencionó de memoria un orden de magnitud de **~$1.000.000 de desarrollo + ~$100.000/mes** (al cambio de hoy, USD 650 y USD 65/mes). Lo busqué: **no hay ningún documento previo que lo respalde.** El número que sale de construirlo desde cero es **4,5 veces más alto en desarrollo** y **3 veces más alto en abono**. Las tres razones:

1. **$1.000.000 de desarrollo son USD 650: 26 horas.** Solo la lista de trabajo crítico de la auditoría de agosto (seguridad + buffer offline + vigía + OTA) no entra en 26 horas ni cortándola por la mitad.
2. **$100.000/mes (USD 65) está por debajo del costo de servir a este cliente.** La cuenta está en §4.4: el costo directo mensual es **USD 110 ≈ $ 169.000**. A $100.000/mes se pierde plata todos los meses, y el que pierde plata todos los meses termina dejando de atender al cliente — que es la peor forma de perder una minera.
3. **Para Pan American, USD 4.350 no es un número grande.** Es la inversión inicial completa. Una cotización demasiado barata en minería no gana la compra: **la vuelve sospechosa**. El riesgo real acá es subcotizar, no sobrecotizar.

### 4.3 Equipos, repuestos y materiales

Precio unitario: **base USD 120** · **sonda estanca con cable USD 40**. Sobre un costo de materiales del orden de USD 30-45 por base, el multiplicador cubre armado, prueba en banco documentada, gabinete apto intemperie, envío a Santa Cruz y la garantía de reposición.

| | **Escenario B — 5 bases (RECOMENDADO)** | Escenario A — 3 bases |
|---|---|---|
| Bases | 5 × 120 = USD 600 | 3 × 120 = USD 360 |
| Sondas (2 por reefer × 5) | 10 × 40 = USD 400 | 10 × 40 = USD 400 |
| **Repuestos en sitio** (1 base + 2 sondas) | USD 200 | USD 200 |
| Materiales de montaje (fuente, prensacables, canalización, protección) | 5 × 40 = USD 200 — **tiradas de 2-5 m** | 3 × 73 = USD 220 — **CAT5 largo, canalización entre contenedores, pull-up de 1 kΩ** |
| **TOTAL** | **USD 1.400** ≈ $ 2.149.000 | **USD 1.180** ≈ $ 1.811.000 |

Notar la línea de materiales: **el escenario recomendado usa ~30 m de cable contra 60-150 m del otro**, así que la diferencia total no es la de tres bases sino **USD 220** — poco más de un mes de abono. Es el mejor argumento contra "el de 5 equipos es mucho más caro": no lo es.

**Los repuestos en sitio no son opcionales y hay que venderlos como criterio, no como upsell.** A 1.500 km, sin repuesto, una base rota es un reefer ciego durante una semana de logística. Con repuesto, Andrés cambia la caja en diez minutos y nosotros reponemos el repuesto por correo sin apuro. Es la diferencia entre un servicio y un problema.

### 4.4 Servicio mensual — qué cuesta servir y qué se cobra

**Costo directo mensual de este cliente:**

| Concepto | USD/mes | Fuente |
|---|---|---|
| Nube dedicada (Supabase Pro — el free tier **se pausa por inactividad**, no sirve para un cliente que paga) | 25 | Precio de lista |
| Reposición amortizada (1 base/año + envíos a Santa Cruz) | 10 | USD 120/12 |
| Soporte y vigilancia del servicio (2 h/mes de ingeniero) | 50 | 2 × USD 25 |
| Informe mensual de cadena de frío por reefer (1 h) | 25 | |
| **Costo directo** | **USD 110/mes** ≈ $ 169.000 | |

**Tarifa propuesta, con estructura escalable:**

| Concepto | USD/mes |
|---|---|
| Cargo fijo de sitio (nube dedicada, soporte, vigía de equipos mudos, informe mensual) | **100** |
| Por reefer monitoreado (incluye sus 2 sondas) | **20** |
| **5 reefers activos** | **USD 200/mes** ≈ $ 307.000 |
| 6 reefers (cuando vuelva el que está fuera de servicio) | USD 220/mes |

Son **USD 40 por reefer por mes**, con margen bruto de **USD 90/mes** (≈ $ 138.000) sobre el costo directo. Y es una estructura que se explica sola: si mañana suman un reefer, son veinte dólares más, no una renegociación.

**Qué cubre el abono — y qué está operativo hoy y qué no** (nada se cobra antes de estar andando, igual que la cláusula 2.2 del contrato v4):

| Incluido en el abono | Estado hoy |
|---|---|
| Nube dedicada, retención de datos **12 meses** | Operativo (la nube existe; la retención se configura) |
| Alerta por temperatura fuera de rango, por reefer, con umbral y tiempo acordados | **Etapa E0** (hoy el umbral es 50 °C y nunca alertó por temperatura real) |
| Alerta de sonda desconectada o rota | Existe en firmware; **no llega a Telegram** hoy → E1 |
| Aviso de "equipo dejó de reportar" con escalado | **Etapa E1** |
| Panel web y app, con usuarios de PAAS | **Etapa E4** |
| Informe mensual de cadena de frío por reefer | **Etapa E4** |
| **Reposición sin cargo** de equipo fallado, con envío incluido | Desde el día 1 |
| Actualizaciones de firmware y nube, sin cargo | Desde el día 1 (con OTA confiable desde E3) |
| Soporte por WhatsApp/teléfono con Matías, respuesta el mismo día hábil | Desde el día 1 |

**Escalón de precio durante el endurecimiento (esto es lo que hace la propuesta honesta):**
- Desde la orden de compra hasta la aceptación de la etapa E4 → **USD 100/mes** ≈ $ 153.500 (el cargo fijo de sitio, sin cargo por reefer). Es **el costo directo, sin utilidad**; de hecho queda USD 10 por debajo del costo, o sea que durante el endurecimiento el servicio se sirve levemente a pérdida, y es deliberado.
- Desde la aceptación de E4 (19-dic-2026) → **USD 200/mes** ≈ $ 307.000.

Está escrito de antemano, con fecha, y no se renegocia después. Es exactamente la regla de `PLATA.md`: **el precio se dice ANTES, no al final.**

### 4.5 Total del primer año

| | **Escenario B (RECOMENDADO)** | Escenario A |
|---|---|---|
| Desarrollo | USD 2.950 | USD 2.950 |
| Equipos | USD 1.400 | USD 1.180 |
| **Inversión inicial** | **USD 4.350** ≈ $ 6.677.000 | USD 4.130 ≈ $ 6.340.000 |
| Abono (4 meses a USD 100 + 8 meses a USD 200) | USD 2.000 | USD 2.000 |
| **TOTAL AÑO 1** | **USD 6.350** ≈ $ 9.747.000 | USD 6.130 ≈ $ 9.410.000 |
| **Recurrente desde el año 2** | **USD 2.400/año** ≈ $ 3.684.000 | idem |

### 4.6 Crecimiento ya cotizado (no se rediscute nada después)

| Agregado | Único | Mensual |
|---|---|---|
| **Sexto reefer** cuando vuelva a servicio, con su propia base (2 sondas + base + materiales) | USD 240 | + USD 20 |
| Sensor de puerta por reefer | USD 20 c/u | + USD 7 c/u |
| Sirena en el pasillo de reefers | USD 40 | + USD 7 |
| Sonda adicional en un reefer ya cubierto | USD 40 | + USD 5 |

### 4.7 Moneda y ajuste — DECIDIDO (3-sep-2026)

**Se cotiza en dólares y se acepta el pago en pesos.** Es lo natural para una minera (piensa en dólares), elimina la discusión de inflación, y **esquiva el problema legal de la cláusula de ajuste por IPC**: la prohibición de indexar (leyes 23.928 art. 10 y 25.561 art. 4) sigue vigente fuera de la locación de inmuebles, y por eso las cláusulas IPC del contrato v4 están marcadas "a validar".

**La línea, textual, tal como va en la cotización:**

> *"Facturación en dólares estadounidenses. De abonarse en pesos, se toma el tipo de cambio vendedor del Banco de la Nación Argentina de la fecha de pago."*

**Va como propuesta, no como condición impuesta, y a propósito.** Pan American es una empresa grande y extranjera: las condiciones de pago las fija su área de compras en la orden de compra, no el proveedor. Por eso la línea es sobria, sin "se exige" y sin párrafo explicativo. El motivo de ponerla igual: **si el proveedor no propone nada, se aplica la política del comprador sin discusión; si la propone, muchas veces compras la toma tal cual.**

**En el PDF del cliente no va ninguna validez de la cotización, y es deliberado.** La validez existe para cubrirse de la devaluación, y cotizando en dólares eso ya está cubierto; ponerle vencimiento a una compra que en una minera tarda meses en aprobarse solo obliga a re-cotizar y le da al comprador una excusa para reabrir la negociación. **Nota interna:** si pasan más de 6 meses desde el 3-sep-2026, revisar precios antes de facturar (costo de reposición, nube y equipos) — por decisión propia, no porque un papel lo obligue.

**Si fijan el tipo de cambio a la fecha de FACTURA y pagan a 60 días**, esto es lo que cuesta, sobre un margen de USD 90/mes:

| Si el peso se deprecia entre factura y pago | Se cobra realmente | Se pierde | Sobre el margen |
|---|---|---|---|
| 10 % | USD 182/mes | USD 18/mes | se va el **20 %** del margen |
| 20 % | USD 167/mes | USD 33/mes | se va el **37 %** del margen |
| 30 % | USD 154/mes | USD 46/mes | se va el **51 %** del margen |

Sobre la inversión inicial de USD 4.350 el mismo efecto son **USD 395** con 10 % y **USD 725** con 20 %.

**Si Panamerican impone su propia política cambiaria** —hay compañías que solo emiten órdenes de compra en pesos, a valor fijo, o que fijan el tipo de cambio de su propia tesorería—, la respuesta es esta:

- **El piso es el costo directo: USD 110/mes** (≈ $ 169.000 al cambio de hoy; son los $ 167.000 de la cuenta de §4.4). Por debajo de eso no se firma en ninguna moneda, porque un servicio que pierde plata todos los meses se termina desatendiendo, y desatender a una minera es perderla.
- **Con un abono fijo de $ 307.000/mes, el número deja de cubrir el costo directo cuando el dólar pasa de $ 2.790**, es decir con una suba del **82 %** desde hoy. Ese es el colchón real de un precio fijo en pesos: para 12 meses alcanza salvo salto grande; para 24, no. **Y ojo con el escalón: el abono reducido del endurecimiento, $ 153.500 fijos, ya está por debajo del costo directo hoy mismo** — en pesos fijos ese tramo hay que acortarlo o cobrarlo al costo pleno.
- **Si exigen pesos a valor fijo por 12 meses**, hay que pedir una de tres: revisión trimestral pactada por escrito, o un precio en pesos con colchón calculado sobre el plazo (no un número redondo puesto a ojo), o plazo de pago corto (15 días) que haga irrelevante la diferencia. Si no aceptan ninguna, el abono en pesos fijos se cotiza tomando el costo directo como suelo y el colchón por encima, y **el que decide si vale la pena es Matías, con el número a la vista**.
- **La inversión inicial (pago único) es lo menos sensible**: se cobra al principio y el riesgo cambiario dura lo que tarde la orden de compra. La pelea de la moneda hay que darla en el **abono**, que es lo que se cobra 12 veces por año.

### 4.8 Contra una sola pérdida de carga

Al valor **más conservador posible** — precio de novillo **en pie**, $ 4.181/kg (índice INMAG, jul-2026), que es mucho menor que el de la carne ya faenada y puesta en un campamento a 1.500 km:

| Pérdida | Valor | Equivale a |
|---|---|---|
| 500 kg (un reefer parcialmente cargado) | $ 2.090.000 | casi 7 meses de servicio |
| 3.000 kg | $ 12.543.000 | **3 años y 5 meses de servicio** |
| Un reefer lleno (~10 t) | $ 41.810.000 | más de 11 años de servicio |

*Equivalencias calculadas contra el abono pleno de USD 200/mes ≈ $ 307.000 al cambio de referencia.*

Y eso es solo la mercadería. En un campamento aislado, lo que de verdad duele es lo otro: **hay que dar de comer igual**, y reponer de urgencia a 1.500 km cuesta más que la mercadería perdida.

### 4.9 Contra las alternativas de mercado

| Alternativa | Costo verificado | Por qué no resuelve ESTE problema |
|---|---|---|
| **testo Saveris 2-T2** (logger WiFi con contacto de puerta) | **USD 318** por unidad (listado eBay, sep-2026; RS Online HK$ 2.294,50 ≈ USD 295). **10 unidades = USD 3.180 ≈ $ 4.881.000 solo de hardware**, antes de importación, y sin la licencia anual de nube | **Se configura con una red WiFi y una clave.** Las redes del campamento son abiertas y la más potente no da internet — lo medimos 128 veces. El logger de catálogo se queda mudo el día 1 y nadie en Cerro Moro lo puede diagnosticar. Además: sin proveedor local, sin repuesto en sitio, garantía por courier internacional |
| Sensor WiFi genérico de MercadoLibre | ~$ 130.000 | Sin instalación, sin soporte, sin informe, sin nadie que mire si dejó de reportar. Es un juguete para una heladera de casa |
| Servicio de monitoreo IoT nacional (IoTMonitoreo, Soluciones FMK, UTelemetry) | Sin precio público — cotizan a medida | Son competencia real y hay que decirlo. Nuestra ventaja no es el precio: es que **ya estamos adentro y funcionando**, y que el problema difícil del sitio (la red) ya está resuelto y probado ahí |
| No hacer nada | $ 0 | Es la alternativa que están usando hoy |

La comparación honesta con testo no es "somos más baratos" (USD 3.180 de loggers contra USD 1.400 de nuestros equipos, pero sin importación, sin licencia de nube y sin nadie que atienda: más o menos empatamos en fierro). Es: **el mismo dinero, pero funcionando en este sitio, con alguien que atiende el teléfono en castellano y con repuesto a diez metros de los reefers.**

---

## PARTE 5 — Lo que NO se promete todavía (innegociable)

La auditoría del 26-ago-2026, hecha por cinco revisores independientes que leyeron el código en frío, concluyó: **"prototipo que funciona de punta a punta, pero NO apto para venderse a una minera hasta endurecerlo"**. Los hallazgos descalificantes:

- **La clave de la app es una llave maestra de escritura**, en claro dentro de un binario en un bucket público. Con ella, desde internet, cualquiera puede falsificar el historial de temperatura (o sea: **ocultar una rotura de cadena de frío**), disparar alarmas falsas, apagar o reflashear el equipo y cambiar los umbrales para que nunca alerte. No hay multitenancy.
- **Se pierden datos durante los cortes.** No hay buffer offline. Y **las alertas que se disparan sin red se pierden para siempre.**
- **Nunca alertó por temperatura real.** El umbral está en 50 °C porque hasta hoy mide ambiente.
- **Un equipo muerto no puede avisar que está muerto.** Falta el vigía del lado de la nube.
- **El OTA no propaga confiablemente**: 1 de 4 intentos de noche; las últimas versiones se flashearon por cable.

**Nada de eso se oculta, y nada de eso se regala: se cobra como desarrollo, con etapas, fechas y aceptación del cliente.** Un sistema cuyo trabajo es ser la prueba de que la cadena se mantuvo no puede venderse con un agujero por el que se puede falsificar esa prueba.

### Plan de endurecimiento

Restricción real que condiciona el cronograma: **octubre es la parada de planta de Louis Dreyfus** (fecha inamovible del portfolio de Matías) y hasta el 31-oct su disponibilidad para este proyecto es acotada. Por eso las etapas pesadas caen después. **Esto se le dice al cliente**: una fecha cumplida vale más que una fecha optimista.

| Etapa | Qué entrega | Desde | Hasta | Cómo se acepta |
|---|---|---|---|---|
| **E0 — Sondas adentro y umbrales reales** | Andrés monta las 2 sondas del REEFER_01 adentro; se acuerda rango y tiempo de alerta; primera alerta por temperatura real verificada punta a punta | lun 8-sep | **vie 19-sep** | Captura de la alerta recibida en el celular de Andrés + registro en la nube |
| **E1 — Que no se pierda un dato ni un aviso, y que no sobre ninguno** | Buffer offline de lecturas, alertas encoladas cuando no hay red, alerta de sonda caída que sí llega, y **vigía de equipo mudo con escalado** (aviso a 5 min, alarma a 30 min). *Ya hay tres ramas escritas y sin mergear, del 23, 26 y 29 de agosto.* **Más los dos ítems de salud de bus del §5.1** | lun 22-sep | **vie 10-oct** | Prueba en sitio: se desenchufa el equipo y llega la alarma; se corta la red 20 min y no falta ninguna lectura; y **una semana entera sin una sola alarma falsa** |
| **E2 — Credencial por equipo** | RLS cerrada (anon solo lectura), escrituras y comandos detrás de backend con credencial por equipo, secretos fuera del binario, revocación de las claves ya quemadas. *Se aplica con el equipo a la vista y verificando los tres caminos del firmware tras cada política: una RLS mal escrita deja el equipo mudo a 1.500 km* | lun 13-oct | **vie 14-nov** | Demostración: con la clave vieja ya no se puede escribir; el equipo sigue reportando |
| **E3 — OTA con manifiesto** | Manifiesto inmutable por versión + cambio de `OTA_URL` por comando, sin depender del caché del CDN | lun 17-nov | **vie 28-nov** | Tres actualizaciones seguidas entrando por aire al primer intento |
| **E4 — Panel de la minera y registro auditable** | Usuarios de PAAS con rol de lectura, vista de los reefers en una pantalla, exportación mensual con código de verificación, informe mensual automático | lun 1-dic | **vie 19-dic** | Un usuario de PAAS entra solo y descarga el informe del mes |

**Aceptación final: viernes 19-dic-2026.** Desde ese día el abono pasa a tarifa plena.

### 5.1 Dos ítems chicos y baratos que entran en E1 — y que valen más de lo que cuestan

Salieron del análisis de bus de `@muestreador` (§2.4). Son 8 horas en total y están cotizados dentro del desarrollo (§4.1), pero merecen un párrafo propio porque **atacan el modo de falla que arruina productos como este**.

**(a) Distinguir "sonda desconectada" de "bus con ruido".** Hoy no se puede, y la evidencia se está tirando: la lectura devuelve el mismo valor de error (−127) tanto si la sonda no contestó como si el CRC de la respuesta salió mal por ruido. Verificando el CRC nosotros y llevando contadores por sonda queda un diagnóstico de cuatro estados en lugar de uno: **bus caído** (el cable principal), **sonda desconectada** (la alerta actual, que está bien), **bus degradado con ruido** (que hoy no existe y debería ser aviso de mantenimiento, no alarma crítica), y **conversión que no ocurrió** (la lectura de 85,00 °C exactos, que es el canario: significa que la sonda perdió tensión justo mientras medía). Con esos contadores viajando en el dato, **vemos la degradación desde Bahía Blanca meses antes de que falle**, en lugar de enterarnos por un reclamo.

**(b) Histéresis de 3 barridos antes de alertar por sonda faltante.** Hoy alerta con **un solo** barrido fallido. A un barrido cada 30 segundos, eso da del orden de **una falsa alarma por día**; exigiendo tres barridos seguidos, prácticamente cero. **Este cambio hay que hacerlo aunque se instale una base por reefer**, porque no depende de la distancia.

Por qué importa comercialmente, dicho sin vueltas: **una falsa alarma diaria en una minera mata la credibilidad del sistema en la primera semana.** El operador aprende a ignorar el aviso, y el día que la alarma es de verdad, no la mira nadie. Es la única forma de que este producto falle sin que ninguna pieza se rompa.

Dos cosas más que hoy quedan afuera y hay que decirlas:
- **Aviso de corte de energía desde el sitio.** Sin batería y línea propia, si se corta la luz el equipo no mide ni avisa; lo que avisa es la nube, diciendo "dejó de reportar". Como en el campamento hay generación propia, probablemente alcance — **pero se pregunta, no se asume**. Si hace falta, es un desarrollo aparte con batería y 4G, y se cotiza cuando exista.
- **La cadencia de reporte cambia en producción.** Hoy el equipo manda cada ~5 s, que está bien para poner a punto pero no para producción: 10 sondas a 5 s son **5,2 millones de filas por mes**; a 1 minuto son 432.000. Se pasa a lectura cada 1-5 minutos con ráfaga rápida cuando hay un evento. Es parte de E0 y baja el costo de nube — o sea, sostiene el abono.

---

## PARTE 6 — Qué necesitamos del cliente para cerrar

Ocho cosas. Las primeras cuatro las puede contestar Andrés esta semana; las últimas cuatro necesitan que alguien más entre en la conversación.

1. **Las distancias medidas.** De cada reefer al punto donde puede ir la base (con 220 V disponible y donde llegue alguna de las redes). Metros, y si el cable va por bandeja/caño o queda a la intemperie. **Es lo único que puede devolver a la mesa el escenario A, más barato**: si cada tirada da <= 15 m, contigua y en línea, se recotiza con 3 equipos y se ahorran USD 220.
2. **Una foto** de la puerta de un reefer y del lugar por donde entraría el cable (¿hay un paso existente o hay que hacerlo?).
3. **Rango de temperatura de cada reefer** (¿congelado a −18? ¿refrigerado a +2/+4?) **y cuánto tiempo fuera de rango es un problema**: 5 minutos, 30 minutos, 2 horas. Eso define el umbral y el tiempo de alerta, y es lo que evita que el sistema moleste con falsas alarmas.
4. **Quiénes reciben la alerta, en qué turno y por qué medio.** Nombres y teléfonos.
5. **Quién firma la orden de compra**, y hasta qué monto puede firmar Andrés sin subir.
6. **Cómo se factura**: requisitos de alta como proveedor, si aceptan monotributista o exigen Responsable Inscripto, condición de pago (30/60/90 días), confirmación de la cláusula de moneda (precios en dólares, pago en pesos al tipo de cambio vendedor del BNA del día del pago efectivo), y si corresponde alguna póliza. **Confirmar por escrito que, montando Andrés, no hay personal nuestro en sitio y no corresponde legajo de contratista ni ART.**
7. **A quién más hay que mostrarle el sistema.** Andrés ya dijo lo importante: *"la gente de acá no lo vio, no saben ni cómo entrar"*, y que cuando ponga las sondas se lo va a mostrar a todos. Los perfiles que importan: **mantenimiento** (los que arreglan el reefer), **catering/alimentos** (los que pierden la mercadería), **HSE/calidad** (los que necesitan el registro) y **compras** (los que firman). Pedir un nombre de cada uno.
8. **¿Hay generación de respaldo en el sector de reefers?** Define si hace falta cotizar aviso de corte de energía.

### Lo que le facilita a Andrés mostrarlo adentro (esto lo preparamos nosotros)

El equipo instalado **es la demo**. Para que funcione como demo hay que darle a Andrés tres cosas, y ninguna cuesta plata:

- **Un enlace y un usuario que entre sin explicación** (aunque sea provisorio, antes de E4): que cualquiera abra el panel en el celular y vea la temperatura de ahora.
- **Una hoja de una carilla** con qué es, qué avisa y a quién llamar. Para dejar impresa en el pasillo.
- **El momento del hielo**: cuando ponga las sondas adentro, que agarre una y la saque un minuto al ambiente delante de la gente. La curva sube en el celular en vivo. **Nadie que ve eso pregunta cómo funciona.** Ese es el argumento, no el PDF.

---

## PARTE 7 — Mensaje de WhatsApp para Andrés

> Él es el canal, no el que firma. Corto, agradecido, concreto, y que le deje algo para mostrar adentro.
> Se manda **después** de que Matías apruebe los números.

```
Andrés, gracias por reconectar el equipo, lo vi entrar enseguida desde acá.
Está reportando bien y ya lo tengo a la vista.

Dale, metelas adentro cuando puedas. Antes decime dos cosas:
1) ¿A cuántos grados tiene que estar cada reefer, y cuánto tiempo fuera
   de rango ya es un problema? (5 minutos, media hora, dos horas)
2) ¿A qué teléfonos querés que lleguen los avisos?

Con eso queda alertando de verdad esta misma semana.

Lo de la parte económica lo armé: te paso un resumen de una carilla para
que lo puedas mostrar ahí adentro sin tener que explicarlo vos.
La idea es cubrir los 5 reefers en servicio con 2 sondas cada uno, que los
equipos los montes vos (así no hay que mandar a nadie desde acá, que es lo
que encarece todo), y un servicio mensual que incluye soporte, reposición
sin cargo si algo falla, y un informe mensual por reefer.

Sobre lo que me habías dicho de 3 modulos de a dos reefers: lo estudie en
serio y te lo cotizo igual, pero te recomiendo un equipo por reefer. El
motivo corto: el cable de las sondas es la parte fragil de todo esto, y si
igual hay que tirar cable hasta el otro reefer, es mas seguro tirar 220 y
poner un equipo ahi que tirar el cable de sondas. Ademas cada reefer tiene
su propia tierra y unirlas con un cable fino te mete error en la medicion.
Son unos 220 dolares de diferencia, una sola vez: prefiero que midan bien.

Igual necesito de tu lado una cosa que no puedo resolver desde aca: medir
con cinta cuantos metros hay de cada reefer hasta donde podria ir la cajita
(donde haya 220 y llegue alguna de las redes). Si te dan cortitas, menos de
15 metros y en linea, volvemos a los 3 equipos y te ahorro esa plata.

Y decime quién es el que firma una compra de este tamaño y qué le piden a
un proveedor nuevo para darlo de alta, así lo voy tramitando en paralelo.

Cuando pongas las sondas y se lo muestres a los demás, avisame y te dejo un
acceso listo para que entren desde el celular y lo vean, sin que tengas que
explicar nada. Tip: sacá una sonda al aire un minuto delante de ellos y
mirá la pantalla. Eso convence más que cualquier presentación.

Gracias de nuevo por el empuje, che.
```

**Regla para el follow-up:** si el viernes 5 no hay respuesta, se reitera **el lunes 8** solo con la pregunta 1 (los rangos), que es la que desbloquea la instalación de las sondas. **No se manda el precio dos veces.**

---

## Anexo — Fuentes consultadas (3-sep-2026)

- Estado real del equipo y auditoría: `C:\Proyectos\frioseguro\entrega_scz\docs\ESTADO_HONESTO.md` y `AUDITORIA_HALLAZGOS.md` (26-ago-2026).
- **Alcance del bus 1-Wire, topologías, pull-ups, tierras y el veredicto de escenarios: `C:\Proyectos\frioseguro\hardware\ALCANCE_1WIRE.md` (@muestreador, 3-sep-2026)** — es la fuente de toda la §2.4.
- Techo de 4 sondas por base: `C:\Proyectos\frioseguro\entrega_scz\firmware\sondas.h`, `#define SONDAS_MAX 4`. Identificación por ROM vs. por índice: ese archivo contra `firmware_modular/sensors.h`.
- Costo de materiales: `C:\Proyectos\frioseguro\docs\LISTA_MATERIALES.md` (~USD 30-45 por emisor).
- Modelo y tarifa de comercios (que acá NO se aplica): `C:\Proyectos\frioseguro\TERMOVIGIA.md` §3 · `PLATA.md` Línea 1.
- Contrato base a adaptar: `MATI-HQ\comercial\CONTRATO_TERMOVIGIA_v4.md` (límite de responsabilidad, dependencia de terceros, funciones "a desarrollar" que no se cobran).
- 1-Wire, límites de longitud: Maxim/Analog Devices, Application Note 148 "Guidelines for Reliable Long Line 1-Wire Networks" — https://www.maximintegrated.com/en/design/technical-documents/tutorials/1/148.html
- testo Saveris 2-T2, USD 318: https://www.ebay.com/itm/365602217221 · HK$ 2.294,50: https://hkcn.rs-online.com/web/p/data-loggers/1450234 · ficha oficial: https://www.testo.com/en-US/testo-saveris-2-t2/p/0572-2032
- Competencia nacional en monitoreo IoT: https://iotmonitoreo.com.ar/ · https://www.solucionesfmk.com/monitoreo-remoto.php · https://blog.utelemetry.com/publication/monitoreo-cadena-de-frio/
- Valor hora de desarrollo en Argentina 2026 (USD 20-30 junior / 35-55 mid / 65-85 senior): https://teclab.edu.ar/tecnologia-y-desarrollo/cuanto-cobra-un-programador-en-argentina/ · https://www.sodi.com.ar/blog/cuanto-cuesta-software-a-medida-argentina
- Precio de novillo en pie $ 4.181/kg (INMAG, jul-2026): https://www.consignatarias.com.ar/mercado
- Dólar BNA vendedor $ 1.535 (3-sep-2026): https://www.cronista.com/finanzas-mercados/dolar-oficial-asi-abre-la-cotizacion-este-jueves-3-de-septiembre/
- Supabase Pro USD 25/mes: https://www.nocode.mba/articles/supabase-pricing
- Código de Conducta de Proveedores de Pan American Silver: https://panamericansilver.com/wp-content/uploads/2023/02/Supplier-Code-of-Conduct-ES-LA.pdf
- Cerro Moro (operación, Santa Cruz): https://panamericansilver.com/operations-2/silver-segment/cerro-moro/

## Anexo — Lo que quedó abierto (para Matías, antes de mandar)

1. **El número.** ¿USD 2.950 de desarrollo y USD 200/mes, o los movés? Recomiendo no bajarlos: para Panamerican son USD 4.350 iniciales y USD 200/mes, y a USD 65/mes se pierde plata (§4.4).
2. ~~¿Se cotiza en dólares o en pesos?~~ **RESUELTO el 3-sep-2026: se factura en dólares y se acepta el pago en pesos al tipo de cambio vendedor del BNA de la fecha de pago, propuesto y no impuesto. Sin validez de la cotización en el PDF del cliente (§4.7).**
3. **Monotributo vs. RI.** Preguntárselo al contador **antes** de emitir la cotización firme; si exigen RI, cambia el precio final por el IVA.
4. **¿El resumen de la Parte 1 va como texto de WhatsApp o como PDF de una carilla con la marca Termovigía?** Recomiendo PDF (`@diseno` lo maqueta en un día) más el mensaje de la Parte 7 como cuerpo. A un comité interno se le muestra un PDF, no un chat.
5. **La marca.** El folleto iría con Termovigía y la consulta INPI sigue pendiente. Para un cliente industrial no bloquea, pero conviene resolverlo antes de imprimir papelería.
6. **`ALCANCE_1WIRE.md` de `@muestreador` ya existe y está cruzado (§2.4).** Cambió la recomendación: **una base por reefer pasa a ser la opción recomendada** y las 3 bases quedan como alternativa condicionada a que cada rama dé <= 15 m. Si Andrés trae distancias cortas se recotiza y se ahorran USD 220 — pero la recomendación profesional sigue siendo una base por reefer, porque no depende de ninguna medición.
7. **Falta escribir en la orden de armado y en el runbook que a Cerro Moro va `entrega_scz`, no `firmware_modular`** (§2.4-bis). Es una línea, y evita que un equipo salga con el firmware que cruza las lecturas entre sondas.
