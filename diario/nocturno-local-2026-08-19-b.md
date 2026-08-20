# Nocturno local — 2026-08-19-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la jerarquía).
**Branch:** `nocturno/local-2026-08-19-b-fuente-frescura` (pusheado, 2 commits: `a172a86` + `4bdc796`).
**Sale de:** `main`. **No depende de ningún otro branch nocturno** (ver "Una corrección de base", abajo).

## TL;DR

FrioSeguro se cobra con una promesa de una línea: **"el servicio avisa"**. Lo
único que el comerciante mira para creerla es un puñado de textos de frescura:
`● Online`, `hace 3 min`, `12s abierta`.

**Esa resta —`ahora − fecha`— estaba escrita cinco veces, en cinco archivos, sin
que ninguna supiera de las otras. Y las cinco fallaban en la MISMA dirección
peligrosa: ante una fecha futura o inválida, decían *fresco*.**

| dónde | qué mostraba mal |
|---|---|
| `AdminPanel.fmtRelative` | `diff` negativo ⇒ `d`/`h`/`m` ≤ 0 ⇒ cae en `'ahora'`. Con `NaN`, **todas** las comparaciones dan `false` y cae en el **mismo** `'ahora'`. |
| `DevicesAdminTable.fmtRelative` | copia **literal** de la anterior, con el mismo bug |
| `App.getReadingAge` | informaba **`hace -312 seg` con status `fresh`** (verde) |
| `App` (inline, tarjeta de puerta) | `-312s abierta` |
| `supabaseClient.computeIsOnline` | `age` negativo siempre es `< 2 min` ⇒ **online para siempre**, aunque el equipo esté muerto hace una semana |

Y un sexto, que apareció al ir a mirar el CSS: `getReadingAge(null)` devolvía
status `'offline'`, clase que **no existe** en `App.css` — así que el literal
**`Sin datos` se pintaba con la regla base `.reading-time`, que es verde**.

**Ahora hay una sola resta** (`web-dashboard/src/lib/freshness.js`) y una regla:

> Cuando no se puede afirmar que el dato es fresco, se dice que no se sabe.
> **Nunca verde por descarte.**

## Tarea elegida y por qué

Por rotación tocaba frioseguro (el primer turno de anoche fue galgas; los previos
datalogger 08-18-b y frioseguro 08-18). La jerarquía manda **PLATA**, así que
coincide.

Dentro del repo seguí el patrón que funcionó en el primer turno: **no abrir una
auditoría nueva, tomar un pendiente ya nombrado con su evidencia medida.** El
branch `08-16-b-cadena-tiempo` dejó siete hallazgos con dueño, y dos son de
`@frontend` con esta nota literal:

> *«T4 y T5 son dos líneas y son lo único que el cliente ve.»*

Elegí esos dos. `T1`/`T2`/`T3` son firmware y docs (el equipo no tiene reloj: eso
es una decisión de @firmware, no algo que se arregle de noche), `T6` es firmware,
`T7` es backend.

**Lo que encontré es más grande que "dos líneas"** — pero en la dirección buena:
el arreglo salió **más chico** que el código que reemplaza (**−40 líneas netas**
en los archivos tocados).

### Por qué una fecha futura no es un caso hipotético

Es la parte que justifica la noche, y sale del propio análisis del 08-16-b:

- Las fechas las estampa el reloj del **servidor** (Postgres `DEFAULT NOW()` en
  `readings`/`alerts`; el firmware manda la cadena `"now()"` para `last_seen_at`).
- La resta se hace contra el reloj del **navegador** de la PC del comercio.

Si esa PC está atrasada —cosa que pasa, y nadie la administra— **todo dato recién
llegado cae en el futuro** y el dashboard entero se queda clavado en verde. No
hace falta que nada se rompa: alcanza con un reloj mal puesto en el local.

## Qué hice

### 1. `web-dashboard/src/lib/freshness.js` — la única resta

`ageOf(fecha, now)` clasifica en cuatro y **todo lo demás cuelga de ahí**:

| kind | cuándo | qué se muestra |
|---|---|---|
| `missing` | `null` / `undefined` / `''` | `Sin datos` |
| `invalid` | `new Date(x)` da `NaN` | `fecha inválida` |
| `future` | más de 60 s adelante | `reloj desfasado` |
| `ok` | el resto | `ahora` / `hace 3m` / `hace 2h` / `hace 5d` |

