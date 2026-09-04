# PROPUESTA — Monitoreo de temperatura de los reefers del campamento Cerro Moro (Santa Cruz)

> @comercial · **v5.2, 2026-09-04** · **UN SOLO presupuesto: un equipo por reefer**
> **Cambio de precio de Matias (4-sep, v5.2):** el abono pasa a **USD 100 por reefer por mes = USD 500/mes por los 5** (mantenimiento de servidor, custodia de datos y seriedad del servicio) y **se elimina el escalon del 50 % de los primeros 3 meses**: el abono es completo desde el primer mes. Recalculadas A y B.
> **Correccion de Matias (4-sep):** los hitos van en **plazos relativos** (semanas desde la aceptacion), no en fechas de calendario; el WhatsApp a Andres **no le pide nada** (trabaja por turnos de 15 dias y no aprueba); y **no hay logistica hasta que acepten**.
> **Matías decide el número final, siempre.** Todo monto de acá abajo es propuesta con la cuenta a la vista.
> Doctrina: `PLATA.md`. Base técnica: `ALCANCE_1WIRE.md` (@muestreador), `hardware\v1_modulos\BOM_KIT_V1.md` (@hardware, rev B 2-sep), `entrega_scz\docs\ESTADO_HONESTO.md`, y el firmware `firmware_revival` leído el 3-sep.
> **El comprador NO es Pan American Silver:** es "una empresa" que Andrés todavía no identifica. El documento del cliente va **sin destinatario, sin logo ajeno y sin nombrar a Panamerican**. El archivo conserva el nombre por historial.

## Qué cambió en esta versión (dos cosas)

**1. Se cayó el Presupuesto 2.** La v4 llevaba dos presupuestos —uno por reefer y uno cada dos— porque faltaba el dato que decidía. **Andrés lo dio el 3-sep a las 23:33, textual:**

> *"Son aprox 20/25 metros, el problema es que hay que pasar los cables con caño Daisa"*

Con eso el escenario compartido **deja de existir como oferta**. Dos fundamentos, y **el que manda es el segundo** porque se dio vuelta respecto de la v4:

- **Técnico.** 20-25 m por par, con el bus saliendo hacia los dos lados desde el módulo del medio, es una **estrella** de 20-25 m de peso total con 8 sondas colgadas, contra el límite prudente de 15 m que fijó @muestreador. Y las masas de **dos contenedores metálicos con puesta a tierra separada** quedan atadas por el hilo de datos: `ALCANCE_1WIRE.md` §2.6 lo llama *"el riesgo dominante de esta instalación"*.
- **Económico — el vuelco.** La v4 presupuestaba la canalización en **USD 60 por par**, suponiendo tramos cortos con caño ya existente. Con caño rígido Daisa a 20-25 m, la cuenta rehecha con precios de hoy da **USD 161 de materiales y USD 286 con la mano de obra, por par**. Resultado: **compartir equipos sale USD 352 más caro**, y **sigue saliendo más caro (+USD 102) incluso regalando la mano de obra**. Cuenta completa con fuentes en **§3.3**, comparación en **§3.4**, registro de la decisión con la cita de Andrés en **§2.2**. **No se forzó la conclusión:** cada renglón dudoso se resolvió a favor del escenario compartido, y si hubiera dado al revés seguían los dos presupuestos.

**2. Son 5 reefers, no 6** (el sexto está fuera de servicio). Recalculado todo: **5 equipos + kit de repuestos = USD 4.540** y **abono USD 500/mes** (USD 100 por reefer). El equipo unitario pasa de 480 a **520**, porque los USD 1.000 de plataforma ahora se reparten entre 5 y no entre 6 (§3.1). **Y el documento del cliente deja escrita la puerta abierta:** cuando el sexto reefer vuelva a servicio se suma un equipo **al mismo precio unitario** y el abono pasa a 250 — así una limitación se convierte en una opción y no hay que renegociar después.

**El efecto colateral es que se destraba el pendiente de cantidades:** con 5 reefers el pedido son **6 equipos** (5 + el repuesto), y el `BOM_KIT_V1.md` de @hardware está calculado para 5 kits. Falta poco, está costeado renglón por renglón en **§3.10**, y **el hito 1 sigue siendo viable**: las duraciones de la v4 no se movieron, solo dejaron de estar atadas a fechas de calendario.

**Lo que no se movió:** producto por equipo, pago 50/50, formas A y B, los 5 hitos con sus duraciones y criterios de aceptación.

**Sigue eliminada la opción C** de la v2 ("sin inversión inicial", comodato con permanencia 24 meses), por decisión de Matías: *"el de la inversión inicial no lo ofrecería"*. Quedan **A** (equipos + servicio mensual) y **B** (anual adelantado).

---

## PARTE 1 — Documento del cliente (@diseno maqueta 2 páginas A4)

> Copiar de acá hasta la línea de corte. Nada más. Escrito para que **lo presente alguien que no es vendedor** y se lea en dos minutos.

**Termovigía — Monitoreo de temperatura de reefers**
**Campamento Cerro Moro (Santa Cruz) — 5 reefers en servicio**

**Qué es.** Un equipo sobre cada reefer, cinco en total, que vigila la temperatura las 24 horas y avisa al celular cuando algo se sale de rango. Cada equipo es independiente: **no hay un solo cable entre contenedores y ningún reefer depende del de al lado**. Hoy ya hay un equipo instalado y reportando desde el campamento: se puede ver en vivo en el celular antes de decidir nada. **Mientras se evalúa esta propuesta ese equipo sigue midiendo y reportando**, y el panel se puede abrir en cualquier momento: los resultados se muestran durante el proceso, no después.

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

**Qué se instala.** Cinco equipos, uno por reefer, cada uno en un gabinete apto para intemperie con su fuente, **4 sondas, sensor magnético de puerta, 2 salidas a relé y entrada de defrost**, más un kit de repuesto que queda en el campamento. El montaje lo hace personal del campamento con los equipos preconfigurados desde Bahía Blanca y guía por videollamada: por eso esta propuesta no tiene línea de instalación ni viáticos.

**Cada equipo se prueba individualmente antes de viajar.** Los equipos no salen de una línea de montaje: **se arman y se verifican uno por uno en banco de prueba** —las 4 sondas leyendo, la puerta, la señal de defrost y las dos salidas de alarma— y recién ahí se despachan. Para un lote que va a quedar a 1.500 km del proveedor, esa verificación unitaria es la diferencia entre un equipo que llega andando y uno que hay que diagnosticar por teléfono.

**Condiciones de instalación: ninguna.** Cada equipo se monta sobre su propio reefer y todo el cableado queda adentro de ese contenedor: **no hay cable entre reefers, ni canalización, ni obra, ni condición de distancia.** *Se evaluó también un equipo cada dos reefers: con los 20-25 metros que hay entre uno y otro habría que montar caño rígido en todo el recorrido, y esa obra cuesta más que los equipos que se ahorrarían — por eso la propuesta va con un equipo por reefer.*

**El sexto reefer.** Esta propuesta cubre los **5 reefers hoy en servicio**. Cuando el sexto vuelva a funcionar se le suma su equipo **al mismo precio unitario de esta propuesta (USD 520)**, con las mismas 4 sondas, puerta, salidas y defrost, y el servicio mensual pasa de USD 500 a USD 600: **+USD 520 el equipo y +USD 100/mes**. Queda dicho acá para no tener que renegociar nada el día que pase.

**Puesta en marcha y ajuste en sitio (15 semanas, por hitos).** Los hitos son compromiso de entrega con plazo; no se facturan aparte, están incluidos en el precio. **Los plazos se cuentan desde el inicio, y el inicio es la aceptación de esta propuesta con su anticipo.**

