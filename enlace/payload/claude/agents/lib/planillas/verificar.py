# -*- coding: utf-8 -*-
"""QA objetivo: mide en el PDF renderizado si el contenido se corta contra el borde."""
import fitz, sys, os, glob


def bbox_contenido(page, dpi=110):
    """Bounding box del contenido no-blanco, en puntos PDF."""
    pix = page.get_pixmap(dpi=dpi)
    w, h, n = pix.width, pix.height, pix.n
    buf = pix.samples
    minx, maxx, miny, maxy = w, -1, h, -1
    for y in range(h):
        row = y * pix.stride
        for x in range(w):
            p = row + x * n
            if buf[p] < 245 or buf[p + 1] < 245 or buf[p + 2] < 245:
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    if maxx < 0:
        return None
    k = 72.0 / dpi
    return (minx * k, miny * k, maxx * k, maxy * k)


def revisar(pdf, tol=3.0):
    d = fitz.open(pdf)
    print("=" * 74)
    print(os.path.basename(pdf), "-", d.page_count, "paginas")
    problemas = []
    for i in range(d.page_count):
        pg = d[i]
        W, H = pg.rect.width, pg.rect.height
        bb = bbox_contenido(pg)
        if bb is None:
            problemas.append((i + 1, "PAGINA EN BLANCO"))
            print("  p%-3d VACIA" % (i + 1))
            continue
        x0, y0, x1, y1 = bb
        der, izq, arr, aba = W - x1, x0, y0, H - y1
        flags = []
        if der <= tol: flags.append("CORTE DERECHA")
        if izq <= tol: flags.append("CORTE IZQUIERDA")
        if aba <= tol: flags.append("CORTE ABAJO")
        if arr <= tol: flags.append("CORTE ARRIBA")
        if flags:
            problemas.append((i + 1, ", ".join(flags)))
        if i < 3 or flags:
            print("  p%-3d %dx%d | margenes izq=%.0f der=%.0f arr=%.0f aba=%.0f  %s"
                  % (i + 1, W, H, izq, der, arr, aba, " <-- " + ", ".join(flags) if flags else "OK"))
    if problemas:
        print("  >>> %d pagina(s) con problema: %s" % (len(problemas), problemas[:6]))
    else:
        print("  >>> TODAS LAS PAGINAS OK (nada toca el borde)")
    return problemas


if __name__ == '__main__':
    tot = 0
    for p in sorted(glob.glob(os.path.join(sys.argv[1], "*.pdf"))):
        tot += len(revisar(p))
    print("\nTOTAL problemas:", tot)
