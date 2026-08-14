# Nocturno local — 2026-08-14

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\cosechador` (P2 en hardware — **prioridad #1 por
convergencia UNIVERSIDAD**, y el único repo donde el análisis todavía cambia una
compra).
**Branch:** `nocturno/local-2026-08-14-cadena-alarma` (pusheado, `6740014`).

## TL;DR

El cosechador es un **detector de incendios**. Los tres análisis que tenía —el
modelo de energía del 07-18, el presupuesto de standby del 08-11 y todo el resto
de la documentación— miran **el emisor**. Nadie recorrió nunca la cadena que
justifica el proyecto: **hay fuego, ¿alguien en la cabina se entera?**

**De los 8 eslabones: 2 ejecutables, 2 con fricción, 4 ROTOS.** Y los cuatro
rotos comparten el mismo modo de falla: **el sistema se ve exactamente igual
funcionando que muerto.**

Tres números, sacados de los propios documentos del repo:

- **48 % de la autonomía declarada del emisor se gasta con el detector
  encendido y CIEGO.** El módulo de sensor de llama pide 3-5 V (D2); la ventana
  operativa llega a 2,7 V. Entre 3,0 y 2,7 V el nodo está vivo, sano, sin nada
  que reportar — y no puede ver fuego.
- **El receptor no dura 11 días sino 3,6.** `2600 mAh / 30 mA = 87 h`. Los "11
  días" de D10 son los de la LiPo de 8000 mAh **que D10 rechazó por excesiva**
  (`8000/30 = 11,1 días`). El argumento que descartó la batería grande usó, a
  favor de la chica, la autonomía de la grande.
- **El buzzer de 5 V nunca ve 5 V.** En los dos caminos de alimentación que el
  propio documento describe, el rail no pasa de 4,2 V. Y no hay **ni un dB** de
  volumen entre las métricas objetivo, que sí piden alcance RF y sensibilidad
  del sensor.

## Tarea elegida y por qué

Por rotación tocaba cosechador (los cuatro turnos previos: galgas, frioseguro,
datalogger, galgas; la última noche de cosechador fue el **08-11-b**).

Dentro del repo, la elección fue más fácil que de costumbre: **todo el `QUE_FALTA`
está bloqueado por la compra**, y los dos análisis previos ya cubrieron el eje
de la energía. Miré qué eje quedaba sin tocar:

| noche | qué modela | dónde empieza y termina |
|---|---|---|
| 07-18 `modelo-energia` | cuánta energía entra, cuánto dura el sleep | dentro del emisor |
| 08-11-b `presupuesto-standby` | qué se pierde con la máquina parada | dentro del emisor |

**Los dos son presupuestos de energía del emisor.** La función del producto —
detectar fuego y avisar— nunca se auditó. La pregunta que elegí:

> hay fuego en la cosechadora. Se recorre la cadena entera —llama, sensor, INT,
> confirmación, ADC, TX, ACK, receptor, buzzer, oído del operario—.
> **¿Cada eslabón funciona? ¿Qué pasa con cada uno cuando el banco está bajo, la
> batería del receptor vacía o el enlace caído?**

Elegí este ítem sobre cualquier otro por tres razones:

1. **Sigue siendo el único repo donde un análisis puede cambiar una compra.**
   A2 y A3 son del **BOM del receptor** (batería y buzzer) y A1 puede resolverse
   **eligiendo el SKU del sensor de llama con el rango correcto** — el mismo SKU
   cuyo consumo quedó sin cuantificar en S6 del 08-11. Nada de eso está comprado.
2. **La convergencia del repo es UNIVERSIDAD** (TC2, Medidas Electrónicas 2,
   candidato a Proyecto Final), que es prioridad #1.
3. **Un detector cuya falla es indistinguible del funcionamiento normal no es un
   MVP más chico: es otro producto.** Eso conviene saberlo antes de armarlo, no
   después.

## Qué hice

**`analisis/alarm_chain.py`** (stdlib, solo lectura, sin red ni hardware, no
compila nada). **No inventa números: LEE los que el repo declara** en
`DECISIONS.md`, `PROGRESS.md`, `CHANGELOG.md` y `docs/architecture.md`, cita
`archivo:línea` de cada uno y los cruza. Exit 0/1/2/3, `--json`, `--detail`,
`--fail-on`, `--root`.

**Tres oráculos** que demuestran los hallazgos en vez de afirmarlos:

- `--demo-cadena` recorre los **8 eslabones** como quien ejecuta la alarma y
  marca cada uno *ejecutable / fricción / ROTO*. Resultado: **2 / 2 / 4**,
  primer eslabón roto: el **0** (nadie sabe si la cadena está viva).
- `--demo-ventana` baja el banco de 3,3 V escalón por escalón y muestra quién
  sigue en rango: dónde el nodo **MIDE**, dónde queda **CIEGO** y dónde queda
  **MUERTO**, con la energía gastada en cada marca.
- `--demo-receptor` toma los números de D10 y muestra la cuenta correcta, de
  dónde salieron los "11 días", y la línea de tiempo del apagado silencioso.

**`analisis/test_alarm_chain.py` — 87 tests en 7 capas:** utilidades de texto,
física, extractores sobre fuentes sintéticas, los tres oráculos con números
fijados, un test por código de hallazgo sobre un **repo sintético sano al que se
le inyecta un solo defecto** (control negativo + delta), la capa "no salta cuando
no corresponde", y regresión sobre el repo real + CLI.

**`docs/cadena-alarma.md`** — el análisis completo y el orden de arreglo.

### Lo que hubo que resolver

- **Un checker que hardcodea las dos mitades de una contradicción no sirve.**
  Casi todo hallazgo acá es una contradicción **interna** del repo. Si el checker
  trae los dos valores adentro, no puede detectar que alguien arregló uno. Por eso
  **parsea**: corregido el documento, el hallazgo se apaga solo. Hay test de eso
  para los nueve.
- **La primera mención no es la que sirve.** D2 nombra al NRF24L01 dos veces:
  primero en un rechazo (*"NRF24L01 (mínimo 1.9 V)"*, sin rango) y después en la
  frase de compatibilidad (*"1.9-3.6 V"*). Quedarse con la primera aparición
  **pierde el rango y apaga medio análisis en silencio**. Ahora se busca la
  primera que efectivamente trae un rango; la mutación que afloja eso hace fallar
  2 tests.
- **El "24" de NRF24L01 es un número.** La fila de TX de la tabla de energía dice
  `| TX alarma (NRF24L01 + ATmega activo) | ~33 ms | ~12 mA | 1.3 mJ |`: leer los
  tres **primeros** números da un presupuesto de 24 ms / 1 mA inventado. Se leen
  los tres **últimos**. *(Acá la prueba de mutación me corrigió: yo había puesto
  además un filtro explícito del 24 que era **código muerto** — la regla de "los
  tres últimos" ya lo resolvía, y la mutación que lo sacaba **sobrevivía**. Saqué
  el filtro y reescribí el test para que muerda de verdad.)*
- **El "1/2" de la fórmula también es un número.** `E = ½ × 10 F × (...)`: en el
  repo real el ½ es un carácter tipográfico y el primer número es la capacidad,
  pero en cuanto alguien lo escribe `1/2` el extractor devuelve **1 F** y toda la
  energía queda mal por un factor 10. Ahora se lee por **unidad** (`10 F`, `18 J`),
  no por posición.
- **A5 no podía ser "el peor caso es más caro".** Con un solo reintento cualquier
  presupuesto se duplica: eso es aritmética, no un hallazgo. El umbral quedó en
  **5×** y con nombre (`EVENT_WORST_RATIO_MIN`), para separar *"el presupuesto
  quedó corto"* de *"el presupuesto es de otro escenario"*. El caso real da 15×.
- **El eslabón del receptor no se rompe por durar poco.** Que la batería dure 3,6
  días es un costo operativo (recargar seguido). Lo que **rompe** el eslabón es
  que se apague **en silencio**. Por eso el veredicto depende de si existe
  supervisión, no de los días: con heartbeat implementado el mismo eslabón baja a
  *fricción*. Hay test, y la mutación que lo hace incondicional falla.
- **A1 tuve que decidir si era un hallazgo o una queja.** Que un sensor tenga un
  mínimo de tensión no es un defecto. El defecto es la **combinación**: rail
  directo al banco (D7), ventana declarada por debajo de ese mínimo, y **ningún
  mecanismo que distinga "no hay fuego" de "no puedo verlo"**. El test del control
  negativo lo fija: con el sensor llegando al piso, A1 no salta.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **4 error · 2 warn · 3 info.**

| código | sev | qué |
|---|---|---|
| **A1** | error | **el detector se queda ciego mucho antes de quedarse sin energía.** El módulo de llama pide **3-5 V** (D2); el rail **es** el banco (D7: sin LDO) y la ventana declarada llega a **2,7 V**. Por debajo de 3,0 V el MCU sigue vivo (mín. 2,7 V) y la radio también (mín. 1,9 V), pero el sensor está fuera de rango: **8,5 J de los 18 J útiles = 48 % de la autonomía, gastada a ciegas** (con la ventana del paper, 38 %). Nada distingue *"no hay fuego"* de *"no puedo verlo"*. |
| **A2** | error | **la autonomía del receptor está sobrestimada 3×, y con el número de la opción que se rechazó.** D10 afirma ~11 días; `2600/30 = 87 h = 3,6 días`. Y los 11 son los de la **LiPo de 8000 mAh que D10 rechazó por "excesiva"** (`8000/30 = 11,1`). `architecture.md` §3.1 tiene la cuenta bien: el repo se contradice en dos archivos. El receptor es **la mitad que avisa**. |
| **A3** | error | **el buzzer —la única salida perceptible— nunca ve su tensión nominal.** Buzzer activo de **5 V**, fuente 18650 de **3,0-4,2 V**. Camino A (Vin): el propio doc dice que Vin acepta **7-12 V** — con 3,7 V el regulador está muy debajo de su dropout. Camino B (directo al pin 5V): el rail **es** la batería. En los dos, el buzzer trabaja al **60-84 %**, y el volumen cae con la batería. Cabina **ruidosa** de una cosechadora, y **ni un dB** entre las métricas. |
| **A4** | error | **el silencio es a la vez el estado normal y TODOS los estados de falla.** *"No hay tráfico — sistema invisible"*, dice la secuencia normal. Lo mismo se ve si: el emisor se quedó sin banco · está vivo pero ciego (A1) · el receptor se quedó sin batería (A2) · el enlace está obstruido · el firmware se colgó. **5 modos de falla indistinguibles del funcionamiento correcto, en un detector de incendios.** El heartbeat que los separa **ya está diseñado en el mismo documento** (secuencia, payload, período) con su costo calculado —**0,045 µW, ~2 % del sleep del MCU**— y quedó *"no implementado en MVP"*. |
| **A5** | warn | **el evento de alarma está presupuestado sólo en su mejor caso.** Presupuesto: 10 ms de wake + 1 TX = **1,46 mJ**. La secuencia de la misma página exige **50 ms** de confirmación y declara **hasta 15 reintentos**: **21,6 mJ = 15×**. La energía alcanza de sobra; el problema es que el peor caso es **exactamente la situación para la que existe el producto**. Y los 15 reintentos fallidos son el **único** momento en que el emisor sabe que el receptor no está — el repo no dice qué hace con eso. |
| **A6** | warn | **hay dos ventanas operativas y la energía útil sale de la más optimista.** `architecture.md` calcula hasta **2,7 V** (18 J); el paper y la métrica de PROGRESS ponen el piso en **2,8 V** (15,25 J): **18 % de más**. Y 2,7 V es **el mínimo absoluto del Pro Mini**: la ventana se calcula hasta el borde, sin margen para el ripple del pico de TX. |
| **A7** | info | **la corriente del TX no cierra con el diagrama de la misma página**: 4 mA (MCU) + 11 mA (NRF24) = **15 mA** arriba; **12 mA** en la tabla de abajo. Puede ser un promedio sobre los 33 ms, pero no está dicho, y es el número del que cuelgan todos los presupuestos de alarma. |
| **A8** | info | **el despertar por el sensor exige interrupción por NIVEL y no está escrito.** PROGRESS manda el sensor a *"un pin de interrupción (D2 o D3)"* con el MCU en `SLEEP_MODE_PWR_DOWN`. En `PWR_DOWN` sólo despiertan INT0/INT1 **por nivel bajo**, PCINT, WDT y TWI. Un `attachInterrupt(..., FALLING)` compila, **anda perfecto en el banco** con el MCU despierto, y no despierta nunca dormido. Prevenirlo cuesta una línea en el instructivo de la Fase 4. |
| **A9** | info | **los dos campos de diagnóstico del paquete no llevan lo que prometen.** `SUPERCAP_V` es el único dato de salud del emisor y, sin heartbeat, **viaja sólo dentro de la alarma**: llega cuando ya hay fuego. `TIMESTAMP` no puede ser tiempo: sin RTC y con el 99,9 % en `PWR_DOWN`, `millis()` no avanza — cuenta milisegundos **despierto** y desborda a los 65,5 s de vigilia acumulada. |

**Orden sugerido:**

1. **A4 — implementar el heartbeat que ya está diseñado.** Convierte cinco modos
   de falla mudos en un mensaje. **Sin esto, arreglar los otros no se puede
   verificar en el campo.**
2. **A2 + A3 — antes de comprar** (los dos son BOM del receptor): la batería con
   la cuenta correcta, un buzzer que suene con la tensión que realmente hay, y un
   **criterio de volumen** entre las métricas, al lado del alcance RF.
3. **A1 — decidir qué se hace con la zona ciega.** Tres salidas, y es decisión de
   producto: (a) piso de tensión más alto —cuesta autonomía—, (b) **un sensor con
   rango que llegue al piso real** —cambia el SKU, y es el momento: no está
   comprado—, o (c) señalizar la ceguera en el heartbeat de A4. **(c) es la
   barata y no excluye a las otras.**
4. **A6** — unificar la ventana en 2,8 V y rehacer los 18 J.
5. **A8 + A5** — dos líneas en el instructivo de la Fase 4 y una política escrita
   ante fallo de ACK, **antes** de escribir el firmware.
6. **A7, A9** — higiene.

## Lo que está BIEN (fijado por test, para no ir a revisarlo)

- **La topología del enlace es la correcta para el caso**: D4 eligió NRF24 normal
  contra PA+LNA y LoRa con el argumento bueno (metros, no kilómetros) y con los
  números de consumo al lado.
- **El auto-ACK está declarado.** El emisor *puede* saber si el aviso llegó; lo
  que falta es decir qué hace con eso (A5), no la capacidad.
- **`architecture.md` §3.1 tiene la cuenta del receptor bien hecha.** El error de
  A2 vive en D10: la aritmética correcta ya estaba en el repo.
- **El heartbeat está diseñado, no sólo mencionado** — secuencia, payload,
  período y costo. A4 es una decisión de alcance, no un problema técnico abierto.
- **La confirmación de llama de 50 ms existe**: el anti-falso-positivo está
  pensado.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\cosechador
git checkout nocturno/local-2026-08-14-cadena-alarma

python analisis/alarm_chain.py                  # informe; exit 3
python analisis/alarm_chain.py --detail         # + evidencia y afirmaciones leidas
python analisis/alarm_chain.py --demo-cadena    # los 8 eslabones, uno por uno
python analisis/alarm_chain.py --demo-ventana   # quien sigue en rango al caer el banco
python analisis/alarm_chain.py --demo-receptor  # de donde salieron los "11 dias"
python analisis/alarm_chain.py --json

cd analisis && python -m unittest test_alarm_chain   # -> Ran 87 tests, OK
```

