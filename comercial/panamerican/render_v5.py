# -*- coding: utf-8 -*-
"""Render + verificacion de los DOS PDF de reefers Cerro Moro (v5.1, 4-sep-2026).

   Salidas:
     PRESUPUESTO_CERRO_MORO.pdf          cliente, 2 paginas (5 equipos, un solo presupuesto)
     PRESUPUESTO_CERRO_MORO_INTERNO.pdf  interno, marca de agua INTERNO - NO ENVIAR en todas

   Cambia respecto de render_propuestas.py (v4): habia dos documentos gemelos de cliente y
   por eso existia gemelos(); ahora es UNO. El interno se arma desde interno_v5.fuente.html
   (fuente con marcadores) para que el HTML entregable sea reproducible y la fuente no se
   consuma al inlinar el logo.

   1) arma el HTML del cliente desde armar_cliente_v5.py   2) arma el interno desde su fuente
   3) inlina logo y escudo   4) numera las paginas   5) PDF A4 con Chromium (Playwright)
   6) capturas 1440 y 390 px   7) render de CADA pagina del PDF a PNG
   8) medicion REAL con PyMuPDF   9) guarda de fugas sobre el PDF del cliente.
   LECCION HEREDADA: se mide el ENTREGABLE (el PDF), no el HTML.
   Uso: python render_v5.py
"""
import os, io, re
from playwright.sync_api import sync_playwright
import fitz
import armar_cliente_v5 as ARM

AQUI = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(AQUI, "capturas")
LOGO = ARM.LOGO
os.makedirs(CAP, exist_ok=True)
MM = 72.0 / 25.4

CLIENTE = "PRESUPUESTO_CERRO_MORO"
INTERNO = "PRESUPUESTO_CERRO_MORO_INTERNO"
FUENTE_INTERNO = "interno_v5.fuente.html"

DOCS = [(CLIENTE, "cli", 2), (INTERNO, "int", None)]

# Cadenas que NUNCA pueden aparecer en el PDF del cliente. Si alguna aparece, el documento NO sale.
# v5: entran las cadenas internas nuevas (la cuenta del cano, el comparativo, los nombres del taller)
# y sale "USD 110" (la clausula del P2 ya no existe).
PROHIBIDAS_CLIENTE = [
    # el comprador no tiene nombre: ni destinatario ni la minera
    "Panamerican", "PAAS", "Pan American", "Para:", "Destinatario",
    # las tres palabras que Matias prohibio en el documento del cliente
    "plaqueta perforada", "protoboard", "armado a mano",
    # costos, margen y horas hacia adentro
    "margen", "Margen", "costo directo", "Costo directo", "USD 25/h", "USD 90", "USD 46", "USD 148",
    "USD 1.000", "28,5", "plataforma", "Plataforma", "reposición amortizada",
    "38.000", "167.000", "169.000", "133.000", "2.950", "4.892", "4.642", "5.222", "4.517",
    "Desarrollo", "desarrollo", "subcotiz", "Supabase", "Venado", "PLATA", "Dreyfus",
    "comisi", "Monotributo", "monotributo", "INPI", "firmware_modular", "entrega_scz",
    "testo", "MercadoLibre", "ML AR", "llave maestra", "bucket", "LISTA_MATERIALES", "BOM",
    "INTERNO", "Interno", "Objeci", "Validez", "validez", "AUDITORIA", "referidor", "Referidor",
    "financiamos", "Riesgo nuestro", "pull-up", "2k2", "1-Wire", "AN148",
    "@comercial", "@muestreador", "@diseno", "@hardware", "@firmware",
    "SONDAS_MAX", "DS18B20", "ESP32", "GPIO", "firmware_revival", "sondas.h", "config.h",
    "comandos_nube", "NVS", "ALCANCE", "ESTADO_HONESTO", "novillo", "INMAG", "conflicto de inter",
    # la cuenta del cano y el escenario descartado son internos: al cliente va la conclusion, no la cuenta
    "Daisa", "AAIERIC", "electricista", "jornada", "grampa", "Grampa", "cupla", "omega",
    "Gonza", "Sergio", "anticipo del 50", "semana 0",
    "E0", "E1", "E2", "E3", "E4",
]

