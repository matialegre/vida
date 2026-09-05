# Nocturno local — 2026-09-05

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (**P0 octubre**, y con el frente comercial
abierto: la reunión con Juliano fue ayer, viernes 4-sep, y hay cámaras
compitiendo adentro de Dreyfus).
**Branch:** `nocturno/local-2026-09-05-la-potencia-que-nadie-cambio`
(pusheado, `ee2908a`).
**Sale de `main` (`93c2aab`, "Bloque sensor ruteado a mano y bloqueado").**
**No toca SQL, ni `data/field_captures/`, ni nada del ESP32.**

---

## TL;DR

> **`CMD_SET_POTENCIA` contestaba que sí y no cambiaba nada. El firmware
> escribía la potencia pedida al radio al empezar el ciclo, y dos estados
> después la volvía a fijar con el escalón de energía — antes de transmitir. El
> valor se perdía sin que ninguna trama lo usara, y el comando se ecoaba igual.
> La prueba de alcance, que es para lo único que este comando existe, se corría
> entera a la potencia de siempre mientras el operador creía estar barriendo de
> 2 a 20 dBm.**

## Por qué esta tarea

Tres razones, en orden:

1. **Es la única mentira que quedaba en el downlink.** De los siete comandos,
   seis dicen la verdad: `NOP` ackea, `MODO_BANCO` cambia el ciclo, `SET_CICLO`
   persiste, `CEDULA` emite, `REBOOT` reinicia, y `SHUNT_CAL` **se rechaza a
   propósito** porque en la rev E.1 no hay llave que accionar. `SET_POTENCIA`
   era el séptimo, y era el que ecoaba OK sin hacer nada. El firmware tiene
   escrita tres veces la lección del 2026-08-28 —*"un NACK honesto vale más que
   un OK vacío"*, por las tres etapas de calibración que contestaban `ack=OK` sin
   hacer nada— y este comando la violaba en silencio.
2. **Pega justo donde está la presión comercial.** Lo que Dreyfus va a preguntar
   en las próximas dos semanas es si el nodo llega desde arriba del REDLER.
   `SET_POTENCIA` es la herramienta con la que se contesta esa pregunta, y hoy
   contesta con otra medición: un barrido de 2 a 20 dBm daba el mismo alcance en
   los diez puntos, porque las diez tramas salían a 17.
3. **Es 100 % software y se verifica sin hardware.** Cero dependencia de las 4
   mediciones que faltan para liberar gerbers.

No había ningún branch abierto tocándolo (los 30 de galgas: el único que toca
`firmware/nodo_galga_v3/` es el del 09-03, y toca `energia.cpp`).

## El agujero, y por qué nadie lo veía

`ejecutarComandoPendiente()` se ejecuta al empezar el ciclo, en `EST_MEDIR`:

```c
case CMD_SET_POTENCIA:
  if (arg < 2 || arg > 20) return 0x00;
  sx1278SetPotenciaDbm((int8_t)arg);      /* provisorio: NO persiste */
  break;
```

Dos estados después —`EST_MEDIR` → `EST_ESPERA_RECARGA` (30 s durmiendo) →
`EST_TX`— la primera línea de `EST_TX` era:

```c
sx1278SetPotenciaDbm(energiaPotenciaTx());   /* R2 unificado con C7b */
```

Las dos líneas son correctas por separado y las dos tienen su comentario
explicando por qué existen. El defecto está en el **orden**, que no se ve
leyendo ninguna de las dos: entre que el comando escribe y la trama sale, hay un
`dormirSegundos(30)` y un cambio de estado. Nadie lee las dos juntas.

**Y el `ack` tapaba el síntoma.** El comando volvía en `ack_eco` del uplink
siguiente, que es la única prueba de entrega que tiene el downlink. Desde el
receptor, un `SET_POTENCIA` que no hace nada y uno que funciona **se ven
idénticos**. Lo que cambia es el RSSI, que es exactamente el número que la
prueba de alcance está midiendo — o sea que el error se disfraza de resultado.

