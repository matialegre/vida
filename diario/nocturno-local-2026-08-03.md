# Nocturno local — 2026-08-03

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (P0 — "TERMINARLO PRIMERO, antes del trabajo Dreyfus").
**Branch:** `nocturno/local-2026-08-03-registro-sd-contabilidad` (pusheado, commit `e31820d`).

## Tarea elegida y por qué

Datalogger no se tocaba desde el 07-26 y es el único repo donde **entró código nuevo de
día**: el commit `e611bc5` ("Fixes de auditoría: SD desacoplada en core 1 — `RegistroSD`,
cola RAM, cero bloqueo del muestreo"). Código fresco, sin merodear, en el camino exacto
del DoD del proyecto:

> *"Canal MPU + canal piezo **logueando a SD sin gaps** durante N horas"*

Los ítems de `QUE_FALTA` que quedan sin branch son hardware (benchmark uPy vs C con jitter
real, front-end piezo, alcance de campo) o refactors que el propio doc prohíbe hacer gratis
(#9). El único hueco de software puro y verificable offline es el **#5, Integridad SD** —
y ahí hay que tener cuidado: ya existen **3 branches** de `sd_integrity` (07-09, 07-15,
07-25). Los revisé: los tres analizan el **CSV post-mortem**, con la tarjeta ya en la PC.
**Ninguno mira el camino EN LA PLACA que produce ese CSV.** Ese es el hueco que tomé, y
además es el que estrena el código de día.

La pregunta concreta: cuando una muestra se pierde, **¿alguien se entera?**

## Qué hice

`tools/test_registro_sd.py` — **18 tests** (`unittest`, stdlib, sin hardware) sobre el
**código real** de `misiones/registro.py`. No es un modelo/espejo (no puede driftear):
stubbea `time` y `_thread` al estilo de `tools/test_ina219.py` y corre el `_hilo()`
**verdadero** de forma determinista — un gancho en `sleep_ms` corta el bucle cuando el
escritor queda ocioso, así se ejercita el drenaje real, el lock por lote y el `except`
real, no una reimplementación.

Lo que miden es una **ley de conservación**:

```
pusheadas == en_archivo + descartes + en_cola + INVISIBLES
```

Una muestra se puede perder en **tres** lugares y el nodo sólo ve dos:

| | Dónde se pierde | Contador | ¿En vivo? | Rastro en el CSV |
|---|---|---|---|---|
| A | el lazo se atrasa: nunca se lee | `gaps` | sí (frame LoRa) | `seq` **contiguo**, salta `t_ms` |
| B | cola llena: se lee y se descarta | `descartes` | sólo por serie | **hueco de `seq`** |
| C | `write_line` da False o lanza | **ninguno** | **no** | hueco de `seq` |

`INVISIBLES` = el caso C, y es de donde salen casi todos los hallazgos.

## Hallazgos (con test que los demuestra — NO corregidos, generator ≠ evaluator)

- **H1 — el grande: con la SD muerta, el nodo se ve perfectamente sano.**
  `SDLogger.write_line` (`nodo.py:213`) devuelve `False` en sus tres modos de falla (no
  monta, no abre archivo, la escritura tira excepción → `_close()`). `_hilo` hace
  `if self.sd.write_line(linea): self.escritas += 1` y **ya sacó la línea de la cola**: el
  `False` no incrementa nada y la muestra desaparece. Si la tarjeta se sale *después* del
  arranque (el aviso `⚠️ SIN SD` sólo se imprime una vez, en `run()`), el print de cada 5 s
  dice `gaps=0 cola=0 desc=0` — impecable — mientras **no escribe absolutamente nada**.
  `escritas` sí lo notaría, pero no se imprime en ninguna de las dos misiones.
- **H2 — una excepción se traga el resto del lote.** El `except` de `_hilo` envuelve al
  `for` completo: si la línea 10 de 100 lanza, las 90 restantes se pierden sin reintento
  y el `flush()` queda salteado (lo ya escrito tampoco se sincroniza).
- **H3 — `cerrar()` vuelve con el último lote en vuelo.** Espera a que `self.cola` quede
  vacía, pero la cola **ya está vacía** mientras el escritor tiene el lote en la mano
  (`_tomar_lote` se lleva la lista entera). El llamador sigue con `lanzar(cfg)` → selector
  → **`machine.reset()`**: hasta 600 muestras (≈1,8 s) nunca llegan a la tarjeta. Es el
  *"apreto el botón para cambiar de misión y pierdo el último segundo"*.
- **H4 — las misiones ignoran el retorno de `push()`** (`mision_baja.py:159`,
  `mision_media.py:213`): el descarte no marca el CSV ni enciende nada en el momento.
- **H5 — el resumen LoRa reporta `gaps` pero no las pérdidas de SD.** El frame
  `RV1|…|BAJA,…,gaps=%d` es el **único canal en vivo** de la fase de instalación y lleva
  sólo el contador A: un nodo con la SD muerta transmite `gaps=0` y parece sano. En fase
  campaña LoRa se apaga y no queda **ningún** canal.
- **H6 — el colchón real es 1,80 s, no los "2-3 s" del docstring.** `mision_media` corre a
  `fs_real = 1000//(1+div) = 333 Hz`, no 300 → `600/333 = 1,80 s`. Un stall de FAT de 2 s
  —dentro de lo que el propio docstring promete absorber— ya descarta 66 muestras.
- **H7 — el descarte tira la muestra NUEVA, no la vieja:** durante un stall el CSV conserva
  el pasado y pierde justo la ventana del evento. Decisión de diseño legítima, pero no está
  escrita en ningún lado.
- **H8 — los dos modos de pérdida dejan rastros OPUESTOS en el CSV** (A deja `seq`
  contiguo y salto de `t_ms`; B/C dejan hueco de `seq` con `t_ms` contiguo). Un analizador
  que mire **una sola** columna se pierde la mitad. → input directo para las tools de
  `sd_integrity` de los 3 branches previos: deben cruzar `seq` **y** `t_ms`.

**8 tests `test_ok_*`** fijan lo que hoy anda bien y no se debe romper: `push()` no toca la
SD ni el SPI (el fix que motivó el componente **funciona**), el lock se toma una vez por
lote (si no, LoRa quedaría hambreado), hay `flush()` por lote, y una campaña simulada de
60 s a 333 Hz con stalls periódicos de 1 s no pierde una sola muestra.

Fixes candidatos escritos en `docs/registro-sd.md` (contador `fallos` para H1; `try`
adentro del `for` para H2; flag `escribiendo` + retorno de `cerrar()` para H3; `desc=`/`perd=`
en el frame RV1 para H5; `MAX_COLA=800` para H6 — **midiendo RAM antes**). **Ninguno
aplicado:** son cambios de firmware que se confirman en banco.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-03-registro-sd-contabilidad
python -m unittest tools.test_registro_sd -v   # -> Ran 18 tests, OK
python tools/test_misiones.py                  # -> 20 OK, 0 fallos (regresión intacta)
```

## Qué quedó sin verificar (necesita hardware)

- El hilo escritor **real** en el core 1 del RP2350: el test corre `_hilo()` determinista en
  un solo hilo. Las carreras reales core 0 ↔ core 1 (y el costo del GIL de MicroPython)
  sólo se ven en la placa. H3 en particular es una carrera: el test demuestra que la
  **ventana existe**, no con qué frecuencia se gana.
- La latencia real de la FAT sobre la SD física — de ahí sale si 1,80 s de colchón alcanzan.
- La RAM real de la cola: 600 líneas × **70 bytes medidos** = 41 KB de caracteres (el
  docstring dice ~45 KB, correcto), pero en MicroPython cada `str` carga overhead de objeto
  → el costo real está más cerca de 65-75 KB. **Medir con `gc.mem_free()` antes de subir
  `MAX_COLA`.**
- La prueba de N horas continuas del DoD.

## Estado

- Branch `nocturno/local-2026-08-03-registro-sd-contabilidad` pusheado (1 commit, `e31820d`).
- `QUE_FALTA.md` de datalogger: ítem **#5** anotado EN BRANCH (no duplica los 3 branches de
  `sd_integrity`: aquellos son post-mortem del CSV, éste es el camino en la placa).
- 4 repos intactos salvo el branch de trabajo; datalogger volvió a `main` limpio.
  `data/field_captures` de galgas no tocado. Ningún `misiones/` borrado ni movido.
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de anoche:
  `agentes/{esquematico,pcb}.md`, `dominios/{diseno,esquematico,firmware,hardware,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`, + sin trackear `agentes/diseno3d.md` y `dominios/diseno3d.md`).
  **No los toqué ni los commiteé** — no es trabajo mío. Matías: commitealos, o la rutina
  cloud va a chocar en el próximo `git pull`.
- La cola de merge suma **35 branches**. El tooling de drenaje (`tools/merge_queue_status.py`
  + `tools/resolve_doc_conflicts.py`) sigue listo y sin usar: falta la sesión humana.
