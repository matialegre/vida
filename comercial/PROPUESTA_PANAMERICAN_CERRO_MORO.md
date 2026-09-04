# PROPUESTA — Monitoreo de temperatura de 6 reefers, campamento Cerro Moro (Santa Cruz)

> @comercial · **v4, 2026-09-03** · **para revisión de Matías antes del vie 5-sep**
> **Matías decide el número final, siempre.** Todo monto de acá abajo es propuesta con la cuenta a la vista.
> Doctrina: `PLATA.md`. Base técnica: `ALCANCE_1WIRE.md` (@muestreador), `hardware\v1_modulos\BOM_KIT_V1.md` (@hardware, rev B 2-sep), `entrega_scz\docs\ESTADO_HONESTO.md`, y el firmware `firmware_revival` leído el 3-sep.
> **El comprador NO es Pan American Silver:** es "una empresa" que Andrés todavía no identifica. Los dos documentos del cliente van **sin destinatario, sin logo ajeno y sin nombrar a Panamerican**. El archivo conserva el nombre por historial.

## Qué es esta versión: **DOS presupuestos separados, no un documento con escenarios**

Decisión de Matías: *"sino hacé dos presupuestos. Uno así, si es uno por reefer. Y otro, 1 por cada 2 reefers"*. El motivo es una contradicción que Andrés dejó abierta y que no nos corresponde resolver por él: **pidió expresamente los 3 módulos** *("pasale presupuesto por los 3 módulos, así cada uno controla dos reefers")* **y en el mismo rato dijo que acá no pueden haber cables aéreos** — y compartir un módulo entre dos reefers obliga a llevar un cable de uno al otro. En vez de elegir por él, se le dan los dos y elige él, que conoce el lugar.

| | **Presupuesto 1 — Un equipo por reefer** | **Presupuesto 2 — Un equipo cada dos reefers** |
|---|---|---|
| Equipos | 6 | 3 |
| Cable entre contenedores | ninguno | sí, canalizado por piso, ≤ 15 m por par (incluido) |
| Condiciones | **ninguna** | los dos reefers del par contiguos, ≤ 15 m, con canalización |
| Sondas totales | 24 | 24 |
| **Inicial** | **USD 4.920** | **USD 4.770** |
| **Abono** | **USD 250/mes** | **USD 250/mes** |
| Recomendado | **sí** | es válido si los pares están pegados |

**La diferencia son USD 150 sobre casi 5.000: un 3 %.** Ese es el hallazgo de esta versión y hay que tenerlo en la cabeza al presentar: compartir equipos casi no ahorra, porque las 24 sondas son las mismas en los dos casos y lo que se ahorra en electrónica se lo come la canalización y la ingeniería extra del bus compartido. Detalle en §4.4.

**Los dos presupuestos son gemelos en formato** —mismo producto por equipo, mismos 5 hitos, mismas dos formas de pago, mismas condiciones de pago, mismo recuadro de lo que el sistema no hace— justamente para que se comparen de un vistazo.

**Se eliminó la opción C** de la v2 ("sin inversión inicial", comodato con permanencia 24 meses) por decisión de Matías: *"el de la inversión inicial no lo ofrecería"*. Quedan **A** (equipos + servicio mensual) y **B** (anual adelantado).

---

## PARTE 1 — PRESUPUESTO 1, documento del cliente (@diseno maqueta 2 páginas A4)

> Copiar de acá hasta la línea de corte. Nada más. Escrito para que **lo presente alguien que no es vendedor** y se lea en dos minutos.

**Termovigía — Monitoreo de temperatura de reefers**
**Presupuesto 1: un equipo por reefer — 6 reefers, campamento Cerro Moro (Santa Cruz)**

**Qué es.** Un equipo sobre cada reefer, seis en total, que vigila la temperatura las 24 horas y avisa al celular cuando algo se sale de rango. Cada equipo es independiente: **no hay un solo cable entre contenedores y ningún reefer depende del de al lado**. Hoy ya hay un equipo instalado y reportando desde el campamento: se puede ver en vivo en el celular antes de decidir nada.

**Qué hace.**
- Mide la temperatura de cada reefer todo el tiempo, con hasta **4 sondas por reefer**, y la guarda en la nube (12 meses de historial).
- Avisa al celular de las personas que se definan cuando un reefer se sale del rango acordado por más tiempo del acordado.
- Avisa si **queda la puerta abierta** más de los minutos que se definan (sensor magnético incluido en cada reefer).
- Avisa cuando una sonda se desconecta o cuando un equipo deja de reportar.
- **No molesta durante el descongelamiento:** el equipo toma la señal de defrost del propio reefer y calla las alarmas mientras dura el ciclo, para que nadie aprenda a ignorar los avisos.
- Puede **accionar una sirena o baliza** en el pasillo: cada equipo trae 2 salidas a relé libres para eso.
- Genera solo el **registro mensual de temperatura por reefer**, para tener el papel cuando alguien lo pide.
- Funciona con la red de internet que ya hay en el campamento: no hay que contratar nada más.

**Por qué 4 sondas por reefer y no una.** Es la diferencia entre una instalación seria y un termómetro con WiFi.
1. **Un reefer no tiene "una" temperatura.** Cerca de la puerta, cerca del evaporador, arriba y abajo puede haber varios grados de diferencia. Con una sonda se mide un punto y se supone el resto; con cuatro se mide **el peor punto**, que es el que decide si la carga se arruinó. En una auditoría lo que vale es el peor punto, no el promedio.
2. **Si una sonda falla, el reefer sigue vigilado.** En un sistema cuyo trabajo es avisar, quedarse ciego es la peor falla posible: con una sola sonda cualquier problema deja el reefer sin vigilancia hasta que alguien viaje 1.500 km.
3. **Las sondas se controlan entre sí.** Si una empieza a desviarse respecto de las otras tres, se detecta y se avisa. Con una sola sonda, una deriva de 2 o 3 °C es invisible: el registro parece perfecto y está mintiendo. *(Se entrega en el hito 2.)*
4. **Se calibran las cuatro contra la misma referencia** (baño de hielo) y las diferencias quedan registradas. Eso es lo que convierte el registro en algo defendible ante un auditor.

**Qué se instala.** Seis equipos, uno por reefer, cada uno en un gabinete apto para intemperie con su fuente, **4 sondas, sensor magnético de puerta, 2 salidas a relé y entrada de defrost**, más un kit de repuesto que queda en el campamento. **No hay cable entre reefers, ni canalización, ni obra, ni condiciones de distancia**: cada equipo se monta en su propio contenedor y todo el cableado queda adentro de ese reefer. El montaje lo hace personal del campamento con los equipos preconfigurados desde Bahía Blanca y guía por videollamada: por eso esta propuesta no tiene línea de instalación ni viáticos.

**Puesta en marcha y ajuste en sitio (15 semanas, por hitos).** Los hitos son compromiso de entrega con fecha; no se facturan aparte, están incluidos en el precio.

