---
name: ota-nunca-ladrillo
description: Regla dura de Matías - ningún nodo puede quedar irrecuperable por una reprogramación fallida; el OTA siempre tiene que tener rollback
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 45f06a6c-47d0-42b1-91a3-6559cf5c9e34
  modified: 2026-08-25T23:32:30.592Z
---

Matías (2026-08-25, a los gritos y con razón): **"no puede existir bajo ningún concepto que si lo ponemos con una fuente no se pueda reprogramar por OTA y que haya un error reprogramándolo y perderlo"**. Vale para TODOS los nodos: datalogger GIMAP, FríoSeguro, drive del torno, galgas.

**Why:** los nodos terminan instalados donde no se llega — Santa Cruz a 1.500 km, la planta de Dreyfus en parada, un freezer de un cliente. Un nodo que necesita cable es un nodo perdido. Verificar el sha256 NO alcanza: cubre la descarga cortada, pero no el archivo que baja perfecto y no arranca (un import que falta, un error de lógica). Eso ya pasó: `flashear_nodo.py` no copiaba `celda.py` y ningún hash lo iba a detectar.

**How to apply:** todo esquema de OTA que se diseñe o se toque tiene que tener, además del hash:
1. **Lote atómico** — bajar todo a temporales, verificar todos los hashes, y recién ahí pisar.
2. **Copia de seguridad** — `<archivo>.bak` antes de reemplazar.
3. **Rollback automático por arranques fallidos** — un `boot.py` (o equivalente que corra ANTES del código de aplicación) que cuente arranques, que la app ponga en cero al llegar a operativo, y que restaure los `.bak` solo a los N fallidos. Todo dentro de `try/except`: si esa capa explota no hay nadie más abajo.
4. **Probarlo con un control negativo** antes de mandarlo: con un hash malo en el lote, ningún archivo se toca.

Implementado y probado en `C:\Proyectos\datalogger` (`firmwares/nodo-gimap/ota.py` + `boot.py`, `tools/test_ota_gimap.py`, 16 checks). Ese es el patrón a copiar; candidato a cosechar en la [[biblioteca-codigo-reusable]].
