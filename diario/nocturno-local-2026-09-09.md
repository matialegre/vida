# Nocturno local — 2026-09-09

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (**P0** — RuView/GIMAP, *"terminarlo
primero, antes del trabajo Dreyfus"*, orden de Matías del 07-07), zona
`firmwares/nodo-gimap/` + `visor_gimap.py` + `tools/`.
**Branch:** `nocturno/local-2026-09-09-el-acelerometro-que-dice-cero`
(pusheado, `222663a`).
**⚠ Sale de `nocturno/local-2026-09-06-el-hueco-que-no-se-ve` (`9b35eda`)**, que
sale del 09-04, que sale de `nodo-gimap/wifi-y-flasheo-2026-08-24`. **Al mergear
éste entran los tres**: no hace falta mergearlos aparte.
**Nunca hubo mDNS de por medio.** No se tocó nada de galgas ni de frioseguro.

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_datalogger_0909`,
ya eliminado) porque el árbol de `datalogger` tiene 6 archivos modificados y 3
sin trackear de Matías, y un `checkout` los habría tocado. **Verificado al
terminar: los dos árboles (`datalogger` y `datalogger-gimap`) quedaron
idénticos**, en los branches donde estaban.

---

## TL;DR

> **El nodo miraba el acelerómetro una sola vez, al arrancar.** Si no estaba,
> transmitía `ax..gz = 0` **para siempre**, a 200 Hz, adentro de un paquete que
> declara `fs=200` y que la pantalla dibuja como una recta perfecta. **Un
> MPU6050 desconectado y una mesa quieta se veían exactamente igual**, y el JSON
> de estado —que ya publicaba batería, RSSI, `gaps`, cortes de WiFi y errores de
> envío— **no tenía un solo campo del sensor**. En el banco de vibraciones eso
> es un ensayo entero corrido, el CSV lleno, el visor dibujando, y el resultado
> "no vibró nada". Y la otra mitad: si el bus se caía **a mitad de la corrida**,
> la excepción subía hasta el `try` del final de `main.py`, que **reinicia el
> nodo entero** — llevándose puesto el canal de piezos, que estaba sano.

## Por qué esta tarea

1. **La dejaron marcada las dos noches anteriores de este repo.** El informe del
   09-06 dice textual: *"si el MPU6050 no responde, `main()` avisa 3 s y después
   transmite `ax..gz = 0` para siempre, indistinguible de un acelerómetro
   quieto, y el estado no publica ningún campo que lo diga. **Candidato claro
   para la próxima noche**"*. Y el 09-04 lo había dejado anotado antes.
2. **Cierra la doctrina que ya rige el resto de la cadena.** *"Un visor sin
   datos no miente"* está resuelto desde hace semanas (sin paquetes, la pantalla
   se vacía) y el 09-06 cerró *"si llegan incompletos, también lo dice"*. Lo que
   faltaba es el caso peor: **llegan completos, puntuales y son mentira**.
3. **Es la cadena que Matías va a enchufar**: el nodo GIMAP + el visor son lo
   que se usa en el banco de vibraciones.
4. **Se hace entera sin hardware** y no colisiona con ningún branch abierto.
5. Le tocaba a `datalogger` por rotación: las tres noches anteriores fueron
   frioseguro (PLATA) y galgas (octubre), y este repo no se toca desde el 09-06.

## Los tres modos de falla, que no son el mismo

| | qué pasa | qué se veía antes |
|---|---|---|
| **ausente** | no contesta el WHO_AM_I | sólo se detectaba **al arrancar**; un cable que se suelta a los diez minutos no lo veía nadie |
| **mudo** | el bus empieza a tirar `OSError` | **reiniciaba el nodo entero** a los 30 s, y con él el canal de piezos |
| **congelado** | contesta, no tira error, devuelve **siempre lo mismo** | nada. Es el más peligroso porque es el más creíble |

`congelado` no es hipotético: pasa con el MPU en reset (todo cero), con el bus
trabado en alto (todo `0xFFFF`) y con un módulo alimentado a medias.

> Es el mismo patrón que la sonda congelada de FrioSeguro (09-04-b) y el "OK
> vacío" de galgas (08-28): el sistema no falla, contesta bien y dice otra cosa.

## La trampa que ordenó el diseño

**No se puede declarar congelado por dos lecturas repetidas.** El MPU6050 tiene
su propia tasa interna (`SMPLRT_DIV`): si el lazo lee más rápido que ella, lee
**dos veces el mismo registro**, y esa repetición es correcta.

Por eso el umbral está en **segundos** (2 s = 400 muestras a 200 Hz) y no en
muestras, y por eso el estado publica **`repetidas_max`**: es el único número de
todo esto que no se puede estimar desde la PC, y sirve para ver cuánto margen
real hay contra el umbral.

## Qué se entregó

`firmwares/nodo-gimap/salud_mpu.py` — **puro** (sin `machine`, sin I2C, sin
reloj, sin `print`) e **incluido** por `main.py`: no es un espejo, lo que se
testea es lo que se flashea. Mismo criterio que `continuidad_gimap.py` (09-06),
`ota_rescue.h` y `fw_version.h` de galgas, y los `*_model.h` de FrioSeguro.

Cuatro reglas, todas con su motivo escrito:

- **Histéresis simétrica**: 5 errores seguidos para caer, 5 lecturas buenas **y
  distintas** para volver. Asimétrica, un bus flojo parpadea varias veces por
  segundo.
- **Una lectura repetida no es prueba de vida**: un sensor clavado que cambia
  una sola vez cada tanto no se recupera solo.
- **Mientras no esté sano, no se lo lee**: cada lectura fallida cuesta el
  timeout del I2C y a 200 Hz eso desarma la cadencia del **canal de piezos**,
  que no tiene la culpa de nada.
- **El reintento pregunta antes de pagar**: cada 5 s hace `presente()` (un byte,
  microsegundos) y sólo si el chip contesta paga el `iniciar()` que lo resetea y
  duerme 110 ms. Después la cadencia se re-ancla, así que ese pozo no se cobra
  como decenas de `gaps`.

**El formato del paquete NO cambió**, a propósito: tocar la trama toca el
firmware, `rx_gimap.py`, el visor, el emisor sintético y el test de protocolo, y
es una decisión de contrato, no un fix de noche. El nodo **sigue mandando
ceros**; lo que cambia es que **esos ceros dejaron de afirmar algo**. Quien dice
si valen es el JSON de estado, que es canal aparte y de formato abierto.

Y los tres consumidores hacen algo con eso:

- **el nodo**: LED en `ERR_MPU` toda la corrida (cede sólo ante la batería, que
  es lo único que puede romper algo si se ignora) y una línea en el log serie;
- **el visor**: **vacía** los paneles de acelerómetro y giróscopo con el cartel
  y el motivo textual del nodo. **Los dos piezos se siguen dibujando**;
- **`rx_gimap.py`**: columna **`mpu_ok`** al final del CSV — `si` / `no` / **`?`**
  para nodos viejos, porque *no saber* no es lo mismo que *estar bien*.

## Cómo verificarlo (comandos exactos, sin hardware, ~5 minutos)

```bash
cd C:\Proyectos\datalogger
git fetch origin
git checkout nocturno/local-2026-09-09-el-acelerometro-que-dice-cero

# 1) la decision, contra el modulo que se flashea
python tools/test_salud_mpu.py

# 2) que los tests sirvan: reimplantar los defectos y ver que mueran
python tools/test_salud_mpu.py --mutantes

# 3) el JAVASCRIPT REAL del visor, corrido con node (sin navegador)
python tools/test_visor_js.py

# 4) las 9 suites del repo, sin regresion
for %t in (tools\test_*.py) do python %t

# 5) de punta a punta, sin desoldar nada (dos ventanas)
python visor_gimap.py
python emisor_prueba_SIN_HARDWARE.py --destino 127.0.0.1 --mpu ausente
#   -> los dos paneles de arriba VACIOS, los dos piezos latiendo
#   -> probar tambien --mpu congelado y --mpu mudo
```

**Resultados obtenidos esta noche:**

- `test_salud_mpu.py` → **85 chequeos, 0 fallos**. Los bloques marcados
  REGRESIÓN fallan contra el código viejo. No es sólo lógica: hay **cableado
  real** verificado por AST — que `mpu.leer()` esté dentro de un `try` en
  `main.py`, y que `flashear_nodo.py` copie el archivo nuevo.
- `--mutantes` → **12/12 muertos**, y ninguno sobrevivió sin que tuviera que
  endurecer el test primero (tres sobrevivieron en la primera vuelta).

  | mutante | qué reimplanta | checks que fallan |
  |---|---|---|
  | 1 | el congelado no se detecta nunca | 9 |
  | 2 | dos repetidas ya son congelado (las produce la tasa interna del MPU) | 1 |
  | 3 | un solo error de bus declara mudo | 1 |
  | 4 | histéresis asimétrica: una lectura buena lo declara sano | 1 |
  | 5 | se lee el bus caído en cada ciclo (se come la cadencia de los piezos) | 5 |
  | 6 | se reintenta en cada ciclo: el chip vive reseteándose | 3 |
  | 7 | no se reintenta nunca: un cable que se acomoda no vuelve solo | 3 |
  | 8 | el estado publica `ok` siempre (la mentira que esto vino a arreglar) | 3 |
  | 9 | una lectura repetida cuenta como prueba de vida | 1 |
  | 10 | el umbral de congelado deja de seguir a la `fs` | 6 |
  | 11 | reiniciar el chip no borra el rastro de la lectura anterior | 1 |
  | 12 | la muestra se da por buena aunque el sensor no lo esté | 1 |

- **`test_visor_js.py` → 14 chequeos, 0 fallos.** Esto es nuevo en el repo: la
  mitad del visor que decide **qué se dibuja** vive en el `<script>` de la
  página, y hasta hoy sólo se chequeaba que ciertos textos estuvieran en el
  archivo — *"está el string"* no es *"hace lo que dice"*. El test agarra el
  mismo `PAGINA` que se le manda al navegador, le pone un DOM y un `fetch` de
  mentira, lo corre con **node v24.14.0** y mide **qué le llegó a cada canvas**:
  con el MPU caído, el acelerómetro sale con **0 tramos de señal** y el cartel;
  los dos piezos, con **1798**. También cubre los dos casos donde **no hay que
  afirmar nada**: nodo viejo que no manda el campo, y JSON de estado rancio.
- **De punta a punta** contra `127.0.0.1` con el emisor sintético (`--mpu
  ausente`, opción nueva): `/datos` devolvió `mpu.ok=false`, `estado:"ausente"`
  con su motivo, las **600 muestras de `ax` en cero** y el piezo picando 45000.
- **Sin regresión**: las **9** suites de `tools/` en verde. La del reenganche
  (09-04) hubo que tocarla: su doble del MPU devolvía **siempre la misma
  lectura**, así que con esto puesto se declaraba congelado sola. Ahora varía en
  cada lectura, y además el test carga el `salud_mpu.py` **de verdad** (es puro),
  no un doble: de paso comprueba que el reenganche de WiFi sigue funcionando con
  la salud del acelerómetro cableada adentro.

## ⚠️ Al publicar el OTA va el LOTE — leer antes de flashear

`salud_mpu.py` es **archivo nuevo**. Un OTA que publique sólo `main.py` deja al
nodo importando un módulo que no está: arranca mal, y a los 3 intentos `boot.py`
restaura los `.bak` y vuelve a 1.0.6 — el paracaídas funciona, pero el update no
entra y el síntoma se lee como "el OTA no anda".

```
python publicar_ota.py 1.0.7 main.py salud_mpu.py
```

Por USB no hay nada que recordar: `flashear_nodo.py` ya lo tiene en la lista (y
el test lo verifica por AST, porque esa lista **ya causó un arranque fallido**
antes con `celda.py`).

## Qué quedó SIN verificar (pide el nodo enchufado)

1. **Desenchufar el MPU con el nodo andando** y ver la transición entera: panel
   vacío, LED en `ERR_MPU`, cartel con el motivo — y la **recuperación sola** al
   volver a enchufarlo, sin reiniciar nada. 10 minutos con el Pico y el visor
   abierto. [@firmware]
2. **⚠️ `repetidas_max` con el sensor sano y la mesa quieta.** Es el único
   número de todo esto que **no se puede estimar desde la PC**: sale de mirar el
   estado después de una corrida real. El razonamiento dice que con ruido
   térmico las seis cuentas no se repiten 400 veces seguidas, **pero eso no está
   medido**. Si diera cerca de 400, el umbral hay que subirlo o el nodo se va a
   declarar congelado a sí mismo. [@muestreador]
3. **El costo real del reintento**: los 110 ms de `iniciar()` salen del
   `sleep_ms(100)` del reset más margen. Se miden contando `gaps` en una corrida
   con el MPU desenchufado a propósito.
4. **El LED**: en la Pico 2 W va por el chip de WiFi, y esto no cambió cómo se
   maneja — pero `ERR_MPU` durante la corrida nunca se miró en la placa.

## Lo que NO hice, a propósito

- **No le puse un bit de validez a la trama.** Sería lo "correcto" y es
  exactamente lo que el 09-06 ya dejó dicho sobre el tiempo propio del paquete:
  cambiar el formato toca el firmware, `rx_gimap.py`, el visor, el emisor y el
  test de protocolo, y obliga a flashear todo junto. Es una decisión de
  contrato. Mientras tanto el JSON de estado lo dice, que es canal aparte y
  gratis. **Si algún día se abre la trama, los dos cambios van juntos**
  (validez + microsegundos). [@muestreador]
- **No toqué los piezos.** `Piezos.leer()` no puede fallar (es un ADC interno),
  pero **sí puede quedar clavado** un front-end del MCP6004 sin alimentación. El
  criterio de "congelado" no se aplica igual: una envolvente de piezo en reposo
  **sí** da un valor constante durante segundos, que es lo normal. Distinguirlo
  necesita mirar el ruido de la línea de base, y eso es otra noche y otro
  modelo. [@muestreador]
- **No corregí `seq` como `uint32`** (revienta a los ~27 años de encendido
  continuo, anotado el 09-06). Sigue sin valer la pena.

## Anotado y NO tocado

- **`main` de `datalogger` sigue con `visor.log` y dos herramientas sin trackear
  en el árbol de Matías** (`tools/check_sd_integrity.py`,
  `tools/test_integridad_sd.py`) más `firmwares/nodo-gimap/` sin trackear. Es
  trabajo suyo a medio hacer, no lo toqué. **Tercera noche que se anota.**
- **La numeración de `QUE_FALTA.md` de este repo va por letras** (5b del 09-04,
  5c del 09-06, **5d** de éste) para no correr las referencias a `#14`. Al
  mergear los tres conviene renumerar de una vez. [@cronista]
- **`salud_mpu.py` es candidato a la biblioteca**, y **`test_visor_js.py`
  todavía más**: el harness de correr el JS de una página con node y medir qué
  le llegó a cada canvas sirve para el panel de FrioSeguro y para el dashboard
  de galgas, que hoy no tienen nada parecido. No los coseché porque ninguno se
  probó en hardware todavía. [@bibliotecario]

## Estado al cerrar

- Branch pusheado: `nocturno/local-2026-09-09-el-acelerometro-que-dice-cero`
  (`222663a`), sobre `nocturno/local-2026-09-06-el-hueco-que-no-se-ve`
  (`9b35eda`).
- `QUE_FALTA.md` de datalogger actualizado (ítem 5d).
- Worktree `C:\Proyectos\_noche_datalogger_0909` eliminado; `datalogger` quedó
  **idéntico** (los 6 modificados + 3 sin trackear de Matías, intactos, en el
  branch `08-31`) y `datalogger-gimap` limpio en `3491b72`.
- En MATI-HQ quedaron **sin commitear, tal como los encontré**,
  `comercial/panamerican/PRESUPUESTO_CERRO_MORO_INTERNO.html`, `dominios/pcb.md`
  y `scripts/turno_noche_log.txt`: son de otro trabajo y no me corresponde
  firmarlos.
- Nada corriendo, nada abierto.
