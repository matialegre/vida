# -*- coding: utf-8 -*-
"""Render + verificacion de las DOS propuestas de reefers Cerro Moro (v2, 3-sep-2026).
   Enfoque copiado de frioseguro/comercial/venado-tuerto/herramientas/render_folleto.py:
   1) inlina el logo de marca si todavia esta el marcador   2) numera las paginas
   3) PDF A4 con Chromium (Playwright)   4) capturas 1440 y 390 px
   5) render de CADA pagina del PDF a PNG   6) medicion REAL con PyMuPDF
   7) guarda de fugas: el PDF del cliente no puede contener nada interno.
   LECCION HEREDADA: se mide el ENTREGABLE (el PDF), no el HTML.
   Uso: python render_propuestas.py
"""
import os, io, re
from playwright.sync_api import sync_playwright
import fitz

AQUI = os.path.dirname(os.path.abspath(__file__))
CAP  = os.path.join(AQUI, "capturas")
LOGO = r"C:\Proyectos\frioseguro\marca\logo_horizontal.svg"
os.makedirs(CAP, exist_ok=True)
MM = 72.0 / 25.4

DOCS = [
    ("PROPUESTA_REEFERS_CERRO_MORO",         "cli"),   # el que se manda (2 paginas)
    ("PROPUESTA_REEFERS_CERRO_MORO_INTERNO", "int"),   # el de Matias
]
# palabras que NUNCA pueden aparecer en el PDF que se manda: si alguna aparece, el documento NO sale.
PROHIBIDAS_CLIENTE = [
    # el comprador no tiene nombre: ni destinatario ni la minera
    "Panamerican", "PAAS", "Pan American", "Para:", "Destinatario",
    # costos, margen y horas hacia adentro
    "38.000", "167.000", "169.000", "133.000", "margen", "Margen", "costo directo", "Costo directo",
    "26 horas", "160 h", "80 h", "60 h", "USD 25/h", "USD 110", "USD 90", "USD 162", "USD 333",
    "2.950", "Desarrollo", "desarrollo", "subcotiz", "Supabase", "Venado", "PLATA", "Dreyfus",
    "comisi", "Monotributo", "monotributo", "IVA", "INPI", "firmware_modular", "entrega_scz",
    "testo", "MercadoLibre", "IoTMonitoreo", "llave maestra", "bucket", "LISTA_MATERIALES",
    "INTERNO", "Interno", "Objeci", "Validez", "validez", "auditor", "Auditor", "referidor",
    "comodato;", "piso 390", "377", "8,7 %", "financiamos", "Riesgo nuestro", "pull-up", "2k2",
    "1-Wire", "AN148", "@comercial", "@muestreador", "@diseno", "E0", "E1", "E2", "E3", "E4",
]


def inlinar_logo():
    svg = io.open(LOGO, encoding="utf-8").read()
    for nombre, _ in DOCS:
        p = os.path.join(AQUI, nombre + ".html")
        s = io.open(p, encoding="utf-8").read()
        if "<!--LOGO_HORIZONTAL-->" in s:
            s = s.replace("<!--LOGO_HORIZONTAL-->", svg)
            io.open(p, "w", encoding="utf-8").write(s)
            print("logo inlinado en", nombre)


def numerar():
    """Los pies llevan 'N / total' segun la cantidad de <section class="hoja"> del HTML."""
    for nombre, _ in DOCS:
        p = os.path.join(AQUI, nombre + ".html")
        s = io.open(p, encoding="utf-8").read()
        n = s.count('<span class="npag">')
        i = [0]
        def rep(m):
            i[0] += 1
            return '<span class="npag">%d / %d</span>' % (i[0], n)
        s2 = re.sub(r'<span class="npag">[^<]*</span>', rep, s)
        if s2 != s:
            io.open(p, "w", encoding="utf-8").write(s2)


