---
name: kiosco-ofiuco-paco
description: "Todo el Kiosco Ofiuco (cliente Paco) — dónde está el código, la Supabase, el deploy, por qué se pausaba y la deuda de seguridad"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c2ffe10-96cb-49dc-a097-78e5ec79d3b8
  modified: 2026-08-20T11:58:52.341Z
---

Sistema de punto de venta y control de stock para el kiosco de **Paco**, cliente de Matías. Puesto en producción el **2026-08-19**.

## Dónde está cada cosa

- **En vivo:** https://kiosco-ofiuco.vercel.app (equipo Vercel `gimap-s-projects`, proyecto `prj_soDDSjaO8HGvadhUAOyg2h77hjdE`)
- **Código de trabajo:** `C:\Proyectos\kiosco-ofiuco\`
- **Original intacto como referencia:** `C:\Proyectos\kiosco-ofiuco-original\kioscofiuco-main\`
- **Descartable:** `C:\Proyectos\kiosco-ofiuco-mio-descartado\` (lo que escribí de cero antes de que apareciera el código real)
- **Supabase:** `https://egdlgprnanrlvmjfshrv.supabase.co` — clave publicable `sb_publishable_AHhcfa0K-QW2YnF4duy8Mg_zs07XJmb` (es pública por diseño, va en el bundle)
- **Backup de la base:** `MATI-HQ\backups\ofiuco_db_cluster_2026-08-11.backup.gz` y `Documents\KIOSCO OFIUCO PACO\backup_supabase\RESTAURAR_kiosco.sql`

**Trampa para recuperar el código:** el zip de la rama **`master`** de GitHub trae SOLO el README; el código está en la rama **`main`** (`kioscofiuco-main.zip`). Se perdió tiempo creyendo que el repo estaba vacío.

## Qué es

React 19 + TypeScript + Vite 7 + Tailwind 4 + Zustand + Recharts + react-router. **PWA instalable** y con **modo offline real** (Dexie sobre IndexedDB + `syncStore`), que importa porque un kiosco se queda sin internet. Ocho páginas: Sales, Products, Stock, Stats, Settings, Login, Users y CashClosing. Lector de código de barras USB **global** (`useBarcodeScanner`), funciona desde cualquier pantalla.

Datos: 971 productos, 1060 lotes, 8 categorías, 12 ventas. `products.barcode` está poblado (939 códigos distintos, EAN de 13).

## Por qué se le pausaba la Supabase (la pregunta recurrente de Matías)

**El sistema original era 100% LOCAL con SQLite** (Node+Express con `sql.js`, base en `server/kiosco.db`, sin internet). Así que aunque Paco usara el kiosco todos los días, **nadie tocaba Supabase** y el plan free la pausaba a los 7 días. Ver [[supabase-cuentas-proyectos]] para el mecanismo y la solución del guardián.

## DEUDA DE SEGURIDAD — mirar antes de tocar nada

**La app no usa Supabase Auth.** `src/store/authStore.ts` compara contra usuario `OFIUCO` y contraseña `FrancoFranco96` **escritas dentro del JavaScript**, así que viajan en el bundle público: cualquiera que abra la URL las ve. (`src/lib/api/auth.ts` ya tiene todo Supabase Auth escrito, pero nadie lo llama — pasarlo a eso es el arreglo.)

Como paliativo se aplicó RLS con políticas de SELECT/INSERT/UPDATE para `anon` y **ninguna de DELETE**: borrar quedó bloqueado (probado — intentar borrar el catálogo entero afecta 0 filas). **Riesgo que sigue vivo:** con la URL se pueden modificar precios o cargar ventas falsas.

Nota: si `FrancoFranco96` es una contraseña que Matías o Paco reusan en otro lado, hay que cambiarla en todos lados, no solo acá.

## Datos sucios conocidos (no son bugs del código)

8 productos con `stock ≠ suma(lotes)`, 26 productos sin ningún lote, 14 lotes con año imposible (`0026-02-26`, `22027-01-12`), y **43 productos comparten 20 códigos de barras** por altas duplicadas (ej. "coca vidrio 1.25 litros" y "coca cola vidrio x1,25").

Por eso el trigger `trigger_update_product_stock` de `product_batches.sql` está **deliberadamente NO aplicado**: pisa `products.stock` con la suma de lotes y a esos 34 productos les borraría el stock real. Antes hay que conciliar.

## Pendiente

- Pasar el login a Supabase Auth (lo más urgente).
- Stubs vacíos que no guardan nada: `usersApi`, `cashApi.close/getHistory`, `configApi` → la página Usuarios no persiste y el Cierre de Caja no deja historial.
- La pantalla de venta abre con dos banners gigantes de lotes vencidos que en el celular empujan el carrito abajo del pliegue.
- En PORTFOLIO quedó anotado: pasarle a Paco cómo reactivar él mismo la Supabase.

**Duda abierta:** "Paco" es apodo de Francisco, y la contraseña de la app dice "Franco". Matías preguntó una vez por "lo de Franco" como si fuera algo aparte y no hay registro de nadie con ese nombre. Puede ser la misma persona; conviene preguntarle antes de asumirlo.
