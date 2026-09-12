# Nocturno local — 2026-09-11-b

**Trabajador:** worker nocturno local (Matías durmiendo). **Segundo turno** de la
noche — el primero fue `nocturno-local-2026-09-11.md` (datalogger, el piezo que
se calibra mudo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA — prioridad #1 de la
jerarquía**), zona `servidor/` + `docs/`.
**Branch:** `nocturno/local-2026-09-11-b-el-ota-que-insiste`
(pusheado, `6ee07d5`).
**Sale de `origin/main` (`2ac3a7d`) limpio**, sin ningún otro branch mergeado
adentro.
**No toca** `firmware_modular/`, ni `web-dashboard/`, ni el notificador, ni
`supabase/`, ni `hardware/`, ni `data/`. **No colisiona con ninguno de los 13
branches abiertos de frioseguro** — todos viven en firmware o en el panel. El
único roce es con `09-04-b`, que agrega `sql/070_*` y toca la zona de `/ingest`
de `principal.py`: archivos y funciones distintas, se mergean en cualquier orden.

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_frio_0911b`, ya
eliminado) porque el árbol de `frioseguro` tiene el KiCad de Matías sin
commitear (TermoVigía Mini/Lite, 2 modificados + 5 sin trackear). **Verificado al
terminar: el árbol quedó idéntico** (mismo hash de `git status`,
`fb82167c…`), en el branch `09-04-b` donde estaba.

---

## TL;DR

> **El servidor no sabía dejar de ofrecer un firmware que no entra.**
> `release_para()` decide qué versión le toca a un equipo comparando
> `devices.firmware_version` con la del release publicado. Es correcto, y es
> exactamente el problema: **un equipo que baja el .bin y no logra aplicarlo
> conserva su versión vieja**, así que para la base sigue necesitando la
> actualización. Próximo `POST /ota/manifiesto`: el mismo release roto. Y el
> siguiente. Sin final. `ota_progress` guardaba el `status`, pero **nadie lo
> miraba antes de ofrecer** y `release_para()` no lo consulta.
>
> El limitador deja pasar **un manifiesto por minuto** y cada manifiesto habilita
> una descarga entera. Con un .bin de 1,3 MB eso son **2880 descargas y ~3,7 GB
> de SIM en 48 horas**, la partición OTA reescrita 2880 veces, y —lo peor— **un
> Telegram a Matías por cada vuelta**, que es la forma exacta en que un canal de
> avisos deja de existir.
>
> **Y el caso serio no es el que falla avisando: es el que no vuelve.** Un equipo
> que se cuelga a mitad del flasheo nunca manda `failed`; su fila queda en
> `downloading` y, contando sólo los resultados reportados, el contador se
> quedaría en cero para siempre mientras el equipo se rebootea en bucle.

## Por qué esta tarea

1. **Es PLATA y es la regla dura de Matías.** *"OTA nunca ladrillo: ningún nodo
   puede perderse por una reprogramación fallida."* El lado del **equipo** —hash,
   `.bak`, rollback por arranques fallidos— está cubierto; en galgas se cerró
   anoche (`09-10-b`, el bin que arranca y no vuelve). **Lo que faltaba es la
   otra mitad: que el servidor deje de insistir.** Un equipo que no se puede
   ladrillar pero se pasa la vida bajando el mismo .bin roto no es un éxito.
2. **Cuesta plata medible, hoy.** TERMOVIGÍA va a 5 equipos al 31-oct y la línea
   minera es 4G. 3,7 GB en dos días sobre una SIM es una factura, no una
   métrica.
3. **Estaba libre.** Ninguno de los 13 branches abiertos de frioseguro toca
   `servidor/api/principal.py` en la zona de OTA.
4. **Se hace entera sin hardware, sin Docker y sin base**: la decisión es pura y
   los tests corren con la stdlib.
5. **Le tocaba a PLATA por jerarquía**: el primer turno de esta noche fue
   datalogger (octubre).

## El discriminador que ordenó el diseño

La pregunta no era *"¿cuántas veces falló?"* sino **"¿qué es lo que el servidor
ve siempre?"**.

Contar los resultados reportados parece lo natural y **deja afuera justo el caso
que hay que frenar**: el equipo que se cuelga flasheando no reporta nunca. Lo
único que el servidor observa en todos los casos es **haber entregado el
manifiesto**. Entonces la regla es: **el intento se cuenta al ofrecer, no al
reportar.** El que falla avisando y el que se cuelga en silencio quedan cubiertos
por el mismo contador, sin un caso especial.

Mismo patrón que el `lastSupabaseSync = now` del `08-26` y el `faultAlerted1 =
true` del `08-29`: el estado se actualiza en el lugar donde la acción **realmente
ocurre**, no donde uno espera que termine bien.

## La escalera

```
intento 1  →  esperar 15 min
intento 2  →  esperar  1 h
intento 3  →  esperar  4 h
intento 4  →  esperar 12 h
intento 5  →  QUEMADO: no se ofrece más
```

- **El primer reintento es en minutos, no en horas**, a propósito: la causa más
  común de un OTA fallido es una **descarga cortada**, no un binario malo, y
  castigar eso con horas retrasa una actualización sana.
- **Cinco intentos cubren ~29 h**: si era transitorio sobra, y si era el .bin el
  gasto se cortó y Matías se enteró la noche anterior.
- **El quemado NO se desbloquea con el tiempo.** Si se desbloqueara, el bucle
  volvería: más lento, igual de eterno. Se levanta a mano.
- **Se avisa exactamente dos veces**: la primera falla (por si es algo que se
  arregla al toque) y el quemado (hay que decidir). Los del medio no aportan
  información nueva y son justo los que convierten el canal en ruido.

| | con el bucle | con el freno |
|---|---|---|
| descargas del .bin en 48 h | **2880** | **5** |
| datos sobre la SIM (.bin de 1,3 MB) | **~3,7 GB** | **~6,5 MB** |
| escrituras de la partición OTA | 2880 | 5 |
| Telegrams | uno por vuelta | **2** |

## Una sola fuente de verdad

`release_para()` **no se tocó**: sigue contestando *cuál* release corresponde. La
regla de *si insistir* vive **sólo** en `servidor/api/logica/ota_reintentos.py`
—puro, sin psycopg, sin FastAPI, sin red— y la migración 080 sólo **guarda
estado** (dos columnas, append-only, idempotente).

Escribir el umbral también en SQL habría sido cómodo para el panel y es
exactamente cómo se desincroniza en silencio: por eso la vista `v_ota_trabados`
publica `intentos` y **no** una columna `quemado`, con el motivo escrito al lado
en el `.sql`.

## Qué se entregó

- **`servidor/api/logica/ota_reintentos.py`** (nuevo) — `decidir_oferta()` y
  `tras_resultado()`, más la escalera. Puro.
- **`servidor/sql/080_ota_reintentos.sql`** (nuevo) — `ota_progress.intentos` y
  `.bloqueado_hasta`, un índice parcial para los trabados, la función
  `ota_rehabilitar(device, version)` (sólo `service_role`) y la vista
  `v_ota_trabados`. **Append-only e idempotente**; las filas que ya existen
  arrancan en `intentos=0`, así que **nadie queda quemado por historia vieja**.
- **`servidor/api/principal.py`** — los dos endpoints de OTA enchufados.
- **`servidor/herramientas/verificar_e2e.py`** — ver el efecto de borde abajo.
- **`docs/ota-reintentos.md`** y el ítem 21 del `QUE_FALTA.md` de frioseguro.

## Un bug que encontró el repaso del SQL, no el test

La consulta de `/ota/resultado` la escribí primero como
`WHERE p.device_id = %s AND (%s IS NULL OR r.version = %s)` para cubrir de una
vez el firmware que manda `version` y el que no. **Postgres no le puede inferir
el tipo a un NULL suelto como parámetro** (`could not determine data type of
parameter`) — habría explotado la primera vez que un equipo del parque viejo
reportara, y ningún test de lógica pura lo iba a ver. Son dos consultas
separadas, con el porqué escrito al lado.

## Cómo verificarlo (comandos exactos, sin hardware, sin Docker, ~1 minuto)

```bash
cd C:\Proyectos\frioseguro
git fetch origin
git checkout nocturno/local-2026-09-11-b-el-ota-que-insiste

