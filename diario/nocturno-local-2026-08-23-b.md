# Nocturno local — 2026-08-23-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\cosechador` (convergencia UTN: TC2 + Medidas
Electrónicas 2 + candidato a Proyecto Final).
**Branch:** `nocturno/local-2026-08-23-b-la-curva-de-carga` (pusheado, `071ae0e`).
**Sale de:** `main`.

## TL;DR

> **Las 8,69 h contra las que el DoD compara no son un tiempo medido.**

Son `3 V / 0,345 V/h`: la extrapolación **×17,4** de un ensayo de **30 minutos**
en el que la tensión subió **172 mV**. Leído con el modelo que corresponde a un
buck alimentado por un piezo —**potencia** constante, no corriente— el mismo dato
crudo da **151 h**.

Y el corolario, que es lo que de verdad vale:

> **Los dos modelos pasan exactamente por el punto que el paper midió, así que un
> solo punto no puede elegir. El dato que decide 17× de diferencia estaba adentro
> del ensayo que ya se corrió** — a los **10 minutos** las dos curvas ya difieren
> **42 mV**, que son **42 veces** la resolución de un multímetro de mano.

| | supone | design 2 → 3 V |
|---|---|---|
| corriente constante (`i = C·dV/dt`) | recta | **8,70 h** ← lo que el paper publica |
| potencia constante (`P = d(½CV²)/dt`) | raíz | **151,2 h** |
| + las cargas permanentes del 08-11-b | asíntota | **304 h** |

## Tarea elegida y por qué

Por rotación tocaba cosechador: es el único de los cuatro repos que llevaba
**una semana** sin tocarse (último turno, 08-16), y en la jerarquía va con
**UNIVERSIDAD**. Los otros tres se trabajaron ayer y hoy (galgas 08-22-b,
datalogger 08-22, frioseguro 08-23 primer turno).

Dentro del repo seguí el patrón que viene funcionando: **no abrir una auditoría
nueva, tomar un pendiente ya nombrado con su evidencia medida.** La auditoría del
08-16 dejó once hallazgos, y sobre uno escribió esta frase literal:

> *«@energia: M1, M2, M4 y M6 son tuyos, y **M4 es el que ordena todo lo demás**:
> hasta que no esté escrito si la carga se extrapola lineal o por potencia, no se
> puede planificar el ensayo ni juzgar el resultado.»*

Elegí M4 y no otro por tres motivos:

1. **Ordena a los otros.** M5 y M2 son de la lista de compras; M6 es «poner un
   número donde hay un adjetivo» en el criterio de la Fase 2 — y **ese número
   depende de qué modelo se use**. Hacer M6 antes que M4 es escribir el criterio
   dos veces.
2. **Es gratis y es hoy.** El repo está bloqueado en la fase 1 (comprar), así que
   casi todo lo demás necesita hardware o plata. Esto es papel y lápiz, y es lo
   único de la lista que se puede cerrar entero esta noche.
3. **La contradicción es interna, no una opinión sobre el paper.** El modelo del
   07-18 (`harvester_model.py`) codifica corriente constante; la auditoría del
   08-16 dice que el mismo dato da 151 h con potencia. **Dos branches del mismo
   repo con 17× de diferencia sobre la métrica del DoD.**

## Qué hice

**`analisis/carga.py`** — los dos modelos sobre el mismo dato crudo del paper,
más las cargas permanentes que **ninguno de los dos tenía**. Stdlib pura, sin
red, sin hardware. Cinco vistas: `--demo-tabla6`, `--demo-plausibilidad`,
`--demo-discriminar`, `--demo-cargas`, `--json`.

**La decisión (D17): potencia constante.** Tres razones, en orden de peso:

1. **Física.** El LTC3588 es un buck: acumula en el cap de entrada hasta su UVLO
   y entrega paquetes de energía al ritmo que le impone el piezo. Lo que se
   conserva aguas abajo es la potencia; lo que cae con la tensión del banco es la
   corriente.
2. **Plausibilidad — la que más pesa.** El modelo de corriente constante exige
   que **el mismo piezo, con la misma vibración, entregue 17× más potencia con el
   banco lleno que vacío**: 165 µW a 0,17 V y **2,9 mW a 3 V**. Casi 3 mW de un
   disco piezoeléctrico a 4 g. El de potencia pide **82,7 µW constantes**.
