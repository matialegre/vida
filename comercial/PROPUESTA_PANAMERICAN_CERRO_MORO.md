# PROPUESTA — Monitoreo de temperatura de los reefers del campamento Cerro Moro (Santa Cruz)

> @comercial · **v8.0, 2026-09-04** · **UN SOLO presupuesto: 5 módulos = 1 doble de exterior + 4 simples de interior**
> **Configuración DEFINITIVA, cerrada por chat con Andrés el 4-sep 15:23.** Matías preguntó *"¿los de afuera uno, y los otros uno cada uno sería?"*; Andrés: **"Así sería"**. Y sobre el cable: **"No es mucho lo de los cables. Los saco de acá."**
> - **Los 2 reefers de la intemperie están JUNTOS** → **UN módulo doble**, en **caja estanca IP65 apta para exterior** (Matías ya mandó una al sitio).
> - **Los 4 reefers de adentro van con UN MÓDULO CADA UNO** — incluido el que hoy está fuera de servicio: **su módulo se instala igual**, y el día que el reefer vuelva sólo se le conectan las sondas.
> - **Total: 5 módulos.** Repuesto: **1 módulo doble**, que cubre a cualquiera de los cinco (es la misma placa).
> - **Por reefer, siempre igual: 3 sondas + 1 sensor de puerta + 1 señal de defrost.**
> - **Ya no hay cable entre reefers de interior.** La única tirada entre contenedores es la del par de afuera, que está pegado. La nota al pie *"No incluye cable ni tendido entre reefers"* **se mantiene tal cual**.
> **Precio: inicial USD 5.000** — 1 doble de exterior **700** + 4 simples de interior **600** + repuesto doble **350** + puesta en marcha **1.550** (62 h). **Margen parejo del ~32 % en los tres módulos** (Matías liberó el precio del doble el 4-sep: *"no dejes fijado a 850 el exterior... pensalo vos bien"*). **Sube respecto de la v6.1 (4.600) porque hay un equipo más, y se dice así.** El abono **no** se toca: **USD 100 por reefer por mes = 500/mes**, sin escalón, completo desde el primer mes · el **tendido de cable no se cotiza** — a cargo del cliente · **en el documento del cliente no se dice el material del gabinete ni se menciona impresión 3D**.
> **⚠ CONTEXTO QUE MANDA EL MENSAJE: Andrés ya recibió por WhatsApp hoy a las 14:01 el PDF de la v6.1 con USD 4.600.** Esta versión sube a 5.000. En el WhatsApp de §6.1 eso se dice **de frente y corto**, sin justificarse de más. El interno explica en dos líneas cómo se sostiene la diferencia.
> **Se mantiene de la v6.1:** la firma con UTN/GIMAP/Montagne, los hitos relativos y la propuesta sin cláusulas condicionales.
> **Se mantiene de la v5.2:** sin destinatario, sin nombrar a Panamerican, hitos en semanas desde "aceptación + anticipo", 50/50, formas A y B, sin validez, USD con pago en pesos al BNA de la fecha de pago.
> **Matías decide el número final, siempre.** Todo monto de acá abajo es propuesta con la cuenta a la vista.
> Doctrina: `PLATA.md`. Base técnica: `ALCANCE_1WIRE.md` (@muestreador), **`BOM_CERRO_MORO.md` rev A (@hardware, 4-sep — precios ML y JLCPCB verificados en vivo; de ahí salen los costos reales)**, `BOM_MINI.md` (@esquematico, 4-sep), `ESTADO_HONESTO.md`, firmware `firmware_revival` leído el 3-sep y **auditoría del firmware de módulo doble `VERIFICACION_V3.1_2026-09-04.md` (APTO CON CORRECCIONES)**.
> **El comprador NO es Pan American Silver:** es "una empresa" que Andrés todavía no identifica. El documento del cliente va **sin destinatario, sin logo ajeno y sin nombrar a Panamerican**. El archivo conserva el nombre por historial.

## Qué cambió en esta versión

**1. Adentro, un módulo por reefer. Lo confirmó Andrés en el chat.** Matías preguntó textual *"¿los de afuera uno, y los otros uno cada uno sería?"* y Andrés contestó **"Así sería"**. Con eso se cae la idea de emparejar los de adentro: **4 reefers bajo techo = 4 módulos simples, uno cada uno.** Afuera no cambia nada: los dos están pegados y comparten **un módulo doble estanco**. **Total 5 módulos.**

**2. El módulo del reefer fuera de servicio se instala igual, y eso cambia cómo se cuenta.** Antes el sexto reefer era *"un canal libre en un módulo doble"*. Ahora es más simple y más fuerte de vender: **su módulo ya está puesto, alimentado y dado de alta**. El día que el reefer vuelva a servicio no hay que abrir ninguna caja ajena ni tocar la configuración de otro reefer: **se le conectan sus 3 sondas, su sensor de puerta y su señal de defrost — USD 260 — y el abono pasa de 500 a 600/mes.**

**3. El precio SUBE a USD 5.000, y hay un solo motivo.** Un equipo más que en la v6.1 (5 contra 4) y un reefer más con su propio módulo. **No se acomodó ningún unitario para llegar a ese total**, y de hecho **el total no se movió cuando se recalcularon los precios** (ver punto 4): salió 5.000 con el 850 fijado y vuelve a dar 5.000 con el margen parejo. Es coincidencia y la digo como tal.

**4. Margen PAREJO en los tres módulos: ~32 %. Simple 600, doble 700, repuesto 350.** Matías liberó el precio del doble el 4-sep (*"no dejes fijado a 850 el exterior, depende de lo que vayas a cobrar con los individuales... pensalo vos bien"*) y el Director puso el criterio: **un solo margen aplicado parejo**, porque 25 % en el simple y 44 % en el doble es indefendible el día que alguien pone los dos precios uno al lado del otro — y en una compra corporativa eso pasa. **Elegí 32 % sobre precio de venta** (§3.1). **Contra la v6.1, el simple pasa de 600 a 600: queda igual**, pero ahora con margen sano en vez de flaco. **El doble cae en 700**, que es donde tiene que caer: más que un simple y **mucho menos que dos**, porque comparte el ESP32, la fuente, la placa, el alta remota y el punto de red. **El total no cambia: 5.000.**

**5. La puesta en marcha sube de 1.450 a 1.550, y sube en el único renglón que corresponde.** Son **5 altas remotas, 5 credenciales, 5 OTA verificadas y 5 pruebas de puerta y defrost** en vez de 3: **+4 h, de 58 a 62 h a USD 25**. Todo lo demás queda igual. **Las 10 h del software del doble no bajan aunque ahora lo use un solo módulo instalado**: el código se escribe una vez y el repuesto también lo lleva.

**6. El abono NO se toca: USD 100 por reefer por mes = 500/mes.** El abono se cobra por reefer vigilado, no por caja instalada (§3.4). Que ahora haya 5 módulos en lugar de 3 no cambia lo que se vigila y se registra: **5 reefers**. Cuando entre el sexto, **600/mes**. *Y esto ahora juega a favor: si preguntan "pusieron dos equipos más, ¿el mensual no sube?", la respuesta ya estaba escrita desde la v2.*

**7. El riesgo se movió, y esta vez el saldo es claramente bueno.** Está completo en §2.5:
- **(+) SE DESACTIVÓ EL RIESGO MÁS GRANDE de la v7.0: el firmware de módulo doble ya no es crítico para todo el pedido.** Los 4 módulos de interior son **simples** — 3 sondas, 1 puerta, 1 defrost — que es exactamente lo que el firmware que hoy corre en `REEFER_01_SCZ` ya hace, **sin tocar `SONDAS_MAX`** (está en 4). El doble lo necesitan **un solo módulo instalado y el repuesto**: si se atrasa, arrancan igual **4 de los 6 reefers**.
- **(+) El cable prácticamente desapareció**, y con el dato del propio Andrés: *"No es mucho lo de los cables. Los saco de acá."* Adentro no hay tirada entre reefers — cada módulo se monta en su contenedor. **De 3 tiradas (v7.0) a una sola**, la del par de afuera. **La nota al pie no cambia.**
- **(+) Una falla ciega un reefer, no dos** — salvo en el módulo de afuera.
- **(−) 5 puntos de red en vez de 3.** Es lo único que empeora, y es real: cada módulo tiene que llegar solo al WiFi del campamento. **Pasa a ser la pregunta más importante de §5.2**, y hay que contestarla antes de despachar.

**8. Tres sondas por reefer, no cuatro** (decisión de Matías). 15 sondas en servicio. El argumento de por qué más de una **sigue valiendo entero con tres**: peor punto, redundancia ante falla y verificación cruzada (tres es el mínimo que permite saber **cuál** se desvió).

**Sigue eliminada la opción C** de la v2 ("sin inversión inicial", comodato con permanencia 24 meses): *"el de la inversión inicial no lo ofrecería"* (Matías). Quedan **A** (equipos + servicio mensual) y **B** (anual adelantado).

---

## PARTE 1 — Documento del cliente (@diseno maqueta 2 páginas A4)

> Copiar de acá hasta la línea de corte. Nada más. Escrito para que **lo presente alguien que no es vendedor** y se lea en dos minutos.

**Termovigía — Monitoreo de temperatura de reefers**
**Campamento Cerro Moro (Santa Cruz) — 5 reefers en servicio**

**Qué es.** Un sistema que mide la temperatura de cada reefer las 24 horas y avisa al celular cuando algo se sale de rango. Hoy ya hay un equipo instalado y reportando desde el campamento: se puede ver en vivo en el celular antes de decidir nada. **Mientras se evalúa esta propuesta ese equipo sigue midiendo y reportando**, y el panel se puede abrir en cualquier momento: los resultados se muestran durante el proceso, no después.

