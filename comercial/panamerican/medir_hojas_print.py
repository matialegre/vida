# -*- coding: utf-8 -*-
"""Mide, EN MEDIA PRINT, cuanto mide cada .hoja y cada bloque de la hoja pedida.
   Sirve para presupuestar el encaje antes de tirar el PDF: la hoja util es 277 mm.
   Uso: python medir_hojas_print.py ARCHIVO.html [nro_de_hoja]
"""
import os, sys
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
arch = sys.argv[1] if len(sys.argv) > 1 else "PRESUPUESTO_CERRO_MORO.html"
hoja = int(sys.argv[2]) if len(sys.argv) > 2 else 0
url = "file:///" + os.path.join(AQUI, arch).replace("\\", "/")

JS = """(hoja) => {
  const px2mm = 25.4/96, out = [];
  document.querySelectorAll('.hoja').forEach((h,hi)=>{
    let tot = 0;
    h.querySelectorAll(':scope > *').forEach(e=>{
      const st = getComputedStyle(e);
      if (st.position === 'absolute') return;                // la marca de agua no ocupa flujo
      const alto = e.getBoundingClientRect().height
                 + parseFloat(st.marginTop) + parseFloat(st.marginBottom);
      tot += alto;
      if (hoja && hi+1 === hoja)
        out.push([hi+1, (e.className||e.tagName).toString().slice(0,34), +(alto*px2mm).toFixed(1)]);
    });
    out.push([hi+1, '>>> TOTAL HOJA (util 277)', +(tot*px2mm).toFixed(1)]);
  });
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 1000})
    pg.emulate_media(media="print")
    pg.goto(url)
    pg.wait_for_timeout(300)
    for h, cls, mm in pg.evaluate(JS, hoja):
        marca = "  <-- SE PASA" if cls.startswith(">>>") and mm > 277 else ""
        print("hoja %2d  %-36s %7.1f mm%s" % (h, cls, mm, marca))
    b.close()
