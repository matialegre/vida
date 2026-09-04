# PROPUESTA — Monitoreo de temperatura de los reefers del campamento Cerro Moro (Santa Cruz)

> @comercial · **v6.1, 2026-09-04** · **UN SOLO presupuesto: 4 módulos — 2 simples a la intemperie + 2 dobles bajo techo**
> **La configuración la describió Andrés el 4-sep y es la que manda:**
> - **2 reefers están a la intemperie** → cada uno lleva **su propio módulo**, en **caja estanca IP65 apta para exterior** (Matías ya mandó una al sitio).
> - **4 reefers están adentro, bajo techo** → **2 módulos dobles**, uno por par, en gabinete común de interior.
> - **Total: 4 módulos.** De los 4 reefers de adentro, **uno está fuera de servicio**: hoy son **5 reefers activos** y **el segundo módulo doble atiende uno solo, con su canal libre esperando al sexto**. La línea del sexto reefer se resuelve sola: cuando vuelva, **no hay que comprar equipo**.
> - **Por reefer, siempre igual: 3 sondas + 1 sensor de puerta + 1 señal de defrost.** Módulo simple: 3 sondas, 1 puerta, 1 defrost. Módulo doble: 6, 2 y 2.
> **Otras decisiones de Matías del 4-sep:** el **tendido de cable entre reefers no se cotiza** — queda a cargo del cliente, y ahora **solo aplica a los dos pares de adentro, bajo techo** · **abono USD 100 por reefer por mes = 500/mes**, sin escalón, completo desde el primer mes · **en el documento del cliente no se dice el material del gabinete ni se menciona impresión 3D**.
> **Cambio del 4-sep (más urgente que todo lo anterior):** el cable **no** lo manda Matías desde acá; el documento del cliente ya no lleva spec de cable ni promesa de "cable incluido" — eso lo resuelven en el sitio. En su lugar hay una sola nota al pie de la tabla de precios: *"No incluye cable ni tendido entre reefers."*
> **Se mantiene de la v5.2:** sin destinatario, sin nombrar a Panamerican, hitos en semanas desde "aceptación + anticipo", 50/50, formas A y B, sin validez, USD con pago en pesos al BNA de la fecha de pago.
> **Matías decide el número final, siempre.** Todo monto de acá abajo es propuesta con la cuenta a la vista.
> Doctrina: `PLATA.md`. Base técnica: `ALCANCE_1WIRE.md` (@muestreador), `BOM_KIT_V1.md` rev B (@hardware, 2-sep), `ESTADO_HONESTO.md`, firmware `firmware_revival` leído el 3-sep.
> **El comprador NO es Pan American Silver:** es "una empresa" que Andrés todavía no identifica. El documento del cliente va **sin destinatario, sin logo ajeno y sin nombrar a Panamerican**. El archivo conserva el nombre por historial.

## Qué cambió en esta versión

**1. La configuración la fija el sitio, no la planilla.** Andrés informó que **2 reefers están afuera y 4 adentro**. Eso resuelve de una la discusión de las v4 y v5 sobre compartir o no compartir equipos: **se comparte donde se puede compartir bien** (los de adentro, bajo techo, con la tirada corta y protegida) y **no se comparte donde no conviene** (los de afuera, cada uno con su módulo estanco). No es una concesión ni un descarte: es la solución que cae sola cuando aparece el dato real.

**2. Cuatro módulos, dos precios.** **2 simples de exterior a USD 600** + **2 dobles de interior a USD 750** = **USD 2.700 en equipos**, más repuestos **400** y puesta en marcha **1.500** = **USD 4.600**. Era 4.540 en la v5.2: **+USD 60, un 1,3 %**, y el motivo es uno solo y se puede decir en voz alta — **la caja estanca de exterior cuesta casi tres veces la común**, y el kit de repuesto ahora es un módulo doble (que cubre cualquiera de los cuatro) en vez de uno simple.

**3. La obra de cable se achicó sola.** Solo hay **dos tiradas**, las de los pares de adentro, **bajo techo**. Los dos módulos de afuera no tienen ni un metro de cable entre contenedores. Sigue **a cargo del cliente**, y ahora es visiblemente menos trabajo del que Andrés tenía en la cabeza cuando habló del caño Daisa.

**4. Tres sondas por reefer, no cuatro** (decisión de Matías). 15 sondas en servicio. El argumento de por qué más de una **sigue valiendo entero con tres**: peor punto, redundancia ante falla y verificación cruzada (tres es el mínimo que permite saber **cuál** se desvió).

**5. El sexto reefer ya no es una promesa, es un canal libre.** Está adentro, está fuera de servicio, y su módulo doble **ya va instalado**. Cuando vuelva: **USD 260 de sondas, puerta y defrost, +USD 100/mes**. Sin equipo nuevo, sin renegociar nada.

**Sigue eliminada la opción C** de la v2 ("sin inversión inicial", comodato con permanencia 24 meses): *"el de la inversión inicial no lo ofrecería"* (Matías). Quedan **A** (equipos + servicio mensual) y **B** (anual adelantado).

---

## PARTE 1 — Documento del cliente (@diseno maqueta 2 páginas A4)

> Copiar de acá hasta la línea de corte. Nada más. Escrito para que **lo presente alguien que no es vendedor** y se lea en dos minutos.

**Termovigía — Monitoreo de temperatura de reefers**
**Campamento Cerro Moro (Santa Cruz) — 5 reefers en servicio**

**Qué es.** Un sistema que mide la temperatura de cada reefer las 24 horas y avisa al celular cuando algo se sale de rango. Hoy ya hay un equipo instalado y reportando desde el campamento: se puede ver en vivo en el celular antes de decidir nada. **Mientras se evalúa esta propuesta ese equipo sigue midiendo y reportando**, y el panel se puede abrir en cualquier momento: los resultados se muestran durante el proceso, no después.

**Armado según cómo está el sitio.**
- **Los 2 reefers que están a la intemperie llevan un módulo cada uno**, en **gabinete estanco IP65 apto para exterior**: frío, viento y lluvia son la condición normal de trabajo de ese equipo, no una excepción. Ahí no hay ni un metro de cable entre contenedores.
- **Los 4 reefers que están bajo techo se cubren con 2 módulos**, uno cada par, aprovechando que la tirada de cable entre ellos es corta y está protegida.
- Total: **4 módulos** para los 6 reefers, y **por cada reefer siempre lo mismo: 3 sondas, 1 sensor de puerta y 1 señal de defrost**.

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

