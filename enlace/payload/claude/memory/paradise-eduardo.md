---
name: paradise-eduardo
description: "Tienda PARADISE (cliente Eduardo, Macachín LP) — dónde está todo, la Supabase temporal compartida y qué falta del cliente"
metadata: 
  node_type: memory
  type: project
  originSessionId: 764f7a18-232d-4997-81a0-d0f37e5422ee
  modified: 2026-09-01T23:51:30.992Z
---

Tienda online + POS + panel admin para **Paradise** (Eduardo "EEW", cosmética, España 662, Macachín, La Pampa). Construido completo y puesto en producción el 2026-08-27.

**ESTADO COMERCIAL (2026-08-29): SEÑA DEL 50% YA RECIBIDA ($200.000, alias `malegron`).**
Precio bajó de $480.000 a **$400.000** al confirmar que Mercado Pago queda fuera
(era ~15-20% del desarrollo). Abono $55.000/mes sigue igual. Detalle completo y
próximos pasos técnicos en `C:\Proyectos\tienda-cosmetica\ESTADO_SESION.md`
(léer ESE archivo primero al retomar el proyecto — tiene los 3 compromisos de
portabilidad que le hice a Eduardo por escrito y TODAVÍA no cumplí: repo a
GitHub con acceso para él, admin compartido en la Supabase nueva al migrar, y
dominio a su nombre. Eduardo preguntó explícito por vendor lock-in — no bajar
la guardia con esto).

- **Código:** `C:\Proyectos\tienda-cosmetica` (git local, sin remote). README con runbook completo.
- **En vivo:** https://tienda-cosmetica-vert.vercel.app (`/local` POS, `/admin` panel; Vercel `gimap-s-projects/tienda-cosmetica`).
- **Base:** schema `paradise` DENTRO del proyecto Supabase del kiosco (`egdlgprnanrlvmjfshrv`) — **TEMPORAL** por el límite de 2 proyectos free (ver [[supabase-cuentas-proyectos]]). El esquema entero está en `supabase/schema.sql`; la migración a un proyecto Pro propio (USD 25/mes real, verificado 2026-08-28 — OJO, se dijo mal "USD 10" en la sesión del rediseño; el Pro trae 100 GB de storage, muy por encima de los ~45 MB que pesan las 300 fotos, así que storage NUNCA fue el motivo: es proyecto propio + backups diarios. El free tier de 1 GB ya alcanza para las fotos) sale del abono y se dispara cuando entre la seña. El README de `tienda-cosmetica` ya quedó corregido. Efecto colateral bueno: el tráfico de Paradise mantiene viva la base del kiosco.
- **Login del negocio** (POS y admin, Supabase Auth): `paradisee.lp@gmail.com`, contraseña en `CREDENCIALES.local.txt` (gitignoreado).
- **Doble precio en todo**: `precio_efectivo` (efectivo/transferencia) y `precio_lista` (tarjeta). Pedidos por RPC `crear_pedido` (security definer, valida+descuenta stock); ventas del POS por `vender_local`. Realtime mueve el stock de la web en vivo.
- **Mails** de confirmación: `api/nuevo-pedido.js` por SMTP de Gmail (mismo esquema que anduvo en el ERP con contraseña de aplicación) — **bloqueado hasta que Eduardo genere la app password** y se cargue `GMAIL_USER`/`GMAIL_PASS` en Vercel. Los pedidos entran igual sin eso.
- **Paleta oficial** (brandboard abekydesign): crema #F2EEE7, dorado claro #EBCB7C, dorado #BA8D41, marrón #6D3D18; tipografía Cinzel Decorative (Google Fonts). Logos extraídos de los PDF a `public/logo-p.png` y `public/logo-paradise.png`.
- **Faltan del cliente:** seña, alias de transferencia real (hoy placeholder `PARADISE.MP` en `src/datos.js`), app password de Gmail, lista de ~300 productos+fotos (importador listo: `scripts/importar_productos.mjs` + `plantilla_productos.csv`; comprime fotos a WebP), fotos del local para el banner. Los 16 productos actuales son seed de demo con fotos Unsplash.
