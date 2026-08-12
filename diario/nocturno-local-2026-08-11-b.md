# Nocturno local — 2026-08-11-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\cosechador` (P2 en hardware — **prioridad #1 por
convergencia UNIVERSIDAD**).
**Branch:** `nocturno/local-2026-08-11-b-presupuesto-standby` (pusheado, `d2ad9bf`).

## TL;DR

El cosechador tenía calculada la autonomía del emisor sin batería: **77,2 días**.
Ese número cuenta **una sola** de las cuatro cargas que el banco alimenta las 24 h.
Las otras tres salen de las decisiones **D3 y D8 de este mismo repo** y suman 23 µA
contra los 0,75 µA del MCU. **La autonomía real en reposo es de 2,6–6,7 días.**

Y de paso: **las resistencias de balanceo elegidas son 5,6× más débiles que la fuga
de celda que tienen que corregir** — con dispersión 10× entre celdas quedan 33 mV de
margen antes de pasarse de los 2,7 V nominales, que es el modo de falla que la
propia D3 marca como "⚠️ QUEMA".

**Nada de esto está comprado todavía.** Es el momento más barato posible.

## Tarea elegida y por qué

El 1er turno de hoy fue a galgas (cadena de entrega). Por rotación tocaba
datalogger o cosechador. Elegí **cosechador**, por tres razones:

1. **Es el repo más fresco por lejos.** Un solo branch nocturno, del **07-18** —
   hace 24 días. galgas tiene 20 branches, datalogger 16, frioseguro 16. Cosechador,
   uno.
2. **Su convergencia es UNIVERSIDAD, que es prioridad #1**, no #2. El `QUE_FALTA`
   mapea explícitamente el análisis de circuito a **TC2** y la caracterización a
   **Medidas Electrónicas 2**.
3. **Es el único repo donde el análisis todavía puede cambiar una compra.** En los
   otros tres, los hallazgos apuntan a firmware ya flasheado o a placas ya armadas.
   Acá la Fase 1 (comprar, ~$154.500) sigue abierta: **D3 y D8 no se soldaron.**

Dentro del repo, la pregunta la eligió el trabajo del 07-18. Ese modelo respondió
*"cuánta energía entra y cuánto dura el sleep del MCU"*. La pregunta de al lado
nunca se hizo:

> además del MCU, **¿qué más está chupando del banco todo el tiempo?**

## Qué hice

**`analisis/standby_budget.py`** (stdlib, solo análisis, sin hardware ni red, no
compila nada). Enumera las cargas permanentes con **la fuente citada de cada una**,
las suma y recalcula autonomía, margen de balanceo y duty mínimo de vibración.
Exit 0/1/2/3, `--json`, `--detail`, `--fail-on`, y tres oráculos.

**`analisis/test_standby_budget.py` — 79 tests en 7 capas.**

**`docs/presupuesto-standby.md`** — el análisis completo y qué hacer antes de comprar.

### Lo que había que resolver

- **Las cargas son de dos familias físicas distintas, y mezclarlas es el núcleo.**
  El sleep del MCU es **corriente constante** → la tensión cae en recta
  (`t = C·ΔV/I`). Fuga, balanceo y divisor son **resistivos** → cae exponencial
  (`t = RC·ln(V_hi/V_lo)`). Juntas, `C dV/dt = −(V/R + I)` integra a
  `t = RC·ln((V_hi+IR)/(V_lo+IR))`, con los dos casos puros como límites. El modelo
  del 07-18 no necesitaba esto: allá **toda** carga era de corriente constante.
- **Cómo hacer la fuga del supercap comparable con las resistencias de balanceo.**
  El datasheet la da como **corriente máxima a tensión nominal** (15 µA/celda @ 2,7 V,
  a las 72 h; Maxwell doc. 3001976). Modelarla como **resistencia**
  (`R = V_nom/I_spec = 180 kΩ/celda`) es lo que permite ponerla al lado del 1 MΩ del
  balanceo y ver que **el balanceo pierde**. Sin ese cambio de unidades, S3 no se ve.
- **Ser honesto con un spec que es un máximo.** A 1,65 V/celda la fuga real es menor
  que a 2,7 V, y un EDLC no es óhmico. Por eso la herramienta **nunca imprime un
  número solo**: siempre el rango entre el máximo de spec y una fracción típica
  declarada (1/5). La conclusión aguanta el rango entero, y aguanta incluso un
  datasheet 10× pesimista (hay test).
- **El oráculo me corrigió a mí.** Escribí que el atajo `Q/I` del 07-18 sería
  *optimista*. La tabla mostró que es **~7 % conservador** (evaluar la corriente a
  3,3 V es el peor instante del tramo). Reescribí la conclusión: **el error del
  07-18 no estuvo en la matemática del atajo, estuvo en las tres cargas que no
  entraron a la suma.** Sumarlas mal igual habría mostrado el problema; no sumarlas,
  no. Quedó como test.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **3 error · 1 warn · 2 info.**