**Tercer disfraz:** los 17 dBm de `TX_DBM_PLENA` están cerca de los 20 del tope
del rango. Un barrido "de 2 a 20 dBm" que en realidad sale todo a 17 no da un
alcance absurdo: da uno **razonable y plano**. Es el tipo de dato que se anota
en la libreta y se cita seis meses después.

## Lo que salió al arreglarlo (y no estaba en el plan)

Escribir la regla como un módulo aparte hizo aparecer dos cosas que el fix
mínimo —mover una línea— habría dejado adentro:

**1. El sondeo del riel del self-trigger habría empezado a mentir.** El
firmware tiene un ensayo firmado por @energia el 2026-09-04 explicando que el
sondeo del self-trigger va **a la potencia de la TX real** y no a +20 dBm, con
dos motivos concretos (sondear más fuerte puede hundir el riel y perder el
evento; y diferiría eventos que sí habrían salido). Esa regla estaba escrita
como `sondearRiel(energiaPotenciaTx())` y hasta hoy eso *era* la potencia de la
TX real. En cuanto el override empieza a funcionar de verdad, deja de serlo: la
TX saldría con el override y el sondeo certificaría otra cosa. Ahora los dos
llaman al mismo `potenciaTxVigente()`, y el checker vigila que sigan iguales.

**2. El override tiene que vencer, y no es higiene.** Bajar la potencia por
comando puede dejar al nodo **inalcanzable por diseño**:

> el downlink usa como nonce anti-replay el `seq` de la trama que el receptor
> **acaba de escuchar** (C2.4). A un nodo que dejó de escucharse no se le puede
> mandar nada — **ni siquiera el comando que lo arreglaría**.

Un `SET_POTENCIA 2` mal medido, sin vencimiento, es una subida al REDLER con un
ISP. Con vencimiento es una hora de silencio. Es el mismo argumento por el que
`MODO_BANCO` sale solo por timeout, y acá es peor, porque el modo banco al menos
sigue transmitiendo.

## Qué se entregó

`firmware/nodo_galga_v3/potencia_tx.h` — **puro** (sin Arduino, SPI, `energia.h`
ni `sx1278.h`) e **incluido** por el `.ino`. No es un espejo: lo que se testea es
lo que se flashea. Mismo criterio que `medstats`, y que `sensor_fault_model.h` /
`temp_report_model.h` en FrioSeguro.

**Un solo lugar decide la potencia de la próxima TX** (`potenciaTxVigente()`), y
lo usan los dos que transmiten un uplink: `EST_TX` y el sondeo del self-trigger.
La cédula de `EST_TX_DIAG` sigue yendo a `TX_DBM_BACKOFF` a propósito (un nodo
con el BOD mal grabado es justo el que se resetea con su propio pulso de TX).

Tres reglas, ninguna cosmética:

| # | Regla | Por qué |
|---|---|---|
| 1 | **El back-off de energía (R2) le gana siempre al comando.** Se rechaza si llega con la pila fuera de `ENERGIA_PLENA`, y se cancela solo si la pila cae después | Si un comando por aire pudiera pisar el back-off, la barrera que evita que el nodo se resetee en su propio pulso a fin de vida no sería una barrera |
| 2 | **Vence a la hora** (`POT_TX_OVERRIDE_S 3600`) | El nodo inalcanzable de arriba |
| 3 | **`arg = 0` cancela** | Igual que `MODO_BANCO`; es la única forma de deshacer sin esperar la hora |

Que la regla 1 gane *después* de aceptado no es un "OK vacío": el comando **no se
acepta cuando no se puede cumplir** (no se ecoa → el receptor lo reintenta y
registra el fallo), y si gana más tarde es porque cambió el estado del nodo.

## Cómo verificarlo (comandos exactos, sin hardware)

