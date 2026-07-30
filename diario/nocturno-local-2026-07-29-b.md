# Nocturno local — 2026-07-29 (turno 22:00, 2do del día)

> Worker nocturno local (Matías durmiendo). El turno de las 2:00 de hoy ya hizo la
> caracterización de v_pp de galgas (`nocturno-local-2026-07-29.md`). Este es el 2do turno.

## Tarea elegida y por qué
**Hacer DRENABLE la cola de merge** — no producir un branch nuevo, sino atacar el cuello de
botella #1 que los últimos ~10 nocturnos vienen marcando: *"ya no falta trabajo de noche,
falta drenarlo de día con @verificador"*.

Por qué esta y no otra:
- El espacio de análisis offline de los 4 repos está **saturado**: galgas 13 branches
  nocturnos, datalogger 11, frioseguro 8, cosechador 1 = **34 sin mergear**. Cada branch
  nuevo AGRANDA el cuello, no lo achica. Galgas lleva 6 noches seguidas; el frente comercial
  de PLATA (pitch, precios, contrato, hoja mostrador, WhatsApp) está completo.
- La herramienta `tools/merge_queue_status.py` (creada el 07-27-b) es la palanca correcta,
  pero su reporte tenía un **defecto que hacía ver la cola más aterradora de lo que es** y le
  faltaba la señal que decide el orden de drenaje.
- 100% software/análisis, offline, **read-only** (sólo `git merge-tree`/`rev-list`, sin
  checkout/merge/reset), y vive en MATI-HQ main → **no suma un branch a la cola** (habría
  sido el #35). Mismo criterio que el 07-27-b.

## Qué hice
Corregí y extendí `tools/merge_queue_status.py` (MATI-HQ):

1. **Bug de conteo de conflictos (corregido).** `git merge-tree --write-tree --name-only`
   emite, ante conflicto: `<OID>` → archivos en conflicto → **línea en blanco** → mensajes
   informativos (`Auto-merging X`, `CONFLICT (content): …`). El parseo viejo tomaba
   `lines[1:]` entero, metiendo esos 2 mensajes como si fueran archivos → **reportaba "3
   archivos en conflicto" donde había 1**. Ahora corta en la primera línea en blanco.
2. **Clasificación doc vs código (nuevo).** Funciones puras `is_doc(path)` y
   `collision_kind(paths)` → cada conflicto/colisión se etiqueta `[SOLO docs — trivial]`,
   `[codigo — revisar]` o `[doc+codigo]`. Un choque en `QUE_FALTA.md`/`README.md` se resuelve
   tomando ambos lados; un choque en firmware/SQL exige revisión real. No es lo mismo y ahora
   el tool lo dice.
3. **Rollup accionable en la cabecera** del reporte: cuántos `LIMPIO-ADITIVO` (empezar acá),
   cuántos `REVISAR-STALE` de los cuales solo-docs, cuántos `CONFLICTO` de los cuales solo-docs.
4. **Salida ASCII-safe** (marcadores `[VERDE]/[AMBAR]/[ROJO]` en vez de emojis — la consola de
   Windows es cp1252 y reventaba con `✅`).
5. Regeneré el reporte fresco → **`COLA_MERGE_STATUS_2026-07-29.md`** (34 branches) y agregué
   banner de actualización 2026-07-29 en `COLA_MERGE_NOCTURNOS.md`.

### El hallazgo que des-asusta la cola (con evidencia git)
De **34 branches**:
- **9 LIMPIO-ADITIVO** → merge mecánico seguro (empezar por acá).
- **14 REVISAR-STALE**, de los cuales **10 tocan solo docs** (revisión de 1 minuto).
- **8 CONFLICTO**, de los cuales **los 8 son SOLO `QUE_FALTA.md`** — **0 tocan firmware/código**.

Es decir: el "atasco" de galgas (6 CONFLICTO) es un único archivo de bitácora que cada
nocturno amplía, no un choque de firmware. Se drena tomando ambos lados del `.md`. Los únicos
branches que tocan código real y merecen a @verificador sentado: datalogger `07-08-ecolora-fixes`
(doc+código, 8 atrás), galgas `07-09-rx-deuda-verificador` (arrastra 6 binarios de build),
frioseguro `07-11/07-13-resumen-mensual` (conflicto de código, ya conocido).

## Cómo verificarlo (comandos exactos)
```bash
cd "C:/Users/Pandemonium/Documents/MATI-HQ"
python -m unittest tools.test_merge_queue_status      # 23 tests, OK (eran 12; +11 nuevos)
python -X utf8 tools/merge_queue_status.py            # reporte en vivo, <10 s, sin error
# Prueba del bug corregido — antes decía 3, ahora 1:
git -C C:/Proyectos/galgas merge-tree --write-tree --name-only main \
    nocturno/local-2026-07-28-b-scada-monitor-threshold | cat -A   # OID, QUE_FALTA.md, blank, 2 msgs
```
Tests nuevos: `TestIsDoc`, `TestCollisionKind`, y en `TestClassify` los casos de conflicto
solo-docs / código / mixto y stale solo-docs. Los 12 tests originales de `classify` siguen
pasando sin cambios (el contrato de la función no se rompió).

## Qué quedó sin verificar por hardware
Nada aplica — tarea 100% offline/git. **Ninguna verificación pendiente.**

## Branch
**No hay branch nocturno**: como el tooling del 07-27-b (`merge_queue_status.py`,
`COLA_MERGE_STATUS_2026-07-27.md`), esto es tooling+doc del cuartel → va **directo a MATI-HQ
main**. Crear un branch nocturno acá sería contraproducente: la tarea EXISTE para achicar la
cola, no para agregarle el branch #35. (Los 4 repos de trabajo no se tocaron.)

## Nota para @cronista (drift menor detectado, NO tocado)
`dominios/comercial.md` → sección "Material producido": PITCH.md, PRECIOS_FRIOSEGURO.md,
`hoja_mostrador*.html` y CONTRATO_BORRADOR.md **existen y están completos** pero figuran como
`[ ]` sin marcar. Marcarlos `[x]` en una pasada de sync (no lo hice para no salir de scope).