| Hito | Qué queda funcionando | Semana |
|---|---|---|
| 1 | Las 4 sondas dentro de cada reefer, calibradas contra una misma referencia, rangos definidos, primera alerta real recibida en el celular | 2 |
| 2 | Ningún dato ni aviso se pierde si se corta la red; aviso de equipo que deja de reportar; **aviso de sonda que se desvía de las otras tres**; puerta y defrost validados en campo; una semana entera sin falsas alarmas | 6 |
| 3 | Acceso seguro: cada equipo y cada usuario con su propia credencial | 11 |
| 4 | Actualizaciones de los equipos a distancia, sin tocarlos | 13 |
| 5 | Panel para la empresa (usuarios de solo lectura), accionamiento de las salidas de alarma desde el panel e informe mensual descargable | 15 |

**Qué cuesta.**

| Concepto | USD |
|---|---|
| Equipo de monitoreo por reefer (equipo, gabinete, fuente, 4 sondas, sensor de puerta, 2 salidas a relé, entrada de defrost, probado en banco) — 6 × 480 | 2.880 |
| Kit de repuestos en sitio (1 equipo completo armado y probado + 4 sondas + 1 sensor de puerta) | 340 |
| Puesta en marcha y ajuste en sitio, 5 hitos | 1.700 |
| **Total equipos y puesta en marcha** | **4.920** |
| **Servicio mensual** (6 reefers: nube, alertas, soporte, reposición sin cargo, informe mensual) | **250 / mes** |

**Cómo se paga.** **50 % con la orden de compra** (anticipo de materiales) y **50 % contra los equipos instalados y reportando**. El servicio mensual arranca con el primer equipo andando.

| | **A. Equipos + servicio mensual** | **B. Anual adelantado** |
|---|---|---|
| Para quién | Compra activos y paga el servicio mes a mes | Tiene presupuesto de inversión y no quiere 12 facturas |
| Equipos y puesta en marcha | USD 4.920 (50 % con la OC, 50 % contra instalación) | Incluidos |
| Pago inicial total | USD 4.920 | USD 7.130 (equipos + 12 meses, con 10 % de descuento) |
| Mensual | USD 250 (los primeros 3 meses, mientras dura la puesta en marcha, se facturan al 50 %) | — el primer año; renovación anual USD 2.700 |
| Los equipos | Son del cliente | Son del cliente |
| **Total a 12 meses** | **7.545** | **7.130** |
| **Total a 24 meses** | **10.545** | **9.830** |

Facturación en dólares estadounidenses. De abonarse en pesos, se toma el tipo de cambio vendedor del Banco de la Nación Argentina de la fecha de pago. *Referencia al 3-sep-2026 (BNA vendedor $ 1.535): USD 4.920 ≈ $ 7.552.200 · USD 250 ≈ $ 383.750 · USD 7.130 ≈ $ 10.944.550.*

**Incluido en el servicio mensual:** nube con 12 meses de historial · alertas por temperatura, puerta abierta, sonda caída y equipo mudo · reposición sin cargo de cualquier equipo o sonda fallada, envío incluido · actualizaciones · soporte por WhatsApp y teléfono el mismo día hábil · informe mensual por reefer.

**Lo que hay que saber.** El sistema avisa; no garantiza la mercadería ni reemplaza la revisión del reefer. Sin energía en el equipo no mide: lo que avisa en ese caso es la nube, diciendo que dejó de reportar. La entrada de defrost necesita que el reefer tenga una señal o un contacto accesible; si alguno no lo tiene, esa entrada queda libre y el resto funciona igual. Las 2 salidas a relé vienen en el equipo; la sirena o baliza que se conecte no está incluida. Cada equipo necesita llegar a la red del campamento desde su propio reefer.

*Contacto en sitio: Andrés Leiva Chavez · Contacto comercial: Matías Alegre · Termovigía · Bahía Blanca · 2920 59-1019 · alegrematias08@gmail.com*

— — — — — — — — — — corte del Presupuesto 1 — — — — — — — — — —

---

## PARTE 2 — PRESUPUESTO 2, documento del cliente (@diseno maqueta 2 páginas A4)

> Gemelo del Presupuesto 1 en formato y en producto. Cambia el número de equipos, aparecen el cable y la canalización, y aparece una condición.

**Termovigía — Monitoreo de temperatura de reefers**
**Presupuesto 2: un equipo cada dos reefers — 6 reefers, campamento Cerro Moro (Santa Cruz)**

**Qué es.** Tres equipos que vigilan la temperatura de los seis reefers del campamento las 24 horas y avisan al celular cuando algo se sale de rango. Cada equipo atiende **dos reefers contiguos**, con cuatro sondas dentro de cada uno. Hoy ya hay un equipo instalado y reportando desde el campamento: se puede ver en vivo en el celular antes de decidir nada.

**Qué hace.** Lo mismo que el Presupuesto 1, reefer por reefer:
- Mide la temperatura de cada reefer todo el tiempo, con hasta **4 sondas por reefer**, y la guarda en la nube (12 meses de historial).
- Avisa al celular de las personas que se definan cuando un reefer se sale del rango acordado por más tiempo del acordado.
- Avisa si **queda la puerta abierta** más de los minutos que se definan (sensor magnético en cada reefer).
- Avisa cuando una sonda se desconecta o cuando un equipo deja de reportar.
- **No molesta durante el descongelamiento:** toma la señal de defrost de cada reefer y calla las alarmas mientras dura el ciclo.
- Puede **accionar una sirena o baliza**: cada equipo trae 2 salidas a relé libres, una por reefer.
- Genera solo el **registro mensual de temperatura por reefer**.
- Funciona con la red de internet que ya hay en el campamento: no hay que contratar nada más.

**Por qué 4 sondas por reefer y no una.** Es la diferencia entre una instalación seria y un termómetro con WiFi.
1. **Un reefer no tiene "una" temperatura.** Cerca de la puerta, cerca del evaporador, arriba y abajo puede haber varios grados de diferencia. Con una sonda se mide un punto y se supone el resto; con cuatro se mide **el peor punto**, que es el que decide si la carga se arruinó. En una auditoría lo que vale es el peor punto, no el promedio.
2. **Si una sonda falla, el reefer sigue vigilado.** Quedarse ciego es la peor falla posible en un sistema cuyo trabajo es avisar.
3. **Las sondas se controlan entre sí.** Si una empieza a desviarse respecto de las otras tres, se detecta y se avisa. Con una sola sonda, una deriva de 2 o 3 °C es invisible: el registro parece perfecto y está mintiendo. *(Se entrega en el hito 2.)*
4. **Se calibran las cuatro contra la misma referencia** (baño de hielo) y las diferencias quedan registradas: eso es lo que hace defendible el registro ante un auditor.

**Qué se instala.** Tres equipos, cada uno en un gabinete apto para intemperie con su fuente, atendiendo **dos reefers contiguos**: 4 sondas, sensor magnético de puerta, una salida a relé y entrada de defrost **para cada uno de los dos reefers**. Más un kit de repuesto que queda en el campamento. El cable de sondas que va del equipo al reefer vecino **se canaliza por piso o bandeja, nunca aéreo**, y esa canalización está incluida en el precio. El montaje lo hace personal del campamento con los equipos preconfigurados desde Bahía Blanca y guía por videollamada: por eso esta propuesta no tiene línea de instalación ni viáticos.

