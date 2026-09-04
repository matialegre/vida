# PROPUESTA — Monitoreo de temperatura de los reefers del campamento Cerro Moro (Santa Cruz)

> @comercial · **v7.0, 2026-09-04** · **UN SOLO presupuesto: 3 módulos, TODOS DOBLES — 1 estanco de exterior + 2 de interior**
> **Configuración FINAL, cerrada por Andrés el 4-sep (*"los de afuera pueden ir con un solo módulo, están juntos"*) y confirmada por Matías:**
> - **Los 2 reefers de la intemperie están JUNTOS** → van con **UN solo módulo doble**, en **caja estanca IP65 apta para exterior** (Matías ya mandó una al sitio).
> - **4 reefers están adentro, bajo techo** → **2 módulos dobles**, uno por par, en gabinete de interior.
> - **Total: 3 módulos, los tres dobles.** Repuesto: **1 módulo doble**, sirve para cualquiera de los tres.
> - De los 4 reefers de adentro, **uno está fuera de servicio**: hoy son **5 reefers activos** y **el módulo del par donde está ese reefer atiende uno solo, con su canal libre esperando al sexto**. Cuando vuelva, **no hay que comprar equipo**.
> - **Por reefer, siempre igual: 3 sondas + 1 sensor de puerta + 1 señal de defrost.** Por módulo (los tres son dobles): **6 sondas, 2 puertas, 2 defrost**.
> **Precio recalculado hacia abajo, sin acomodar nada (decisión del Director):** menos equipos = menos plata. **Inicial USD 4.115** contra los 4.600 de la v6.1. El abono **no** se toca: **USD 100 por reefer por mes = 500/mes**, sin escalón, completo desde el primer mes · el **tendido de cable entre reefers no se cotiza** — a cargo del cliente, y ahora aplica a **los tres pares** · **en el documento del cliente no se dice el material del gabinete ni se menciona impresión 3D**.
> **Cambio del 4-sep (el cable):** el cable **no** lo manda Matías desde acá; el documento del cliente ya no lleva spec de cable ni promesa de "cable incluido" — eso lo resuelven en el sitio. En su lugar hay una sola nota al pie de la tabla de precios: *"No incluye cable ni tendido entre reefers."* **Ahora esa nota cubre también al par de afuera** (interno: ese tramo tiene que ser cable apto exterior; en el documento del cliente no va nada más que la nota, decisión de Matías).
> **Se mantiene de la v6.1:** la firma con UTN/GIMAP/Montagne, los hitos relativos y la propuesta sin cláusulas condicionales.
> **Se mantiene de la v5.2:** sin destinatario, sin nombrar a Panamerican, hitos en semanas desde "aceptación + anticipo", 50/50, formas A y B, sin validez, USD con pago en pesos al BNA de la fecha de pago.
> **Matías decide el número final, siempre.** Todo monto de acá abajo es propuesta con la cuenta a la vista.
> Doctrina: `PLATA.md`. Base técnica: `ALCANCE_1WIRE.md` (@muestreador), `BOM_KIT_V1.md` rev B (@hardware, 2-sep) y **`BOM_CERRO_MORO.md` (@hardware, 4-sep — de ahí salen los precios reales de gabinete)**, `ESTADO_HONESTO.md`, firmware `firmware_revival` leído el 3-sep y **auditoría del firmware de módulo doble `VERIFICACION_V3.1_2026-09-04.md` (APTO CON CORRECCIONES)**.
> **El comprador NO es Pan American Silver:** es "una empresa" que Andrés todavía no identifica. El documento del cliente va **sin destinatario, sin logo ajeno y sin nombrar a Panamerican**. El archivo conserva el nombre por historial.

## Qué cambió en esta versión

**1. Los dos de afuera están juntos, así que comparten módulo.** Andrés lo cerró el 4-sep: *"los de afuera pueden ir con un solo módulo, están juntos"*. Con eso se cae el único motivo que teníamos para el módulo simple — no lo poníamos por gusto, lo poníamos porque suponíamos dos contenedores separados y un cable a cielo abierto entre ellos. Están pegados. **Configuración final: 3 módulos, los tres dobles — 1 estanco de exterior para el par de afuera, 2 de interior para los dos pares de adentro.**

**2. El precio baja porque hay menos equipos, y se dice así.** **1 doble de exterior a USD 765** + **2 dobles de interior a USD 750** = **USD 2.265 en equipos**, más repuesto **400** y puesta en marcha **1.450** = **USD 4.115**. Era 4.600 en la v6.1: **−USD 485, un 10,5 % menos**. **No se tocó ningún unitario para sostener el 4.600.** Lo que el cliente tiene que ver es exactamente esto: un equipo menos, una puesta en marcha más corta, un precio más bajo. Eso es lo que compra credibilidad para el abono, que es donde está la plata de verdad.

**3. Los USD 765 del de exterior son 750 + la caja, y nada más.** El doble de interior queda en 750, igual que en la v6.1. El de exterior lleva la misma electrónica, las mismas 6 sondas y los mismos 2 reed; lo único que cambia es el gabinete: **Roker PRG357 IP65 200×200×155 a $ 44.419** contra **$ 21.203** de la caja de interior (`BOM_CERRO_MORO.md` de @hardware, precios verificados el 4-sep). Diferencia **$ 23.216 ≈ USD 15** → precio **765**. **El margen absoluto queda igual en los dos módulos (USD 174 cada uno):** no se usó la caja cara de excusa para meter margen extra.

**4. La puesta en marcha baja de 1.500 a 1.450, y baja poco a propósito.** Se cae **un** módulo de alta remota, credencial, OTA verificada y prueba de puertas y defrost: **2 horas menos, de 60 a 58 h a USD 25**. **El software es el mismo trabajo**: la segunda puerta, el segundo defrost con silenciado por reefer y `SONDAS_MAX` a 8 se escriben una sola vez, se usen en dos módulos o en tres. Bajar más sería regalar horas que igual hay que trabajar.

**5. El abono NO se toca: USD 100 por reefer por mes = 500/mes.** El abono se cobra por reefer vigilado, no por caja instalada (§3.4). Que ahora haya 3 módulos en lugar de 4 no cambia lo que se vigila y se registra: **5 reefers**. Cuando entre el sexto, **600/mes**.

**6. El riesgo se movió de lugar — dos cosas empeoraron y dos mejoraron.** Está completo en §2.5:
- **(−) Ahora son 3 tiradas de cable y una es a la intemperie** (la del par de afuera), no 2 bajo techo. Están juntos, así que debería ser la más corta de las tres, pero es la más expuesta. **Interno: ese tramo tiene que ser cable apto exterior**; al cliente solo le va la nota al pie.
- **(−) El firmware de módulo doble pasa a ser crítico para los TRES módulos.** En la v6.1 había colchón: los 2 simples corrían el firmware que ya anda, y si el doble se atrasaba arrancaba igual la mitad del sistema. **Ese colchón ya no existe: sin firmware doble no reporta nadie.** §2.5 punto 3.
- **(+) Un punto de red menos** (3 en vez de 4) y **un equipo menos que comprar, armar, probar y despachar**.
- **(+) Cero cable entre contenedores desaparece como argumento, pero aparece uno mejor:** el par de afuera comparte módulo porque están pegados, y eso lo dijo el sitio.

**7. Tres sondas por reefer, no cuatro** (decisión de Matías). 15 sondas en servicio. El argumento de por qué más de una **sigue valiendo entero con tres**: peor punto, redundancia ante falla y verificación cruzada (tres es el mínimo que permite saber **cuál** se desvió).

**8. El sexto reefer sigue siendo un canal libre, no una promesa.** Está adentro, está fuera de servicio, y su módulo doble **ya va instalado**. Cuando vuelva: **USD 260 de sondas, puerta y defrost, +USD 100/mes**. Sin equipo nuevo, sin renegociar nada.

**Sigue eliminada la opción C** de la v2 ("sin inversión inicial", comodato con permanencia 24 meses): *"el de la inversión inicial no lo ofrecería"* (Matías). Quedan **A** (equipos + servicio mensual) y **B** (anual adelantado).

---

## PARTE 1 — Documento del cliente (@diseno maqueta 2 páginas A4)

> Copiar de acá hasta la línea de corte. Nada más. Escrito para que **lo presente alguien que no es vendedor** y se lea en dos minutos.

**Termovigía — Monitoreo de temperatura de reefers**
**Campamento Cerro Moro (Santa Cruz) — 5 reefers en servicio**

**Qué es.** Un sistema que mide la temperatura de cada reefer las 24 horas y avisa al celular cuando algo se sale de rango. Hoy ya hay un equipo instalado y reportando desde el campamento: se puede ver en vivo en el celular antes de decidir nada. **Mientras se evalúa esta propuesta ese equipo sigue midiendo y reportando**, y el panel se puede abrir en cualquier momento: los resultados se muestran durante el proceso, no después.

**Armado según cómo está el sitio.**
- **Los 2 reefers que están a la intemperie están juntos**, así que van con **un solo módulo**, en **gabinete estanco IP65 apto para exterior**: frío, viento y lluvia son la condición normal de trabajo de ese equipo, no una excepción.
- **Los 4 reefers que están bajo techo se cubren con 2 módulos**, uno cada par, aprovechando que la tirada de cable entre ellos es corta y está protegida.
- Total: **3 módulos** para los 6 reefers, y **por cada reefer siempre lo mismo: 3 sondas, 1 sensor de puerta y 1 señal de defrost**.