def render(nombre, tag):
    html = os.path.join(AQUI, nombre + ".html")
    pdf  = os.path.join(AQUI, nombre + ".pdf")
    url  = "file:///" + html.replace("\\", "/")
    errores = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=2)
        pg.on("console", lambda m: errores.append(m.type + ": " + m.text))
        pg.on("pageerror", lambda e: errores.append("pageerror: " + str(e)))
        pg.goto(url); pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(CAP, tag + "_pantalla_1440.png"), full_page=True)
        pg.pdf(path=pdf, format="A4", print_background=True, prefer_css_page_size=True)
        pg2 = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg2.goto(url); pg2.wait_for_timeout(300)
        pg2.screenshot(path=os.path.join(CAP, tag + "_celular_390.png"), full_page=True)
        ancho = pg2.evaluate("() => [document.documentElement.scrollWidth, window.innerWidth]")
        b.close()
    print("  consola:", errores if errores else "0 mensajes")
    print("  a 390 px: scrollWidth=%s innerWidth=%s -> %s"
          % (ancho[0], ancho[1], "OK" if ancho[0] <= ancho[1] else "DESBORDA"))
    return pdf


def medir(pdf, nombre, tag):
    # capturas viejas de este doc fuera, para que no queden paginas fantasma
    for f in os.listdir(CAP):
        if f.startswith(tag + "_p") and f.endswith(".png"):
            os.remove(os.path.join(CAP, f))
    d = fitz.open(pdf); ok = True
    print("  PDF: %d paginas" % d.page_count)
    for i, pg in enumerate(d, 1):
        r = pg.rect
        x0 = y0 = 1e9; x1 = y1 = -1e9
        for b in pg.get_text("blocks"):
            x0 = min(x0, b[0]); y0 = min(y0, b[1]); x1 = max(x1, b[2]); y1 = max(y1, b[3])
        tx0, ty0, tx1, ty1 = x0, y0, x1, y1
        for dr in pg.get_drawings():
            rr = dr["rect"]
            if rr.is_empty or rr.width > r.width or rr.height > r.height:
                continue
            x0 = min(x0, rr.x0); y0 = min(y0, rr.y0); x1 = max(x1, rr.x1); y1 = max(y1, rr.y1)
        f = lambda v: v / MM
        print("   p%d %.1fx%.1fmm | TEXTO izq %.1f der %.1f (marg %.1f) sup %.1f inf %.1f | TINTA izq %.1f der %.1f sup %.1f inf %.1f"
              % (i, f(r.width), f(r.height), f(tx0), f(tx1), f(r.width - tx1), f(ty0), f(r.height - ty1),
                 f(x0), f(x1), f(y0), f(r.height - y1)))
        if tx1 > r.width - 13.0 * MM: print("     !! TEXTO invade margen derecho"); ok = False
        if tx0 < 13.0 * MM: print("     !! TEXTO invade margen izquierdo"); ok = False
        if ty0 < 14.0 * MM: print("     !! TEXTO invade margen superior"); ok = False
        if r.height - ty1 < 14.0 * MM: print("     !! TEXTO invade margen inferior"); ok = False
        if x1 > r.width - 13.0 * MM or x0 < 13.0 * MM: print("     !! VECTOR fuera de margen"); ok = False
        t = pg.get_text()
        if "Termovig" not in t: print("     !! falta el pie de marca (hoja desbordada?)"); ok = False
        if tag == "int" and "NO ENVIAR" not in t.upper(): print("     !! falta la marca de INTERNO"); ok = False
        pg.get_pixmap(dpi=110).save(os.path.join(CAP, tag + "_p%d.png" % i))
    texto = "\n".join(pg.get_text() for pg in d)
    if tag == "cli":
        print("  --- guarda de fugas (%d cadenas prohibidas) ---" % len(PROHIBIDAS_CLIENTE))
        fugas = [w for w in PROHIBIDAS_CLIENTE if w in texto]
        print("  ", "SIN FUGAS" if not fugas else "!! FUGA: %s" % fugas)
        if fugas: ok = False
        if d.page_count != 2: print("  !! el PDF del cliente tiene que ser de 2 paginas"); ok = False
    print("  MEDICION:", "OK" if ok else "HAY DEFECTOS")
    claves = {"cli": ["Total a 12 meses", "Total a 24 meses", "USD 220 m\u00e1s por par", "Hito"],
              "int": ["Riesgo de C", "Dale Andr", "Guion de 5", "Referidor formal", "M\u00f3dulo doble USD 720"]}
    for k in claves[tag]:
        pgs = [i for i, pg in enumerate(d, 1) if k in pg.get_text()]
        print("   %-28s -> paginas %s" % (k, pgs))
    d.close()
    return ok


if __name__ == "__main__":
    inlinar_logo()
    numerar()
    for nombre, tag in DOCS:
        print("\n=== %s ===" % nombre)
        pdf = render(nombre, tag)
        medir(pdf, nombre, tag)
