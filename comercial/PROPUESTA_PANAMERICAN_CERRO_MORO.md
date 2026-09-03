# PROPUESTA — Monitoreo de temperatura de 6 reefers, campamento Cerro Moro (Santa Cruz)

> @comercial · **v2, 2026-09-03** (rehecha con lo nuevo de Andrés: *"acá no pueden haber cables aéreos"* + *"pasale presupuesto por los 3 módulos, así cada uno controla dos reefers, y pensá cómo se lo puedo ofrecer a esa empresa. No le pongas el nombre"*) · **para revisión de Matías antes del vie 5-sep**
> **Matías decide el número final, siempre.** Todo monto de acá abajo es propuesta con la cuenta a la vista.
> Doctrina: `PLATA.md`. Base técnica: `C:\Proyectos\frioseguro\hardware\ALCANCE_1WIRE.md` (@muestreador) y `C:\Proyectos\frioseguro\entrega_scz\docs\ESTADO_HONESTO.md`.
> **El comprador NO es Pan American Silver:** es "una empresa" que Andrés todavía no identifica (contratista o servicio del campamento). Por eso la Parte 1 va **sin destinatario, sin logo ajeno y sin nombrar a Panamerican**. El archivo conserva el nombre por historial; el PDF que sale de acá se llama `PROPUESTA_REEFERS_CERRO_MORO.pdf`.

---

## PARTE 1 — El documento del cliente (lo que @diseno maqueta en PDF, 2 páginas A4)

> Copiar de acá hasta la línea de corte. Nada más. Escrito para que **lo presente alguien que no es vendedor** y se lea en dos minutos: qué es, qué hace, qué cuesta, cómo se paga.

**Termovigía — Monitoreo de temperatura de reefers**
**Propuesta: 6 reefers, campamento Cerro Moro (Santa Cruz)**

**Qué es.** Tres equipos que vigilan la temperatura de los seis reefers del campamento las 24 horas y avisan al celular cuando algo se sale de rango. Cada equipo atiende dos reefers contiguos, con dos sondas dentro de cada reefer. Hoy ya hay un equipo instalado y reportando desde el campamento: se puede ver en vivo en el celular antes de decidir nada.

**Qué hace.**
- Mide la temperatura de cada reefer todo el tiempo y la guarda en la nube (12 meses de historial).
- Avisa al celular de las personas que se definan cuando un reefer se sale del rango acordado por más tiempo del acordado.
- Avisa cuando una sonda se desconecta o cuando un equipo deja de reportar.
- Genera solo el **registro mensual de temperatura por reefer**, para tener el papel cuando alguien lo pide.
- Funciona con la red de internet que ya hay en el campamento: no hay que contratar nada más.

**Qué se instala.** Tres módulos, cada uno en un gabinete apto para intemperie con su fuente, dos sondas por reefer y un kit de repuesto que queda en el campamento. Cada módulo atiende **dos reefers contiguos**; el cable de sondas entre ambos **va canalizado por piso o bandeja, nunca aéreo, y no supera los 15 metros**. La canalización está incluida en el precio. El montaje lo hace personal del campamento con los equipos preconfigurados desde Bahía Blanca y guía por videollamada: por eso esta propuesta no tiene línea de instalación ni viáticos.

**Puesta en marcha y ajuste en sitio (15 semanas, por hitos).** Se cobra por hito aceptado, no por horas.

| Hito | Qué queda funcionando | Semana |
|---|---|---|
| 1 | Sondas dentro de los reefers, rangos definidos, primera alerta real recibida en el celular | 2 |
| 2 | Ningún dato ni aviso se pierde si se corta la red; aviso de equipo que deja de reportar; una semana entera sin falsas alarmas | 6 |
| 3 | Acceso seguro: cada equipo y cada usuario con su propia credencial | 11 |
| 4 | Actualizaciones de los equipos a distancia, sin tocarlos | 13 |
| 5 | Panel para la empresa (usuarios de solo lectura) e informe mensual descargable | 15 |

**Qué cuesta.**

