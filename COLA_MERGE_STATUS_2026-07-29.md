# Estado de la cola de merge (regenerado con git en vivo)

> Generado por `tools/merge_queue_status.py`. Metrica de merge = arbol 3-way real (`merge-tree --write-tree`) diffeado contra main, NO `diff main..branch`.
> Solo lectura: el tool no hace checkout/merge/reset ni toca refs.

**34 branches nocturnos** en 4 repos.

**Lectura rapida (drenaje):**
- **[VERDE] 9 LIMPIO-ADITIVO** — merge mecanico seguro, empezar por aca.
- **[AMBAR] 14 REVISAR-STALE**, de los cuales **10 tocan solo docs** (revision de 1 minuto: que no reviertan el estado actual del .md).
- **[ROJO] 8 CONFLICTO**, de los cuales **8 son SOLO docs** (triviales: tomar ambos lados; el conflicto es de bitacora, no de firmware). Solo 0 tocan codigo/config.

## C:/Proyectos/galgas  ·  main=main (4 commits)
| Branch | Atras | Merge | +A | ~M | -D | Estado | Nota |
|---|--:|---|--:|--:|--:|---|---|
| `…2026-07-09-rx-deuda-verificador` | 2 | limpio | 8 | 4 | 0 | **BINARIOS** | arrastra 6 binario(s)/artefacto(s) de build |
| `…2026-07-11-vpp-threshold-audit` | 2 | CONFLICTO | - | - | - | **CONFLICTO** | 1 archivo(s) en conflicto [SOLO docs — trivial, tomar ambos lados]: QUE_FALTA.md |
| `…2026-07-15-energy-budget` | 2 | limpio | 3 | 1 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 1 archivo(s) [solo docs] desde base 2 atras: QUE_FALTA.md — revisar que no reviertan main |
| `…2026-07-16-alert-hold-replay` | 2 | CONFLICTO | - | - | - | **CONFLICTO** | 1 archivo(s) en conflicto [SOLO docs — trivial, tomar ambos lados]: QUE_FALTA.md |
| `…2026-07-16-b-docs-entrada` | 2 | limpio | 0 | 4 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 4 archivo(s) [solo docs] desde base 2 atras: CLAUDE.md, QUE_FALTA.md, README.md, docs/INDEX.md — revisar que no reviertan main |
| `…2026-07-17-linaje-firmware` | 2 | CONFLICTO | - | - | - | **CONFLICTO** | 1 archivo(s) en conflicto [SOLO docs — trivial, tomar ambos lados]: QUE_FALTA.md |
| `…2026-07-19-rx-detection-replay` | 2 | CONFLICTO | - | - | - | **CONFLICTO** | 1 archivo(s) en conflicto [SOLO docs — trivial, tomar ambos lados]: QUE_FALTA.md |
| `…2026-07-20-b-ota-decision-model` | 2 | limpio | 3 | 1 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 1 archivo(s) [solo docs] desde base 2 atras: QUE_FALTA.md — revisar que no reviertan main |
| `…2026-07-21-b-readme-drift` | 2 | limpio | 0 | 0 | 0 | **YA-EN-MAIN** | sin commits mas alla de main — nada que mergear, borrar la rama |
| `…2026-07-22-readme-drift` | 2 | limpio | 0 | 2 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 2 archivo(s) [solo docs] desde base 2 atras: QUE_FALTA.md, README.md — revisar que no reviertan main |
| `…2026-07-23-firmware-check-edge` | 2 | limpio | 4 | 1 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 1 archivo(s) [solo docs] desde base 2 atras: QUE_FALTA.md — revisar que no reviertan main |
| `…2026-07-27-readme-drift` | 2 | limpio | 0 | 2 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 2 archivo(s) [solo docs] desde base 2 atras: QUE_FALTA.md, README.md — revisar que no reviertan main |
| `…2026-07-28-b-scada-monitor-threshold` | 2 | CONFLICTO | - | - | - | **CONFLICTO** | 1 archivo(s) en conflicto [SOLO docs — trivial, tomar ambos lados]: QUE_FALTA.md |
| `…2026-07-29-vpp-field-characterization` | 1 | CONFLICTO | - | - | - | **CONFLICTO** | 1 archivo(s) en conflicto [SOLO docs — trivial, tomar ambos lados]: QUE_FALTA.md |

