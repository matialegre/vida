# PROPUESTA — Monitoreo de temperatura de los reefers del campamento Cerro Moro (Santa Cruz)

> @comercial · **v9.0, 2026-09-08** · **UN SOLO presupuesto: 3 módulos dobles, uno por cada par de reefers, con la caja sobre la unión**
> **Configuración cambiada por Andrés el 8-sep por WhatsApp:** *"con tres módulos solucionamos lo de Cerro Moro, un módulo para dos reefer; al estar juntos de a dos es fácil hacer la conexión; pongo la caja sobre la unión de los dos y saco las sondas".* Matías aceptó, **mantiene 3 sondas por reefer** (*"3 es mucho mejor para calibración"* — y Andrés **midió casi 3 °C entre la puerta y el fondo** de un reefer) y le dijo: *"rehago el presupuesto, queda más o menos lo mismo, porque le tengo que meter un poco más de electrónica adentro de la caja y programación".*
> - **3 módulos dobles**: 1 de **exterior** estanco IP65 (los 2 de la intemperie) + 2 de **interior** (los 4 bajo techo, de a dos). **Uno de los 4 está fuera de servicio y ya queda cubierto por su módulo, con sus sondas incluidas.**
> - **Por módulo: 6 sondas, 2 puertas, 2 defrost, 2 relés.** A cada reefer le llega **un solo cable de 3 hilos** desde el módulo y las 3 sondas se reparten adentro (puerta, medio, fondo) — no 9 hilos.
> - **Repuesto: 1 módulo doble completo** (6 sondas + 2 reed), reemplaza a cualquiera de los tres.
> - **Precio: inicial USD 4.800** — doble de interior **900 × 2** + doble de exterior **950** + repuesto **400** + puesta en marcha **1.650** (66 h). **Margen parejo ~32 % en los tres ítems, el mismo criterio de la v8.0.** Baja 200 sobre los 5.000 de la v8.0 (−4 %): *"más o menos lo mismo"*, y se dice así — menos cajas, pero cada una lleva más electrónica y más programación. **Abono INTACTO: USD 100 por reefer/mes = 500/mes.** B anual **10.200**. Anticipo 50 % **2.400**.
> - **Sexto reefer: sin costo de equipo** (antes USD 260). Sólo el abono pasa de 500 a 600. Se dice como ventaja.
> - **Fecha 8-sep-2026, ref `PROP-CM-2026-09-08`, BNA vendedor billete $ 1.530 (bna.com.ar, 8-sep 09:50).**
> - **Reglas fijas de Matías, verificadas sobre el texto del PDF:** nunca "Ing.", sin "en funcionamiento", sin "instalado en", sin nombrar a Panamerican, firma como está.
> **Generadores:** `comercial/panamerican/armar_cliente_v7.py` (dict `PRECIOS` = única fuente de verdad + `calcular()`; la cuenta del margen está en su docstring), `armar_interno_v7.py`, `render_v7.py` (guarda de frases prohibidas ampliada con TODA la configuración vieja: "5 módulos", "cinco", "simples", "USD 260", 5.000, 10.400, 1.550, 700, 1.535, 4-sep…). Verificación independiente del PDF contra `calcular()`: **TODO OK** (8-sep).
> **Historial:** v9.0 (8-sep, 3 dobles, 4.800) ← v8.0 (4-sep 15:23, 1 doble ext + 4 simples int, 5.000) ← v7.0 (4-sep, 3 dobles, 4.115) ← v6.1 (4-sep, 2 simples ext + 2 dobles int, 4.600; **es el PDF que Andrés recibió a las 14:01**) ← v5 (4-sep, 5 simples, 4.540 + cuenta del caño) ← v4/v3/v2/v1. Las versiones anteriores están íntegras en el historial de git de este archivo.
> **Se mantiene de la v8.0:** margen parejo, hitos relativos desde "aceptación + anticipo", 50/50, formas A y B, sin validez, sin destinatario, sin material de gabinete ni impresión 3D, firma con UTN/GIMAP/Montagne, USD con pago en pesos al BNA de la fecha de pago.
> **Matías decide el número final, siempre.** Todo monto de acá abajo es propuesta con la cuenta a la vista.
> Doctrina: `PLATA.md`. Base técnica: `ALCANCE_1WIRE.md` (@muestreador), **`BOM_CERRO_MORO.md` rev A (@hardware, 4-sep)**, `BOM_MINI.md` y **`PINOUT_MINI.md`** (@esquematico — un bus 1-Wire en GPIO 4 y **GPIO 18/23 reservados para un 2.º bus**), `ESTADO_HONESTO.md`, firmware `firmware_revival` leído el 3-sep, auditoría del firmware doble `VERIFICACION_V3.1_2026-09-04.md` (APTO CON CORRECCIONES).
> **El comprador NO es Pan American Silver:** es "una empresa" que Andrés todavía no identifica. El documento del cliente va **sin destinatario, sin logo ajeno y sin nombrar a Panamerican**. El archivo conserva el nombre por historial.

## Qué cambió en esta versión

**1. Tres módulos dobles, uno por par, con la caja sobre la unión. Lo armó Andrés con la caja en la mano.** Los 6 reefers están de a dos: 2 afuera y 4 adentro en dos pares. *"Pongo la caja sobre la unión de los dos y saco las sondas."* Es la configuración con **menos cable de todas las versiones**: cero entre contenedores, seis tiradas cortas de la unión a cada reefer. **3 puntos de red** en vez de 5.

**2. Un solo cable de 3 hilos por reefer, tres sondas adentro.** Matías mantuvo las 3 sondas (*"3 es mucho mejor para calibración"*) y el argumento ahora tiene **dato del sitio**: Andrés midió **casi 3 °C entre la puerta y el fondo**. Con una sonda, ese reefer miente. Las tres van por un solo cable y se reparten adentro: puerta, medio, fondo.

**3. El sexto reefer entra sin costo de equipo.** El doble de su par ya trae sus 3 sondas, su reed y su defrost. Antes eran USD 260; ahora es conectar y subir el abono a 600. **Se dice como ventaja en el PDF** (§05 Ampliación).

**4. USD 4.800, con el mismo margen parejo (~32 %) de la v8.0.** Matías le dijo a Andrés *"queda más o menos lo mismo"*, y la cuenta lo sostiene sola: dos cajas menos, pero cada doble lleva **más electrónica** (2.º bus 1-Wire con su protección, 2.ª entrada de defrost, borneras y prensacables ×2: +8), **la plataforma se reparte entre 3 y no entre 5** (333 c/u en vez de 200), **dos buses a probar en banco** (+10 de armado), y la puesta en marcha suma **8 h de software** para repartir por reefer (−4 h por 3 altas en vez de 5). Interior **900**, exterior **950**, repuesto **400**, puesta en marcha **1.650** → **4.800**. **−200 (−4 %)**. Cuenta completa en §3.1. **Alternativa para sostener 5.000** (36 %, desparejo) en §3.1, no recomendada.

**5. El abono NO se toca: 500/mes.** Por reefer vigilado, no por caja. Y esta vez la regla juega al revés y también sirve: si preguntan "¿con menos equipos no baja el mensual?", la respuesta está escrita desde la v2.

**6. El riesgo que VOLVIÓ: el firmware doble es crítico para los tres módulos** (como en la v7.0; en la v8.0 había salido del camino crítico porque los simples corrían lo que ya anda). Sin él no reporta ningún módulo nuevo. Estado: APTO CON CORRECCIONES, sin fecha de cierre. Plan B parcial: cada doble arranca vigilando un solo reefer (3 de 5). **Hay que decírselo al Director.** Y **una caja sin energía deja dos reefers sin vigilancia, siempre**: para eso el repuesto, y así está escrito en "Lo que hay que saber".

**7. Decisión de placa antes de pedir la PCB: poblar el 2.º bus 1-Wire de la Mini** (GPIO 18, pines ya reservados en `PINOUT_MINI.md`), sin el TVS D2 que rompe el bus a 25 m. Con **un bus por reefer** el reparto de sondas es por pin, el defrost de un reefer no puede callar al otro por diseño y una sonda en corto no tumba las del vecino. Es la "más electrónica" que Matías le dijo a Andrés. **Después de JLCPCB ya no se cambia.**

**8. Cuarta vuelta de configuración no hay.** Tres presupuestos en cuatro días es el límite: la próxima conversación con Andrés es de aceptación, no de configuración.

---

## PARTE 1 — Documento del cliente (2 páginas A4, generado por `armar_cliente_v7.py`)

> Copiar de acá hasta la línea de corte. Nada más. Escrito para que **lo presente alguien que no es vendedor** y se lea en dos minutos.

**Termovigía — Monitoreo de temperatura de reefers**
**Campamento Cerro Moro (Santa Cruz) — 5 reefers en servicio**
**Tres módulos, uno por cada par de reefers** — 1 módulo estanco de exterior + 2 módulos de interior, cada uno para dos reefers que están juntos. Presupuesto del 8 de septiembre de 2026, ref. PROP-CM-2026-09-08.

**Qué es.** Un sistema que mide la temperatura de cada reefer las 24 horas y avisa al celular cuando algo se sale de rango. Por cada reefer, siempre lo mismo: **3 sondas, 1 sensor de puerta y 1 señal de defrost**, y **un solo cable de 3 hilos** desde el módulo hasta el reefer. Hoy ya hay un equipo instalado y reportando desde el campamento. **Mientras se evalúa esta propuesta ese equipo sigue midiendo y reportando**, y el panel se puede abrir en el celular en cualquier momento: los resultados se ven durante el proceso, no después.

**Qué módulo va en cada reefer.**