3. **Consistencia.** Bajo el modelo lineal el paper estaría reportando un
   harvester de miliwatts alimentando un nodo de 0,75 µA, holgura que su propia
   Tabla 5 no insinúa en ningún lado.

**Y no queda como opinión — ese es el punto del branch.** La medición que
confirma o revierte D17 es la más barata del proyecto:

```
       t  corriente cte   potencia cte   separacion
     5 min          28.7m          70.4m        41.7m
    10 min          57.5m          99.6m        42.1m   <-- primera lectura defendible
    30 min         172.5m         172.5m         0.0m   <-- fin del ensayo del paper
    60 min         345.0m         244.0m      -101.0m
```

Las curvas se cruzan en los 30 min **porque las dos están ajustadas a ese punto**.
El criterio pide **dos** cosas a la vez —separación ≥ 20 mV **y** banco arriba de
**100 mV** (abajo de eso manda el escalón de ESR y la relajación dieléctrica, el
mismo piso que ya usaba `measurement_chain.py`)— y da los **10,1 min**. Sin ese
piso la respuesta sería «a los 30 s», cuando las dos curvas valen milivolts y la
lectura no significa nada; **hay un test que fija que ese piso es lo que mueve la
respuesta**, para que nadie lo saque por prolijidad.

**La Fase 2 se reescribe:** banco a 0 V, excitar, **anotar la tensión cada 5 min
durante 30 min**, ajustar los dos modelos a la última lectura y ver cuál pega
con las intermedias. **No hay que cargar hasta 3 V para elegir modelo** — y bajo
el modelo adoptado, cargar hasta 3 V son **6,3 días**, no una noche. Esto además
cierra de hecho M6 (el criterio cualitativo «sube monotónicamente»).

**El hallazgo de paso, que no buscaba:** el 08-11-b encontró 24 µA colgados del
banco y los usó para la **descarga**. También entran en la **carga**, y ahí hacen
algo que la descarga no muestra: la corriente de carga **cae** con V y la de las
cargas **sube** con V, así que **se cruzan**. Hay asíntota.

```
C·dV/dt = P/V − V/R − I₀     →     V∞ = ½(−I₀R + √(I₀²R² + 4PR))
```

Con la fuga al máximo de spec, **V∞ = 3,37 V**: el banco llega a los 3 V, pero
con 0,37 V de margen y por el tramo más lento de la curva (**304 h**, el doble).
**Si alguien baja las resistencias de balanceo o el piezo rinde menos que el del
paper, la asíntota cruza por debajo de 3 V y el banco no llega nunca** — no
«tarda mucho»: **no llega**. Ese modo de falla **no existe** en el modelo lineal
(958 µA contra 24 µA es una corrección del 2 %). La fuga del banco pasa de
detalle de datasheet a **parámetro de diseño**.

La integral va en el eje de la **tensión** y no del tiempo, porque con potencia
constante `dV/dt` es singular en V=0 y `C·V dV/(P − V²/R − I₀V)` no. Es la misma
cuenta de TC2 que hizo el 08-11-b para la descarga, del otro lado del signo — o
sea que la convergencia académica del branch no es decorativa.

**Consecuencias escritas en el repo:**

- **`PROGRESS.md`**: la métrica pasa de «tiempo de carga ≤ 12 h» —que bajo el
  modelo adoptado **ningún** diseño del paper cumple— a **potencia cosechada
  ≥ 80 µW @ 4 g / 150 Hz**, con el tiempo de carga como cantidad **derivada**.
  El objetivo viejo se había escrito pegado al número del paper: el design 3 daba
  12,65 h contra un objetivo de 12 h.
- **`Tchr [V/h]` no es una propiedad del harvester**: depende del tramo de
  tensión y del banco. Dos tests lo fijan — con Tchr como dato el tiempo a 3 V
  **no depende de C** (la capacidad ya está adentro del dato), y el mismo Tchr
  sobre 1 F es 10× menos potencia: un harvester que con las cargas puestas **ya
  no pasa de ~1 V**.
- **`DECISIONS.md` D17**, con su cláusula de reversión explícita.

**Archivos:** `analisis/carga.py` + `analisis/test_carga.py` (nuevos),
`docs/carga-supercap.md` (nuevo), `DECISIONS.md` (D17), `PROGRESS.md` (métrica),
`QUE_FALTA.md` (puntero + nota de merge), `.gitignore` (no existía en `main`).

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\cosechador
git checkout nocturno/local-2026-08-23-b-la-curva-de-carga