Tres hallazgos se comprueban **sin la herramienta, con la calculadora**:

- `2600 / 30 = 86,7 h = 3,6 días` contra los "11 días" de `DECISIONS.md:207`; y
  `8000 / 30 = 11,1 días` (A2).
- `DECISIONS.md:44` dice **3-5 V** para el sensor; `docs/architecture.md:110`
  dice que la ventana llega a **2,7 V** (A1).
- `DECISIONS.md:199` dice buzzer de **5 V**; `docs/architecture.md:141` dice que
  la fuente es de **3,0-4,2 V** (A3).

**Verificado en esta máquina:**

- `py_compile` de los dos archivos.
- **87 tests en verde** (0,65 s). Sin descargas ni toolchains: cero riesgo de
  timeout.
- **Control negativo real:** un repo sintético sano no enciende **nada**, y cada
  defecto inyectado por separado enciende **uno y sólo un** código. Los nueve
  tienen además su test "no salta cuando no corresponde".
- **Verificado por mutación — 13 mutaciones, las 13 hacen fallar la suite:**
  quedarse con la primera mención en vez de la que trae rango · fracción ciega
  por tensión en vez de por energía · `parse_span` sin la forma en prosa · el
  eslabón del receptor ROTO sin mirar la supervisión · A2 tolerando desvíos de
  5× · `_ma` sin `\b` (comiéndose los `mAh`) · leer los tres **primeros** números
  de la fila de TX · exit code con la severidad menos grave · capacidad del banco
  por posición · A6 exigiendo las dos mitades en vez de cualquiera · A1 sin
  exigir que el sensor no llegue al piso · A5 sin umbral · A3 comparando contra
  el mínimo de la batería.
  *(El andamio de mutación fue descartable, en `/tmp`: no se commiteó. Borré el
  `__pycache__` antes de cada corrida y restauré el archivo al final —la trampa
  del 08-11. La primera pasada dejó **una mutación viva**: el filtro del "24" era
  código muerto. La saqué y reescribí su test; ahora muerde.)*