| Concepto | USD |
|---|---|
| Módulo de monitoreo para 2 reefers (equipo, gabinete, fuente, 4 sondas, probado en banco) — 3 unidades × 720 | 2.160 |
| Kit de canalización por par de reefers (caño galvanizado, curvas, grampas, caja de paso, cable exterior) — 3 × 60 | 180 |
| Kit de repuestos en sitio (electrónica de reemplazo + 2 sondas) | 260 |
| Puesta en marcha y ajuste en sitio, 5 hitos | 1.500 |
| **Total equipos y puesta en marcha** | **4.100** |
| **Servicio mensual** (6 reefers: nube, alertas, soporte, reposición sin cargo, informe mensual) | **220 / mes** |

**Cómo se paga: tres formas, el mismo servicio.**

| | **A. Equipos + servicio mensual** | **B. Anual adelantado** | **C. Sin inversión inicial** |
|---|---|---|---|
| Para quién | Compra activos y paga el servicio mes a mes | Tiene presupuesto de inversión y no quiere 12 facturas | No puede comprar activos pero sí contratar un servicio |
| Pago inicial | USD 4.100 | USD 6.070 (equipos + 12 meses, con 10 % de descuento) | USD 0 |
| Mensual | USD 220 (los primeros 3 meses, mientras dura la puesta en marcha, se facturan al 50 %) | — el primer año; renovación anual USD 2.376 | USD 410, permanencia mínima 24 meses |
| Los equipos | Son del cliente | Son del cliente | Quedan en comodato; desde el mes 25 el servicio sigue a USD 220/mes |
| **Total a 12 meses** | **6.410** | **6.070** | **4.920** (y sigue) |
| **Total a 24 meses** | **9.050** | **8.446** | **9.840** |

Facturación en dólares estadounidenses. De abonarse en pesos, se toma el tipo de cambio vendedor del Banco de la Nación Argentina de la fecha de pago. *Referencia al 3-sep-2026 (BNA vendedor $ 1.535): USD 4.100 ≈ $ 6.293.500 · USD 220 ≈ $ 337.700 · USD 410 ≈ $ 629.350.*

**Incluido en el servicio mensual:** nube con 12 meses de historial · alertas por temperatura, sonda y equipo mudo · reposición sin cargo de cualquier equipo fallado, envío incluido · actualizaciones · soporte por WhatsApp y teléfono el mismo día hábil · informe mensual por reefer.

**Lo que hay que saber.** El sistema avisa; no garantiza la mercadería ni reemplaza la revisión del reefer. Sin energía en el equipo no mide: lo que avisa en ese caso es la nube, diciendo que dejó de reportar. Si alguno de los pares de reefers no está contiguo o el cable entre ambos supera los 15 metros, ese par se resuelve con dos módulos simples (uno por reefer) por **USD 220 más por par**; el servicio mensual no cambia.

*Contacto en sitio: Andrés Leiva Chavez · Contacto comercial: Matías Alegre · Termovigía · Bahía Blanca · 2920 59-1019 · alegrematias08@gmail.com*

— — — — — — — — — — corte: lo de abajo NO se manda — — — — — — — — — —

---

## PARTE 2 — Alcance (interno)

### 2.1 Qué hay hoy, verificado (3-sep-2026)

| Hecho | Evidencia |
|---|---|
| 1 equipo instalado en el campamento, `REEFER_01_SCZ`, firmware `firmware_revival` 2.6.21 | Puesto el 21-ago; reconectado por Andrés el 3-sep |
| Reportando cada ~5 s | Consulta a la base de Santa Cruz, 3-sep |
| **1 sola sonda y está FUERA del reefer** — mide ambiente | Andrés espera confirmación de Matías para meterlas |
| Elección de red abierta con internet real: probada 128 ciclos | `ESTADO_HONESTO.md` |
| **Sin contrato y sin un peso cobrado** | `PLATA.md` |
| **Restricción nueva del sitio: no puede haber cables aéreos** | Andrés, WhatsApp 3-sep 17:11 |
| **Pedido explícito: 3 módulos, 2 reefers cada uno, propuesta sin nombre de empresa** | Andrés, WhatsApp 3-sep 17:13 |

### 2.2 El escenario principal pasa a ser 3 módulos × 2 reefers — y por qué ahora es razonable

La v1 recomendaba una base por reefer porque el escenario de 3 bases dependía de una medición que nadie hizo, y lo que @muestreador descartó eran **tiradas de 60-150 m en estrella**. El dato nuevo cambia el cuadro: si no puede haber cable aéreo, el cable **va por piso o bandeja, canalizado**, y la única forma de que eso cierre en costo es que los dos reefers de cada par sean **contiguos** — pocos metros. Y pocos metros canalizados el bus 1-Wire los tolera de sobra.