**Armado según cómo está el sitio.**
- **Los 2 reefers que están a la intemperie están juntos**, así que van con **un solo módulo**, en **gabinete estanco IP65 apto para exterior**: frío, viento y lluvia son la condición normal de trabajo de ese equipo, no una excepción.
- **Los 4 reefers que están bajo techo llevan un módulo cada uno.** Así cada contenedor es independiente: si un equipo se queda sin energía no arrastra a ningún otro reefer, y no hay que pasar cable de un contenedor a otro.
- Total: **5 módulos** para los 6 reefers, y **por cada reefer siempre lo mismo: 3 sondas, 1 sensor de puerta y 1 señal de defrost**.

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

**Qué se instala.** **Un módulo de exterior** (gabinete estanco IP65, para los dos reefers que están juntos a la intemperie: uno solo atiende a los dos) y **cuatro módulos de interior, uno por cada reefer que está bajo techo**. Cada módulo trae su fuente y **2 salidas a relé**, y por cada reefer van **3 sondas, 1 sensor magnético de puerta y 1 entrada de señal de defrost**. Se suma un **kit de repuesto que queda en el campamento y puede reemplazar a cualquiera de los cinco**. El montaje lo hace personal del campamento con los equipos preconfigurados desde Bahía Blanca y guía por videollamada: por eso esta propuesta no tiene línea de instalación ni viáticos.

**Cada módulo se prueba con el cable real antes de viajar.** Los equipos no salen de una línea de montaje: **se arman y se verifican uno por uno en banco de prueba** —todas las sondas leyendo, las puertas, las señales de defrost y las salidas de alarma— y **cada módulo se prueba con 25 metros de cable puestos**, la distancia real del sitio. Para un lote que va a quedar a 1.500 km del proveedor, esa verificación es la diferencia entre un equipo que llega andando y uno que hay que diagnosticar por teléfono.

**El sexto reefer.** De los 4 reefers de adentro, uno está hoy fuera de servicio, **y su módulo se instala igual, montado y dado de alta junto con los demás**. Cuando el reefer vuelva a funcionar **no hay que comprar ningún equipo ni tocar la instalación de los otros**: se le conectan sus 3 sondas, su sensor de puerta y su entrada de defrost por **USD 260**, y el servicio mensual pasa de USD 500 a USD 600. Queda dicho acá para no tener que renegociar nada el día que pase.

**Puesta en marcha y ajuste en sitio (15 semanas, por hitos).** Los hitos son compromiso de entrega con plazo; no se facturan aparte, están incluidos en el precio. **Los plazos se cuentan desde el inicio, y el inicio es la aceptación de esta propuesta con su anticipo.**

| Hito | Qué queda funcionando | Plazo |
|---|---|---|
| 1 | El equipo que ya está instalado, con sus 3 sondas dentro del reefer, calibradas contra una misma referencia, rangos definidos y primera alerta real recibida en el celular | a las 2 semanas de iniciado |
| 2 | Los 5 módulos montados y los 5 reefers reportando; ningún dato ni aviso se pierde si se corta la red; aviso de módulo que deja de reportar; **aviso de sonda que se desvía de las otras del mismo reefer**; puertas y defrost validados en campo; una semana entera sin falsas alarmas | a las 5 semanas |
| 3 | Acceso seguro: cada módulo y cada usuario con su propia credencial | a las 10 semanas |
| 4 | Actualizaciones de los equipos a distancia, sin tocarlos | a las 12 semanas |
| 5 | Panel para la empresa (usuarios de solo lectura), accionamiento de las salidas de alarma desde el panel e informe mensual descargable | a las 15 semanas |

**Qué cuesta.**

| Concepto | USD |
|---|---|
| Módulo de exterior para los dos reefers que están juntos a la intemperie (gabinete estanco IP65 apto para exterior, fuente, 2 salidas a relé, y por cada reefer 3 sondas + sensor de puerta + entrada de defrost; probado en banco con 25 m de cable) — 1 × 700 | 700 |
| Módulo para un reefer bajo techo (gabinete, fuente, 2 salidas a relé, 3 sondas + sensor de puerta + entrada de defrost; probado en banco con 25 m de cable) — 4 × 600 | 2.400 |
| Kit de repuestos en sitio (1 módulo completo armado y probado, que puede reemplazar a cualquiera de los cinco, + 3 sondas + 1 sensor de puerta) | 350 |
| Puesta en marcha y ajuste en sitio, 5 hitos | 1.550 |
| **Total equipos y puesta en marcha** | **5.000** |
| **Servicio mensual** — **USD 100 por reefer por mes**, 5 reefers en servicio (nube, alertas, soporte, reposición sin cargo, informe mensual) | **500 / mes** |

*No incluye cable ni tendido entre reefers.*

**Cómo se paga.** **50 % con la orden de compra** (anticipo de materiales) y **50 % contra los equipos instalados y reportando**. El servicio mensual arranca con el primer equipo andando.

| | **A. Equipos + servicio mensual** | **B. Anual adelantado** |
|---|---|---|
| Para quién | Compra activos y paga el servicio mes a mes | Tiene presupuesto de inversión y no quiere 12 facturas |
| Equipos y puesta en marcha | USD 5.000 (50 % con la OC, 50 % contra instalación) | Incluidos |
| Pago inicial total | USD 5.000 | USD 10.400 (equipos + 12 meses de servicio, con 10 % de descuento sobre el servicio) |
| Mensual | USD 500 — USD 100 por reefer, completo desde el primer mes | — el primer año; renovación anual USD 5.400 |
| Los equipos | Son del cliente | Son del cliente |
| **Total a 12 meses** | **11.000** | **10.400** |
| **Total a 24 meses** | **17.000** | **15.800** |

Facturación en dólares estadounidenses. De abonarse en pesos, se toma el tipo de cambio vendedor del Banco de la Nación Argentina de la fecha de pago. *Referencia al 4-sep-2026 (BNA vendedor $ 1.535): USD 5.000 ≈ $ 7.675.000 · USD 500 ≈ $ 767.500 · USD 10.400 ≈ $ 15.964.000.*

**Incluido en el servicio mensual:** nube con 12 meses de historial · alertas por temperatura, puerta abierta, sonda caída y equipo mudo · reposición sin cargo de cualquier módulo o sonda fallada, envío incluido · actualizaciones · soporte por WhatsApp y teléfono el mismo día hábil · informe mensual por reefer.

**Lo que hay que saber.** El sistema avisa; no garantiza la mercadería ni reemplaza la revisión del reefer. Sin energía en el módulo no mide: lo que avisa en ese caso es la nube, diciendo que dejó de reportar. La entrada de defrost necesita que el reefer tenga una señal o un contacto accesible; si alguno no lo tiene, esa entrada queda libre y el resto funciona igual. Las 2 salidas a relé vienen en el módulo; la sirena o baliza que se conecte no está incluida. Cada módulo necesita llegar a la red del campamento. El tendido del cable entre los dos reefers de la intemperie lo hace el cliente. Si un módulo de interior se queda sin energía queda **ese** reefer sin vigilancia; si es el de exterior, quedan los **dos** de la intemperie: para eso está el módulo de repuesto en el campamento. Los plazos de los hitos 1 y 2 suponen que el montaje en sitio se hace dentro de la ventana prevista, que depende de personal del campamento.

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
| **"Son aprox 20/25 metros, el problema es que hay que pasar los cables con caño Daisa"** | Andrés, WhatsApp **3-sep 23:33** |
| **2 reefers están a la intemperie y JUNTOS; 4 están adentro, bajo techo** | Andrés a Matías, **4-sep** |
| **De los 4 de adentro, uno está fuera de servicio: hoy hay 5 reefers activos** | Matías, 4-sep |
| Ya se mandó al sitio una **caja estanca IP65 apta para exterior** | Matías, 4-sep |
| **CONFIGURACIÓN DEFINITIVA — Matías: *"¿los de afuera uno, y los otros uno cada uno sería?"* → Andrés: *"Así sería"*** | Chat, **4-sep 15:23**. Es el dato que fija esta versión |
| **"No es mucho lo de los cables. Los saco de acá."** — el cable lo resuelve el sitio | Andrés, **4-sep 15:23** |
| **Andrés ya recibió el PDF de la v6.1 (4 módulos, USD 4.600)** | WhatsApp, **4-sep 14:01**. Condiciona el mensaje de §6.1 |
| **Firmware de módulo doble: escrito y en auditoría, veredicto APTO CON CORRECCIONES** | `C:\Proyectos\frioseguro-v31\firmware_modular\VERIFICACION_V3.1_2026-09-04.md` — correcciones en curso |

### 2.2 Qué módulo va en cada reefer

| Ubicación | Reefers | Módulos | Gabinete | Por módulo |
|---|---:|---|---|---|
| **Intemperie** (los 2 están **juntos**) | 2 | **1 doble** | **IP65 estanco de exterior** (Roker PRG357, $ 44.419) | 6 sondas, 2 puertas, 2 defrost |
| **Bajo techo** | 4 (uno hoy fuera de servicio) | **4 simples, uno por reefer** | interior (Genrod IP65 210×310×110, $ 21.203) | 3 sondas, 1 puerta, 1 defrost |
| Repuesto en el campamento | — | **1 doble** | interior | armado y probado, cubre a cualquiera de los 5 |
| **Total** | **6** | **5 instalados + 1 repuesto** | | |

