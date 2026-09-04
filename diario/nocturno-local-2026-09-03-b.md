# Nocturno local — 2026-09-03-b

**Trabajador:** worker nocturno local (Matías durmiendo). Segundo turno de la
noche (el primero fue `nocturno-local-2026-09-03.md`, galgas / el ADC que no se
apaga).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la
jerarquía), zona `servidor/notificador/`.
**Branch:** `nocturno/local-2026-09-03-b-el-aviso-que-se-da-por-dado`
(pusheado, `c9583a2`).
**Sale de `backend/neon-primer-despliegue-2026-09-02` (`63dbe0f`), NO de `main`**
— ver la nota de merge más abajo, es lo único que hay que saber antes de tocarlo.
**No colisiona con ninguno de los 32 branches abiertos**: es el único que toca
`notificador/`. **No toca SQL: no hay migración que aplicar.**

---

## TL;DR

> **El notificador daba por dado el aviso que ningún canal pudo entregar. No lo
> demoraba: lo perdía. Con la sesión de WhatsApp caída y Supabase andando, todas
> las alertas de la caída se iban en silencio, sin más rastro que un
> `registro.error` en el log.**

El bookkeeping de "ya avisé" lo hacía la **decisión**, no la **entrega**.
`reglas.decidir()` marcaba la ventana de silencio **antes de tocar un canal**, y
`una_vuelta()` guardaba ese estado y avanzaba las marcas de agua en el paso 7
**pasara lo que pasara**.

Lo notable es que el código *sabía* del problema y lo tenía escrito:

```python
# Ningún canal pudo. No se marca como avisado: la próxima vuelta lo
# reintenta. Es la diferencia entre "no salió" y "se perdió".
```

`ya_avisado` efectivamente no se marcaba. Las **otras dos** memorias sí.

**D1 — la vuelta fallida gastaba igual la ventana.** Vuelta N: entra la alerta,
`ultimo_envio = ahora`, los canales fallan, el estado se guarda igual. Vuelta
N+1 (60 s después): la alerta vuelve a llegar y `decidir` la encuentra **`en
silencio, faltan 1740s`**. El reintento que el comentario promete no ocurre
nunca — y mientras el canal siga caído, cada vuelta renueva el descarte.

**D2 — y la marca de agua la dejaba atrás.** El pedido de cada vuelta es
`created_at >= marca - solape`, con `NOTI_SOLAPE_SEG` = **120 s**, y
`marcas_nuevas[tabla] = max(momentos)` avanzaba aunque el aviso no hubiera
salido. En cuanto entraba una alerta nueva más de 120 s posterior, la vieja
quedaba **fuera de la ventana de consulta y no se volvía a pedir jamás**.

El escenario no es exótico, es **el más probable**: un canal caído con Supabase
andando (sesión de WhatsApp vencida, token de Telegram revocado, SMTP que
rechaza la clave). Si lo que se cae es internet, `origen.traer` lanza, la vuelta
entera falla y no se avanza nada — ese caso ya estaba bien. Es exactamente el
caso parcial el que perdía todo.

El docstring del servicio dice, textual: *"preferimos repetir […] antes que
perder una alerta"*. Para este camino era al revés.

**D3 —** el registro de "no salió" guardaba sólo `mensaje.claves[0]`: de un
mensaje agrupado de 3 alertas, la 2.ª y la 3.ª no dejaban rastro. Es justo la
tabla que se mira cuando el cliente llama preguntando por qué no le avisaron.

**Quinta aparición del patrón** después de `lastSupabaseSync` (08-26),
`faultAlerted1` (08-29), `lastTelegramAlert` (09-01-b) y `probe_fault` (09-02-b):
**el estado avanza y no vuelve.** Las cuatro anteriores fueron en firmware o en
la base. Ésta está en el proceso que le manda el mensaje al cliente — o sea, en
lo que se cobra.

## Por qué esta tarea y no otra

1. **Jerarquía.** PLATA es la prioridad #1 y esto es literalmente el producto:
   "el servicio avisa". El turno anterior de esta misma noche fue galgas
   (octubre, 2.º).
2. **`notificador/` es código de anteayer que nadie auditó** y ninguno de los 32
   branches nocturnos abiertos lo toca. Cero colisión, cero trabajo repetido.
3. **Software puro y verificable sin banco**: `reglas.py` es lógica pura y
   `una_vuelta()` recibe almacén, origen y canales inyectados. Se prueba entero
   sin red, sin base y sin hardware.