**El X, con la cuenta de `ALCANCE_1WIRE.md`:** con CAT5, el límite físico por tiempo de subida a 3,3 V es **4k7 → 30 m · 2k2 → 64 m** (§1.4). El escenario (b) está rotulado *"riesgo bajo si cada rama ≤ 15 m"* (§3b). Un módulo entre dos reefers contiguos tiene una rama corta (2-3 m, el reefer donde está montado) y una rama al vecino: **con la rama larga ≤ 15 m el peso total del bus queda en ~20 m, tres veces por debajo del límite del 2k2.** De ahí la condición escrita al cliente: **"el cable entre ambos va canalizado y no supera los 15 metros"** — es el número de riesgo bajo con 2× de margen, no el límite.

**Lo que va de fábrica en los 3 módulos, sin discutirlo con el cliente:** pull-up **2k2** (no 4k7), CAT5 con DQ y GND en el mismo par, 100 nF + 10 µF al pie de la sonda lejana, y **la prueba de banco §6 de `ALCANCE_1WIRE.md` corrida con 15 m de cable real antes de despachar** (criterio: cero errores). Entre 15 y 25 m: 1 kΩ + prueba de banco a 25 m, y se recotiza. **Arriba de 25 m, o si el par no es contiguo: dos módulos simples para ese par** (la alternativa que quedó escrita en la Parte 1 como "+ USD 220 por par").

**Las tierras siguen siendo el riesgo dominante** (§2.6 de @muestreador) y no se pueden probar en Bahía. Mitigación que va en el runbook de montaje: VDD y GND por par propio y grueso (pares 3 y 4 en paralelo), un solo punto de unión de tierras, y **la primera semana del hito 1 sirve de prueba en sitio**: si el módulo compartido muestra CRC malos o lecturas de 85,00 °C, se parte en dos antes de seguir. Está cubierto por el "+ USD 220 por par" ya cotizado: no hay renegociación.

**Sigue vigente:** a Cerro Moro va la línea `entrega_scz` (`sondas.h`, identificación por ROM de 64 bits), **no** `firmware_modular` (lee por índice: con dos sondas, si cae una, la otra se reporta con el nombre equivocado). 4 sondas por módulo es exactamente `SONDAS_MAX 4`. Escribirlo en la orden de armado.

### 2.3 Canalización — "no aéreo" tiene precio

Supuesto por par: base montada en un reefer, cable al vecino contiguo por piso, **~10 m de caño + ~20 m de UTP exterior** (ida por el caño, más subidas y entradas a cada reefer).

| Material (por par) | Cantidad | Precio ML AR (3-sep-2026) | Subtotal |
|---|---|---|---|
| Caño galvanizado Daisa 3/4 liviano, tira 3 m | 4 | $ 11.637 c/u | $ 46.548 |
| Curvas, grampas, caja de paso estanca, prensacables, conectores | — | estimado | $ 15.000 |
| Cable UTP cat5e exterior 100 % cobre (rollo 100 m ≈ $ 40.000) | 20 m | $ 400/m | $ 8.000 |
| **Total por par** | | | **≈ $ 70.000 ≈ USD 46** |

Se cotiza **USD 60 por par** (flete a Santa Cruz y sobrante). Si el campamento ya tiene bandeja o caño disponible (pregunta a Andrés), el kit se reduce a cable + accesorios y el ahorro se traslada. Alternativa más barata si el tramo va embutido o bajo losa: corrugado 3/4 pesado ($ 13.500 el rollo de 25 m). Fuentes en el anexo.

### 2.4 Lo que se instala, y quién

Por módulo: gabinete estanco, fuente, prensacables, 4 sondas DS18B20 estancas con cable, kit de canalización. **Montaje: Andrés (o quien la empresa designe), con kit preconfigurado y probado en banco + videollamada.** Dos pasajes a Santa Cruz, alojamiento, inducción y 5 días de ingeniero rondan los $ 2.500.000, y Matías no puede viajar en octubre (parada de Dreyfus). Eso es lo que la propuesta **no** cobra.