- **No se tocó ninguna decisión de compra, ni el BOM, ni el paper, ni los PDFs.**
  El branch agrega 3 archivos y edita `QUE_FALTA.md` y `PROGRESS.md`. No hay
  dashboard ni firmware que compilar: el repo no tiene código de producción.

## Qué quedó sin verificar

- **Todo sale de leer los documentos, no de medir un sistema.** No hay sistema:
  nada está comprado. Los oráculos demuestran el efecto de lo que el repo *dice*.
- **A1 se apoya en el "3-5 V" que D2 le atribuye al módulo de sensor de llama**,
  que todavía **no tiene SKU ni datasheet en el repo**. Es el mismo hueco que S6
  del 08-11 (el consumo del módulo). **Al elegir el SKU hay que anotar las dos
  cosas juntas: rango de alimentación y consumo en reposo.** Si el módulo elegido
  arranca desde 2,7 V, **A1 se cae** — y elegirlo así es, de hecho, la salida (b).
- **A3 supone que un buzzer activo pierde volumen con la tensión.** Es cierto en
  general para los piezo con oscilador integrado, pero **cuántos dB se pierden a
  3,7 V depende del SKU** y no está medido. La premisa del dropout del regulador
  del Nano (camino A) es externa; **el camino B no depende de ella**.
