# Dominio: COMERCIAL (agente @comercial)

Pipeline + bitácora. El agente lo lee al arrancar y lo actualiza al cerrar. Doctrina completa: `PLATA.md`.

## Pipeline de leads (tabla viva)
| Lead | Rubro | Zona | Dolor | Estado | Próximo paso (fecha) |
|---|---|---|---|---|---|
| (vacío — se llena en semana 2-4 según PLAN_MES) | | | | | |

Estados: identificado → contactado → demo hecha → piloto → ABONO → (churn)

## Metas (v3, alineadas con PLAN_MES y PLATA)
- 1 piloto comercial instalado en julio · 1 abono COBRADO antes del 18-ago · 3 en pipeline al 18-ago · 3-5 activos antes de octubre
- Slots de venta: mediodía 12:15-12:55 (lun/mié fijo) + viernes a la mañana + sábado tarde
- Legal (semana 2): monotributo + contrato con límite de responsabilidad + link de cobro probado
- 1 acción comercial de Modulia por semana (vigilancia, ejecuta el equipo del ERP)

## Material producido
- [ ] Precio definido (Matías, con 2-3 escenarios del agente) — vie 10-jul
- [ ] Pitch 5 renglones por segmento — vie 10-jul
- [ ] Hoja de mostrador (1 página)
- [ ] Contrato simple con límite de responsabilidad (validar con contador)
- [x] Plantillas WhatsApp Business → `comercial/plantillas_whatsapp.md` (2026-07-28)

## Bitácora
- 2026-07-07 — Agente creado por Claude Fable. Primer hito: piloto casero (heladera de Matías) jue 9-jul; precio+pitch vie 10-jul; primera visita a comercio sáb 11 o lun 13-jul.
- 2026-07-28 (nocturno-local) — Escritas las **plantillas de WhatsApp Business** (`comercial/plantillas_whatsapp.md`): configuración de la cuenta (perfil, bienvenida/ausencia, respuestas rápidas, etiquetas = pipeline) + 12 plantillas del funnel (§A–§L: primer contacto → demo → follow-ups → cierre → onboarding → alerta real → conversión de piloto → cobro → retención → reactivación) + objeciones versión chat (§M) + upsell/cross-sell/referido (§N/§O/§P) — 16 secciones §A–§P. Todo anclado y verificado contra PITCH/PRECIOS/guion_visita/CONTRATO (mismos precios, mismo disclaimer, sin nombrar "FrioSeguro"). Cierra el item #13 de `frioseguro/QUE_FALTA.md`. Falta (Matías): [MARCA], CBU/alias, número, tono, y grabar el video-demo de §B.

---

## Línea 2 — Marketing técnico para representantes industriales (replicar EMSICA)

**Qué es:** el servicio que Matías ya le vendió a EMSICA S.R.L. (Bahía Blanca, instrumentación
desde 1981). Campaña por producto en 5 pasos: análisis de la doc del fabricante → relevamiento
de plantas y responsable → folleto A4 + hoja de datos → envío con seguimiento a 7 días →
publicación del producto en la web del cliente. **$150.000/campaña · $600.000/mes de abono
(4 campañas) · $250.000 rediseño de sitio, aparte.** Diferencial: Matías entiende los productos
(lee una hoja de datos y escribe la pieza comercial); una agencia genérica no puede.

**Métrica:** abonos mensuales activos. Una campaña suelta es prueba, no negocio.

### Base de prospectos — `C:\Proyectos\marketing-tecnico\`
- `prospectos.csv` (fuente de verdad, 15 columnas) · `prospectos.md` (legible, generado)
- `pitch.md` (aperturas WhatsApp/mail/teléfono + objeciones) · `README.md` (cómo seguir)
- `_audit/audit.py` — auditor de sitios: fuerza HTTPS, robots.txt, sitemap.xml, versión de PHP,
  titles repetidos, fichas indexables, redes. Es lo que da el gancho de apertura.

**60 empresas, todas con el sitio auditado desde afuera.** Score 5: 5 · 4: 15 · 3: 21 · 2: 18 · 1: 1.
Zonas: Bahía Blanca 12, Buenos Aires 32, Rosario 6, Mendoza 4, Neuquén 3, Córdoba 1, Litoral/NOA 1.
Regla cumplida: ningún mail ni teléfono inventado — todo sale de la web de la empresa; lo que no
está figura como `a relevar` (20 sin teléfono, 24 sin mail).