| Hito | Qué queda funcionando | Plazo |
|---|---|---|
| 1 | El equipo que ya está instalado, con sus 4 sondas dentro del reefer, calibradas contra una misma referencia, rangos definidos y primera alerta real recibida en el celular | a las 2 semanas de iniciado |
| 2 | Los 5 equipos montados y reportando; ningún dato ni aviso se pierde si se corta la red; aviso de equipo que deja de reportar; **aviso de sonda que se desvía de las otras tres**; puerta y defrost validados en campo; una semana entera sin falsas alarmas | a las 5 semanas |
| 3 | Acceso seguro: cada equipo y cada usuario con su propia credencial | a las 10 semanas |
| 4 | Actualizaciones de los equipos a distancia, sin tocarlos | a las 12 semanas |
| 5 | Panel para la empresa (usuarios de solo lectura), accionamiento de las salidas de alarma desde el panel e informe mensual descargable | a las 15 semanas |

**Qué cuesta.**

| Concepto | USD |
|---|---|
| Equipo de monitoreo por reefer (equipo, gabinete, fuente, 4 sondas, sensor de puerta, 2 salidas a relé, entrada de defrost, probado individualmente en banco) — 5 × 520 | 2.600 |
| Kit de repuestos en sitio (1 equipo completo armado y probado + 4 sondas + 1 sensor de puerta) | 340 |
| Puesta en marcha y ajuste en sitio, 5 hitos | 1.600 |
| **Total equipos y puesta en marcha** | **4.540** |
| **Servicio mensual** — **USD 100 por reefer por mes**, 5 reefers (nube, alertas, soporte, reposición sin cargo, informe mensual) | **500 / mes** |

**Cómo se paga.** **50 % con la orden de compra** (anticipo de materiales) y **50 % contra los equipos instalados y reportando**. El servicio mensual arranca con el primer equipo andando.

| | **A. Equipos + servicio mensual** | **B. Anual adelantado** |
|---|---|---|
| Para quién | Compra activos y paga el servicio mes a mes | Tiene presupuesto de inversión y no quiere 12 facturas |
| Equipos y puesta en marcha | USD 4.540 (50 % con la OC, 50 % contra instalación) | Incluidos |
| Pago inicial total | USD 4.540 | USD 9.940 (equipos + 12 meses de servicio, con 10 % de descuento sobre el servicio) |
| Mensual | USD 500 — USD 100 por reefer, completo desde el primer mes | — el primer año; renovación anual USD 5.400 |
| Los equipos | Son del cliente | Son del cliente |
| **Total a 12 meses** | **10.540** | **9.940** |
| **Total a 24 meses** | **16.540** | **15.340** |

Facturación en dólares estadounidenses. De abonarse en pesos, se toma el tipo de cambio vendedor del Banco de la Nación Argentina de la fecha de pago. *Referencia al 4-sep-2026 (BNA vendedor $ 1.535): USD 4.540 ≈ $ 6.968.900 · USD 500 ≈ $ 767.500 · USD 9.940 ≈ $ 15.257.900.*

**Incluido en el servicio mensual:** nube con 12 meses de historial · alertas por temperatura, puerta abierta, sonda caída y equipo mudo · reposición sin cargo de cualquier equipo o sonda fallada, envío incluido · actualizaciones · soporte por WhatsApp y teléfono el mismo día hábil · informe mensual por reefer.

**Lo que hay que saber.** El sistema avisa; no garantiza la mercadería ni reemplaza la revisión del reefer. Sin energía en el equipo no mide: lo que avisa en ese caso es la nube, diciendo que dejó de reportar. La entrada de defrost necesita que el reefer tenga una señal o un contacto accesible; si alguno no lo tiene, esa entrada queda libre y el resto funciona igual. Las 2 salidas a relé vienen en el equipo; la sirena o baliza que se conecte no está incluida. Cada equipo necesita llegar a la red del campamento desde su propio reefer. Los plazos de los hitos 1 y 2 suponen que el montaje en sitio se hace dentro de la ventana prevista, que depende de personal del campamento.

*Contacto en sitio: Andrés Leiva Chavez · Contacto comercial: Matías Alegre · Termovigía · Bahía Blanca · 2920 59-1019 · alegrematias08@gmail.com*

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
| **Los reefers en servicio son 5, no 6: el sexto está fuera de servicio** | Matías, 4-sep. Toda la propuesta se recalculó sobre 5 |

**La última fila cierra la contradicción de las dos anteriores y liquida el escenario compartido.** Registro completo de la decisión en §2.2, cuenta en §3.3.

### 2.2 Registro: por qué se descartó compartir equipos (decisión del 4-sep-2026)

> Esta sección existe para que Matías pueda defender la decisión si alguien pregunta por qué no se ofreció la variante con menos equipos.

**Qué se preguntó y cuándo.** El 3-sep se le mandó a Andrés la pregunta de la v4: por dónde iría el cable entre los dos reefers de cada par, si ya hay bandeja o caño hecho, y a cuántos metros están uno del otro.

**Qué contestó, textual (WhatsApp, 3-sep 23:33):** *"Son aprox 20/25 metros, el problema es que hay que pasar los cables con caño Daisa"*.

**Cómo se leyó esa respuesta, punto por punto.**

**1. "20/25 metros" mata el escenario técnicamente.** El límite prudente que fijó @muestreador para este bus es **15 m**, y acá hablamos de 20-25 m *por par*. Peor: con el módulo en el medio el bus sale hacia los dos lados, y eso es una **estrella no conmutada** — AN148 la desaconseja dos veces en el mismo párrafo y no da garantías a ninguna distancia, porque los rebotes recorren el **peso total** y no la rama más larga. Con 4 sondas por reefer el módulo compartido lleva **8 sondas**: bus largo **y** bus cargado, las dos cosas juntas (más sondas = más capacitancia = menor largo admisible). Y arriba de todo eso, el riesgo que no se puede probar desde Bahía: cada reefer es un **contenedor metálico con su propia puesta a tierra**, el cable de sondas ata esas dos masas por un hilo fino, y como **DQ se mide contra ese GND, la diferencia de potencial entra sumada al dato**. No la filtra el trenzado: no es modo común, es corriente real por el retorno. @muestreador lo llama textualmente *"el riesgo dominante de esta instalación"* (`ALCANCE_1WIRE.md` §2.6).

**2. "caño Daisa" mata el escenario económicamente, y es el argumento que manda.** Andrés no dijo "hay bandeja": dijo **caño rígido galvanizado**, y dijo que **hay que pasarlo**. Eso es obra: caño, cuplas, curvas, cajas de paso, grampas amuradas cada 1,5 m, y **un electricista montando 25 metros por cada par**. La v4 tenía ese renglón en **USD 60 por par**; la cuenta con los metros reales da **USD 161 de materiales y USD 286 con mano de obra, por par** (§3.3).

**3. La comparación, y el vuelco.** Con los 5 reefers en servicio, compartir sería **2 módulos dobles + 1 simple**: ahorra **USD 500** en equipos, pero exige **2 canalizaciones a USD 286 = USD 572**, un repuesto más caro (+80) y 12 h de software que no existe (+200). **Compartir termina saliendo USD 352 más caro** (§3.4). Y el detalle que hace la conclusión irrebatible: **incluso valorizando la mano de obra en cero** —o sea, si Andrés y su gente montan los 50 m de caño gratis— compartir sigue saliendo **USD 102 más caro**, solo con el material. Ésa es la única objeción que puede aparecer y ya está contestada.