CLAVES = {
    "cli": ["Un equipo por reefer", "Condiciones de instalación: ninguna",
            "El sexto reefer", "se prueba individualmente", "sigue midiendo y reportando",
            "a las 2 semanas de iniciado", "a las 15 semanas", "Se acepta con",
            "4.540", "500", "520", "50 %", "Total a 12 meses", "10.540", "15.340"],
    "int": ["WhatsApp para Andr", "LA CUENTA DEL CA", "439.700", "286",
            "Los 13 pendientes", "Lo que quedó abierto", "semana 0", "500/mes", "9.940",
            "352", "4.540", "520"],
}


def armar_htmls():
    logo = io.open(LOGO, encoding="utf-8").read()
    io.open(os.path.join(AQUI, CLIENTE + ".html"), "w", encoding="utf-8").write(ARM.armar(ARM.D, logo))
    fuente = io.open(os.path.join(AQUI, FUENTE_INTERNO), encoding="utf-8").read()
    io.open(os.path.join(AQUI, INTERNO + ".html"), "w", encoding="utf-8").write(fuente)
    print("armados: %s.html (generador) y %s.html (desde %s)" % (CLIENTE, INTERNO, FUENTE_INTERNO))


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
    pdf = os.path.join(AQUI, nombre + ".pdf")
    url = "file:///" + html.replace("\\", "/")
    errores = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=2)
        pg.on("console", lambda m: errores.append(m.type + ": " + m.text))
        pg.on("pageerror", lambda e: errores.append("pageerror: " + str(e)))
        pg.goto(url)
        pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(CAP, tag + "_pantalla_1440.png"), full_page=True)
        pg.pdf(path=pdf, format="A4", print_background=True, prefer_css_page_size=True)
        pg2 = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
        pg2.goto(url)
        pg2.wait_for_timeout(300)
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
    d = fitz.open(pdf)
    ok = True
    print("  PDF: %d paginas" % d.page_count)
    for i, pg in enumerate(d, 1):
        r = pg.rect
        x0 = y0 = 1e9
        x1 = y1 = -1e9
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
    if tag == "cli":
        print("  --- guarda de fugas (%d cadenas prohibidas) ---" % len(PROHIBIDAS_CLIENTE))
        fugas = [w for w in PROHIBIDAS_CLIENTE if w in texto]
        print("  ", "SIN FUGAS" if not fugas else "!! FUGA: %s" % fugas)
        if fugas: ok = False
        for mala in ["19-sep", "10-oct", "14-nov", "28-nov", "19-dic", "5-sep", "26-30"]:
            if mala in texto:
                print("   !! FECHA DE CALENDARIO en los hitos:", mala); ok = False
    if paginas_esperadas and d.page_count != paginas_esperadas:
        print("  !! se esperaban %d paginas" % paginas_esperadas); ok = False
    print("  MEDICION:", "OK" if ok else "HAY DEFECTOS")

    for k in CLAVES[tag]:
        pgs = [i for i, pg in enumerate(d, 1) if k in pg.get_text()]
        print("   %-34s -> paginas %s" % (k, pgs))
        if not pgs:
            print("     !! clave ausente"); ok = False
    d.close()
    return ok


if __name__ == "__main__":
    armar_htmls()
    inlinar()
    numerar()
    todo = True
    for nombre, tag, npag in DOCS:
        print("\n=== %s ===" % nombre)
        pdf = render(nombre, tag)
        todo = medir(pdf, nombre, tag, npag) and todo
    print("\n>>> RESULTADO GLOBAL:", "TODO OK" if todo else "HAY DEFECTOS QUE CORREGIR")
