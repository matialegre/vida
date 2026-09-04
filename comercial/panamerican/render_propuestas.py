# -*- coding: utf-8 -*-
"""Render + verificacion de los TRES PDF de reefers Cerro Moro (v4, 3-sep-2026).

   Salidas:
     PRESUPUESTO_1_UNO_POR_REEFER.pdf         cliente, 2 paginas (6 equipos)
     PRESUPUESTO_2_UNO_CADA_DOS.pdf           cliente, 2 paginas (3 equipos)
     PROPUESTA_REEFERS_CERRO_MORO_INTERNO.pdf interno, marca de agua en todas

   Enfoque copiado de frioseguro/comercial/venado-tuerto/herramientas/render_folleto.py:
   1) arma los dos del cliente desde UNA plantilla (armar_presupuestos.py) para que sean gemelos
   2) inlina logo y escudo   3) numera las paginas   4) PDF A4 con Chromium (Playwright)
   5) capturas 1440 y 390 px   6) render de CADA pagina del PDF a PNG
   7) medicion REAL con PyMuPDF   8) guarda de fugas sobre LOS DOS PDF del cliente.
   LECCION HEREDADA: se mide el ENTREGABLE (el PDF), no el HTML.
   Uso: python render_propuestas.py
"""
import os, io, re
from playwright.sync_api import sync_playwright
import fitz
import armar_presupuestos as ARM

AQUI = os.path.dirname(os.path.abspath(__file__))
CAP  = os.path.join(AQUI, "capturas")
LOGO = ARM.LOGO
os.makedirs(CAP, exist_ok=True)
MM = 72.0 / 25.4

DOCS = [
    ("PRESUPUESTO_1_UNO_POR_REEFER",         "cli1", 2),
    ("PRESUPUESTO_2_UNO_CADA_DOS",           "cli2", 2),
    ("PROPUESTA_REEFERS_CERRO_MORO_INTERNO",  "int", None),
]

# Cadenas que NUNCA pueden aparecer en un PDF del cliente. Si alguna aparece, el documento NO sale.
# Nota v4: se sacaron de la lista "auditor" (el cliente SI habla de su auditor y de auditoria: es
# argumento de venta legitimo) y "USD 110" (es el precio del ajuste del P2, que va a la vista por
# pedido expreso). En su lugar entran las cadenas internas concretas de la v4.
PROHIBIDAS_CLIENTE = [
    # el comprador no tiene nombre: ni destinatario ni la minera
    "Panamerican", "PAAS", "Pan American", "Para:", "Destinatario",
    # costos, margen y horas hacia adentro
    "38.000", "167.000", "169.000", "133.000", "margen", "Margen", "costo directo", "Costo directo",
    "26 horas", "160 h", "80 h", "60 h", "USD 25/h", "USD 90", "USD 162", "USD 333", "USD 167",
    "USD 46", "USD 48", "USD 231", "USD 141", "USD 1.000", "USD 2.460", "USD 1.230", "USD 118",
    "2.950", "Desarrollo", "desarrollo", "subcotiz", "Supabase", "Venado", "PLATA", "Dreyfus",
    "comisi", "Monotributo", "monotributo", "RI,", "INPI", "firmware_modular", "entrega_scz",
    "testo", "MercadoLibre", "ML AR", "llave maestra", "bucket", "LISTA_MATERIALES", "BOM",
    "INTERNO", "Interno", "Objeci", "Validez", "validez", "AUDITORIA", "referidor", "Referidor",
    "piso 390", "377", "8,7 %", "financiamos", "Riesgo nuestro", "pull-up", "2k2",
    "1-Wire", "AN148", "@comercial", "@muestreador", "@diseno", "@hardware", "@firmware",
    "SONDAS_MAX", "DS18B20", "ESP32", "GPIO", "firmware_revival", "sondas.h", "config.h",
    "comandos_nube", "NVS", "ALCANCE", "ESTADO_HONESTO", "novillo", "INMAG", "conflicto de inter",
    "E0", "E1", "E2", "E3", "E4",
]


def inlinar():
    """El logo horizontal y el escudo del pie viven en marcadores; se inyectan aca."""
    svg = io.open(LOGO, encoding="utf-8").read()
    for nombre, _, _ in DOCS:
        p = os.path.join(AQUI, nombre + ".html")
        s = io.open(p, encoding="utf-8").read()
        s2 = s.replace("<!--LOGO_HORIZONTAL-->", svg).replace("<!--ESCUDO-->", ARM.ESCUDO)
        if s2 != s:
            io.open(p, "w", encoding="utf-8").write(s2)
            print("  logo/escudo inlinados en", nombre)