**4. No se forzó la conclusión.** La cuenta se hizo con precios verificados el 4-sep y con **la hipótesis más favorable al escenario compartido en cada renglón dudoso**: caño liviano y no pesado (el pesado cuesta 58 % más), grampas a precio de pack y no de góndola, 22 m y no 25, y la mano de obra al **piso** del rango de tarifa. Si hubiera dado al revés, el Presupuesto 2 seguía en pie y se mandaban los dos, como en la v4.

**5. Lo que además se gana, y no estaba en la cuenta.** Sin equipos compartidos: no hay condición de metros en la propuesta, no hay cláusula de corrección de +USD 110 por par, no hay software que hoy no existe (segunda puerta, segundo defrost, `SONDAS_MAX` a 8), y si se apaga un equipo queda **un** reefer ciego en vez de dos.

> **Argumento que NO hay que usar, ni interno ni al cliente:** `SONDAS_MAX 4` (línea 31 de `firmware_revival/sondas.h`) **no es un límite de arquitectura** — es el tamaño de un arreglo, se cambia a 8 o a 16 en una línea, y el bus 1-Wire direcciona por ROM de 64 bits, así que admite decenas de sondas en un mismo pin. Las 4 sondas por reefer son **decisión de producto, ampliable**. El escenario compartido se cayó por los metros, las tierras y el caño; nunca por el firmware.

**La consecuencia comercial, y es buena: el argumento dejó de ser defensivo.** No estamos diciendo *"no se puede compartir"*: estamos diciendo **"les evitamos una obra y además sale menos"**. Ese es el tono de la línea que va en el documento del cliente y del WhatsApp de §6.1.

**Y lo que se le debe a Andrés:** la decisión salió de un dato que dio él. Hay que decírselo así — porque es cierto, y porque lo pone del lado correcto de la mesa.

### 2.3 Qué lleva cada equipo, y qué de eso anda HOY (verificado en el código el 3-sep)

| Función | Cant. | Qué hace el firmware hoy | Evidencia |
|---|---|---|---|
| Sondas DS18B20 | hasta 4 | Cada una identificada por ROM de 64 bits y reportada por separado; enganche en caliente; aviso si se desconecta; **offset de calibración por sonda en NVS** | `sondas.h`: `sondasEscanear`, `sondasLeer`, `sondasCalibrar` |
| **Verificación cruzada entre sondas** | — | **NO existe.** `sondasCalibrar()` iguala las sondas en un momento dado, pero el lazo de lectura **no compara sondas entre sí** ni alerta por deriva | ídem. Vendida en el **hito 2**, con la aclaración escrita en la página del cliente |
| Sensor magnético de puerta | 1 | Implementado: GPIO5, alerta por puerta abierta más de 180 s (configurable) y **suprime la alerta de temperatura mientras está abierta**. Viene **deshabilitado por defecto** (`SENSOR_DOOR_ENABLED false`) | `config.h` 72-74, 105, 119 · `.ino` 804-890 |
| Salidas a relé | 2 | **1 gobernada**: GPIO26, se activa sola con la alerta si `relayEnabled`. La segunda queda cableada y disponible. **El accionamiento manual desde el panel NO existe** | `config.h` 76-77, 140-150 · `.ino` 369-375, 483-488, 915-944 · `comandos_nube.h` sin comando de relé → **hito 5** |
| Entrada de defrost | 1 | Implementada: GPIO33, contacto NA o NC configurable; durante el ciclo **deshabilita todas las alertas**, con 30 min de enfriamiento configurable | `config.h` 91-96, 122 · `.ino` 54-55, 100-101, 872-878 |

**Regla de venta:** lo único que **no** está andando hoy es la **verificación cruzada entre sondas** y el **accionamiento manual del relé desde el panel**; los dos van en hitos con fecha, no como característica de hoy.

> **Beneficio colateral de haber descartado el escenario compartido, y no es menor:** desaparecen las 12 h de software que hoy no existe (segunda puerta, segundo defrost, `SONDAS_MAX` a 8) y desaparece el riesgo de que @firmware dijera que eran más y hubiera que recotizar. **Lo que se vende ahora es exactamente lo que el firmware ya hace, con dos excepciones fechadas.**

**Orden de armado:** línea `entrega_scz`/`firmware_revival` (identificación por ROM), **no** `firmware_modular` (lee por índice: si cae una sonda, la otra se reporta con el nombre equivocado). Pull-up **2k2**, 3 hilos (nada de parasite power), 100 nF + 10 µF al pie de la sonda más lejana. **Habilitar `SENSOR_DOOR_ENABLED` y probar la puerta antes de despachar.**

### 2.4 Lo que se instala, y quién

Por equipo: gabinete estanco IP65 165×165×80, fuente de 5 V 2 A, plaqueta de conexiones con borneras a tornillo, ESP32 en zócalo, módulo de 2 relés, prensacables, **4 sondas DS18B20 estancas con 3 m de cable**, reed de puerta. **Montaje: Andrés (o quien la empresa designe), con kit preconfigurado y probado en banco + videollamada.** Dos pasajes a Santa Cruz, alojamiento, inducción y 5 días de ingeniero rondan los $ 2.500.000, y Matías no puede viajar en octubre (parada de Dreyfus). Eso es lo que esta propuesta no cobra.

### 2.5 El único riesgo técnico que queda abierto

Con un equipo por reefer hacen falta **5 puntos con cobertura de la red del campamento, no 3**. Si algún reefer queda sin señal se resuelve con un repetidor —material barato— pero **hay que saberlo antes de despachar**, no después. Es la pregunta 1 de §5.2 y no frena el envío de la propuesta.

### 2.6 Opcionales, después de la primera orden

**El sexto reefer cuando vuelva a servicio: USD 520 el equipo + USD 100/mes** — ya está escrito con precio en el documento del cliente, así que no hay que venderlo de nuevo, solo ejecutarlo. **Es el upsell más probable y el de mejor margen de esta cuenta**, porque la plataforma ya está paga y el costo de sitio del abono ya está cubierto por los otros cinco. · Sirena o baliza física para conectar a la salida de relé (USD 40; el relé ya está incluido) · sonda **quinta o siguiente** en un reefer (USD 40 + USD 5/mes) · base con batería y 4G, la única que avisa el corte de energía por sí misma (a cotizar). Se ofrecen cuando las sondas estén andando, no antes.

---

## PARTE 3 — Números de respaldo

Todo lo de abajo sale del BOM real (`BOM_KIT_V1.md` rev B de @hardware, precios de MercadoLibre AR verificados el 2-sep-2026, §3.4 "Costo real por equipo", **a precio de reposición**), no de prorratear la v2. Cambio $ → USD al BNA vendedor 1.535 del 3-sep.

### 3.1 El equipo por reefer, USD 520

| | ARS | USD |
|---|---:|---:|
| Materiales sin sondas ni reed: compra nueva §3.1 del BOM ÷ 5 = 35.674 + ESP32 13.990 + **1** módulo de 2 relés 5.028 + fuente 5 V 2 A 7.980 + caja IP65 8.500 | 71.172 | **46** |
| 4 sondas DS18B20 estancas rearmadas con 3 m de cable y prensacable (la sumergible de plaza viene con 1 m) | ~36.800 | **24** |
| 1 sensor magnético de puerta cableado, con carcasa | 4.746 | **4** |
| Envío a Santa Cruz, prorrateado por equipo | ~12.300 | **8** |
| Armado (1,5 h) + **prueba de banco individual documentada con las 4 sondas, la puerta, el defrost y las dos salidas** (1 h) + garantía de reposición amortizada | | **90** |
| Parte de plataforma del desarrollo: USD 1.000 repartidos en **5** equipos | | **200** |
| Margen | | **148** |
| **Precio** | | **520** |

