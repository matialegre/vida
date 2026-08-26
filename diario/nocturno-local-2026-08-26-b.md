# Nocturno local — 2026-08-26 (segunda pasada, "-b")

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (**RuView** — P0, "terminarlo primero, antes del trabajo Dreyfus").
**Branch:** `nocturno/local-2026-08-26-b-la-rafaga-que-ensordece` (pusheado, `85aed9d`).
**Sale de:** `main` (`e611bc5`). **No depende de ningún otro branch nocturno** — es el único que toca `firmwares/pico2w-node/nodo.py`.

## TL;DR

> **El nodo se apagaba dos segundos cada quince, y nadie lo había anotado.**
> No solo dejaba de medir: dejaba de **escuchar la malla**. Y el hueco que dejaba
> en la SD era indistinguible de un archivo sano.

Cada `fft_period_s` (15 s por defecto), `tick()` llamaba a `capture_and_send()`, y
esa función paraba el lazo entero:

| | ms |
|---|---|
| captura: 256 muestras a 1 kHz, espera activa en µs | 256 |
| envío: 8 chunks × (~200 ms de aire SF7 + `sleep_ms(25)`) | 1800 |
| **el lazo detenido, de un saque** | **~2056** |

Durante esos ~2 s no corre **nada** de `tick()`: no se muestrea el MPU (~41 muestras
a `mpu_hz=20`), no se escribe la SD, no se lee la batería, y —lo que nadie había
dicho— **no se llama `lora.poll()`**: el nodo está **sordo**, y los frames de la
malla que tendría que repetir en esa ventana se pierden sin más. **El 13,7 % del
tiempo el nodo no es un datalogger.**

Y el hueco era **invisible**: el CSV de la SD queda con `seq` contiguo y un salto en
`t_ms`. Nada dice "acá estuve ciego". Un *"sin gaps durante N horas"* declarado sobre
ese archivo es un cheque contra un agujero que nadie contó.

## Tarea elegida y por qué

Por rotación tocaba datalogger o cosechador (los más viejos: 08-24 y 08-23-b;
frioseguro se hizo hace unas horas en la primera pasada de hoy, galgas el 08-25).
**Desempató la jerarquía**: cosechador es P2 y todo lo que le queda está bloqueado
por la compra — sus cinco branches ya agotaron el análisis offline; no hay tarea
nueva ahí que no sea inventar trabajo. Datalogger es **P0** con orden explícita de
Matías de terminarlo antes del trabajo Dreyfus.

Dentro del repo seguí el patrón que viene funcionando: **no abrir una auditoría
nueva, tomar un pendiente ya nombrado con su evidencia.** Y había uno esperando, el
único que las dos últimas noches de datalogger dejaron explícitamente sin cerrar:

> *"Sigue abierto y sigue siendo de arquitectura: **B9**, la FFT automática que
> bloquea 1–3 s."* — `docs/fase-prod.md`, 2026-08-24

Con esta conclusión colgando de él: **`gaps=0` no se puede cumplir con esta
arquitectura, gane MicroPython o gane C** — o sea, B9 estaba tapando el **bloqueante
#1 del DoD** (la decisión MicroPython vs C) *y* el **#5** (integridad SD sin gaps).
Las auditorías del 08-08 y el 08-24 lo midieron y lo nombraron bien; lo que faltaba
no era más análisis, era el código. Eso es este branch.

## Qué hice

### 1. El envío deja de bloquear

`send_burst()` era un `for` cerrado sobre los chunks con `sleep_ms(20)` de reintento
y `sleep_ms(25)` de espaciado adentro. Se parte en dos:

- **`queue_burst(...)`** — agenda y vuelve. No manda nada.
- **`service_burst()`** — manda **como mucho un chunk**, y solo si venció su deadline.
  Se llama desde `tick()` al lado de `lora.poll()` y `lora.service()`, que ya usaban
  ese mismo patrón de "un ítem por tick".

Los sleeps se vuelven deadlines. **El aire se espacia igual que antes** — lo que
cambia es que en el medio el lazo corre.