**Qué hace.**
- Mide la temperatura de cada reefer todo el tiempo, con **3 sondas por reefer**, y la guarda en la nube (12 meses de historial).
- Avisa al celular de las personas que se definan cuando un reefer se sale del rango acordado por más tiempo del acordado.
- Avisa si **queda la puerta abierta** más de los minutos que se definan (sensor magnético en cada reefer).
- Avisa cuando una sonda se desconecta o cuando un módulo deja de reportar.
- **No molesta durante el descongelamiento:** toma la señal de defrost de cada reefer y calla las alarmas **de ese reefer** mientras dura el ciclo, para que nadie aprenda a ignorar los avisos.
- Puede **accionar una sirena o baliza**: cada módulo trae 2 salidas a relé libres para eso.
- Genera solo el **registro mensual de temperatura por reefer**, para tener el papel cuando alguien lo pide.
- Funciona con la red de internet que ya hay en el campamento: no hay que contratar nada más.

**Por qué 3 sondas por reefer y no una.** Es la diferencia entre una instalación seria y un termómetro con WiFi.
1. **Un reefer no tiene "una" temperatura.** Cerca de la puerta, cerca del evaporador, arriba y abajo puede haber varios grados de diferencia. Con una sonda se mide un punto y se supone el resto; con tres se mide **el peor punto**, que es el que decide si la carga se arruinó. En una auditoría lo que vale es el peor punto, no el promedio.
2. **Si una sonda falla, el reefer sigue vigilado.** En un sistema cuyo trabajo es avisar, quedarse ciego es la peor falla posible: con una sola sonda cualquier problema deja el reefer sin vigilancia hasta que alguien viaje 1.500 km. Con tres, se pierde una y quedan dos midiendo.
3. **Las sondas se controlan entre sí.** Tres es el mínimo que permite saber **cuál** se desvió: si una se aparta de las otras dos, se detecta y se avisa. Con una sola sonda, una deriva de 2 o 3 °C es invisible: el registro parece perfecto y está mintiendo. *(Se entrega en el hito 2.)*
4. **Se calibran las tres contra la misma referencia** (baño de hielo) y las diferencias quedan registradas. Eso es lo que convierte el registro en algo defendible ante un auditor.

**Qué se instala.** **Un módulo de exterior** (gabinete estanco IP65, para los dos reefers que están juntos a la intemperie) y **dos módulos de interior** (uno cada par de los que están bajo techo). Los tres son módulos dobles: cada uno atiende dos reefers. Cada módulo trae su fuente y **2 salidas a relé**, y por cada reefer van **3 sondas, 1 sensor magnético de puerta y 1 entrada de señal de defrost**. Se suma un **kit de repuesto que queda en el campamento**. El montaje lo hace personal del campamento con los equipos preconfigurados desde Bahía Blanca y guía por videollamada: por eso esta propuesta no tiene línea de instalación ni viáticos.

**Cada módulo se prueba con el cable real antes de viajar.** Los equipos no salen de una línea de montaje: **se arman y se verifican uno por uno en banco de prueba** —todas las sondas leyendo, las puertas, las señales de defrost y las salidas de alarma— y **cada módulo se prueba con 25 metros de cable puestos**, la distancia real del sitio. Para un lote que va a quedar a 1.500 km del proveedor, esa verificación es la diferencia entre un equipo que llega andando y uno que hay que diagnosticar por teléfono.

**El sexto reefer.** De los 4 reefers de adentro, uno está hoy fuera de servicio, **y el módulo de su par ya va instalado con el canal libre esperándolo**. Cuando vuelva a funcionar **no hay que comprar ningún equipo**: se le suman sus 3 sondas, su sensor de puerta y su entrada de defrost por **USD 260**, y el servicio mensual pasa de USD 500 a USD 600. Queda dicho acá para no tener que renegociar nada el día que pase.

**Puesta en marcha y ajuste en sitio (15 semanas, por hitos).** Los hitos son compromiso de entrega con plazo; no se facturan aparte, están incluidos en el precio. **Los plazos se cuentan desde el inicio, y el inicio es la aceptación de esta propuesta con su anticipo.**

| Hito | Qué queda funcionando | Plazo |
|---|---|---|
| 1 | El equipo que ya está instalado, con sus 3 sondas dentro del reefer, calibradas contra una misma referencia, rangos definidos y primera alerta real recibida en el celular | a las 2 semanas de iniciado |
| 2 | Los 3 módulos montados y los 5 reefers reportando; ningún dato ni aviso se pierde si se corta la red; aviso de módulo que deja de reportar; **aviso de sonda que se desvía de las otras del mismo reefer**; puertas y defrost validados en campo; una semana entera sin falsas alarmas | a las 5 semanas |
| 3 | Acceso seguro: cada módulo y cada usuario con su propia credencial | a las 10 semanas |
| 4 | Actualizaciones de los equipos a distancia, sin tocarlos | a las 12 semanas |
| 5 | Panel para la empresa (usuarios de solo lectura), accionamiento de las salidas de alarma desde el panel e informe mensual descargable | a las 15 semanas |

**Qué cuesta.**

| Concepto | USD |
|---|---|
| Módulo de exterior para los dos reefers que están juntos a la intemperie (gabinete estanco IP65 apto para exterior, fuente, 2 salidas a relé, y por cada reefer 3 sondas + sensor de puerta + entrada de defrost; probado en banco con 25 m de cable) — 1 × 765 | 765 |
| Módulo para dos reefers bajo techo (gabinete, fuente, 2 salidas a relé, y por cada reefer 3 sondas + sensor de puerta + entrada de defrost; probado en banco con 25 m de cable) — 2 × 750 | 1.500 |
| Kit de repuestos en sitio (1 módulo completo armado y probado, que puede reemplazar a cualquiera de los tres, + 3 sondas + 1 sensor de puerta) | 400 |
| Puesta en marcha y ajuste en sitio, 5 hitos | 1.450 |
| **Total equipos y puesta en marcha** | **4.115** |
| **Servicio mensual** — **USD 100 por reefer por mes**, 5 reefers en servicio (nube, alertas, soporte, reposición sin cargo, informe mensual) | **500 / mes** |

*No incluye cable ni tendido entre reefers.*

**Cómo se paga.** **50 % con la orden de compra** (anticipo de materiales) y **50 % contra los equipos instalados y reportando**. El servicio mensual arranca con el primer equipo andando.

| | **A. Equipos + servicio mensual** | **B. Anual adelantado** |
|---|---|---|
| Para quién | Compra activos y paga el servicio mes a mes | Tiene presupuesto de inversión y no quiere 12 facturas |
| Equipos y puesta en marcha | USD 4.115 (50 % con la OC, 50 % contra instalación) | Incluidos |
| Pago inicial total | USD 4.115 | USD 9.515 (equipos + 12 meses de servicio, con 10 % de descuento sobre el servicio) |
| Mensual | USD 500 — USD 100 por reefer, completo desde el primer mes | — el primer año; renovación anual USD 5.400 |
| Los equipos | Son del cliente | Son del cliente |
| **Total a 12 meses** | **10.115** | **9.515** |
| **Total a 24 meses** | **16.115** | **14.915** |

Facturación en dólares estadounidenses. De abonarse en pesos, se toma el tipo de cambio vendedor del Banco de la Nación Argentina de la fecha de pago. *Referencia al 4-sep-2026 (BNA vendedor $ 1.535): USD 4.115 ≈ $ 6.317.000 · USD 500 ≈ $ 767.500 · USD 9.515 ≈ $ 14.606.000.*

**Incluido en el servicio mensual:** nube con 12 meses de historial · alertas por temperatura, puerta abierta, sonda caída y equipo mudo · reposición sin cargo de cualquier módulo o sonda fallada, envío incluido · actualizaciones · soporte por WhatsApp y teléfono el mismo día hábil · informe mensual por reefer.

**Lo que hay que saber.** El sistema avisa; no garantiza la mercadería ni reemplaza la revisión del reefer. Sin energía en el módulo no mide: lo que avisa en ese caso es la nube, diciendo que dejó de reportar. La entrada de defrost necesita que el reefer tenga una señal o un contacto accesible; si alguno no lo tiene, esa entrada queda libre y el resto funciona igual. Las 2 salidas a relé vienen en el módulo; la sirena o baliza que se conecte no está incluida. Cada módulo necesita llegar a la red del campamento. El tendido del cable entre los dos reefers de cada par lo hace el cliente. Si un módulo se queda sin energía, quedan **dos** reefers sin vigilancia hasta que vuelva; para eso está el módulo de repuesto en el campamento. Los plazos de los hitos 1 y 2 suponen que el montaje en sitio se hace dentro de la ventana prevista, que depende de personal del campamento.

