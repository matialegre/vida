---
name: emsica-cliente
description: "EMSICA S.R.L. es cliente activo (2026-08-27) — sitio, campañas mail, dónde vive cada cosa y qué falta pedirles"
metadata: 
  node_type: memory
  type: project
  originSessionId: bed65084-edc1-46b4-aaef-37bb7f45ff15
  modified: 2026-08-28T01:58:23.578Z
---

EMSICA S.R.L. (instrumentación industrial, Bahía Blanca, desde 1981, emsica.com.ar) pasó de prospecto a **cliente activo el 2026-08-27**. Contactos: Jorge Piñeiro (jorge.pineiro@emsica.com.ar) y Joaquín Villalba (taller@emsica.com.ar).

**Dónde vive todo:**
- Sitio nuevo: `C:\Proyectos\emsica-web` (Next.js 16, demo en emsica-sitio.vercel.app, 27 páginas de marca con SEO local). Sitio viejo: GoDaddy compartido administrado por **Control Bay LLC**; FTP y repo GitHub privado EMSICA/web-emsica en `C:\Proyectos\emsica-comercial\CREDENCIALES.md` (fuera de git).
- Comercial: `C:\Proyectos\emsica-comercial` (repo git local). Base de contactos del cliente exportada del Access: `fuente\accdb_2025\` (596 contactos/106 empresas; el .accdb NO se commitea). OJO: mails de la base pueden traer punto final — normalizar antes de cruzar.
- Campaña 1 = **Sealweld** (grasas/selladores de válvulas; sin distribuidor listado en Sudamérica). Segmento 341 contactos, plantilla Outlook-safe + generador autocontenido en `entregables\`.

**Mail del dominio:** vive en **Microsoft 365** (no en el hosting). Hay una cuenta **Brevo a medio verificar** en el DNS (falta DKIM) y el **DKIM de M365 tampoco está activo** → riesgo spam. Camino elegido: completar Brevo + Graph API para leer la casilla.

**Falta pedirles:** dueño de la cuenta Brevo, acceso DNS (Control Bay/GoDaddy), admin M365, acceso al repo GitHub, lista contractual de marcas "representante oficial" (el brief decía "Kane May" pero la marca real es Kistler-Morse), OK logo Sealweld, teléfono/dirección para firma de mails, autorización escrita para leer la casilla.

Antecedente: propuesta y honorarios en `MATI-HQ\comercial\EMSICA_plan_y_honorarios.html` ($150k/campaña, $600k/mes abono, $250k rediseño web). Relacionado: [[biblioteca-codigo-reusable]].