- **A6 tiene una premisa externa**: el nivel del fusible BOD del Pro Mini
  3.3 V/8 MHz. Se lee en un minuto con `avrdude -U lfuse:r` cuando haya placa.
- **A8 se apoya en el datasheet del ATmega328P** (tabla de fuentes de wake-up por
  modo de sleep), no en una prueba.
- **Ningún fix aplicado** — generator ≠ evaluator. El más barato (A6, unificar la
  ventana) tampoco lo toqué: el que corrige un número del paper tiene que ser el
  que decide la ventana.

## Estado

- Branch `nocturno/local-2026-08-14-cadena-alarma` pusheado (`6740014`), sale de
  `main` (`388795b`). **cosechador volvió a `main` limpio** (venía checkouteado
  en el branch del 08-11-b desde esa noche; lo dejé en main).
- `QUE_FALTA.md` y `PROGRESS.md` del repo actualizados **dentro del branch**.
  ⚠️ **Conflicto anunciado:** el branch del **08-11-b** agrega una sección con el
  **mismo encabezado** (`## Análisis offline hecho…`) en `QUE_FALTA.md` y también
  escribe al final de `## Anda ✅` y en la tabla de métricas de `PROGRESS.md`. Al
  mergear los dos va a haber conflicto **trivial**: se conserva un solo
  encabezado y **los dos bloques**, uno abajo del otro. Usé el encabezado
  textualmente igual justamente para que la resolución sea obvia.
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Decimocuarta noche que lo reporto:** es firmware que va a un equipo a 2000 km
  y vive **sólo en este disco**. **No lo toqué.**