*Contacto en sitio: Andrés Leiva Chavez · Contacto comercial: Matías Alegre — Ingeniería Electrónica, UTN Facultad Regional Bahía Blanca · Grupo de investigación GIMAP · Encargado de proyectos de sistemas, Montagne · Mundo Outdoor · Termovigía, Bahía Blanca · 2920 59-1019 · alegrematias08@gmail.com · termovigia.vercel.app*

— — — — — — — — — — corte: lo de abajo NO se manda — — — — — — — — — —


## PARTE 2 — Alcance (interno)

### 2.1 Qué hay hoy, verificado

| Hecho | Evidencia |
|---|---|
| 1 equipo instalado en el campamento, `REEFER_01_SCZ`, firmware `firmware_revival` 2.6.21 | Puesto el 21-ago; reconectado por Andrés el 3-sep |
| Reportando cada ~5 s | Consulta a la base de Santa Cruz, 3-sep |
| **1 sola sonda y está FUERA del reefer** — mide ambiente | Andrés espera confirmación de Matías para meterlas |
| Elección de red abierta con internet real: probada 128 ciclos | `ESTADO_HONESTO.md` |
| **Sin contrato y sin un peso cobrado** | `PLATA.md` |
| **"Acá no pueden haber cables aéreos"** | Andrés, WhatsApp 3-sep 17:11 |
| **"Pasale presupuesto por los 3 módulos, así cada uno controla dos reefers"** | Andrés, WhatsApp 3-sep 17:13 |
| **"Son aprox 20/25 metros, el problema es que hay que pasar los cables con caño Daisa"** | Andrés, WhatsApp **3-sep 23:33** |
| **2 reefers están a la intemperie y 4 están adentro, bajo techo** | Andrés a Matías, **4-sep**. Es el dato que define toda esta versión |
| **De los 4 de adentro, uno está fuera de servicio: hoy hay 5 reefers activos** | Matías, 4-sep |
| Ya se mandó al sitio una **caja estanca IP65 apta para exterior** | Matías, 4-sep |
| **"Los de afuera pueden ir con un solo módulo, están juntos"** — el dato que fija esta versión | Andrés a Matías, **4-sep** |
| **Configuración final confirmada: 4 reefers adentro con 2 módulos, 1 módulo para los 2 de afuera. Los tres, dobles** | Matías, 4-sep |
| **Firmware de módulo doble: escrito y en auditoría, veredicto APTO CON CORRECCIONES** | `C:\Proyectos\frioseguro-v31\firmware_modular\VERIFICACION_V3.1_2026-09-04.md` — correcciones en curso |

### 2.2 Registro: por qué los tres módulos son dobles

> Las v4 y v5 discutieron dos versiones enteras si convenía un equipo por reefer o uno cada dos. La v6.1 partió la diferencia con el dato de Andrés (2 afuera / 4 adentro). **El 4-sep Andrés cerró el último hueco: los dos de afuera están juntos.** Con eso la discusión termina sin ganador ideológico: **se comparte en los tres pares, porque en los tres pares los reefers están al lado.**

**La regla que quedó, en una frase:** *se comparte módulo cuando los dos reefers están juntos — y en este sitio lo están los tres pares. Lo que cambia entre ellos no es el equipo, es la caja: estanca afuera, común adentro.*

**Qué se gana:**
- **Un equipo menos** que comprar, armar, probar, despachar y dar de alta: **−USD 485 en el precio** y **−USD 190 de costo directo**, y un punto de red menos que verificar.
- **El repuesto cubre el 100 % del parque con una sola caja**: los tres módulos son idénticos por dentro.
- **El módulo del par donde está el reefer fuera de servicio ya queda comprado con el canal libre** — el sexto entra después por USD 260, no por un equipo entero.

**Qué se pierde, y hay que tenerlo escrito:**
- **Una tirada más de cable, y a la intemperie.** Ahora son **3 tiradas**: dos bajo techo y una entre los dos contenedores de afuera. Están juntos (por eso comparten), así que debería ser la más corta, pero es la más expuesta. **Interno: ese tramo tiene que ser cable apto exterior, par trenzado, sin empalmes y canalizado.** En el documento del cliente **no va nada de esto**: solo la nota al pie de que el cable y el tendido no están incluidos (decisión de Matías).
- **Si cae un módulo, quedan dos reefers ciegos — ahora en los tres casos.** Antes los de afuera caían de a uno. Lo que compensa: el repuesto está en el campamento y es intercambiable con cualquiera.
- **El firmware doble pasa a ser crítico para el sistema entero** (§2.5 punto 3).

**El riesgo del bus, asumido con conocimiento — que quede escrito.** Andrés dijo *"son aprox 20/25 metros"* (3-sep 23:33) y el límite prudente que fijó @muestreador para este bus es **15 m**. Además, el cable ata las masas de **dos contenedores metálicos con puesta a tierra separada** por el hilo de datos (`ALCANCE_1WIRE.md` §2.6: *"el riesgo dominante de esta instalación"*). **Matías conoce el dato y acepta el riesgo.** Lo que se hace para acotarlo:

- **Pull-up de 2k2 con posición alternativa de 1k** en la placa (@esquematico lo está poniendo). El 1k es la carta que se juega si el bus no cierra a 25 m.
- **Los tres módulos se prueban en banco con 25 m de cable real antes de despachar**, con las 6 sondas colgadas. No sale nada que no haya cerrado a la distancia real.
- **Especificación de cable** (par trenzado exterior, el par DQ/GND junto en todo el recorrido, sin empalmes, canalizado): **queda interna**, no se manda al cliente — desde el 4-sep el cable no lo provee Matías, así que no corresponde especificarle un tipo que no le vamos a mandar. **Pero si Andrés pregunta qué cable comprar, se le dice: par trenzado apto exterior en las tres tiradas, y en la de afuera no se negocia.**
- Si aun así un bus no cierra en sitio, la salida técnica existe y es barata: pasar ese par a un segundo bus con su propio pin, o un repetidor 1-Wire. **No hay escenario en el que haya que devolver plata.**

**Lo que NO se le dice al cliente:** que esto es un riesgo. En el documento va la nota de que el cable y el tendido no están incluidos, y nada más sobre el cable. La mitigación real (prueba de banco con 25 m) tampoco se explica: se hace y punto.

**Y el tendido no se cotiza** (decisión de Matías, textual: *"no contemples el tema de las tiradas"*). La cuenta del caño de la v5 queda archivada en §3.3 **como historia y como argumento**, no como renglón: el precio que mandamos es firme y no depende de nada que pase en una zanja.

### 2.3 Qué lleva cada módulo, y qué de eso anda HOY (verificado en el código el 3-sep)

| Función | Por módulo (los tres son dobles) | Qué hace el firmware hoy | Evidencia |
|---|---|---|---|---|
| Sondas DS18B20 | 6 | Cada una identificada por ROM de 64 bits y reportada por separado; enganche en caliente; aviso si se desconecta; **offset de calibración por sonda en NVS**. **`SONDAS_MAX` está en 4: para el doble hay que subirlo a 8** — es el tamaño de un arreglo, una línea | `sondas.h`: `sondasEscanear`, `sondasLeer`, `sondasCalibrar`; línea 31 |
| **Verificación cruzada entre sondas** | — | **NO existe.** `sondasCalibrar()` iguala las sondas en un momento dado; el lazo de lectura **no compara sondas entre sí** ni alerta por deriva | ídem. Vendida en el **hito 2**, con la aclaración escrita en la página del cliente |
| Sensor de puerta | **2** | Implementado **para una sola puerta**: GPIO5, alerta por puerta abierta > 180 s, suprime la alerta de temperatura mientras está abierta. Viene deshabilitado por defecto (`SENSOR_DOOR_ENABLED false`). **La segunda puerta hay que agregarla, y ahora hace falta en los tres módulos** | `config.h` 72-74, 105, 119 · `.ino` 804-890 |
| Entrada de defrost | **2** | Implementada **para una sola entrada**: GPIO33, NA/NC configurable, deshabilita alertas durante el ciclo con 30 min de enfriamiento. **La segunda hay que agregarla, y tiene que silenciar solo el reefer que descongela** | `config.h` 91-96, 122 · `.ino` 54-55, 100-101, 872-878 |
| Salidas a relé | 2 | **1 gobernada**: GPIO26, se activa sola con la alerta si `relayEnabled`. La segunda queda cableada y disponible. **El accionamiento manual desde el panel NO existe** | `config.h` 76-77, 140-150 · `.ino` 369-375, 483-488, 915-944 · `comandos_nube.h` sin comando de relé → **hito 5** |
| Gabinete | **1 IP65 estanco de exterior** (Roker PRG357, $ 44.419) + **2 de interior** (Genrod IP65 210×310×110, $ 21.203) | — | `BOM_CERRO_MORO.md` §5 · caja de exterior ya enviada al sitio (4-sep) |

**Regla de venta.** Lo que **no** está andando hoy y va vendido con hito, nunca como característica de hoy:
- **Segunda puerta, segundo defrost y `SONDAS_MAX` a 8** — el software del módulo doble. Costeado en §3.2, hito 2.
- **Verificación cruzada entre sondas** — hito 2.
- **Accionamiento manual del relé desde el panel** — hito 5.