> Las v4 y v5 discutieron dos versiones enteras si convenía un equipo por reefer o uno cada dos. La v7.0 se fue del todo al "uno cada dos". **El 4-sep 15:23 el sitio zanjó la discusión: adentro, uno por reefer; afuera, uno para los dos que están pegados.**

**La regla que quedó, en una frase:** *se comparte módulo sólo cuando los dos reefers están físicamente pegados — y en este sitio eso pasa únicamente afuera. Adentro, uno por reefer.* **Y es la que dijo el sitio, no la que dedujimos nosotros.**

**Qué se gana:**
- **Cero cable entre reefers de interior.** Cada módulo se monta en su contenedor. De **3 tiradas** (v7.0) a **una sola**, la del par de afuera. Andrés lo cerró él mismo: *"No es mucho lo de los cables. Los saco de acá."*
- **Los 4 de interior corren el firmware que YA anda.** 3 sondas (`SONDAS_MAX` está en 4), 1 puerta, 1 defrost: es literalmente lo que hace hoy `REEFER_01_SCZ`. **El firmware de módulo doble deja de ser crítico para el pedido entero** (§2.5 punto 2).
- **Una falla ciega un reefer, no dos** — salvo en el módulo de afuera.
- **El módulo del reefer fuera de servicio queda instalado y de alta**, no colgado de un canal libre ajeno: el sexto entra sin abrir ninguna otra caja.
- **La plataforma se reparte entre 5 módulos vendidos, no entre 3**: USD 333 → **200 por módulo**. Es lo que permite que el simple siga costando USD 600 como en la v6.1 **pero con margen sano** (31,7 %) en vez del 25 % flaco, y que el doble caiga en 700 (§3.1).
- **El repuesto cubre el 100 % del parque con una sola caja**: los 5 módulos son la misma placa (`BOM_CERRO_MORO.md` §1).

**Qué se pierde, y hay que tenerlo escrito:**
- **5 puntos de red en vez de 3.** Es lo que más empeora y es el precio de tener un módulo por reefer: cada uno tiene que llegar solo al WiFi del campamento. Pregunta 1 de §5.2. Si alguno queda corto, repetidor **antes** de despachar.
- **5 altas remotas, credenciales y OTA** en vez de 3: +4 h de puesta en marcha (§3.2).
- **Un equipo más que comprar, armar, probar y despachar**, y **6 bultos** en vez de 4.

**El riesgo del bus, ahora acotado a UNA tirada.** Andrés dijo *"son aprox 20/25 metros"* (3-sep 23:33) y el límite prudente que fijó @muestreador para este bus es **15 m**; además el cable ata las masas de **dos contenedores metálicos con puesta a tierra separada** por el hilo de datos (`ALCANCE_1WIRE.md` §2.6: *"el riesgo dominante de esta instalación"*). **Con esta configuración eso aplica a un solo módulo: el de afuera.** Los 4 de interior tienen las 3 sondas dentro de su propio reefer, con el módulo al lado: tiradas cortas, sin cruce de tierras entre contenedores. **Matías conoce el dato y acepta el riesgo.** Mitigaciones que se mantienen:

- **Pull-up de 2k2 con posición alternativa de 1k** en la placa (@esquematico lo está poniendo). El 1k es la carta que se juega si el bus no cierra a 25 m.
- **Los 5 módulos se prueban en banco con 25 m de cable real antes de despachar**, con todas sus sondas colgadas. No sale nada que no haya cerrado a la distancia real.
- **Especificación de cable** (par trenzado exterior, el par DQ/GND junto, sin empalmes, canalizado): **queda interna**, no se manda al cliente — el cable no lo provee Matías. **Pero si Andrés pregunta qué comprar para el tramo de afuera, se le dice, y ahí no se negocia.**
- Si aun así el bus de afuera no cierra en sitio, la salida técnica existe y es barata: segundo bus con su propio pin, o repetidor 1-Wire. **No hay escenario en el que haya que devolver plata.**

**Lo que NO se le dice al cliente:** que esto es un riesgo. En el documento va la nota de que el cable y el tendido no están incluidos, y nada más sobre el cable. La mitigación real (prueba de banco con 25 m) tampoco se explica: se hace y punto.

**Y el tendido no se cotiza** (decisión de Matías, textual: *"no contemples el tema de las tiradas"*). La cuenta del caño de la v5 queda archivada en §3.3 **como historia y como argumento**, no como renglón: el precio que mandamos es firme y no depende de nada que pase en una zanja.

### 2.3 Qué lleva cada módulo, y qué de eso anda HOY (verificado en el código el 3-sep)

| Función | Simple de interior (×4) | Doble de exterior (×1) | Qué hace el firmware hoy | Evidencia |
|---|---|---|---|---|
| Sondas DS18B20 | **3** | **6** | Cada una identificada por ROM de 64 bits y reportada por separado; enganche en caliente; aviso si se desconecta; **offset de calibración por sonda en NVS**. **`SONDAS_MAX` está en 4: alcanza tal cual para los simples; sólo el doble pide subirlo a 8** — es el tamaño de un arreglo, una línea | `sondas.h`: `sondasEscanear`, `sondasLeer`, `sondasCalibrar`; línea 31 |
| **Verificación cruzada entre sondas** | — | — | **NO existe.** `sondasCalibrar()` iguala las sondas en un momento dado; el lazo de lectura **no compara sondas entre sí** ni alerta por deriva | ídem. Vendida en el **hito 2**, con la aclaración escrita en la página del cliente |
| Sensor de puerta | **1** | **2** | Implementado **para una sola puerta**: GPIO5, alerta por puerta abierta > 180 s, suprime la alerta de temperatura mientras está abierta. Viene deshabilitado por defecto (`SENSOR_DOOR_ENABLED false`). **Los 4 simples usan lo que ya está; la segunda puerta hace falta sólo en el doble** | `config.h` 72-74, 105, 119 · `.ino` 804-890 |
| Entrada de defrost | **1** | **2** | Implementada **para una sola entrada**: GPIO33, NA/NC configurable, deshabilita alertas durante el ciclo con 30 min de enfriamiento. **La segunda hay que agregarla sólo en el doble, y tiene que silenciar solo el reefer que descongela** | `config.h` 91-96, 122 · `.ino` 54-55, 100-101, 872-878 |
| Salidas a relé | 2 | 2 | **1 gobernada**: GPIO26, se activa sola con la alerta si `relayEnabled`. La segunda queda cableada y disponible. **El accionamiento manual desde el panel NO existe** | `config.h` 76-77, 140-150 · `.ino` 369-375, 483-488, 915-944 · `comandos_nube.h` sin comando de relé → **hito 5** |
| Gabinete | Genrod IP65 210×310×110, **$ 21.203** | Roker PRG357 IP65 200×200×155, **$ 44.419** | — | `BOM_CERRO_MORO.md` §3 · caja de exterior ya enviada al sitio (4-sep) |

**Es la misma placa en los cinco.** La Mini se puebla entera (6 sondas + puertas + 2 defrost + 2 relés) y en el simple simplemente **se cablean menos borneras** (`BOM_CERRO_MORO.md` §1). Una PCB, un firmware, un stock de repuestos — y el repuesto doble reemplaza a cualquiera de los cinco.

**Regla de venta.** Lo que **no** está andando hoy y va vendido con hito, nunca como característica de hoy:
- **Segunda puerta, segundo defrost por reefer y `SONDAS_MAX` a 8** — el software del módulo doble. Costeado en §3.2, hito 2. **Ahora sólo lo necesitan el módulo de afuera y el repuesto.**
- **Verificación cruzada entre sondas** — hito 2.
- **Accionamiento manual del relé desde el panel** — hito 5.

**Lo que esta configuración desactiva, y hay que decirlo:** en la v7.0 los tres módulos eran dobles y **sin firmware doble no reportaba nadie**. **Acá los 4 de interior son simples y corren lo que ya anda hoy en `REEFER_01_SCZ`**, así que el firmware doble queda como requisito de **un solo módulo instalado más el repuesto**: si se atrasa, **arrancan igual 4 de los 6 reefers**. Estado real: **escrito y en auditoría** — `C:\Proyectos\frioseguro-v31\firmware_modular\VERIFICACION_V3.1_2026-09-04.md`, veredicto **APTO CON CORRECCIONES**, correcciones en curso. **No se vende como cosa hecha: se vende en el hito 2, como siempre.**

**Detalle que no se puede pasar por alto en el diseño del doble:** **el defrost de un reefer no puede silenciar las alarmas del otro.** Hoy el defrost deshabilita *todas* las alertas del equipo. En el módulo doble tiene que silenciar **solo las sondas del reefer que está descongelando**. Está dentro de las horas de §3.2 y hay que probarlo antes del hito 2. **Ahora afecta a 1 módulo y 2 reefers, no a 3 módulos y 6.**

**Orden de armado:** identificación por ROM sí o sí (si se lee por índice, cuando cae una sonda la otra se reporta con el nombre equivocado). **Cuál de las dos líneas se despacha — `firmware_revival` extendido o `firmware_modular` v3.1 — lo define @firmware cuando cierren las correcciones de la auditoría del 4-sep; con esta configuración esa decisión ya NO bloquea a los 4 simples.** **Pull-up 2k2 con posición alternativa de 1k** (@esquematico), 3 hilos (nada de parasite power), 100 nF + 10 µF al pie de la sonda más lejana de cada rama. **Habilitar `SENSOR_DOOR_ENABLED`, probar la puerta y el defrost de cada canal de los 5 módulos, y correr la prueba de banco con 25 m de cable en los cinco antes de despachar.**

### 2.4 Lo que se instala, y quién