| Dónde está el reefer | Qué le va | Qué lleva cada reefer | Equipos |
|---|---|---|---|
| **2** a la intemperie, juntos | **Un módulo para los dos**, en gabinete **estanco IP65 apto para exterior**, montado sobre la unión de los dos contenedores. Comparten módulo porque están pegados: a cada reefer le llega un solo cable, corto, desde la caja. | 3 sondas · 1 sensor de puerta · 1 señal de defrost · 1 cable de 3 hilos | **1 módulo** de exterior, para 2 reefers |
| **4** bajo techo, de a dos | **Un módulo por cada par**, en gabinete de interior, montado sobre la unión de los dos. Están de a dos, así que cada par comparte un módulo. Uno de los 4 está hoy fuera de servicio: **su módulo y sus sondas ya quedan incluidos**. | 3 sondas · 1 sensor de puerta · 1 señal de defrost · 1 cable de 3 hilos | **2 módulos** de interior, para 2 reefers cada uno |

**Total: 3 módulos para los 6 reefers** — **5 en servicio hoy** y el sexto ya cubierto por el módulo que comparte con su vecino.

**Qué hace.**
- Mide la temperatura de cada reefer todo el tiempo, con **3 sondas por reefer**, y la guarda en la nube (12 meses de historial).
- Avisa al celular de quien se defina cuando un reefer se sale del rango acordado, por más tiempo del acordado.
- Avisa si **queda la puerta abierta** más de los minutos que se definan (sensor magnético en cada reefer).
- Avisa cuando una sonda se desconecta o cuando un módulo deja de reportar.
- **No molesta durante el descongelamiento:** toma la señal de defrost de cada reefer y calla las alarmas **de ese reefer solamente** —el que comparte módulo sigue vigilado— para que nadie aprenda a ignorar los avisos.
- Puede **accionar una sirena o baliza**: cada módulo trae 2 salidas a relé libres para eso.
- Genera solo el **registro mensual de temperatura por reefer**, para tener el papel cuando alguien lo pide.
- Funciona con la red de internet que ya hay en el campamento: no hay que contratar nada más.

**Por qué 3 sondas por reefer y no una.** Es la diferencia entre una instalación seria y un termómetro con WiFi.
1. **Un reefer no tiene "una" temperatura.** En uno de los reefers del campamento ya se midió **casi 3 °C de diferencia entre la puerta y el fondo**. Con una sonda se mide un punto y se supone el resto; con tres —puerta, medio y fondo— se mide **el peor punto**, que es el que decide si la carga se arruinó y el que vale en una auditoría, no el promedio.
2. **Si una sonda falla, el reefer sigue vigilado.** En un sistema cuyo trabajo es avisar, quedarse ciego es la peor falla posible: con una sola sonda, cualquier problema deja el reefer sin vigilancia hasta que alguien viaje 1.500 km. Con tres, se pierde una y quedan dos.
3. **Las sondas se controlan entre sí.** Tres es el mínimo que permite saber **cuál** se desvió: si una se aparta de las otras dos, se detecta y se avisa. Con una sola sonda, una deriva de 2 o 3 °C es invisible: el registro parece perfecto y está mintiendo. *(Se entrega en el hito 2.)*
4. **Se calibran las tres contra la misma referencia** (baño de hielo) y las diferencias quedan registradas: eso es lo que hace defendible el registro ante un auditor. Y las tres van por **un solo cable de 3 hilos**: se reparten adentro del reefer, no hay que pasar nueve.

**Cada módulo se prueba con el cable real antes de viajar.** Los equipos **se arman y se verifican uno por uno en banco de prueba** —las 6 sondas leyendo, las dos puertas, las dos señales de defrost y las salidas de alarma—, y **cada salida a reefer se prueba con 25 metros de cable antes de despachar**, más de lo que va a haber en el sitio. Para un lote que va a quedar a 1.500 km, esa verificación es la diferencia entre uno que llega andando y uno que hay que diagnosticar por teléfono.

**Ampliación. El sexto reefer, sin costo de equipo.** El reefer que hoy está fuera de servicio comparte módulo con su vecino, y ese módulo **ya trae sus 3 sondas, su sensor de puerta y su entrada de defrost**. Cuando vuelva **no hay que comprar ningún equipo ni tocar nada de lo instalado**: se le conectan y el servicio mensual pasa de USD 500 a USD 600. Queda dicho acá para no renegociar nada el día que pase.

**Puesta en marcha y ajuste en sitio (15 semanas, por hitos, incluidos en el precio).** **Los plazos se cuentan desde el inicio, y el inicio es la aceptación de esta propuesta con su anticipo.**

| Hito | Qué queda funcionando · cómo se comprueba | Plazo |
|---|---|---|
| 1 | El equipo ya instalado, con sus 3 sondas dentro del reefer, calibradas contra una misma referencia, rangos definidos y primera alerta real en el celular. *Se acepta con:* captura de la alerta en el celular, el registro en la nube y la planilla de calibración de las 3 sondas. | a las 2 semanas de iniciado |
| 2 | Los 3 módulos montados y los 5 reefers reportando; nada se pierde si se corta la red; aviso de módulo mudo y **de sonda que se desvía de las otras del mismo reefer**; puertas y defrost validados; una semana sin falsas alarmas. *Se acepta con:* desenchufar una sonda y que llegue la alarma; cortar la red 20 minutos sin perder lecturas; abrir una puerta 4 minutos y que avise; **forzar el defrost de un reefer y que el que comparte módulo siga alarmando**. | a las 5 semanas |
| 3 | Acceso seguro: cada módulo y cada usuario con su propia credencial. *Se acepta con:* con una credencial dada de baja ya no se puede escribir, y todos los módulos siguen reportando. | a las 10 semanas |
| 4 | Actualizaciones de los equipos a distancia, sin tocarlos. *Se acepta con:* tres actualizaciones seguidas por aire, al primer intento, en todos los módulos. | a las 12 semanas |
| 5 | Panel para la empresa (usuarios de solo lectura), accionamiento de las salidas de alarma e informe mensual descargable. *Se acepta con:* un usuario de la empresa entra solo, baja el informe y acciona una salida desde el panel. | a las 15 semanas |

**Qué cuesta.**

| Concepto | Unid. | USD |
|---|---|---|
| Módulo de exterior para los dos reefers que están juntos a la intemperie (gabinete estanco IP65 apto para exterior, fuente, 2 relés, y por cada reefer 3 sondas + puerta + defrost por un solo cable; probado en banco con 25 m) | 1 | 950 |
| Módulo de interior para dos reefers que están juntos bajo techo (gabinete, fuente, 2 relés, y por cada reefer 3 sondas + puerta + defrost por un solo cable; probado en banco con 25 m) — 2 × 900 | 2 | 1.800 |
| Kit de repuestos en sitio (1 módulo completo, con sus 6 sondas y 2 sensores de puerta, que reemplaza a cualquiera de los tres) | 1 | 400 |
| Puesta en marcha y ajuste en sitio (los 5 hitos de arriba, con su plazo; incluidos en el precio, no se facturan aparte; el montaje lo hace personal del campamento con los equipos preconfigurados y guía por videollamada: no hay línea de instalación ni viáticos) | 5 hitos | 1.650 |
| **Total equipos y puesta en marcha** | | **4.800** |
| **Servicio mensual** — USD 100 por reefer por mes, 5 reefers en servicio: nube, alertas, soporte, reposición sin cargo, informe mensual | | **500 / mes** |

*No incluye cable ni tendido.*

**Cómo se paga.**

| | **A. Equipos + servicio mensual** | **B. Anual adelantado** |
|---|---|---|
| Pago inicial | USD 4.800 (50 % con la OC, 50 % contra instalación) | USD 10.200 (equipos + 12 meses de servicio, con 10 % de descuento sobre el servicio) |
| Mensual | USD 500 — USD 100 por reefer, completo desde el primer mes | — el primer año; renovación anual USD 5.400 |
| Los equipos | Son del cliente en las dos formas | |
| **Total a 12 meses** | **10.800** | **10.200** |
| **Total a 24 meses** | **16.800** | **15.600** |

Facturación en dólares estadounidenses. De abonarse en pesos, se toma el tipo de cambio vendedor del Banco de la Nación Argentina de la fecha de pago. *Ref. al 8-sep-2026 (BNA vendedor $ 1.530): USD 4.800 ≈ $ 7.344.000 · USD 500 ≈ $ 765.000 · USD 10.200 ≈ $ 15.606.000.*

**Incluido en el servicio mensual:** nube con 12 meses de historial · alertas por temperatura, puerta abierta, sonda caída y equipo mudo · reposición sin cargo de cualquier módulo o sonda fallada, envío incluido · actualizaciones · soporte por WhatsApp y teléfono el mismo día hábil · informe mensual por reefer.

**Lo que hay que saber.** El sistema avisa; no garantiza la mercadería ni reemplaza la revisión del reefer. Sin energía en el módulo no mide: lo que avisa en ese caso es la nube, diciendo que dejó de reportar. La entrada de defrost necesita una señal o un contacto accesible; si algún reefer no lo tiene, esa entrada queda libre y el resto funciona igual. Las 2 salidas a relé vienen en el módulo; la sirena o baliza que se conecte no está incluida. Cada módulo necesita llegar a la red del campamento. El tendido del cable de cada reefer al módulo lo hace el cliente. Si un módulo se queda sin energía quedan **sus dos** reefers sin vigilancia: para eso está el módulo de repuesto en el campamento. Los plazos de los hitos 1 y 2 suponen que el montaje en sitio se hace dentro de la ventana prevista, que depende de personal del campamento.