**Lo que esta configuración se lleva puesto, y hay que decirlo:** en la v6.1 los 2 módulos simples corrían el firmware que ya anda hoy, y eso era un colchón — si el software del doble se atrasaba, arrancaba igual la mitad del sistema. **Con los tres módulos dobles ese colchón desaparece: el firmware de módulo doble pasa a ser crítico para el 100 % del pedido.** Estado real: **escrito y en auditoría** — `C:\Proyectos\frioseguro-v31\firmware_modular\VERIFICACION_V3.1_2026-09-04.md`, veredicto **APTO CON CORRECCIONES**, correcciones en curso. **No se vende como cosa hecha: se vende en el hito 2, como siempre.**

**Detalle que no se puede pasar por alto en el diseño del doble:** **el defrost de un reefer no puede silenciar las alarmas del otro.** Hoy el defrost deshabilita *todas* las alertas del equipo. En el módulo doble tiene que silenciar **solo las sondas del reefer que está descongelando**. Está dentro de las horas de §3.2 y es lo que hay que probar sí o sí antes del hito 2.

**Orden de armado:** identificación por ROM sí o sí (si se lee por índice, cuando cae una sonda la otra se reporta con el nombre equivocado — con 6 sondas y 2 reefers por caja eso es inaceptable). **Cuál de las dos líneas se despacha — `firmware_revival` extendido o `firmware_modular` v3.1 — lo define @firmware cuando cierren las correcciones de la auditoría del 4-sep; es la decisión técnica que bloquea el despacho.** **Pull-up 2k2 con posición alternativa de 1k** (@esquematico), 3 hilos (nada de parasite power), 100 nF + 10 µF al pie de la sonda más lejana de cada rama. **Habilitar `SENSOR_DOOR_ENABLED`, probar las dos puertas y los dos defrost, y correr la prueba de banco con 25 m de cable en los tres módulos antes de despachar.**

### 2.4 Lo que se instala, y quién

**Módulo doble de exterior (×1, para el par de afuera):** **gabinete estanco IP65 apto para exterior** (Roker PRG357 200×200×155), fuente de 5 V 2 A, plaqueta con borneras a tornillo, ESP32 en zócalo, módulo de 2 relés, **prensacables en todas las entradas**, 6 sondas DS18B20 estancas, 2 reed de puerta, 2 entradas de defrost.
**Módulo doble de interior (×2):** gabinete IP65 de interior (Genrod 210×310×110 o las de stock si pasan la medición `M9`), misma electrónica, 6 sondas, 2 reed, 2 defrost.
**Kit de repuesto (×1):** un **módulo doble** completo — los tres son idénticos por dentro, así que **cubre a cualquiera de los tres** — + 3 sondas + 1 reed. Va con gabinete de interior: **si el que falla es el de afuera, la electrónica se pasa a la caja estanca que ya está en sitio** (queda escrito en el runbook).
**El cable no lo mandamos** (decisión del 4-sep): las tres tiradas las provee y las hace el cliente.

**Montaje: Andrés (o quien la empresa designe), con kit preconfigurado y probado en banco + videollamada.** Dos pasajes a Santa Cruz, alojamiento, inducción y 5 días de ingeniero rondan los $ 2.500.000, y Matías no puede viajar en octubre (parada de Dreyfus). Eso es lo que esta propuesta no cobra.

**Intemperie: en el documento del cliente se dice "gabinete estanco IP65 apto para exterior" y nada más.** Ni material, ni proceso de fabricación, ni impresión 3D. Ni en el PDF ni en el WhatsApp.

### 2.5 Los riesgos técnicos abiertos

1. **Las tres tiradas de 20-25 m** — riesgo asumido, mitigaciones en §2.2. **Subió respecto de la v6.1**: tres tiradas en vez de dos, y **una es a la intemperie** (la del par de afuera, que es la más corta pero la más expuesta). Interno: cable apto exterior en esa tirada, sin empalmes.
2. **Cobertura de red en 3 puntos** — el mejor número de todas las versiones (eran 5 en la v5.2 y 4 en la v6.1). Si alguno queda corto se resuelve con un repetidor barato, pero hay que saberlo **antes de despachar**. Pregunta 1 de §5.2, no frena el envío.
3. **EL RIESGO NUEVO Y EL MÁS GRANDE: el firmware de módulo doble ahora es crítico para los TRES módulos.** En la v6.1 dos de los cuatro equipos corrían el firmware que ya anda hoy en `REEFER_01_SCZ`; si el doble se atrasaba, la mitad del sistema arrancaba igual. **Ese colchón ya no existe: sin firmware doble no reporta nadie, y el hito 2 cae entero.** Estado real, verificado: el firmware está **escrito y auditado** — `C:\Proyectos\frioseguro-v31\firmware_modular\VERIFICACION_V3.1_2026-09-04.md`, veredicto **APTO CON CORRECCIONES**, correcciones **en curso**. Lo que esto obliga a @comercial: **no prometer el hito 2 por teléfono con más firmeza que la del papel**, y avisarle al Director que **el cierre de las correcciones del firmware doble está en el camino crítico de esta venta**, no al costado.
4. **El defrost cruzado** (§2.3): que el descongelamiento de un reefer no ciegue al otro. Antes aplicaba a 2 módulos; **ahora a los 3, o sea a los 6 reefers**. Trabajo de software, costeado, y es lo que hay que probar antes del hito 2.
5. **Si cae un módulo quedan dos reefers ciegos, ahora en los tres pares.** Mitigación real y ya cotizada: el **módulo de repuesto queda en el campamento** y sirve para cualquiera de los tres.
6. **La caja de exterior a la intemperie de Santa Cruz** es la única parte del equipo sin antecedente de campo largo, y ahora **de ella dependen 2 reefers, no 1**. La que se mandó al sitio el 4-sep es, de hecho, **la prueba de campo**: conviene pedirle a Andrés una foto después del primer temporal.

### 2.6 Opcionales, después de la primera orden

**El sexto reefer cuando vuelva a servicio: USD 260 + USD 100/mes** — entra en el canal libre del módulo de su par, **sin equipo nuevo**. Ya está escrito con precio en el documento del cliente: no hay que venderlo de nuevo, solo ejecutarlo. **Es el upsell más probable y el de mejor margen de esta cuenta.** · Sirena o baliza física para la salida de relé (USD 40; el relé ya está incluido) · **cuarta sonda** en un reefer (USD 40 + USD 5/mes) · base con batería y 4G, la única que avisa el corte de energía por sí misma (a cotizar) — **especialmente vendible para el módulo de la intemperie, del que ahora dependen dos reefers**. Se ofrecen cuando las sondas estén andando, no antes.

---

## PARTE 3 — Números de respaldo

Base: BOM real (`BOM_KIT_V1.md` rev B de @hardware, precios de MercadoLibre AR verificados el 2-sep-2026, a precio de reposición). Cambio $ → USD al BNA vendedor 1.535 del 3-sep.

### 3.1 Los dos precios: USD 750 el doble de interior, USD 765 el doble de exterior

| | Doble interior (ARS) | USD | Doble exterior (ARS) | USD |
|---|---:|---:|---:|---:|
| Electrónica: ESP32 13.990 + módulo de 2 relés 5.028 + fuente 5 V 2 A 7.980 + consumibles de placa y prensacables ~11.800 | ~38.800 | **25** | ~38.800 | **25** |
| **Gabinete** — interior Genrod IP65 210×310×110 **$ 21.203** · exterior **Roker PRG357 IP65 200×200×155 $ 44.419** | 21.203 | **14** | 44.419 | **29** |
| Sondas DS18B20 estancas rearmadas con 3 m de cable y prensacable (6) | ~55.200 | **36** | ~55.200 | **36** |
| Sensores magnéticos de puerta cableados (2) | 9.492 | **6** | 9.492 | **6** |
| Envío a Santa Cruz, prorrateado | ~18.400 | **12** | ~18.400 | **12** |
| Armado + **prueba de banco documentada con 25 m de cable** + garantía de reposición amortizada | | **150** | | **150** |
| Parte de plataforma del desarrollo: USD 1.000 repartidos en **3** módulos vendidos | | **333** | | **333** |
| **Costo** | | **576** | | **591** |
| Margen | | **174** | | **174** |
| **Precio** | | **750** | | **765** |

**Los USD 15 de diferencia son la caja, exactos.** $ 44.419 − $ 21.203 = **$ 23.216 = USD 15,1** al BNA vendedor 1.535. **El margen absoluto es idéntico en los dos módulos (USD 174).** No se aprovechó la caja cara para meter margen: el que va afuera cuesta más porque su caja cuesta más, y eso es todo lo que hay para explicar si preguntan.

**Los márgenes bajaron y hay que saberlo: de 34 % a 23 %.** Tres motivos, los tres honestos y ninguno reversible con marketing:
1. **La plataforma se reparte entre 3 módulos en vez de 4:** USD 250 → **333 por módulo**. Es el costo de vender menos cajas. (`+83`)
2. **La caja de interior real cuesta $ 21.203, no los ~$ 8.500 que asumió la v6.1.** El BOM de @hardware del 4-sep corrigió el número; la propuesta lo toma. (`+8`)
3. **A favor:** se cae el renglón de los 25 m de cable de interconexión (USD 10), porque desde el 4-sep el cable no lo proveemos. (`−10`)