**La condición de este presupuesto, sin letra chica.** Los dos reefers de cada par tienen que estar **contiguos**, con el cable **canalizado por piso o bandeja (nunca aéreo)** y **no más de 15 metros** entre uno y otro. El porqué en una línea: el cable que une el equipo con las sondas es un bus de sensores digitales, y cuanto más largo y más cargado, más riesgo de lecturas intermitentes. **Si algún par no cumple, ese par se resuelve con dos equipos simples (uno por reefer, sin cable entre contenedores) por USD 110 más.** Está dicho acá para no renegociar nada después: el precio de la corrección ya está puesto.

**Puesta en marcha y ajuste en sitio (15 semanas, por hitos).** Los hitos son compromiso de entrega con fecha; no se facturan aparte, están incluidos en el precio.

| Hito | Qué queda funcionando | Semana |
|---|---|---|
| 1 | Las 4 sondas dentro de cada reefer, calibradas contra una misma referencia, rangos definidos, primera alerta real recibida en el celular. **La primera semana de medición sirve además de verificación del cable entre los dos reefers de cada par** | 2 |
| 2 | Ningún dato ni aviso se pierde si se corta la red; aviso de equipo que deja de reportar; **aviso de sonda que se desvía de las otras tres**; puertas y defrost de los dos reefers validados en campo; una semana entera sin falsas alarmas | 6 |
| 3 | Acceso seguro: cada equipo y cada usuario con su propia credencial | 11 |
| 4 | Actualizaciones de los equipos a distancia, sin tocarlos | 13 |
| 5 | Panel para la empresa (usuarios de solo lectura), accionamiento de las salidas de alarma desde el panel e informe mensual descargable | 15 |

**Qué cuesta.**

| Concepto | USD |
|---|---|
| Equipo de monitoreo para 2 reefers (equipo, gabinete, fuente, 8 sondas —4 por reefer—, 2 sensores de puerta, 2 salidas a relé, 2 entradas de defrost, probado en banco con el cable definitivo) — 3 × 790 | 2.370 |
| Cable y canalización entre los dos reefers de cada par (caño galvanizado, curvas, grampas, caja de paso, cable exterior) — 3 × 60 | 180 |
| Kit de repuestos en sitio (1 equipo completo armado y probado + 4 sondas + 1 sensor de puerta) | 420 |
| Puesta en marcha y ajuste en sitio, 5 hitos | 1.800 |
| **Total equipos y puesta en marcha** | **4.770** |
| **Servicio mensual** (6 reefers: nube, alertas, soporte, reposición sin cargo, informe mensual) | **250 / mes** |

**Cómo se paga.** **50 % con la orden de compra** (anticipo de materiales) y **50 % contra los equipos instalados y reportando**. El servicio mensual arranca con el primer equipo andando.

| | **A. Equipos + servicio mensual** | **B. Anual adelantado** |
|---|---|---|
| Para quién | Compra activos y paga el servicio mes a mes | Tiene presupuesto de inversión y no quiere 12 facturas |
| Equipos y puesta en marcha | USD 4.770 (50 % con la OC, 50 % contra instalación) | Incluidos |
| Pago inicial total | USD 4.770 | USD 7.000 (equipos + 12 meses, con 10 % de descuento) |
| Mensual | USD 250 (los primeros 3 meses, mientras dura la puesta en marcha, se facturan al 50 %) | — el primer año; renovación anual USD 2.700 |
| Los equipos | Son del cliente | Son del cliente |
| **Total a 12 meses** | **7.395** | **7.000** |
| **Total a 24 meses** | **10.395** | **9.700** |

Facturación en dólares estadounidenses. De abonarse en pesos, se toma el tipo de cambio vendedor del Banco de la Nación Argentina de la fecha de pago. *Referencia al 3-sep-2026 (BNA vendedor $ 1.535): USD 4.770 ≈ $ 7.321.950 · USD 250 ≈ $ 383.750 · USD 7.000 ≈ $ 10.745.000.*

**Incluido en el servicio mensual:** nube con 12 meses de historial · alertas por temperatura, puerta abierta, sonda caída y equipo mudo · reposición sin cargo de cualquier equipo o sonda fallada, envío incluido · actualizaciones · soporte por WhatsApp y teléfono el mismo día hábil · informe mensual por reefer.

**Lo que hay que saber.** El sistema avisa; no garantiza la mercadería ni reemplaza la revisión del reefer. Sin energía en el equipo no mide: lo que avisa en ese caso es la nube, diciendo que dejó de reportar. **Si un equipo se apaga o falla, quedan sin vigilancia los dos reefers que atiende.** La entrada de defrost necesita que el reefer tenga una señal o un contacto accesible; si alguno no lo tiene, esa entrada queda libre y el resto funciona igual. Las salidas a relé vienen en el equipo; la sirena o baliza que se conecte no está incluida. Cada equipo necesita llegar a la red del campamento desde donde esté montado.

*Contacto en sitio: Andrés Leiva Chavez · Contacto comercial: Matías Alegre · Termovigía · Bahía Blanca · 2920 59-1019 · alegrematias08@gmail.com*

— — — — — — — — — — corte del Presupuesto 2: lo de abajo NO se manda — — — — — — — — — —

---

## PARTE 3 — Alcance (interno)

### 3.1 Qué hay hoy, verificado (3-sep-2026)

| Hecho | Evidencia |
|---|---|
| 1 equipo instalado en el campamento, `REEFER_01_SCZ`, firmware `firmware_revival` 2.6.21 | Puesto el 21-ago; reconectado por Andrés el 3-sep |
| Reportando cada ~5 s | Consulta a la base de Santa Cruz, 3-sep |
| **1 sola sonda y está FUERA del reefer** — mide ambiente | Andrés espera confirmación de Matías para meterlas |
| Elección de red abierta con internet real: probada 128 ciclos | `ESTADO_HONESTO.md` |
| **Sin contrato y sin un peso cobrado** | `PLATA.md` |
| **"Acá no pueden haber cables aéreos"** | Andrés, WhatsApp 3-sep 17:11 |
| **"Pasale presupuesto por los 3 módulos, así cada uno controla dos reefers"** | Andrés, WhatsApp 3-sep 17:13 |

**Las dos últimas filas se contradicen** y de ahí sale esta versión de dos presupuestos: ver §6.2.

### 3.2 Por qué el Presupuesto 1 es el recomendado (y por qué el 2 se cotiza igual, sin descalificarlo)

**1. El cable entre contenedores es el problema, y no lo arregla ningún software.** Un reefer es un contenedor metálico con su propia puesta a tierra, alimentado desde un tablero de campamento probablemente con grupo electrógeno. Tirar el cable de sonda del reefer A al B ata el GND de las sondas de B al GND del ESP32 que está en A por un conductor fino. Cualquier diferencia de potencial entre esas dos tierras —décimas de volt en régimen, volts durante el arranque de un motor— circula por ese retorno, y como **DQ se mide contra ese mismo GND, la diferencia aparece sumada al dato**. No la filtra el trenzado: no es modo común, es corriente real por el retorno. @muestreador lo llama textualmente *"el riesgo dominante de esta instalación"* (`ALCANCE_1WIRE.md` §2.6).