| código | sev | qué |
|---|---|---|
| **S1** | error | la autonomía publicada cuenta **1 de las 4** cargas permanentes: 77,2 días → **2,6–6,7 días** (12–30× menos). Un **detector de incendios** que se muere en menos de una semana de máquina parada no vigila el fin de semana largo, ni la temporada baja, ni las tres semanas en el galpón. Modo de falla: el nodo está apagado **justo cuando nadie lo mira**. |
| **S2** | error | la métrica `sleep ≤ 5 µA` de PROGRESS mide **la carga** (Pro Mini + sensor + radio). El banco entrega **9,4–24,0 µA**, de los cuales el MCU es 0,75. **La métrica puede dar OK con la autonomía rota**: mide el consumidor equivocado. Lo que decide es la corriente en el **borne del banco**, y no está pedida en ningún lado. |
| **S3** | error | **el balanceo (1 MΩ) es 5,6× más débil que la fuga (180 kΩ)** que debe corregir. Con dispersión 10× entre celdas la más cargada queda a **2,667 V contra 2,7 V nominales: 33 mV**. Con 20×, se pasa. D3 rechazó los 100 kΩ por consumo — pero son **33 µA contra 958 µA de harvest (3,4 %)**. **El trade real es "margen de sobretensión vs. días parada", y nunca se planteó así.** |
| **S4** | info | queda acotado el **duty mínimo de vibración: 0,8–2,1 %** = **12–31 min/día** (design 2). Es el ítem que el 07-18 dejó abierto. No es el duty *real* de la cosechadora (eso se mide) sino **el mínimo que exige el diseño**, que es contra qué compararlo. Buena noticia: no pide vibración continua. |
| **S5** | info | los parásitos **NO** comprometen el arranque en frío (8,12 h → 8,21 h, +1,1 %): vibrando, el harvest domina 40×. **El cuello de botella del 07-18 sigue en pie**; esto rompe la autonomía **en reposo**, que es otro eje. Los dos conviven. |
| **S6** | warn | **la doctrina del LED se aplicó a una sola de las dos placas siempre alimentadas.** D1 declara *mandatorio* desoldar el LED del Pro Mini por estar prendido 24 h. El módulo de sensor de llama también lo está, también trae LED, y además un comparador — y ninguna decisión lo menciona. **No lo cuantifiqué a propósito**: no está comprado y no hay datasheet del SKU. Es carga **conocida y no cuantificada**, y puede dominar todo lo demás. |

**Orden sugerido** (todo antes de comprar, salvo el último):
decidir **a qué autonomía en reposo se apunta** (decisión de producto, ordena el
resto) → si importa, entender que **el término dominante es inherente al SKU**, no
se sale con resistencias → rehacer **D3** como el trade que realmente es → corregir
la métrica de PROGRESS (**S2**) → **cuantificar el sensor de llama (S6)**, que puede
invalidar todo lo anterior.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\cosechador
git checkout nocturno/local-2026-08-11-b-presupuesto-standby

python analisis/standby_budget.py                    # informe; exit 3 (hay errores)
python analisis/standby_budget.py --detail           # los 6 hallazgos con sus numeros
python analisis/standby_budget.py --demo-autonomy    # las dos familias de carga
python analisis/standby_budget.py --demo-balance     # la tabla de sobretension (S3)
python analisis/standby_budget.py --demo-coldstart   # por que el arranque no sufre
python analisis/standby_budget.py --json