**Dónde está la plata de esta cuenta, entonces:** en el **abono (76 % de margen, §3.4)** y en la **puesta en marcha**. Los equipos son el ticket de entrada, no el negocio. **Eso es exactamente el modelo de PLATA.md** — y por eso el abono no se toca ni un dólar aunque el inicial haya bajado 485.

**Por qué NO se subieron los unitarios para sostener el 4.600.** Se podía: bastaba poner el doble de exterior en 900 y el repuesto en 500 y nadie iba a auditar el número. **No se hace.** El cliente que ve bajar el precio cuando baja el alcance cree el precio; el que ve el mismo total con un equipo menos aprende que el número era blando y va a apretar en el abono, que es lo único que importa acá. **Menos equipos = menos plata, dicho en voz alta, es lo que hace creíble el 500/mes.**

**El repuesto queda en USD 400** (sin cambio). Ahora cubre **el 100 % del parque** con una sola caja, porque los tres módulos son idénticos por dentro — en la v6.1 cubría 4 equipos de 2 tipos distintos. Es el renglón que más ganó con esta configuración.

### 3.2 Puesta en marcha, USD 1.450

| Trabajo | h |
|---|---:|
| Sondas, rangos y umbrales por reefer + **calibración de las 15 sondas** contra referencia y registro de offsets | 10 |
| **Software del módulo doble: segunda puerta, segundo defrost con silenciado por reefer, `SONDAS_MAX` a 8, validación del bus a 25 m** | 10 |
| Registro exportable con código de verificación | 14 |
| Panel multi-equipo y usuarios de lectura | 10 |
| Puesta en marcha remota (alta, credencial, OTA verificada, prueba de puertas y defrost), pruebas de campo con Andrés, runbook y capacitación — **3 módulos** | 10 |
| Salud de bus, histéresis de 3 barridos y **verificación cruzada entre sondas** | 4 |
| **Total a USD 25/h** | **58 = USD 1.450** |

**Bajó de 1.500 a 1.450, y baja poco a propósito.** Lo único que se cae es **un módulo** de alta remota, credencial, OTA verificada y prueba de puertas y defrost: **2 h**. Todo lo demás es idéntico con 3 módulos que con 4 — **y el software del doble, que son 10 h, ahora hay que escribirlo igual pero lo usan los tres equipos en vez de dos.** Si alguien pregunta por qué no bajó más: porque las horas que quedan hay que trabajarlas.

*Las 10 h del software del doble siguen siendo la línea a vigilar, y ahora con más razón: el firmware está escrito y auditado (APTO CON CORRECCIONES, 4-sep) pero las correcciones no están cerradas. **Si @firmware dice que son más horas, salen del margen, no del precio.***

### 3.3 **LA CUENTA DEL CAÑO** — archivo, y por qué ya no entra en el precio

> Se conserva de la v5 **como historia y como argumento**, no como parte del presupuesto. **El tendido lo hace y lo paga el cliente, y no aparece en el documento que se manda.** Ahora son **3 tiradas: 2 bajo techo y 1 a la intemperie** (la del par de afuera, que está junto y debería ser la más corta). Para las dos de adentro el número real es **más bajo que esta cuenta**, que se hizo para caño rígido exterior; para la de afuera esta cuenta es la buena.

| Ítem (por par, 25 m de recorrido) | Subtotal |
|---|---:|
| Caño galvanizado Daisa 3/4 liviano, 9 tiras de 3 m a $ 11.637 | $ 104.733 |
| Cuplas (8), curvas (6), cajas de paso estancas (4), conectores caño-caja (10) | $ 96.000 |
| Grampas omega 3/4 una cada 1,5 m (18) + tarugos y tornillos | $ 35.000 |
| Cable exterior, 30 m a $ 400/m | $ 12.000 |
| **Materiales por par** | **≈ $ 247.700 ≈ USD 161** |
| Mano de obra: 2 jornadas de oficial electricista al piso de tarifa ($ 12.000/h × 16 h) | **$ 192.000 ≈ USD 125** |
| **Total por par** | **$ 439.700 ≈ USD 286** |

**Para qué sirve esta cuenta ahora que no la cotizamos.** Tres cosas concretas:
1. **Saber el tamaño de lo que el cliente gasta por su lado** (≈ USD 286 por tirada en el peor caso, bastante menos bajo techo y menos aún entre dos contenedores pegados). Si dicen "esto de la obra no lo teníamos previsto", la respuesta ya está: **la configuración la describieron ellos**, y compartir módulo es justamente lo que les ahorró un equipo.
2. **Tener lista la variante de rescate.** Si la obra los frena, **no se pierde la venta**: se ofrece un módulo por reefer, sin ninguna obra, con el mismo total. Está calculado en la v5.2 de este archivo (historial de git).
3. **Que nadie regale la instalación.** Si aparece la tentación de "se lo hacemos nosotros para cerrar", el número a tener en la cabeza es **USD 286 por tirada**, más pasajes y estadía.

### 3.4 Servicio mensual: qué cuesta servir y qué se cobra

| Costo directo mensual | v2 (12 sondas) | **v7.0 (15 sondas, 5 reed, 3 módulos)** |
|---|---:|---:|
| Supabase Pro | 25 | 25 |
| Reposición amortizada (módulos y sondas en garantía) | 10 | **15** |
| Soporte (2 h → 2,3 h a USD 25) | 50 | **57** |
| Informe mensual | 25 | 25 |
| **Total** | **110** | **122** |

**Tarifa: USD 100 por reefer por mes × 5 = USD 500/mes** (decisión de Matías, 4-sep, **no se toca con la configuración nueva**). Costo directo 122 → **margen bruto USD 378 (76 %)**. **Con el inicial en 4.115, el abono paga el equipamiento entero en 8,2 meses de margen: es el renglón que sostiene la cuenta.** La justificación, y es la que hay que decir si preguntan: **mantenimiento del servidor, custodia de los datos y seriedad del servicio** — el registro que se entrega tiene que estar disponible y ser defendible dentro de un año, y eso se paga todos los meses aunque no pase nada.

**El abono es estrictamente proporcional a los reefers, no a los equipos**: 5 reefers = 500, 6 = 600. **Eso es exactamente lo que permite bajar el inicial sin tocar el abono**: pasamos de 4 cajas a 3 y se vigila lo mismo — 5 reefers. Si alguien intenta el argumento *"pusieron un equipo menos, bajen el abono"*, la respuesta está escrita desde la v2: **el servicio se cobra por reefer vigilado, no por caja instalada.** **Cuando entre el sexto, los USD 100 adicionales son casi margen puro** y el equipo ya está puesto.

**El escalón de los primeros 3 meses al 50 % sigue eliminado** (decisión de Matías, 4-sep): abono completo desde el primer mes en las dos formas. Lo justifica que el servicio ya está corriendo —servidor, custodia y guardia de alertas— desde el primer equipo que reporta.

### 3.5 Condiciones de pago — 50 / 50, y por qué no 25

**50 % con la orden de compra (anticipo de materiales) y 50 % contra los equipos instalados y reportando.** El abono arranca con el primer equipo andando.

El fundamento es de caja: hay que comprar y armar **4 módulos** (3 + el repuesto) antes de ver un peso del segundo tramo, y cobrar ese tramo a un contratista que todavía no tiene nombre. Con el 50 % (**USD 2.057,50 ≈ $ 3.158.000**) la compra completa de materiales —**≈ $ 375.000 con flete, §3.7**— queda cubierta **más de ocho veces** antes de tocar un componente. Con el 25 % también alcanzaría para los materiales; lo que no cubriría es el **riesgo de cobranza del segundo tramo**, que es lo que en realidad se está financiando.

Los hitos siguen existiendo **como compromiso de entrega con plazo**, y así está escrito en el documento del cliente: *"no se facturan aparte, están incluidos en el precio"*. **Punto para que Matías confirme:** cobrar antes de entregar los hitos es más cómodo para la caja y más exigente con la palabra.

### 3.6 Las dos formas de pagar, y por qué se cayó la tercera

**A. Equipos + servicio mensual.** 4.115 + 12 × 500 = **10.115** el primer año; 6.000/año después; **24 meses 16.115**.

**B. Anual adelantado, 10 % de descuento sobre el año de servicio.** 4.115 + (12 × 500) × 0,9 = 4.115 + 5.400 = **USD 9.515**; renovación 5.400/año; **24 meses 14.915**. El descuento le ahorra **USD 600 el primer año** y lo que compra es concreto: **cero riesgo de cobranza durante 12 meses con un contratista que probablemente pague a 60-90 días, una factura en lugar de doce, y caja para armar los equipos.** *Se perdió el USD 10.000 redondo de la v6.1, y no se recupera inflando: **la B ahora entra abajo de cinco cifras**, que para un comprador con nivel de aprobación es todavía mejor argumento que un número redondo.*

**C, eliminada.** Matías: *"el de la inversión inicial no lo ofrecería"*. Era la única que ponía USD ~4.115 nuestros en manos de un contratista a 1.500 km, sin poder retirar los equipos y sin contrato con permanencia. **No se vuelve a ofrecer sin contrato validado por contador y un cliente con historial de pago.** Con dos opciones el comprador elige; con tres se paraliza.