**De dónde salen los USD 40 de diferencia con la v4 (480 → 520): de un solo renglón.** Los USD 1.000 de plataforma —los mismos de siempre, no un cargo nuevo— antes se repartían entre 6 equipos (167 c/u) y ahora entre 5 (200 c/u). Todo lo demás está igual. Margen **28,5 %**, el mismo criterio de la v4.

**Si Matías prefiere sostener el número redondo de 480**, se puede: el margen baja de 28,5 % a **23 %** y la plataforma recupera 833 en vez de 1.000. **Recomiendo 520**, por dos razones: el precio **nunca se le comunicó a nadie todavía** (el WhatsApp de la v4 no se mandó, así que no hay ningún número previo que defender), y **la línea del sexto reefer convierte esos 520 en el precio de referencia de la ampliación** — cada equipo que se sume después entra a 520 con la plataforma ya paga, que es margen limpio.

**Dato de venta, sigue valiendo:** la v2 cotizaba **USD 500 el módulo de un solo reefer** con 2 sondas, sin puerta, sin relés y sin defrost. Acá son **520 con 4 sondas, puerta, 2 relés y defrost**, y probado unidad por unidad.

### 3.2 Puesta en marcha, USD 1.600

| Trabajo | h |
|---|---:|
| Sondas, rangos y umbrales por reefer + **calibración de las 20 sondas** contra referencia y registro de offsets | 14 |
| Registro exportable con código de verificación | 16 |
| Panel multi-equipo y usuarios de lectura | 12 |
| Puesta en marcha remota (alta, credencial, OTA verificada, prueba de puerta y defrost), pruebas de campo con Andrés, runbook y capacitación — 5 equipos | 18 |
| Salud de bus, histéresis de 3 barridos y **verificación cruzada entre sondas** | 4 |
| **Total a USD 25/h** | **64 = USD 1.600** |

*Bajó de 1.700 a 1.600 respecto de la v4 por las 20 sondas en lugar de 24 y un equipo menos que dar de alta. **No** bajó por el escenario descartado: ahí la puesta en marcha era más cara, no más barata (§3.4).*

### 3.3 **LA CUENTA DEL CAÑO** — por qué compartir equipos salía más caro

> Esta sección existe por pedido explícito de Matías: que el número se pueda defender si se lo preguntan. Precios de MercadoLibre AR y listas públicas **verificados el 4-sep-2026**; enlaces en el anexo de fuentes.

**El supuesto, deliberadamente favorable al escenario compartido.** Andrés dijo "20/25 metros": tomo **22 m** (el extremo bajo del rango) y le sumo **3 m** de subidas, bajadas y entradas a los dos reefers → **25 m de recorrido por par**. Caño **liviano** y no pesado (el pesado cuesta 58 % más). Grampas a precio de pack y no de góndola. Mano de obra al **piso** del rango de tarifa. Si el metraje real fuera el otro extremo, todo esto sube ~15 %.

**Materiales, por par de reefers:**

| Ítem | Cant. | Precio unitario | Subtotal |
|---|---:|---:|---:|
| Caño galvanizado Daisa 3/4 **liviano**, tira de 3 m | 9 tiras (27 m, con recorte) | $ 11.637 | **$ 104.733** |
| Cuplas de unión 3/4 | 8 | ~$ 1.500 | $ 12.000 |
| Curvas / codos 3/4 (salidas, entradas, esquivos) | 6 | ~$ 4.000 | $ 24.000 |
| Cajas de paso estancas (cambios de dirección y tramos > 12 m) | 4 | ~$ 12.000 | $ 48.000 |
| Conectores caño-caja (tuerca + boquilla) | 10 | ~$ 1.200 | $ 12.000 |
| Grampas omega 3/4, **una cada 1,5 m** | 18 | ~$ 1.500 (pack) · **$ 3.977 de góndola** | $ 27.000 |
| Tarugos y tornillos para 18 grampas | — | — | $ 8.000 |
| Cable UTP cat5e exterior 100 % cobre | 30 m | $ 400/m | $ 12.000 |
| **Materiales por par** | | | **≈ $ 247.700 ≈ USD 161** |

*Con las grampas compradas por unidad en vez de por pack, sube a ≈ $ 292.300 (USD 190) por par.*

**Mano de obra — y esto no se regala aunque lo haga Andrés.** Montar **25 m de caño rígido** por par son: 18 grampas amuradas con tarugo sobre estructura, 4 cajas de paso, 6 curvas, todas las uniones roscadas, más el pasado del cable y el conexionado en los dos extremos. Rendimiento razonable de un oficial electricista en caño rígido a la vista: **12-18 m por jornada**. A 15 m/jornada son **~1,7 jornadas de montaje + 0,3 de pasado de cable ≈ 2 jornadas (16 h) por par**.

| Tarifa de oficial electricista (valores AAIERIC vigentes 2026, CABA/GBA) | $/h | 16 h |
|---|---:|---:|
| **Piso del rango (el que se usa)** | 12.000 | **$ 192.000 ≈ USD 125** |
| Techo del rango | 25.000 | $ 400.000 ≈ USD 261 |

Se usa **el piso**, y encima es un piso optimista: Santa Cruz y un campamento minero pagan **más** que CABA, no menos.

| Canalización, por par | ARS | USD |
|---|---:|---:|
| Materiales | 247.700 | **161** |
| Mano de obra, 2 jornadas al piso de tarifa | 192.000 | **125** |
| **Total por par** | **439.700** | **286** |

**Cotizado en la v4: USD 60 por par. La diferencia es 4,8×.** El motivo hay que decirlo sin vueltas: **la v4 supuso tramos cortos con canalización existente, y Andrés informó 20-25 m de caño rígido a montar.** No fue un error de cálculo, fue un supuesto — y el dato que lo corrigió lo dio él.

### 3.4 La comparación final: compartir vs. no compartir, con 5 reefers

Con 5 reefers en servicio, el escenario compartido sería **2 módulos dobles + 1 equipo simple = 3 equipos y 2 canalizaciones**.

| | **Un equipo por reefer (5)** | **Compartido (2 dobles + 1 simple)** | Diferencia |
|---|---:|---:|---|
| Equipos | 5 × 520 = **2.600** | 2 × 790 + 520 = **2.100** | −500 |
| Canalización (§3.3) — 2 pares × 286 | **0** | **572** | +572 |
| Repuestos | 340 | 420 | +80 |
| Puesta en marcha | 1.600 | 1.800 | +200 |
| **Inicial** | **4.540** | **4.892** | **+352** |
| Abono | 500/mes | 500/mes | igual |
| Sondas en servicio | 20 | 20 | igual |
| Cable entre contenedores | 0 m | ~50 m en caño rígido | — |
| Obra en el sitio | ninguna | 2 canalizaciones | — |
| Condiciones en la propuesta | ninguna | contiguos, metros, canalizado | — |
| Reefers ciegos si falla un equipo | 1 | 2 | — |

**Tres lecturas, en orden de fuerza:**

1. **Compartir sale USD 352 más caro.** No es "más barato con condiciones": es directamente más caro.
2. **Y sale más caro aun regalando la mano de obra.** Solo con materiales: 2.100 + 322 + 420 + 1.800 = **USD 4.642**, todavía **USD 102 arriba** de 4.540. Ni *"el caño lo montamos nosotros"* lo salva — y ésa es la única objeción que puede aparecer.
3. **Con las grampas de góndola y la mano de obra al techo del rango**, el compartido llega a **USD 5.222: USD 682 más caro.** Sirve para saber que **no hay variante de la cuenta que dé vuelta la conclusión.**