4. **Un test del repo ya delataba el bug** (abajo). Cuando el harness te está
   avisando, eso es la tarea.
5. Miré antes los otros tres: galgas lo trabajé hace unas horas, datalogger
   anteanoche, y cosechador sigue bloqueado por la compra.

**Lo que NO elegí, y por qué lo digo:** venía siguiendo el hallazgo colateral #1
de anoche (los umbrales de "esto es una temperatura" que difieren entre firmware
`-55..125`, Python `-60..85` y el trigger SQL `-100..84`). Es real y está bien
anotado, pero al mirarlo de cerca **el daño concreto es fino**: la ventana en
disputa (84–85 °C) casi no es alcanzable por un equipo real, y el `-80` que
supuestamente ensuciaba el promedio **no puede llegar**, porque el firmware ya
rechaza todo lo menor a −55. Preferí no inflarlo y agarrar el que sí pierde
avisos hoy. Queda como estaba en el QUE_FALTA.

## Qué hice

**Invariante: el silencio y el cupo se consumen cuando el aviso SALE, no cuando
se decide mandarlo.**

**1. `decidir()` es de solo lectura; el único escritor es `confirmar()`.**

```python
def decidir(avisos, estado, ahora, politica):    # -> (mensajes, descartados)
def confirmar(estado, mensajes, ahora, politica) -> estado_nuevo
```

`decidir()` **ya no devuelve estado**. No es cosmética: es lo que hace que el bug
no se pueda reintroducir por descuido — el que decide no tiene con qué marcar, y
quien quiera marcar tiene que pasarle mensajes que hayan salido. Es el mismo
razonamiento del chokepoint que usé anoche en `dormirSegundos()`: el guard va
donde no se pueda saltear por olvido.

Sigue razonando sobre una **copia de trabajo**, porque adentro de una misma
vuelta el silencio y el techo tienen que valer entre los avisos de la tanda (si
no, un equipo en bucle que dispara 400 alertas en una vuelta las manda todas).
Esa copia se descarta al salir.

Tres cosas que aparecieron al separarlo, y las tres son bugs que me evité:

- **El grupo marca por cada aviso que lleva adentro** (`Mensaje.marcas`). Si
  marcara sólo el primero, un mensaje de "3 avisos" dejaría dos tipos sin
  silenciar y el rebote volvería por ahí.
- **El aviso de tope no gasta cupo ni abre ventana.** Su antiduplicado es la
  bandera `avisada` de la cubeta; si consumiera cupo se mordería la cola. Es lo
  que ya hacía la versión vieja, pero por accidente de dónde caía el `continue`:
  ahora está escrito y con test.
- **La cubeta de la hora se renueva en un solo lugar** (`_cubeta()`). Efecto
  colateral gratis: como el estado ahora sólo se crea al confirmar, dejan de
  acumularse entradas vacías que `limpiar_estado()` conservaba para siempre
  (`momento is None` → se queda) — que era el "JSON de 40 MB" que su propio
  docstring temía.

**2. La marca de agua no pasa por encima de un aviso no entregado.**

```python
if pendientes and TABLA_ALERTAS in marcas_nuevas:
    piso = min(m.momento for m in pendientes)
```

**El más viejo**, no el más nuevo: con el más nuevo los otros pendientes se
pierden igual (es uno de los mutantes). Sólo se frena `alerts`: de `readings` y
`events` no cuelga ningún mensaje.

**3. `AlmacenMemoria` ahora imita a `AlmacenPostgres`.** Y éste es el hallazgo
del harness de la noche: `AlmacenPostgres.avanzar_marca` usa **`GREATEST(...)`**
en su `ON CONFLICT` — la marca **nunca retrocede** —, mientras que
`AlmacenMemoria` asignaba a secas. O sea que el freno del punto 2 **habría dado
verde en los tests contra una semántica que en producción no existe.** Casi
mando un arreglo que sólo funcionaba en el harness. Ahora las dos hacen lo mismo
y hay un test que lo fija.

(El freno es correcto igual bajo `GREATEST`, y lo dejé demostrado en el doc: por
inducción, `desde = marca − solape ≤ piso` siempre, así que la alerta se vuelve a
pedir en cada vuelta hasta que salga.)

**4. El descarte registra todas las claves del grupo.**

## El test que ya delataba el bug