**Sin cláusulas condicionales.** La propuesta no tiene condición de metros, ni de canalización, ni corrección de precio por par: **el tendido es del cliente y el precio es firme.**

### 3.7 **Los 4 módulos: qué falta comprar y cuánto sale**

**Qué hace falta.** 4 módulos dobles: **1 de exterior + 2 de interior + 1 de repuesto**. Sondas: 15 instaladas + 3 de repuesto = **18**. Reed: 5 instalados + 1 de repuesto = **6**. Defrost: 5 entradas (cable y bornera, sin componente caro).

**Cruce contra el stock declarado** (`BOM_KIT_V1.md` §1 y `BOM_CERRO_MORO.md` de @hardware, tomando el número más bajo de cada rango, y reservando **3 ESP32 para las galgas de Dreyfus**, que es P0 de octubre):

| Ítem | Hacen falta | Stock declarado | Faltan | Precio | **A comprar** |
|---|---:|---:|---:|---:|---:|
| ESP32 DevKit | 4 + 3 (galgas) = **7** | 4 | **3** | $ 13.990 c/u | **$ 41.970** |
| Sondas DS18B20 | **18** | 15 | **3** | $ 4.388 c/u | **$ 13.164** |
| **Caja IP65 de intemperie** Roker PRG357 (el módulo de afuera) | 1 | 0 de esa medida | **1** | $ 44.419 | **$ 44.419** |
| Gabinetes de interior para los 3 dobles restantes (2 + repuesto) | 3 | 3 de 165×165 — **medida sin verificar para 6 sondas + 2 puertas + 2 defrost** | **3** (peor caso) | $ 21.203 c/u | **$ 63.609** |
| Fuentes 5 V **2 A** | 4 | 5, **amperaje sin verificar** | **4** (peor caso) | $ 7.980 c/u | **$ 31.920** |
| Módulos de relé 2 canales | 4 | 10 | 0 | — | **$ 0** |
| Reed / sensor de puerta | 6 | 10 | 0 | — | **$ 0** |
| Consumibles del §3.1 del BOM reescalados a 4 módulos (plaquetas, borneras, tiras hembra, **R 2k2 y 1k**, 10 k, 100 nF, electrolíticos, separadores, **prensacables** por las entradas del estanco) | — | — | — | — | **$ 120.000** |
| Cable de 3 hilos para rearmar 18 sondas a 3 m + termocontraíble | — | — | — | — | **$ 40.000** |
| **Cable de interconexión entre reefers** | — | — | — | **lo compra el cliente** | **$ 0** |
| **TOTAL** | | | | | **≈ $ 355.000** |

Con flete y diferencias de vendedor: **≈ $ 375.000 ≈ USD 244**. **Si las 3 cajas de stock pasan la medición `M9` de @hardware, baja $ 63.609 → ≈ $ 291.000 (USD 190)**; si además las fuentes de stock son de 2 A, baja otros $ 31.920.

*Contra la v6.1 (≈ $ 430.000): **−$ 55.000**, y eso con la caja de exterior real a $ 44.419 en vez de los $ 22.000 mal presupuestados. El equipo que se cae paga con creces la corrección del BOM.*

**Contra el anticipo del 50 % (USD 2.057,50 ≈ $ 3.158.000), la compra completa es el 12 %.** No hay problema de plata ni de cantidades. **La caja IP65 de intemperie es el renglón de mayor plazo de entrega: hay que pedirla primero** (y ya hay una en el sitio, que es la prueba de campo).

**Por qué el hito 1 SÍ es alcanzable.** El hito 1 es *"el equipo que ya está instalado, con sus 3 sondas dentro del reefer, calibradas, rangos definidos y primera alerta real"*. **No depende de que lleguen los módulos nuevos ni del firmware doble: depende de que lleguen 2 sondas** (el equipo instalado ya tiene 1, y ahora son 3 por reefer). `REEFER_01_SCZ` está montado y reportando desde el 21-ago con **1 sola sonda, y está fuera del reefer**.

**El plan arranca cuando aceptan, no antes.** Semana 0 = aceptación + anticipo del 50 %. Hasta que eso pase **no se compra, no se arma y no se despacha nada**, y a Andrés no se le pide que reserve ninguna ventana: trabaja por turnos de 15 días y no es él quien aprueba.

| Paso | Plazo desde la aceptación | Quién |
|---|---|---|
| Conteo del stock real + las mediciones del §8.1 del BOM y la `M9` (interior de las 3 cajas, amperaje de las fuentes, relé con IN al aire) | semana 0 | Gonza |
| Compra del faltante — **la caja de exterior primero** — y rearmado de sondas a 3 m | semana 0-1 | Gonza / Matías |
| Despacho de 2 sondas para el equipo ya instalado (encomienda, 5-8 días hábiles) | semana 1 | — |
| **Cierre de las correcciones del firmware doble** (auditoría 4-sep, APTO CON CORRECCIONES) + 2ª puerta, 2º defrost por reefer, `SONDAS_MAX` a 8 — **ahora bloquea a los 3 módulos** | semana 1-2 | Matías / @firmware |
| Alta, calibración remota, rangos y primera alerta real | semana 2 | Andrés + Matías |
| **HITO 1** | **semana 2** | — |
| Armado de los 4 módulos + **prueba de banco de los tres con 25 m de cable** (~16 h) | semana 1-2 | Gonza / Sergio |
| Despacho de los 4 bultos (3 módulos + repuesto) a Cerro Moro | semana 2 | — |
| **Tendido del cable en los 3 pares** (el de afuera, con cable apto exterior) | semana 2-3 | **cliente** |
| Montaje de los módulos por personal del campamento | semana 3-4 | campamento |
| Alta y calibración de las 12 sondas nuevas (las 3 de `REEFER_01_SCZ` ya quedaron en el hito 1) | semana 4 | Matías |
| **HITO 2** (los 5 reefers reportando + una semana sin falsas alarmas) | **semana 5** | — |

**El riesgo que hay que decir en voz alta: el hito 2 está apretado y ahora tiene DOS dependencias, no una.** La semana sin falsas alarmas arranca cuando los 3 módulos reportan —alrededor de la semana 4— y el hito vence en la 5: **una semana, sin colchón**. Y depende de (a) **una obra ajena** —el tendido del cliente, ahora en tres pares— y (b) **el firmware doble, que ya no tiene plan B**: en la v6.1 los 2 simples reportaban igual con lo que ya anda. **Matías no debería prometer el hito 2 por teléfono con más firmeza que la que dice el papel.**

**Por qué se puede empezar a armar antes de la orden de compra, sin exponer un peso nuevo.** Los kits **ya estaban planificados como las unidades de demostración del plan comercial de Bahía**. Si Cerro Moro no compra, **no quedan colgados: van a su destino original**. **La contracara para el Director: si Cerro Moro compra, Bahía se queda sin demos** — aunque ahora son **4 módulos y no 5**, así que el golpe es menor. Recomendación: **la reposición de los kits de Bahía se dispara en el mismo pedido que la orden de compra**, no después.

### 3.8 Moneda, validez, facturación

**Facturación en USD, pago en pesos al BNA vendedor de la fecha de pago, sin validez en el PDF.** Nota interna: revisar precios si pasan más de 6 meses desde el 4-sep. Antes de la cotización firme hay que saber: monotributo vs. RI, plazo de pago, si acepta la cláusula de moneda, quién firma. Se pregunta cuando la empresa tenga nombre.

### 3.9 Contra una pérdida y contra la competencia

Una pérdida de 3 t valuada al precio de novillo en pie ($ 4.181/kg, INMAG jul-2026) son $ 12,5 M: **16 meses de servicio** al abono de USD 500 (≈ $ 767.500 por mes). testo Saveris 2-T2: USD 318 por unidad y mide **un** punto; para cubrir los 15 puntos de esta propuesta harían falta 15 unidades = **USD 4.770** antes de importación — **más que el total de esta propuesta, que ahora es 4.115** — sin nube, sin puerta, sin relé, sin defrost, sin repuesto en sitio — y se configura con una red WiFi y una clave, que es exactamente lo que este sitio no tiene. **Y ninguna de esas unidades es apta para la intemperie sin gabinete adicional.**

---

## PARTE 4 — Puesta en marcha: qué es cada hito por dentro

Las duraciones se cuentan **en semanas desde la aceptación**, no contra el calendario. Los hitos pesados caen después de la semana 5 para no chocar con la parada de Dreyfus.