**Qué se instala.** **Dos módulos de exterior** (gabinete estanco IP65, uno por cada reefer a la intemperie) y **dos módulos dobles de interior** (uno cada par de los que están bajo techo). Cada módulo trae su fuente y **2 salidas a relé**, y por cada reefer van **3 sondas, 1 sensor magnético de puerta y 1 entrada de señal de defrost**. Se suma un **kit de repuesto que queda en el campamento**. El montaje lo hace personal del campamento con los equipos preconfigurados desde Bahía Blanca y guía por videollamada: por eso esta propuesta no tiene línea de instalación ni viáticos.

**Cada módulo se prueba con el cable real antes de viajar.** Los equipos no salen de una línea de montaje: **se arman y se verifican uno por uno en banco de prueba** —todas las sondas leyendo, las puertas, las señales de defrost y las salidas de alarma— y **los módulos dobles se prueban con 25 metros de cable puestos**, la distancia real del sitio. Para un lote que va a quedar a 1.500 km del proveedor, esa verificación es la diferencia entre un equipo que llega andando y uno que hay que diagnosticar por teléfono.

**El sexto reefer.** De los 4 reefers de adentro, uno está hoy fuera de servicio, **y su módulo ya va instalado con el canal libre esperándolo**. Cuando vuelva a funcionar **no hay que comprar ningún equipo**: se le suman sus 3 sondas, su sensor de puerta y su entrada de defrost por **USD 260**, y el servicio mensual pasa de USD 500 a USD 600. Queda dicho acá para no tener que renegociar nada el día que pase.

**Puesta en marcha y ajuste en sitio (15 semanas, por hitos).** Los hitos son compromiso de entrega con plazo; no se facturan aparte, están incluidos en el precio. **Los plazos se cuentan desde el inicio, y el inicio es la aceptación de esta propuesta con su anticipo.**

| Hito | Qué queda funcionando | Plazo |
|---|---|---|
| 1 | El equipo que ya está instalado, con sus 3 sondas dentro del reefer, calibradas contra una misma referencia, rangos definidos y primera alerta real recibida en el celular | a las 2 semanas de iniciado |
| 2 | Los 4 módulos montados y los 5 reefers reportando; ningún dato ni aviso se pierde si se corta la red; aviso de módulo que deja de reportar; **aviso de sonda que se desvía de las otras del mismo reefer**; puertas y defrost validados en campo; una semana entera sin falsas alarmas | a las 5 semanas |
| 3 | Acceso seguro: cada módulo y cada usuario con su propia credencial | a las 10 semanas |
| 4 | Actualizaciones de los equipos a distancia, sin tocarlos | a las 12 semanas |
| 5 | Panel para la empresa (usuarios de solo lectura), accionamiento de las salidas de alarma desde el panel e informe mensual descargable | a las 15 semanas |

**Qué cuesta.**

| Concepto | USD |
|---|---|
| Módulo de exterior para un reefer a la intemperie (gabinete estanco IP65 apto para exterior, fuente, 2 salidas a relé, 3 sondas, sensor de puerta, entrada de defrost; probado en banco) — 2 × 600 | 1.200 |
| Módulo doble para dos reefers bajo techo (gabinete, fuente, 2 salidas a relé, y por cada reefer 3 sondas + sensor de puerta + entrada de defrost; probado en banco con 25 m de cable) — 2 × 750 | 1.500 |
| Kit de repuestos en sitio (1 módulo doble completo armado y probado, que puede reemplazar a cualquiera de los cuatro, + 3 sondas + 1 sensor de puerta) | 400 |
| Puesta en marcha y ajuste en sitio, 5 hitos | 1.500 |
| **Total equipos y puesta en marcha** | **4.600** |
| **Servicio mensual** — **USD 100 por reefer por mes**, 5 reefers en servicio (nube, alertas, soporte, reposición sin cargo, informe mensual) | **500 / mes** |

*No incluye cable ni tendido entre reefers.*

**Cómo se paga.** **50 % con la orden de compra** (anticipo de materiales) y **50 % contra los equipos instalados y reportando**. El servicio mensual arranca con el primer equipo andando.

| | **A. Equipos + servicio mensual** | **B. Anual adelantado** |
|---|---|---|
| Para quién | Compra activos y paga el servicio mes a mes | Tiene presupuesto de inversión y no quiere 12 facturas |
| Equipos y puesta en marcha | USD 4.600 (50 % con la OC, 50 % contra instalación) | Incluidos |
| Pago inicial total | USD 4.600 | USD 10.000 (equipos + 12 meses de servicio, con 10 % de descuento sobre el servicio) |
| Mensual | USD 500 — USD 100 por reefer, completo desde el primer mes | — el primer año; renovación anual USD 5.400 |
| Los equipos | Son del cliente | Son del cliente |
| **Total a 12 meses** | **10.600** | **10.000** |
| **Total a 24 meses** | **16.600** | **15.400** |

Facturación en dólares estadounidenses. De abonarse en pesos, se toma el tipo de cambio vendedor del Banco de la Nación Argentina de la fecha de pago. *Referencia al 4-sep-2026 (BNA vendedor $ 1.535): USD 4.600 ≈ $ 7.061.000 · USD 500 ≈ $ 767.500 · USD 10.000 ≈ $ 15.350.000.*

**Incluido en el servicio mensual:** nube con 12 meses de historial · alertas por temperatura, puerta abierta, sonda caída y equipo mudo · reposición sin cargo de cualquier módulo o sonda fallada, envío incluido · actualizaciones · soporte por WhatsApp y teléfono el mismo día hábil · informe mensual por reefer.

**Lo que hay que saber.** El sistema avisa; no garantiza la mercadería ni reemplaza la revisión del reefer. Sin energía en el módulo no mide: lo que avisa en ese caso es la nube, diciendo que dejó de reportar. La entrada de defrost necesita que el reefer tenga una señal o un contacto accesible; si alguno no lo tiene, esa entrada queda libre y el resto funciona igual. Las 2 salidas a relé vienen en el módulo; la sirena o baliza que se conecte no está incluida. Cada módulo necesita llegar a la red del campamento. El tendido del cable entre los reefers de cada par de adentro lo hace el cliente. En los pares de adentro, si un módulo se queda sin energía quedan **dos** reefers sin vigilancia hasta que vuelva; en los de la intemperie, uno. Los plazos de los hitos 1 y 2 suponen que el montaje en sitio se hace dentro de la ventana prevista, que depende de personal del campamento.

*Contacto en sitio: Andrés Leiva Chavez · Contacto comercial: Matías Alegre — Ingeniería Electrónica, UTN Facultad Regional Bahía Blanca · Grupo de investigación GIMAP · Termovigía, Bahía Blanca · 2920 59-1019 · alegrematias08@gmail.com · termovigia.vercel.app*

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

### 2.2 Registro: cómo quedó resuelta la discusión de compartir o no compartir