### 2.5 Opcionales, después de la primera orden

Sensor de puerta por reefer (USD 20 + USD 7/mes) · sirena en el pasillo (USD 40 + USD 7/mes) · sonda adicional (USD 40 + USD 5/mes). Se ofrecen cuando las sondas estén andando, no antes.

---

## PARTE 3 — La forma de cobrar (lo central de la v2)

### 3.1 Por qué desaparece el renglón "Desarrollo USD 2.950"

Matías: *"pensá si realmente el plan de cómo cobrarlo no sería de otra forma"*. Tiene razón. Para una minera con área de compras, "desarrollo y puesta en servicio industrial" era una partida presupuestaria legible. Para **una empresa que compra 3 equipos** (contratista de catering, servicio de campamento) ese renglón se lee como *"me cobrás por inventar el producto"* — y es el renglón más grande de la hoja. El trabajo no desaparece ni se regala: **se reparte donde el comprador espera verlo**.

| v1 (para una minera) | v2 (para una empresa que compra 3 equipos) |
|---|---|
| Desarrollo y puesta en servicio industrial — USD 2.950 | **Puesta en marcha y ajuste en sitio, 5 hitos — USD 1.500** (lo específico de este sitio: sondas, rangos, pruebas de campo, panel, informe) |
| Equipos, repuestos y materiales — USD 1.180 (3 bases) | **Módulo para 2 reefers — USD 720 × 3 = 2.160** (absorbe la parte de plataforma del desarrollo: seguridad, buffer offline, vigía, OTA — que es lo que hace que el equipo valga 720 y no 120) |
| — | **Canalización — USD 180** (nuevo, por "no aéreo") |
| — | **Repuestos — USD 260** |
| **Inicial USD 4.130** | **Inicial USD 4.100** |

Mismo valor, otra lectura: el comprador ve **tres equipos a USD 720** (un logger testo Saveris 2 sale USD 318 y no hace nada de esto) más una puesta en marcha por hitos. Nada de "horas".

**Cómo se factura la puesta en marcha (interno, no va al cliente):** 40 % a la orden de compra (USD 600), 30 % al aceptar el hito 2 (USD 450), 30 % al aceptar el hito 5 (USD 450). Los módulos, 100 % contra entrega. Qué se hace en cada hito y con qué fecha: Parte 5.

### 3.2 Servicio mensual: qué cuesta servir y qué se cobra

Costo directo: Supabase Pro USD 25 + reposición amortizada USD 10 + soporte 2 h USD 50 + informe 1 h USD 25 = **USD 110/mes**. Tarifa: **USD 100 de sitio + USD 20 por reefer, 6 reefers = USD 220/mes** (Andrés pidió 3 módulos de 2 = 6 reefers; si arrancan con 5 activos son USD 200 y el sexto entra por USD 20 cuando vuelva). Margen bruto USD 110/mes.

**El escalón de la puesta en marcha se conserva en A** (los primeros 3 meses al 50 % = USD 110, el costo directo): es lo que hace honesta la propuesta — se paga el valor entregado — y ahora está dicho en una línea, sin drama. En B y C no aplica: B ya lleva descuento y C ya está financiando equipos.

### 3.3 Las tres formas de pagar lo mismo

**A. Equipos + servicio mensual.** USD 4.100 + 3 × 110 + 9 × 220 = **USD 6.410 el primer año**; USD 2.640/año después. **24 meses: USD 9.050.** Es la estructura base; las otras dos se calculan contra esta.

**B. Anual adelantado, 10 % de descuento.** Lista de 12 meses a tarifa plena: 4.100 + 2.640 = USD 6.740, con 10 % queda en **USD 6.070** en un solo pago (6.066 redondeado a número comercial). Renovación: USD 2.640 × 0,9 = **USD 2.376** por año adelantado. **24 meses: USD 8.446.** Por qué 10 % y no 8: el descuento tiene que valer más que el escalón de A (que ya le deja USD 330 al que paga mes a mes), si no B no tiene sentido; y lo que compra el 10 % (USD 670) es concreto: **cero riesgo de cobranza durante 12 meses con un contratista que probablemente pague a 60-90 días, una factura en lugar de doce, y caja hoy para armar la segunda tanda de equipos.** El costo de financiar 12 cuotas de 220 a 60 días es menor que eso, pero el riesgo de que un contratista de campamento deje de pagar en el mes 7 no lo es. Es un descuento que se paga solo.