**Por qué la puesta en marcha del compartido cuesta MÁS (renglón contraintuitivo, conviene tenerlo a mano):** tiene 3 equipos en vez de 5, lo que ahorra 4 h de alta remota; pero **las 20 sondas hay que calibrarlas igual**, y arriba hay **12 h de software que hoy no existe** — segunda puerta, segundo defrost, `SONDAS_MAX` a 8 y validación del bus compartido en sitio. Neto: 72 h contra 64.

**Contra qué se comparaba en la v4:** ahí la diferencia daba **a favor** de compartir, con la canalización en USD 60 por par y la mano de obra sin valorizar. **Ese renglón era el error, y el dato de Andrés lo corrigió.**

### 3.5 Servicio mensual: qué cuesta servir y qué se cobra

| Costo directo mensual | v2 (12 sondas) | **v5 (20 sondas, 5 reed)** |
|---|---:|---:|
| Supabase Pro | 25 | 25 |
| Reposición amortizada (equipos y sondas en garantía) | 10 | **18** |
| Soporte (2 h → 2,3 h a USD 25) | 50 | **57** |
| Informe mensual | 25 | 25 |
| **Total** | **110** | **125** |

**Tarifa: USD 100 por reefer por mes × 5 = USD 500/mes** (decisión de Matías, 4-sep). Costo directo 125 → **margen bruto USD 375 (75 %)**. La justificación, y es la que hay que decir si preguntan: **mantenimiento del servidor, custodia de los datos y seriedad del servicio** — el registro que se entrega tiene que estar disponible y ser defendible dentro de un año, y eso se paga todos los meses aunque no pase nada. Sube de 20 (v2, 2 sondas por reefer) a 100 por reefer, con **4 sondas + puerta + 2 salidas + defrost por reefer**: **USD 25 por sonda y por mes**.

El abono ahora es **estrictamente proporcional a los reefers**: 5 reefers = 500, 6 = 600. **Cuando entre el sexto reefer, los USD 100 adicionales son casi margen puro** (el costo directo apenas se mueve: Supabase, informe y la mayor parte del soporte son por cliente, no por reefer) — es el mejor upsell que tiene esta cuenta y ya está escrito en el documento del cliente.

**El escalón de los primeros 3 meses al 50 % se eliminó** (decisión de Matías, 4-sep): el abono se cobra completo desde el primer mes en las dos formas. Lo que justifica cobrarlo desde el día uno es que el servicio ya está corriendo —servidor, custodia de datos y guardia de alertas— desde el primer equipo que reporta.

### 3.6 Condiciones de pago — 50 / 50, y por qué no 25

**Decisión del Director: 50 % con la orden de compra (anticipo de materiales) y 50 % contra los equipos instalados y reportando.** El abono arranca con el primer equipo andando.

El fundamento es de caja: hay que comprar y armar **6 equipos** (5 + el repuesto) antes de ver un peso del segundo tramo, y cobrar ese tramo a 60 días a un contratista que todavía no tiene nombre. Con el 50 % (**USD 2.270 ≈ $ 3.484.450**) la compra completa de materiales —**≈ $ 436.000 con flete, ver §3.10**— queda cubierta **más de ocho veces** antes de tocar un componente, y sobra para el envío a Santa Cruz y para las horas de Gonza y Sergio. Con el 25 % también alcanzaría para los materiales; lo que no cubriría es el **riesgo de cobranza del segundo tramo**, que es lo que en realidad se está financiando.

**Qué cambia respecto de la v2:** desaparece el esquema de facturar la puesta en marcha por hitos (40/30/30). Los hitos siguen existiendo **como compromiso de entrega con plazo**, y así está escrito en el documento del cliente: *"los hitos no se facturan aparte, están incluidos en el precio"*. **Punto para que Matías confirme:** cobrar antes de entregar los hitos es más cómodo para la caja y más exigente con la palabra.

### 3.7 Las dos formas de pagar, y por qué se cayó la tercera

**A. Equipos + servicio mensual.** 4.540 + 12 × 500 = **10.540** el primer año; 6.000/año después; **24 meses 16.540**.

**B. Anual adelantado, 10 % de descuento sobre el año de servicio.** 4.540 + (12 × 500) × 0,9 = 4.540 + 5.400 = **USD 9.940**; renovación 5.400/año; **24 meses 15.340**. El descuento le ahorra **USD 600 el primer año** y lo que compra es concreto — **cero riesgo de cobranza durante 12 meses con un contratista que probablemente pague a 60-90 días, una factura en lugar de doce, y caja para armar los equipos.**

**C, eliminada.** Matías: *"el de la inversión inicial no lo ofrecería"*. Coincide con el párrafo de riesgo que la propia v2 tenía escrito: era la única que ponía USD ~4.500 nuestros en manos de un contratista a 1.500 km, sin poder retirar los equipos, recuperables recién cerca del mes 20, y la única que no existía sin contrato firmado con permanencia. **No se vuelve a ofrecer sin contrato validado por contador y un cliente con historial de pago.** Con dos opciones el comprador elige; con tres se paraliza.

> **Revisión hecha al quedar un solo presupuesto y 5 reefers:** los 5 hitos **con sus duraciones originales**, el 50/50 y las formas A y B **siguen teniendo sentido tal cual**. Se cayó por arrastre **la cláusula de corrección de "+ USD 110 por par"**, que existía solo para el escenario compartido: sin pares, no hay nada que corregir, y **la propuesta queda sin una sola cláusula condicional.** Eso también es un argumento de venta. Y se agregó **una sola línea nueva**, la del sexto reefer, que es lo contrario de una condición: es una opción con precio ya puesto.

### 3.8 Moneda, validez, facturación

**Facturación en USD, pago en pesos al BNA vendedor de la fecha de pago, sin validez en el PDF.** Nota interna: revisar precios si pasan más de 6 meses desde el 4-sep. Antes de la cotización firme hay que saber: monotributo vs. RI, plazo de pago, si acepta la cláusula de moneda, quién firma. Se pregunta cuando la empresa tenga nombre.

### 3.9 Contra una pérdida y contra la competencia

Una pérdida de 3 t valuada al precio de novillo en pie ($ 4.181/kg, INMAG jul-2026) son $ 12,5 M: **16 meses de servicio** al abono de USD 500 (≈ $ 767.500 por mes). testo Saveris 2-T2: USD 318 por unidad y mide **un** punto; para cubrir los 20 puntos de esta propuesta harían falta 20 unidades = **USD 6.360** antes de importación, sin nube, sin puerta, sin relé, sin defrost, sin repuesto en sitio — y se configura con una red WiFi y una clave, que es exactamente lo que este sitio no tiene.


### 3.10 **Los 6 equipos: qué falta comprar, cuánto sale y por qué el hito 1 sí da**

> Este era el pendiente 13 de la v4 ("verificar stock con @hardware antes de comprometer el hito 1"). Queda resuelto acá — y **con 5 reefers en vez de 6 el problema prácticamente desaparece**.

**Qué hace falta.** 6 equipos: **5 instalados + 1 de repuesto en sitio**, cada uno con 4 sondas y 1 reed. Total: **6 ESP32 · 6 fuentes · 6 cajas · 6 módulos de relé · 24 sondas** (20 instaladas + 4 de repuesto) **· 6 reed**. El `BOM_KIT_V1.md` rev B de @hardware está calculado para **5 kits de 3 sondas y 3 puertas cada uno**: es casi la misma cantidad de equipos, pero **otro reparto de sondas y puertas**, así que el pedido se recalcula renglón por renglón y no se escala a ojo.