*Se puede ver en vivo antes de decidir. Contacto en sitio: Andrés Leiva Chavez · Matías Alegre — Ingeniería Electrónica, UTN Facultad Regional Bahía Blanca · Grupo de investigación GIMAP · Encargado de proyectos de sistemas — Montagne · Mundo Outdoor · Termovigía, Bahía Blanca · 2920 59-1019 · alegrematias08@gmail.com · termovigia.vercel.app*

— — — — — — — — — — corte: lo de abajo NO se manda — — — — — — — — — —


## PARTE 2 — Alcance (interno)

### 2.1 Qué hay hoy, verificado

| Hecho | Evidencia |
|---|---|
| 1 equipo instalado en el campamento, `REEFER_01_SCZ`, firmware `firmware_revival` 2.6.21 | Puesto el 21-ago; reconectado por Andrés el 3-sep |
| Reportando cada ~5 s, **con 1 sola sonda y FUERA del reefer** — mide ambiente | Base de Santa Cruz, 3-sep; Andrés espera confirmación para meterlas |
| **Sin contrato y sin un peso cobrado** | `PLATA.md` |
| "Acá no pueden haber cables aéreos" | Andrés, WhatsApp 3-sep 17:11 |
| **2 reefers a la intemperie y JUNTOS; 4 adentro, bajo techo, también de a dos** | Andrés, 4-sep y **8-sep** |
| **De los 4 de adentro, uno está fuera de servicio: hoy hay 5 reefers activos** | Matías, 4-sep |
| Ya se mandó al sitio una **caja estanca IP65 apta para exterior** | Matías, 4-sep |
| **CONFIGURACIÓN v9 — Andrés: *"con tres módulos solucionamos lo de Cerro Moro, un módulo para dos reefer; al estar juntos de a dos es fácil hacer la conexión; pongo la caja sobre la unión de los dos y saco las sondas"*** | WhatsApp, **8-sep**. Es el dato que fija esta versión |
| **Andrés midió casi 3 °C de diferencia entre la puerta y el fondo de un reefer** | WhatsApp, 8-sep. **Argumento de las 3 sondas, con dato del sitio** |
| **Matías: 3 sondas por reefer se mantienen (*"3 es mucho mejor para calibración"*); *"rehago el presupuesto, queda más o menos lo mismo, porque le tengo que meter un poco más de electrónica adentro de la caja y programación"*** | WhatsApp, 8-sep. Fija el precio objetivo |
| Andrés tiene en el celular un presupuesto anterior (v6.1 de 4.600 del 4-sep 14:01 seguro; la v8.0 de 5.000 si se mandó el 5-sep) | Condiciona el WhatsApp de §6.1: *"reemplaza al anterior"*, sin cifra vieja |
| **La placa Mini tiene UN bus 1-Wire (GPIO 4, hasta 6 sondas) y deja GPIO 18/23 reservados para un 2.º bus** | `PINOUT_MINI.md` filas 4 y "libres". Es la "más electrónica" de esta versión |
| **Firmware de módulo doble: escrito y en auditoría, veredicto APTO CON CORRECCIONES** | `C:\Proyectos\frioseguro-v31\firmware_modular\VERIFICACION_V3.1_2026-09-04.md` — correcciones en curso |

### 2.2 Qué módulo va en cada reefer

| Ubicación | Reefers | Módulos | Gabinete | Por módulo |
|---|---:|---|---|---|
| **Intemperie** (los 2 están juntos) | 2 | **1 doble** | **IP65 estanco de exterior** (Roker PRG357, $ 44.419) — ya hay una en el sitio | 6 sondas, 2 puertas, 2 defrost, 2 relés · un cable de 3 hilos a cada reefer |
| **Bajo techo, de a dos** (uno de los 4 fuera de servicio) | 4 | **2 dobles**, uno por par | interior (Genrod IP65 210×310×110, $ 21.203) | ídem · el par con el reefer parado arranca con 3 sondas conectadas y 3 en espera |
| Repuesto en el campamento | — | **1 doble** | interior | completo, con 6 sondas y 2 reed: reemplaza a cualquiera de los 3 |
| **Total** | **6** | **3 instalados + 1 repuesto** | | 4 placas Mini idénticas, las 4 con el 2.º bus poblado |

> Las v4 y v5 discutieron si convenía un equipo por reefer o uno cada dos; la v7.0 se fue al "uno cada dos"; la v8.0 volvió a "uno por reefer adentro". **El 8-sep Andrés la cerró desde el sitio, con la caja en la mano: los seis están de a dos, y la caja va sobre la unión de cada par.**

**La regla que quedó, en una frase:** *un módulo por cada par de reefers pegados, montado sobre la unión, con un cable de 3 hilos a cada reefer.* Es la que dijo el sitio, no la que dedujimos nosotros. Y es la que **menos cable** tiene de todas las versiones.

**Qué se gana:**
- **3 puntos de red** en vez de 5 (era el riesgo que más había subido en la v8.0).
- **Ningún cable entre contenedores**: la caja está sobre la unión y cada reefer recibe el suyo, corto.
- **Dos cajas menos** que comprar, armar, probar y despachar: 4 bultos en vez de 6.
- **Un solo diseño de módulo** para los cuatro (3 + repuesto): un firmware, un stock, un runbook.
- **El sexto reefer entra gratis**, porque el doble de su par ya trae sus sondas.
- El argumento de las 3 sondas ahora tiene **dato del sitio**: casi 3 °C entre puerta y fondo.

**Qué se pierde, y hay que tenerlo escrito:**
- **El firmware doble vuelve a ser crítico para los tres módulos** (§2.5 punto 1). En la v8.0 los simples corrían lo que ya anda; acá no hay simples.
- **Un módulo sin energía deja dos reefers sin vigilancia, siempre.** Mitigación real y cotizada: el repuesto en el campamento y el aviso de equipo mudo desde la nube.
- **La plataforma se reparte entre 3 módulos** (USD 333 c/u en vez de 200): es la mitad de por qué un doble cuesta 900 y no 700.
- **Hay una decisión de placa antes de pedir la PCB**: poblar el 2.º bus (§2.3).

**El riesgo del bus, ahora repartido en seis tiradas cortas.** El límite prudente que fijó @muestreador es **15 m** (`ALCANCE_1WIRE.md`); con la caja sobre la unión, cada tirada es del gabinete a la sonda más lejana de un reefer: unos metros. Lo que sí queda: **cada módulo ata por el hilo de masa dos contenedores metálicos con puesta a tierra separada** (§2.6 de ALCANCE: *"el riesgo dominante de esta instalación"*). Con **un bus por reefer** (2.º bus en GPIO 18) los dos reefers no comparten hilo de datos, el defrost de uno no puede callar al otro por diseño y una sonda en corto en un reefer no tumba las del vecino. **Matías conoce el dato y acepta el riesgo.** Mitigaciones:
- **Un bus 1-Wire por reefer**: poblar el 2.º bus de la Mini (pull-up 2k2 con alternativa 1k, 100 Ω serie, clamps; **sin el TVS D2 que @hardware demostró que rompe el bus a 25 m**, `BOM_CERRO_MORO.md` §5.1). A definir con @esquematico **antes de mandar la PCB a JLCPCB**.
- **Las 8 salidas a reefer (4 módulos × 2) se prueban en banco con 25 m de cable real antes de despachar**, con sus 3 sondas colgadas cada una.
- **Especificación de cable** (3 hilos, el par DQ/GND junto, sin empalmes, apto exterior para el par de afuera): **queda interna**. Si Andrés pregunta qué comprar, se le dice.
- Sondas sujetas con aislación respecto de la chapa; defrost por optoacoplador; reed es contacto seco.

**Lo que NO se le dice al cliente:** que esto es un riesgo. En el documento van *"No incluye cable ni tendido"* y *"El tendido del cable de cada reefer al módulo lo hace el cliente"*, y nada más. **Y el tendido no se cotiza** (*"no contemples el tema de las tiradas"*): la cuenta del caño queda archivada en §3.3 como historia y como argumento.

### 2.3 Qué lleva cada módulo, y qué de eso anda HOY (verificado en el código el 3-sep)

**Los cuatro módulos (3 + repuesto) son la misma placa Mini, poblada entera y con el 2.º bus.** Ya no hay "simple": lo que corre hoy en `REEFER_01_SCZ` sirve para el hito 1 y como plan B parcial, no para el pedido.

| Función | Doble (×3 + rep.) | Qué hace el firmware hoy | Evidencia |
|---|---|---|---|
| Sondas DS18B20 | **6** (3 + 3) | Cada una identificada por ROM de 64 bits y reportada por separado; enganche en caliente; aviso si se desconecta; **offset de calibración por sonda en NVS**. `SONDAS_MAX` está en 4: **hay que subirlo a 8 y asignar cada ROM a su reefer** — con un bus por reefer la asignación es por pin, no por tabla | `sondas.h`: `sondasEscanear`, `sondasLeer`, `sondasCalibrar`; línea 31 · `PINOUT_MINI.md` GPIO 4 / 18 |
| **Verificación cruzada entre sondas** | — | **NO existe.** `sondasCalibrar()` iguala las sondas en un momento dado; el lazo de lectura **no compara sondas entre sí** ni alerta por deriva. Con 3 °C reales entre puerta y fondo, la comparación tiene que ser **contra la propia historia de cada sonda**, no contra el promedio del reefer | ídem. Vendida en el **hito 2** |
| Sensor de puerta | **2** | Implementado **para una sola puerta**: GPIO5, alerta > 180 s, suprime la alerta de temperatura mientras está abierta. Deshabilitado por defecto (`SENSOR_DOOR_ENABLED false`). **La segunda puerta hace falta en los tres** | `config.h` 72-74, 105, 119 · `.ino` 804-890 |
| Entrada de defrost | **2** | Implementada **para una sola entrada**: GPIO33, NA/NC, deshabilita alertas durante el ciclo con 30 min de enfriamiento. **La segunda hace falta en los tres, y tiene que silenciar sólo el reefer que descongela** — es la prueba de aceptación del hito 2 | `config.h` 91-96, 122 · `.ino` 54-55, 100-101, 872-878 |
| Salidas a relé | 2 | **1 gobernada**: GPIO26, se activa sola con la alerta si `relayEnabled`. La segunda queda cableada y disponible. **El accionamiento manual desde el panel NO existe** | `config.h` 76-77, 140-150 · `.ino` 369-375, 483-488, 915-944 · `comandos_nube.h` sin comando de relé → **hito 5** |
| Gabinete | 1 | Interior: Genrod IP65 210×310×110, $ 21.203 (×2 + repuesto). Exterior: Roker PRG357 IP65 200×200×155, $ 44.419 (×1, ya en el sitio) | `BOM_CERRO_MORO.md` §3 |