Encima: `fmtRelative`, `readingAge`, `fmtDoorElapsed`, `isOnline`. `now` es un
parámetro inyectable — los tests no dependen del reloj de la máquina que los corre.

**Los 60 s de tolerancia de skew son deliberados.** Cubren el jitter normal entre
Postgres y el navegador, que no es un problema y **no debe alarmar**: sin esa
tolerancia, una lectura que llega 3 segundos "en el futuro" gritaría *reloj
desfasado* varias veces por minuto y la señal se volvería ruido. Más de 60 s ya
no es jitter: es un reloj mal puesto, y el operario tiene que enterarse.

### 2. Los cinco call sites, apoyados en el módulo

`AdminPanel.jsx`, `DevicesAdminTable.jsx` (las dos copias literales borradas),
`App.jsx` (la función y el inline de la puerta) y `supabaseClient.js`.

**El caso normal no cambia**: las mismas cadenas, los mismos umbrales de color
(`fresh` < 1 min, `stale` 1-5, `very-stale` > 5) y el **mismo** umbral de online
(2 min). **Cero regresión visual para un equipo sano** — eso es requisito, no
casualidad, y está fijado con tests que comparan contra los textos de siempre.

### 3. T4: la frescura ahora se muestra en las DOS ramas

Antes: `● Online` pelado, y la fecha **sólo** en la rama offline. Ahora
`● Online · hace 1m` en las dos. El operador nunca veía de cuándo era el dato
justamente en el estado en el que pasa el 99 % del tiempo.

### 4. El agujero de CSS

`.reading-time.unknown` (gris) en `App.css`. `Sin datos` dejó de ser verde.

### 5. `freshness.test.js` — 16 tests

Puros: sin DOM, sin red, sin hardware, ~0,1 s. Cubren los cuatro `kind`, la
frontera exacta de la tolerancia de skew, la **monotonía** (más viejo nunca se
lee como más fresco), la conservación literal de los textos de siempre, y un test
de coherencia final: si un renderer dice "no se sabe", **ninguno** de los otros
puede estar diciendo "fresco".

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-19-b-fuente-frescura
cd web-dashboard

