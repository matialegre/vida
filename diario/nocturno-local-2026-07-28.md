# Nocturno LOCAL — 2026-07-28 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
Escribí las **plantillas de WhatsApp Business** del servicio de monitoreo de frío
(`comercial/plantillas_whatsapp.md`): el único deliverable de **PLATA** (categoría 1, la cima de la
jerarquía) que estaba **genuinamente pendiente, sin tachar y 100% offline**. Era el **item #13 de
`frioseguro/QUE_FALTA.md`** y el `[ ]` "Plantillas WhatsApp Business" de `dominios/comercial.md`.
16 secciones §A–§P: las 12 plantillas del funnel (§A–§L: primer contacto → demo → follow-ups → cierre →
onboarding → alerta real → conversión de piloto → cobro → retención → reactivación) + objeciones en
versión chat (§M, 6 respuestas) + upsell/cross-sell/referido (§N/§O/§P) + config de la cuenta. **Todo anclado y verificado contra PITCH/PRECIOS/guion_visita/CONTRATO** — mismos
precios, mismo disclaimer legal, sin nombrar "FrioSeguro". Es un **borrador para que Matías ajuste el
tono**; falta solo completar `[MARCA]`, CBU/alias, número y grabar UNA vez el video-demo.
**Entregable en MATI-HQ main** (cuartel, donde vive TODO el material comercial hermano).