**Regla de venta.** Lo que **no** está andando hoy y va vendido con hito, nunca como característica de hoy:
- **Segunda puerta, segundo defrost por reefer, `SONDAS_MAX` a 8, reparto de sondas por reefer (un bus por reefer) y panel que muestra dos reefers por módulo** — el software del módulo doble. Costeado (18 h, §3.2), hito 2. **Lo necesitan los tres módulos y el repuesto.**
- **Verificación cruzada entre sondas** — hito 2.
- **Accionamiento manual del relé desde el panel** — hito 5.

**⚠ El riesgo que VOLVIÓ: sin firmware doble no reporta ningún módulo nuevo.** Como en la v7.0. Estado real: **APTO CON CORRECCIONES** (auditoría 4-sep), correcciones en curso, **sin fecha de cierre confirmada por @firmware**. Lo que lo hace tolerable: el hito 1 no depende de él (es `REEFER_01_SCZ` con lo que ya anda + 2 sondas), y si se atrasa hay un plan B parcial: **cada doble arranca vigilando un solo reefer con el firmware actual** (3 de 5) mientras se cierra. **No se vende como cosa hecha: se vende en el hito 2, como siempre. Y esto hay que decírselo al Director: volvió al camino crítico de la venta.**

**Orden de armado:** identificación por ROM sí o sí. **Un bus por reefer** (GPIO 4 y 18), cada uno con pull-up 2k2 y alternativa 1k, 3 hilos, 100 nF + 10 µF al pie de la sonda más lejana, **sin D2**. **Cuál de las dos líneas se despacha — `firmware_revival` extendido o `firmware_modular` v3.1 — lo define @firmware** cuando cierren las correcciones; **esta vez la decisión bloquea a los tres.** Habilitar `SENSOR_DOOR_ENABLED`, probar puerta y defrost de **los dos canales de los 4 módulos**, y correr la prueba de banco con 25 m en las 8 salidas antes de despachar.

### 2.4 Lo que se instala, y quién

**Módulo doble de exterior (×1, USD 950):** gabinete estanco IP65 apto para exterior (Roker PRG357 200×200×155), fuente de 5 V 2 A, placa Mini con borneras a tornillo y **2 buses 1-Wire**, ESP32 en zócalo, módulo de 2 relés, **prensacables en todas las entradas**, 6 sondas DS18B20 estancas, 2 reed de puerta, 2 entradas de defrost — para el par de afuera, montado sobre la unión.
**Módulo doble de interior (×2, USD 900):** uno por cada par bajo techo. Gabinete IP65 de interior (Genrod 210×310×110 o las de stock si pasan la medición `M9`), **la misma placa**, 6 sondas, 2 reed, 2 defrost. El par con el reefer parado arranca con 3 sondas puestas y 3 en espera, ya calibradas.
**Kit de repuesto (×1, USD 400):** un **módulo doble completo** — la placa es la misma en los cuatro, así que **cubre a cualquiera** — con 6 sondas y 2 reed. Va con gabinete de interior: **si el que falla es el de afuera, la electrónica se pasa a la caja estanca que ya está en sitio** (queda escrito en el runbook).
**El cable no lo mandamos** (decisión del 4-sep): son seis tiradas cortas de la unión a cada reefer, y las hace el cliente.
**Qué pasa con `REEFER_01_SCZ`:** cumple el hito 1 con sus 3 sondas; en el hito 2 su reefer pasa al doble de su par, **sus 3 sondas ya calibradas se reaprovechan** y el kit viejo queda en el campamento como segundo respaldo o vuelve a Bahía (decide Matías, pendiente 7).

**Montaje: Andrés (o quien la empresa designe), con kit preconfigurado y probado en banco + videollamada.** Dos pasajes a Santa Cruz, alojamiento, inducción y 5 días de ingeniero rondan los $ 2.500.000, y Matías no puede viajar en octubre (parada de Dreyfus). Eso es lo que esta propuesta no cobra.

**Intemperie: en el documento del cliente se dice "gabinete estanco IP65 apto para exterior" y nada más.** Ni material, ni proceso de fabricación, ni impresión 3D. Ni en el PDF ni en el WhatsApp.

### 2.5 Los riesgos técnicos abiertos

1. **⚠ EL QUE VOLVIÓ: el firmware doble es crítico para los tres módulos.** Como en la v7.0. APTO CON CORRECCIONES, en curso, sin fecha. Plan B parcial: cada doble arranca con un solo reefer (3 de 5). **@firmware tiene que dar fecha antes de que Matías prometa el hito 2 por teléfono.**
2. **Una caja sin energía = dos reefers ciegos, siempre.** Mitigación cotizada: repuesto en el campamento + aviso de equipo mudo. Está escrito en "Lo que hay que saber" del PDF, sin dramatizar.
3. **Decisión de placa: poblar el 2.º bus antes de pedir la PCB.** La Mini deja GPIO 18/23 reservados. Con un bus por reefer el reparto es por pin y el defrost cruzado es trivial; con un solo bus de 6 sondas hay que repartir por tabla de ROM y probar el bus a 6 sondas con dos ramas. **Lo define @esquematico con Matías esta semana; después de JLCPCB ya no.**
4. **✅ Cobertura de red: 3 puntos.** Mejor que los 5 de la v8.0 y que los 4 de la v6.1. Sigue siendo pregunta para Andrés antes de despachar.
5. **✅ Cable: seis tiradas cortas, ninguna entre contenedores.** Queda el cruce de masas entre los dos contenedores de cada par por el hilo de GND: un bus por reefer lo aísla en datos, no en masa. Riesgo asumido (§2.2).
6. **El defrost cruzado, ahora en los tres.** Es la prueba de aceptación del hito 2 (*"forzar el defrost de un reefer y que el que comparte módulo siga alarmando"*) y aplica a los 3 pares.
7. **La caja de exterior a la intemperie de Santa Cruz** es la única parte del equipo sin antecedente de campo largo, y de ella dependen 2 reefers. La que se mandó el 4-sep es la prueba de campo: pedirle a Andrés una foto tras el primer temporal.
8. **⚠ Plazo de fabricación — sigue siendo el cuello.** @hardware: con la PCB Mini el despacho realista es **semana 4-5, no 2**, y el hito 2 caería en la **7-8** (`BOM_CERRO_MORO.md` §7.2). Son 4 placas en vez de 6, pero el plazo lo pone JLCPCB + DHL, no la cantidad. En el documento del cliente los hitos quedan como están; **Matías resuelve con @hardware antes de firmar** (pedir la PCB ya, USD 43, sirve igual para las demos de Bahía).

**Resumen para el Director, en una línea:** contra la v8.0 **bajaron** la red (5 → 3 puntos), el cable (1 tirada larga → 6 cortas), las cajas (5 → 3) y el precio (−200); **subieron** el firmware doble (vuelve a bloquear a todos) y el alcance de una caída (siempre 2 reefers). El cuello de fabricación es el mismo. **Saldo: mejor negocio, mismo riesgo de plazo, un riesgo técnico más concentrado.**

### 2.6 Opcionales, después de la primera orden

**El sexto reefer cuando vuelva a servicio: sin costo de equipo, +USD 100/mes.** El doble de su par ya trae sus 3 sondas, su reed y su defrost. Es conectar y subir el abono de 500 a 600. Está escrito con ese precio (cero) en el documento del cliente: no hay que venderlo de nuevo, solo ejecutarlo. **Es el upsell más probable y de mejor margen de esta cuenta, y ahora no tiene fricción de compra.** · **Sirena o baliza: a USD 40 NO deja margen** — @hardware midió que la BR300 de exterior sale $ 39.530 (USD 26) **más su propia fuente de 12 V**, porque el relé entrega contacto seco (`BOM_CERRO_MORO.md` §4.5). **Propuesta: USD 70 instalada**, o baliza LED de 12 V. **Decide Matías.** · **Cuarta sonda** en un reefer (USD 40 + USD 5/mes) — con 3 °C entre puerta y fondo, puede pedirse sola · **base con batería y 4G**, la única que avisa el corte de energía por sí misma (a cotizar) — especialmente vendible para la caja de la intemperie, de la que dependen dos reefers. Se ofrecen cuando las sondas estén andando, no antes.

---

## PARTE 3 — Números de respaldo

Base: **`BOM_CERRO_MORO.md` rev A (@hardware, 4-sep)**, precios de MercadoLibre AR y JLCPCB verificados en vivo ese día. Cambio $ → USD al BNA vendedor **1.530 (8-sep)**: los mismos pesos dan los mismos dólares redondeados que al 1.535 de la v8.0.

### 3.1 Los tres precios, con el MISMO margen: interior 900 · exterior 950 · repuesto 400