node --test src\lib\freshness.test.js   # 16 tests, ~0,1 s
npm run build                            # vite
npx eslint src\
```

**Lo que verifiqué yo, corriendo:**

- **16/16 tests OK.**
- **`npm run build` OK** (vite 7.3.1, 1,4 s, 44 módulos).
- **`eslint src/`: exactamente los mismos 31 errores y 7 warnings que en `main`**
  — los comparé archivo por archivo contra un baseline con `git stash`. **Cero
  nuevos**, y los dos archivos nuevos salen limpios. (Los 31 son deuda vieja de
  `Login.jsx`, `SensorManager.jsx`, etc.; no los toqué.)
- **Mutación** — que los tests sean red y no decorado:

  | mutación | resultado |
  |---|---|
  | sacar la guarda de futuro de `ageOf` | **7 tests fallan** |
  | `isOnline` sin exigir `kind === 'ok'` | **2 fallan** |
  | `readingAge` devuelve `fresh` en futuro | **3 fallan** |
  | `fmtDoorElapsed` sin guarda | **2 fallan** |
  | tolerancia de skew en 0 | **1 falla** |

  Restaurado → 16/16 OK. **Ninguna mutación sobrevivió.**

## Lo que quedó sin verificar (necesita ojos / datos vivos)

1. **Nadie lo vio en pantalla.** El texto del badge cambió (`● Online · hace 1m`)
   y el copy de los tres estados nuevos (`Sin datos` / `fecha inválida` /
   `reloj desfasado`) es de **@diseno**. Es de **@tester**, con un device
   reportando: 10 minutos.
2. **`reloj desfasado` es una cadena que inventé yo.** Dice la verdad pero es
   media técnica para un carnicero. Si @diseno prefiere *"no se puede confirmar
   la hora"* o similar, se cambia en **un** lugar — que es todo el punto del
   módulo.
3. **Cuánto skew hay realmente en una PC de comercio: no medido.** Los 60 s son
   un número elegido con criterio, no medido en campo. Si aparece un local con el
   reloj corrido de a minutos, el número se discute (está exportado como
   `CLOCK_SKEW_TOLERANCE_MS`).

## Una corrección de base (vale anotarla como higiene)

Al ir a commitear descubrí que **el worktree de frioseguro había quedado parado
en el branch de anoche** (`08-18-fix-alert-delay-defrost`), así que mi branch
nació **apilado encima del firmware**. Eso es un problema real y no cosmético:
mergear "el fix del dashboard" habría arrastrado **en silencio** un cambio de
`firmware_modular/alerts.h` que todavía no se probó en banco.

Lo rebasé sobre `main` (cherry-pick del commit sobre `main` limpio, tests y build
re-corridos sobre la base nueva, reemplazo del ref remoto). **Sin `push --force`
y sin borrar nada de nadie**: el único ref que borré fue el que yo mismo había
pusheado cinco minutos antes, y su contenido está entero en el branch nuevo.

**Este branch se puede mergear solo, en cualquier orden, sin arrastrar nada.** Es
el primero de frioseguro en varias noches del que se puede decir eso.

## Lo que este branch NO toca

- **No toca el firmware**, ni el schema, ni Supabase, ni el umbral de 2 min de
  online, ni la lógica de alertas.
- **No resuelve T2** (el equipo sigue sin reloj). Arregla cómo se **muestra** una
  fecha, no de dónde **sale**. Mientras hay internet los dos relojes coinciden;
  se separan justo durante un corte, que es el escenario contra el que se vende
  el abono. **T2 sigue siendo de @firmware y sigue abierto.**
- **No tocó nada del trabajo sin commitear de Matías** (ver higiene).

## Nota para el Director

Segunda noche seguida en que la tarea la eligió **un pendiente ya nombrado por un
informe anterior**, no una búsqueda nueva. El 08-16-b escribió *«T4 y T5 son dos
líneas y son lo único que el cliente ve»* y eso alcanzó para arrancar sin
re-investigar nada.

Lo que agrega esta noche al patrón: **el hallazgo escrito era la punta.** El
informe hablaba de dos funciones; en el repo había **cinco copias de la misma
resta y un agujero de CSS**, todas fallando igual. La auditoría vio dos porque
buscó por síntoma; el arreglo encontró seis porque fue a buscar **todos los
lugares que hacen la misma cuenta**. Es exactamente la doctrina de *una sola
fuente de verdad*: el dato duplicado a mano se desincroniza y nadie lo ve.

La cola de merge de frioseguro sube a **19 branches sin mergear a `main`**. Éste
es el único que **sale de `main` y no depende de nadie**: si querés bajar el
contador con algo barato y verificable, es el candidato — `node --test` +
`npm run build` en 5 segundos, y lo que el cliente ve deja de mentir en la
dirección peligrosa.

---

**Higiene del cuartel:**

- ⚠️ **`C:\Proyectos\frioseguro` tiene trabajo de día SIN COMMITEAR y es MUCHO**:
  `REVIVAL_2026-08.md`, `firmware_revival/`, `kit_santacruz/` (con firmware, app,
  runbook, guardián y herramientas), `backup_supabase/`, `.build_revival/`, dos
  ZIP del kit Santa Cruz y `supabase/BOOTSTRAP_2026-08-19.sql` +
  `migration_device_logs.sql`. **No toqué nada de eso** — y verifiqué que los 9
  ítems siguen intactos después de mis cambios de branch. Matías: es el revival de
  Cerro Moro entero viviendo **sólo en este disco**. Commitealo.
- ⚠️ **MATI-HQ sigue con los mismos 16 modificados + 4 sin trackear** de los
  informes anteriores. **No los toqué ni los commiteé.** Este commit sólo agrega
  este informe.
- ℹ️ En `frioseguro` quedó un `stash@{0}` viejo (de julio, rama
  `nocturno/local-2026-07-07-frioseguro-particion-ota`), que **ya estaba antes**
  de esta noche. No es mío y no lo toqué.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío. El latido de DESKTOP-RK8DH7C
  sigue parado desde el **2026-08-07** (12 días).
