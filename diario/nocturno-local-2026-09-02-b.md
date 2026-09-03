# Nocturno local — 2026-09-02-b

**Trabajador:** worker nocturno local (Matías durmiendo). Segundo turno de la
noche (el primero fue `nocturno-local-2026-09-02.md`, datalogger / OTA).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la
jerarquía), zona `servidor/`.
**Branch:** `nocturno/local-2026-09-02-b-la-sonda-que-vuelve` (pusheado, `640f4fb`).
**Sale de:** `main` (`d53c02f`). **No depende de ningún otro branch nocturno y no
colisiona con ninguno**: es el único de los 31 abiertos que toca `servidor/`, que
nació hoy mismo. Toca `servidor/api/principal.py` y agrega 5 archivos.
**No toca SQL: no hay migración que aplicar.**

---

## TL;DR

> **La alerta de "sonda no responde" se abría y no se cerraba nunca. Y como esa
> alerta abierta era la memoria de "ya avisé", la segunda caída de esa sonda no
> avisaba nunca más.**

`/ingest` abría una `probe_fault` con este guardia:

```sql
WHERE NOT EXISTS (SELECT 1 FROM alerts
                   WHERE device_id = %s AND alert_type = 'probe_fault'
                     AND NOT resolved AND metadata->>'slot' = %s)
```

`resolver_silencios()` (`sql/060`) cierra los `device_silence` que abre la nube.
Para `probe_fault` **no hay equivalente**: el string no aparece en ningún otro
`.sql` ni `.py` del servidor. Grepeado, no supuesto.

1. **El panel miente para siempre.** El cliente ve "La sonda 1 no responde"
   aunque la sonda haya vuelto a los dos minutos. Una alerta roja permanente es
   una alerta que se deja de mirar — y esto se cobra por avisar.
2. **La segunda caída queda muda.** El `NOT EXISTS` es falso para siempre, así
   que la sonda se cae, se arregla, se vuelve a caer un mes después: silencio
   total. El primer episodio deja el canal cerrado de por vida.

Es la **cuarta** aparición del mismo patrón en el portfolio, después de
`lastSupabaseSync` (`08-26`), `faultAlerted1` (`08-29`) y `lastTelegramAlert`
(`09-01-b`): **el estado avanza y no vuelve.** Las tres anteriores fueron en
firmware; ésta es en el servidor, que se desplegó contra una base real **hoy**.

## Por qué esta tarea y no otra

1. **Jerarquía.** PLATA es la prioridad #1 y esto es el core de lo que se cobra:
   el aviso. El turno anterior de esta misma noche fue datalogger (octubre, 2°).
2. **Es la mitad que faltaba de un ítem ya empezado.** El branch `08-29` hizo que
   el **firmware** avise cuando la sonda se cae; éste hace que la **nube** lleve
   el episodio. Mismo hueco, otra capa.
3. **`servidor/` es código de hoy y nadie lo auditó.** Se desplegó contra Neon
   esta tarde (25/25 tests de aislamiento, login E2E). Ninguno de los 31 branches
   nocturnos abiertos lo toca. Cero riesgo de colisión, cero trabajo repetido.
4. **Software puro y verificable sin banco** — el servidor no necesita hardware.
5. Miré antes galgas, datalogger y cosechador: galgas tiene su checkout en un
   branch nocturno, datalogger lo trabajé hace unas horas y cosechador sigue
   bloqueado por la compra.

## Qué hice

La decisión salió del handler HTTP a **`servidor/api/logica/episodios.py`**, un
módulo **puro** (stdlib, sin FastAPI ni psycopg — la regla escrita del paquete
`logica`), y por eso se prueba entero sin Docker ni Postgres.

| Estado del slot | ¿Alerta abierta? | Acción |
|---|---|---|
| `FALLA` | no, nunca hubo (o cerró hace ≥15 min) | **ABRIR** (fila nueva → el cliente escucha) |
| `FALLA` | no, cerró hace <15 min | **REABRIR** (misma fila, `reaperturas` +1) |
| `FALLA` | sí | nada (una alerta por episodio) |
| `OK` | sí | **CERRAR** |
| `AUSENTE` | cualquiera | **nada** |

**Dos decisiones que aparecieron al escribirlo como máquina de estados, y las dos
son bugs que me evité:**

- **`AUSENTE` no es `OK` ni es `FALLA`.** Un equipo con dos sondas no manda
  `temp3` ni `temp4`. Si la ausencia contara como falla, **cada equipo arrancaría
  con dos alertas eternas**; si contara como sana, **cerraría el episodio de una
  sonda que justamente dejó de reportar**. Los dos casos son test, y son dos de
  los mutantes.
