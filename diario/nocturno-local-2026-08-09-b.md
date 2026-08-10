# Nocturno local — 2026-08-09 (2do turno, "-b")

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-09-b-cadena-medicion` (pusheado, commit `926b623`).

## Tarea elegida y por qué

El 1er turno de hoy fue a frioseguro (aislamiento entre clientes), el de ayer a
datalogger. Por rotación tocaba **galgas**, que no se toca desde el 08-07-b.

Repasé el `QUE_FALTA`: los 🔴 sin branch son hardware puro (#1 RX completo, #3
LiPo real, #4 reflashear B); de los 🟡, el #5, #6 y #8 ya los auditó el branch
del contrato de schema. Los 17 branches previos de galgas cubren vpp/umbrales,
energía, alertas, linaje, OTA, readme-drift, contrato de comandos, identidad de
binarios y contrato de schema.

**Ninguno mira la medición en sí.** Los contratos auditados hasta ahora son de
*forma*: qué columnas existen, qué comandos existen, qué binario es cuál. Falta
el de *significado*:

> **Del ADC crudo al número que pinta una card de rojo delante de Dreyfus,
> ¿todos los tramos están de acuerdo sobre qué significa ese número?**

```
ADC raw --(transformada de calibración)--> v --(agregados)--> v_pp
     --(umbral)--> in_alert --(POST)--> readings --(dashboard)--> card
```

Esa cadena está escrita **cuatro veces en tres lenguajes** —familia monolítica
(`ota_wm_pp`, la que está publicada en `redler/bins_ota/`), familia modular
(`esp_a/b_emisor` + `shared`), dashboard y migraciones— y **nadie las había
comparado**.

Lo elegí porque es la **precondición del ítem 🔴 #2** (validar con galga física
contra `field_captures`): antes de comparar contra el ground truth hay que saber
qué unidades tiene lo que se compara. Y porque el modo de falla de esta cadena
**no es un crash**: es un número creíble que significa otra cosa.

## Qué hice

**`tools/check_measurement_chain.py`** (stdlib, solo lectura, sin nube ni
hardware, no entra a `field_captures`). Auditor dirigido: modela la transformada
de cada familia, sus centinelas de min/max, de dónde sale `in_alert`, dónde vive
la calibración en NVS y qué umbrales están hardcodeados. Exit 0/1/2/3, `--json`,
`--fail-on`, `--root`, `--demo-sentinel`.

Lo que hubo que resolver:

- **El sampler modular tiene DOS lazos de agregación**, y el primero es el de
  `#ifdef DEV_SIMULATE_ADC` (señal sintética, sin ADC ni calibración). Agarrando
  ese, el checker concluye que **la familia modular no tiene transformada** —
  justo al revés de la verdad, y encima en la dirección que absuelve. Hay que
  blanquear la rama del `#ifdef` y quedarse con la real.
- **Una definición `static inline` en un header no es un uso.** Sin esa
  distinción, `nvsLoadCalK()` "tiene call sites" y el hallazgo más grave de la
  noche (H1) desaparece solo.
- **El centinela no se juzga por su valor sino por si acota el rango
  alcanzable.** `vmin=3.3` es un número perfectamente razonable… para la señal
  cruda. La regla correcta es "¿bracketea cualquier valor **calibrado**?".
- **Al hallazgo del centinela no alcanza con afirmarlo**: el tool trae un
  **oráculo numérico** (`burst_vpp`) que replica el lazo real y lo demuestra con
  números, con y sin el bug.

**`tools/test_check_measurement_chain.py` — 69 tests en 7 capas:** utilidades de
texto, clasificadores puros, extractores sobre fuentes sintéticas, **el oráculo
numérico**, un test por código de hallazgo con repos sintéticos armados en disco
(+ **control negativo**: un repo sano no dispara nada), la regresión sobre el
repo real y el CLI.

**`docs/measurement-chain.md`** — el análisis completo.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **2 transformadas · 7 umbrales hardcodeados · 6 comandos de
calibración · 3 fuentes de `in_alert` → 4 error / 3 warn.**

### H4 — `v_pp` puede reportar la DERIVA DC en vez de la vibración

Es el más caro porque **`v_pp` ES la alerta**. `ota_wm_pp.ino:807-808`:

```c
float vmin = 3.3f;
float vmax = 0.0f;
```

Ese par sólo es correcto si toda muestra cae en 0..3,3 V — el rango del **ADC
crudo**. La transformada `(v_raw - offset)*k` produce negativos **por diseño**
(centrar en cero es para lo que existe `autoffset`).

Modo de falla: la placa se autoffsetea en reposo; horas después el DC deriva
hacia abajo (térmica, no mecánica); todas las muestras corregidas quedan
negativas; `vmax` **se queda en 0.0** y `v_pp = |deriva|`. Con números
(`--demo-sentinel`, fijado por test):