cd analisis && python -m unittest test_standby_budget   # -> Ran 79 tests, OK (skipped=1)
```

**Verificado en esta máquina:**

- `py_compile` de los dos archivos.
- **79 tests en verde** (0,013 s). El *skipped* es a propósito: es el cross-check
  contra `harvester_model.py`, que **no está en `main`** porque el branch del 07-18
  sigue sin mergear.
- **El skip no es decorativo — lo probé.** Monté los dos branches juntos en un
  temporal (`git show nocturno/local-2026-07-18-modelo-energia:analisis/harvester_model.py`)
  y corrió: **79/79, cero skips**. Los dos modelos son consistentes: el nuevo
  reproduce los 77,2 días del viejo con la misma carga única, y las dos corrientes
  de harvest coinciden a 1e-12. El día que ambos se mergeen, el test se activa solo.
- **Verificado por mutación:** las **6** hacen fallar la suite — serie/paralelo
  invertidos, `decay_time_s` ignorando el offset `I·R`, el divisor de balanceo dado
  vuelta (celda mala en vez de buena), el sostenimiento evaluado a 3,3 en vez de
  2,8 V, la fuga multiplicada en vez de dividida, y la capacidad 2s2p invertida.
- **Control negativo:** con celdas ideales la autonomía **vuelve a 77,2 días** y el
  valor del balanceo deja de importar. Las conclusiones se dan vuelta cuando se dan
  vuelta las premisas físicas.

Sin descargas ni toolchains: cero riesgo de timeout. **No se tocó ninguna decisión
de compra, ni el BOM, ni el paper.** El branch agrega 4 archivos y edita 2 docs.

> ⚠️ **Trampa del harness, para que no confunda a nadie:** en el temporal de la
> prueba de mutación, restaurar el archivo dejó un `__pycache__` obsoleto (mismo
> tamaño y mtime que la versión mutada) y la corrida siguiente reportó 2 fallos
> falsos. Se arregla borrando `__pycache__`. **El repo nunca estuvo afectado** —
> verificado llamando la función directamente.

## Qué quedó sin verificar (necesita banco)

- **Todo sale de leer decisiones y aplicar circuitos, no de medir un banco.** La
  medición que cierra esto es barata y no necesita instrumental raro: cargar el
  banco, desconectar el harvester, y medir la caída de tensión durante 72 h.
- **La fuga real.** El spec es un **máximo a tensión nominal y 25 °C**; en operación
  la celda está a ~1,65 V. Además, a los **60 °C** del riesgo ya anotado en PROGRESS
  la fuga **sube**, y este modelo no cubre la temperatura.
- **El sensor de llama no está contado** (S6). Es el hueco más grande y el que puede
  mover todo.
- **El quiescent del LTC3588 tampoco** — falta el datasheet en el repo. Suma, no resta.

## Estado

- Branch `nocturno/local-2026-08-11-b-presupuesto-standby` pusheado (`d2ad9bf`),
  sale de `main`. `QUE_FALTA.md` y `PROGRESS.md` del repo actualizados **dentro del
  branch**.
- ℹ️ **Moví `cosechador` de branch.** Estaba checkouteado en
  `nocturno/local-2026-07-18-modelo-energia` (estado que arrastraba desde el 07-18);
  lo pasé a `main` para sacar el branch nuevo de ahí. **Ningún commit perdido** — el
  branch del 07-18 sigue intacto, local y en origin.
- ℹ️ El repo no tenía `.gitignore` en `main`; agregué uno (`__pycache__/`, `*.pyc`).
  **El branch del 07-18 agrega el suyo**: cuando se mergeen los dos va a haber un
  conflicto trivial en ese archivo. Avisado.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`). **Décima
  noche que lo reporto:** es firmware que va a un equipo a 2000 km y vive **sólo en
  este disco**. **No lo toqué.**
- ⚠️ **`C:\Proyectos\datalogger` sigue con trabajo de día sin commitear**
  (`firmwares/nodo-gimap/`, `tools/rx_gimap.py`, `tools/test_protocolo_gimap.py`,
  `tools/test_red_gimap.py`, `docs/ARMADO_NODO_GIMAP.html`, `.gitignore` modificado).
  **No lo toqué.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las quince
  noches anteriores, más `agentes/diseno3d.md`, `dominios/diseno3d.md`,
  `dominios/LOGO_RED_GUIA.html` y `propuestas/MAIL_SAE_PPS.md`). **No los toqué.**
  Matías: commitealos, o la rutina cloud choca en el próximo `git pull`.
- ⚠️ Sigue el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando quieras.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío (sólo el `.gitkeep`). El único
  `enlace\maquinas\*.estado.json` sigue con `ultima_vez_viva` del **2026-07-07**.
  **No lo toqué.**
- La cola de merge suma **53 branches** en origin (galgas 20, datalogger 16,
  frioseguro 16, cosechador **2**).
  **Nota de prioridad para el drenaje:** los **2 de cosechador son los más baratos
  de mergear de toda la cola** — el repo no tiene firmware, no tiene nube y no tiene
  dashboard, así que no hay nada que romper. Y son los únicos cuyo hallazgo **todavía
  puede cambiar una compra**. Si hay una hora de día para la cola, empezar por acá
  rinde más que por cualquiera de los otros tres.

## Para @energia / @esquematico / @hardware / @verificador

- **@energia** (dueño del perfil de energía): la pregunta que ordena todo es **a qué
  autonomía en reposo se apunta**. Es decisión de producto. El modelo te da los dos
  extremos y el duty mínimo (0,8–2,1 %) que cierra el ítem que dejaste abierto el
  07-18.
- **@esquematico** (dueño de D3 y D8): **S3 es tuyo.** El valor del balanceo hay que
  reelegirlo con el criterio correcto (dominar la dispersión de fuga), no con el de
  ahorro de corriente. Y D8 ya trae su propia salida escrita (divisor por GPIO) que
  nadie adoptó.
- **@hardware**: el término dominante (18 µA) **es inherente al SKU**. Si la
  autonomía importa, la variable de compra es la **fuga especificada** de la celda,
  no su capacidad — y el BOM hoy sólo mira capacidad.
- **@verificador**: el DoD es *"cada carga tiene fuente citada, y el modelo reproduce
  los 77,2 días del 07-18 con la misma carga única"*. Los 79 tests son el oráculo.
  **Puntos a atacar, en orden:** (1) ¿es legítimo modelar la fuga del EDLC como
  resistencia? Es primer orden declarado, y es lo que hace la comparación con el
  balanceo posible — si se cae, se cae S3 (S1 aguanta, porque cualquier modelo de
  fuga razonable deja la corriente muy por encima de 0,75 µA). (2) ¿la dispersión
  10× entre celdas del mismo lote es realista? Es la premisa de la tabla de S3, y es
  la que menos apoyo tiene: no tengo dato de dispersión, sólo el máximo de spec.
  (3) S4 y S5 dependen de la tasa de carga del paper, ya validada el 07-18.