> Las v4 y v5 discutieron durante dos versiones si convenía un equipo por reefer o uno cada dos. **El dato de Andrés del 4-sep —2 afuera, 4 adentro— cerró la discusión sin que hubiera que elegir bando.** Esta sección deja escrito por qué, para poder defenderlo si alguien pregunta.

**La regla que quedó, y es defendible con una frase:** *se comparte módulo donde compartir es barato y seguro (adentro, bajo techo, tirada corta y protegida), y no se comparte donde no lo es (a la intemperie, donde el cable tendría que salir a cielo abierto entre dos contenedores)*.

**Qué se gana con cada mitad:**
- **Los 2 de afuera, con módulo propio:** cero cable entre contenedores en la zona más hostil, **cero obra**, y si un módulo cae queda **un** reefer ciego, no dos. Se paga con una caja más cara, y vale la pena.
- **Los 4 de adentro, de a pares:** dos módulos en vez de cuatro, la tirada es corta y bajo techo, y **el módulo del par donde está el reefer fuera de servicio ya queda comprado con el canal libre** — el sexto reefer entra después por USD 260 en vez de por un equipo entero.

**El riesgo del bus, asumido con conocimiento — que quede escrito.** Andrés dijo *"son aprox 20/25 metros"* (3-sep 23:33) y el límite prudente que fijó @muestreador para este bus es **15 m**. Además, el cable ata las masas de **dos contenedores metálicos con puesta a tierra separada** por el hilo de datos (`ALCANCE_1WIRE.md` §2.6: *"el riesgo dominante de esta instalación"*). **Matías conoce el dato y acepta el riesgo.** Lo que se hace para acotarlo:

- **Pull-up de 2k2 con posición alternativa de 1k** en la placa (@esquematico lo está poniendo). El 1k es la carta que se juega si el bus no cierra a 25 m.
- **Los dos módulos dobles se prueban en banco con 25 m de cable real antes de despachar**, con las 6 sondas colgadas. No sale nada que no haya cerrado a la distancia real.
- **Especificación de cable** (par trenzado exterior, el par DQ/GND junto en todo el recorrido, sin empalmes, canalizado): **queda interna**, no se manda al cliente — desde el 4-sep el cable no lo provee Matías, así que no corresponde especificarle un tipo que no le vamos a mandar.
- **El riesgo se redujo a la mitad respecto de la v6.0:** ahora son **2 tiradas y las dos bajo techo**, no tres a la intemperie. Menos metros expuestos, menos humedad en las uniones, menos diferencia de potencial entre masas.
- Si aun así un bus no cierra en sitio, la salida técnica existe y es barata: pasar ese par a un segundo bus con su propio pin, o un repetidor 1-Wire. **No hay escenario en el que haya que devolver plata.**

**Lo que NO se le dice al cliente:** que esto es un riesgo. En el documento va la nota de que el cable y el tendido no están incluidos, y nada más sobre el cable — la spec queda interna. La mitigación real (prueba de banco con 25 m) tampoco se explica al cliente: se hace y punto.

**Y el tendido no se cotiza** (decisión de Matías, textual: *"no contemples el tema de las tiradas"*). La cuenta del caño de la v5 queda archivada en §3.3 **como historia y como argumento**, no como renglón: el precio que mandamos es firme y no depende de nada que pase en una zanja.

### 2.3 Qué lleva cada módulo, y qué de eso anda HOY (verificado en el código el 3-sep)

| Función | Simple (exterior) | Doble (interior) | Qué hace el firmware hoy | Evidencia |
|---|---|---|---|---|
| Sondas DS18B20 | 3 | 6 | Cada una identificada por ROM de 64 bits y reportada por separado; enganche en caliente; aviso si se desconecta; **offset de calibración por sonda en NVS**. **`SONDAS_MAX` está en 4: para el doble hay que subirlo a 8** — es el tamaño de un arreglo, una línea | `sondas.h`: `sondasEscanear`, `sondasLeer`, `sondasCalibrar`; línea 31 |
| **Verificación cruzada entre sondas** | — | — | **NO existe.** `sondasCalibrar()` iguala las sondas en un momento dado; el lazo de lectura **no compara sondas entre sí** ni alerta por deriva | ídem. Vendida en el **hito 2**, con la aclaración escrita en la página del cliente |
| Sensor de puerta | 1 | **2** | Implementado **para una sola puerta**: GPIO5, alerta por puerta abierta > 180 s, suprime la alerta de temperatura mientras está abierta. Viene deshabilitado por defecto (`SENSOR_DOOR_ENABLED false`). **La segunda puerta hay que agregarla, solo en el doble** | `config.h` 72-74, 105, 119 · `.ino` 804-890 |
| Entrada de defrost | 1 | **2** | Implementada **para una sola entrada**: GPIO33, NA/NC configurable, deshabilita alertas durante el ciclo con 30 min de enfriamiento. **La segunda hay que agregarla, y tiene que silenciar solo el reefer que descongela** | `config.h` 91-96, 122 · `.ino` 54-55, 100-101, 872-878 |
| Salidas a relé | 2 | 2 | **1 gobernada**: GPIO26, se activa sola con la alerta si `relayEnabled`. La segunda queda cableada y disponible. **El accionamiento manual desde el panel NO existe** | `config.h` 76-77, 140-150 · `.ino` 369-375, 483-488, 915-944 · `comandos_nube.h` sin comando de relé → **hito 5** |
| Gabinete | **IP65 estanco de exterior** | Gabinete común de interior | — | Caja de exterior ya enviada al sitio (4-sep) |

**Regla de venta.** Lo que **no** está andando hoy y va vendido con hito, nunca como característica de hoy:
- **Segunda puerta, segundo defrost y `SONDAS_MAX` a 8** — el software del módulo doble. Costeado en §3.2, hito 2.
- **Verificación cruzada entre sondas** — hito 2.
- **Accionamiento manual del relé desde el panel** — hito 5.

**Ventaja no obvia de esta configuración para el firmware:** **los 2 módulos de exterior corren el firmware que ya anda hoy, sin una línea nueva.** Solo los dos dobles necesitan el software de doble reefer. Eso baja el riesgo de entrega: **si el software del doble se atrasa, la mitad del sistema igual arranca**.

**Detalle que no se puede pasar por alto en el diseño del doble:** **el defrost de un reefer no puede silenciar las alarmas del otro.** Hoy el defrost deshabilita *todas* las alertas del equipo. En el módulo doble tiene que silenciar **solo las sondas del reefer que está descongelando**. Está dentro de las horas de §3.2 y es lo que hay que probar sí o sí antes del hito 2.