def numerar():
    """Los pies llevan 'N / total' segun la cantidad de <section class="hoja"> del HTML."""
    for nombre, _, _ in DOCS:
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


def medir(pdf, nombre, tag, paginas_esperadas):
    for f in os.listdir(CAP):
        if re.match(re.escape(tag) + r"_p\d+\.png$", f):   # no borrar _pantalla_1440.png
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
        if tx1 > r.width - 9.0 * MM: print("     !! TEXTO invade margen derecho"); ok = False
        if tx0 < 9.0 * MM: print("     !! TEXTO invade margen izquierdo"); ok = False
        if ty0 < 9.0 * MM: print("     !! TEXTO invade margen superior"); ok = False
        if r.height - ty1 < 9.0 * MM: print("     !! TEXTO invade margen inferior"); ok = False
        if x1 > r.width - 9.0 * MM or x0 < 9.0 * MM: print("     !! VECTOR fuera de margen"); ok = False
        t = pg.get_text()
        if "Termovig" not in t: print("     !! falta el pie de marca (hoja desbordada?)"); ok = False
        if tag == "int" and "NO ENVIAR" not in t.upper(): print("     !! falta la marca de INTERNO"); ok = False
        pg.get_pixmap(dpi=110).save(os.path.join(CAP, tag + "_p%d.png" % i))

    texto = "\n".join(pg.get_text() for pg in d)
    if tag.startswith("cli"):
        print("  --- guarda de fugas (%d cadenas prohibidas) ---" % len(PROHIBIDAS_CLIENTE))
        fugas = [w for w in PROHIBIDAS_CLIENTE if w in texto]
        print("  ", "SIN FUGAS" if not fugas else "!! FUGA: %s" % fugas)
        if fugas: ok = False
    if paginas_esperadas and d.page_count != paginas_esperadas:
        print("  !! se esperaban %d paginas" % paginas_esperadas); ok = False
    print("  MEDICION:", "OK" if ok else "HAY DEFECTOS")

    claves = {
        "cli1": ["Presupuesto 1", "Un equipo por reefer", "Sin condiciones", "Total a 12 meses",
                 "4.920", "no lleva", "50 %"],
        "cli2": ["Presupuesto 2", "Un equipo cada dos reefers", "sin letra chica", "USD 110",
                 "Total a 12 meses", "4.770", "canalizaci", "50 %"],
        "int":  ["WhatsApp para Andr", "Qué hacer con cada respuesta", "USD 150",
                 "Guion de 5", "Referidor formal", "790"],
    }
    for k in claves[tag]:
        pgs = [i for i, pg in enumerate(d, 1) if k in pg.get_text()]
        print("   %-34s -> paginas %s" % (k, pgs))
    d.close()
    return ok


def gemelos():
    """Los dos del cliente tienen que tener las MISMAS secciones en el MISMO orden."""
    sec = []
    for nombre, tag, _ in DOCS[:2]:
        t = io.open(os.path.join(AQUI, nombre + ".html"), encoding="utf-8").read()
        sec.append(re.findall(r'<h2><span class="n">(\d\d)</span>([^<]+)</h2>', t))
    print("\n=== gemelos ===")
    print("  P1:", [s[0] + " " + s[1] for s in sec[0]])
    print("  P2:", [s[0] + " " + s[1] for s in sec[1]])
    print("  ", "MISMA ESTRUCTURA" if sec[0] == sec[1] else "!! LAS SECCIONES NO COINCIDEN")
    return sec[0] == sec[1]


if __name__ == "__main__":
    logo = io.open(LOGO, encoding="utf-8").read()
    for d in (ARM.P1, ARM.P2):
        io.open(os.path.join(AQUI, d["archivo"] + ".html"), "w", encoding="utf-8").write(ARM.armar(d, logo))
    print("armados los dos presupuestos del cliente desde la plantilla unica")
    inlinar()
    numerar()
    todo = gemelos()
    for nombre, tag, npag in DOCS:
        print("\n=== %s ===" % nombre)
        pdf = render(nombre, tag)
        todo = medir(pdf, nombre, tag, npag) and todo
    print("\n>>> RESULTADO GLOBAL:", "TODO OK" if todo else "HAY DEFECTOS QUE CORREGIR")
