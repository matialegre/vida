# @planillas — bitácora

Entregables Excel/PDF que van al cliente. Doctrina: `~/.claude/agents/planillas.md`.
Herramientas: `~/.claude/agents/lib/planillas/` (`xlsxfix.py` para RE-guardar sin
matar los WMF, `verificar.py`, `qa_texto.py`).

---

## 2026-09-04 · EMSICA — las dos planillas de revisión de catálogo, rehechas como ÁRBOL

**Qué pasó.** La v1 era una tabla plana (una fila por línea, columnas
Categoría / Subcategoría / Línea). Correcta pero inútil para lo que el cliente
tiene que hacer: reconocer su propio catálogo y tachar. Matías pidió el espejo
del mega-menú del sitio. Rehechas como árbol con sangría y jerarquía
tipográfica.

- `C:\Proyectos\emsica-comercial\entregables\catalogo_revision\generar_catalogo_xlsx.py`
  — reescrito de `# estilo` para abajo. Sigue leyendo TODO de `emsica-web`
  (`content/lineas.ts`, `categorias.ts`, `marcas.ts`, `enlaces-fabricante.ts`,
  `components/LogoMarca.tsx`). Nada tipeado a mano.
- `EMSICA_catalogo_por_categoria.xlsx` — CATEGORÍA › (bajada) › GRUPO › LÍNEA,
  200 filas. `EMSICA_catalogo_por_marca.xlsx` — MARCA › CATEGORÍA › LÍNEA,
  243 filas. Copias de la v1 en `_previo_tabla_plana\`.
- El orden de marcas es ESPEJO de `emsica-web/lib/orden-marcas.ts` (fluke,
  foxboro, swagelok → resto por cantidad de líneas desc → las 5 sin líneas).
  **Si cambia aquel archivo, hay que cambiar `PRIORIDAD_CLIENTE` /
  `marcas_ordenadas()` acá o la planilla y el sitio dejan de coincidir.**

**Decisiones de formato (van al cliente en la hoja Léame).**
1. **Autofiltro: sacado.** Filtrar un árbol lo destruye (líneas huérfanas sin
   su título, parece que faltan filas).
2. **Orientación en una fila suelta:** última columna «Ubicación (para no
   perderse)» con el camino repetido en cada fila + panel congelado en `C2`
   (encabezado + las dos columnas del árbol) + fila 1 repetida al imprimir.

**Tres bugs de render encontrados y arreglados mirando el PDF** (LibreOffice no
recalcula el alto de fila; lo que sobra se dibuja ENCIMA de la fila de abajo):
- la URL cruda a 12 pt bold desbordaba la banda azul del título → los enlaces
  de las filas de título van en 9 pt (`font_url` por nivel);
- el alto se calculaba con un interlineado único: dos renglones de 12 pt no
  entran en el alto de dos de 10 pt → interlineado por cuerpo de letra;
- el encabezado de 3 renglones se cortaba en 32 pt → 40 pt y textos más cortos.

**Evidencia.** Los 10 totales cuadran (161 líneas, 170 pares, 31 marcas, 6
categorías, 27 grupos, 116 imágenes, 161/175 filas de línea, 31 marcas,
113 con foto) + 7 controles nuevos de estructura del árbol. Zip íntegro, 0
imágenes que preservar (los archivos se generan de cero, por eso openpyxl es
seguro acá). PDF de control en `_preview\`: 10 y 9 páginas, datos en apaisado,
contenido de 36 a 806 pt = usa exactamente el ancho imprimible, ninguna columna
partida (6 CATEGORÍA / 27 GRUPO / 161 LÍNEA aparecen una sola vez).

**Impresión: NO se tocó** (escalas 46 % y 34 %, A4 apaisado, márgenes 0,5"). El
árbol es más angosto que la tabla plana y sigue entrando. Si @impresion quiere
agrandar la letra, hay margen.

**Pendiente / para Matías:** falta el paso de @qa-visual (yo no verifico lo
mío). Sin commitear, por pedido.
