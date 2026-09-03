# Nocturno local — 2026-09-03

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (**P0** — parada Dreyfus de octubre, y con
el frente comercial abierto: reunión con Juliano el viernes 4-sep).
**Branch:** `nocturno/local-2026-09-03-el-adc-que-no-se-apaga` (pusheado, `fcaf2b9`).
**Sale de:** `main` (`7e67985`, "Rev D cerrada"). **No depende de ningún otro branch
nocturno y no colisiona con ninguno**: es el único de los 29 abiertos de galgas que
toca `firmware/nodo_galga_v3/`, que nació anteanoche. Modifica **una función** de
`energia.cpp` y agrega 2 archivos.
**No toca SQL, ni `data/field_captures/`, ni nada del ESP32.**

---

## TL;DR

> **El sondeo de arranque en frío prendía el ADC del ATmega y nadie lo apagaba.
> El nodo se iba a dormir 30 s por sondeo con el convertidor y el bandgap
> polarizados — cientos de µA contra un reposo de 29 µA y contra los ~0,19 mA
> con los que el diodo recarga el supercap. La rutina que existe para esperar a
> que el capacitor cargue se lo estaba comiendo mientras esperaba.**

`vccProbePreparar()` abre el ADC:

```c
power_adc_enable();
ADMUX  = _BV(REFS0) | 0x0E;                    /* AVcc ref, bandgap adentro */
ADCSRA = _BV(ADEN) | _BV(ADPS2) | _BV(ADPS0);
```

y no lo cierra nunca. El otro consumidor de ADC del firmware,
`energiaLeerVbatMv()`, sí lo hace y con las dos mitades (`ADEN` y el bit de PRR).
Un grep sobre `main` da **dos `power_adc_enable` y un solo `power_adc_disable`**:
el que falta es el del sondeo. Grepeado, no supuesto.

El ATmega **no apaga el ADC solo** al dormir. Datasheet del ATmega328P §14.5:
*"If enabled, the ADC will be enabled in all sleep modes. To save power, the ADC
should be disabled before entering any sleep mode."* Y la referencia interna
sigue encendida mientras el ADC la pida, así que quedan polarizados los dos.

**Por qué es grave justo en ese camino y no en cualquier otro:**

| Estado | Duerme | ADC prendido |
|---|---|---|
| `EST_ARRANQUE_FRIO` | 30 s **por sondeo, hasta converger** | sí |
| `EST_ARRANQUE_CONFIRMA` | 120 s | sí |

`EST_ARRANQUE_FRIO` se entra con `MCUSR & _BV(PORF)` — **power-on reset, o sea el
momento exacto de la instalación** — y se repite hasta que la caída del riel en
una TX a +20 dBm baja del 1,5 %. Según lo que cerraste anteanoche eso es típico
~75 s y **hasta ~216 s con una celda pasivada de estante, que es el caso normal**.
Todo ese rato dormía con el ADC prendido, y el consumo parásito es **del mismo
orden que la única corriente de recarga que tiene el nodo**. En el mejor caso el
arranque en frío tarda bastante más de lo que dicen tus números; en el peor no
converge y el nodo queda sondeando para siempre sin llegar a medir.

Es la **cuarta** vez que aparece este patrón en el nodo v3 en tres días —después
del fusible, de la ráfaga perdida y del checklist que daba falso "pasa"—: **algo
que compila, no cambia ninguna trama, anda perfecto en el banco y sólo falla
arriba del REDLER.** Y esta vez le pega justo a la función estrella de anteanoche,
la que iba a hacer que *"el instalador ya no espere, mida ni interprete"*.

## Por qué esta tarea y no otra

1. **Jerarquía + calendario.** PLATA fue el turno de anoche (frioseguro,
   `09-02-b`) y el anterior datalogger (`09-02`). Galgas es P0 de octubre y
   además tiene la reunión con Juliano **el viernes 4**: lo que se toque acá
   esta semana pesa doble.
2. **Es código de anteanoche que nadie auditó.** `firmware/nodo_galga_v3/` se
   escribió el 02-09 junto con la rev D. Ninguno de los 29 branches nocturnos
   abiertos de galgas lo toca (todos son ESP32 / backend / SCADA). Cero riesgo
   de colisión, cero trabajo repetido.
3. **Software puro, verificable sin banco**, y encima con toolchain ya instalado
   (arduino-cli 1.4.1 + `arduino:avr` 1.8.7): compilación real, no "compilaría".
4. **Ataca la fila del medio del camino crítico.** No arregla nada del ruteo ni
   de la compra del lunes: arregla el firmware que va a correr en esas placas.
5. Miré antes los otros tres repos: datalogger y frioseguro los trabajé anoche y
   anteanoche, y cosechador sigue bloqueado por la compra (sin firmware que
   auditar).

## Qué hice

**Un solo cambio de comportamiento, en el chokepoint** (`energia.cpp`):

```c
static void adcApagar(void)
{
  ADCSRA &= (uint8_t)~_BV(ADEN);
  power_adc_disable();
}

void dormirSegundos(uint16_t s)
{
  adcApagar();
  while (s > 0) { ... }
}
```

Tres decisiones, y las tres son de tu propia doctrina:

- **Va en `dormirSegundos()`, no en el que prende el ADC.** Es el único lugar por
  el que pasan **todos** los sleeps del nodo (ciclo, espera de recarga R3, espera
  de ráfaga, los dos sondeos, degradado y fusibles-mal). Exactamente el mismo
  razonamiento que escribiste para `rafagaPermitida()`: *el guard va en el punto
  único por el que pasan todos, para que un consumidor nuevo no lo saltee por
  olvido*. La versión anterior confiaba en que cada usuario del ADC se acordara,
  y el usuario más nuevo no se acordó.