```
deriva DC 50 mV, vibración real 14 mV  ->  v_pp reportado 57 mV
umbral ALERTA 40 mV  ->  alerta real: no | alerta reportada: SÍ
```

Tres cosas lo empeoran:

1. **En banco no se ve.** Recién autoffseteada, la señal cruza cero y los
   centinelas funcionan. El defecto aparece *horas después, en planta* — o sea,
   durante la parada.
2. **La evidencia para diagnosticarlo no se manda:** `v_min`/`v_max` se calculan
   y **no se postean**. Desde la nube no hay con qué distinguirlo de una alerta
   real.
3. **La familia modular no tiene el bug** (usa `±1e9`). Es exclusivo del
   firmware publicado.

Fix candidato: una línea (`±1e30f`, o arrancar con la primera muestra) + postear
`v_min`/`v_max`, que ya son columnas.

### H3 — `in_alert` no mira la señal en el firmware publicado

`ota_wm_pp.ino:1411`: `is_alert = (strcmp(PROFILE_NAME, "ALERTA") == 0)` — una
**constante de compilación**. O sea:

- binario `*-palerta` (existe: `3.6.3-palerta`) → **`in_alert = true` en TODAS
  las lecturas**, con la galga en reposo o rota igual → card roja permanente.
- binario `*-pnorm` / `*-palways` / `*-pmax` → **`in_alert = false` siempre**, y
  la única detección que queda es la comparación `v_pp > 40 mV` que hace **el
  navegador**, que sólo corre mientras alguien tiene la pestaña abierta.

La familia modular sí lo deriva de la señal (`v_pp > SELF_TRIGGER_VPP_V`). **Las
dos escriben la misma columna** y el dashboard la lee sin saber cuál corre.
La definición de "listo para octubre" dice *"con alertas visibles en el SCADA"*:
hoy esa visibilidad depende del perfil que se flasheó, no de la galga.

### H1 — la calibración de la familia modular es un dead store

`nvsSaveCalibration()` tiene call sites (`command_handler.cpp:208`);
`nvsLoadCalK()`/`nvsLoadCalOffsetV()` **ninguno**. El sampler usa `DEFAULT_K` y
`DEFAULT_OFFSET`, **de compilación** (`adc_sampler.cpp:148-149`). El comando
valida el rango, escribe NVS, ackea `0` (éxito) y el dashboard muestra los
`cal_*` nuevos — **y no cambia un solo volt**. Recalibrar esa familia requiere
recompilar.

Mismo patrón que el H2 del REVIVAL y el H5 del aislamiento de tenant de anoche:
**el sistema informa éxito por un camino que no verificó.**

### H2 — las dos familias hacen cuentas distintas con las mismas dos constantes

```
monolítica : v = (v_raw - offset_v) * k     [restar, después escalar]
modular    : v = v_raw * k + off            [escalar, después sumar]
```

Coinciden **sólo si `k == 1`** (fijado por test). Y hay una tercera variante:
`OFFSET_SIGN` es `+1` en A y `-1` en B. La migración documenta una sola de las
dos. **Nada registra qué familia corre cada placa**, así que mirando
`devices.cal_*` no se sabe qué cuenta se le hizo a esos números.

### H5 / H6 / H7

- **H5 — `cal_with_load` cambia las UNIDADES de `v_pp`.** El handler calcula
  `k = applied_load / v_corr`: después de ese comando `v_pp` ya no está en volts,
  está en unidades de carga. Los **7 umbrales** del sistema siguen hardcodeados
  en volts y la UI sigue rotulando `mV` — y **seis de los siete son el mismo
  número escrito seis veces**. **Precondición para el ítem #2:**
  `data/field_captures` es ground truth en volts crudos (`k=1`); comparar contra
  esas capturas sólo vale con la calibración en identidad. Calibrar con carga
  **antes** de caracterizar invalida la caracterización.
- **H6** — los 6 botones de calibración del dashboard (`autoffset`, `cal_set`,
  `cal_with_load`, `cal_step1`, `cal_step_joint`, `cal_reset`) **no existen en la
  familia modular**, que sólo parsea `set_calibration`. Caen al catch-all que —
  según midió el branch del 08-04 — ackea `'ack'` y no `'error'`: **la UI los
  pinta verdes**. Sumado a H1, calibrar esa familia falla de dos maneras
  independientes y las dos informan éxito.
- **H7** — cada familia guarda la calibración en un namespace de NVS distinto
  (`"cal"` con keys `offset_v/k` vs `"galgas"` con `cal_offset/cal_k`): dos
  cajones que no se ven, en el mismo chip. Un OTA que cruce de familia —posible,
  comparten target, que es el ítem #5— deja la placa midiendo con la calibración
  de fábrica mientras `devices.cal_*` sigue mostrando la vieja.

### Lo que está BIEN y queda fijado por test

Tan importante: es lo que **no** hay que ir a revisar.