**Cruce contra el stock declarado** (`BOM_KIT_V1.md` §1, tomando siempre **el número más bajo** de cada rango, y sin olvidar que **@hardware necesita 3 ESP32 para las galgas de Dreyfus**, que es P0 de octubre):

| Ítem | Hacen falta | Stock declarado | Faltan | Precio | **A comprar** |
|---|---:|---:|---:|---:|---:|
| ESP32 DevKit | 6 + 3 (galgas) = **9** | 4 (los 5 de la tabla menos el que está en Cerro Moro) | **5** | $ 13.990 c/u | **$ 69.950** |
| Sondas DS18B20 | **24** | 15 | **9** | $ 4.388 c/u | **$ 39.492** |
| Cajas IP65 165×165×80 | 6 | 3 | **3** (2 packs ×2, sobra 1) | $ 17.000 el pack | **$ 34.000** |
| Fuentes 5 V **2 A** | 6 | 5, **amperaje sin verificar** | **6** (peor caso) | $ 7.980 c/u | **$ 47.880** |
| Módulos de relé 2 canales | 6 | 10 módulos | 0 | — | **$ 0** |
| Reed / sensor de puerta | 6 | 10 | 0 | — | **$ 0** |
| Consumibles del §3.1 del BOM **reescalados a 6 equipos con 4 sondas + 1 puerta** (plaquetas PE04 ×6, borneras 4 packs, tiras hembra 3 packs, R 4k7 y 10 k, 100 nF, electrolíticos, kit de separadores, prensacables 4 packs) | — | — | — | — | **$ 172.874** |
| Cable de 3 hilos para rearmar las 24 sondas a 3 m (≈85 m) + termocontraíble | — | — | — | — | **$ 52.000** |
| **TOTAL** | | | | | **≈ $ 416.200** |

Con flete y diferencias de vendedor: **≈ $ 436.000 ≈ USD 284**. Si las 5 fuentes resultan ser de 2 A, baja a **≈ $ 396.000 (USD 258)**; si los módulos de relé eran 5 y no 10, sube $ 5.028.

**Contra el anticipo del 50 % (USD 2.270 ≈ $ 3.484.450), la compra completa es el 12,5 %.** No hay problema de plata ni de cantidades.

**Por qué el hito 1 SÍ es alcanzable, y qué lo asegura.** El hito 1 es *"el equipo que ya está instalado, con sus 4 sondas dentro del reefer, calibradas, rangos definidos y primera alerta real"*. **No depende de que lleguen los 5 equipos nuevos: depende de que lleguen 3 sondas.** El equipo `REEFER_01_SCZ` ya está montado y reportando desde el 21-ago; hoy tiene **1 sola sonda y está fuera del reefer**.

**El plan arranca cuando aceptan, no antes.** Semana 0 = aceptación de la propuesta + anticipo del 50 %. Hasta que eso pase **no se compra, no se arma y no se despacha nada**, y a Andrés no se le pide que reserve ninguna ventana: trabaja por turnos de 15 días y no es él quien aprueba.

| Paso | Plazo desde la aceptación | Quién |
|---|---|---|
| Conteo del stock real + las 2 mediciones del §8.1 del BOM (amperaje de las fuentes, relé con IN al aire) | semana 0 | Gonza |
| Compra del faltante y rearmado de sondas a 3 m | semana 0-1 | Gonza / Matías |
| Despacho de 3 sondas para el equipo ya instalado (encomienda, 5-8 días hábiles) | semana 1 | — |
| Alta, calibración remota, rangos y primera alerta real | semana 2 | Andrés + Matías |
| **HITO 1** | **semana 2** | — |
| Armado de los 6 equipos + **prueba de banco individual** (~20 h) | semana 1-2 | Gonza / Sergio |
| Despacho de los 5 bultos (4 equipos + repuesto) a Cerro Moro | semana 2 | — |
| Montaje de los 4 equipos restantes por personal del campamento | semana 3-4 | campamento |
| Alta y calibración de las 16 sondas nuevas | semana 4 | Matías |
| **HITO 2** (los 5 reportando + una semana sin falsas alarmas) | **semana 5** | — |

**El riesgo que hay que decir en voz alta: el hito 2 está apretado.** La semana sin falsas alarmas arranca recién cuando los 5 equipos reportan —alrededor de la semana 4— y el hito vence en la 5: **es exactamente una semana, sin colchón**. Si la encomienda a Santa Cruz tarda más de 8 días hábiles o el montaje se corre, el hito 2 se corre con él. **Está dicho así en el documento del cliente**, que aclara que los plazos de los hitos 1 y 2 dependen de la ventana de montaje del campamento.

**Por qué se puede empezar a armar antes de la orden de compra, sin exponer un peso nuevo.** Los 6 kits **ya estaban planificados como las unidades de demostración del plan comercial de Bahía** (5 equipos para laboratorio, farmacia, carnicería, distribuidora y restaurante). Si Cerro Moro no compra, **los equipos no quedan colgados: van a su destino original**. O sea que adelantar el armado **no crea inventario nuevo, solo lo anticipa** — y por eso las fechas de los hitos no tienen que colgar de la firma del cliente.

> **La contracara, y hay que ponerla sobre la mesa del Director:** si Cerro Moro **sí** compra, **Bahía se queda sin sus 5 equipos de demo** y el plan comercial local queda parado hasta reponerlos. La segunda tanda son otros **≈ $ 400.000** y **10 días** entre compra y armado. **Recomendación: en cuanto llegue la orden de compra, se dispara la reposición de los 5 kits de Bahía en el mismo pedido**, no después — el anticipo del 50 % la paga sin despeinarse y evita que un cliente bueno mate el pipeline del otro.

---

## PARTE 4 — Puesta en marcha: qué es cada hito por dentro

Es el plan de endurecimiento de la auditoría del 26-ago, con nombre de cliente. **Las duraciones son las mismas de la v4; lo que cambió es que se cuentan en semanas desde la aceptación y no contra el calendario** — el detalle de por qué cierran, paso por paso, está en §3.10. Los hitos pesados caen después de la semana 5 para no chocar con la parada de Dreyfus, sea cuando sea que arranque.

| Hito (cliente) | Etapa interna | Desde | Hasta | Cómo se acepta |
|---|---|---|---|---|
| 1 — El equipo ya instalado con sus 4 sondas adentro y calibradas, rangos, primera alerta real | E0 | semana 0 | **semana 2** | Captura de la alerta en el celular + registro en nube + **planilla de calibración con el offset de las 4 sondas de `REEFER_01_SCZ`** |
| 2 — Los 5 equipos reportando; nada se pierde, nada sobra | E1: buffer offline, alertas encoladas, alerta de sonda caída que llega, vigía de equipo mudo, discriminador de bus + histéresis, **detección de sonda que se desvía de las otras del mismo reefer**, habilitación y prueba de puerta y defrost | semana 2 | **semana 5** | Los 5 montados y reportando con sus 20 sondas calibradas; desenchufar una sonda y que llegue la alarma; cortar la red 20 min sin perder lecturas; abrir una puerta 4 min y que avise; forzar un defrost y que **no** avise; **una semana sin falsas alarmas** |
| 3 — Acceso seguro | E2: RLS cerrada, credencial por equipo, secretos fuera del binario, revocar claves quemadas | semana 5 | **semana 10** | Con la clave vieja no se escribe; todos los equipos siguen reportando |
| 4 — Actualización a distancia | E3: OTA con manifiesto inmutable | semana 10 | **semana 12** | Tres actualizaciones seguidas por aire al primer intento, en todos los equipos |
| 5 — Panel e informe | E4: usuarios de lectura, vista de los 5 reefers, exportación con código, informe mensual automático, **comando de relé desde el panel** | semana 12 | **semana 15** | Un usuario de la empresa entra solo, baja el informe y acciona una salida desde el panel |