**C. Sin inversión inicial, permanencia 24 meses, equipos en comodato.** Piso: 24 × c tiene que ser al menos 9.050, o sea c de USD 377 como mínimo. **Propuesto USD 410/mes: 24 meses = USD 9.840**, un 8,7 % sobre A. Por qué no el piso de 377-390: en C **nosotros ponemos los USD 4.100 de equipos y puesta en marcha y los cobramos a lo largo de dos años** — a un contratista, a 1.500 km, sin posibilidad práctica de retirar los equipos si deja de pagar. El 8,7 % es el costo de ese financiamiento más el riesgo del activo; a 390 sería un regalo con permanencia. Desde el mes 25 pasa a USD 220 (los equipos ya se pagaron). Si Matías prefiere redondear a USD 400: 24 meses = 9.600, +6 %. No bajar de 390.

**Riesgo de C, escrito:** es la opción que más plata nuestra pone en juego. Si el cliente corta en el mes 8, cobramos 3.280 contra 4.100 invertidos más el servicio prestado, y la cláusula de permanencia es exigible pero difícil de cobrar a distancia. Mitigaciones para el contrato: **primer y último mes a la firma**, corte del servicio (no del equipo) por mora a 30 días, saldo de permanencia exigible. **C solo se firma con contrato; sin contrato, C no existe.**

| | A | B | C |
|---|---|---|---|
| Inicial | 4.100 | 6.070 | 0 |
| 12 meses | 6.410 | 6.070 | 4.920 |
| 24 meses | 9.050 | 8.446 | 9.840 |
| Riesgo nuestro | bajo | nulo | alto (financiamos 4.100) |
| Recomendado para | quien compra activos | quien tiene presupuesto de inversión | quien solo puede contratar servicio |

Los tres caminos convergen: **B es el más barato porque paga antes, C el más caro porque no paga nada al principio, A está en el medio.** Es la lectura que tiene que tener alguien de compras en 30 segundos.

### 3.4 Alternativa 5-6 módulos (si algún par no es contiguo)

Módulo simple para 1 reefer (2 sondas) **USD 500**; sin kit de canalización (tiradas de 2-5 m). Reemplazar un módulo doble por dos simples: 2 × 500 - 720 - 60 = **+ USD 220 por par**. Si ningún par es contiguo: 6 × 500 + 260 + 1.500 = USD 4.760 inicial (+660). El abono no cambia (es por reefer). Es la regla de la Parte 1 y evita recotizar.

### 3.5 Moneda, validez, facturación

Sin cambios: **facturación en USD, pago en pesos al BNA vendedor de la fecha de pago, sin validez en el PDF.** Nota interna: revisar precios si pasan más de 6 meses desde el 3-sep. Lo que hay que averiguar antes de la cotización firme **cambió de destinatario**: ya no es el sistema de compras de PAAS sino el de la empresa que Andrés identifique — monotributo vs. RI, plazo de pago, si acepta la cláusula de moneda, quién firma. Se pregunta cuando aparezca el nombre.

---

## PARTE 4 — Números de respaldo

### 4.1 Módulo doble USD 720 — cómo cierra

| | USD |
|---|---|
| Materiales base (ESP32, fuente, gabinete estanco, prensacables, pull-up 2k2, TVS, capacitores) | 45 |
| 4 sondas DS18B20 estancas con cable | 60 |
| Armado, prueba de banco §6 con 15 m documentada, envío a Santa Cruz, garantía de reposición | 120 |
| Parte de plataforma del desarrollo (80 h al 50 % = USD 1.000, repartido en 3 módulos) | 333 |
| Margen | 162 |
| **Precio** | **720** |

Con 3 módulos, la parte de plataforma recupera los mismos USD 1.000 que la v1 cobraba como "desarrollo al 50 %". Nada se regaló; cambió de renglón.

### 4.2 Puesta en marcha USD 1.500 — 60 h de lo específico del sitio