`test_si_ningun_canal_entrega_no_se_marca_como_avisado` existía y estaba **en
verde**. Pasaba por esta línea:

```python
self.almacen.estado = {}          # pasó la ventana de silencio
```

El test **borraba el estado a mano** para que el reintento funcionara. El
comentario dice "pasó la ventana de silencio", pero entre las dos vueltas **no
pasa ni un segundo simulado**. Era un workaround del bug escrito como si fuera
una condición del escenario — y por eso el bug sobrevivió a tener un test que lo
apuntaba. **La línea se borró**; el test sigue verde por el arreglo.

## Cómo verificarlo (comandos exactos, sin red, sin base y sin hardware)

```bash
cd C:\Proyectos\frioseguro
# el checkout de esta carpeta está en otro branch y con cambios: usá un worktree
git worktree add /c/Proyectos/_fs-rev nocturno/local-2026-09-03-b-el-aviso-que-se-da-por-dado

cd /c/Proyectos/_fs-rev/servidor
python -m unittest discover -s notificador/tests -t . -q    # -> Ran 44 tests, OK
python -m unittest discover -s api/tests -t api -q          # -> Ran 77 tests, OK

cd /c/Proyectos/_fs-rev
python tools/check_aviso_no_entregado.py                    # -> OK -- 27 checks, 0 fallas
python tools/check_aviso_no_entregado.py --mutantes         # -> 7/7 mutantes muertos

# la prueba de que el checker sirve: contra el código de antes tiene que REPROBAR
python tools/check_aviso_no_entregado.py --root /c/Proyectos/frioseguro
#   -> FALLO -- 25 checks, 19 fallas   (rc=1)

git worktree remove --force /c/Proyectos/_fs-rev
```

Los cinco corrieron esta noche y dieron exactamente eso. También `py_compile`
sobre los seis archivos tocados.

**Los 7 mutantes** existen porque un test verde sobre algo que no se puede
romper no prueba nada. El checker reintroduce cada defecto en una copia del árbol
y exige rojo: el bug D1 original · el bug D2 original · el freno tomado del
pendiente más nuevo · el bug D3 · `confirmar()` que no gasta la ventana (rompe el
antiduplicado en el otro sentido) · el tope que se come cupo · `AlmacenMemoria`
sin `GREATEST`. **Los tres primeros reproducen el estado anterior a este branch:
no son tests que acompañan al arreglo, son tests que habrían cazado el defecto.**

El último punto —que el checker reprueba contra el código viejo— es el que le da
valor al resto.

## ⚠ Al mergear — leer esto primero

**Este branch NO sale de `main`.** `servidor/notificador/` (y el portal, y
`identidad.py`, y `NEON.md`) **todavía no están en `main`**: viven en
`backend/neon-primer-despliegue-2026-09-02` (`63dbe0f`, pusheado), que es un
commit por delante de `main`. Ese branch se mergea primero; después éste, que
sale de él y aplica limpio.

Vale la pena notarlo aparte: **el trabajo del servidor de anteayer sigue sin
llegar a `main`**, y ya hay dos branches nocturnos colgando de esa zona (el de
anoche, `09-02-b`, salió de `main` y toca `principal.py`, que sí está en `main`,
así que ése es independiente). No es urgente, pero cuanto más se acumule, más
caro el merge.

Después del merge conviene sumar `python tools/check_aviso_no_entregado.py` al
mismo lugar donde ya corren los otros checks.

## Qué quedó SIN verificar (necesita una corrida real, NO hardware)

1. **Ningún notificador corrió contra Supabase con este código.** Todo lo de acá
   es lógica pura y `AlmacenMemoria`; **`AlmacenPostgres` no se ejecutó** — no
   hay Postgres ni `psycopg` en esta máquina (chequeado). Lo único que le cambié
   es un comentario, pero conviene ver una vez cómo se lleva `guardar_estado`
   (que hace `DELETE` + `INSERT` de todo el estado) con el estado más chico que
   ahora produce `confirmar()`.
2. **El ciclo completo con un canal caído de verdad**, ~15 minutos: apagar el
   token de Telegram · dejar entrar alertas 3-4 vueltas · volver a prenderlo ·
   confirmar que **sale el aviso viejo** y que la marca de `alerts` se destrabó.
   Éste es el bug de fondo y es el que hay que ver ocurrir. En el log tiene que
   aparecer `la marca de alerts se frena en <fecha>: hay N aviso(s) sin entregar`.