**Módulo doble de exterior (×1, para el par de afuera):** **gabinete estanco IP65 apto para exterior** (Roker PRG357 200×200×155), fuente de 5 V 2 A, placa Mini con borneras a tornillo, ESP32 en zócalo, módulo de 2 relés, **prensacables en todas las entradas**, 6 sondas DS18B20 estancas, 2 reed de puerta, 2 entradas de defrost.
**Módulo simple de interior (×4, uno por cada reefer bajo techo):** gabinete IP65 de interior (Genrod 210×310×110 o las de stock si pasan la medición `M9`), **la misma placa**, 3 sondas, 1 reed, 1 defrost.
**Kit de repuesto (×1):** un **módulo doble** completo — la placa es la misma en los cinco, así que **cubre a cualquiera** — + 3 sondas + 1 reed. Va con gabinete de interior: **si el que falla es el de afuera, la electrónica se pasa a la caja estanca que ya está en sitio** (queda escrito en el runbook).
**El cable no lo mandamos** (decisión del 4-sep): adentro no hace falta tirada entre reefers, y la del par de afuera la provee y la hace el cliente (*"los saco de acá"*, Andrés).

**Montaje: Andrés (o quien la empresa designe), con kit preconfigurado y probado en banco + videollamada.** Dos pasajes a Santa Cruz, alojamiento, inducción y 5 días de ingeniero rondan los $ 2.500.000, y Matías no puede viajar en octubre (parada de Dreyfus). Eso es lo que esta propuesta no cobra.

**Intemperie: en el documento del cliente se dice "gabinete estanco IP65 apto para exterior" y nada más.** Ni material, ni proceso de fabricación, ni impresión 3D. Ni en el PDF ni en el WhatsApp.

### 2.5 Los riesgos técnicos abiertos

1. **⚠ EL RIESGO QUE SUBIÓ: cobertura de red en 5 puntos**, contra 3 en la v7.0 y 4 en la v6.1. Es el peor número de todas las versiones y es el precio de tener un módulo por reefer: cada uno tiene que llegar solo al WiFi del campamento. Si alguno queda corto se resuelve con un repetidor barato, **pero hay que saberlo antes de despachar**. Pregunta 1 de §5.2 — **ahora es la pregunta más importante de la lista**, y no frena el envío pero sí lo condiciona.
2. **✅ EL RIESGO QUE BAJÓ, y era el más grande: el firmware de módulo doble ya no es crítico para todo el pedido.** En la v7.0 los tres módulos eran dobles y sin ese firmware no reportaba nadie. **Acá los 4 simples corren lo que ya anda hoy en `REEFER_01_SCZ`** (3 sondas ≤ `SONDAS_MAX` 4, 1 puerta, 1 defrost). El firmware doble lo necesitan **el módulo de afuera y el repuesto**: si se atrasa, **arrancan igual 4 de los 6 reefers** y el hito 2 se cumple parcial en vez de caer entero. Estado real, verificado: `C:\Proyectos\frioseguro-v31\firmware_modular\VERIFICACION_V3.1_2026-09-04.md`, **APTO CON CORRECCIONES**, correcciones **en curso**. **Sigue habiendo que cerrarlo, pero salió del camino crítico de la venta** — y eso hay que decírselo al Director.
3. **✅ Una sola tirada de 20-25 m, la de afuera** (eran 3 en la v7.0). Riesgo asumido, mitigaciones en §2.2. Interno: cable apto exterior, sin empalmes, canalizado. Adentro no hay cruce de tierras entre contenedores porque no hay cable entre contenedores.
4. **El defrost cruzado** (§2.3): que el descongelamiento de un reefer no ciegue al otro. **Ahora aplica a 1 módulo y 2 reefers**, no a 3 módulos y 6. Trabajo de software, costeado, y es lo que hay que probar antes del hito 2.
5. **Si cae un módulo de interior queda 1 reefer ciego; si cae el de afuera, 2.** Mejor que la v7.0, donde cualquier caída ciegaba dos. Mitigación real y ya cotizada: el **módulo de repuesto queda en el campamento** y sirve para cualquiera de los cinco.
6. **La caja de exterior a la intemperie de Santa Cruz** es la única parte del equipo sin antecedente de campo largo, y **de ella dependen 2 reefers**. La que se mandó al sitio el 4-sep es, de hecho, **la prueba de campo**: conviene pedirle a Andrés una foto después del primer temporal.
7. **Plazo de fabricación — el cuello nuevo.** @hardware avisa (`BOM_CERRO_MORO.md` §7.2) que con la PCB Mini el despacho realista es **semana 4-5, no 2**, y que el hito 2 caería en la **7-8**. En el documento del cliente los hitos quedan como están (decisión de mantener la v6.1); **internamente esto es lo que Matías tiene que resolver con @hardware antes de firmar**, y la salida que recomienda @hardware es **pedir la PCB ahora** (USD 43, sirve igual para las demos de Bahía si Cerro Moro no compra).

### 2.6 Opcionales, después de la primera orden

**El sexto reefer cuando vuelva a servicio: USD 260 + USD 100/mes** — **su módulo ya está instalado y de alta**, así que es conectar 3 sondas, el reed y el defrost, sin abrir la caja de ningún vecino. El precio no cambió respecto de la v7.0 porque los componentes son exactamente los mismos; lo que cambió es que ahora no depende de que quede un canal libre. Ya está escrito con precio en el documento del cliente: no hay que venderlo de nuevo, solo ejecutarlo. **Es el upsell más probable y el de mejor margen de esta cuenta.** · **Sirena o baliza: a USD 40 NO deja margen** — @hardware midió que la BR300 de exterior sale $ 39.530 (USD 26) **más su propia fuente de 12 V**, porque el relé entrega contacto seco (`BOM_CERRO_MORO.md` §4.5). **Propuesta: USD 70 instalada**, o baliza LED de 12 V que es mucho más barata. **Decide Matías.** · **cuarta sonda** en un reefer (USD 40 + USD 5/mes) · base con batería y 4G, la única que avisa el corte de energía por sí misma (a cotizar) — **especialmente vendible para el módulo de la intemperie, del que ahora dependen dos reefers**. Se ofrecen cuando las sondas estén andando, no antes.

---

## PARTE 3 — Números de respaldo

Base: **`BOM_CERRO_MORO.md` rev A (@hardware, 4-sep)**, precios de MercadoLibre AR y JLCPCB verificados en vivo ese día. Cambio $ → USD al BNA vendedor 1.535.

### 3.1 Los tres precios, con el MISMO margen: simple 600 · doble 700 · repuesto 350

| | Simple interior (ARS) | USD | Doble exterior (ARS) | USD |
|---|---:|---:|---:|---:|
| Electrónica: ESP32 + módulo de 2 relés + fuente 5 V 2 A + PCB Mini prorrateada + consumibles de placa y prensacables | ~46.000 | **30** | ~46.000 | **30** |
| **Gabinete** — interior Genrod IP65 210×310×110 **$ 21.203** · exterior **Roker PRG357 IP65 200×200×155 $ 44.419** | 21.203 | **14** | 44.419 | **29** |
| Sondas DS18B20 estancas moldeadas de 3 m ($ 10.587 c/u): **3** en el simple, **6** en el doble | 31.761 | **21** | 63.522 | **41** |
| Sensores magnéticos de puerta cableados: 1 / 2 | 8.137 | **5** | 16.274 | **11** |
| Envío a Santa Cruz, prorrateado en 6 bultos | | **10** | | **12** |
| Armado + **prueba de banco documentada con 25 m de cable** + garantía de reposición amortizada | | **130** | | **150** |
| Parte de plataforma del desarrollo: USD 1.000 repartidos en **5** módulos vendidos | | **200** | | **200** |
| **Costo** | | **410** | | **473** |
| Margen (**~32 % en los dos**) | | **190** | | **227** |
| **Precio** | | **600** | | **700** |

**El margen elegido: 32 % sobre el precio de venta, igual en los tres ítems.** Matías liberó el precio del doble (*"no dejes fijado a 850 el exterior... pensalo vos bien"*), así que lo pensé desde el costo. **Por qué 32 y no 25:** el 25 % que tenía el simple es margen de reventa, no de producto propio con soporte, garantía de reposición con envío incluido y respuesta a **1.500 km** — donde **una sola placa que haya que rehacer se come USD 90 y un viaje se come el margen entero** (@hardware, `BOM_CERRO_MORO.md` §6). **Por qué 32 y no 40:** este es el **primer** cliente del producto y es una corrida de 6 unidades, la más cara que vamos a hacer nunca — la PCB sola pasa de USD 4,31 a ~1,9 por placa a 20 unidades. Y **el equipo es el ticket de entrada, no el negocio: el negocio es el abono al 74 %.** Un inicial caro pone en riesgo lo único que importa, que es el 500/mes.

**Los tres precios, para que Matías pueda defender cualquiera sin abrir nada más:**

| Ítem | Costo | Margen | **Precio** | % |
|---|---:|---:|---:|---:|
| **Simple de interior** (×4) | 410 | 190 | **600** | **31,7 %** |
| **Doble de exterior** (×1) | 473 | 227 | **700** | **32,4 %** |
| **Repuesto doble** (×1, sin cargo de plataforma) | 232 | 118 | **350** | **33,7 %** |
| **Total equipos + repuesto** | **2.345** | **1.105** | **3.450** | **32,0 %** |

**Por qué el doble sale 700 y no 1.200: la cuenta, renglón por renglón.** Es lo que hay que mostrar si alguien pone los dos precios uno al lado del otro — y en una compra corporativa eso pasa siempre.