| | Doble interior (ARS) | USD | Doble exterior (ARS) | USD |
|---|---:|---:|---:|---:|
| Electrónica: ESP32 + módulo de 2 relés + fuente 5 V 2 A + PCB Mini prorrateada + consumibles y prensacables **+ 2.º bus 1-Wire con su protección, 2.ª entrada de defrost, borneras y prensacables ×2** (30 de la v8 + ~8) | ~58.000 | **38** | ~58.000 | **38** |
| **Gabinete** — interior Genrod IP65 210×310×110 **$ 21.203** · exterior **Roker PRG357 IP65 200×200×155 $ 44.419** | 21.203 | **14** | 44.419 | **29** |
| Sondas DS18B20 estancas moldeadas de 3 m ($ 10.587 c/u): **6** por módulo | 63.522 | **41** | 63.522 | **41** |
| Sensores magnéticos de puerta cableados: **2** por módulo | 16.274 | **11** | 16.274 | **11** |
| Envío a Santa Cruz, prorrateado en **4** bultos (eran 6) | | **15** | | **17** |
| Armado + **prueba de banco documentada de los DOS buses con 25 m de cable** + garantía de reposición amortizada (era 150 en el doble de la v8) | | **160** | | **160** |
| Parte de plataforma del desarrollo: USD 1.000 repartidos en **3** módulos vendidos (eran 5 → 200) | | **333** | | **333** |
| **Costo** | | **612** | | **629** |
| Precio a 32 % sobre venta (costo / 0,68), redondeado | | **900** | | 925 → **950** |

**El margen elegido: 32 % sobre el precio de venta, el mismo criterio de la v8.0**, aplicado a los costos nuevos. Por qué 32 y no 25, y por qué 32 y no 40: igual que en la v8.0 — es producto propio con soporte, garantía de reposición y respuesta a 1.500 km (una placa a rehacer se come USD 90; un viaje, el margen entero), y a la vez es el primer cliente en la corrida más cara que se va a hacer nunca, y **el negocio es el abono al 76 %**, no el equipo.

**Los tres precios, para que Matías pueda defender cualquiera sin abrir nada más:**

| Ítem | Costo | Margen | **Precio** | % |
|---|---:|---:|---:|---:|
| **Doble de interior** (×2) | 612 | 288 | **900** | **32,0 %** |
| **Doble de exterior** (×1) — redondeado a 950: caja de intemperie, de la que dependen 2 reefers, y mayor plazo | 629 | 321 | **950** | **33,8 %** |
| **Repuesto doble** (×1, completo, sin cargo de plataforma) — redondeado a 400 hacia abajo: queda en estante | 279 | 121 | **400** | **30,2 %** |
| **Total equipos + repuesto** | **2.132** | **1.018** | **3.150** | **32,3 %** |

**Por qué un doble sale 900 y no 1.200 (ni 700).** Contra dos simples de la v8 (2 × 600): ESP32 + fuente + relés + PCB + gabinete + envío + alta + punto de red **NO se duplican**; sondas y reed **sí**. Contra el doble de la v8 (700): **+8 de electrónica** (2.º bus, 2.º defrost, borneras), **+10 de armado** (dos buses a probar), **+5 de envío** (menos bultos) y **+133 de plataforma** (USD 1.000 entre 3 y no entre 5). Costo 473 → 612 (+139); precio 700 → 900 (+200). **Se le dice al cliente sin abrir la cuenta: menos cajas, más electrónica y más programación por caja.** Y si la abren, los tres ítems tienen el mismo margen.

**Por qué el total baja 200 y no 1.000: dos cajas menos no son dos precios menos.** v8: 4 × 600 + 700 + 350 = 3.450 en equipos. v9: 2 × 900 + 950 + 400 = **3.150**. **−300 en equipos (−8,7 %)**, con la misma plataforma (1.000), las mismas 15 sondas en servicio (y 6 más en el repuesto) y 4 placas en vez de 6. Puesta en marcha 1.550 → 1.650 (**+100**: +8 h de software del doble que ahora corre en todos, −4 h por 3 altas en vez de 5). **Neto −200.** El margen absoluto de equipos baja de 1.105 a 1.018 (−87): es lo que cuesta que Andrés tenga razón — y la tiene: menos cable, menos red, menos cajas.

**Cómo llegó a 4.800, y por qué no se forzó a 5.000.** Se costeó cada ítem desde el BOM rev A con los tres cambios reales (2.º bus, plataforma entre 3, dos buses a probar), se aplicó el 32 % de la v8.0 y se redondeó cada unitario (900 / 950 / 400); la puesta en marcha se recontó hora por hora (66). **La suma dio 4.800 sola.** Matías dijo *"más o menos lo mismo"*, no *"lo mismo"*: −4 % es exactamente eso, y es honesto con el cliente que propuso la configuración más barata de instalar. **Alternativa si Matías prefiere sostener los 5.000:** exterior 1.000 · interior 950 × 2 · repuesto 400 · puesta 1.700 (68 h) = 5.000, margen de equipos 36 % — defendible, pero desparejo con el 32 % que ya se escribió en la v8.0 y con lo que se le dijo a Andrés. **Recomiendo 4.800. Decide Matías.**

**Dónde está la plata de esta cuenta, igual:** en el **abono (76 % de margen, §3.4)** y en la **puesta en marcha**. Los equipos son el ticket de entrada, no el negocio. **Eso es exactamente el modelo de PLATA.md.**

### 3.2 Puesta en marcha, USD 1.650

| Trabajo | h |
|---|---:|
| Sondas, rangos y umbrales por reefer + **calibración de las 15 sondas** contra referencia y registro de offsets (con los 3 °C puerta-fondo de Andrés como primer dato de rango) | 10 |
| **Software del módulo doble, ahora en los tres: segunda puerta, segundo defrost con silenciado por reefer, `SONDAS_MAX` a 8, un bus por reefer con asignación de sondas por bus, panel que muestra dos reefers por módulo, validación de los dos buses a 25 m** (10 h en la v8 + 8 del reparto por reefer y el panel) | 18 |
| Registro exportable con código de verificación | 14 |
| Panel multi-equipo y usuarios de lectura | 10 |
| Puesta en marcha remota (alta, credencial, OTA verificada, prueba de puerta y defrost de los dos canales), pruebas de campo con Andrés, runbook y capacitación — **3 módulos** (eran 5 → 14 h) | 10 |
| Salud de bus, histéresis de 3 barridos y **verificación cruzada entre sondas** | 4 |
| **Total a USD 25/h** | **66 = USD 1.650** |

De 62 a 66 h: **+8 h en el software del doble** (es la "programación" que Matías le dijo a Andrés: repartir por reefer lo que entra por dos buses, silenciar por reefer y mostrar dos reefers por caja) y **−4 h** en altas remotas (3 en vez de 5). Si @firmware dice que son más horas, **salen del margen, no del precio**.

### 3.3 **LA CUENTA DEL CAÑO** — archivo, y por qué ya no entra en el precio

> Se conserva de la v5 **como historia y como argumento**, no como parte del presupuesto. **El tendido lo hace y lo paga el cliente, y no aparece en el documento que se manda.** Con la v9 **no queda ninguna tirada entre contenedores**: la caja va sobre la unión de cada par y de ahí sale un cable corto a cada reefer. Esta cuenta era la de UNA tirada de 25 m con caño Daisa; hoy sirve para saber cuánto se ahorró el sitio con la configuración que propuso Andrés.

| Ítem (por par, 25 m de recorrido) | Subtotal |
|---|---:|
| Caño galvanizado Daisa 3/4 liviano, 9 tiras de 3 m a $ 11.637 | $ 104.733 |
| Cuplas (8), curvas (6), cajas de paso estancas (4), conectores caño-caja (10) | $ 96.000 |
| Grampas omega 3/4 una cada 1,5 m (18) + tarugos y tornillos | $ 35.000 |
| Cable exterior, 30 m a $ 400/m | $ 12.000 |
| **Materiales por par** | **≈ $ 247.700 ≈ USD 161** |
| Mano de obra: 2 jornadas de oficial electricista al piso de tarifa ($ 12.000/h × 16 h) | **$ 192.000 ≈ USD 125** |
| **Total por par** | **$ 439.700 ≈ USD 286** |

**Para qué sirve esta cuenta ahora que no la cotizamos.** (1) **Saber cuánto vale lo que Andrés resolvió con la caja en la mano:** tres pares que hubieran costado hasta USD 286 cada uno de canalización se convirtieron en seis cables cortos. Si igual dicen "esto de la obra no lo teníamos previsto": **la configuración la describieron ellos, y es la de menos obra posible**. (2) **El argumento del precio del doble:** si alguien compara 900 contra "dos simples de 600", acá está lo que NO se paga — ni canalización entre contenedores ni un segundo punto de red por par. (3) **Que nadie regale la instalación:** si aparece la tentación de "se lo hacemos nosotros para cerrar", el número a tener en la cabeza es **USD 286 por tirada**, más pasajes y estadía. Los renglones de cuplas, curvas, cajas y grampas son estimados a precio de plaza; el caño y la mano de obra, relevados. **Nosotros no la cotizamos y no la ejecutamos.**

### 3.4 Servicio mensual: qué cuesta servir y qué se cobra

| Costo directo mensual | v8.0 (5 módulos) | **v9.0 (15 sondas, 5 reed, 3 módulos)** |
|---|---:|---:|
| Supabase Pro | 25 | 25 |
| Reposición amortizada (módulos y sondas en garantía) | 18 | **15** |
| Soporte (2,5 h → 2,3 h a USD 25) | 62 | **57** |
| Informe mensual | 25 | 25 |
| **Total** | **130** | **122** |