3. **Cuánto crece el re-pedido** durante una caída larga (ver el límite abajo).

## Límites declarados (no son omisiones)

- **Mientras un canal esté caído, la marca de `alerts` no avanza**, así que cada
  vuelta re-pide un tramo cada vez más largo. Es **a propósito** —preferimos
  re-pedir a perder— y está acotado por `lote × max_paginas` (1000 × 50). Con
  alertas de a decenas por día no molesta; con un equipo en bucle **y** el canal
  caído varios días, el pedido se pone pesado. El que tiene que gritar antes de
  eso es healthchecks (`latido.mal`), no el silencio. Si molesta en campo, el
  arreglo natural es un techo de antigüedad ("no frenes por un aviso de más de N
  horas: dalo por perdido y anotalo"), que es **decisión de producto, no de una
  noche**.
- **Un aviso descartado por política** (severidad `info`, ventana de silencio,
  techo por hora) **no frena la marca**: se decidió no mandarlo, no falló al
  mandarlo. Si frenara, la marca no avanzaría nunca.
- **No hay reintento adentro de la misma vuelta.** Los 3 intentos con espera
  creciente de `canales/base.py` siguen siendo todo; el siguiente intento es la
  vuelta que viene (60 s).
- **No hay aviso de "el canal estuvo caído N minutos"**. El log lo dice y
  healthchecks late igual (la vuelta no falla): un canal caído hoy es visible
  sólo mirando. Es del mismo tamaño que este trabajo.

## Hallazgo colateral que el branch NO toca (a propósito)

**El techo por hora cuenta avisos, pero manda mensajes.** `max_por_hora` (6 por
defecto) se descuenta por **aviso**, mientras que la agrupación los junta en un
solo mensaje. Un equipo con 4 cámaras que se calientan juntas produce 4 avisos →
**1 mensaje**, pero consume **4 de los 6** cupos de la hora. Dos episodios así y
el equipo queda contenido habiendo mandado 2 mensajes. Es defendible como está
(el techo protege del bucle, y el bucle se mide en avisos), pero **no es lo que
dice el docstring**, que habla de mensajes. Es una decisión de producto: la dejo
anotada, sin tocar comportamiento.

## Cosecha a biblioteca

El par **decidir / confirmar** —decidir sin efectos y consumir el estado sólo
contra el acuse de entrega— es el mismo invariante que `telegram_gate.h`
(09-01-b), `sensor_fault_model.h` (08-29) y la máquina de episodios de sonda
(09-02-b): ya van **cuatro implementaciones del mismo invariante en dos
lenguajes**. **No se cosecha todavía**, por la regla de la casa: ningún módulo
entra sin decir dónde se probó, y esto no vio una corrida real. Cuando las cuatro
pasen su prueba, conviene mirarlas juntas con `@bibliotecario` y cosechar una
sola.

## Estado del repo — dos cosas para un minuto tuyo

- `C:\Proyectos\frioseguro` sigue en `backend/neon-primer-despliegue-2026-09-02`
  con los 6 archivos del gabinete 3D modificados y **`TERMOVIGIA_KIT_V1.zip` y
  `TERMOVIGIA_SERVIDOR.zip` sin trackear** (los zips pesan y no deberían entrar
  al repo). **No los toqué**: trabajé en un worktree aparte y verifiqué al cerrar
  que el checkout quedó idéntico. El worktree ya se borró. (Es la segunda noche
  que lo anoto.)
- `C:\Proyectos\datalogger` **sigue con el árbol sucio** y el branch
  `nocturno/local-2026-08-31-el-csv-que-no-avisa` **sin un solo commit**, quinta
  noche. Ya no bloquea (se esquiva con worktree) pero es trabajo colgando: o se
  commitea, o se tira.

---

## Estado del branch

`nocturno/local-2026-09-03-b-el-aviso-que-se-da-por-dado` → `c9583a2`, pusheado a
`origin`. `QUE_FALTA.md` de frioseguro actualizado (ítem **#21**). Documento
largo: `C:\Proyectos\frioseguro\servidor\AVISO_NO_ENTREGADO.md`.

**Archivos:** `notificador/reglas.py` · `notificador/servicio.py` ·
`notificador/almacen.py` · `notificador/tests/test_reglas.py` ·
`notificador/tests/test_vuelta.py` (modificados) ·
`tools/check_aviso_no_entregado.py` · `servidor/AVISO_NO_ENTREGADO.md` (nuevos).
