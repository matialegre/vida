# -*- coding: utf-8 -*-
"""QA de contenido: verifica que textos que DEBEN estar en el PDF esten realmente."""
import fitz, sys, os, json

# textos que tienen que aparecer si ninguna columna quedo cortada
ESPERADO = {
    "1A00690 - Listado de Documentos.pdf": [
        "21/08/2026", "REVISIÓN: 0", "1A00690",
        "BB26005", "Layout de Ubicación de Instrumentos Detectores de Llama",
    ],
    "1A00711_1 - Listado de Direcciones Modbus.pdf": [
        "20/08/2026", "REVISIÓN: 1", "1A00711", "Señales Comunicadas",
        "DIRECCION", "TIPO DE ALIAS", "READ/WRITE",
        "FHD_DH2_01_BPO", "400100:8", "FHD_FHS_01_HRT", "401283",
        "Estado comunicación DCS",
    ],
    "1A00721 - Listado de Materiales.pdf": [
        "21/08/2026", "REVISIÓN: 0", "1A00721",
        "Observacion", "Descripcion", "Cantidad", "Modelo", "Marca",
        "SE- Norte 2", "Sala de rack", "SE- Sur", "JB",
    ],
}


# textos que NO deben aparecer (notas internas / campos corregidos)
PROHIBIDO = {
    "1A00690 - Listado de Documentos.pdf": ["Emitir en", "Dejar para CAO", "Fire & Gas Planta HDT", "HOJA 2 DE"],
    "1A00711_1 - Listado de Direcciones Modbus.pdf": ["Senales", "HOJA 2 A"],
    "1A00721 - Listado de Materiales.pdf": ["HOJA 2 DE", "HOJA 2 A"],
}


def texto_pdf(p):
    d = fitz.open(p)
    return "\n".join(d[i].get_text() for i in range(d.page_count)), d.page_count


def run(carpeta, solo=None):
    fallos = {}
    for nombre, probes in ESPERADO.items():
        if solo and solo not in nombre:
            continue
        p = os.path.join(carpeta, nombre)
        if not os.path.exists(p):
            print("FALTA", nombre); fallos[nombre] = ["archivo ausente"]; continue
        txt, n = texto_pdf(p)
        falta = [x for x in probes if x not in txt]
        sobra = [x for x in PROHIBIDO.get(nombre, []) if x in txt]
        estado = "OK" if not (falta or sobra) else "FALTAN %d / SOBRAN %d" % (len(falta), len(sobra))
        print("%-46s %2d pag  %s" % (nombre[:44], n, estado))
        for x in falta:
            print("      NO APARECE (deberia): %r" % x)
        for x in sobra:
            print("      APARECE (no deberia): %r" % x)
        if falta or sobra:
            fallos[nombre] = falta + sobra
    return fallos


if __name__ == '__main__':
    f = run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print("\nRESULTADO:", "TODO OK" if not f else "%d archivo(s) con texto faltante" % len(f))
    sys.exit(1 if f else 0)