| Hito (cliente) | Etapa interna | Desde | Hasta | Cómo se acepta |
|---|---|---|---|---|
| 1 — El equipo ya instalado con sus 3 sondas adentro y calibradas, rangos, primera alerta real | E0 | semana 0 | **semana 2** | Captura de la alerta en el celular + registro en nube + **planilla de calibración con el offset de las 3 sondas de `REEFER_01_SCZ`** |
| 2 — Los 3 módulos y los 5 reefers reportando; nada se pierde, nada sobra | E1: buffer offline, alertas encoladas, alerta de sonda caída, vigía de equipo mudo, discriminador de bus + histéresis, **detección de sonda que se desvía de las otras del mismo reefer**, **segunda puerta y segundo defrost con silenciado por reefer — en los tres módulos** | semana 2 | **semana 5** | Los 3 módulos montados con sus 15 sondas calibradas; desenchufar una sonda y que llegue la alarma; cortar la red 20 min sin perder lecturas; abrir una puerta 4 min y que avise; **forzar el defrost de un reefer de un par y verificar que el otro del mismo módulo sigue alarmando, en los tres módulos**; **una semana sin falsas alarmas** |
| 3 — Acceso seguro | E2: RLS cerrada, credencial por módulo, secretos fuera del binario, revocar claves quemadas | semana 5 | **semana 10** | Con la clave vieja no se escribe; todos los módulos siguen reportando |
| 4 — Actualización a distancia | E3: OTA con manifiesto inmutable | semana 10 | **semana 12** | Tres actualizaciones seguidas por aire al primer intento, en todos los módulos |
| 5 — Panel e informe | E4: usuarios de lectura, vista de los reefers, exportación con código, informe mensual automático, **comando de relé desde el panel** | semana 12 | **semana 15** | Un usuario de la empresa entra solo, baja el informe y acciona una salida desde el panel |

**El hito 2 es el apretado** (§3.7): la semana sin falsas alarmas arranca cuando los 3 módulos reportan, alrededor de la semana 4, y vence en la 5. **Sin colchón, con el tendido del cliente en el camino crítico de los tres pares y con el firmware doble sin plan B.**

Lo que hoy está roto y cada hito arregla (llave maestra en el binario, datos perdidos sin red, umbral en 50 °C, equipo muerto que no avisa, OTA que entra 1 de 4) está en `AUDITORIA_HALLAZGOS.md`; no cambió.

---

## PARTE 5 — Qué necesitamos para cerrar

### 5.1 De la empresa, cuando tenga nombre

Quién firma, cómo factura (monotributo/RI, plazo), si acepta la cláusula de moneda, **cuál de las dos formas de pago elige (A o B)**, y confirmación de que el montaje **y el tendido del cable en los tres pares** los hace personal del campamento (sin personal nuestro en sitio no corresponde ART ni legajo de contratista).

### 5.2 De Andrés: lo que sigue abierto

**Ninguna de estas frena el envío.**

1. **¿La red del campamento llega bien a los 3 puntos donde van los módulos?** Si alguno queda corto se resuelve con un repetidor barato, pero hay que saberlo **antes de despachar**.
2. **¿Los reefers tienen una señal o contacto de defrost accesible?** Si alguno no lo tiene, esa entrada queda libre y el resto funciona igual — ya está dicho así en el documento del cliente, sin letra chica.
3. **¿Cuál de los 4 de adentro es el que está fuera de servicio?** Define cómo se arman los pares: **el que está fuera va emparejado con un activo**, para que el canal libre quede en un módulo ya instalado y andando. **Es la única pregunta que todavía puede cambiar el armado.**
5. **¿Cuántos metros hay entre los dos de afuera?** Están juntos, así que debería ser la tirada más corta de las tres — pero es la única a la intemperie y conviene saber el número antes de armar.
4. **¿Para quién trabaja Andrés?** (empleado de PAAS o de una contratista). No es técnica: decide la Parte 7.

---

## PARTE 6 — Para Andrés (aparte del PDF)

### 6.1 WhatsApp — lo manda Matías

```
Andrés, quedó como me dijiste: los dos de afuera van con UN solo
módulo, ya que están juntos. Y los cuatro de adentro con dos módulos,
uno cada par. Tres módulos en total.

Los tres son iguales por dentro (cada uno atiende dos reefers); el de
afuera va en caja estanca para intemperie. Por cada reefer: 3 sondas
adentro, sensor de puerta y la señal de defrost, así no suena la alarma
cada vez que descongela.

Con un equipo menos el presupuesto bajó: quedó en USD 4.115 (era 4.600
con cuatro módulos). El servicio mensual sigue igual, USD 100 por reefer
por mes = 500 por los cinco que están andando.

El cable entre los dos reefers de cada par y su tendido corren por
cuenta de ustedes, incluido el de afuera. Los módulos los pruebo acá en
el banco con 25 metros de cable puestos antes de despacharlos.

El reefer que está fuera de servicio queda emparejado con uno que anda,
así el módulo ya va puesto y el día que vuelva se le suman las sondas
nomás, sin equipo nuevo.

Te paso el presupuesto: dos hojas, sin nombre de empresa, para que se lo
pases a quien corresponda. El equipo que ya está puesto sigue
reportando, así que mientras lo miran se puede ver el panel en cualquier
momento.
```

> **Por qué está escrito así, para que no se suavice al copiarlo:**
> **(a)** Arranca con **quedó como me dijiste** y repite su frase (*están juntos*). Andrés dio el dato y lo primero que lee es que se hizo exactamente eso. Vale más que cualquier argumento técnico.
> **(b)** **El precio que baja va en su propio párrafo, con el número viejo al lado.** Es lo más importante del mensaje: **menos equipos, menos plata**. Un presupuesto que baja cuando baja el alcance es un presupuesto en el que se puede confiar, y eso es lo que sostiene el abono cuando lo miren.
> **(c)** **Que el abono NO baja se aclara en la misma frase.** Se dice ahora, tranquilo, y no en una discusión dentro de tres semanas: se cobra por reefer vigilado, y los reefers siguen siendo cinco.
> **(d)** **El tendido queda dicho en una línea, con “incluido el de afuera” explícito.** No se esconde que ahora hay una tirada más. Lo que **no** va es la spec de cable ni la palabra riesgo (decisión de Matías).
> **(e)** **La prueba con 25 m compra confianza técnica.** Dice, sin decirlo: sé que hay distancia y me hago cargo.
> **(f)** **El sexto reefer aparece como previsión, no como recorte.**
> **(g)** **No le pide nada.** Andrés trabaja por turnos de 15 días y **no es él quien aprueba**. Cierra en *te paso el presupuesto*.
> **(h)** **No menciona el material de la caja ni cómo se fabrica.** Ni acá ni en el PDF.

### 6.2 Guion de 5 líneas para que la presente él

1. **Arrancá por el problema, no por el producto:** "un reefer que se corta un fin de semana es la comida de todo el campamento, y hoy nadie se entera hasta que abren la puerta."
2. **Mostrá lo que ya anda:** abrí el panel en el celular y mostrá la temperatura de ahora del equipo instalado — sigue reportando mientras la propuesta se evalúa. Si podés, sacá una sonda al aire un minuto y que vean subir la curva. Eso convence más que el PDF.
3. **Decilo en una frase:** "los dos de afuera comparten un módulo estanco porque están pegados; los cuatro de adentro se cubren con dos. Tres sondas adentro de cada reefer, te avisa al celular si se sale de rango o si queda la puerta abierta, y arma el registro mensual solo."
4. **Si preguntan por el cable:** "son tres tiradas cortas, una por cada par, y los dos reefers de cada par están al lado. El cable y el caño los ponemos nosotros; ellos dicen cómo va."
5. **Lo que NO prometés:** que garantiza la mercadería (avisa, no garantiza) · que avisa el corte de luz (avisa que el equipo dejó de reportar) · que la sirena está incluida (van las salidas, la sirena se conecta) · que está terminado (hay una puesta en marcha por hitos, y está en el precio) · fechas o precios distintos a los del PDF. Cualquier pregunta técnica o de números: "eso lo contesta Matías, lo llamamos ahora."

---

## PARTE 7 — La relación con Andrés (para que Matías decida)

**Lo que cambió:** en la v1 Andrés era el contacto en sitio de un cliente (Panamerican) y la regla era simple: **ningún pago ni beneficio ligado a que su empleador compre.** Ahora es él quien **ofrece y presenta** la propuesta a una tercera empresa que él elige. Está haciendo de referidor, de hecho.

**Lo que sigue vigente, sin discusión:** si el comprador termina siendo Pan American Silver, o una contratista que opera bajo su Código de Conducta de Proveedores (que alcanza a proveedores **y a sus subcontratistas**), **no hay comisión ni reconocimiento material.** Y hay que ser honesto con la probabilidad: **cualquier empresa que opere dentro del campamento de Cerro Moro está, casi seguro, bajo ese código.**

**El conflicto de interés, escrito:** Andrés trabaja adentro (no sabemos todavía si es empleado de PAAS o de una contratista — **hay que preguntarlo**), elige a quién ofrecerle el sistema y lo presenta con la credibilidad de su puesto. Si cobra por eso, pasa de "el que trajo un proveedor bueno" a "el que le vendió algo a la empresa de al lado y se llevó una parte". **El costo de un reconocimiento mal puesto sigue siendo mayor que el negocio.**