**Orden de armado:** línea `entrega_scz`/`firmware_revival` (identificación por ROM), **no** `firmware_modular` (lee por índice: si cae una sonda, la otra se reporta con el nombre equivocado). **Pull-up 2k2 con posición alternativa de 1k** (@esquematico), 3 hilos (nada de parasite power), 100 nF + 10 µF al pie de la sonda más lejana de cada rama. **Habilitar `SENSOR_DOOR_ENABLED`, probar puertas y defrost, y correr la prueba de banco con 25 m de cable en los dos dobles antes de despachar.**

### 2.4 Lo que se instala, y quién

**Módulo simple de exterior (×2):** **gabinete estanco IP65 apto para exterior** 200×200×80, fuente de 5 V 2 A, plaqueta con borneras a tornillo, ESP32 en zócalo, módulo de 2 relés, **prensacables en todas las entradas**, 3 sondas DS18B20 estancas, 1 reed de puerta.
**Módulo doble de interior (×2):** gabinete común 200×200×80, misma electrónica, 6 sondas, 2 reed, y **25 m de par trenzado exterior** para llegar al reefer vecino.
**Kit de repuesto (×1):** un **módulo doble** completo —cubre a cualquiera de los cuatro— + 3 sondas + 1 reed.

**Montaje: Andrés (o quien la empresa designe), con kit preconfigurado y probado en banco + videollamada.** Dos pasajes a Santa Cruz, alojamiento, inducción y 5 días de ingeniero rondan los $ 2.500.000, y Matías no puede viajar en octubre (parada de Dreyfus). Eso es lo que esta propuesta no cobra.

**Intemperie: en el documento del cliente se dice "gabinete estanco IP65 apto para exterior" y nada más.** Ni material, ni proceso de fabricación, ni impresión 3D. Ni en el PDF ni en el WhatsApp.

### 2.5 Los riesgos técnicos abiertos

1. **Los dos buses de 20-25 m de los pares de adentro** — riesgo asumido, mitigaciones en §2.2. **Bajó respecto de la v6.0**: dos tiradas en vez de tres, y las dos bajo techo.
2. **Cobertura de red en 4 puntos** — mejor que los 5 de la v5.2, peor que los 3 de la v6.0. Si alguno queda corto se resuelve con un repetidor barato, pero hay que saberlo **antes de despachar**. Pregunta 1 de §5.2, no frena el envío.
3. **El defrost cruzado en los módulos dobles** (§2.3): que el descongelamiento de un reefer no ciegue al otro. Trabajo de software, costeado, y es lo que hay que probar antes del hito 2.
4. **La caja de exterior a la intemperie de Santa Cruz** es la única parte del equipo que no tiene antecedente de campo largo. La que se mandó al sitio el 4-sep es, de hecho, **la prueba de campo**: conviene pedirle a Andrés una foto después del primer temporal.

### 2.6 Opcionales, después de la primera orden

**El sexto reefer cuando vuelva a servicio: USD 260 + USD 100/mes** — entra en el canal libre de su módulo doble, **sin equipo nuevo**. Ya está escrito con precio en el documento del cliente: no hay que venderlo de nuevo, solo ejecutarlo. **Es el upsell más probable y el de mejor margen de esta cuenta.** · Sirena o baliza física para la salida de relé (USD 40; el relé ya está incluido) · **cuarta sonda** en un reefer (USD 40 + USD 5/mes) · base con batería y 4G, la única que avisa el corte de energía por sí misma (a cotizar) — **especialmente vendible para los dos de la intemperie**. Se ofrecen cuando las sondas estén andando, no antes.

---

## PARTE 3 — Números de respaldo

Base: BOM real (`BOM_KIT_V1.md` rev B de @hardware, precios de MercadoLibre AR verificados el 2-sep-2026, a precio de reposición). Cambio $ → USD al BNA vendedor 1.535 del 3-sep.

### 3.1 Los dos módulos: USD 600 el simple de exterior, USD 750 el doble de interior

| | Simple exterior (ARS) | USD | Doble interior (ARS) | USD |
|---|---:|---:|---:|---:|
| Electrónica y gabinete: ESP32 13.990 + módulo de 2 relés 5.028 + fuente 5 V 2 A 7.980 + consumibles de placa §3.1 del BOM + prensacables. **Caja: IP65 de exterior ~22.000 en el simple, gabinete común ~8.500 en el doble** | ~59.000 | **38** | ~47.500 | **31** |
| Sondas DS18B20 estancas rearmadas con 3 m de cable y prensacable (3 y 6) | ~27.600 | **18** | ~55.200 | **36** |
| Sensores magnéticos de puerta cableados (1 y 2) | 4.746 | **3** | 9.492 | **6** |
| Cable de interconexión al reefer vecino (25 m de par trenzado exterior) — **solo el doble** | — | **0** | ~15.000 | **10** |
| Envío a Santa Cruz, prorrateado | ~12.300 | **8** | ~18.400 | **12** |
| Armado + **prueba de banco documentada** (el doble, con 25 m de cable) + garantía de reposición amortizada | | **100** | | **150** |
| Parte de plataforma del desarrollo: USD 1.000 repartidos en **4** módulos | | **250** | | **250** |
| Margen | | **183** | | **255** |
| **Precio** | | **600** | | **750** |

**Márgenes: 30,5 % el simple, 34 % el doble.** El doble gana más porque **carga el riesgo del bus de 25 m** (si no cierra hay que resolverlo remoto o mandar material) y porque su garantía pesa el doble: un doble caído deja dos reefers ciegos.

**Por qué 600 y 750, y no otros números.** Los dos son redondos, se dicen en una frase, y la cuenta cierra sin forzar nada: **2 × 600 + 2 × 750 = 2.700 en equipos**, exactamente el mismo renglón de equipos que la v5.2 y la v6.0. **La configuración cambió tres veces y el cliente vería siempre el mismo número de equipos: eso es señal de que el precio está bien puesto, no de que se acomodó.**

**De dónde salen los USD 60 de diferencia con la v5.2 (4.540 → 4.600), y es un solo renglón y medio.** El **kit de repuestos pasa de 340 a 400** porque ahora el repuesto es un **módulo doble** (que puede reemplazar a cualquiera de los cuatro, incluido un simple) y no un simple. Los equipos y la puesta en marcha no se movieron. **Es un 1,3 % de diferencia y compra una garantía que cubre el sistema entero con una sola caja de repuesto.** Si Matías prefiere el número redondo de 4.540, se llega bajando el repuesto a 340 y aceptando que el repuesto sea un simple: **no lo recomiendo** — el día que falle un doble, un repuesto simple deja un reefer sin vigilancia y obliga a un envío urgente a 1.500 km.

### 3.2 Puesta en marcha, USD 1.500

