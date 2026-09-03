# -*- coding: utf-8 -*-
"""Render + verificacion de las DOS propuestas Panamerican / Cerro Moro.
   Enfoque copiado de frioseguro/comercial/venado-tuerto/herramientas/render_folleto.py:
   1) inlina el logo de marca si todavia esta el marcador
   2) PDF A4 con Chromium (Playwright)   3) capturas 1440 y 390 px
   4) render de CADA pagina del PDF a PNG   5) medicion REAL con PyMuPDF.
   LECCION HEREDADA: se mide el ENTREGABLE (el PDF), no el HTML.
   Uso: python render_propuestas.py
"""
import os, io, sys
from playwright.sync_api import sync_playwright
import fitz

AQUI = os.path.dirname(os.path.abspath(__file__))
CAP  = os.path.join(AQUI, "capturas")
LOGO = r"C:\Proyectos\frioseguro\marca\logo_horizontal.svg"
os.makedirs(CAP, exist_ok=True)
MM = 72.0 / 25.4

DOCS = [
    ("PROPUESTA_PANAMERICAN",        "cli"),   # el que se manda
    ("PROPUESTA_PANAMERICAN_INTERNO", "int"),  # el de Matias
]
# palabras que NUNCA pueden aparecer en el PDF que se manda
PROHIBIDAS_CLIENTE = [
    # costos, margen y horas hacia adentro: si alguna de estas aparece en el PDF
    # que se manda, el documento NO sale. (El chequeo corre en cada render.)
    "38.000", "167.000", "133.000", "4.560.000", "3.040.000", "1.520.000", "1.000.000",
    "margen", "Margen", "costo directo", "Costo directo", "26 horas", "160 h", "80 h",
    "subcotiz", "Supabase", "Venado", "PLATA", "Dreyfus", "comisi", "Monotributo",
    "monotributista", "IVA", "INPI", "firmware_modular", "entrega_scz", "testo",
    "MercadoLibre", "IoTMonitoreo", "llave maestra", "bucket", "LISTA_MATERIALES",
    "INTERNO", "Interno", "Objeci", "Validez", "validez", "auditoría de agosto",
]


def inlinar_logo():
    svg = io.open(LOGO, encoding="utf-8").read()
    svg = svg.replace('width="485.5" height="112"', 'width="485.5" height="112" class="logo-svg"')
    for nombre, _ in DOCS:
        p = os.path.join(AQUI, nombre + ".html")
        s = io.open(p, encoding="utf-8").read()
        if "<!--LOGO_HORIZONTAL-->" in s:
            s = s.replace("<!--LOGO_HORIZONTAL-->", svg)
            io.open(p, "w", encoding="utf-8").write(s)
            print("logo inlinado en", nombre)


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
        if "Termovig" not in t: print("     !! falta el pie de marca"); ok = False
        if tag == "int" and "NO ENVIAR" not in t.upper(): print("     !! falta la marca de INTERNO"); ok = False
        pg.get_pixmap(dpi=110).save(os.path.join(CAP, tag + "_p%d.png" % i))
    texto = "\n".join(pg.get_text() for pg in d)
    if tag == "cli":
        print("  --- control de fuga de datos internos ---")
        fugas = [w for w in PROHIBIDAS_CLIENTE if w in texto]
        print("  ", "SIN FUGAS" if not fugas else "!! FUGA: %s" % fugas)
        if fugas: ok = False
    print("  MEDICION:", "OK" if ok else "HAY DEFECTOS")
    # bloques que no se pueden partir entre paginas
    claves = {"cli": ["Si igual hay que tirar", "3 a\u00f1os y medio", "Aceptaci\u00f3n final",
                      "Sexto reefer", "cinco revisores"],
              "int": ["Objeci\u00f3n 5", "Costo directo", "Pendientes", "una falsa alarma por d\u00eda"]}
    for k in claves[tag]:
        pgs = [i for i, pg in enumerate(d, 1) if k in pg.get_text()]
        print("   %-28s -> paginas %s" % (k, pgs))
    d.close()
    return ok


if __name__ == "__main__":
    inlinar_logo()
    for nombre, tag in DOCS:
        print("\n=== %s ===" % nombre)
        pdf = render(nombre, tag)
        medir(pdf, nombre, tag)
