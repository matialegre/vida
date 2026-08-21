# -*- coding: utf-8 -*-
"""Corrige los 3 entregables: revision, fecha propagada, y setup de impresion."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlsxfix import Book, set_scale, needed_scale, clear_header_footer

UP = r"C:\Users\Pandemonium\.claude\uploads\f1778220-d42b-4e80-837a-b9112ca538cd"
OUT = r"C:\Users\Pandemonium\Desktop\planillas_corregidas"

SRC = {
    'doc':   os.path.join(UP, "1ef69909-1A006900__Listado_de_Documentos.xlsx"),
    'modbus': os.path.join(UP, "2f7f20a0-1A00711_1__Listado_de_Direcciones_de_Comunicaci_n_Modbus.xlsx"),
    'mat':   os.path.join(UP, "cc1cfae3-1A00721__Listado_de_Materiales.xlsx"),
}
DST = {
    'doc':   os.path.join(OUT, "1A00690 - Listado de Documentos.xlsx"),
    'modbus': os.path.join(OUT, "1A00711_1 - Listado de Direcciones Modbus.xlsx"),
    'mat':   os.path.join(OUT, "1A00721 - Listado de Materiales.xlsx"),
}

# hojas: N total de paginas del PDF (se pasa por arg; 1a pasada usa el valor viejo)
TOTALES = {'doc': None, 'modbus': None, 'mat': None}
if len(sys.argv) > 1:
    import json
    TOTALES.update(json.loads(sys.argv[1]))


def hoja(b, nombre):
    for i, (n, _) in enumerate(b.sheets):
        if n.replace('&amp;', '&') == nombre:
            return i
    raise KeyError(nombre + ' / ' + str(b.sheets))


# =============== 1A00690 - Listado de Documentos - REV 0 ===============
def doc():
    b = Book(SRC['doc'])
    C, D = hoja(b, 'CARAT'), hoja(b, 'Documentos')
    # --- carATula: fecha de la rev actual (fila 34 = rev 0, 21/08/2026) ---
    b.set_formula(C, 'K44', 'C34', '21/08/2026')
    b.set_formula(C, 'J46', 'Q46', '0')
    b.set_number(C, 'Q46', 0)                       # revision 0
    if TOTALES['doc']:
        b.set_number(C, 'R44', TOTALES['doc'])
    # --- impresion carATula: 1 pagina exacta, A4 vertical ---
    b.margins(C, 0.25, 0.25, 0.25, 0.25)
    set_scale(b, C, 82, 'portrait')   # 86 no entraba con margenes de 0.25
    b.print_area(C, '$A$2:$S$47')
    # --- hoja Documentos: entraban solo hasta col M; N y Q quedaban FUERA ---
    b.print_area(D, '$A$1:$M$46')            # N y Q son notas internas: NO se imprimen
    SC_D = 52                                       # ancho A..M = 13.9" -> vertical necesita 55%
    b.margins(D, 0.25, 0.25, 0.35, 0.35)
    b.clear_breaks(D)                               # cortes viejos que ya no aplican
    b.set_formula(D, 'M4', 'CARAT!K44', '21/08/2026')   # cache viejo mostraba 06/04/2026
    b.set_text(C, 'D41', 'BB26005')                 # OBRA: decia 'Fire & Gas Planta HDT'
    b.set_formula(D, 'B4', 'CARAT!D41', 'BB26005')  # la hoja cuelga de D41: refrescar cache
    b.set_formula(D, 'K5', 'CARAT!L44', 'BB26005')  # cartel: nro de obra
    set_scale(b, D, SC_D, 'portrait')               # VERTICAL (como el original)
    for _h in range(len(b.sheets)):
        clear_header_footer(b, _h)   # sin 'Pagina N de M'
    b.recalc_on_load()
    b.save(DST['doc'])
    print('OK doc   -> rev 0 | K44==C34 | printArea A1:Q46 landscape')


# =============== 1A00711_1 - Direcciones Modbus - REV 1 ===============
def modbus():
    b = Book(SRC['modbus'])
    C, F = hoja(b, 'CARAT'), hoja(b, 'F&G')
    b.set_formula(C, 'K44', 'C35', '20/08/2026')    # fila 35 = revision vigente
    b.set_text(C, 'B35', '1')                       # 0 -> 1
    b.set_text(C, 'D41', 'BB26005')                 # OBRA: decia 'F&G HDT'
    b.set_number(C, 'Q46', 1)
    b.set_formula(C, 'J46', 'Q46', '1')
    if TOTALES['modbus']:
        b.set_number(C, 'R44', TOTALES['modbus'])
    b.margins(C, 0.25, 0.25, 0.25, 0.25)
    set_scale(b, C, 82, 'portrait')   # ORIGINAL 82: a 86 la portada se cortaba al imprimir
    b.print_area(C, '$A$2:$S$47')
    # --- hoja F&G: G4 era texto fijo '10/06/2026' -> colgarla de la carATula ---
    b.set_formula(F, 'G4', 'CARAT!K44', '20/08/2026')
    b.col_width(F, 4, 60)                           # col D: 109 -> 60 (era enorme)
    b.print_area(F, '$B$2:$G$876')
    set_scale(b, F, 58, 'portrait')                 # VERTICAL (como el original); ancho exige 63%
    b.set_text(F, 'D2', 'Listado de Señales Comunicadas')   # decia 'Senales'
    b.set_formula(F, 'E5', 'CARAT!L44', 'BB26005')  # cartel: nro de obra (estaba vacio)
    b.margins(F, 0.25, 0.25, 0.35, 0.35)
    b.clear_breaks(F)
    b.set_formula(F, 'E3', '"REVISIÓN: "&CARAT!Q46', 'REVISIÓN: 1')
    for _h in range(len(b.sheets)):
        clear_header_footer(b, _h)   # sin 'Pagina N de M'
    b.recalc_on_load()
    b.save(DST['modbus'])
    print('OK modbus-> rev 1 | K44==C35 | F&G!G4==CARAT!K44 | col D 109->60 landscape')


# =============== 1A00721 - Listado de Materiales - REV 0 ===============
PRIMERA_MAT = {'SE-Norte 2': 2, 'Sala de racks': 5, 'SE-Sur': 6, 'JB': 7}


def mat():
    b = Book(SRC['mat'])
    C = hoja(b, 'CARAT')
    b.set_formula(C, 'K44', 'C36', '21/08/2026')    # fila 36 = rev 0
    b.set_formula(C, 'J46', 'Q46', '0')
    b.set_number(C, 'Q46', 0)
    if TOTALES['mat']:
        b.set_number(C, 'R44', TOTALES['mat'])
    b.margins(C, 0.25, 0.25, 0.25, 0.25)
    set_scale(b, C, 81, 'portrait')   # escala original del doc
    b.print_area(C, '$A$2:$S$47')
    # --- las 4 hojas: P3 apuntaba a CARAT!B35 que esta VACIA -> no salia la revision ---
    areas = {'SE-Norte 2': '$A$1:$S$131', 'Sala de racks': '$A$1:$S$63',
             'SE-Sur': '$A$1:$S$66', 'JB': '$A$1:$S$19'}   # cortar filas con item vacio
    ESC = {'SE-Norte 2': 58, 'Sala de racks': 50, 'SE-Sur': 50, 'JB': 51}
    PRIMERA = PRIMERA_MAT
    _t = TOTALES['mat'] or 7
    ROTULO = {'SE-Norte 2': 'HOJA 2 A 4 DE %d' % _t, 'Sala de racks': 'HOJA 5 DE %d' % _t,
              'SE-Sur': 'HOJA 6 DE %d' % _t, 'JB': 'HOJA 7 DE %d' % _t}
    for nm, area in areas.items():
        i = hoja(b, nm)
        b.set_formula(i, 'P3', '"REVISI\u00d3N: "&CARAT!Q46', 'REVISI\u00d3N: 0')
        b.set_formula(i, 'R4', 'CARAT!K44', '21/08/2026')
        b.set_formula(i, 'P5', 'CARAT!L44', 'BB26005')   # cartel: nro de obra
        b.print_area(i, area)
        set_scale(b, i, ESC[nm], 'landscape')       # el original ya era horizontal
        b.margins(i, 0.25, 0.25, 0.35, 0.35)
        b.clear_breaks(i)
    for _h in range(len(b.sheets)):
        clear_header_footer(b, _h)   # sin 'Pagina N de M'
    b.recalc_on_load()
    b.save(DST['mat'])
    print('OK mat   -> rev 0 | K44==C36 | P3 B35(vacia)->Q46 en 4 hojas | R4==CARAT!K44')


doc(); modbus(); mat()