- ⚠️ **`C:\Proyectos\datalogger` sigue con trabajo de día SIN COMMITEAR**
  (`firmwares/nodo-gimap/`, `tools/rx_gimap.py`, los dos tests del nodo GIMAP,
  `docs/ARMADO_NODO_GIMAP.html`, `.gitignore`). **No lo toqué.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las
  diecinueve noches anteriores: `agentes/`, `dominios/`, `enlace/`, más
  `agentes/diseno3d.md`, `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html` y
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- ⚠️ Sigue el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando quieras.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío (sólo el `.gitkeep`). El único
  `enlace\maquinas\*.estado.json` (DESKTOP-RK8DH7C) sigue con `ultima_vez_viva`
  del **2026-08-07**: el latido está parado hace **7 días**. **No lo toqué** (los
  scripts de ENLACE son trabajo de día sin commitear).
- La cola de merge suma **57 branches** en origin (galgas 20, datalogger 17,
  frioseguro 17, cosechador **3**).
  **Nota de prioridad, otra vez:** los **3 de cosechador siguen siendo los más
  baratos de mergear de toda la cola** — el repo no tiene firmware, ni nube, ni
  dashboard: no hay nada que romper. Y son los únicos cuyos hallazgos **todavía
  pueden cambiar una compra**.