| Trabajo | h |
|---|---:|
| Sondas, rangos y umbrales por reefer + **calibración de las 15 sondas** contra referencia y registro de offsets | 10 |
| **Software del módulo doble: segunda puerta, segundo defrost con silenciado por reefer, `SONDAS_MAX` a 8, validación del bus a 25 m** | 10 |
| Registro exportable con código de verificación | 14 |
| Panel multi-equipo y usuarios de lectura | 10 |
| Puesta en marcha remota (alta, credencial, OTA verificada, prueba de puertas y defrost), pruebas de campo con Andrés, runbook y capacitación — 4 módulos | 12 |
| Salud de bus, histéresis de 3 barridos y **verificación cruzada entre sondas** | 4 |
| **Total a USD 25/h** | **60 = USD 1.500** |

*Bajó de 1.600 (v5.2) a 1.500: se ahorran horas en calibración (15 sondas en vez de 20) y en alta remota (4 módulos en vez de 5), y se gastan 10 h nuevas en el software del doble. **Las 10 h del software del doble son la línea a vigilar**: si @firmware dice que son más, salen del margen, no del precio.*

### 3.3 **LA CUENTA DEL CAÑO** — archivo, y por qué ya no entra en el precio

> Se conserva de la v5 **como historia y como argumento**, no como parte del presupuesto. **El tendido lo hace y lo paga el cliente, y no aparece en el documento que se manda.** Y ahora son **2 tiradas bajo techo**, no 2 a la intemperie: el número real que van a gastar es **más bajo que esta cuenta**, que se hizo para caño rígido exterior.

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
1. **Saber el tamaño de lo que el cliente gasta por su lado** (≈ USD 572 por las 2 tiradas en el peor caso, bastante menos bajo techo). Si dicen "esto de la obra no lo teníamos previsto", la respuesta ya está: **la configuración la describieron ellos**, y las tiradas bajaron de 3 a 2 y de la intemperie al interior.
2. **Tener lista la variante de rescate.** Si la obra los frena, **no se pierde la venta**: se ofrece un módulo por reefer, sin ninguna obra, con el mismo total. Está calculado en la v5.2 de este archivo (historial de git).
3. **Que nadie regale la instalación.** Si aparece la tentación de "se lo hacemos nosotros para cerrar", el número a tener en la cabeza es **USD 286 por tirada**, más pasajes y estadía.

### 3.4 Servicio mensual: qué cuesta servir y qué se cobra

| Costo directo mensual | v2 (12 sondas) | **v6.1 (15 sondas, 5 reed, 4 módulos)** |
|---|---:|---:|
| Supabase Pro | 25 | 25 |
| Reposición amortizada (módulos y sondas en garantía) | 10 | **17** |
| Soporte (2 h → 2,3 h a USD 25) | 50 | **57** |
| Informe mensual | 25 | 25 |
| **Total** | **110** | **124** |

**Tarifa: USD 100 por reefer por mes × 5 = USD 500/mes** (decisión de Matías, 4-sep). Costo directo 124 → **margen bruto USD 376 (76 %)**. La justificación, y es la que hay que decir si preguntan: **mantenimiento del servidor, custodia de los datos y seriedad del servicio** — el registro que se entrega tiene que estar disponible y ser defendible dentro de un año, y eso se paga todos los meses aunque no pase nada.

**El abono es estrictamente proporcional a los reefers, no a los equipos**: 5 reefers = 500, 6 = 600. Eso importa con módulos mezclados: **el precio del servicio no depende de cuántas cajas haya**, porque lo que se vigila y se registra son reefers. **Cuando entre el sexto, los USD 100 adicionales son casi margen puro** y el equipo ya está puesto.

**El escalón de los primeros 3 meses al 50 % sigue eliminado** (decisión de Matías, 4-sep): abono completo desde el primer mes en las dos formas. Lo justifica que el servicio ya está corriendo —servidor, custodia y guardia de alertas— desde el primer equipo que reporta.

### 3.5 Condiciones de pago — 50 / 50, y por qué no 25

**50 % con la orden de compra (anticipo de materiales) y 50 % contra los equipos instalados y reportando.** El abono arranca con el primer equipo andando.

El fundamento es de caja: hay que comprar y armar **5 módulos** (4 + el repuesto) antes de ver un peso del segundo tramo, y cobrar ese tramo a un contratista que todavía no tiene nombre. Con el 50 % (**USD 2.300 ≈ $ 3.530.500**) la compra completa de materiales —**≈ $ 430.000 con flete, §3.7**— queda cubierta **más de ocho veces** antes de tocar un componente. Con el 25 % también alcanzaría para los materiales; lo que no cubriría es el **riesgo de cobranza del segundo tramo**, que es lo que en realidad se está financiando.

Los hitos siguen existiendo **como compromiso de entrega con plazo**, y así está escrito en el documento del cliente: *"no se facturan aparte, están incluidos en el precio"*. **Punto para que Matías confirme:** cobrar antes de entregar los hitos es más cómodo para la caja y más exigente con la palabra.

### 3.6 Las dos formas de pagar, y por qué se cayó la tercera

**A. Equipos + servicio mensual.** 4.600 + 12 × 500 = **10.600** el primer año; 6.000/año después; **24 meses 16.600**.

**B. Anual adelantado, 10 % de descuento sobre el año de servicio.** 4.600 + (12 × 500) × 0,9 = 4.600 + 5.400 = **USD 10.000 redondos**; renovación 5.400/año; **24 meses 15.400**. El descuento le ahorra **USD 600 el primer año** y lo que compra es concreto: **cero riesgo de cobranza durante 12 meses con un contratista que probablemente pague a 60-90 días, una factura en lugar de doce, y caja para armar los equipos.** *Que la B dé USD 10.000 exactos es una casualidad útil: es el número más fácil de aprobar de toda la propuesta.*

**C, eliminada.** Matías: *"el de la inversión inicial no lo ofrecería"*. Era la única que ponía USD ~4.600 nuestros en manos de un contratista a 1.500 km, sin poder retirar los equipos y sin contrato con permanencia. **No se vuelve a ofrecer sin contrato validado por contador y un cliente con historial de pago.** Con dos opciones el comprador elige; con tres se paraliza.

**Sin cláusulas condicionales.** La propuesta no tiene condición de metros, ni de canalización, ni corrección de precio por par: **el tendido es del cliente y el precio es firme.**

### 3.7 **Los 5 módulos: qué falta comprar y cuánto sale**

**Qué hace falta.** 5 módulos: **2 simples de exterior + 2 dobles de interior + 1 doble de repuesto**. Sondas: 15 instaladas + 3 de repuesto = **18**. Reed: 5 instalados + 1 de repuesto = **6**. Defrost: 5 entradas (cable y bornera, sin componente caro).

**Cruce contra el stock declarado** (`BOM_KIT_V1.md` §1, tomando el número más bajo de cada rango, y reservando **3 ESP32 para las galgas de Dreyfus**, que es P0 de octubre):

