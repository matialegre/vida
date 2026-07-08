# PROTOCOLO DE CALIBRACIÓN — galgas Dreyfus (2026-07-08)

> Problema real (Matías): las 2 galgas NO son iguales, y los 2 INA333 tampoco (ganancias distintas, offsets distintos). La lógica de alerta compara canal A vs canal B → si no están calibrados igual, A vs B miente. Hay que calibrar **espectacular** para llegar a la planta (Rosario/campo) con todo calibrado e **in situ verificar que las muestras son buenas**.

## El objetivo en una frase
Que una MISMA deformación física dé el MISMO número en el canal A y en el B, de forma repetible, verificable en el lugar sin instrumental de laboratorio.

## Modelo de cada canal
`valor_fisico = K_canal · (adc_raw − offset_canal)`
Cada canal (A y B) tiene su **propio K** (corrige ganancia distinta de galga+INA) y su **propio offset** (corrige el cero distinto). Se persisten en NVS/EEPROM por canal (como ya hace galgas-supabase).

## Las 3 fuentes de diferencia entre canales (y cómo las mata cada paso)
1. **Offset del INA333 + desbalance del puente** → paso OFFSET (tara).
2. **Ganancia distinta (resistor de ganancia del INA + gauge factor de la galga)** → paso SPAN con referencia conocida.
3. **Deriva térmica** (offset del INA y de la galga con temperatura) → medir temperatura y/o half-bridge autocompensado.

## ⭐ El método pro: CALIBRACIÓN POR SHUNT (shunt calibration)
Es el estándar industrial para galgas y resuelve TODO sin pesas ni banco: **se pone en paralelo un resistor de precisión conocido (R_cal) sobre un brazo del puente**, lo que produce una **deformación simulada CALCULABLE** (ε_sim depende de R_gauge, R_cal y el gauge factor). Como es un número exacto y repetible:
- Se aplica el MISMO R_cal a los dos canales → ambos deben leer la MISMA ε_sim → se ajusta K de cada canal para que coincidan.
- Se puede llevar al campo (un resistor + un relay/mosfet o un jumper): **en la planta apretás el shunt-cal y verificás que A y B leen lo esperado → prueba que toda la cadena (galga, INA, ADC, constantes) sobrevivió el transporte y el montaje.** Si ambos dan el valor esperado → las muestras son buenas. Ese es el "verificar in situ" que pediste.

## Procedimiento paso a paso (banco GIMAP)
1. **Estabilización térmica:** dejar el sistema 10-15 min encendido antes de calibrar (el INA333 y el puente derivan al arrancar).
2. **OFFSET / tara (por canal):** puente en reposo (sin carga) → promediar N muestras (ej. 500) del adc_raw → ese es `offset_canal`. Guardar. Repetir para A y B por separado.
3. **SPAN por shunt-cal (por canal):** activar R_cal sobre el brazo → medir adc_raw → calcular ε_sim teórico → `K_canal = ε_sim / (adc_raw − offset_canal)`. Guardar. Repetir A y B.
   - (Alternativa sin shunt: aplicar una deformación/carga física conocida idéntica a ambos — más engorroso; el shunt es superior.)
4. **Verificación cruzada A=B:** con las K/offset cargadas, aplicar el shunt-cal (o la misma deformación) a AMBOS → confirmar que A y B dan el MISMO valor dentro de tolerancia (ej. ±2%). Si no, revisar.
5. **Linealidad (opcional pero recomendado):** 2-3 puntos de shunt-cal distintos (varios R_cal) → confirmar que la respuesta es lineal en el rango de trabajo. Si hay alinealidad, tabla o ajuste.
6. **Registro de temperatura:** guardar la temp durante la calibración; en campo, comparar y compensar si difiere mucho.
7. **Persistir en NVS:** K_A, offset_A, K_B, offset_B, R_cal usado, ε_sim, temp_cal, fecha. Que sobreviva power-cycle (regla ya conocida del sistema).

## Procedimiento IN SITU (en la planta, antes de confiar en los datos)
1. Montar, alimentar, estabilizar térmicamente.
2. **Disparar el shunt-cal en A y en B** → verificar que cada uno lee su ε_sim esperado (±tolerancia). ✅ = cadena sana post-transporte/montaje.
3. **Auto-offset in situ:** re-tarar el cero con el eje en reposo real (el montaje puede meter una pretensión distinta a la del banco).
4. Recién ahí, empezar a confiar en la comparación A vs B para detectar el golpeteo/rotura de cadena (0.33 Hz).

## Qué hay que agregar al hardware para que esto ande
- **Resistor de shunt-cal + conmutación** (relay pequeño o MOSFET) por canal, comandable por firmware. Barato, y es lo que hace el sistema "calibrable en campo con un comando".
- INA333 con resistor de ganancia de precisión (1% o mejor); idealmente **el mismo valor en ambos canales** (aunque las galgas difieran, arrancás más parejo).
- Sensor de temperatura (el MPU ya da temp; o uno dedicado cerca de la galga).

## Relación con lo existente
galgas-supabase ya tiene calibración de 3 etapas + auto-offset persistido en NVS y CSVs de campo reales (`data/field_captures`, sample #6 mencionado por Matías → analizar). Este protocolo lo FORMALIZA y le agrega el **shunt-cal** (verificación in situ) que es lo que faltaba para llegar calibrado y confiar en las muestras en la planta.

Dominios: @muestreador (adquisición + constantes), @esquematico (shunt-cal + INA de precisión), @firmware (comando de cal + persistencia), @verificador (que A=B se pruebe, no se asuma).