- **Ventana de reapertura de 15 min.** Una sonda con mal contacto flapea; con
  lecturas de 60 s, abrir fila nueva en cada caída serían avisos por minuto y en
  media hora el cliente deja de leerlos. Adentro de la ventana es el mismo
  episodio. **El costo, declarado:** el notificador sólo mira filas nuevas, así
  que una reapertura no vuelve a notificar — el cliente se entera del episodio,
  no de cada rebote.

Cerrar es seguro en el otro sentido: el `UPDATE` no crea fila y
`avisos_de_alertas()` descarta las resueltas, así que **nadie recibe spam de
recuperación** al mergear esto.

Dos reglas de la casa que el puente respeta: la consulta filtra `source='cloud'`
(el servidor nunca cierra una alerta que abrió el equipo, `sql/010`) y el cierre
lleva `AND NOT resolved` para ser idempotente.

## Cómo verificarlo (comandos exactos, sin hardware y sin base)

```bash
cd C:\Proyectos\frioseguro
# el checkout de esta carpeta está en otro branch y con cambios: usá un worktree
git worktree add /c/Proyectos/_fs-rev nocturno/local-2026-09-02-b-la-sonda-que-vuelve
cd /c/Proyectos/_fs-rev/servidor

# 1. los tests (42 previos + 17 de la decisión + 7 del puente)
python -m unittest discover -s api/tests -t api
#    -> Ran 66 tests, OK (skipped=7)     <- los 7 del puente piden FastAPI
/c/Proyectos/frioseguro/servidor/.venv/Scripts/python.exe -m unittest discover -s api/tests -t api
#    -> Ran 66 tests, OK                 <- con el venv del servidor, ninguno se saltea

# 2. cableado + 14 mutantes (10 de la decisión, 4 del puente)
cd /c/Proyectos/_fs-rev
/c/Proyectos/frioseguro/servidor/.venv/Scripts/python.exe tools/check_episodios_sonda.py --mutants
#    -> OK -- 43 checks, 0 fallas

# 3. la prueba de que el checker sirve: contra main tiene que REPROBAR
git worktree add /c/Proyectos/_fs-main main
python tools/check_episodios_sonda.py --root /c/Proyectos/_fs-main
#    -> FALLO -- 29 checks, 27 fallas (rc=1), incluido "FALTA EL CIERRE"

git worktree remove --force /c/Proyectos/_fs-rev; git worktree remove --force /c/Proyectos/_fs-main
```

Los tres corrieron esta noche y dieron eso. También `python -m py_compile` sobre
los cuatro archivos, y la app real **se importa** con el venv del servidor
(`principal.app` levanta con `/ingest` y las tres rutas de OTA en su lugar): no
es sólo sintaxis, FastAPI aceptó el handler.

El punto 3 es el que le da valor al resto: un checker que no reprueba el bug que
dice cazar no vale nada. Y los 14 mutantes existen porque un test verde sobre un
módulo que no se puede romper tampoco prueba nada — entre ellos: no cerrar nunca
(el bug original), el slot ausente como falla y como sano, abrir una alerta por
lectura, la ventana invertida, un off-by-one en su borde, que `plan()` ignore lo
que la base ya sabe, que el cierre pierda el `AND NOT resolved`, que la consulta
deje de filtrar `source='cloud'`.

> **Detalle del harness que vale para las próximas noches:** un `unittest` que
> saltea tests devuelve **0**, así que un mutante del puente "sobreviviría" en
> silencio en una máquina sin FastAPI. El checker no lo tapa: chequea que el
> intérprete pueda importar FastAPI y, si no, **reporta falla** diciendo con qué
> python repetir. Corrido con el Python pelado da `FALLO -- 40 checks, 1 falla`,
> no un OK mentiroso.

## Qué quedó SIN verificar (necesita una base, no hardware)

**Ningún Postgres ejecutó este SQL.** En esta máquina no hay Docker, ni `psql`,
ni `psycopg` (los tres chequeados), y la base de Neon es la de producción que
desplegaste hoy: no se toca de noche. Los tests del puente usan una conexión
falsa: prueban **qué sentencia se emite y sobre qué fila**, no que Postgres la
acepte.

Pendiente, ~10 minutos con el stack levantado (`docker compose up`):

1. Que las tres sentencias sean válidas — sobre todo el
   `DISTINCT ON (metadata->>'slot') … ORDER BY metadata->>'slot', created_at DESC`,
   la única construcción no trivial.
2. **El ciclo completo**: POST `temp1:-127` → alerta abierta; POST `temp1:-18` →
   `resolved` con su `resolved_at`; POST `-127` otra vez → **fila nueva**. Éste
   es el bug de fondo y es el que hay que ver ocurrir.
3. Que la reapertura escriba `metadata.reaperturas` sin pisar el `slot` (el `||`
   sobre jsonb).
4. Que el contador de alertas abiertas del portal baje al cerrarse el episodio.

`herramientas/verificar_e2e.py` es el lugar natural para 2 y 3.

## Límites declarados (no son omisiones)