**2. Más sondas empeoran el bus compartido.** Cada sonda suma capacitancia y más capacitancia = **menor largo máximo admisible**. Con 4 sondas por reefer, el módulo compartido lleva **8 sondas sobre un bus que además cruza al contenedor vecino**: bus largo **y** bus cargado, las dos cosas juntas. En el Presupuesto 1 las 4 sondas viven en 2-4 m dentro del mismo contenedor.

> **Argumento que NO hay que usar (y que en una versión anterior estuvo mal escrito):** `SONDAS_MAX 4` (línea 31 de `firmware_revival/sondas.h`) **no es un límite de arquitectura** — es el tamaño de un arreglo, se cambia a 8 o a 16 en una línea, y el bus 1-Wire direcciona por ROM de 64 bits, así que admite decenas de sondas en un mismo pin. Las 4 sondas por reefer son **decisión de producto, ampliable**. Para el Presupuesto 2 hay que subirlo a 8: **es una línea, y está contemplada en las horas de §4.3.**

**3. Sin equipos compartidos no hay canalización** —que es lo que Matías no quiere recomendar (*"la canalización por par de reefers, no la recomendaría"*)—, no hay condición de metros y no hay cláusula de corrección. El Presupuesto 1 es una sola cosa, sin condicionales.

**4. Y hay un punto de falla menos:** si se apaga un equipo del Presupuesto 2, quedan dos reefers ciegos. Está escrito en el recuadro honesto de la Parte 2, sin dramatizarlo.

**Lo que el Presupuesto 1 cuesta y hay que decir:** hacen falta **6 puntos con cobertura de la red del campamento**, no 3. Si algún reefer queda sin señal se resuelve con un repetidor —material barato— pero hay que saberlo antes de despachar. Es la única pregunta técnica nueva que abre el escenario recomendado.

**Cómo se presenta el 2, sin quemarlo:** es un presupuesto legítimo, cotizado en serio, con la canalización a la vista y una condición honesta. Si los reefers están pegados y hay bandeja, **es una opción razonable y ahorra USD 150**. Lo que no se hace es esconder la condición ni descubrirla después de la orden de compra.

### 3.3 Qué lleva cada equipo, y qué de eso anda HOY (verificado en el código el 3-sep)

| Función | P1 (por reefer) | P2 (por módulo) | Qué hace el firmware hoy | Evidencia |
|---|---|---|---|---|
| Sondas DS18B20 | hasta 4 | hasta 8 (4 por reefer) | Cada una identificada por ROM de 64 bits y reportada por separado; enganche en caliente; aviso si se desconecta; **offset de calibración por sonda en NVS** | `sondas.h`: `sondasEscanear`, `sondasLeer`, `sondasCalibrar`. **P2 necesita subir `SONDAS_MAX` de 4 a 8: una línea** |
| **Verificación cruzada entre sondas** | — | — | **NO existe.** `sondasCalibrar()` iguala las sondas en un momento dado, pero el lazo de lectura **no compara sondas entre sí** ni alerta por deriva | ídem. Vendida en el **hito 2** en los dos presupuestos, con la aclaración en la página del cliente |
| Sensor magnético de puerta | 1 | 2 | Implementado: GPIO5, alerta por puerta abierta más de 180 s (configurable) y **suprime la alerta de temperatura mientras está abierta**. Viene **deshabilitado por defecto** (`SENSOR_DOOR_ENABLED false`) | `config.h` 72-74, 105, 119 · `.ino` 804-890. **P2 necesita una segunda puerta: la plaqueta v1 ya tiene 3 pines (GPIO5/13/14), falta el software** |
| Salidas a relé | 2 | 2 (una por reefer) | **1 gobernada**: GPIO26, se activa sola con la alerta si `relayEnabled`. La segunda queda cableada y disponible. **El accionamiento manual desde el panel NO existe** | `config.h` 76-77, 140-150 · `.ino` 369-375, 483-488, 915-944 · `comandos_nube.h` sin comando de relé → **hito 5** |
| Entrada de defrost | 1 | 2 | Implementada: GPIO33, contacto NA o NC configurable; durante el ciclo **deshabilita todas las alertas**, con 30 min de enfriamiento configurable | `config.h` 91-96, 122 · `.ino` 54-55, 100-101, 872-878. **P2 necesita una segunda entrada: software** |

**Regla de venta:** lo único que **no** está andando hoy es la **verificación cruzada entre sondas** y el **accionamiento manual del relé desde el panel**; los dos van en hitos con fecha, no como característica de hoy. **Y el Presupuesto 2 necesita además software que hoy no existe** (segunda puerta, segundo defrost, `SONDAS_MAX` a 8): son las 8 h extra que explican por qué su puesta en marcha cuesta USD 100 más que la del Presupuesto 1 aunque tenga la mitad de equipos.

**Orden de armado, para los dos:** línea `entrega_scz`/`firmware_revival` (identificación por ROM), **no** `firmware_modular` (lee por índice: si cae una sonda, la otra se reporta con el nombre equivocado). Pull-up **2k2**, 3 hilos (nada de parasite power), 100 nF + 10 µF al pie de la sonda más lejana. En el P2 además: **prueba de banco §6 de `ALCANCE_1WIRE.md` con 15 m de cable real y las 8 sondas, criterio cero errores, antes de despachar.**

### 3.4 Lo que se instala, y quién

Por equipo: gabinete estanco IP65 165×165×80, fuente de 5 V 2 A, plaqueta de conexiones con borneras a tornillo, ESP32 en zócalo, módulo de 2 relés, prensacables, sondas DS18B20 estancas con cable, reed de puerta. **Montaje: Andrés (o quien la empresa designe), con kit preconfigurado y probado en banco + videollamada.** Dos pasajes a Santa Cruz, alojamiento, inducción y 5 días de ingeniero rondan los $ 2.500.000, y Matías no puede viajar en octubre (parada de Dreyfus). Eso es lo que ninguno de los dos presupuestos cobra.

### 3.5 Canalización del Presupuesto 2 — "no aéreo" tiene precio, y está costeado

Supuesto por par: equipo montado en un reefer, cable al vecino contiguo por piso, **~10 m de caño + ~20 m de UTP exterior** (ida por el caño, más subidas y entradas a cada reefer).

| Material (por par) | Cant. | Precio ML AR (3-sep-2026) | Subtotal |
|---|---|---|---|
| Caño galvanizado Daisa 3/4 liviano, tira 3 m | 4 | $ 11.637 c/u | $ 46.548 |
| Curvas, grampas, caja de paso estanca, prensacables, conectores | — | estimado | $ 15.000 |
| Cable UTP cat5e exterior 100 % cobre (rollo 100 m ≈ $ 40.000) | 20 m | $ 400/m | $ 8.000 |
| **Total por par** | | | **≈ $ 70.000 ≈ USD 46** |

Se cotiza **USD 60 por par** (flete a Santa Cruz y sobrante). Si el campamento ya tiene bandeja o caño disponible —**hay que preguntárselo a Andrés, §6.2**— el kit se reduce a cable y accesorios y el ahorro se traslada. Alternativa más barata si el tramo va embutido o bajo losa: corrugado 3/4 pesado ($ 13.500 el rollo de 25 m). Fuentes en el anexo.