Sondas, rangos y umbrales por reefer (12 h) · registro exportable con código de verificación (16 h) · panel multi-equipo y usuarios de lectura (12 h) · puesta en marcha remota, pruebas de campo con Andrés, runbook y capacitación (16 h) · salud de bus + histéresis de 3 barridos (4 h). A USD 25/h = USD 1.500. La v1 tenía 80 h a USD 2.000 en este bloque; las 20 h de diferencia son la parte de "puesta en servicio industrial" que ahora está dentro del precio del módulo (4.1).

### 4.3 Servicio y contra una pérdida

Sin cambios de la v1: costo directo USD 110/mes; una pérdida de 3 t valuada al precio de novillo en pie ($ 4.181/kg, INMAG jul-2026) son $ 12,5 M, unos **3 años de servicio**. testo Saveris 2-T2: USD 318 por unidad, 12 unidades = USD 3.816 antes de importación y sin nube, y se configura con una red WiFi y una clave — que es lo que este sitio no tiene.

---

## PARTE 5 — Puesta en marcha: qué es cada hito por dentro (no se esconde, se traduce)

Es el plan de endurecimiento de la auditoría del 26-ago, con nombre de cliente. Octubre es Dreyfus: por eso los hitos pesados caen después.

| Hito (cliente) | Etapa interna | Desde | Hasta | Cómo se acepta |
|---|---|---|---|---|
| 1 — Sondas adentro, rangos, primera alerta real | E0 | lun 8-sep | **vie 19-sep** | Captura de la alerta en el celular + registro en nube. **Además: primera semana con módulo compartido = prueba de tierras en sitio** |
| 2 — Nada se pierde, nada sobra | E1: buffer offline, alertas encoladas, alerta de sonda caída que llega, vigía de equipo mudo, discriminador de bus + histéresis | lun 22-sep | **vie 10-oct** | Desenchufar y que llegue la alarma; cortar red 20 min sin perder lecturas; una semana sin falsas alarmas |
| 3 — Acceso seguro | E2: RLS cerrada, credencial por equipo, secretos fuera del binario, revocar claves quemadas | lun 13-oct | **vie 14-nov** | Con la clave vieja no se escribe; el equipo sigue reportando |
| 4 — Actualización a distancia | E3: OTA con manifiesto inmutable | lun 17-nov | **vie 28-nov** | Tres actualizaciones seguidas por aire al primer intento |
| 5 — Panel e informe | E4: usuarios de lectura, vista de 6 reefers, exportación con código, informe mensual automático | lun 1-dic | **vie 19-dic** | Un usuario de la empresa entra solo y baja el informe |

Lo que hoy está roto y cada hito arregla (llave maestra en el binario, datos perdidos sin red, umbral en 50 °C, equipo muerto que no avisa, OTA que entra 1 de 4) está en `AUDITORIA_HALLAZGOS.md`; no cambió.

---

## PARTE 6 — Qué necesitamos para cerrar

**De Andrés, esta semana (lo único que bloquea el número):**
1. **Metros entre los dos reefers de cada par, por donde iría el cable** (piso, no línea recta). Y cuáles son los pares.
2. **¿Hay canalización existente** (caño, bandeja, canaleta) entre reefers, o la ponemos nosotros?
3. Rango de cada reefer y cuánto tiempo fuera de rango es problema.
4. Teléfonos que reciben las alertas.

**De la empresa, cuando tenga nombre:** quién firma, cómo factura (monotributo/RI, plazo), si acepta la cláusula de moneda, cuál de las tres formas prefiere, y confirmación de que el montaje lo hace personal del campamento (sin personal nuestro en sitio no corresponde ART ni legajo de contratista).

---

## PARTE 7 — Para Andrés (aparte del PDF)

### 7.1 WhatsApp de respuesta (lo manda Matías)

```
Dale Andrés, van los 3 módulos, cada uno controla dos reefers, y con cable
canalizado por el piso, nada aéreo.

La propuesta te la armo sin nombre de empresa, así se la ofrecés a quien
corresponda. Va en 2 hojas: qué es, qué hace, qué cuesta y tres formas de
pagarlo (compran los equipos y pagan mensual, pagan el año de una, o no
compran nada y pagan solo un servicio mensual por dos años).

Lo único que necesito de tu lado para cerrar el número: entre los dos
reefers de cada par, ¿cuántos metros hay por donde iría el cable? ¿Y hay
algún caño, bandeja o canaleta ya hecha entre ellos, o lo canalizamos
nosotros? Con eso te mando el PDF.
```