| Ítem | Hacen falta | Stock declarado | Faltan | Precio | **A comprar** |
|---|---:|---:|---:|---:|---:|
| ESP32 DevKit | 5 + 3 (galgas) = **8** | 4 | **4** | $ 13.990 c/u | **$ 55.960** |
| Sondas DS18B20 | **18** | 15 | **3** | $ 4.388 c/u | **$ 13.164** |
| **Cajas IP65 de exterior** (los 2 módulos de la intemperie) | 2 | 0 de esa medida | **2** | ~$ 22.000 c/u | **$ 44.000** |
| Gabinetes para los 3 dobles (2 + repuesto) | 3 | 3 de 165×165 — **chicas para 6 sondas + 2 puertas + 2 defrost** | **3** | ~$ 14.000 c/u | **$ 42.000** |
| Fuentes 5 V **2 A** | 5 | 5, **amperaje sin verificar** | **5** (peor caso) | $ 7.980 c/u | **$ 39.900** |
| Módulos de relé 2 canales | 5 | 10 | 0 | — | **$ 0** |
| Reed / sensor de puerta | 6 | 10 | 0 | — | **$ 0** |
| Consumibles del §3.1 del BOM reescalados a 5 módulos (plaquetas PE04 ×5, borneras, tiras hembra, **R 2k2 y 1k**, 10 k, 100 nF, electrolíticos, separadores, **prensacables 6 packs** por las entradas extra de los estancos) | — | — | — | — | **$ 150.000** |
| Cable de 3 hilos para rearmar 18 sondas a 3 m + termocontraíble | — | — | — | — | **$ 40.000** |
| **Cable par trenzado exterior para las 2 tiradas (60 m con sobrante)** | — | — | — | — | **$ 24.000** |
| **TOTAL** | | | | | **≈ $ 409.000** |

Con flete y diferencias de vendedor: **≈ $ 430.000 ≈ USD 280**. Si las fuentes de stock resultan ser de 2 A, baja a ≈ $ 390.000 (USD 254).

**Contra el anticipo del 50 % (USD 2.300 ≈ $ 3.530.500), la compra completa es el 12 %.** No hay problema de plata ni de cantidades. **Las 2 cajas IP65 de exterior son el renglón de mayor plazo de entrega: hay que pedirlas primero.** Las 3 cajas de 165×165 que hay en stock **no sirven para los dobles** (6 sondas + 2 puertas + 2 defrost + fuente no entran cómodos): quedan para las demos de Bahía.

**Por qué el hito 1 SÍ es alcanzable.** El hito 1 es *"el equipo que ya está instalado, con sus 3 sondas dentro del reefer, calibradas, rangos definidos y primera alerta real"*. **No depende de que lleguen los módulos nuevos: depende de que lleguen 2 sondas** (el equipo instalado ya tiene 1, y ahora son 3 por reefer, no 4). `REEFER_01_SCZ` está montado y reportando desde el 21-ago con **1 sola sonda, y está fuera del reefer**.

**El plan arranca cuando aceptan, no antes.** Semana 0 = aceptación + anticipo del 50 %. Hasta que eso pase **no se compra, no se arma y no se despacha nada**, y a Andrés no se le pide que reserve ninguna ventana: trabaja por turnos de 15 días y no es él quien aprueba.

| Paso | Plazo desde la aceptación | Quién |
|---|---|---|
| Conteo del stock real + las 2 mediciones del §8.1 del BOM (amperaje de las fuentes, relé con IN al aire) | semana 0 | Gonza |
| Compra del faltante — **las 2 cajas de exterior primero** — y rearmado de sondas a 3 m | semana 0-1 | Gonza / Matías |
| Despacho de 2 sondas para el equipo ya instalado (encomienda, 5-8 días hábiles) | semana 1 | — |
| Software del módulo doble (2ª puerta, 2º defrost por reefer, `SONDAS_MAX` a 8) | semana 1-2 | Matías / @firmware |
| Alta, calibración remota, rangos y primera alerta real | semana 2 | Andrés + Matías |
| **HITO 1** | **semana 2** | — |
| Armado de los 5 módulos + **prueba de banco, los dobles con 25 m de cable** (~20 h) | semana 1-2 | Gonza / Sergio |
| Despacho de los 5 bultos (4 módulos + repuesto) a Cerro Moro | semana 2 | — |
| **Tendido del cable en los 2 pares de adentro** | semana 2-3 | **cliente** |
| Montaje de los módulos por personal del campamento | semana 3-4 | campamento |
| Alta y calibración de las 13 sondas nuevas | semana 4 | Matías |
| **HITO 2** (los 5 reefers reportando + una semana sin falsas alarmas) | **semana 5** | — |

**El riesgo que hay que decir en voz alta: el hito 2 está apretado y depende de una obra ajena.** La semana sin falsas alarmas arranca cuando los 4 módulos reportan —alrededor de la semana 4— y el hito vence en la 5: **una semana, sin colchón**. Está cubierto en el documento del cliente por la línea de que los plazos de los hitos 1 y 2 dependen de la ventana de montaje del campamento; **Matías no debería prometer el hito 2 por teléfono con más firmeza que la que dice el papel.** **Lo que sí mejoró:** los 2 módulos de exterior **no dependen de ningún tendido** y pueden estar reportando apenas se montan.

**Por qué se puede empezar a armar antes de la orden de compra, sin exponer un peso nuevo.** Los kits **ya estaban planificados como las unidades de demostración del plan comercial de Bahía**. Si Cerro Moro no compra, **no quedan colgados: van a su destino original**. **La contracara para el Director: si Cerro Moro compra, Bahía se queda sin demos.** Recomendación: **la reposición de los kits de Bahía se dispara en el mismo pedido que la orden de compra**, no después.

### 3.8 Moneda, validez, facturación

**Facturación en USD, pago en pesos al BNA vendedor de la fecha de pago, sin validez en el PDF.** Nota interna: revisar precios si pasan más de 6 meses desde el 4-sep. Antes de la cotización firme hay que saber: monotributo vs. RI, plazo de pago, si acepta la cláusula de moneda, quién firma. Se pregunta cuando la empresa tenga nombre.

### 3.9 Contra una pérdida y contra la competencia

Una pérdida de 3 t valuada al precio de novillo en pie ($ 4.181/kg, INMAG jul-2026) son $ 12,5 M: **16 meses de servicio** al abono de USD 500 (≈ $ 767.500 por mes). testo Saveris 2-T2: USD 318 por unidad y mide **un** punto; para cubrir los 15 puntos de esta propuesta harían falta 15 unidades = **USD 4.770** antes de importación, sin nube, sin puerta, sin relé, sin defrost, sin repuesto en sitio — y se configura con una red WiFi y una clave, que es exactamente lo que este sitio no tiene. **Y ninguna de esas unidades es apta para la intemperie sin gabinete adicional.**