**El protocolo RV1 no cambia y el gateway no se toca**: mismo frame, mismo orden,
mismo `CH=32`, mismos 4 reintentos por chunk. Hay un test que compara el frame
carácter por carácter contra el formato viejo, justamente para que un merge no lo
mueva sin querer.

### 2. La captura sigue siendo ciega, pero deja de ser invisible

La captura **no se puede repartir** — es la adquisición a 1 kHz, es el dato que la
ráfaga existe para tomar. Se queda. Lo que cambia es que ahora **se cuenta**:
`burst_gaps / burst_gap_ms / burst_gap_max / burst_skipped` en `status()`, más un
evento `{"e":"burst_gap","t":...,"seq":...,"ms":...}` por USB con el `seq` exacto
donde arranca el salto. **El hueco del CSV ahora tiene un recibo.**

Eso además arregla el DoD, que pedía algo imposible: deja de ser *"sin gaps"* y pasa
a ser lo que corresponde — **gaps declarados, acotados y medidos**.

Y al volver de la ventana ciega se **resincronizan** `next_sample` y `next_sd`, en
vez de intentar recuperar 41 muestras atrasadas a máxima velocidad (que sería un
segundo transitorio arriba del primero).

### 3. No se captura si la anterior sigue en el aire

`capture_and_send()` pregunta `burst_busy()` **antes** de capturar. Lo caro no es
encolar de más: es pagar 256 ms de espera activa por una ráfaga que no se va a poder
mandar.

### Resultado

| | antes | ahora |
|---|---|---|
| peor racha continua sin `tick()` | **~2056 ms** | **256 ms** — la captura |
| bloqueo por chunk | — (todo junto) | ~200 ms, **lo mismo que un TX de telemetría normal** que el lazo ya paga cada `lora_period_ms` |
| `lora.poll()` durante la ráfaga | 0 veces | entre cada chunk |
| el hueco en el CSV | invisible | contado, con `seq` y ms |

**Sin exagerar:** esto no deja al nodo libre de huecos. Cada `_tx` sigue bloqueando lo
que dura el frame en el aire. Lo que hace es bajar la peor racha **8×**, no introducir
ninguna clase de bloqueo que el lazo no pagara ya, y dejar el resto **medido**.

## Un hallazgo nuevo que salió al reescribir el chunker (y que NO arreglé)

Armando el frame chunk por chunk se puede medir cuánto ocupa. **Se pasa de 255 bytes:**

```
cabecera "RV1|P1|GW|1000001|3|B||"       23 B
prefijo  "1 0 8 1000 z 16384 "           23 B
32 valores de hasta 6 chars ("-32768")  192 B
31 comas                                 31 B
                                        -----
                                        269 B
```

`SX127x.send()` hace `self._write(REG_PAYLOAD_LEN, len(data))` y **ese registro es de
8 bits**: 269 entra como 13. El frame no sale "un poco cortado", sale con un largo
equivocado y se pierde entero.

Lo que lo hace feo: los valores llegan a 6 caracteres cuando la aceleración es
grande — **justo cuando hay un golpe fuerte, que es exactamente para lo que existe la
ráfaga**. Pérdida silenciosa y dependiente del dato.

**No lo arreglé a propósito.** El arreglo real es bajar `CH` de 32 a ≤29, y `CH` está
hardcodeado **también en el gateway** (`esp32_dashboard.ino`, `handleBurst()`:
`const int CH = 32; int off = seq * CH`). Cambiarlo de un solo lado desparrama las
muestras en el buffer del gateway. Es un cambio coordinado de dos firmwares, uno de
ellos ESP32 que hay que compilar y flashear — no es trabajo de una noche sin banco, y
meterlo acá habría contaminado un cambio que ahora es verificable solo.

Lo que sí puse es el **guard**: si un frame se pasa de `LORA_MAX_PAYLOAD`, no se
manda — se saltea, se cuenta en `burst_oversize` (visible en `status()`) y se imprime.
Cero cambio de protocolo, y la pérdida deja de ser silenciosa. Queda anotado como
**QUE_FALTA #14**.

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-26-b-la-rafaga-que-ensordece

python -m unittest tools.test_rafaga_no_bloqueante -v      # 26 tests, todos verdes
python -m unittest discover -s tools -p "test_*.py"        # suite del repo