| Renglón | Simple | Doble | ¿Se duplica? |
|---|---:|---:|---|
| ESP32 + fuente + módulo de relé + PCB + consumibles | 30 | 30 | **NO** — es **un solo equipo** |
| Gabinete | 14 (Genrod interior) | 29 (Roker estanco) | no se duplica, pero **la caja de exterior cuesta el doble** |
| Sondas DS18B20 | 21 (3) | 41 (6) | **SÍ** |
| Reed de puerta | 5 (1) | 11 (2) | **SÍ** |
| Envío prorrateado | 10 | 12 | casi no — **un solo bulto** |
| Armado + prueba de banco con 25 m | 130 | 150 | no — **la misma placa**, más canales que verificar |
| Plataforma (USD 1.000 / 5 módulos) | 200 | 200 | **NO** — **un solo alta remota, una sola credencial, una sola OTA, un solo punto de red** |
| **Costo** | **410** | **473** | **+63** |
| **Precio a 32 %** | **600** | **700** | **+100** |

**En una frase, y es el argumento de venta:** *dos reefers pegados se cubren con un equipo, y por eso salen **700 en vez de 1.200**. El cliente se ahorra **USD 500** por el solo hecho de que esos dos contenedores estén al lado.* **Se duplica lo que va adentro del reefer (sondas y reed); no se duplica lo que va adentro de la caja.** Y a diferencia de la versión con el doble a 850, **acá el desglose se puede abrir sin que quede nadie mal parado**: los tres ítems tienen el mismo margen.

**El margen del conjunto sube de 23 % a 32 %, y ahora es parejo.** Ingreso de equipos + repuesto: **4 × 600 + 700 + 350 = USD 3.450**. Costo directo: 4 × 410 + 473 + 232 = **USD 2.345**. **Margen USD 1.105 = 32,0 %.** Cruza contra la cuenta independiente de @hardware (`BOM_CERRO_MORO.md` §6, que da 27,6 % para 5 placas con **dos** cajas de intemperie y la plataforma repartida distinto): **la diferencia es exactamente el reparto entre 5 módulos y la segunda caja Roker que ya no se compra.** Cierra. *Dato para que no se pierda: el ingreso total y el margen total son **idénticos** a los de la versión con el doble a 850 — lo único que cambió es **cómo se reparte entre los ítems**. Por eso el total sigue en 5.000 y el WhatsApp no cambia de cifra.*

**Dónde está la plata de esta cuenta, igual:** en el **abono (74 % de margen, §3.4)** y en la **puesta en marcha**. Los equipos son el ticket de entrada, no el negocio. **Eso es exactamente el modelo de PLATA.md** — y por eso el abono no se toca ni un dólar aunque el inicial haya subido 400.

**Por qué el total quedó en 5.000 otra vez, y por qué no lo forcé.** Los precios salieron de aplicar 32 % al costo de cada ítem y redondear cada unitario a la decena: **600, 700 y 350**. **La suma dio 5.000 sola** (con los unitarios sin redondear da 4.998,4). **Es coincidencia y la digo como tal:** la versión anterior también daba 5.000 con el doble a 850 y el simple a 550, porque lo que se movió fue el reparto, no la torta. Se podía haber puesto el simple en 620 para llegar a 5.100 o en 575 para "amortiguar" la suba: **no se hace ninguna de las dos.** El cliente que ve unitarios redondos con margen parejo entiende que el número está calculado y no negociado, y eso es lo que hace creíble el 500/mes, que es donde está el negocio.

**Cómo se sostiene la diferencia contra los USD 4.600 que Andrés ya vio (v6.1, 14:01 de hoy).** En dos líneas, que es lo que hay que poder decir por teléfono: **(1) hay un equipo más — 5 módulos en vez de 4 — porque cada reefer de adentro lleva el suyo, que es lo que él confirmó a las 15:23; (2) eso agrega un reefer entero con su propio módulo y saca todo el cable entre contenedores de adentro.** **El unitario del módulo de interior no subió: sigue en USD 600, el mismo número de la v6.1** — y ahora esos 600 son por una caja de interior, no por una estanca de intemperie. **+USD 400 sobre 4.600 = +8,7 %, y el abono no se movió.**

**El repuesto baja de 400 a USD 350**, por el mismo criterio de margen parejo (costo 232, 33,7 %). Cubre **el 100 % del parque** con una sola caja, porque los 5 módulos son la misma placa. **Es el único renglon que baja respecto de la primera cuenta de la v8, y baja porque no había motivo para que llevara más margen que el resto.**

### 3.2 Puesta en marcha, USD 1.550

| Trabajo | h |
|---|---:|
| Sondas, rangos y umbrales por reefer + **calibración de las 15 sondas** contra referencia y registro de offsets | 10 |
| **Software del módulo doble: segunda puerta, segundo defrost con silenciado por reefer, `SONDAS_MAX` a 8, validación del bus a 25 m** | 10 |
| Registro exportable con código de verificación | 14 |
| Panel multi-equipo y usuarios de lectura | 10 |
| Puesta en marcha remota (alta, credencial, OTA verificada, prueba de puerta y defrost), pruebas de campo con Andrés, runbook y capacitación — **5 módulos** | 14 |
| Salud de bus, histéresis de 3 barridos y **verificación cruzada entre sondas** | 4 |
| **Total a USD 25/h** | **62 = USD 1.550** |

**Subió de 58 a 62 h, y sube sólo en el renglón que corresponde: la puesta en marcha remota por módulo.** Son **5 altas, 5 credenciales, 5 OTA verificadas y 5 pruebas de puerta y defrost** en vez de 3. La serie de las versiones anteriores era 3 módulos → 10 h y 4 → 12 h: **5 → 14 h**, o sea 2 h por módulo sobre una base de 4 h de runbook y capacitación que no depende de la cantidad. Todo lo demás queda idéntico.

**Las 10 h del software del doble NO bajan aunque ahora lo use un solo módulo instalado.** El código se escribe una vez, se use en uno o en tres, y el repuesto también lo lleva. **Lo que cambió es el riesgo, no el costo** (§2.5 punto 2). *El firmware está escrito y auditado (APTO CON CORRECCIONES, 4-sep) pero las correcciones no están cerradas. **Si @firmware dice que son más horas, salen del margen, no del precio.***

### 3.3 **LA CUENTA DEL CAÑO** — archivo, y por qué ya no entra en el precio

> Se conserva de la v5 **como historia y como argumento**, no como parte del presupuesto. **El tendido lo hace y lo paga el cliente, y no aparece en el documento que se manda.** Con la v8 queda **una sola tirada**: la del par de afuera, que está pegado y debería ser corta. **Adentro no hay tirada entre reefers** — cada módulo se monta en su contenedor.

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
1. **Saber el tamaño de lo que el cliente gasta por su lado** — y con esta configuración es **una sola tirada corta entre dos contenedores pegados**, mucho menos que esta cuenta, que además **Andrés ya dijo que resuelve él** (*"no es mucho lo de los cables, los saco de acá"*). Si igual dicen "esto de la obra no lo teníamos previsto", la respuesta ya está: **la configuración la describieron ellos**.
2. **La variante de rescate ya está aplicada.** Era *"un módulo por reefer, sin obra"* — y es exactamente lo que ahora se cotiza adentro. **Ya no hay obra que pueda frenar la venta salvo en el par de afuera.**
3. **Que nadie regale la instalación.** Si aparece la tentación de "se lo hacemos nosotros para cerrar", el número a tener en la cabeza es **USD 286 por tirada**, más pasajes y estadía.

### 3.4 Servicio mensual: qué cuesta servir y qué se cobra

| Costo directo mensual | v2 (12 sondas) | **v8.0 (15 sondas, 5 reed, 5 módulos)** |
|---|---:|---:|
| Supabase Pro | 25 | 25 |
| Reposición amortizada (módulos y sondas en garantía) | 10 | **18** |
| Soporte (2 h → 2,5 h a USD 25) | 50 | **62** |
| Informe mensual | 25 | 25 |
| **Total** | **110** | **130** |

*(Reposición y soporte suben respecto de la v7.0 —15 y 57— porque hay 5 equipos en campo, no 3.)*

**Tarifa: USD 100 por reefer por mes × 5 = USD 500/mes** (decisión de Matías, 4-sep, **no se toca con la configuración nueva**). Costo directo 130 → **margen bruto USD 370 (74 %)**. **Con el inicial en 5.000, el abono paga el equipamiento entero en 13,5 meses de margen: sigue siendo el renglón que sostiene la cuenta.** La justificación, y es la que hay que decir si preguntan: **mantenimiento del servidor, custodia de los datos y seriedad del servicio** — el registro que se entrega tiene que estar disponible y ser defendible dentro de un año, y eso se paga todos los meses aunque no pase nada.

**El abono es estrictamente proporcional a los reefers, no a los equipos**: 5 reefers = 500, 6 = 600. **Eso es lo que permite mover el inicial sin tocar el abono**: pasamos de 3 cajas a 5 y se vigila lo mismo — 5 reefers. Y **ahora juega a favor**: si alguien intenta *"pusieron dos equipos más, ¿el mensual no sube?"*, la respuesta está escrita desde la v2: **el servicio se cobra por reefer vigilado, no por caja instalada.** **Cuando entre el sexto, los USD 100 adicionales son casi margen puro** y el equipo ya está puesto.

**El escalón de los primeros 3 meses al 50 % sigue eliminado** (decisión de Matías, 4-sep): abono completo desde el primer mes en las dos formas. Lo justifica que el servicio ya está corriendo —servidor, custodia y guardia de alertas— desde el primer equipo que reporta.

### 3.5 Condiciones de pago — 50 / 50, y por qué no 25

**50 % con la orden de compra (anticipo de materiales) y 50 % contra los equipos instalados y reportando.** El abono arranca con el primer equipo andando.