---

## PARTE 4 — Puesta en marcha: qué es cada hito por dentro

Las duraciones se cuentan **en semanas desde la aceptación**, no contra el calendario. Los hitos pesados caen después de la semana 5 para no chocar con la parada de Dreyfus.

| Hito (cliente) | Etapa interna | Desde | Hasta | Cómo se acepta |
|---|---|---|---|---|
| 1 — El equipo ya instalado con sus 3 sondas adentro y calibradas, rangos, primera alerta real | E0 | semana 0 | **semana 2** | Captura de la alerta en el celular + registro en nube + **planilla de calibración con el offset de las 3 sondas de `REEFER_01_SCZ`** |
| 2 — Los 4 módulos y los 5 reefers reportando; nada se pierde, nada sobra | E1: buffer offline, alertas encoladas, alerta de sonda caída, vigía de equipo mudo, discriminador de bus + histéresis, **detección de sonda que se desvía de las otras del mismo reefer**, **segunda puerta y segundo defrost con silenciado por reefer en los dobles** | semana 2 | **semana 5** | Los 4 módulos montados con sus 15 sondas calibradas; desenchufar una sonda y que llegue la alarma; cortar la red 20 min sin perder lecturas; abrir una puerta 4 min y que avise; **forzar el defrost de un reefer de un par y verificar que el otro del mismo módulo sigue alarmando**; **una semana sin falsas alarmas** |
| 3 — Acceso seguro | E2: RLS cerrada, credencial por módulo, secretos fuera del binario, revocar claves quemadas | semana 5 | **semana 10** | Con la clave vieja no se escribe; todos los módulos siguen reportando |
| 4 — Actualización a distancia | E3: OTA con manifiesto inmutable | semana 10 | **semana 12** | Tres actualizaciones seguidas por aire al primer intento, en todos los módulos |
| 5 — Panel e informe | E4: usuarios de lectura, vista de los reefers, exportación con código, informe mensual automático, **comando de relé desde el panel** | semana 12 | **semana 15** | Un usuario de la empresa entra solo, baja el informe y acciona una salida desde el panel |

**El hito 2 es el apretado** (§3.7): la semana sin falsas alarmas arranca cuando los 4 módulos reportan, alrededor de la semana 4, y vence en la 5. **Sin colchón, y con el tendido del cliente en el camino crítico de los dos pares de adentro.**

Lo que hoy está roto y cada hito arregla (llave maestra en el binario, datos perdidos sin red, umbral en 50 °C, equipo muerto que no avisa, OTA que entra 1 de 4) está en `AUDITORIA_HALLAZGOS.md`; no cambió.

---

## PARTE 5 — Qué necesitamos para cerrar

### 5.1 De la empresa, cuando tenga nombre

Quién firma, cómo factura (monotributo/RI, plazo), si acepta la cláusula de moneda, **cuál de las dos formas de pago elige (A o B)**, y confirmación de que el montaje **y el tendido del cable en los dos pares de adentro** los hace personal del campamento (sin personal nuestro en sitio no corresponde ART ni legajo de contratista).

### 5.2 De Andrés: lo que sigue abierto

**Ninguna de estas frena el envío.**

1. **¿La red del campamento llega bien a los 4 puntos donde van los módulos?** Si alguno queda corto se resuelve con un repetidor barato, pero hay que saberlo **antes de despachar**.
2. **¿Los reefers tienen una señal o contacto de defrost accesible?** Si alguno no lo tiene, esa entrada queda libre y el resto funciona igual — ya está dicho así en el documento del cliente, sin letra chica.
3. **¿Cuál de los 4 de adentro es el que está fuera de servicio?** Define cómo se arman los pares: **el que está fuera va emparejado con un activo**, para que el canal libre quede en un módulo ya instalado y andando.
4. **¿Para quién trabaja Andrés?** (empleado de PAAS o de una contratista). No es técnica: decide la Parte 7.

---

## PARTE 6 — Para Andrés (aparte del PDF)

### 6.1 WhatsApp — lo manda Matías

```
Andrés, quedó armado tal cual me lo describiste: los 2 reefers que están
a la intemperie llevan un módulo cada uno, en caja estanca IP65 para
exterior, y los 4 de adentro van con 2 módulos, uno cada par. Cuatro
módulos en total.

Por cada reefer: 3 sondas adentro, sensor de puerta y la señal de
defrost, así no suena la alarma cada vez que descongela.

El cable entre los dos reefers de cada par de adentro y su tendido
corren por cuenta de ustedes, eso lo ven ahí. Los de afuera no llevan ni
un metro de cable entre contenedores. Los módulos dobles los pruebo acá
en el banco con 25 metros de cable puestos antes de despacharlos.

Una cosa más: el reefer que está fuera de servicio queda emparejado con
uno que anda, así el módulo ya va puesto y el día que vuelva se le suman
las sondas nomás, sin equipo nuevo.

Te paso el presupuesto: dos hojas, sin nombre de empresa, para que se lo
pases a quien corresponda. El equipo que ya está puesto sigue reportando,
así que mientras lo miran se puede ver el panel en cualquier momento.
```

> **Por qué está escrito así, para que no se suavice al copiarlo:**
> **(a)** Arranca con **"quedó armado tal cual me lo describiste"**. Andrés dio la configuración y lo primero que lee es que se hizo exactamente eso. Vale más que cualquier argumento técnico.
> **(b)** **Devuelve la información en su propio idioma** (2 afuera / 4 adentro, dos tiradas bajo techo): le confirma que se entendió el sitio.
> **(c)** **El tendido queda dicho en una línea, con algo a cambio y con el alivio adelante**: son dos tiradas, bajo techo, y nosotros mandamos el cable. No es una carga, es un reparto.
> **(d)** **La prueba con 25 m de cable compra confianza técnica.** Dice, sin decirlo, "sé que hay distancia y me hago cargo".
> **(e)** **El sexto reefer aparece como una previsión inteligente, no como un recorte.** Es la frase que muestra que estamos mirando el sitio de verdad.
> **(f)** **No le pide nada.** Andrés trabaja por turnos de 15 días y **no es él quien aprueba**. Cierra en *"te paso el presupuesto"*; la logística arranca con la aceptación y el anticipo, no antes.
> **(g)** **No menciona el material de la caja ni cómo se fabrica.** Ni acá ni en el PDF.

### 6.2 Guion de 5 líneas para que la presente él