cd servidor/api
python -m unittest discover -s tests -t .
```

⚠️ **Ojo con el comando que dice `logica/__init__.py`**
(`python -m unittest discover -s api/tests -t .` desde `servidor/`): **no
funciona**, tira `ModuleNotFoundError: No module named 'logica'`. El bueno es el
de arriba, desde `servidor/api`. Drift viejo del docstring, **no lo toqué** para
no mezclar; anotado para @cronista.

**Resultados obtenidos esta noche:**

- **77 tests OK** (eran 48: los 48 previos del servidor siguen en verde, sin
  regresión). Los bloques marcados **REGRESIÓN** fallan contra el código viejo.
- **10 mutaciones sembradas a mano en la lógica, las 10 muertas:**

  | mutante | qué reimplanta |
  |---|---|
  | 1 | no bloquear al ofrecer (**el bucle entero vuelve**) |
  | 2 | nunca quemarse |
  | 3 | `applied` no pone el contador en cero |
  | 4 | avisar en cada falla (la tormenta de Telegrams) |
  | 5 | `downloading` libera el bloqueo (el equipo se auto-habilita otra descarga) |
  | 6 | escalera plana (sin backoff creciente) |
  | 7 | un `bloqueado_hasta` naive tumba el endpoint |
  | 8 | off-by-one en el quemado |
  | 9 | contar el intento dos veces (quema a la mitad de los reintentos prometidos) |
  | 10 | reofrecer lo que el equipo ya aplicó |

- **`TestCableado`**: `principal.py` **no se puede importar** en esta máquina (no
  hay FastAPI instalado), así que se lo lee por **AST** y se verifica que la
  decisión esté **enchufada** en los dos endpoints — no sólo escrita en el
  módulo. También verifica que la migración sea append-only (ni un `DROP`, ni un
  `DELETE`, ni un `TRUNCATE`) y que **no toque `release_para()`**.
- `principal.py` y `verificar_e2e.py`: **sintaxis OK** por `ast.parse`.

## Cambios de contrato (chicos, hacia atrás compatibles)

- `POST /ota/manifiesto` puede devolver `{"hay_actualizacion": false, "motivo":
  "..."}`. El firmware viejo lee `hay_actualizacion` y sigue igual.
- `POST /ota/resultado` acepta **`version`** opcional. Sin ella se elige la fila
  más reciente, que es lo que hacía antes.
- `POST /ota/resultado` devuelve **404** si no hay ningún OTA en curso para ese
  equipo. Antes el `UPDATE` no tocaba ninguna fila y contestaba `{"ok":true}`
  igual: un reporte que no se guardaba en ningún lado, con acuse de recibo.

## ⚠️ Efecto de borde que hay que saber antes de usarlo

**`verificar_e2e.py` hace `POST /ota/manifiesto`, así que cada corrida cuenta
como un intento de OTA.** Cinco corridas seguidas contra un equipo con un release
pendiente **lo dejan quemado**. Está escrito en el docstring de la herramienta, y
cuando pasa la herramienta ahora imprime *"hay un release pero no se ofrece:
&lt;motivo&gt;"* en vez del engañoso *"no hay firmware nuevo"*.

Para destrabarlo: `SELECT ota_rehabilitar('<device_id>', '<version>');`

## Qué quedó SIN verificar (pide la base y el banco)

1. **⚠️ La migración 080 nunca se corrió contra Postgres.** La aplica sola el
   servicio al arrancar. Hay que confirmar que las filas existentes de
   `ota_progress` queden con `intentos=0` (es el default de la columna, pero eso
   es razonamiento, no observación). [@backend]
2. **`ota_rehabilitar()` no se ejecutó nunca.** El `UPDATE ... FROM` con alias y
   el `GET DIAGNOSTICS` están escritos contra la documentación, no probados. Es
   lo único del branch que no tiene ni un test. [@backend]
3. **Un OTA fallido de verdad**: publicar un .bin corrupto a propósito contra un
   equipo de banco y ver la escalera entera —15 min, 1 h, 4 h, 12 h, quemado—
   con los **dos** Telegrams y ninguno más. [@firmware + @backend]
4. **El caso del equipo que se cuelga flasheando**, que es el que motivó el
   diseño: sólo se probó en el modelo. [@firmware]

## Lo que NO hice, a propósito

- **No le puse un desbloqueo automático al quemado.** Sería el arreglo "amable" y
  es exactamente el que no va: un release que vuelve a ofrecerse solo a los 7
  días es el mismo bucle con otro período. La salida es publicar un .bin nuevo
  (release nuevo = fila nueva = contador en cero solo) o rehabilitarlo mirando
  el error. El quemado es una **decisión de quien opera**, no del servidor.
- **No toqué `/ota/bajar`.** Sigue marcando `downloading` sobre cualquier fila en
  `offered` de ese equipo, sin mirar el `release_id` (la URL firmada lo tiene, en
  el `archivo`). No afecta a los contadores y meterse ahí era abrir otra cosa.
  **Deuda anotada.** [@backend]
- **No toqué el firmware** para que mande `version` en `/ota/resultado`. Es el
  otro lado del contrato y se hace con el equipo en la mano. [@firmware]
- **No arreglé el comando roto del docstring de `logica/__init__.py`**: es drift
  de doc, de otro dueño, y mezclarlo acá ensucia el diff.

## Anotado y NO tocado

- **13 branches nocturnos abiertos en frioseguro**, ninguno mergeado. Éste es el
  14.º y es el único que vive en `servidor/api/` — el resto son firmware y panel.
  Los tres de julio (`07-11-b`, `07-13`, `07-14`) tienen veredicto de
  @verificador y siguen esperando. **Sigue siendo la deuda más grande del repo:
  el trabajo está hecho y no está en `main`.** [@verificador → MATÍAS]
- **`ota_reintentos.py` es candidato a la biblioteca.** Un backoff con quemado y
  rehabilitación explícita sirve igual para la cola de comandos de galgas y para
  cualquier reintento contra la nube. **No lo coseché porque no se probó contra
  una base real.** [@bibliotecario]
- **El comando de tests de `logica/__init__.py` está mal** (`-s api/tests` desde
  `servidor/`). El bueno es `-s tests` desde `servidor/api`. [@cronista]
- En MATI-HQ quedaron **sin commitear, tal como los encontré**,
  `comercial/panamerican/PRESUPUESTO_CERRO_MORO_INTERNO.html`,
  `dominios/{backend,comercial,diseno,frontend,pcb}.md` y
  `scripts/turno_noche_log.txt`: son de otro trabajo y no me corresponde
  firmarlos. **Segunda noche que se anota.**

## Estado al cerrar

- Branch pusheado: `nocturno/local-2026-09-11-b-el-ota-que-insiste` (`6ee07d5`),
  sobre `origin/main` (`2ac3a7d`) limpio.
- `QUE_FALTA.md` de frioseguro actualizado (ítem **21**). Detalle técnico en
  `docs/ota-reintentos.md`.
- Worktree `C:\Proyectos\_noche_frio_0911b` eliminado; el árbol de `frioseguro`
  quedó **idéntico** (los 2 modificados + 5 sin trackear de Matías, intactos, en
  el branch `09-04-b`).
- Nada corriendo, nada abierto.