- **La familia monolítica recarga la calibración de NVS en cada boot**
  (`:1826`) → sobrevive deep sleep **y** power-cycle. Es **media respuesta al
  ítem #10**, leída del código.
- **`factory_reset` sí borra el namespace `"cal"`** (`:1694`), como promete su
  comentario.
- **`sampleMeanRaw()` muestrea crudo**: `autoffset` y `cal_with_load` **no** se
  corrigen dos veces. La cuenta de calibración en sí está bien planteada.
- **La familia monolítica implementa los 6 comandos** y el CHECK los acepta a
  todos: el camino que se usa en banco cierra.
- **`cal_set` valida `k > 0 && isfinite`** — no hay forma de meter un `k` que
  vuelva `NaN` toda la telemetría.
- **La familia modular no tiene el bug del centinela.**

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-09-b-cadena-medicion
python tools/check_measurement_chain.py                  # -> 4 error / 3 warn, exit 1
python tools/check_measurement_chain.py --json
python tools/check_measurement_chain.py --demo-sentinel   # la demostración numérica de H4
python -m unittest tools.test_check_measurement_chain     # -> Ran 69 tests, OK
```

H3 se comprueba sin la herramienta, leyendo una línea: `ota_wm_pp.ino:1411`
contra `PlantaView.jsx:49`, y preguntándose **qué mira ese booleano**.

`TestRepoReal` **fija los 7 hallazgos**: si alguien arregla uno, el test falla y
obliga a actualizar `docs/measurement-chain.md` en el mismo commit.

**Verificado por mutación** (las 4 hacen fallar la suite): no saltear la rama
`DEV_SIMULATE_ADC`, tratar el centinela `3.3/0.0` como seguro, contar la
definición inline como call site, e ignorar los centinelas en el oráculo
numérico.

## Qué quedó sin verificar (banco — trabajo de día)

Todo está **leído del código, no observado en una placa**. Lo bueno: **ninguna
de estas pruebas necesita galga física ni LiPo** — alcanza una placa en el banco
con el Serial abierto. En orden de valor:

1. **H4 en 10 minutos:** `cal_set` con `offset_v` 100 mV por encima de la tensión
   de reposo del ADC → todas las muestras corregidas quedan negativas → mirar el
   `[BURST]` del Serial: `max=0.0000` y `vpp` ≈ el offset. Si eso pasa, H4 está
   confirmado y es un fix de una línea.
2. **H3 en un minuto:** placa con binario `*-palerta` posteando en reposo →
   `select in_alert from readings order by ts desc limit 20;` → 20 `true` lo
   confirma.
3. **H1 en dos minutos:** con la familia modular, `set_calibration {k: 2.0,
   offset_v: 0}` → el comando ackea OK y `v_mean` de la lectura siguiente **no**
   se duplica.
4. **H7:** flashear una familia sobre la otra y ver si `v_mean` salta de escala.

- **No compilé firmware ni bajé toolchains** (regla de disciplina de tiempo). La
  auditoría es estática.
- **No corrí `npm run build`**: no toqué `web/`, sólo lo leo.
- **No entré a `data/field_captures`** (sagrado, read-only). No lo necesita.
- **Ningún fix aplicado** — generator ≠ evaluator. El de H4 es de una línea y
  tiene dueño (@firmware); el de H3 es una decisión de diseño (¿`in_alert` es
  "la señal está mal" o "estoy en modo rápido"?), que **hay que tomar antes de
  octubre** porque es lo que Dreyfus va a mirar.

## Estado

- Branch `nocturno/local-2026-08-09-b-cadena-medicion` pusheado (1 commit,
  `926b623`: 4 archivos, +1934). galgas volvió a `main` limpio.
- `QUE_FALTA.md` de galgas: ítem **#17** + notas en el **#2** y el **#10** (en el
  branch).
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Séptima noche que lo reporto:** es un firmware que va a un equipo a 2000 km y
  vive **sólo en este disco**. **No lo toqué.**
- ℹ️ `C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-07-18-modelo-energia`, no en `main` (estado previo). **No
  lo cambié.**
- ℹ️ `C:\Proyectos\datalogger` tiene sin trackear `docs/CONEXIONES_LAB.html`
  (previo). **No lo toqué.**
- ⚠️ Queda el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando Matías quiera.
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las doce
  noches anteriores). **No los toqué.** Matías: commitealos, o la rutina cloud
  choca en el próximo `git pull`.
- La cola de merge suma **49 branches** en origin (galgas 18, datalogger 15,
  frioseguro 15, cosechador 1). El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo
  y sin usar: falta la sesión humana.
  **Nota de prioridad:** de los 18 de galgas, éste es el que toca **el número que
  Dreyfus va a mirar en pantalla**. H4 y H3 son fixes chicos con consecuencia
  grande, y los dos se confirman en el banco en 10 minutos sin galga ni batería —
  o sea, se pueden cerrar **antes** de que llegue el hardware del ítem #2.