**Tarifa: USD 100 por reefer por mes × 5 = USD 500/mes** (decisión de Matías, **no se toca con la configuración nueva**). Costo directo 122 → **margen bruto USD 378 (76 %)**. **Con el inicial en 4.800, el abono paga el equipamiento entero en 12,7 meses de margen.** La justificación, si preguntan: **mantenimiento del servidor, custodia de los datos y seriedad del servicio**.

**El abono es estrictamente proporcional a los reefers, no a los equipos**: 5 = 500, 6 = 600. Pasamos de 5 cajas a 3 y se vigila lo mismo. **Y esta vez la regla juega al revés y también sirve:** si preguntan *"¿con menos equipos no baja el mensual?"*, la respuesta está escrita desde la v2: **el servicio se cobra por reefer vigilado, no por caja instalada.** Cuando entre el sexto, los USD 100 adicionales son margen puro: el equipo ya está puesto y las sondas también.

**El escalón de los primeros 3 meses al 50 % sigue eliminado** (decisión de Matías, 4-sep): abono completo desde el primer mes en las dos formas.

### 3.5 Condiciones de pago — 50 / 50, y por qué no 25

**50 % con la orden de compra (anticipo de materiales) y 50 % contra los equipos instalados y reportando.** El abono arranca con el primer equipo andando. Hay que comprar y armar **4 módulos dobles** (3 + el repuesto) antes de ver un peso del segundo tramo. Con el 50 % (**USD 2.400 ≈ $ 3.672.000**) la compra completa de materiales —**≈ $ 749.000, §3.7**— queda cubierta **casi cinco veces**. Con el 25 % (USD 1.200 ≈ $ 1.836.000) también alcanzaría para los materiales; lo que no cubriría es el **riesgo de cobranza del segundo tramo**, que es lo que en realidad se está financiando. Los hitos siguen existiendo **como compromiso de entrega con plazo**. **Punto para que Matías confirme:** cobrar antes de entregar los hitos es más cómodo para la caja y más exigente con la palabra.

### 3.6 Las dos formas de pagar, y por qué se cayó la tercera

**A. Equipos + servicio mensual.** 4.800 + 12 × 500 = **10.800** el primer año; 6.000/año después; **24 meses 16.800**.
**B. Anual adelantado, 10 % de descuento sobre el año de servicio.** 4.800 + (12 × 500) × 0,9 = 4.800 + 5.400 = **USD 10.200**; renovación 5.400/año; **24 meses 15.600**. El descuento le ahorra **USD 600 el primer año** y compra **cero riesgo de cobranza durante 12 meses**, una factura en lugar de doce, y caja para armar los equipos.
**C, eliminada.** Matías: *"el de la inversión inicial no lo ofrecería"*. **No se vuelve a ofrecer sin contrato validado por contador y un cliente con historial de pago.**
**Sin cláusulas condicionales:** el tendido es del cliente y el precio es firme.

### 3.7 Los 4 módulos: qué falta comprar y cuánto sale (estimación — pide rev B a @hardware)

**Qué hace falta.** 4 placas Mini: **1 doble de exterior + 2 dobles de interior + 1 doble de repuesto, las 4 con el 2.º bus**. Gabinetes: 1 de intemperie (ya en sitio) + 3 de interior. Sondas: 18 en los dobles (las 3 de `REEFER_01_SCZ`, ya calibradas, se reaprovechan) + 6 del repuesto = **21 a comprar**. Reed: 6 + 2 − 1 existente = **7**. Defrost: 6 entradas (opto, cable y bornera). Reservados **3 ESP32 para las galgas de Dreyfus** (P0 de octubre).

| Ajuste a la v9 (desde los ≈ $ 821.000 de la v8, 6 placas) | $ |
|---|---:|
| **−2 placas** (4 en vez de 6): 2 ESP32 ($ 14.999), 2 fuentes ($ 10.579), 2 gabinetes de interior ($ 21.203) y sus consumibles, borneras, optos y prensacables | **−$ 160.000** |
| **+2.º bus 1-Wire en las 4 placas**: pull-up + alternativa, resistencia serie, clamps, bornera, prensacable y opto de la 2.ª entrada de defrost (≈ $ 12.000 por placa, estimado; los pines ya están) | **+$ 48.000** |
| **+3 sondas** (21 en vez de 18: los dobles van completos y el repuesto también) | **+$ 31.761** |
| **+1 reed** (7 en vez de 6) | **+$ 8.137** |
| Rollo de UTP para la prueba de banco, módulos de relé, caja Roker (ya comprada): sin cambio | 0 |
| **TOTAL v9 (estimado)** | **≈ $ 749.000 ≈ USD 490** |

**Bajan si:** las 3 cajas IP65 de stock pasan la medición **`M9`** (**−$ 63.609** — ahora alcanzan justo para los 3 gabinetes de interior) y las fuentes de stock resultan de **2 A** (**−$ 52.895**). **Contra el anticipo del 50 % (USD 2.400 ≈ $ 3.672.000), la compra completa es el 20 %.** **Lo que hay que pedirle a @hardware:** rev B del BOM para 4 placas dobles con 2 buses y sin D2, y confirmar si el stock de 20 sondas y 10 reed de `PLATA.md` sirve (escenario A, rearmar) o se compran moldeadas (B, recomendado). **El margen del 32 % aguanta ± USD 40 por placa sin tocar precios.**

**La PCB es el renglón de mayor plazo de entrega: se pide primero, y con el 2.º bus ya decidido.** Orden de pago el día de la OC: 1. PCB a JLCPCB (10 placas: las 4 de Cerro Moro + demos de Bahía) · 2. los ESP32, todos al mismo vendedor y en la misma orden · 3. sondas y cable · 4. gabinetes de interior si `M9` no pasa · 5. el resto. **Nada antes del conteo de stock de 30 minutos.**

**El plan arranca cuando aceptan, no antes.** Semana 0 = aceptación + anticipo del 50 %. Hasta que eso pase **no se compra, no se arma y no se despacha nada**. **Única excepción, y es de diseño, no de compra:** decidir el 2.º bus con @esquematico esta semana, porque condiciona la PCB.

| Paso | Plazo desde la aceptación | Quién |
|---|---|---|
| **Decisión del 2.º bus en la Mini** (GPIO 18, sin D2) — antes de pedir la PCB | esta semana | Matías / @esquematico |
| Conteo del stock real + mediciones `M1`-`M5`, `M7`, `M9` y etiqueta V/A de las fuentes | semana 0 | Gonza |
| Compra del faltante — **la PCB primero** | semana 0-1 | Gonza / Matías |
| Despacho de 2 sondas para el equipo ya instalado (encomienda, 5-8 días hábiles) | semana 1 | — |
| **Cierre del firmware doble** (correcciones + 2.ª puerta, 2.º defrost por reefer, `SONDAS_MAX` a 8, un bus por reefer) — **bloquea a los tres módulos** | semana 1-3 | Matías / @firmware |
| Alta, calibración remota, rangos y primera alerta real en `REEFER_01_SCZ` | semana 2 | Andrés + Matías |
| **HITO 1** | **semana 2** | — |
| Armado de los 4 módulos + **prueba de banco de las 8 salidas con 25 m de cable** | semana 1-3 | Gonza / Sergio |
| Despacho de los 4 bultos (3 módulos + repuesto) a Cerro Moro | semana 2-3 | — |
| **Tendido de los 6 cables cortos**, de la unión de cada par a cada reefer (apto exterior en el par de afuera) | semana 3 | **cliente** |
| Montaje de las 3 cajas sobre la unión de cada par; el reefer de `REEFER_01_SCZ` pasa a su doble con sus 3 sondas | semana 3-4 | campamento |
| Alta y calibración de las 12 sondas nuevas | semana 4 | Matías |
| **HITO 2** (los 3 módulos y los 5 reefers reportando + una semana sin falsas alarmas) | **semana 5** | — |

**El riesgo que hay que decir en voz alta: el hito 2 tiene dos dueños otra vez.** **La fabricación** (@hardware: despacho realista semana 4-5, hito 2 en la 7-8) **y el firmware doble**, que en la v8.0 había salido del camino crítico y **acá vuelve para los tres módulos**. Lo que ya no aprieta: la obra del cliente y la red. **Matías no debería prometer el hito 2 por teléfono con más firmeza que la que dice el papel.**

**Por qué se puede empezar a armar antes de la orden de compra, sin exponer un peso nuevo.** Los kits ya estaban planificados como las unidades de demostración de Bahía. Si Cerro Moro no compra, van a su destino original. **La contracara para el Director: si Cerro Moro compra, Bahía se queda sin demos — ahora son 4 módulos, no 6.** Recomendación: reposición en el mismo pedido que la OC.

### 3.8 Moneda, validez, facturación

**Facturación en USD, pago en pesos al BNA vendedor de la fecha de pago, sin validez en el PDF.** Referencia impresa: **BNA vendedor billete $ 1.530 del 8-sep-2026** (bna.com.ar/Personas, cotización de las 09:50; compra $ 1.480). Nota interna: revisar precios si pasan más de 6 meses desde el 8-sep. Antes de la cotización firme: monotributo vs. RI, plazo de pago, cláusula de moneda, quién firma. Se pregunta cuando la empresa tenga nombre.

### 3.9 Contra una pérdida y contra la competencia

Una pérdida de 3 t valuada al precio de novillo en pie ($ 4.181/kg, INMAG jul-2026) son $ 12,5 M: **16 meses de servicio** al abono de USD 500 (≈ $ 765.000 por mes). testo Saveris 2-T2: USD 318 por unidad y mide **un** punto; para cubrir los 15 puntos de esta propuesta harían falta 15 unidades = **USD 4.770** antes de importación — **prácticamente el total de esta propuesta** — sin nube, sin puerta, sin relé, sin defrost, sin repuesto en sitio, y se configura con una red WiFi y una clave, que es exactamente lo que este sitio no tiene. **Y ninguna de esas unidades es apta para la intemperie sin gabinete adicional.**