### 7.2 Guion de 5 líneas para que la presente él

1. **Arrancá por el problema, no por el producto:** "un reefer que se corta un fin de semana es la comida de todo el campamento, y hoy nadie se entera hasta que abren la puerta."
2. **Mostrá lo que ya anda:** abrí el panel en el celular y mostrá la temperatura de ahora del equipo instalado. Si podés, sacá una sonda al aire un minuto y que vean subir la curva. Eso convence más que el PDF.
3. **Decilo en una frase:** "son tres cajas, cada una vigila dos reefers, avisa al celular y arma el registro mensual solo."
4. **Dejá el PDF y señalá las tres formas de pagar:** "eligen ellos según cómo compren: equipos más servicio mensual, el año pagado de una, o cero inversión y solo un servicio mensual por dos años."
5. **Lo que NO prometés:** que garantiza la mercadería (avisa, no garantiza) · que avisa el corte de luz (avisa que el equipo dejó de reportar) · que está terminado (hay una puesta en marcha de 15 semanas por hitos, y está en el precio) · fechas o precios distintos a los del PDF. Cualquier pregunta técnica o de números: "eso lo contesta Matías, lo llamamos ahora."

---

## PARTE 8 — La relación con Andrés, pensada de nuevo (para que Matías decida)

**Lo que cambió:** en la v1 Andrés era el contacto en sitio de un cliente (Panamerican) y la regla era simple: **ningún pago ni beneficio ligado a que su empleador compre.** Ahora es él quien **ofrece y presenta** la propuesta a una tercera empresa que él elige. Está haciendo de referidor, de hecho.

**Lo que sigue vigente, sin discusión:** si el comprador termina siendo Pan American Silver, o una contratista que opera bajo su Código de Conducta de Proveedores (que alcanza a proveedores **y a sus subcontratistas**), **no hay comisión ni reconocimiento material.** Y hay que ser honesto con la probabilidad: **cualquier empresa que opere dentro del campamento de Cerro Moro está, casi seguro, bajo ese código.** O sea: en este negocio en particular, la respuesta más probable es "no".

**El conflicto de interés, escrito:** Andrés trabaja adentro (no sabemos todavía si es empleado de PAAS o de una contratista — **hay que preguntarlo**), elige a quién ofrecerle el sistema y lo presenta con la credibilidad de su puesto. Si cobra por eso, pasa de "el que trajo un proveedor bueno" a "el que le vendió algo a la empresa de al lado y se llevó una parte", y eso lo expone a él ante su empleador y a nosotros ante el cliente el día que alguien pregunte. **El costo de un reconocimiento mal puesto sigue siendo mayor que el negocio.**

**Las opciones, para Matías:**

| Opción | Qué es | A favor | En contra |
|---|---|---|---|
| **1. Nada material, todo el reconocimiento no monetario** (status quo) | Agradecer por escrito, darle el acceso y la hoja de una carilla para que quede bien adentro, nombrarlo como contacto en sitio, contarle el caso como logro suyo | Cero riesgo. Es lo que él pidió (*"la gente de acá no lo vio"*): quedar bien, no cobrar | Si el negocio crece por él y no recibe nada, el empuje puede enfriarse |
| **2. Referidor formal solo para leads AJENOS al campamento** (Bahía, Venado Tuerto, futuros) | Esquema escrito: reconocimiento único equivalente a 1 mes de abono del cliente referido, pagado después del 3er abono cobrado; **excluye explícitamente** a PAAS, sus contratistas y cualquier empresa de Cerro Moro; condicionado a que su empleador lo permita | Es honesto, separa los mundos, y **ya tiene un caso real: Venado Tuerto lo trajo él** | Hay que escribirlo y preguntarle si su empleador tiene política de actividades externas |
| **3. Reconocimiento en especie, fuera del negocio** | Un equipo Termovigía para uso propio, o capacitación, sin vínculo con ninguna compra | Barato, tangible | Si se da mientras Cerro Moro está en discusión, se lee igual que una comisión. Solo después de cerrado y solo si el comprador es ajeno |

**Mi recomendación honesta:** 1 ahora, 2 por escrito cuando Venado Tuerto avance, y **preguntarle a Andrés para quién trabaja y si su empresa tiene política de actividades externas** antes de ofrecerle cualquier cosa. La 3, nunca durante la negociación de Cerro Moro. **No decido: decide Matías.**