- **El camino viejo sigue sin esto.** El firmware que está en campo POSTea a
  `/rest/v1/readings` (PostgREST), no a `/ingest`: por ahí no pasa ni el descarte
  de `-127` ni el episodio. Ya estaba dicho en el docstring de `/ingest`; este
  branch no lo cambia. Es una decisión de migración, no de una noche.
- **No hay aviso de recuperación** ("la sonda volvió"). Darlo toca el notificador,
  que hoy descarta a propósito las filas resueltas, y es del mismo tamaño que
  este trabajo.
- **No hay histéresis por cantidad de lecturas**: una lectura mala abre el
  episodio, igual que antes. Un CRC malo aislado del bus 1-Wire puede abrir y
  cerrar un episodio. Agregar "N malas seguidas" pide memoria entre requests que
  el servidor no tiene y el firmware sí (`sensor_fault_model.h`, `08-29`): si
  molesta en campo, se arregla ahí, no acá.
- **La ventana de 15 min no está calibrada con datos reales** — no hay histórico
  de sondas flapeando en producción. Es un parámetro, vive en un solo lugar y su
  borde tiene test.

**Cosecha a biblioteca:** la máquina de episodios (abrir / reabrir con ventana /
cerrar, con el estado "sin dato" separado del "sano") es candidata clara — es el
mismo problema que `telegram_gate.h` (`09-01-b`) y `sensor_fault_model.h`
(`08-29`) resuelven en C. **No se cosecha todavía:** la regla del
`@bibliotecario` es que ningún módulo entra sin decir dónde se probó, y esto no
vio una base. Cuando los tres pasen su prueba real conviene mirarlos juntos: son
tres implementaciones del mismo invariante en dos lenguajes.

## Hallazgos colaterales — cuatro cosas de la misma cadena, NINGUNA tocada

Aparecieron leyendo "el equipo publica → el cliente lo ve". Tres son SQL y no se
pueden probar en esta máquina; cada una es su propia tarea. Están en el doc del
branch con más detalle.

1. **Dos umbrales distintos para la misma decisión.** `lecturas.py` invalida
   `v <= -60` o `v >= 85`; el trigger `repartir_lectura_por_sonda` (`sql/020`)
   usa `v > -100 AND v < 84`. Los dos huecos son reales: **84.5 °C** entra a
   `readings` pero el trigger no la copia a `probe_readings` → el cliente no la
   ve; y por el camino legacy **-80 °C** entra a `probe_readings` como si fuera
   temperatura y ensucia el promedio del reporte mensual.
2. **`probe_readings.org_id` puede nacer NULL y quedar invisible para siempre.**
   Se desnormaliza al insertar desde `devices.org_id`; un equipo que reporta
   **antes** de asignarse a una organización (o sea: recién flasheado en el
   taller) escribe filas que la policy `org_id = ANY(user_org_ids())` no deja ver
   nunca, ni después de asignarlo. Falta un backfill al asignar el equipo.
3. **`sensor_probes.last_seen_at` no es monótono**: el trigger lo pisa con
   `NEW.created_at` sin comparar. Cuando el firmware vacía su buffer offline
   (`offline_buffer.h`, `08-26`) las lecturas viejas llegan últimas y **el panel
   muestra la temperatura de hace horas como si fuera la actual**.
4. **`created_at` es escribible por el equipo** (está en `lecturas.COLUMNAS`).
   Hoy el firmware no la manda. Si la mandara, con el NTP sin validar (ítem #9
   del QUE_FALTA) y `PRIMARY KEY (probe_id, ts)` + `ON CONFLICT DO NOTHING`, dos
   lecturas con la misma hora se descartan **en silencio**.

## Estado del repo — dos cosas para un minuto tuyo

- `C:\Proyectos\frioseguro` tiene el checkout en `backend/neon-primer-despliegue-2026-09-02`
  con 6 archivos del gabinete 3D modificados y **`TERMOVIGIA_KIT_V1.zip` y
  `TERMOVIGIA_SERVIDOR.zip` sin trackear** (los zips pesan y no deberían entrar al
  repo). **No los toqué**: trabajé en un worktree aparte sacado de `main`, y
  verifiqué al cerrar que el checkout quedó idéntico. Los worktrees ya se borraron.
- `C:\Proyectos\datalogger` **sigue con el árbol sucio** y el branch
  `nocturno/local-2026-08-31-el-csv-que-no-avisa` **sin un solo commit**, cuarta
  noche. Ya no bloquea (se esquiva con worktree) pero es trabajo colgando: o se
  commitea, o se tira.

---

## Estado del branch

`nocturno/local-2026-09-02-b-la-sonda-que-vuelve` → `640f4fb`, pusheado a `origin`.
`QUE_FALTA.md` de frioseguro actualizado (ítem **#20**). Documento largo:
`C:\Proyectos\frioseguro\servidor\EPISODIOS_SONDA.md`.