---

## PARTE 4 — Puesta en marcha: qué es cada hito por dentro

Las duraciones se cuentan **en semanas desde la aceptación**, no contra el calendario. Los hitos pesados caen después de la semana 5 para no chocar con la parada de Dreyfus.

| Hito (cliente) | Etapa interna | Desde | Hasta | Cómo se acepta |
|---|---|---|---|---|
| 1 — El equipo ya instalado con sus 3 sondas adentro y calibradas, rangos, primera alerta real | E0 | semana 0 | **semana 2** | Captura de la alerta en el celular + registro en nube + **planilla de calibración con el offset de las 3 sondas de `REEFER_01_SCZ`** |
| 2 — Los 3 módulos y los 5 reefers reportando; nada se pierde, nada sobra | E1: buffer offline, alertas encoladas, alerta de sonda caída, vigía de equipo mudo, discriminador de bus + histéresis, **detección de sonda que se desvía de las otras del mismo reefer**, **segunda puerta y segundo defrost con silenciado por reefer, un bus por reefer — en los tres módulos y en el repuesto** | semana 2 | **semana 5** | Los 3 módulos montados con sus 15 sondas calibradas; desenchufar una sonda y que llegue la alarma; cortar la red 20 min sin perder lecturas; abrir una puerta 4 min y que avise; **forzar el defrost de un reefer y verificar que el que comparte módulo sigue alarmando**; **una semana sin falsas alarmas** |
| 3 — Acceso seguro | E2: RLS cerrada, credencial por módulo, secretos fuera del binario, revocar claves quemadas | semana 5 | **semana 10** | Con la clave vieja no se escribe; los 3 módulos siguen reportando |
| 4 — Actualización a distancia | E3: OTA con manifiesto inmutable | semana 10 | **semana 12** | Tres actualizaciones seguidas por aire al primer intento, en todos los módulos |
| 5 — Panel e informe | E4: usuarios de lectura, vista de los reefers (dos por módulo), exportación con código, informe mensual automático, **comando de relé desde el panel** | semana 12 | **semana 15** | Un usuario de la empresa entra solo, baja el informe y acciona una salida desde el panel |

**El hito 2 es el apretado**: la semana sin falsas alarmas arranca cuando los 3 módulos reportan, alrededor de la semana 4, y vence en la 5. Sin colchón — y con dos cuellos: la fabricación de la PCB y el firmware doble, que ahora necesitan los tres. Lo que hoy está roto y cada hito arregla está en `AUDITORIA_HALLAZGOS.md`; no cambió.

---

## PARTE 5 — Qué necesitamos para cerrar

### 5.1 De la empresa, cuando tenga nombre

Quién firma, cómo factura (monotributo/RI, plazo), si acepta la cláusula de moneda, **cuál de las dos formas de pago elige (A o B)**, y confirmación de que el montaje **y el tendido de los 6 cables cortos de cada reefer a su caja** los hace personal del campamento (sin personal nuestro en sitio no corresponde ART ni legajo de contratista).

### 5.2 De Andrés: lo que sigue abierto

**Ninguna de estas frena el envío.**

1. **¿Cuál de los 4 de adentro es el que está fuera de servicio?** Ahora **sí** cambia algo: define qué par tiene un solo reefer activo hoy, y por lo tanto qué módulo arranca con 3 sondas conectadas y 3 en espera.
2. **¿Cuántos metros hay de la unión de cada par a la sonda más lejana de cada reefer?** Con la caja sobre la unión deberían ser pocos; conviene el número antes de cortar cable de prueba.
3. **¿La red del campamento llega bien a los 3 puntos donde van las cajas?** Son 3, no 5: mejoró. Si alguno queda corto, repetidor **antes** de despachar.
4. **¿Los reefers tienen una señal o contacto de defrost accesible?** Y **¿es 12-24 V o contacto seco?** (@hardware: dos puentes de soldadura en la placa, se define **antes de rutear**).
5. **¿Cómo midió los 3 °C?** Pedirle el dato o la foto: sirve para fijar rangos por reefer y es evidencia del argumento de las 3 sondas.
6. **¿Para quién trabaja Andrés?** (empleado de PAAS o de una contratista). No es técnica: decide la Parte 7.

---

## PARTE 6 — Para Andrés (aparte del PDF)

### 6.1 WhatsApp — lo manda Matías, junto con el PDF nuevo

> Andrés tiene en el celular un presupuesto anterior (el de 4.600 del 4-sep seguro; el de 5.000 si se mandó). Este mensaje lo reemplaza **sin citar la cifra vieja**, así cubre los dos casos.

```
Andrés, ahí va el presupuesto rehecho como lo armaste vos: tres
módulos, uno por cada par de reefers, con la caja sobre la unión de los
dos y un solo cable de 3 hilos a cada reefer. Queda en USD 4.800: son
menos cajas, pero cada una lleva más electrónica adentro y más
programación para repartir por reefer, así que queda más o menos lo
mismo, como te dije. El abono es el mismo, USD 100 por reefer por mes
= 500 por los cinco que andan.

Mantengo las 3 sondas por reefer: con los casi 3 grados que mediste
entre la puerta y el fondo, con una sola sonda no sabés qué temperatura
tiene la carga. Van puerta, medio y fondo por el mismo cable, y se
calibran las tres juntas.

El de afuera va en caja estanca para intemperie. Los módulos los pruebo
acá en el banco con 25 metros de cable antes de despacharlos.

El reefer que está parado ya queda cubierto por el módulo de su
vecino, con sus sondas incluidas: el día que vuelva se conectan y
listo, sin comprar nada.

Mismas dos hojas, sin nombre de empresa. Este reemplaza al anterior.
```

> **Por qué está escrito así, para que no se suavice al copiarlo:**
> **(a)** **Arranca con "rehecho como lo armaste vos".** La configuración es de él; lo primero que lee es que se hizo exactamente eso, con sus dos frases (caja sobre la unión, un cable por reefer).
> **(b)** **El número va una sola vez, con el motivo pegado en la misma oración**, y es el mismo motivo que Matías ya le dijo por chat; cierra con "como te dije": coherencia entre lo hablado y lo escrito.
> **(c)** **No cita la cifra vieja.** No sabemos con certeza si tiene el de 4.600 o el de 5.000. "Este reemplaza al anterior" sirve para los dos.
> **(d)** **Que el abono NO cambia se dice en la misma frase que el total.** Y con menos cajas y el mismo abono, la regla "por reefer vigilado, no por caja" queda demostrada por segunda vez.
> **(e)** **Las 3 sondas se defienden con SU dato** (casi 3 °C puerta-fondo). No se discute con teoría: se le devuelve su medición y se le dice qué haría una sola sonda con ese gradiente.
> **(f)** **"Por el mismo cable"** anticipa la objeción de los 9 hilos.
> **(g)** **La prueba con 25 m compra confianza técnica**, y 25 m es más que cualquier tirada de esta configuración.
> **(h)** **El sexto reefer aparece como previsión, y ahora gratis.** Es lo que él gana adentro para defender la compra.
> **(i)** **No le pide nada. No menciona material de caja ni riesgo.**
> **(j)** **No se manda hasta que el PDF esté al lado.** Los dos juntos, o el mensaje pierde la mitad.

### 6.2 Guion de 5 líneas para que la presente él

1. **Arrancá por el problema, no por el producto:** "un reefer que se corta un fin de semana es la comida de todo el campamento, y hoy nadie se entera hasta que abren la puerta."
2. **Mostrá lo que ya anda:** abrí el panel en el celular y mostrá la temperatura de ahora del equipo instalado — sigue reportando mientras la propuesta se evalúa. Si podés, sacá una sonda al aire un minuto y que vean subir la curva.
3. **Decilo en una frase:** "tres equipos, uno por cada par de reefers, con la caja sobre la unión. Tres sondas adentro de cada reefer —medí casi 3 grados entre la puerta y el fondo—, te avisa al celular si se sale de rango o si queda la puerta abierta, y arma el registro mensual solo."
4. **Si preguntan por el cable:** "un solo cable de tres hilos de la caja a cada reefer, corto, porque la caja va entre los dos. No hay que cruzar nada de un contenedor a otro."
5. **Lo que NO prometés:** que garantiza la mercadería (avisa, no garantiza) · que avisa el corte de luz (avisa que el equipo dejó de reportar) · que la sirena está incluida (van las salidas, la sirena se conecta) · que está terminado (hay una puesta en marcha por hitos, y está en el precio) · fechas o precios distintos a los del PDF. Cualquier pregunta técnica o de números: "eso lo contesta Matías, lo llamamos ahora."

---

## PARTE 7 — La relación con Andrés (para que Matías decida)

**Lo que cambió:** en la v1 Andrés era el contacto en sitio de un cliente y la regla era simple: **ningún pago ni beneficio ligado a que su empleador compre.** Ahora es él quien **ofrece y presenta** la propuesta a una tercera empresa que él elige, **y quien armó la configuración final** con la caja en la mano. Está haciendo de referidor —y de co-diseñador— de hecho.

**Lo que sigue vigente, sin discusión:** si el comprador termina siendo Pan American Silver, o una contratista que opera bajo su Código de Conducta de Proveedores (que alcanza a proveedores **y a sus subcontratistas**), **no hay comisión ni reconocimiento material.** Cualquier empresa que opere dentro del campamento está, casi seguro, bajo ese código.