### 3.6 Opcionales, después de la primera orden

Sirena o baliza física para conectar a la salida de relé (USD 40; el relé ya está incluido) · sonda **quinta o siguiente** en un reefer (USD 40 + USD 5/mes) · base con batería y 4G, la única que avisa el corte de energía por sí misma (a cotizar). Se ofrecen cuando las sondas estén andando, no antes.

---

## PARTE 4 — Números de respaldo

Todo lo de abajo sale del BOM real (`BOM_KIT_V1.md` rev B de @hardware, precios de MercadoLibre AR verificados el 2-sep-2026, §3.4 "Costo real por equipo", **a precio de reposición**), no de prorratear la v2. Cambio $ → USD al BNA vendedor 1.535 del 3-sep.

### 4.1 Presupuesto 1 — equipo por reefer, USD 480

| | ARS | USD |
|---|---:|---:|
| Materiales sin sondas ni reed: compra nueva §3.1 ÷ 5 = 35.674 + ESP32 13.990 + **1** módulo de 2 relés 5.028 + fuente 5 V 2 A 7.980 + caja IP65 8.500 | 71.172 | **46** |
| 4 sondas DS18B20 estancas rearmadas con 3 m de cable y prensacable (la sumergible de plaza viene con 1 m) | ~36.800 | **24** |
| 1 sensor magnético de puerta cableado, con carcasa | 4.746 | **4** |
| Envío a Santa Cruz, prorrateado por equipo | ~12.300 | **8** |
| Armado (1,5 h), prueba de banco documentada con las 4 sondas (1 h), garantía de reposición amortizada | | **90** |
| Parte de plataforma del desarrollo: USD 1.000 repartidos en **6** equipos | | **167** |
| Margen | | **141** |
| **Precio** | | **480** |

**La economía de escala que pedía Matías está en un solo renglón: la plataforma pasa de USD 333 por equipo (v2, 3 módulos) a USD 167.** Eso es lo que permite bajar de 720 a 480 con más hardware adentro. Margen **29 %** (la v2 tenía 22,5 %) y la plataforma sigue recuperando los mismos USD 1.000 que la v1 cobraba como "desarrollo al 50 %". Nada se regaló.

**Dato de venta:** la v2 cotizaba **USD 500 el módulo simple de un solo reefer**, con 2 sondas y sin puerta, sin relés y sin defrost. Acá son **USD 480 con 4 sondas, puerta, 2 relés y defrost**: el precio por reefer bajó y el producto subió.

### 4.2 Presupuesto 2 — módulo para 2 reefers, USD 790

| | ARS | USD |
|---|---:|---:|
| Materiales sin sondas ni reed (mismo kit; caja y plaqueta más holgadas por 10 borneras) | ~76.750 | **50** |
| 8 sondas DS18B20 estancas rearmadas con cable (4 cortas + 4 largas, las del reefer vecino) | ~73.700 | **48** |
| 2 sensores magnéticos de puerta | 9.492 | **8** |
| Envío a Santa Cruz, prorrateado (3 bultos más pesados) | ~15.350 | **10** |
| Armado (2 h) + **prueba de banco con 15 m de cable real y las 8 sondas** (1,5 h) + garantía amortizada | | **110** |
| Parte de plataforma del desarrollo: USD 1.000 repartidos en **3** módulos | | **333** |
| Margen | | **231** |
| **Precio** | | **790** |

Margen **29 %**, el mismo criterio que el P1: los dos presupuestos ganan lo mismo en proporción, así que **la recomendación no está sesgada por el margen**. Por reefer el módulo compartido sale 395 (contra 480), pero hay que sumarle USD 30 por reefer de canalización → 425, y la diferencia se termina de comer en la puesta en marcha (§4.3).

**Corrección si un par no cumple la condición:** reemplazar un módulo doble por dos equipos simples = 2 × 480 − 790 − 60 de canalización que no se usa = **+ USD 110 por par**. Está escrito en la Parte 2, así que no hay renegociación. Si fallaran los tres pares: +330 → USD 5.100, **más caro que el Presupuesto 1**, que además no tuvo que pagar la ingeniería del bus compartido. Conviene tenerlo a mano.

### 4.3 Puesta en marcha: 1.700 (P1) contra 1.800 (P2)

| Trabajo | P1 (h) | P2 (h) |
|---|---:|---:|
| Sondas, rangos y umbrales por reefer + **calibración de las 24 sondas** contra referencia y registro de offsets | 16 | 16 |
| Registro exportable con código de verificación | 16 | 16 |
| Panel multi-equipo y usuarios de lectura | 12 | 12 |
| Puesta en marcha remota (alta, credencial, OTA verificada, prueba de puerta y defrost), pruebas de campo con Andrés, runbook y capacitación | **20** (6 equipos) | **12** (3 equipos) |
| Salud de bus, histéresis de 3 barridos y **verificación cruzada entre sondas** | 4 | 4 |
| **Solo P2:** segunda puerta y segundo defrost por módulo, `SONDAS_MAX` a 8, y validación del bus compartido en sitio | — | **12** |
| **Total a USD 25/h** | **68 = USD 1.700** | **72 = USD 1.800** |

**Es el renglón contraintuitivo, y por eso hay que decirlo:** el Presupuesto 2 tiene la mitad de equipos y **su puesta en marcha cuesta más**, porque las 24 sondas son las mismas y arriba hay software que hoy no existe (§3.3). **Los 5 hitos y sus fechas son idénticos en los dos.**

### 4.4 Los dos presupuestos, lado a lado

| | **P1 — un equipo por reefer** | **P2 — un equipo cada dos** | Diferencia |
|---|---:|---:|---|
| Equipos | 6 × 480 = 2.880 | 3 × 790 = 2.370 | −510 |
| Cable y canalización | 0 | 180 | +180 |
| Repuestos | 340 | 420 | +80 |
| Puesta en marcha | 1.700 | 1.800 | +100 |
| **Inicial** | **4.920** | **4.770** | **−150 (−3 %)** |
| Abono | 250/mes | 250/mes | igual |
| 12 meses (A) | 7.545 | 7.395 | −150 |
| 24 meses (A) | 10.545 | 10.395 | −150 |
| Sondas en servicio | 24 | 24 | igual |
| Cable entre contenedores | 0 m | ~120 m canalizados | — |
| Condiciones | ninguna | contiguos, ≤ 15 m, canalizado | — |
| Reefers ciegos si falla un equipo | 1 | 2 | — |
| Obra en el sitio | ninguna | 3 canalizaciones | — |

**Qué se compra con esos USD 150:** poco menos de un mes de abono. A cambio, cero obra, cero cable entre contenedores (que es justo lo que el sitio no admite según el propio Andrés), cero condición de distancia, cero riesgo de tierras, y un reefer ciego en vez de dos si un equipo se apaga.

**Ese es todo el argumento, y es honesto: el P2 no es una trampa, simplemente casi no ahorra.** El motivo estructural es que **las 24 sondas son las mismas en los dos casos**, y el ahorro de tres ESP32 con sus cajas y fuentes (~USD 510) se lo comen la canalización (180), el repuesto más caro (80) y la ingeniería del bus compartido (100).