---

## Anexo — Fuentes consultadas (3-sep-2026)

- Alcance del bus, pull-ups, tierras, escenarios: `C:\Proyectos\frioseguro\hardware\ALCANCE_1WIRE.md` (@muestreador).
- Estado real y auditoría: `C:\Proyectos\frioseguro\entrega_scz\docs\ESTADO_HONESTO.md` · `AUDITORIA_HALLAZGOS.md`.
- Techo de sondas por base y firmware por ROM: `entrega_scz/firmware/sondas.h` (`SONDAS_MAX 4`).
- Costo de materiales: `C:\Proyectos\frioseguro\docs\LISTA_MATERIALES.md` (~USD 30-45 por emisor).
- Contrato base: `MATI-HQ\comercial\CONTRATO_TERMOVIGIA_v4.md`.
- **Canalización (ML AR, 3-sep-2026):** caño galvanizado Daisa 3/4 liviano tira 3 m $ 11.637 — https://www.electricidadarevonline.com.ar/MLA-1439417798-cano-galvanizado-daisa-34-liviano-x-tira-de-3-metros-_JM · pesado $ 18.388 — https://electrodorrego.mercadoshops.com.ar/MLA-1116414163-cano-galvanizado-daisa-34-pesado-x-tira-de-3-metros-_JM · corrugado 3/4 pesado 25 m $ 13.500 — https://electrooestesanjusto.mercadoshops.com.ar/MLA-840435552-cano-corrugado-34-gris-pesado-losa-x-rollo-25mt-ha-ignifugo-_JM (Genrod $ 31.644 — https://www.luzytecnologia.com.ar/MLA-827625739-rollo-x-25mt-cano-corrugado-34-ignifugo-gris-pesado-p-losa-_JM) · UTP cat5e exterior 100 % cobre 100 m desde ~$ 40.000 — https://articulo.mercadolibre.com.ar/MLA-934596791-cable-utp-rollo-100mts-100-cobre-exterior-cat5e-4-pares-_JM · cablecanal 40x40 $ 5.000-18.000 — https://listado.mercadolibre.com.ar/cable-canal-40x40
- 1-Wire: Maxim/Analog AN148 — https://www.analog.com/media/en/technical-documentation/tech-articles/guidelines-for-reliable-long-line-1wire-networks.pdf
- testo Saveris 2-T2 USD 318: https://www.ebay.com/itm/365602217221
- Novillo en pie $ 4.181/kg (INMAG jul-2026): https://www.consignatarias.com.ar/mercado
- Dólar BNA vendedor $ 1.535 (3-sep-2026): https://www.cronista.com/finanzas-mercados/dolar-oficial-asi-abre-la-cotizacion-este-jueves-3-de-septiembre/
- Supabase Pro USD 25/mes: https://www.nocode.mba/articles/supabase-pricing
- Código de Conducta de Proveedores de Pan American Silver (alcanza a subcontratistas): https://panamericansilver.com/wp-content/uploads/2023/02/Supplier-Code-of-Conduct-ES-LA.pdf

## Anexo — Lo que quedó abierto (para Matías, antes de mandar)

1. **Los números:** módulo USD 720 · puesta en marcha USD 1.500 · abono USD 220 · B con 10 % · **C a USD 410** (piso 390). ¿Van?
2. **¿6 reefers o 5?** Andrés pidió 3 módulos de 2. Se cotiza 6; si arrancan con 5, USD 200/mes.
3. **C solo con contrato** (permanencia, primer y último mes a la firma). ¿Se ofrece igual o se guarda hasta tener el contrato validado por el contador?
4. **Andrés:** opción 1, 2 o 3 de la Parte 8, y preguntarle para quién trabaja.
5. **PDF:** @diseno maqueta la Parte 1 en 2 páginas A4, marca Termovigía, sin logo ajeno, sin "Para:", sin validez. Nombre del archivo `PROPUESTA_REEFERS_CERRO_MORO.pdf`.
6. Monotributo vs. RI: se pregunta cuando la empresa tenga nombre.
7. Sigue pendiente escribir en la orden de armado que va `entrega_scz`, con pull-up 2k2 y la prueba de banco a 15 m.