| Opción | Qué es | A favor | En contra |
|---|---|---|---|
| **1. Nada material, todo el reconocimiento no monetario** (status quo) | Agradecer por escrito, darle el acceso y la hoja de una carilla para que quede bien adentro, nombrarlo como contacto en sitio, contarle el caso como logro suyo | Cero riesgo. Es lo que él pidió (*"la gente de acá no lo vio"*): quedar bien, no cobrar | Si el negocio crece por él y no recibe nada, el empuje puede enfriarse |
| **2. Referidor formal solo para leads AJENOS al campamento** (Bahía, Venado Tuerto, futuros) | Reconocimiento único equivalente a 1 mes de abono del cliente referido, pagado después del 3er abono cobrado; **excluye** a PAAS, sus contratistas y cualquier empresa de Cerro Moro; condicionado a que su empleador lo permita | Es honesto, separa los mundos, y **ya tiene un caso real: Venado Tuerto lo trajo él** | Hay que escribirlo y preguntarle si su empleador tiene política de actividades externas |
| **3. Reconocimiento en especie, fuera del negocio** | Un equipo Termovigía para uso propio, o capacitación, sin vínculo con ninguna compra | Barato, tangible | Si se da mientras Cerro Moro está en discusión, se lee igual que una comisión |

**Mi recomendación honesta:** 1 ahora, 2 por escrito cuando Venado Tuerto avance, y **preguntarle a Andrés para quién trabaja y si su empresa tiene política de actividades externas** antes de ofrecerle cualquier cosa. La 3, nunca durante la negociación de Cerro Moro. **No decido: decide Matías.**

**Lo bueno de esta vuelta:** a Andrés le llega **exactamente el sistema que él describió**, armado sobre datos que dio él (los metros, el caño, la intemperie, el reparto adentro/afuera y que los de afuera están juntos) — **y con el precio más bajo, que es lo que él va a tener que defender adentro**. Ya no hay que explicarle ningún "no". Eso simplifica el mensaje y lo deja bien parado adentro, que es lo único que él pidió para sí.

---

## Anexo — Fuentes consultadas

- Alcance del bus, pull-ups, tierras entre contenedores, estrella no conmutada y límite prudente de 15 m: `C:\Proyectos\frioseguro\hardware\ALCANCE_1WIRE.md` (@muestreador), §2.6.
- **Costo por equipo y stock declarado:** `C:\Proyectos\frioseguro\hardware\v1_modulos\BOM_KIT_V1.md` rev B (@hardware) — §1 inventario, §3.1 compra, §3.4 costo por equipo, §8.1 las dos mediciones que bloquean el pedido. Precios ML verificados el 2-sep-2026.
- **Precios reales de gabinete (Roker PRG357 $ 44.419 de intemperie, Genrod $ 21.203 de interior) y la corrección del ~$ 22.000 mal presupuestado:** `C:\Proyectos\frioseguro\hardware\mini\BOM_CERRO_MORO.md` (@hardware, 4-sep-2026), §5 y §9.
- **Firmware de módulo doble — el que ahora hace falta en los tres equipos:** `C:\Proyectos\frioseguro-v31\firmware_modular\VERIFICACION_V3.1_2026-09-04.md`, veredicto **APTO CON CORRECCIONES**, correcciones en curso.
- Estado real y auditoría: `C:\Proyectos\frioseguro\entrega_scz\docs\ESTADO_HONESTO.md` · `AUDITORIA_HALLAZGOS.md`.
- **Qué hace hoy el firmware con sondas, puerta, relé y defrost (leído el 3-sep-2026):** `firmware_revival/sondas.h` (línea 31, `SONDAS_MAX`) · `config.h` 67-150 · `firmware_revival.ino` 369-375, 483-488, 804-944 · `comandos_nube.h` (**sin** comando de relé).
- Contrato base: `MATI-HQ\comercial\CONTRATO_TERMOVIGIA_v4.md`.
- Precios de canalización (§3.3, archivo), 1-Wire AN148, testo Saveris 2-T2, novillo INMAG, dólar BNA vendedor 1.535, Supabase Pro y Código de Conducta de Proveedores de PAAS: enlaces conservados en la v5.2 de este archivo (historial de git).

## Anexo — Lo que quedó abierto (para Matías, antes de mandar)

1. **Los números, recalculados hacia abajo:** doble de interior **USD 750 × 2 = 1.500** · doble de exterior **USD 765 × 1** (750 + los USD 15 reales de la caja Roker) · repuesto **400** · puesta en marcha **1.450** (58 h) · **inicial 4.115** (era 4.600, **−485**) · abono **500/mes, sin tocar** · B = **9.515**. Márgenes: **23 % los equipos** (bajaron: la plataforma se reparte entre 3 y la caja de interior real cuesta $ 21.203, no $ 8.500), **76 % el abono**. **¿Van?**
2. **Si querés un número redondo para la OC: 4.100.** Se llega poniendo **los tres módulos a 750** y dejando que el de exterior absorba los USD 15 de la caja (margen 174 → 159 en ese módulo). Queda 50 % = **2.050**, B = **9.500**, 12 meses = **10.100**. **No lo recomiendo por sobre el 765** —el 765 explica solo por qué el de afuera cuesta más— pero **es la única alternativa que NO implica inflar nada**, y es tu decisión.
3. **Lo que NO se hizo, y quiero que conste:** no se subieron los unitarios ni el repuesto para sostener el 4.600. Se podía y nadie lo iba a auditar. **Menos equipos = menos plata, dicho en voz alta, es lo que hace creíble el 500/mes** — y el abono es el negocio (§3.4).
4. **RIESGO NUEVO Y EL MÁS IMPORTANTE: el firmware de módulo doble ahora es crítico para los TRES módulos.** Se acabó el colchón de la v6.1 (los 2 simples corrían lo que ya anda). Estado verificado: **escrito y auditado**, `C:\Proyectos\frioseguro-v31\firmware_modular\VERIFICACION_V3.1_2026-09-04.md`, **APTO CON CORRECCIONES**, correcciones en curso. **Sin ese firmware cerrado no reporta ni un reefer y el hito 2 cae entero.** @firmware tiene que confirmar (a) que las correcciones cierran antes de la semana 2 y (b) que las 10 h de §3.2 alcanzan. Si son más horas, **salen del margen, no del precio**.
5. **El cable: ahora son 3 tiradas y una es a la intemperie.** En el documento del cliente **no va nada más que la nota al pie** *"No incluye cable ni tendido entre reefers"* (tu decisión). **Interno:** el tramo de afuera tiene que ser par trenzado **apto exterior**, sin empalmes, canalizado. Si Andrés pregunta qué comprar, se le dice.
6. **El sexto reefer entra a USD 260** (canal libre del módulo de su par, sin equipo nuevo) **+ USD 100/mes**. Está escrito en el documento del cliente. **¿Va así?**
7. **Riesgo de los tres buses de 20-25 m: asumido con conocimiento** (§2.2). Mitigación: pull-up 2k2 con opción a 1k (@esquematico), **prueba de banco con 25 m en los tres módulos**. **Confirmar con @esquematico que la posición del 1k queda en la placa.**
8. **Compra de materiales: ≈ $ 355.000 ($ 375.000 con flete ≈ USD 244)** — §3.7. **−$ 55.000 contra la v6.1**, y eso **ya con la caja de exterior real a $ 44.419** (la v6.1 la había presupuestado a ~$ 22.000; la corrigió @hardware el 4-sep). Reservados 3 ESP32 para las galgas de Dreyfus (P0 de octubre).
9. **`M9` de @hardware vale $ 63.609:** medir con calibre el interior de las 3 cajas de stock. Si entran los 3 dobles de interior, no se compra ni un gabinete de interior. **5 minutos, antes del pedido.**
10. **@hardware: contar stock y hacer las mediciones del §8.1 del BOM** (amperaje real de las fuentes, relé con IN al aire) antes de comprar.
11. **DECISIÓN DE PORTFOLIO, no comercial:** los kits siguen siendo los mismos que iban a ser las demos de Bahía, pero ahora son **4 y no 5**. Recomendación: reposición en el mismo pedido que la OC. **Decide el Director.**
12. **Preguntarle a Andrés cuál de los 4 de adentro está fuera de servicio** (§5.2 punto 3): es lo único que todavía puede cambiar el armado. Y de paso, **cuántos metros hay entre los dos de afuera**.
13. **Verificación cruzada entre sondas: hoy NO existe.** Vendida en el hito 2. Si no se puede cumplir, sacar el punto 3 del bloque "por qué 3 sondas".
14. **Accionamiento del relé desde el panel: tampoco existe.** Hito 5.
15. **El sensor de puerta viene deshabilitado por defecto** (`SENSOR_DOOR_ENABLED false`): que quede en la orden de armado habilitarlo y probar **las dos** puertas de **cada uno de los tres** módulos.
16. **Cobertura de red en los 3 puntos** (§5.2). Si alguno queda corto, repetidor **antes** de despachar.
17. **La caja de exterior que ya está en el sitio es la prueba de campo** (§2.5 punto 6) y ahora de ella dependen **2 reefers**: pedirle a Andrés una foto después del primer temporal.
18. **Andrés:** opción 1, 2 o 3 de la Parte 7, y preguntarle para quién trabaja.
19. **PDF:** @diseno maqueta **un solo** documento de 2 páginas A4, marca Termovigía, sin logo ajeno, sin "Para:", sin validez. **Sin mencionar material de gabinete ni impresión 3D.** Archivo `PRESUPUESTO_CERRO_MORO.pdf` (+ `PRESUPUESTO_CERRO_MORO_INTERNO.pdf`).
20. Monotributo vs. RI: se pregunta cuando la empresa tenga nombre.