### 4.5 Servicio mensual: qué cuesta servir y qué se cobra (igual en los dos)

| Costo directo mensual | v2 (12 sondas) | **v4 (24 sondas, 6 reed)** |
|---|---:|---:|
| Supabase Pro | 25 | 25 |
| Reposición amortizada (equipos y sondas en garantía) | 10 | **20** |
| Soporte (2 h → 2,5 h a USD 25) | 50 | **62** |
| Informe mensual | 25 | 25 |
| **Total** | **110** | **132** |

**Tarifa: USD 100 de sitio + USD 25 por reefer × 6 = USD 250/mes.** Margen bruto USD 118 (47 %). Sube de 20 a 25 por reefer porque en la v2 un reefer eran **2 sondas** y ahora son **4 sondas + puerta + salidas + defrost**. **Y el precio por punto medido baja: de USD 18,3 a 10,4 por sonda y por mes** — es la respuesta si preguntan por qué el abono sube USD 30. Con 5 reefers activos son USD 225; el sexto entra por 25 cuando vuelva.

**El escalón de los primeros 3 meses al 50 % (USD 125) se conserva en A:** es apenas menos que el costo directo y es lo que hace honesta la propuesta mientras dura la puesta en marcha. En B no aplica: ya lleva descuento.

### 4.6 Condiciones de pago — 50 / 50, y por qué no 25

**Decisión del Director, va en los dos presupuestos: 50 % con la orden de compra (anticipo de materiales) y 50 % contra los equipos instalados y reportando.** El abono arranca con el primer equipo andando.

El fundamento es de caja y es concreto: los materiales del P1 son **7 equipos a armar** (6 + el repuesto) y el BOM de @hardware está presupuestado para 5 kits. Con un anticipo del 25 % (USD 1.230) Matías estaría **financiando de su bolsillo la mayor parte de los materiales** y cobrando el resto a 60 días de un contratista que todavía no tiene nombre. Con el 50 % (USD 2.460) los materiales quedan cubiertos con margen antes de comprar el primer componente.

**Qué cambia respecto de la v2:** desaparece el esquema de facturar la puesta en marcha por hitos (40/30/30). Los hitos siguen existiendo **como compromiso de entrega con fecha**, y así están escritos en los dos documentos del cliente: *"los hitos no se facturan aparte, están incluidos en el precio"*. **Es un punto para que Matías confirme:** cobrar antes de entregar los hitos es más cómodo para la caja y más exigente con la palabra. Está en el anexo de pendientes.

### 4.7 Las dos formas de pagar, y por qué se cayó la tercera

**A. Equipos + servicio mensual.** P1: 4.920 + 3 × 125 + 9 × 250 = **7.545** el primer año, 3.000/año después, **24 meses 10.545**. P2: 4.770 + 375 + 2.250 = **7.395**, **24 meses 10.395**.

**B. Anual adelantado, 10 % de descuento.** P1: (4.920 + 3.000) × 0,9 = **7.130** (7.128 redondeado a número comercial); renovación 2.700/año; **24 meses 9.830**. P2: (4.770 + 3.000) × 0,9 = **7.000** (6.993 redondeado); **24 meses 9.700**. Por qué 10 % y no 8: tiene que valer más que el escalón de A (que ya le deja USD 375 al que paga mes a mes), y lo que compra es concreto — **cero riesgo de cobranza durante 12 meses con un contratista que probablemente pague a 60-90 días, una factura en lugar de doce, y caja para armar los equipos.**

**C, eliminada.** Matías: *"el de la inversión inicial no lo ofrecería"*. Coincide con el párrafo de riesgo que la propia v2 tenía escrito: era la única que ponía USD ~4.900 nuestros en manos de un contratista a 1.500 km, sin poder retirar los equipos, recuperables recién cerca del mes 20, y la única que no existía sin contrato firmado con permanencia. **No se vuelve a ofrecer sin contrato validado por contador y un cliente con historial de pago.** Con dos opciones el comprador elige; con tres se paraliza.

### 4.8 Moneda, validez, facturación

**Facturación en USD, pago en pesos al BNA vendedor de la fecha de pago, sin validez en el PDF.** Nota interna: revisar precios si pasan más de 6 meses desde el 3-sep. Antes de la cotización firme hay que saber: monotributo vs. RI, plazo de pago, si acepta la cláusula de moneda, quién firma. Se pregunta cuando la empresa tenga nombre.

### 4.9 Contra una pérdida y contra la competencia

Una pérdida de 3 t valuada al precio de novillo en pie ($ 4.181/kg, INMAG jul-2026) son $ 12,5 M: unos **2 años y medio de servicio**. testo Saveris 2-T2: USD 318 por unidad y mide un punto; para cubrir 24 puntos harían falta 24 unidades = **USD 7.632** antes de importación, sin nube, sin puerta, sin relé, sin defrost, y se configura con una red WiFi y una clave — que es exactamente lo que este sitio no tiene.

---

## PARTE 5 — Puesta en marcha: qué es cada hito por dentro (idéntico en los dos presupuestos)

Es el plan de endurecimiento de la auditoría del 26-ago, con nombre de cliente. Octubre es Dreyfus: por eso los hitos pesados caen después.

| Hito (cliente) | Etapa interna | Desde | Hasta | Cómo se acepta |
|---|---|---|---|---|
| 1 — Las 4 sondas adentro y calibradas, rangos, primera alerta real | E0 | lun 8-sep | **vie 19-sep** | Captura de la alerta en el celular + registro en nube + **planilla de calibración con el offset de cada una de las 24 sondas**. En el P2, además: la primera semana es la verificación del cable de cada par (CRC malos o lecturas de 85,00 °C → se parte el par, + USD 110 ya cotizados) |
| 2 — Nada se pierde, nada sobra | E1: buffer offline, alertas encoladas, alerta de sonda caída que llega, vigía de equipo mudo, discriminador de bus + histéresis, **detección de sonda que se desvía de las otras del mismo reefer**, habilitación y prueba de puerta y defrost | lun 22-sep | **vie 10-oct** | Desenchufar una sonda y que llegue la alarma; cortar la red 20 min sin perder lecturas; abrir una puerta 4 min y que avise; forzar un defrost y que **no** avise; una semana sin falsas alarmas |
| 3 — Acceso seguro | E2: RLS cerrada, credencial por equipo, secretos fuera del binario, revocar claves quemadas | lun 13-oct | **vie 14-nov** | Con la clave vieja no se escribe; todos los equipos siguen reportando |
| 4 — Actualización a distancia | E3: OTA con manifiesto inmutable | lun 17-nov | **vie 28-nov** | Tres actualizaciones seguidas por aire al primer intento, en todos los equipos |
| 5 — Panel e informe | E4: usuarios de lectura, vista de 6 reefers, exportación con código, informe mensual automático, **comando de relé desde el panel** | lun 1-dic | **vie 19-dic** | Un usuario de la empresa entra solo, baja el informe y acciona una salida desde el panel |

Lo que hoy está roto y cada hito arregla (llave maestra en el binario, datos perdidos sin red, umbral en 50 °C, equipo muerto que no avisa, OTA que entra 1 de 4) está en `AUDITORIA_HALLAZGOS.md`; no cambió.