**El hito 2 es el apretado, no el 1** (§3.10): la semana sin falsas alarmas arranca recién cuando los 5 equipos reportan, alrededor de la semana 4, y vence en la 5. **Sin colchón.** Depende de la encomienda a Santa Cruz y de la ventana de montaje que defina el campamento cuando el trabajo esté aceptado.

Lo que hoy está roto y cada hito arregla (llave maestra en el binario, datos perdidos sin red, umbral en 50 °C, equipo muerto que no avisa, OTA que entra 1 de 4) está en `AUDITORIA_HALLAZGOS.md`; no cambió.

---

## PARTE 5 — Qué necesitamos para cerrar

### 5.1 De la empresa, cuando tenga nombre

Quién firma, cómo factura (monotributo/RI, plazo), si acepta la cláusula de moneda, **cuál de las dos formas de pago elige (A o B)**, y confirmación de que el montaje lo hace personal del campamento (sin personal nuestro en sitio no corresponde ART ni legajo de contratista).

### 5.2 De Andrés: lo que sigue abierto

**Las tres preguntas sobre el cable ya están contestadas** (3-sep 23:33) y por eso hay un solo presupuesto — registro en §2.2. Quedan dos, y **ninguna frena el envío**:

1. **¿La red del campamento llega bien a los cinco reefers?** Es el único riesgo técnico nuevo del escenario elegido: hacen falta 5 puntos con señal, no 3. Si alguno queda corto se resuelve con un repetidor barato, pero hay que saberlo **antes de despachar** — o sea, después de la aceptación, no ahora.
2. **¿Los reefers tienen una señal o contacto de defrost accesible?** Si alguno no lo tiene, esa entrada queda libre y el resto funciona igual — ya está dicho así en el documento del cliente, sin letra chica.

Y una tercera que no es técnica y decide la Parte 7: **¿para quién trabaja Andrés?** (empleado de PAAS o de una contratista).

---

## PARTE 6 — Para Andrés (aparte del PDF)

### 6.1 WhatsApp — respuesta a su mensaje del 3-sep 23:33 (lo manda Matías)

```
Andrés, gracias por el dato de los metros, en serio: con eso me quedó
resuelto y te termino mandando un solo presupuesto en vez de dos.

Saqué la cuenta del caño: por cada par de reefers son unas 9 tiras, más
curvas, cajas de paso y una grampa cada metro y medio, y encima dos
jornadas de electricista para montarlo. Compartir un equipo entre dos
reefers ahorra unos 500 dólares, pero el caño con la mano de obra son
unos 570: termina saliendo más caro que poner uno en cada reefer, y
aunque el caño lo montaran ustedes sin cobrar la mano de obra tampoco
cierra.

Por eso va uno por reefer: ni un cable entre contenedores, ni caño, ni
obra, ni condiciones de distancia. Lo armé por los 5 que están andando;
cuando el sexto vuelva le sumamos el suyo al mismo precio, ya está
escrito en el presupuesto.

Te paso el presupuesto: dos hojas, sin nombre de empresa, para que se lo
pases a quien corresponda. El equipo que ya está puesto sigue reportando,
así que mientras lo miran se puede ver el panel en cualquier momento.
```

> **Por qué está escrito así, para que no se suavice de más al copiarlo:**
> **(a)** Arranca **agradeciendo el dato y atribuyéndole la decisión a él** — es cierto, y lo pone del lado correcto de la mesa: él pidió tres módulos y le llega uno por reefer, así que lo único que evita que eso se lea como *"tu idea no servía"* es que quede claro que **la cuenta la cambió su información**.
> **(b)** Da **la cuenta completa en dos párrafos de criollo**, sin tabla y sin tecnicismo: tiras de caño, grampas, jornadas de electricista. Números redondos y verificables.
> **(c)** Incluye la línea del *"aunque lo monten ustedes gratis tampoco cierra"*, que desactiva la única objeción posible.
> **(d)** **El sexto reefer se nombra como una puerta abierta, no como un recorte:** "cuando vuelva le sumamos el suyo al mismo precio". Además demuestra que estamos mirando el sitio de verdad y no vendiendo un paquete cerrado.
> **(e)** **Cierra en "te paso el presupuesto"**, no en la explicación ni en una cifra suelta: el número vive en el PDF, que es donde se puede leer entero y pasar a quien decide. Y el tono es **"les evitamos una obra"**, nunca *"no se puede"*.
> **(f)** **No le pide nada.** Andrés trabaja por turnos de 15 días y **no es él quien aprueba**: pedirle que reserve una ventana de montaje o que espere una encomienda lo pone a administrar algo que no decide. El mensaje cierra en *"te paso el presupuesto"*; la logística arranca cuando haya aceptación y anticipo, no antes. Lo único que se le ofrece es lo que ya está pasando: el equipo instalado sigue reportando y el panel se puede mirar en cualquier momento.
> **(g)** No pide disculpas por haber cotizado antes USD 60 de canalización por par: el supuesto cambió porque llegó un dato mejor, que es exactamente como tiene que funcionar.

### 6.2 Guion de 5 líneas para que la presente él

1. **Arrancá por el problema, no por el producto:** "un reefer que se corta un fin de semana es la comida de todo el campamento, y hoy nadie se entera hasta que abren la puerta."
2. **Mostrá lo que ya anda:** abrí el panel en el celular y mostrá la temperatura de ahora del equipo instalado — sigue reportando mientras la propuesta se evalúa. Si podés, sacá una sonda al aire un minuto y que vean subir la curva. Eso convence más que el PDF.
3. **Decilo en una frase:** "cuatro sondas adentro de cada reefer, te avisa al celular si se sale de rango o si queda la puerta abierta, y arma el registro mensual solo."
4. **Si preguntan por qué un equipo por reefer y no uno cada dos:** "porque entre reefer y reefer hay 20 metros y habría que pasar caño; el caño con la mano de obra sale más que los equipos que se ahorrarían. Sale menos así, y no hay que abrir ninguna obra acá adentro."
5. **Lo que NO prometés:** que garantiza la mercadería (avisa, no garantiza) · que avisa el corte de luz (avisa que el equipo dejó de reportar) · que la sirena está incluida (van las salidas, la sirena se conecta) · que está terminado (hay una puesta en marcha por hitos, y está en el precio) · fechas o precios distintos a los del PDF. Cualquier pregunta técnica o de números: "eso lo contesta Matías, lo llamamos ahora."

---

## PARTE 7 — La relación con Andrés (para que Matías decida)

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

**Lo delicado de esta vuelta:** Andrés pidió el escenario de 3 módulos y le llega uno de 6 equipos. **Se resuelve entero con el dato que dio él mismo**, y por eso el mensaje de §6.1 empieza agradeciéndole los metros: le muestra que **la decisión salió de su información, no de que su idea estuviera mal**. Las tres sondas por encomienda del último párrafo son la otra mitad de lo mismo — algo concreto, gratis y ahora, que lo hace quedar bien adentro. **Es lo único de este documento que no conviene que Matías recorte al copiar.**

---

## Anexo — Fuentes consultadas