1. **Arrancá por el problema, no por el producto:** "un reefer que se corta un fin de semana es la comida de todo el campamento, y hoy nadie se entera hasta que abren la puerta."
2. **Mostrá lo que ya anda:** abrí el panel en el celular y mostrá la temperatura de ahora del equipo instalado — sigue reportando mientras la propuesta se evalúa. Si podés, sacá una sonda al aire un minuto y que vean subir la curva. Eso convence más que el PDF.
3. **Decilo en una frase:** "los dos de afuera llevan cada uno su módulo estanco; los cuatro de adentro se cubren con dos. Tres sondas adentro de cada reefer, te avisa al celular si se sale de rango o si queda la puerta abierta, y arma el registro mensual solo."
4. **Si preguntan por el cable:** "solo hay dos tiradas y las dos son adentro, bajo techo. El cable lo mandan ellos y dicen cómo va; el caño lo pasamos nosotros. Los de la intemperie no llevan cable entre contenedores."
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

**Lo bueno de esta vuelta:** a Andrés le llega **exactamente el sistema que él describió**, armado sobre datos que dio él (los metros, el caño, la intemperie, el reparto adentro/afuera). Ya no hay que explicarle ningún "no". Eso simplifica el mensaje y lo deja bien parado adentro, que es lo único que él pidió para sí.

---

## Anexo — Fuentes consultadas

- Alcance del bus, pull-ups, tierras entre contenedores, estrella no conmutada y límite prudente de 15 m: `C:\Proyectos\frioseguro\hardware\ALCANCE_1WIRE.md` (@muestreador), §2.6.
- **Costo por equipo y stock declarado:** `C:\Proyectos\frioseguro\hardware\v1_modulos\BOM_KIT_V1.md` rev B (@hardware) — §1 inventario, §3.1 compra, §3.4 costo por equipo, §8.1 las dos mediciones que bloquean el pedido. Precios ML verificados el 2-sep-2026.
- Estado real y auditoría: `C:\Proyectos\frioseguro\entrega_scz\docs\ESTADO_HONESTO.md` · `AUDITORIA_HALLAZGOS.md`.
- **Qué hace hoy el firmware con sondas, puerta, relé y defrost (leído el 3-sep-2026):** `firmware_revival/sondas.h` (línea 31, `SONDAS_MAX`) · `config.h` 67-150 · `firmware_revival.ino` 369-375, 483-488, 804-944 · `comandos_nube.h` (**sin** comando de relé).
- Contrato base: `MATI-HQ\comercial\CONTRATO_TERMOVIGIA_v4.md`.
- Precios de canalización (§3.3, archivo), 1-Wire AN148, testo Saveris 2-T2, novillo INMAG, dólar BNA vendedor 1.535, Supabase Pro y Código de Conducta de Proveedores de PAAS: enlaces conservados en la v5.2 de este archivo (historial de git).

## Anexo — Lo que quedó abierto (para Matías, antes de mandar)

1. **Los números:** simple de exterior **USD 600 × 2 = 1.200** · doble de interior **USD 750 × 2 = 1.500** · repuestos **400** · puesta en marcha **1.500** · **inicial 4.600** · abono **500/mes** · B = **10.000 redondos**. Márgenes: 30,5 % el simple, 34 % el doble, 76 % el abono. **¿Van?** *(Si querés el 4.540 exacto, se llega bajando el repuesto a 340 y aceptando que sea un módulo simple — no lo recomiendo, §3.1.)*
2. **El sexto reefer entra a USD 260** (canal libre de su módulo doble, sin equipo nuevo) **+ USD 100/mes**. Está escrito en el documento del cliente. **¿Va así?**
3. **Riesgo de los dos buses de 20-25 m: asumido con conocimiento** (§2.2). Mitigación: pull-up 2k2 con opción a 1k (@esquematico), prueba de banco con 25 m en los dos dobles, spec de cable en el documento. **Confirmar con @esquematico que la posición del 1k queda en la placa.**
4. **10 h de software del módulo doble** (2ª puerta, 2º defrost con silenciado por reefer, `SONDAS_MAX` a 8) vendidas en el hito 2, costeadas en §3.2. **@firmware tiene que confirmar que 10 h alcanzan** — si son más, sale del margen, no del precio. **Los 2 módulos de exterior no necesitan ni una línea nueva: corren lo que ya anda.**
5. **Las 2 cajas IP65 de exterior no están en stock**: renglón de mayor plazo, pedir primero. **@hardware confirma medida y precio.** Y **las 3 cajas de 165×165 del stock no sirven para los dobles**: quedan para Bahía.
6. **Compra de materiales: ≈ $ 409.000 ($ 430.000 con flete)** — §3.7, cruzada contra stock. Reservados 3 ESP32 para las galgas de Dreyfus (P0 de octubre).
7. **@hardware: contar stock y hacer las 2 mediciones del §8.1 del BOM** (amperaje real de las fuentes, relé con IN al aire) antes de comprar.
8. **DECISIÓN DE PORTFOLIO, no comercial:** los kits son los mismos que iban a ser las demos de Bahía. **Si Cerro Moro compra, Bahía se queda sin demos.** Recomendación: reposición en el mismo pedido que la OC. **Decide el Director.**
9. **Preguntarle a Andrés cuál de los 4 de adentro está fuera de servicio** (§5.2 punto 3): define el emparejamiento, y de eso depende que el canal libre quede en un módulo instalado y andando.
10. **Verificación cruzada entre sondas: hoy NO existe.** Vendida en el hito 2. Con 3 sondas el argumento es incluso mejor (tres permiten saber cuál se desvió). Si no se puede cumplir, sacar el punto 3 del bloque "por qué 3 sondas".
11. **Accionamiento del relé desde el panel: tampoco existe.** Hito 5.
12. **El sensor de puerta viene deshabilitado por defecto** (`SENSOR_DOOR_ENABLED false`): que quede en la orden de armado habilitarlo y probar **las dos** puertas en los dobles.
13. **Cobertura de red en los 4 puntos** (§5.2). Si alguno queda corto, repetidor **antes** de despachar.
14. **La caja de exterior que ya está en el sitio es la prueba de campo** (§2.5 punto 4): pedirle a Andrés una foto después del primer temporal. Es evidencia gratis para la venta siguiente.
15. **Andrés:** opción 1, 2 o 3 de la Parte 7, y preguntarle para quién trabaja.
16. **PDF:** @diseno maqueta **un solo** documento de 2 páginas A4, marca Termovigía, sin logo ajeno, sin "Para:", sin validez. **Sin mencionar material de gabinete ni impresión 3D.** Archivo `PRESUPUESTO_CERRO_MORO.pdf` (+ `PRESUPUESTO_CERRO_MORO_INTERNO.pdf`).
17. Monotributo vs. RI: se pregunta cuando la empresa tenga nombre.