- **No se restaura al despertar.** Los dos consumidores reescriben `ADCSRA` y
  `ADMUX` enteros antes de convertir, así que apagar acá no le rompe el estado a
  nadie.
- **Orden `ADEN` → PRR.** Al revés, `PRADC` le corta el reloj al ADC y `ADEN` ya
  no se puede limpiar: queda congelado prendido.

Y el harness para que no vuelva: **`tools/check_sleep_adc.py`**, en el estilo de
`check_pinout_nodo_v3.py` / `check_ota_rescue_wiring.py`. Vigila cuatro
invariantes (A: el chokepoint apaga antes del lazo y en el orden correcto · B:
no hay `SLEEP_MODE_PWR_DOWN` fuera de `dormirSegundos()` · C: no se duerme entre
`vccProbePreparar()` y la lectura de la caída, que ahora sería medir basura · D:
todo el que prende el ADC lo configura entero, que es lo que permite apagar sin
restaurar). Tira comentarios antes de buscar, porque en este firmware los
comentarios nombran las funciones que explican y un check ingenuo daría verde con
el código borrado.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-09-03-el-adc-que-no-se-apaga

python tools/check_sleep_adc.py                 # 17 checks, 0 fallas
python tools/check_sleep_adc.py --mutantes      # 4/4 mutantes muertos
python tools/check_pinout_nodo_v3.py            # sin regresión

arduino-cli compile --fqbn arduino:avr:pro:cpu=8MHzatmega328 \
  --build-property build.f_cpu=4000000L \
  --build-property "compiler.cpp.extra_flags=-DMCU_DIP28=1" \
  --warnings all firmware/nodo_galga_v3
```

Resultados obtenidos acá, esta noche:

- `check_sleep_adc.py`: **17 checks, 0 fallas**.
- `--mutantes`: **4/4 muertos**. El primero (`el bug original: se saca la apagada
  del chokepoint`) reproduce el estado de `main` y el check **reprueba** — o sea
  que no es un test que acompaña al arreglo, es uno que habría cazado el defecto.
- `check_pinout_nodo_v3.py`: OK, sin regresión.
- Compilación **real** de las dos variantes de encapsulado, sin un warning:
  **5856 B (19 %) DIP-28** y **5840 B TQFP-32** contra **5836 B** de `main`.
  Costo: **+20 bytes de flash, 0 de RAM**.
- Y porque en este repo *código escrito no es código corriendo* (la lección de
  `g_mcusr_boot`, que el linker se llevaba puesta), miré el **desensamblado**:

```
00000544 <_Z14dormirSegundosj>:
 54e: lds  r24, 0x007A   ; ADCSRA
 552: andi r24, 0x7F     ; limpia ADEN
 554: sts  0x007A, r24
 558: lds  r24, 0x0064   ; PRR
 55c: ori  r24, 0x01     ; PRADC
 55e: sts  0x0064, r24
 562: sbiw r28, 0x00     ; recién acá arranca el lazo de sleep
```

Las dos escrituras sobreviven a `-Os` y quedan **antes** del lazo.

## Qué quedó SIN verificar por falta de hardware

1. **Cuánto costaba de verdad.** La cifra "cientos de µA" sale del datasheet, no
   de esta placa. Amperímetro en serie con el nodo durmiendo, con y sin el
   arreglo. **Es la misma medición que ya debe `@energia`** para convertir la
   autonomía de 2,43 años de cálculo en dato: se hacen juntas.
2. **Cronometrar un arranque en frío real con celda pasivada**, antes y después.
   Es lo único que dice si el sondeo **no convergía** o sólo tardaba de más.
3. Nada de esto bloquea gerbers ni la compra del lunes.

## Hallazgo abierto que el branch NO toca (a propósito)

Los sondeos del arranque en frío transmiten a **+20 dBm sin pasar por
`rafagaPermitida()`**: `rafagaMarcarEvento()` se llama **sólo** en `EST_MEDIR`.
Cuando `EST_ARRANQUE_CONFIRMA` da `listo`, el nodo entra a `EST_MEDIR` con
`s_hubo_evento == false` y dispara medición + TX **pegada** a la TX de
confirmación: dos eventos seguidos, que es justo lo que `RAFAGA_MIN_S` = 120 s
existe para impedir. En el arranque en frío la pila es nueva y el capacitor acaba
de declararse cargado, así que probablemente no muerda — pero **quién decide eso
es `@energia` con la curva de recarga, no yo**. Lo dejé anotado en el doc y en
`QUE_FALTA.md`, sin cambiar comportamiento: es el mismo tipo de bypass del
chokepoint que el de este branch y merece su propia decisión, no un parche
nocturno.

## Al mergear

Merge limpio: `main` no tocó `firmware/nodo_galga_v3/` desde `7e67985`. Después
del merge conviene sumar `python tools/check_sleep_adc.py` al mismo lugar donde
ya corre `check_pinout_nodo_v3.py` antes de compilar.

## Archivos

- `firmware/nodo_galga_v3/energia.cpp` — **modificado** (+31 líneas: el helper,
  la llamada y el por qué).
- `tools/check_sleep_adc.py` — **nuevo** (read-only, sin nube ni hardware).
- `docs/adc-en-power-down.md` — **nuevo** (el defecto, el datasheet, el porqué
  del chokepoint, la evidencia y lo que falta de banco).
- `QUE_FALTA.md` — item **4b** en Bloqueantes, marcado EN BRANCH. Numerado "4b"
  y no "5" a propósito: el archivo referencia items por número (#5, #9, #11) y
  correr la numeración habría roto esas referencias.