- Alcance del bus, pull-ups, **tierras entre contenedores (§2.6)**, estrella no conmutada y límite prudente de 15 m: `C:\Proyectosrioseguro\hardware\ALCANCE_1WIRE.md` (@muestreador).
- **Costo por equipo y stock declarado:** `C:\Proyectosrioseguro\hardware1_modulos\BOM_KIT_V1.md` rev B (@hardware) — §1 inventario, §3.1 compra, §3.3 contingencias, §3.4 costo por equipo, §8.1 las dos mediciones que bloquean el pedido. Precios ML verificados el 2-sep-2026.
- Estado real y auditoría: `C:\Proyectosrioseguro\entrega_scz\docs\ESTADO_HONESTO.md` · `AUDITORIA_HALLAZGOS.md`.
- **Qué hace hoy el firmware con sondas, puerta, relé y defrost (leído el 3-sep-2026):** `firmware_revival/sondas.h` · `config.h` líneas 67-150 · `firmware_revival.ino` líneas 369-375, 483-488, 804-944 · `comandos_nube.h` (**sin** comando de relé).
- Contrato base: `MATI-HQ\comercial\CONTRATO_TERMOVIGIA_v4.md`.

**Canalización — precios verificados el 4-sep-2026 (la cuenta de §3.3):**
- Caño galvanizado Daisa 3/4 **liviano**, tira de 3 m, **$ 11.637** — https://www.electricidadarevonline.com.ar/MLA-1439417798-cano-galvanizado-daisa-34-liviano-x-tira-de-3-metros-_JM · ficha ML: https://www.mercadolibre.com.ar/cano-galvanizado-daisa-34-liviano-x-tira-de-3-metros/up/MLAU288375773
- Caño Daisa 3/4 **pesado** (no usado en la cuenta; 58 % más caro), $ 18.388 — https://electrodorrego.mercadoshops.com.ar/MLA-1116414163-cano-galvanizado-daisa-34-pesado-x-tira-de-3-metros-_JM
- Grampa omega galvanizada 3/4, **$ 3.976,85 la unidad de góndola** — https://www.grupodimexo.com.ar/MLA-1811056410-grampa-galvanizado-34-para-cano-_JM · referencia de pack ×100 (medida 2"): https://herrafex.mercadoshops.com.ar/MLA-1632841418-grampa-omega-para-cano-galvanizada-2-pulgada-x-100-unid-_JM
- Cable UTP cat5e exterior 100 % cobre, rollo 100 m ≈ $ 40.000 — https://articulo.mercadolibre.com.ar/MLA-934596791-cable-utp-rollo-100mts-100-cobre-exterior-cat5e-4-pares-_JM
- **Mano de obra de electricista: ARS 12.000-25.000/h** (valores AAIERIC vigentes 2026, CABA/GBA; el interior y la zona austral no son más baratos) — https://solvitapp.com.ar/blog/electricidad-precios-mano-obra-argentina-2026 · https://electricista24horas.ar/electricistas-matriculados/costos-mano-de-obra/ · https://roomix.ai/blog/cuanto-cuesta-electricista-2026
- **Honestidad sobre esta cuenta:** curvas, cuplas, cajas de paso estancas y conectores caño-caja son **estimados de plaza, no verificados uno por uno**. Suman $ 96.000 por par sobre $ 247.700 (39 % del material). **Aun poniéndolos en cero**, el escenario compartido da 2.100 + 197 + 420 + 1.800 = **USD 4.517 solo de material** — y basta media jornada de electricista por par para volver a superar los 4.540. **La conclusión de §3.4 no depende de esos renglones.**

**Otras:**
- 1-Wire: Maxim/Analog AN148 — https://www.analog.com/media/en/technical-documentation/tech-articles/guidelines-for-reliable-long-line-1wire-networks.pdf
- testo Saveris 2-T2 USD 318: https://www.ebay.com/itm/365602217221
- Novillo en pie $ 4.181/kg (INMAG jul-2026): https://www.consignatarias.com.ar/mercado
- Dólar BNA vendedor $ 1.535 (3-sep-2026): https://www.cronista.com/finanzas-mercados/dolar-oficial-asi-abre-la-cotizacion-este-jueves-3-de-septiembre/
- Supabase Pro USD 25/mes: https://www.nocode.mba/articles/supabase-pricing
- Código de Conducta de Proveedores de Pan American Silver (alcanza a subcontratistas): https://panamericansilver.com/wp-content/uploads/2023/02/Supplier-Code-of-Conduct-ES-LA.pdf

## Anexo — Lo que quedó abierto (para Matías, antes de mandar)

1. **Los números:** equipo **USD 520 × 5 = 2.600** · repuestos **340** · puesta en marcha **1.600** · **inicial 4.540** · abono **500/mes** (USD 100 por reefer) · B = **9.940**. Margen del equipo 28,5 %, del abono 75 %. ¿Van? *(El 520 sale de repartir la plataforma entre 5 y no entre 6; si preferís sostener 480, el margen baja a 23 % — §3.1.)*
2. **La línea del sexto reefer** (se suma a USD 520 el equipo y USD 100/mes de abono) está en el documento del cliente. Es lo único que se agregó de contenido nuevo al PDF. **¿Va así?**
3. **Condiciones de pago 50/50** (OC / equipos instalados y reportando): cambia el criterio de la v2, que facturaba la puesta en marcha por hitos (40/30/30). Ahora los hitos son compromiso de entrega, no facturas. **Confirmar.**
4. **Compra de materiales para los 6 equipos: ≈ $ 416.200 ($ 436.000 con flete)** — §3.10, con el cruce contra stock renglón por renglón.
5. **@hardware tiene que contar el stock y hacer las 2 mediciones del §8.1 del BOM** (amperaje real de las 5 fuentes, y si el relé cliquea con IN al aire) **antes de comprar**: mueven ~$ 40.000 del pedido. **Y hay que reservarle 3 ESP32 a las galgas de Dreyfus**, que es P0 de octubre — por eso el pedido de ESP32 es de 5 y no de 2.
6. **DECISIÓN DE PORTFOLIO, no comercial: los 6 kits son los mismos que iban a ser las 5 demos de Bahía.** Armarlos ahora no expone capital nuevo (si Cerro Moro no compra, van a su destino original), **pero si Cerro Moro compra, Bahía se queda sin demos.** Recomendación: **la reposición de los 5 kits de Bahía se dispara en el mismo pedido que la orden de compra** (≈ $ 400.000, 10 días). **Esto lo decide el Director, no yo.**
7. **Verificación cruzada entre sondas: hoy NO existe** (`sondas.h` calibra en un momento dado, no vigila deriva continua). Vendida en el **hito 2, semana 5**. Si no se puede cumplir, hay que sacar el punto 3 del bloque "por qué 4 sondas" del documento del cliente. **Decisión de Matías + confirmación de @firmware.**
8. **Accionamiento del relé desde el panel: tampoco existe** (no hay comando en `comandos_nube.h`). Vendido en el **hito 5, semana 15**. La alerta local que dispara el relé sola sí anda hoy.
9. **El sensor de puerta viene deshabilitado por defecto** (`SENSOR_DOOR_ENABLED false`): que quede en la orden de armado habilitarlo y probarlo antes de despachar. Y la **segunda salida a relé se vende como "disponible", no como gobernada**: verificar que el pin esté asignado en la línea que va a Cerro Moro.
10. **Cobertura de red en los 5 reefers:** único riesgo técnico abierto, depende de la respuesta de Andrés (§5.2). Si algún reefer queda sin señal, sumar un repetidor **antes** de despachar.
11. **Andrés:** opción 1, 2 o 3 de la Parte 7, y preguntarle para quién trabaja.
12. **PDF:** @diseno maqueta **un solo** documento de 2 páginas A4, marca Termovigía, sin logo ajeno, sin "Para:", sin validez. Archivo `PRESUPUESTO_CERRO_MORO.pdf` (+ `PRESUPUESTO_CERRO_MORO_INTERNO.pdf`). *(La v4 pedía dos maquetas gemelas; ahora es una.)*
13. Monotributo vs. RI: se pregunta cuando la empresa tenga nombre.