## Para @firmware / @hardware / @comms / @energia / @cronista / @verificador

- **@firmware:** **A4 es tuyo y es el más importante de la noche.** No es diseñar
  nada: el heartbeat está **escrito completo** en `architecture.md` §4.3 —
  secuencia, payload, período— con el costo ya calculado (0,045 µW). Sacarlo de
  "opcional" es lo único que hace verificable todo lo demás. Después **A8**, que
  es una línea en el instructivo de la Fase 4 (**nivel**, no flanco) y te ahorra
  el bug que anda perfecto en el banco y no despierta nunca en campo.
- **@hardware:** **A2 y A3 son tuyos y tocan el BOM del receptor**, que no está
  comprado. La batería hay que elegirla con la cuenta correcta (3,6 días, no 11)
  y el buzzer con la tensión que realmente hay (3,0-4,2 V, no 5). Y el **SKU del
  sensor de llama** ahora tiene **dos** requisitos que anotar juntos: **rango de
  alimentación** (A1, esta noche) y **consumo en reposo** (S6, del 08-11).
- **@comms:** **A5 es tuyo.** El auto-ACK ya te dice si el aviso llegó — falta la
  **política**: qué hace el emisor después de 15 reintentos fallidos. Es el único
  momento en que el sistema sabe que el enlace está cortado, y hoy esa información
  se tira.
- **@energia:** **A1 y A6 son tuyos.** A6 es coherencia (unificar la ventana en
  2,8 V y rehacer los 18 J). A1 es más de fondo: **el piso útil del banco no lo
  fija el MCU, lo fija el sensor**, y eso cambia el número contra el que venís
  midiendo autonomía desde el 07-18. Los 2,6-6,7 días de S1 son de un nodo
  **vivo**; la parte **útil** de esa ventana es más corta.
- **@cronista:** `docs/architecture.md` es el documento que sostiene el proyecto
  y **se contradice consigo mismo en tres lugares** (§2.1 vs §3.1 vs D10; la
  tabla de energía vs el diagrama de arriba; la ventana vs el paper). No es drift
  contra el código —no hay código—: es drift **interno**. Conviene arreglarlo
  junto con los fixes, no antes.
- **@verificador:** el DoD es *"cada eslabón de la cadena de alarma tiene un
  hecho del repo que lo confirma o lo desmiente"*. Los 87 tests son el oráculo y
  `TestRepoReal` fija los 9 hallazgos. **Puntos a atacar, en orden:** (1) **A1 es
  el que más se apoya en un dato que el repo no tiene**: el "3-5 V" es lo que D2
  le atribuye a un módulo sin SKU. Si el módulo real arranca desde 2,7 V, A1 se
  cae entero (**A2, A3 y A4 no dependen de ella**). (2) **A3 tiene una premisa
  externa** (dropout del regulador del Nano) que sólo afecta al camino A; el
  camino B se sostiene con la aritmética sola. (3) **A5 y A7 son los más
  discutibles**: los dos podrían defenderse como "el número es un promedio", y
  por eso están en warn/info y no en error. (4) **A2 es el más sólido de todos**:
  es una división, y el repo ya la tiene hecha bien en otro archivo.