## Tarea elegida y por qué
**Plantillas de WhatsApp Business para el funnel de FrioSeguro** (item #13).
- **Es PLATA = categoría 1, la cima de la jerarquía** (empatada con universidad, por encima de octubre).
  El worker nocturno viene sirviendo casi solo a octubre (galgas) porque **todos los bloqueantes de
  PLATA son hardware o decisión humana** (flashear, caja estanca, precio, SIM real…). Este es **la
  excepción**: el único item de FrioSeguro que es puro software/docs, offline, y NO estaba en ningún
  branch ni tachado. Romper 2 noches de meta-trabajo (drift + tooling de merge) con contenido real que
  mueve la aguja hacia "1 abono cobrado antes del 18-ago" es lo correcto dado el estado.
- **Genuinamente pendiente y NO en un branch:** el `[ ]` seguía sin tachar en `dominios/comercial.md`
  desde el 07-07, y `grep -ril whatsapp` no encontró ningún archivo dedicado de plantillas (solo
  menciones sueltas en guion/hoja/precios). No lo inventé: es el material que faltaba del funnel.
- **Anti-especulativo y verificable sin hardware:** no inventé precios ni claims — cada número y cada
  frase sale de las fuentes ya escritas por @comercial/@diseno; la "verificación" es la **consistencia
  con esas fuentes** (checklist al pie del archivo, todo ✔).
- **Cero riesgo de timeout** (disciplina 07-07): docs puros, sin red/nube/compilación/hardware. No toca
  firmware, backend, ni `data/field_captures` (ni mirado). No es decisión de plata: el precio ya está
  decidido en PRECIOS_FRIOSEGURO.md, yo solo lo reflejo.

## Por qué NO otra tarea (descarte honesto)
- **Otro modelo/test offline (galgas/datalogger/cosechador):** el sistema lleva ~10 noches gritando que
  el cuello es **merge humano, no producción** (COLA_MERGE = 32 branches). Un branch #28 tendría valor
  negativo. Ya lo dijeron 07-24/07-27/07-27-b.
- **Fix de firmware del hallazgo alert-model (frioseguro #18):** es firmware que toca el core que se
  cobra y el propio branch 07-18 lo dejó marcado "para que @firmware lo confirme en hardware" — no se
  aplica a ciegas de noche (generator ≠ evaluator).
- **Más drift de docs (fallback del paso 5):** ya se hizo 2 noches seguidas. Había una tarea de
  categoría MÁS ALTA disponible → esa gana.

## Qué hice
1. **Confirmé el hueco antes de escribir** (no manufacturar trabajo): `grep -ril whatsapp` en el cuartel
   → menciones sueltas pero **ningún archivo de plantillas**; el `[ ]` de `dominios/comercial.md` seguía
   sin tachar. Item #13 real y pendiente.
2. **Leí las 4 fuentes para anclar** (PITCH.md, PRECIOS_FRIOSEGURO.md, guion_visita.md,
   CONTRATO_BORRADOR.md) y extraje los invariantes: precios recomendados ($70k/$45k/$25k + upsell
   $10–15k), cobro del 1 al 10, disclaimer de la cláusula 2ª, regla no-nombrar-FrioSeguro, "desarrollado
   PARA Panamerican", piloto único 30 días / garantía 60 días, cerrar-con-fecha, cross-sell Modulia.
3. **Escribí `comercial/plantillas_whatsapp.md`** (quirúrgico, práctico, rioplatense):
   - **6 reglas madre** al tope (las que atraviesan todas las plantillas) + tabla de precios de referencia.
   - **Config de la cuenta** (perfil, bienvenida, ausencia, respuestas rápidas con atajos `/`, y
     **etiquetas mapeadas al pipeline** de `dominios/comercial.md` → el WhatsApp ES el CRM).
   - **16 plantillas del funnel** (§A–§P): primer contacto, envío de demo, 2 follow-ups, confirmar fecha,
     recordatorio pre-instalación, onboarding día 1, **aviso de alerta real** (el momento de mayor valor),
     conversión del piloto a abono, cobro mensual, resumen mensual de retención, reactivación de dormido,
     objeciones versión chat (las 5 de PITCH + una 6ª de disclaimer), upsell relé, cross-sell Modulia,
     pedido de referido/testimonio.
   - **"Qué NO hacer por WhatsApp"** + **checklist de consistencia verificado** contra las fuentes.
4. **Taché el item** en `dominios/comercial.md` (`[x]` + entrada de bitácora con lo que falta para Matías).

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
cd C:\Users\Pandemonium\Documents\MATI-HQ
# El archivo existe y tiene las 16 secciones §A..§P (12 plantillas nivel 3 + M/N/O/P nivel 2):
(Select-String -Path comercial\plantillas_whatsapp.md -Pattern '^#{2,3} [A-P] ').Count   # -> 16
# Consistencia de precios con la fuente (mismos numeros):
Select-String -Path comercial\plantillas_whatsapp.md,comercial\PRECIOS_FRIOSEGURO.md -Pattern '70\.000|45\.000|25\.000'
# NO aparece la marca ajena en ninguna plantilla (regla 1):
Select-String -Path comercial\plantillas_whatsapp.md -Pattern 'FrioSeguro' | Select-String -NotMatch 'QUE_FALTA|repo|item #13|frioseguro/'  # -> solo referencias a docs, ninguna en el copy
# El disclaimer coincide con el contrato (cláusula 2ª = "avisa y registra, no garantiza"):
Select-String -Path comercial\plantillas_whatsapp.md -Pattern 'avisa y (te )?deja el registro|no garantiza'
# El item quedó tachado:
Select-String -Path dominios\comercial.md -Pattern 'Plantillas WhatsApp'   # -> [x] ... plantillas_whatsapp.md
```
**Resultado de esta noche:** archivo nuevo con 16 plantillas + config + objeciones, 100% consistente con
las 4 fuentes (checklist al pie, todo ✔), item #13 tachado. Solo docs — no hay build ni tests que correr.

## Qué quedó SIN verificar / para el día (Matías + @comercial)
1. **El tono es de Matías.** Las plantillas son un **borrador**; la voz del vendedor es personal —
   Matías debe pasarles su tono antes de mandarlas a un cliente real.
2. **Placeholders a completar (día):** `[MARCA]` (falta la decisión de nombre — hueco conocido del
   PORTFOLIO), CBU/alias de cobro, número de contacto. Sin marca, no se manda nada con `[MARCA]` crudo.
3. **El video-demo de §B** hay que grabarlo UNA vez (dashboard propio andando + una alerta llegando) y
   reutilizarlo — no es tarea de un agente.
4. **§H (alerta real) y §K (resumen mensual)** hoy se mandan a mano; se vuelven **automáticas** cuando
   estén en producción el aviso de desconexión y el branch `resumen-mensual` (que sigue pendiente de
   merge, frioseguro #11). No las automaticé de noche: eso es backend + merge humano.
5. **Marcar #13 en `frioseguro/QUE_FALTA.md`:** NO lo toqué para dejar el repo frioseguro prístino (como
   hizo la noche del merge-queue). Cuando Matías/@comercial adopten el archivo, tachar #13 ahí.

## Observaciones para el día (no tareas mías)
- **PLATA por fin recibió trabajo nocturno.** El worker estuvo semanas atrapado en octubre (galgas)
  porque los bloqueantes de FrioSeguro eran físicos/humanos. Este era el único deliverable de la cima de
  la jerarquía que un agente offline podía cerrar entero — y ya estaba listo para cerrarse.
- **El material comercial de FrioSeguro está casi completo:** PITCH, guion_visita, hoja_mostrador (x2),
  PRECIOS, CONTRATO_BORRADOR y ahora las plantillas WhatsApp. Lo que falta para vender ya NO es material:
  es **acción humana** (marca, primera visita, piloto instalado) — exactamente lo que PLATA.md pide.
- El cuello de merge sigue: 32 branches (ver `COLA_MERGE_STATUS_2026-07-27.md`, regenerable con
  `python tools\merge_queue_status.py`). Este entregable NO suma a esa cola (es cuartel, va a main).

## Reglas respetadas
Solo software (docs) + análisis + lectura. **Nada mergeado, borrado, movido ni deployado**; no toqué
ninguno de los 4 repos de proyecto (frioseguro quedó **prístino**, ni un commit); sin `rm -rf`,
`reset --hard` ni `push --force`; sin migraciones; sin mDNS; `data/field_captures` intacto; sin tocar
firmware/backend; sin decisiones de plata (reflejo el precio ya decidido, no lo cambio); sin
compilaciones ni descargas → cero riesgo de timeout.

## Entregable (dónde)
En **MATI-HQ, rama `main`** (es cuartel — mismo criterio que TODO el material comercial hermano
—PITCH/guion/hoja_mostrador/PRECIOS/CONTRATO viven acá, ninguno en el repo frioseguro— y que el tool de
cola de merge del 07-27-b):
- `comercial/plantillas_whatsapp.md` — las 16 plantillas + config + objeciones (nuevo).
- `dominios/comercial.md` — item #13 tachado + entrada de bitácora.

## Branch
Ninguno — entregable de cuartel en **MATI-HQ main**. Los 4 repos de proyecto quedaron intactos.

## Notas para @verificador
- **DoD** = *"existe un archivo de plantillas de WhatsApp Business que cubre el funnel completo del
  servicio de monitoreo de frío, con precios/disclaimer/reglas 100% consistentes con
  PITCH/PRECIOS/guion/CONTRATO, sin usar la marca ajena 'FrioSeguro' en ninguna plantilla, y el item #13
  queda tachado en la bitácora de @comercial"*.
- Ataques sugeridos: (a) contar `### [A-P] ` → 16 plantillas; (b) los 3 precios contra
  `PRECIOS_FRIOSEGURO.md` → idénticos; (c) grep `FrioSeguro` en el copy de las plantillas → 0 (solo en
  referencias a docs/repo); (d) el texto del disclaimer contra `CONTRATO_BORRADOR.md` cláusula 2ª →
  fiel ("avisa y registra, no garantiza la mercadería"); (e) confirmar que NO se prometen features
  inexistentes como base (sirena/informe firmado están como upsell "a consultar", regla 2); (f)
  `git status` de los 4 repos → sin cambios.
</content>