# volver a donde estaba (te lo dejé como lo encontré):
git checkout nodo-gimap/wifi-y-flasheo-2026-08-24
```

Los tests **no copian** el firmware: lo extraen **por AST** de `nodo.py` y lo corren
contra un reloj falso y una radio falsa con costos declarados en el archivo — si el
firmware cambia, los tests corren sobre el cambio. Hay guardas explícitas contra la
regresión más fácil: que alguien vuelva a meter un `sleep_ms`, un `for` dentro de
`service_burst`, o el `send_burst` viejo en un merge.

**Y muerden:** corrí **14 mutaciones** sobre `nodo.py` (no avanzar `seq` tras un TX
exitoso, no abandonar nunca un chunk, espaciado a 0, no chequear la ráfaga en vuelo,
guard de 255 desactivado, no resincronizar, no limpiar `burst_tx`, `CH` 32→40, …) y
**ninguna sobrevive**.

> Nota de higiene: la primera corrida de mutación se colgó porque un `while` del
> propio test no tenía cota, y el script murió dejando `nodo.py` mutado. Lo detecté,
> lo restauré, le puse la cota al test y volví a correr. Lo digo porque el archivo
> estuvo unos minutos con una mutación adentro; lo commiteado está verificado limpio.

## Qué quedó SIN verificar (necesita hardware)

Nada corrió en un Pico. Pendiente de banco, en orden:

1. **El número que cierra B9**: con `sd_interval_s=0` y `mpu_hz=20`, el CSV tiene que
   mostrar **un solo** salto de `t_ms` de ~256 ms por ráfaga, no uno de ~2 s.
2. Que el `{"e":"burst_gap",...,"ms":N}` que sale cada 15 s diga **~256**. Si dice
   mucho más, la captura cuesta más de lo modelado y el modelo está mal, no el código.
3. Que el espectro siga llegando **completo** al gateway (`[vib] P1 rafaga N
   completa`). Si aparecen ráfagas incompletas donde antes llegaban enteras, el
   espaciado de 25 ms no alcanza con el lazo corriendo en el medio → se sube el
   deadline, **no** se vuelve al `for`.
4. `st`: `burst_chunk_lost`, `burst_oversize` y `burst_skipped` en 0 en operación
   normal. Si `burst_oversize` sube, apareció el bug del frame de 269 B en la vida
   real y sube la prioridad de #14.
5. Los ~200 ms de aire por chunk son **calculados** (SF7/BW125/CR4-5, ~180 B), no
   medidos.

## Estado del repo y notas de merge

- Branch pusheado a `origin`. Además dejé un **puntero en `main`** (`9c63a2b`,
  solo `QUE_FALTA.md`, sin tocar código) como las noches anteriores.
- **`QUE_FALTA.md` actualizado**: bloqueante #1 con el `EN BRANCH ... pendiente de
  merge`, y **#14 nuevo** con el hallazgo del frame de 269 B.
- Al mergear con `nocturno/local-2026-08-08-fidelidad-benchmark` y
  `...-08-24-fase-prod`: `check_benchmark_fidelity.py` detecta B9 buscando
  `capture_and_send()` dentro de `tick()`. **La llamada sigue ahí** (la captura sigue
  bloqueando), así que el detector no se rompe — pero su mensaje habla de un
  `send_burst()` que ya no existe. **Actualizar el texto y bajar B9 de error a info**,
  con el número nuevo (256 ms, no 1–3 s).
- Dejé el repo en el branch donde lo encontré (`nodo-gimap/wifi-y-flasheo-2026-08-24`)
  y **no toqué** el trabajo de día sin commitear que hay ahí (`firmwares/nodo-gimap/`
  y `visor.log`, ambos fuera de git). Sigue igual que anoche: hay trabajo de día
  viviendo fuera del control de versiones.

**Documento largo con todo el detalle:** `docs/rafaga-no-bloqueante.md` (en el branch).

---

*(No pude anexar el resumen a `scripts/turno_noche_log.txt`: el archivo está tomado
por el wrapper que corre este turno — `Device or resource busy`. El resumen completo
es este documento.)*