**El conflicto de interés, escrito:** Andrés trabaja adentro (no sabemos si es empleado de PAAS o de una contratista — **hay que preguntarlo**), elige a quién ofrecerle el sistema y lo presenta con la credibilidad de su puesto. Si cobra por eso, pasa de "el que trajo un proveedor bueno" a "el que le vendió algo a la empresa de al lado y se llevó una parte". **El costo de un reconocimiento mal puesto sigue siendo mayor que el negocio.**

| Opción | Qué es | A favor | En contra |
|---|---|---|---|
| **1. Nada material, todo el reconocimiento no monetario** (status quo) | Agradecer por escrito, darle el acceso y la hoja de una carilla, nombrarlo como contacto en sitio, contarle el caso como logro suyo — **y la configuración como idea suya, porque lo es** | Cero riesgo. Es lo que él pidió (*"la gente de acá no lo vio"*): quedar bien, no cobrar | Si el negocio crece por él y no recibe nada, el empuje puede enfriarse |
| **2. Referidor formal solo para leads AJENOS al campamento** (Bahía, Venado Tuerto, futuros) | Reconocimiento único equivalente a 1 mes de abono del cliente referido, pagado después del 3er abono cobrado; **excluye** a PAAS, sus contratistas y cualquier empresa de Cerro Moro; condicionado a que su empleador lo permita | Es honesto, separa los mundos, y **ya tiene un caso real: Venado Tuerto lo trajo él** | Hay que escribirlo y preguntarle si su empleador tiene política de actividades externas |
| **3. Reconocimiento en especie, fuera del negocio** | Un equipo Termovigía para uso propio, o capacitación, sin vínculo con ninguna compra | Barato, tangible | Si se da mientras Cerro Moro está en discusión, se lee igual que una comisión |

**Mi recomendación honesta:** 1 ahora, 2 por escrito cuando Venado Tuerto avance, y **preguntarle a Andrés para quién trabaja** antes de ofrecerle cualquier cosa. La 3, nunca durante la negociación de Cerro Moro. **No decido: decide Matías.**

**Lo bueno de esta vuelta:** a Andrés le llega **exactamente el sistema que él armó**, con sus tres frases adentro y su medición de los 3 °C como argumento. **Lo que hay que cuidar:** es el tercer presupuesto en cuatro días. Se compensa con que esta vez el número **baja** y con que la razón es suya. **Cuarta vuelta no hay: la próxima conversación es de aceptación, no de configuración.**

---

## Anexo — Fuentes consultadas

- **Configuración v9:** WhatsApp de Andrés, 8-sep (*"con tres módulos solucionamos lo de Cerro Moro, un módulo para dos reefer; al estar juntos de a dos es fácil hacer la conexión; pongo la caja sobre la unión de los dos y saco las sondas"*; *"casi 3 °C entre la puerta y el fondo"*) y respuesta de Matías (*"3 es mucho mejor para calibración"*; *"rehago el presupuesto, queda más o menos lo mismo, porque le tengo que meter un poco más de electrónica adentro de la caja y programación"*).
- **Un solo bus en la Mini y pines reservados para el 2.º:** `C:\Proyectos\frioseguro\hardware\mini\PINOUT_MINI.md` (GPIO 4 bus DS18B20 hasta 6 sondas; 18 y 23 "quedan para un 2.º bus 1-Wire si hace falta").
- Alcance del bus, pull-ups, tierras entre contenedores y límite prudente de 15 m: `C:\Proyectos\frioseguro\hardware\ALCANCE_1WIRE.md` (@muestreador), §2.6.
- **Costos reales, gabinetes, PCB, plazos y margen:** `C:\Proyectos\frioseguro\hardware\mini\BOM_CERRO_MORO.md` rev A (@hardware, 4-sep-2026) — §5.1 D2 rompe el bus a 25 m.
- **BOM de la placa:** `C:\Proyectos\frioseguro\hardware\mini\BOM_MINI.md` rev A (@esquematico, 4-sep-2026).
- **Firmware de módulo doble:** `C:\Proyectos\frioseguro-v31\firmware_modular\VERIFICACION_V3.1_2026-09-04.md`, APTO CON CORRECCIONES, correcciones en curso.
- Estado real y auditoría: `C:\Proyectos\frioseguro\entrega_scz\docs\ESTADO_HONESTO.md` · `AUDITORIA_HALLAZGOS.md`.
- Qué hace hoy el firmware (leído el 3-sep-2026): `firmware_revival/sondas.h` línea 31 · `config.h` 67-150 · `firmware_revival.ino` 369-375, 483-488, 804-944 · `comandos_nube.h` (sin comando de relé).
- Contrato base: `MATI-HQ\comercial\CONTRATO_TERMOVIGIA_v4.md`.
- **Dólar BNA vendedor billete $ 1.530, 8-sep-2026 09:50** (bna.com.ar/Personas; compra $ 1.480). Precios de canalización, 1-Wire AN148, testo Saveris 2-T2, novillo INMAG, Supabase Pro y Código de Conducta de Proveedores de PAAS: enlaces conservados en la v5.2 de este archivo (historial de git).
- **Generadores y verificación:** `comercial/panamerican/armar_cliente_v7.py` · `armar_interno_v7.py` · `render_v7.py` (guarda: SIN FUGAS, 2 páginas, márgenes OK) · verificación independiente del texto del PDF contra `calcular()` (8-sep): TODO OK.

## Anexo — Lo que quedó abierto (para Matías, antes de mandar)

1. **Los números, con el mismo margen parejo (~32 %) de la v8.0:** doble de interior **900 × 2** · doble de exterior **950** · repuesto **400** · puesta en marcha **1.650** (66 h) · **inicial USD 4.800** (v8.0: 5.000; −4 %) · abono **500/mes, sin tocar** · B = **10.200** · anticipo 50 % = **2.400**. Alternativa para sostener 5.000 en §3.1 (36 %, desparejo). **¿Van?**
2. **Mandar el WhatsApp de §6.1 junto con el PDF.** Dice "reemplaza al anterior" sin cifra vieja: sirve tanto si Andrés tiene el de 4.600 como el de 5.000.
3. **⚠ Decisión de placa, esta semana: poblar el 2.º bus 1-Wire de la Mini** (GPIO 18, pines reservados) para tener un bus por reefer, sin D2. Es la "más electrónica" que se le dijo a Andrés y condiciona la PCB. **Después de JLCPCB ya no se cambia.** (Matías / @esquematico)
4. **⚠ El firmware doble VOLVIÓ al camino crítico: lo necesitan los tres módulos.** @firmware da fecha de cierre y confirma que las 18 h de §3.2 alcanzan; si son más, salen del margen. Plan B parcial: cada doble arranca con un reefer. **Avisar al Director.**
5. **Preguntarle a Andrés** lo de §5.2: cuál de los 4 está fuera de servicio, metros de la unión a cada reefer, defrost 12-24 V o seco, red en los 3 puntos, cómo midió los 3 °C.
6. **⚠ El cuello de fabricación sigue:** PCB Mini, despacho semana 4-5, hito 2 en la 7-8. O se corren los hitos en el PDF, o se pide la PCB ya (USD 43, con el 2.º bus decidido). **Decisión tuya, antes de firmar.**
7. **Qué pasa con `REEFER_01_SCZ` en el hito 2:** su reefer pasa al doble de su par, sus 3 sondas calibradas se reaprovechan; el kit viejo queda como segundo respaldo o vuelve a Bahía como demo.
8. **El sexto reefer entra sin costo de equipo** y sube el abono a 600. Está escrito así en el documento del cliente. **¿Va así?**
9. **Compra de materiales ≈ $ 749.000 ≈ USD 490, estimado** sobre el BOM rev A. **@hardware recuesta las 4 placas dobles con 2 buses (rev B)** y confirma si el stock de 20 sondas y 10 reed sirve.
10. **`M9`** ($ 63.609 — las 3 cajas de stock cubren justo los 3 gabinetes de interior) y **etiqueta V/A** de las fuentes ($ 52.895): 10 minutos con un calibre, antes del pedido. (@hardware)
11. **Decisión de portfolio:** si Cerro Moro compra, Bahía se queda sin demos — ahora son 4 módulos. Reposición en el mismo pedido que la OC. (Director)
12. **Verificación cruzada entre sondas: hoy NO existe.** Hito 2. Con 3 °C reales entre puerta y fondo, tiene que comparar cada sonda contra su propia historia, no contra el promedio. Si no se puede cumplir, sacar el punto 3 del bloque "por qué 3 sondas".
13. **Accionamiento del relé desde el panel: tampoco existe.** Hito 5.
14. **`SENSOR_DOOR_ENABLED`** viene deshabilitado: habilitar y probar puerta y defrost de **los dos canales de los 4 módulos**.
15. **Sirena:** a USD 40 no deja margen. Propongo USD 70 instalada, o baliza LED de 12 V.
16. **Foto de la caja de exterior** después del primer temporal (de ella dependen 2 reefers).
17. **Andrés:** opción 1, 2 o 3 de la Parte 7, y preguntarle para quién trabaja. Reconocerle la configuración como suya: lo es.
18. **PDF: hecho y verificado** — 2 páginas A4, sin logo ajeno, sin "Para:", sin validez, sin material de gabinete, **sin "cinco", sin "5 módulos", sin USD 260 ni ninguna cuenta vieja**, texto cruzado contra `calcular()`.
19. Monotributo vs. RI: se pregunta cuando la empresa tenga nombre.
20. **Cuarta vuelta no hay.** Tres presupuestos en cuatro días es el límite: si aparece otro cambio de configuración, se contesta por teléfono y se ajusta después de la aceptación, no antes.