---

## PARTE 6 — Qué necesitamos para cerrar

### 6.1 De la empresa, cuando tenga nombre

Quién firma, cómo factura (monotributo/RI, plazo), si acepta la cláusula de moneda, **cuál de los dos presupuestos elige** y cuál de las dos formas de pago, y confirmación de que el montaje lo hace personal del campamento (sin personal nuestro en sitio no corresponde ART ni legajo de contratista).

### 6.2 De Andrés: la contradicción que hay que resolver, y cómo preguntarla

**La contradicción, escrita:** el 3-sep a las 17:11 dijo *"acá no pueden haber cables aéreos"* y a las 17:13 *"pasale presupuesto por los 3 módulos, así cada uno controla dos reefers"*. **Un módulo cada dos reefers exige un cable de un contenedor al otro.** O ese cable va por el piso canalizado (y entonces el Presupuesto 2 es válido, con su condición y su costo de canalización), o no hay por dónde llevarlo (y entonces el único que se puede instalar es el Presupuesto 1).

**No la resolvemos nosotros: la resuelve él, que conoce el lugar.** Por eso van los dos presupuestos y por eso la pregunta se hace sin tono de auditoría — él es el que vende adentro y su criterio es el activo más valioso que tenemos en Cerro Moro.

**Las tres cosas que hay que preguntarle (redacción exacta en §7.1):**
1. **Por dónde irían los cables entre los dos reefers de cada par** — piso, bandeja, canaleta, por arriba de algo.
2. **Si ya hay bandeja o caño hecho** entre ellos, o hay que poner la canalización nosotros.
3. **A cuántos metros está uno del otro** (por donde iría el cable, no en línea recta).

Y dos preguntas que no dependen del presupuesto elegido: **¿la red del campamento llega a los seis reefers?** (crítica para el P1: son 6 puntos con señal, no 3) y **¿los reefers tienen una señal o contacto de defrost accesible?**

### 6.3 Qué hacer con cada respuesta (regla de decisión escrita de antemano)

| Si Andrés contesta… | Va el… | Qué se hace |
|---|---|---|
| **Están pegados y hay bandeja o caño** | **Presupuesto 2** | Se manda el P2 y **el kit de canalización baja** (solo cable y accesorios): el ahorro se traslada al cliente y se recotiza el renglón de 180 hacia abajo. El P1 queda igual como alternativa recomendada |
| **Están pegados pero no hay por dónde: hay que canalizar** | **los dos** | Es el caso base ya cotizado. Se manda el P2 con los USD 180 a la vista y el P1 al lado: **la diferencia real son USD 150** y la decisión la toma el cliente sabiendo lo que compra |
| **Están lejos (más de 15 m) o no hay forma de llevar el cable** | **Presupuesto 1** | Es el único instalable. Se dice sin dramatizar: *"con esa distancia el compartido no da, va uno por reefer"* |
| **No sabe / no puede medir ahora** | **los dos** | Se mandan igual, con el P1 marcado como recomendado. Ningún dato pendiente frena el envío de la propuesta |

**Regla de fondo:** el dato que falta **ajusta** la propuesta, no la bloquea. Los dos presupuestos ya están cotizados con su condición y su corrección de USD 110 por par, así que ninguna respuesta obliga a renegociar nada.

---

## PARTE 7 — Para Andrés (aparte de los PDF)

### 7.1 WhatsApp de respuesta (lo manda Matías)

```
Andrés, te armo DOS presupuestos y elegís vos, que conocés el lugar.

Uno es como me pediste: 3 módulos, cada uno controlando dos reefers. El
otro es uno por reefer, seis. Los dos van con lo mismo adentro: hasta 4
sondas por reefer, sensor de puerta, dos salidas para sirena o baliza y una
entrada para tomar el defrost del propio reefer, así no te alarma cada vez
que descongela.

Te explico por qué te mando los dos. Vos me dijiste que ahí no pueden
haber cables aéreos, y el módulo compartido necesita sí o sí un cable de un
reefer al otro. Si ese cable puede ir por el piso, canalizado, el de 3
módulos anda perfecto y lo cotizo con el caño y todo incluido. Si no hay
por dónde llevarlo, entonces el que se puede instalar es el de uno por
reefer, que no lleva un solo cable entre contenedores.

Por eso necesito tres cosas de tu lado, que las sabés vos y no las puedo
adivinar desde acá:
1) Los dos reefers de cada par, ¿por dónde iría el cable de uno al otro?
   (piso, bandeja, canaleta)
2) ¿Ya hay bandeja o caño hecho entre ellos, o hay que ponerlo?
3) ¿A cuántos metros está uno del otro, por donde iría el cable?

Y dos más, que valen para cualquiera de los dos: ¿la red del campamento
llega bien a los seis reefers o hay alguno que queda medio lejos del wifi?
¿Y los reefers tienen alguna señal o contacto de descongelamiento al que
se pueda enganchar?

Los dos presupuestos van sin nombre de empresa, así se los ofrecés a quien
corresponda. Dos hojas cada uno: qué es, qué hace, qué cuesta y dos formas
de pagarlo (compran los equipos y pagan el mensual, o pagan el año de una
con descuento).

Un adelanto para que no te sorprenda el número: entre los dos hay muy poca
diferencia de plata, como 150 dólares sobre casi 5.000. Las sondas son las
mismas 24 en los dos casos, así que lo que se ahorra en cajas se va en el
caño y el cable. Te lo digo de una para que no parezca que te quiero vender
el más caro.
```

### 7.2 Guion de 5 líneas para que la presente él

1. **Arrancá por el problema, no por el producto:** "un reefer que se corta un fin de semana es la comida de todo el campamento, y hoy nadie se entera hasta que abren la puerta."
2. **Mostrá lo que ya anda:** abrí el panel en el celular y mostrá la temperatura de ahora del equipo instalado. Si podés, sacá una sonda al aire un minuto y que vean subir la curva. Eso convence más que el PDF.
3. **Decilo en una frase:** "cuatro sondas adentro de cada reefer, te avisa al celular si se sale de rango o si queda la puerta abierta, y arma el registro mensual solo."
4. **Dejá los dos presupuestos y explicá la diferencia en una línea:** "uno es una caja por reefer, el otro una caja cada dos con cable canalizado entre ellos; se llevan 150 dólares de diferencia y el de una por reefer no necesita obra."
5. **Lo que NO prometés:** que garantiza la mercadería (avisa, no garantiza) · que avisa el corte de luz (avisa que el equipo dejó de reportar) · que la sirena está incluida (van las salidas, la sirena se conecta) · que está terminado (hay una puesta en marcha de 15 semanas por hitos, y está en el precio) · fechas o precios distintos a los de los PDF. Cualquier pregunta técnica o de números: "eso lo contesta Matías, lo llamamos ahora."

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