### Pipeline — los 5 de score 5 (semana del 24-ago-2026)
| Lead | Rubro | Zona | Gancho (hallazgo verificado) | Estado | Próximo paso (fecha) |
|---|---|---|---|---|---|
| ASI Electric | Integrador oficial Schneider | Buenos Aires | **PHP/5.6.40** (sin soporte desde ene-2019) + sitemap 404 + sitio de 2 páginas | identificado | Llamar (011) 4738-5747 — sem. 24-ago |
| CV Control S.A. | Instrumentación (Yokogawa + 13 marcas) | CABA **con sucursal en Bahía Blanca** | **PHP/7.4.33 — la misma versión que Emsica** + no fuerza HTTPS + 14 marcas sin ficha indexable | identificado | Mail a ventas@cvcontrol.com.ar — sem. 24-ago |
| Cientist S.A. | Instrumental de laboratorio | CABA | **Las 7 páginas con el mismo `<title>`** + robots 404 + sitemap 404 + sin HTTPS forzado = clon exacto de Emsica | identificado | Mail a cientist@cientist.com — sem. 24-ago |
| IRB S.A. | Bombas, válvulas, torque, soldadura (Lincoln Electric, HYTORC, Maus Italia) | **Bahía Blanca** | robots 404 + sitemap 404 + no fuerza HTTPS + HTML estático sin fichas | identificado | Llamar 0291 412-6060 — sem. 24-ago |
| NI Servicios Industriales | Instrumentación y calibración (MSA, Mettler-Toledo, SMC) | **Bahía Blanca** | robots 404 + sitemap 404 + **sin viewport (no anda en celular)** | identificado | Mail a jorgemancini@niservicios.com.ar — sem. 24-ago |

Cola inmediata (score 4, sem. 24-ago a 14-sep): LTM Suministros (BB, distribuidor oficial 3M,
sitio vacío) · Sincro Sur (BB, representa **Delga antiexplosivas** — el pitch del Smart-Ex se
transfiere entero) · SILA SRL (Rosario, **23 marcas representadas**) · SIPEL (Rosario, 7 títulos
iguales; además Emsica los representa → apertura tibia) · Fulcrum (Rosario, Mettler Toledo) ·
Famiq (Neuquén, el home se titula literalmente "Index | Famiq") · Distribuidora Müller (PHP 5.6) ·
Control-Tec (distribuidor Siemens **sin HTTPS**) · Valbol · VAL-AR · Soluciones FMK · BioDiagnóstico ·
Freshen · Hardval · ASI Suministros.

**Bloqueantes antes del primer envío:** (1) pedirle permiso a Jorge Piñeiro para usar los PDF del
Smart-Ex 03 como muestra; (2) línea de baja en el mail (Ley 25.326). `fluke.com.ar` queda **en
pausa**: Emsica también representa Fluke, consultar con Jorge antes.

### Bitácora (línea 2)
- 2026-08-27 — @comercial. **EMSICA pasó de prospecto a CLIENTE activo**: encargó su primera
  campaña de mail (producto SEALWELD — grasas/sellantes/inyectores para válvulas de oil & gas).
  Entregado en `C:\Proyectos\emsica-comercial\entregables\campania_sealweld\`:
  (1) `investigacion_sealweld.md` — 5 productos estrella + el procedimiento de 3 pasos
  (Cleaner→911→#5050) como eje del copy; (2) `mail_sealweld_copy.md` — mail 1 completo por
  bloques (3 asuntos, preheader, 3 bloques de producto, CTA info@emsica.com.ar, baja Ley 25.326)
  listo para que @diseno lo maquete en HTML/Outlook; (3) `segmentos_sealweld.csv` — **341
  contactos** de los 596 de la base real (dedup por mail; P1=197 técnicos de empresas target,
  P2=54 mantenimiento de industrial pesada, P3=90 compras) + `segmentos_notas.md` con huecos
  (YPF 1 técnico, TGN cero, VM cero, minería casi vacía); (4) `prospectos_nuevos.md` — 15
  empresas fuera de la base (TGN, Oldelval, CGC, Vista, Tecpetrol, Pan American Silver con
  puerta tibia vía Matías, etc.), sin mails/teléfonos inventados. **Próximo paso (fechado):
  sem. 31-ago — Jorge valida segmento y ola 1 (P1 sin TGS, ~135 mails); TGS se avisa al
  vendedor de cuenta antes de tocarla. Antes del envío: verificar SPF/DKIM del dominio.**

- 2026-08-21 — @comercial. Base creada y entregada en `C:\Proyectos\marketing-tecnico\`:
  60 empresas argentinas del perfil "representante/distribuidor con catálogo de marcas",
  **cada una con el sitio auditado desde afuera** (script propio `_audit/audit.py`, evidencia
  cruda en `_audit/wave*.jsonl`; `wave0_referencia.jsonl` guarda la auditoría de emsica.com.ar
  como patrón). Hallazgos más fuertes encontrados: 2 sitios en PHP 5.6 (sin soporte desde 2019),
  1 distribuidor Siemens sin HTTPS, 1 sitio caído mostrando la pantalla del hosting, 1 home sin
  `<title>`, y 4 sitios con todos los títulos repetidos igual que Emsica. Entregado también
  `pitch.md` con las 4 objeciones pedidas resueltas ("ya tenemos marketing", "no vendemos por
  internet", "es caro", "lo hace mi sobrino") y la regla de no bajar precio (se ofrece menos
  alcance, nunca el mismo alcance más barato). Nadie contactado todavía: los 60 están en
  `identificado` con próximo paso fechado. **Próxima acción de plata: los 5 de score 5 en la
  semana del 24-ago — 3 de ellos son visita presencial en Bahía Blanca.**