# 1. la decision y sus cuatro vistas
python analisis/carga.py
python analisis/carga.py --demo-tabla6
python analisis/carga.py --demo-plausibilidad
python analisis/carga.py --demo-discriminar
python analisis/carga.py --demo-cargas
python analisis/carga.py --json

# 2. los tests -> Ran 79 tests, OK (0,17 s)
cd analisis && python -m unittest test_carga
```

**Verificado esta noche:**

- **79/79 tests OK** en 0,17 s.
- Los cinco demos y el `--json` corren; hay un test que exige que **toda la
  salida sea ASCII** (la consola de Windows te rompía los guiones largos — se
  vio en la primera corrida de esta noche).
- **Mutación: 12 mutantes, los 12 caen.** Modelo de potencia linealizado, raíz
  sacada, `i_harvest` sin la caída con V, `R_eq` sin el balanceo, cargas sin el
  sleep del MCU, signo de V∞, integrador ignorando las cargas, pesos de Simpson
  planos, piso de legibilidad removido, banda de plausibilidad abierta, fuga
  típica igualada al spec, `t_hasta_v` sin el cuadrado.
- **Ancla contra el paper:** el modelo reproduce los tres «Time 0→3V» publicados
  a menos de 0,02 h leyendo el ensayo como corriente constante. Si no los
  reprodujera, el que está mal es el modelo, no el paper.
- Dos afirmaciones se chequean **sin la herramienta**, con calculadora:
  `3 / 0.345 = 8.70` y `0.5·10·0.1725²/1800 = 82,7 µW` → `10·3²/(2·82,7µ)/3600 = 151 h`.

## Lo que quedó SIN verificar (y por qué)

- **Nada se midió.** Todo es papel y lápiz ejecutable. Cierra **M4** (la decisión
  estaba sin tomar y ahora está tomada, escrita y con cláusula de reversión);
  **no** cierra la métrica.
- **La premisa que sostiene la razón #2**: la banda de 10-500 µW plausible para
  un piezo de laboratorio es **externa al repo**, declarada como constante con
  nombre. Si el piezo real de Matías entrega 3 mW, ese argumento se cae — y la
  decisión igual se resuelve con el ensayo de 30 min, que no depende de la banda.
- **La eficiencia del buck se supone constante.** Si el LTC3588 fuera bastante
  menos eficiente a baja tensión de salida, la curva real quedaría **entre** los
  dos modelos, más cerca del de potencia.
- **M5 sigue siendo la compra y esto no lo tapa**: sin excitador de vibración
  controlada + acelerómetro, el ensayo de 30 min caracteriza *nuestro* harvester
  pero no lo hace comparable con las 4 g / 150 Hz del paper.
- **M1 y M2 no se tocaron** — son de la métrica de sleep, no de la de carga.

## ⚠️ Nota de merge (vale para los 5 branches del repo)

`cosechador` tiene ahora **cinco branches nocturnos** (07-18, 08-11-b, 08-14,
08-16 y este) y **los cinco salen de `main` y los cinco agregan secciones a
`PROGRESS.md` y `QUE_FALTA.md`**. Van a conflictuar entre sí, pero son
**conflictos de añadido contra añadido**: se resuelven quedándose con los dos
lados. Orden sugerido, del más viejo al más nuevo: **07-18 → 08-11-b → 08-14 →
08-16 → 08-23-b** (este último cita a los dos del medio). Lo dejé escrito también
en el `QUE_FALTA.md` del branch.

## Próximo paso (para Matías, de día)

1. **Mergear los cinco branches en ese orden.** `main` de cosechador tiene hoy
   0 líneas de análisis y hay cuatro noches de trabajo esperando afuera.
2. **Leer D17 y decidir si la comprás.** Es la decisión que ordena el ensayo, y
   la escribí para que se pueda revertir con datos, no con opiniones.
3. **Cuando se compre y se arme: el ensayo de la Fase 2 son 30 minutos con una
   planilla, no una noche.** Anotar la tensión cada 5 min. Si la serie sale
   lineal, D17 se revierte — y ahí hay algo más interesante para entender.
4. **Drift menor que vi y no toqué:** `DECISIONS.md` **D16 dice «No usar git
   (todavía)»** y el repo está en git desde el 2026-07-07. Es una línea, es de
   @cronista, y no la metí acá para no mezclarla con la decisión técnica.