**Lo nuevo de esta vuelta, y es lo más delicado del documento:** Andrés pidió el de 3 módulos y le llegan **dos** presupuestos. Todo el WhatsApp de §7.1 está redactado para que eso se lea como *"te doy las dos y elegís vos, que conocés el lugar"* y nunca como *"tu idea no servía"*. Tres decisiones concretas de redacción, por si Matías quiere cambiarlas: **(a)** el presupuesto que él pidió se nombra primero; **(b)** la contradicción se le devuelve como una pregunta práctica sobre el sitio, no como una objeción a su criterio; **(c)** la diferencia de precio se adelanta en el propio mensaje (*"como 150 dólares sobre casi 5.000"*) para que no parezca que le estamos empujando el más caro — es el riesgo de reputación más grande que corre este lead, y se desactiva diciéndolo primero nosotros.

---

## Anexo — Fuentes consultadas (3-sep-2026)

- Alcance del bus, pull-ups, **tierras entre contenedores (§2.6)**, escenarios y lista negra: `C:\Proyectos\frioseguro\hardware\ALCANCE_1WIRE.md` (@muestreador).
- **Costo real por equipo, con precios de MercadoLibre AR verificados el 2-sep-2026:** `C:\Proyectos\frioseguro\hardware\v1_modulos\BOM_KIT_V1.md` rev B (@hardware), §3.1, §3.3 y §3.4.
- Estado real y auditoría: `C:\Proyectos\frioseguro\entrega_scz\docs\ESTADO_HONESTO.md` · `AUDITORIA_HALLAZGOS.md`.
- **Qué hace hoy el firmware con sondas, puerta, relé y defrost (leído el 3-sep-2026):** `firmware_revival/sondas.h` (identificación por ROM, `sondasCalibrar`, **sin** verificación cruzada continua) · `firmware_revival/config.h` líneas 67-150 · `firmware_revival/firmware_revival.ino` líneas 369-375, 483-488, 804-944 · `firmware_revival/comandos_nube.h` (**sin** comando de relé).
- Contrato base: `MATI-HQ\comercial\CONTRATO_TERMOVIGIA_v4.md`.
- **Canalización (ML AR, 3-sep-2026):** caño galvanizado Daisa 3/4 liviano tira 3 m $ 11.637 — https://www.electricidadarevonline.com.ar/MLA-1439417798-cano-galvanizado-daisa-34-liviano-x-tira-de-3-metros-_JM · pesado $ 18.388 — https://electrodorrego.mercadoshops.com.ar/MLA-1116414163-cano-galvanizado-daisa-34-pesado-x-tira-de-3-metros-_JM · corrugado 3/4 pesado 25 m $ 13.500 — https://electrooestesanjusto.mercadoshops.com.ar/MLA-840435552-cano-corrugado-34-gris-pesado-losa-x-rollo-25mt-ha-ignifugo-_JM · UTP cat5e exterior 100 % cobre 100 m desde ~$ 40.000 — https://articulo.mercadolibre.com.ar/MLA-934596791-cable-utp-rollo-100mts-100-cobre-exterior-cat5e-4-pares-_JM
- 1-Wire: Maxim/Analog AN148 — https://www.analog.com/media/en/technical-documentation/tech-articles/guidelines-for-reliable-long-line-1wire-networks.pdf
- testo Saveris 2-T2 USD 318: https://www.ebay.com/itm/365602217221
- Novillo en pie $ 4.181/kg (INMAG jul-2026): https://www.consignatarias.com.ar/mercado
- Dólar BNA vendedor $ 1.535 (3-sep-2026): https://www.cronista.com/finanzas-mercados/dolar-oficial-asi-abre-la-cotizacion-este-jueves-3-de-septiembre/
- Supabase Pro USD 25/mes: https://www.nocode.mba/articles/supabase-pricing
- Código de Conducta de Proveedores de Pan American Silver (alcanza a subcontratistas): https://panamericansilver.com/wp-content/uploads/2023/02/Supplier-Code-of-Conduct-ES-LA.pdf

## Anexo — Lo que quedó abierto (para Matías, antes de mandar)

1. **Los números del Presupuesto 1:** equipo **USD 480 × 6 = 2.880** · repuestos **340** · puesta en marcha **1.700** · **inicial 4.920** · abono **250/mes** · B = **7.130**. Margen del equipo 29 %, del abono 47 %. ¿Van?
2. **Los números del Presupuesto 2:** módulo **USD 790 × 3 = 2.370** · canalización **180** · repuestos **420** · puesta en marcha **1.800** · **inicial 4.770** · abono **250/mes** · B = **7.000** · **corrección + USD 110 por par** si alguno no cumple. ¿Van?
3. **La diferencia entre los dos es de USD 150 (3 %).** Es el dato más importante de esta versión y está adelantado en el propio WhatsApp a Andrés para que no parezca que le empujamos el caro. ¿Se deja así?
4. **Condiciones de pago 50/50** (OC / equipos instalados y reportando): **cambia el criterio de la v2**, que facturaba la puesta en marcha por hitos (40/30/30). Ahora los hitos son compromiso de entrega, no facturas. **Confirmar.**
5. **Verificación cruzada entre sondas: hoy NO existe** (`sondas.h` calibra en un momento dado, no vigila deriva continua). Vendida en el **hito 2, vie 10-oct**, y aclarado en la página del cliente. Si no se puede cumplir, hay que sacar el punto 3 del bloque "por qué 4 sondas". **Decisión de Matías + confirmación de @firmware.**
6. **Accionamiento del relé desde el panel: tampoco existe** (no hay comando en `comandos_nube.h`). Vendido en el **hito 5, vie 19-dic**. La alerta local que dispara el relé sola sí anda hoy.
7. **El Presupuesto 2 necesita software que hoy no existe:** segunda puerta, segundo defrost y `SONDAS_MAX` a 8. Son las 12 h del §4.3. **Si @firmware dice que es más, el P2 sube de precio: confirmar antes de mandarlo.**
8. **El sensor de puerta viene deshabilitado por defecto** (`SENSOR_DOOR_ENABLED false`): que quede en la orden de armado habilitarlo y probarlo antes de despachar. Y la **segunda salida a relé se vende como "disponible", no como gobernada**: verificar que el pin esté asignado en la línea que va a Cerro Moro.
9. **Cobertura de red en los 6 reefers:** es el único riesgo nuevo que abre el Presupuesto 1 y depende de la respuesta de Andrés. Si algún reefer queda sin señal, hay que sumar un repetidor (barato, pero hay que saberlo antes de despachar).
10. **Andrés:** opción 1, 2 o 3 de la Parte 8, y preguntarle para quién trabaja. Y leer el WhatsApp §7.1 con el ojo de la última sección de la Parte 8: él pidió 3 módulos y le llegan dos presupuestos.
11. **PDF:** @diseno maqueta **dos** documentos de 2 páginas A4 cada uno, gemelos en formato, marca Termovigía, sin logo ajeno, sin "Para:", sin validez. Archivos `PRESUPUESTO_1_REEFERS_CERRO_MORO.pdf` y `PRESUPUESTO_2_REEFERS_CERRO_MORO.pdf`.
12. Monotributo vs. RI: se pregunta cuando la empresa tenga nombre.
13. **Stock:** el Presupuesto 1 son **7 equipos a armar** (6 + repuesto) y el BOM de @hardware está presupuestado para **5 kits**. El Presupuesto 2 son 4 módulos con 32 sondas. **Verificar compra y stock con @hardware antes de comprometer la fecha del hito 1 (vie 19-sep).**