El fundamento es de caja: hay que comprar y armar **6 módulos** (5 + el repuesto) antes de ver un peso del segundo tramo, y cobrar ese tramo a un contratista que todavía no tiene nombre. Con el 50 % (**USD 2.500 ≈ $ 3.837.500**) la compra completa de materiales —**≈ $ 821.000, §3.7**— queda cubierta **más de cuatro veces** antes de tocar un componente. Con el 25 % (USD 1.250 ≈ $ 1.919.000) también alcanzaría para los materiales; lo que no cubriría es el **riesgo de cobranza del segundo tramo**, que es lo que en realidad se está financiando. *(La holgura cayó de 8× a 4× respecto de la v7.0 porque el BOM real de @hardware es más caro que la estimación vieja de perfboard — sigue siendo cómoda, pero ya no es infinita.)*

Los hitos siguen existiendo **como compromiso de entrega con plazo**, y así está escrito en el documento del cliente: *"no se facturan aparte, están incluidos en el precio"*. **Punto para que Matías confirme:** cobrar antes de entregar los hitos es más cómodo para la caja y más exigente con la palabra.

### 3.6 Las dos formas de pagar, y por qué se cayó la tercera

**A. Equipos + servicio mensual.** 5.000 + 12 × 500 = **11.000** el primer año; 6.000/año después; **24 meses 17.000**.

**B. Anual adelantado, 10 % de descuento sobre el año de servicio.** 5.000 + (12 × 500) × 0,9 = 5.000 + 5.400 = **USD 10.400**; renovación 5.400/año; **24 meses 15.800**. El descuento le ahorra **USD 600 el primer año** y lo que compra es concreto: **cero riesgo de cobranza durante 12 meses con un contratista que probablemente pague a 60-90 días, una factura en lugar de doce, y caja para armar los equipos.**

**C, eliminada.** Matías: *"el de la inversión inicial no lo ofrecería"*. Era la única que ponía USD ~5.000 nuestros en manos de un contratista a 1.500 km, sin poder retirar los equipos y sin contrato con permanencia. **No se vuelve a ofrecer sin contrato validado por contador y un cliente con historial de pago.** Con dos opciones el comprador elige; con tres se paraliza.

**Sin cláusulas condicionales.** La propuesta no tiene condición de metros, ni de canalización, ni corrección de precio: **el tendido es del cliente y el precio es firme.**

### 3.7 **Los 6 módulos: qué falta comprar y cuánto sale**

**Qué hace falta.** 6 placas Mini: **1 doble de exterior + 4 simples de interior + 1 doble de repuesto**. Gabinetes: **1 de intemperie + 5 de interior**. Sondas: 15 instaladas + 3 de repuesto = **18**. Reed: 5 instalados + 1 de repuesto = **6**. Defrost: 5 entradas (cable y bornera, sin componente caro). Reservados **3 ESP32 para las galgas de Dreyfus**, que es P0 de octubre.

**La cuenta arranca del BOM real de @hardware, no de la estimación vieja.** `BOM_CERRO_MORO.md` rev A costeó **5 placas** en escenario RECOMENDADO (sondas moldeadas de 3 m + gabinetes de interior nuevos) en **$ 828.490 ≈ USD 541**. De ahí a la v8:

| Ajuste a la v8 | $ |
|---|---:|
| **+1 placa** (6 en vez de 5): 1 ESP32 más ($ 14.999), 1 fuente más ($ 10.579), 1 gabinete de interior más ($ 21.203) y su juego de consumibles, borneras, optos y prensacables | **+$ 80.000** |
| **−1 caja Roker de intemperie**: la v8 tiene **un** módulo de exterior, no dos | **−$ 44.419** |
| **−1 rollo de UTP Cat5e exterior**: sin tiradas entre reefers de interior alcanza **1 rollo de 50 m** para la prueba de banco (el cable del tramo de afuera lo pone el cliente) | **−$ 43.200** |
| Sondas (18), reeds (6) y módulos de relé: **sin cambio** | 0 |
| **TOTAL v8** | **≈ $ 821.000 ≈ USD 535** |

**Bajan si:** las 3 cajas IP65 de stock pasan la medición **`M9`** (**−$ 63.609**) y las 5 fuentes de stock resultan de **2 A** (**−$ 52.895**). **Las dos mediciones juntas valen USD 76 y son 10 minutos con un calibre** (`BOM_CERRO_MORO.md` §7.1).

⚠ **Corrección honesta contra las versiones anteriores:** el §3.7 de la v7.0 decía ≈ $ 375.000 de compra. **Ese número era del Kit v1 de perfboard con sondas rearmadas y sin PCB.** Con la Mini (PCB fabricada + sondas moldeadas de 3 m, que evitan 18 empalmes dentro de un reefer a −20 °C) el número real es el de arriba. **El margen igual cierra en 32 %** (§3.1) porque el ingreso también subió al haber más módulos.

**Contra el anticipo del 50 % (USD 2.500 ≈ $ 3.837.500), la compra completa es el 21 %.** No hay problema de plata ni de cantidades. **La caja IP65 de intemperie sigue siendo el renglón de mayor plazo de entrega: se pide primero** (y ya hay una en el sitio, que es la prueba de campo). Orden de pago el día de la OC (`BOM_CERRO_MORO.md` §8): **1.** caja Roker · **2.** PCB a JLCPCB · **3.** los ESP32, todos al mismo vendedor y en la misma orden (la separación de filas del DevKit de 38 p varía por fabricante) · **4.** sondas y cable, que bloquean la prueba de banco · **5.** el resto. **Nada antes del conteo de stock de 30 minutos.**

**Por qué el hito 1 SÍ es alcanzable.** El hito 1 es *"el equipo que ya está instalado, con sus 3 sondas dentro del reefer, calibradas, rangos definidos y primera alerta real"*. **No depende de que lleguen los módulos nuevos ni del firmware doble: depende de que lleguen 2 sondas** (el equipo instalado ya tiene 1, y ahora son 3 por reefer). `REEFER_01_SCZ` está montado y reportando desde el 21-ago con **1 sola sonda, y está fuera del reefer**.

**El plan arranca cuando aceptan, no antes.** Semana 0 = aceptación + anticipo del 50 %. Hasta que eso pase **no se compra, no se arma y no se despacha nada**, y a Andrés no se le pide que reserve ninguna ventana: trabaja por turnos de 15 días y no es él quien aprueba.

| Paso | Plazo desde la aceptación | Quién |
|---|---|---|
| Conteo del stock real + las mediciones `M1`-`M5` (huellas), `M7`, la `M9` (interior de las 3 cajas) y la etiqueta V/A de las fuentes | semana 0 | Gonza |
| Compra del faltante — **la caja de exterior y la PCB primero** | semana 0-1 | Gonza / Matías |
| Despacho de 2 sondas para el equipo ya instalado (encomienda, 5-8 días hábiles) | semana 1 | — |
| **Cierre de las correcciones del firmware doble** (auditoría 4-sep, APTO CON CORRECCIONES) + 2ª puerta, 2º defrost por reefer, `SONDAS_MAX` a 8 — **bloquea sólo al módulo de afuera y al repuesto** | semana 1-2 | Matías / @firmware |
| Alta, calibración remota, rangos y primera alerta real | semana 2 | Andrés + Matías |
| **HITO 1** | **semana 2** | — |
| Armado de los 6 módulos + **prueba de banco de los cinco con 25 m de cable** | semana 1-3 | Gonza / Sergio |
| Despacho de los 6 bultos (5 módulos + repuesto) a Cerro Moro | semana 2-3 | — |
| **Tendido del cable del par de afuera** (cable apto exterior) | semana 3 | **cliente** |
| Montaje de los módulos por personal del campamento | semana 3-4 | campamento |
| Alta y calibración de las 12 sondas nuevas (las 3 de `REEFER_01_SCZ` ya quedaron en el hito 1) | semana 4 | Matías |
| **HITO 2** (los 5 reefers reportando + una semana sin falsas alarmas) | **semana 5** | — |

**El riesgo que hay que decir en voz alta: el hito 2 sigue apretado, pero cambió de dueño.** Ya **no** depende del firmware doble para todo (los 4 simples arrancan con lo que ya anda hoy) **ni** de una obra ajena en tres pares (ahora es una sola tirada corta que Andrés dijo que resuelve él). **Lo que ahora lo aprieta es la fabricación:** @hardware dice que con la PCB Mini el despacho realista es **semana 4-5** y el hito 2 caería en la **7-8** (`BOM_CERRO_MORO.md` §7.2, §2.5 punto 7 de acá). **Matías no debería prometer el hito 2 por teléfono con más firmeza que la que dice el papel, y esto hay que resolverlo con @hardware antes de firmar.**

**Por qué se puede empezar a armar antes de la orden de compra, sin exponer un peso nuevo.** Los kits **ya estaban planificados como las unidades de demostración del plan comercial de Bahía**. Si Cerro Moro no compra, **no quedan colgados: van a su destino original**. **La contracara para el Director: si Cerro Moro compra, Bahía se queda sin demos, y ahora son 6 módulos, no 4.** Recomendación: **la reposición de los kits de Bahía se dispara en el mismo pedido que la orden de compra**, no después. *(Las 10 placas de JLCPCB por USD 43,10 ya contemplan las de sobra para eso: pedir 10 en vez de 5 cuesta USD 5,70.)*

### 3.8 Moneda, validez, facturación