```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-09-05-la-potencia-que-nadie-cambio

# 1) la lógica pura: 36 checks. Los 3 primeros bloques son REGRESIÓN
#    (fallan contra la lógica vieja)
g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_potencia_tx.exe tools/test_potencia_tx.cpp
./tools/test_potencia_tx.exe

# 2) el cableado + el harness que se auto-verifica
python tools/check_pinout_nodo_v3.py --mutantes

# 3) compila en las DOS variantes de encapsulado
arduino-cli compile --fqbn arduino:avr:pro:cpu=8MHzatmega328 \
  --build-property build.f_cpu=4000000L \
  --build-property "compiler.cpp.extra_flags=-DMCU_DIP28" \
  --build-property "compiler.c.extra_flags=-DMCU_DIP28" \
  --warnings all firmware/nodo_galga_v3
# idem con -DMCU_TQFP32
```

**Resultados obtenidos esta noche:**

- `test_potencia_tx.exe` → **36 checks, 0 fallos**, sin warnings.
- `check_pinout_nodo_v3.py --mutantes` → **OK** y **79/79 mutantes muertos**
  (eran 71: **+8 nuevos**). Los dos que importan: *"vuelve el defecto: EST_TX
  pisa el override de potencia"* y *"el override deja de vencer y el nodo puede
  quedar mudo para siempre"*. También se agregaron 5 reglas estáticas nuevas
  (que `EST_TX` no use `energiaPotenciaTx()` pelado, que el comando no le escriba
  al radio, que pase por `potenciaTxCmd()`, que pueda no ecoarse, y los tres
  invariantes de `potencia_tx.h`).
- Compilación **DIP-28 y TQFP-32**: exit 0, **sin warnings**, 8610 B = **28 % de
  flash**, 140 B = **6 % de RAM**.

Baseline antes de tocar nada: 71/71 mutantes, rc=0. O sea que las 8 muertes
nuevas son del trabajo de esta noche, no herencia.

## Qué queda sin verificar (pide hardware)

Cuatro escenarios de banco, ninguno largo, todos con el receptor mirando el RSSI:

1. `SET_POTENCIA 2` → el RSSI del receptor tiene que **caer de verdad**. Es la
   prueba de que el fix llegó al aire y no sólo a un `struct`.
2. `SET_POTENCIA 0` → vuelve al escalón en el ciclo siguiente.
3. Dejar pasar **una hora sin comandos** → vuelve solo (12 ciclos de 300 s).
4. Con la pila bajo 3150 mV (`ENERGIA_BAJA`), mandar `SET_POTENCIA 20` → el
   comando **no se ecoa**, y la TX sigue saliendo a 14 dBm.

## Anotado y NO tocado

- **Pedido a @comms** (es su contrato, no el mío): firmar o corregir la sección
  **C2.4.2** que el branch agregó a `hardware/COMMS_REV_D.md`. Cuando entre el
  NACK de C2.4.1, los motivos ya existen y no hay que inventar ninguno:
  `ARG_INVALIDO` (3) para el fuera de rango, **`ENERGIA` (5)** para la pila baja.
- **La trama no dice a qué potencia salió.** El receptor sabe qué comandó, pero
  no qué usó el nodo — y con la regla 1 esos dos números pueden diferir. Para un
  mapa de cobertura serio, la potencia real debería viajar. Eso **crece la trama
  y es contrato de @comms**, así que queda pedido, no hecho.
- **Drift en `QUE_FALTA.md` de galgas:** el pendiente del nodo v3 del 09-03 está
  **duplicado**, como **#3** y como **#4b**, con el mismo texto. Arreglarlo ahora
  garantizaba un conflicto con ese branch; se resuelve al mergearlo. [@cronista]

## Nota de merge

Sale de `main` (`93c2aab`). **Colisiona sólo con
`nocturno/local-2026-09-03-el-adc-que-no-se-apaga`, y sólo en
`tools/check_pinout_nodo_v3.py`**: los dos le agregan reglas y mutantes, en
bloques distintos del archivo. Es conflicto de añadido contra añadido → se
resuelve **quedándose con los dos lados**, y después `--mutantes` tiene que dar
`79 + 4 = 83/83`. En el `.ino` no hay colisión (el del 09-03 trabaja en
`energia.cpp`). Con el resto de los 30 branches abiertos de galgas, ninguna.
