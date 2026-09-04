# -*- coding: utf-8 -*-
"""Mide en mm la altura de cada bloque de la hoja, para presupuestar el encaje."""
import os
from playwright.sync_api import sync_playwright
AQUI = os.path.dirname(os.path.abspath(__file__))
url = "file:///" + os.path.join(AQUI, __import__("sys").argv[1] if len(__import__("sys").argv)>1 else "PRESUPUESTO_1_UNO_POR_REEFER.html").replace("\\", "/")
js = """() => {
  const px2mm = 25.4/96;
  const out = [];
  document.querySelectorAll('.hoja').forEach((h,hi)=>{
    let tot = 0;
    h.querySelectorAll(':scope > *').forEach(e=>{
      const st = getComputedStyle(e);
      const alto = e.getBoundingClientRect().height
                 + parseFloat(st.marginTop) + parseFloat(st.marginBottom);
      tot += alto;
      out.push([hi+1, (e.className||e.tagName).toString().slice(0,34),
                +(alto*px2mm).toFixed(1)]);
    });
    out.push([hi+1, '>>> TOTAL HOJA', +(tot*px2mm).toFixed(1)]);
  });
  return out;
}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1440,"height":1000})
    pg.goto(url); pg.wait_for_timeout(300)
    for h, cls, mm in pg.evaluate(js):
        print("hoja %d  %-36s %7.1f mm" % (h, cls, mm))
    b.close()