**Facturación en USD, pago en pesos al BNA vendedor de la fecha de pago, sin validez en el PDF.** Nota interna: revisar precios si pasan más de 6 meses desde el 4-sep. Antes de la cotización firme hay que saber: monotributo vs. RI, plazo de pago, si acepta la cláusula de moneda, quién firma. Se pregunta cuando la empresa tenga nombre.

### 3.9 Contra una pérdida y contra la competencia

Una pérdida de 3 t valuada al precio de novillo en pie ($ 4.181/kg, INMAG jul-2026) son $ 12,5 M: **16 meses de servicio** al abono de USD 500 (≈ $ 767.500 por mes). testo Saveris 2-T2: USD 318 por unidad y mide **un** punto; para cubrir los 15 puntos de esta propuesta harían falta 15 unidades = **USD 4.770** antes de importación — **casi el total de esta propuesta, que es 5.000** — sin nube, sin puerta, sin relé, sin defrost, sin repuesto en sitio — y se configura con una red WiFi y una clave, que es exactamente lo que este sitio no tiene. **Y ninguna de esas unidades es apta para la intemperie sin gabinete adicional.**

---

## PARTE 4 — Puesta en marcha: qué es cada hito por dentro

Las duraciones se cuentan **en semanas desde la aceptación**, no contra el calendario. Los hitos pesados caen después de la semana 5 para no chocar con la parada de Dreyfus.

| Hito (cliente) | Etapa interna | Desde | Hasta | Cómo se acepta |
|---|---|---|---|---|
| 1 — El equipo ya instalado con sus 3 sondas adentro y calibradas, rangos, primera alerta real | E0 | semana 0 | **semana 2** | Captura de la alerta en el celular + registro en nube + **planilla de calibración con el offset de las 3 sondas de `REEFER_01_SCZ`** |
| 2 — Los 5 módulos y los 5 reefers reportando; nada se pierde, nada sobra | E1: buffer offline, alertas encoladas, alerta de sonda caída, vigía de equipo mudo, discriminador de bus + histéresis, **detección de sonda que se desvía de las otras del mismo reefer**, **segunda puerta y segundo defrost con silenciado por reefer — en el módulo de exterior y en el repuesto** | semana 2 | **semana 5** | Los 5 módulos montados con sus 15 sondas calibradas; desenchufar una sonda y que llegue la alarma; cortar la red 20 min sin perder lecturas; abrir una puerta 4 min y que avise; **forzar el defrost de uno de los dos reefers de afuera y verificar que el otro sigue alarmando**; **una semana sin falsas alarmas** |
| 3 — Acceso seguro | E2: RLS cerrada, credencial por módulo, secretos fuera del binario, revocar claves quemadas | semana 5 | **semana 10** | Con la clave vieja no se escribe; los 5 módulos siguen reportando |
| 4 — Actualización a distancia | E3: OTA con manifiesto inmutable | semana 10 | **semana 12** | Tres actualizaciones seguidas por aire al primer intento, en todos los módulos |
| 5 — Panel e informe | E4: usuarios de lectura, vista de los reefers, exportación con código, informe mensual automático, **comando de relé desde el panel** | semana 12 | **semana 15** | Un usuario de la empresa entra solo, baja el informe y acciona una salida desde el panel |

**El hito 2 es el apretado** (§3.7): la semana sin falsas alarmas arranca cuando los 5 módulos reportan, alrededor de la semana 4, y vence en la 5. **Sin colchón — pero ahora el cuello es la fabricación de la PCB, no el firmware doble (los 4 simples corren lo que ya anda) ni la obra del cliente (queda una sola tirada).**

Lo que hoy está roto y cada hito arregla (llave maestra en el binario, datos perdidos sin red, umbral en 50 °C, equipo muerto que no avisa, OTA que entra 1 de 4) está en `AUDITORIA_HALLAZGOS.md`; no cambió.

---

## PARTE 5 — Qué necesitamos para cerrar

### 5.1 De la empresa, cuando tenga nombre

Quién firma, cómo factura (monotributo/RI, plazo), si acepta la cláusula de moneda, **cuál de las dos formas de pago elige (A o B)**, y confirmación de que el montaje **y el tendido del cable del par de afuera** los hace personal del campamento (sin personal nuestro en sitio no corresponde ART ni legajo de contratista).

### 5.2 De Andrés: lo que sigue abierto

**Ninguna de estas frena el envío.**

1. **⚠ LA MÁS IMPORTANTE AHORA: ¿la red del campamento llega bien a los 5 puntos donde van los módulos?** Con un módulo por reefer son 5 puntos, no 3. Si alguno queda corto se resuelve con un repetidor barato, pero **hay que saberlo antes de despachar**.
2. **¿Los reefers tienen una señal o contacto de defrost accesible?** Si alguno no lo tiene, esa entrada queda libre y el resto funciona igual — ya está dicho así en el documento del cliente, sin letra chica. **@hardware pide además saber si es 12-24 V o contacto seco**: hay una mitigación de costo cero (dos puentes de soldadura en la placa) que hace que la misma placa sirva para las dos posibilidades, pero se define **antes de rutear**.
3. **¿Cuál de los 4 de adentro es el que está fuera de servicio?** Ya **no** cambia el armado —cada uno lleva su módulo igual— pero sirve para nombrar bien los equipos y para no salir a calibrar sondas que no están puestas.
4. **¿Cuántos metros hay entre los dos de afuera?** Es la **única** tirada que queda; están juntos, así que debería ser corta, pero es la única a la intemperie y conviene saber el número antes de armar.
5. **¿Para quién trabaja Andrés?** (empleado de PAAS o de una contratista). No es técnica: decide la Parte 7.

---

## PARTE 6 — Para Andrés (aparte del PDF)

### 6.1 WhatsApp — lo manda Matías

> **⚠ Andrés ya tiene en el celular el PDF de 4 módulos y USD 4.600: se lo mandaste hoy a las 14:01.** Este mensaje lo corrige. **Va corto y de frente, sin justificarse de más.**

```
Andrés, quedó como me confirmaste: uno por reefer adentro y uno doble
para los dos de afuera, que están juntos. Son 5 módulos, por eso sube
respecto del PDF que te mandé recién: queda en USD 5.000. El abono es
el mismo, USD 100 por reefer por mes = 500 por los cinco que andan.

El de afuera va en caja estanca para intemperie y atiende a los dos.
Los cuatro de adentro llevan uno cada uno, así que entre reefers de
adentro no hay que pasar ningún cable: queda sólo el tramo de los dos
de afuera, que lo resolvés vos como me dijiste.

Por cada reefer: 3 sondas adentro, sensor de puerta y la señal de
defrost, así no suena la alarma cada vez que descongela. Los módulos los
pruebo acá en el banco con 25 metros de cable puestos antes de
despacharlos.

El reefer que está fuera de servicio lleva su módulo igual, instalado y
andando. El día que vuelva se le conectan las sondas nomás, sin equipo
nuevo.

Te mando el presupuesto corregido, mismas dos hojas y sin nombre de
empresa. Ignorá el anterior.
```

> **Por qué está escrito así, para que no se suavice al copiarlo:**
> **(a)** **La suba va en el primer párrafo, con el motivo pegado y en la misma oración:** *"Son 5 módulos, por eso sube."* Sin preámbulo y sin disculpa. El que sube un precio con vueltas pierde exactamente lo mismo que el que lo baja sin motivo: credibilidad.
> **(b)** **Arranca con "quedó como me confirmaste".** Él dio el dato a las 15:23; lo primero que lee es que se hizo exactamente eso.
> **(c)** **Que el abono NO cambia se dice en la misma frase que la suba.** Ahí se corta la conversación de *"¿y el mensual también sube?"* antes de que exista.
> **(d)** **Se le devuelve su propia frase sobre el cable** (*"lo resolvés vos como me dijiste"*) y se remarca lo que él gana: **entre reefers de adentro no hay cable**. Es lo mejor que tiene esta configuración para el que la va a defender adentro. Lo que **no** va es la spec de cable ni la palabra riesgo (decisión de Matías).
> **(e)** **La prueba con 25 m compra confianza técnica.** Dice, sin decirlo: sé que hay distancia y me hago cargo.
> **(f)** **El sexto reefer aparece como previsión, no como recorte** — y ahora es más fuerte: *"lleva su módulo igual, instalado y andando"*.
> **(g)** **"Ignorá el anterior", explícito.** Un PDF viejo de USD 4.600 dando vueltas en un grupo de WhatsApp de la empresa es el peor escenario posible.
> **(h)** **No le pide nada.** Andrés trabaja por turnos de 15 días y **no es él quien aprueba**.
> **(i)** **No menciona el material de la caja ni cómo se fabrica.** Ni acá ni en el PDF.
> **(j)** **No se manda hasta que el PDF corregido esté listo.** Los dos juntos, o el mensaje pierde la mitad.

### 6.2 Guion de 5 líneas para que la presente él

1. **Arrancá por el problema, no por el producto:** "un reefer que se corta un fin de semana es la comida de todo el campamento, y hoy nadie se entera hasta que abren la puerta."
2. **Mostrá lo que ya anda:** abrí el panel en el celular y mostrá la temperatura de ahora del equipo instalado — sigue reportando mientras la propuesta se evalúa. Si podés, sacá una sonda al aire un minuto y que vean subir la curva. Eso convence más que el PDF.
3. **Decilo en una frase:** "los cuatro de adentro llevan un equipo cada uno, y los dos de afuera comparten uno estanco porque están pegados. Tres sondas adentro de cada reefer, te avisa al celular si se sale de rango o si queda la puerta abierta, y arma el registro mensual solo."
4. **Si preguntan por el cable:** "adentro no hay que pasar cable de un contenedor a otro: cada reefer tiene su equipo al lado. Queda una sola tirada corta, la de los dos de afuera, y esa la resolvemos nosotros."
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