## C:/Proyectos/datalogger  ·  main=main (10 commits)
| Branch | Atras | Merge | +A | ~M | -D | Estado | Nota |
|---|--:|---|--:|--:|--:|---|---|
| `…2026-07-07-ina219-ecolora` | 8 | limpio | 3 | 7 | 0 | **SUBSUMIDO** | ancestro de nocturno/local-2026-07-08-ecolora-fixes — drenar solo ese |
| `…2026-07-08-ecolora-fixes` | 8 | limpio | 3 | 9 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 9 archivo(s) [doc+codigo] desde base 8 atras: CHANGELOG.md, QUE_FALTA.md, firmwares/esp32s3-com11/esp32_dashboard/esp32_dashboard.ino, firmwares/pico2w-node/config.py — revisar que no reviertan main |
| `…2026-07-09-sd-integrity` | 6 | limpio | 3 | 1 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 1 archivo(s) [solo docs] desde base 6 atras: QUE_FALTA.md — revisar que no reviertan main |
| `…2026-07-10-rssi-calib` | 6 | limpio | 3 | 2 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 2 archivo(s) [doc+codigo] desde base 6 atras: QUE_FALTA.md, firmwares/pico2w-node/nodo.py — revisar que no reviertan main |
| `…2026-07-15-sd-integrity` | 6 | limpio | 3 | 1 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 1 archivo(s) [solo docs] desde base 6 atras: QUE_FALTA.md — revisar que no reviertan main |
| `…2026-07-17-b-ssid-casing` | 6 | limpio | 2 | 4 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 4 archivo(s) [doc+codigo] desde base 6 atras: QUE_FALTA.md, firmwares/pico2w-node/eco.py, firmwares/pico2w-node/ota.py, firmwares/pico2w-node/wifi_push.py — revisar que no reviertan main |
| `…2026-07-19-b-rv1-mesh-model` | 6 | limpio | 3 | 1 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 1 archivo(s) [solo docs] desde base 6 atras: QUE_FALTA.md — revisar que no reviertan main |
| `…2026-07-21-eco-schedule-model` | 6 | limpio | 3 | 1 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 1 archivo(s) [solo docs] desde base 6 atras: QUE_FALTA.md — revisar que no reviertan main |
| `…2026-07-25-b-ina219-extract` | 0 | limpio | 2 | 1 | 0 | **LIMPIO-ADITIVO** | solo agrega archivos — drenaje mecanico seguro |
| `…2026-07-25-sd-integrity-rebase` | 0 | limpio | 2 | 1 | 0 | **LIMPIO-ADITIVO** | solo agrega archivos — drenaje mecanico seguro |
| `…2026-07-26-stale-cluster-extract` | 0 | limpio | 9 | 1 | 0 | **LIMPIO-ADITIVO** | solo agrega archivos — drenaje mecanico seguro |

## C:/Proyectos/frioseguro  ·  main=main (13 commits)
| Branch | Atras | Merge | +A | ~M | -D | Estado | Nota |
|---|--:|---|--:|--:|--:|---|---|
| `…2026-07-11-b-resumen-mensual` | 10 | CONFLICTO | - | - | - | **CONFLICTO** | 1 archivo(s) en conflicto [SOLO docs — trivial, tomar ambos lados]: QUE_FALTA.md |
| `…2026-07-13-resumen-mensual-fixes` | 10 | CONFLICTO | - | - | - | **CONFLICTO** | 1 archivo(s) en conflicto [SOLO docs — trivial, tomar ambos lados]: QUE_FALTA.md |
| `…2026-07-14-vista-estabilidad-comercio` | 2 | limpio | 0 | 3 | 0 | **REVISAR-STALE** | limpio+aditivo pero modifica 3 archivo(s) [codigo] desde base 2 atras: web-dashboard/src/App.css, web-dashboard/src/App.jsx, web-dashboard/src/supabaseClient.js — revisar que no reviertan main |
| `…2026-07-18-alert-model` | 1 | limpio | 3 | 0 | 0 | **LIMPIO-ADITIVO** | solo agrega archivos — drenaje mecanico seguro |
| `…2026-07-20-door-alert-model` | 0 | limpio | 3 | 1 | 0 | **LIMPIO-ADITIVO** | solo agrega archivos — drenaje mecanico seguro |
| `…2026-07-23-b-retencion-datos` | 0 | limpio | 3 | 3 | 0 | **LIMPIO-ADITIVO** | solo agrega archivos — drenaje mecanico seguro |
| `…2026-07-24-scan-secrets-sbkeys` | 0 | limpio | 0 | 4 | 0 | **LIMPIO-ADITIVO** | solo agrega archivos — drenaje mecanico seguro |
| `…2026-07-26-b-provision-device` | 0 | limpio | 3 | 2 | 0 | **LIMPIO-ADITIVO** | solo agrega archivos — drenaje mecanico seguro |

## C:/Proyectos/cosechador  ·  main=main (2 commits)
| Branch | Atras | Merge | +A | ~M | -D | Estado | Nota |
|---|--:|---|--:|--:|--:|---|---|
| `…2026-07-18-modelo-energia` | 0 | limpio | 4 | 2 | 0 | **LIMPIO-ADITIVO** | solo agrega archivos — drenaje mecanico seguro |