**Lo bueno de esta vuelta:** a Andrés le llega **exactamente el sistema que él describió**, armado sobre datos que dio él (los metros, el caño, la intemperie, que los de afuera están juntos, que adentro va uno por reefer y que el cable lo saca de ahí). **Lo incómodo:** el precio sube una hora después de haberle mandado un PDF. **Eso se compensa con velocidad y con el motivo dicho de frente** — y con lo que él gana adentro para defenderlo: un equipo por reefer, independientes entre sí, y sin obra de cableado entre contenedores.

---

## Anexo — Fuentes consultadas

- **Configuración definitiva: chat con Andrés, 4-sep 15:23** (*"¿los de afuera uno, y los otros uno cada uno sería?"* → **"Así sería"**; *"No es mucho lo de los cables. Los saco de acá."*).
- Alcance del bus, pull-ups, tierras entre contenedores, estrella no conmutada y límite prudente de 15 m: `C:\Proyectos\frioseguro\hardware\ALCANCE_1WIRE.md` (@muestreador), §2.6.
- **Costos reales, gabinetes, PCB, plazos y margen:** `C:\Proyectos\frioseguro\hardware\mini\BOM_CERRO_MORO.md` rev A (@hardware, 4-sep-2026) — §1 configuración de placas, §3 gabinetes (Roker PRG357 $ 44.419 / Genrod $ 21.203), §4 lista de compras, §4.5 la sirena a USD 40 no deja margen, §6 margen, §7 mediciones y plazos, §8 orden de pago.
- **BOM de la placa:** `C:\Proyectos\frioseguro\hardware\mini\BOM_MINI.md` rev A (@esquematico, 4-sep-2026).
- **Firmware de módulo doble — el que ahora hace falta sólo en el módulo de exterior y en el repuesto:** `C:\Proyectos\frioseguro-v31\firmware_modular\VERIFICACION_V3.1_2026-09-04.md`, veredicto **APTO CON CORRECCIONES**, correcciones en curso.
- Estado real y auditoría: `C:\Proyectos\frioseguro\entrega_scz\docs\ESTADO_HONESTO.md` · `AUDITORIA_HALLAZGOS.md`.
- **Qué hace hoy el firmware con sondas, puerta, relé y defrost (leído el 3-sep-2026):** `firmware_revival/sondas.h` (línea 31, `SONDAS_MAX`) · `config.h` 67-150 · `firmware_revival.ino` 369-375, 483-488, 804-944 · `comandos_nube.h` (**sin** comando de relé).
- Contrato base: `MATI-HQ\comercial\CONTRATO_TERMOVIGIA_v4.md`.
- Precios de canalización (§3.3, archivo), 1-Wire AN148, testo Saveris 2-T2, novillo INMAG, dólar BNA vendedor 1.535, Supabase Pro y Código de Conducta de Proveedores de PAAS: enlaces conservados en la v5.2 de este archivo (historial de git).

## Anexo — Lo que quedó abierto (para Matías, antes de mandar)

1. **Los números, con MARGEN PAREJO del ~32 % en los tres ítems** (liberaste el 850, así que lo recalculé desde el costo): **simple de interior 600 × 4 = 2.400** · **doble de exterior 700 × 1** · **repuesto 350** · puesta en marcha **1.550** (62 h) · **inicial USD 5.000** (era 4.600 en la v6.1, **+400, +8,7 %**) · abono **500/mes, sin tocar** · B = **10.400** · anticipo 50 % = **2.500**. **El total NO se movió respecto de la versión con el doble a 850: cambió el reparto, no la torta** — así que @diseno maqueta el mismo total y el WhatsApp no cambia de cifra. **¿Van?**
2. **⚠ EL PUNTO MÁS INCÓMODO Y HAY QUE MIRARLO: Andrés ya tiene el PDF de 4.600 desde las 14:01 de hoy.** El WhatsApp de §6.1 pone la suba en el primer párrafo con el motivo pegado y cierra con *"ignorá el anterior"*. **No mandes el mensaje sin el PDF corregido al lado**: un PDF viejo circulando adentro de la empresa es peor que llegar dos horas más tarde.
3. **Ya no hay un ítem con margen raro: 31,7 % el simple, 32,4 % el doble, 33,7 % el repuesto.** Eso significa que **ahora sí podés abrir el desglose de cualquiera de los tres** si te lo piden, cosa que con el 850 (44 % contra 25 %) no convenía. **El argumento del doble, si preguntan por qué 700 y no 1.200:** comparte el ESP32, la fuente, la placa, el gabinete, el alta remota y el punto de red — se duplica lo que va **adentro del reefer** (sondas y reed), no lo que va **adentro de la caja**. **El cliente se ahorra USD 500 por tener esos dos contenedores pegados** (tabla completa en §3.1).
4. **✅ Se desactivó el riesgo más grande de la v7.0:** los 4 simples corren el firmware que **ya anda hoy** (3 sondas ≤ `SONDAS_MAX` 4, 1 puerta, 1 defrost). **El firmware doble ahora bloquea sólo al módulo de afuera y al repuesto**: si se atrasa, arrancan igual **4 de los 6 reefers**. **Avisale al Director que el firmware doble salió del camino crítico de esta venta.** @firmware igual tiene que confirmar que las 10 h de §3.2 alcanzan; si son más, **salen del margen, no del precio**.
5. **⚠ El riesgo que SUBIÓ: 5 puntos de red** (eran 3). Es lo primero que hay que preguntarle a Andrés (§5.2 punto 1) y hay que saberlo **antes de despachar**. Repetidor si hace falta.
6. **⚠ El cuello ahora es la FABRICACIÓN, no el firmware ni la obra del cliente.** @hardware dice que con la PCB Mini el despacho es **semana 4-5, no 2**, y el hito 2 caería en la **7-8** (`BOM_CERRO_MORO.md` §7.2). **En el papel dejé los hitos como estaban. O se corren en el PDF, o se pide la PCB ya (USD 43, sirve igual para las demos de Bahía si Cerro Moro no compra). Decisión tuya, antes de firmar.**
7. **El cable: una sola tirada, la de afuera, y la resuelve Andrés** (*"no es mucho lo de los cables, los saco de acá"*). En el documento del cliente **no va nada más que la nota al pie** *"No incluye cable ni tendido entre reefers"*, tal cual (tu decisión). **Interno:** ese tramo tiene que ser par trenzado **apto exterior**, sin empalmes, canalizado. Si Andrés pregunta qué comprar, se le dice. **Confirmar con @esquematico que la posición alternativa del 1k queda en la placa.**
8. **El sexto reefer entra a USD 260 + USD 100/mes**, y ahora es más fuerte de vender: **su módulo ya está instalado y de alta**, no depende de un canal libre en la caja de un vecino. Está escrito en el documento del cliente. **¿Va así?**
9. **Compra de materiales: ≈ $ 821.000 ≈ USD 535** (§3.7), del BOM real de @hardware. **Es más que los $ 375.000 que decía la v7.0 — ese número era del perfboard, no de la Mini** (PCB fabricada + sondas moldeadas). **El margen igual cierra en 32 %.** Reservados 3 ESP32 para las galgas de Dreyfus (P0 de octubre).
10. **`M9` vale $ 63.609 y la etiqueta V/A de las fuentes $ 52.895:** 10 minutos con un calibre, antes del pedido. **Es la actividad de mayor rendimiento por minuto de todo el proyecto.** @hardware además tiene que contar stock y hacer `M1`-`M5` y `M7` antes de rutear.
11. **DECISIÓN DE PORTFOLIO, no comercial:** si Cerro Moro compra, Bahía se queda sin demos, y ahora son **6 módulos**. Recomendación: reposición en el mismo pedido que la OC. Las 10 placas de JLCPCB ya cubren las de sobra. **Decide el Director.**
12. **Preguntarle a Andrés:** los 5 puntos de red (§5.2.1), cuál de los 4 de adentro está fuera de servicio, cuántos metros hay entre los dos de afuera, y si el defrost es 12-24 V o contacto seco.
13. **Verificación cruzada entre sondas: hoy NO existe.** Vendida en el hito 2. Si no se puede cumplir, sacar el punto 3 del bloque "por qué 3 sondas".
14. **Accionamiento del relé desde el panel: tampoco existe.** Hito 5.
15. **El sensor de puerta viene deshabilitado por defecto** (`SENSOR_DOOR_ENABLED false`): que quede en la orden de armado habilitarlo y probar la puerta y el defrost de **cada canal de los 5 módulos**.
16. **La sirena a USD 40 no deja margen** (@hardware, `BOM_CERRO_MORO.md` §4.5): la BR300 sale USD 26 más su propia fuente de 12 V porque el relé es contacto seco. **Propongo USD 70 instalada, o baliza LED de 12 V. Decidís vos.**
17. **La caja de exterior que ya está en el sitio es la prueba de campo** (§2.5 punto 6) y de ella dependen **2 reefers**: pedirle a Andrés una foto después del primer temporal.
18. **Andrés:** opción 1, 2 o 3 de la Parte 7, y preguntarle para quién trabaja.
19. **PDF:** @diseno maqueta **un solo** documento de 2 páginas A4, marca Termovigía, sin logo ajeno, sin "Para:", sin validez. **Sin mencionar material de gabinete ni impresión 3D.** Archivo `PRESUPUESTO_CERRO_MORO.pdf` (+ `PRESUPUESTO_CERRO_MORO_INTERNO.pdf`). **Es lo que bloquea el WhatsApp de §6.1.**
20. Monotributo vs. RI: se pregunta cuando la empresa tenga nombre.
