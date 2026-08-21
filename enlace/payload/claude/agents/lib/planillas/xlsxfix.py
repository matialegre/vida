"""Editor quirurgico de .xlsx por XML: preserva imagenes WMF, estilos y todo lo no tocado."""
import zipfile, re, os


class Book:
    def __init__(self, path):
        z = zipfile.ZipFile(path)
        self.infos = z.infolist()
        self.items = {n: z.read(n) for n in z.namelist()}
        z.close()
        wb = self.x('xl/workbook.xml')
        self.sheets = re.findall(r'<sheet name="([^"]*)"[^>]*r:id="(rId\d+)"', wb)
        rels = self.x('xl/_rels/workbook.xml.rels')
        rmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]*)"', rels))
        self.path_of = {}
        for i, (nm, rid) in enumerate(self.sheets):
            t = rmap[rid].lstrip('/')
            self.path_of[i] = t if t.startswith('xl/') else 'xl/' + t

    def x(self, n):
        return self.items[n].decode('utf8')

    def put(self, n, s):
        self.items[n] = s.encode('utf8')

    def sheet(self, i):
        return self.x(self.path_of[i])

    def putsheet(self, i, s):
        self.put(self.path_of[i], s)

    # ---------- estilos ----------
    def clone_style(self, idx, numfmt='0'):
        """Clona cellXfs[idx] con numFmtId dado y sin quotePrefix. Devuelve nuevo indice."""
        st = self.x('xl/styles.xml')
        m = re.search(r'(<cellXfs count=")(\d+)(">)(.*?)(</cellXfs>)', st, re.S)
        xfs = re.findall(r'<xf\b[^>]*/>|<xf\b[^>]*>.*?</xf>', m.group(4), re.S)
        new = re.sub(r'numFmtId="\d+"', 'numFmtId="%s"' % numfmt, xfs[idx]).replace(' quotePrefix="1"', '')
        if new in xfs:
            return xfs.index(new)
        out = (st[:m.start()] + m.group(1) + str(len(xfs) + 1) + m.group(3)
               + m.group(4) + new + m.group(5) + st[m.end():])
        self.put('xl/styles.xml', out)
        return len(xfs)

    # ---------- celdas ----------
    def _cell(self, s, ref):
        """OJO: el orden de la alternancia importa. Con `(?: [^>]*)?(?:/>|>.*?</c>)`,
        `[^>]*` puede tragarse la `/` de una celda vacia self-closing y entonces la
        segunda rama se come TODO hasta el proximo </c>, destruyendo celdas vecinas
        (asi se borro el encabezado TAG del 1A00711_1). Self-closing PRIMERO."""
        return re.search(r'<c r="%s"[^>]*/>|<c r="%s"[^>]*>.*?</c>' % (ref, ref), s, re.S)

    def set_formula(self, i, ref, formula, cached, numfmt='0'):
        s = self.sheet(i)
        m = self._cell(s, ref)
        if not m:
            raise KeyError('no existe %s en hoja %d' % (ref, i))
        sm = re.search(r's="(\d+)"', m.group(0))
        st = self.clone_style(int(sm.group(1)), numfmt) if sm else None
        sattr = ' s="%d"' % st if st is not None else ''
        esc = formula.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        cv = str(cached).replace('&', '&amp;').replace('<', '&lt;')
        cell = '<c r="%s"%s t="str"><f>%s</f><v>%s</v></c>' % (ref, sattr, esc, cv)
        self.putsheet(i, s[:m.start()] + cell + s[m.end():])

    def set_number(self, i, ref, num):
        s = self.sheet(i)
        m = self._cell(s, ref)
        sm = re.search(r's="(\d+)"', m.group(0))
        sattr = ' s="%s"' % sm.group(1) if sm else ''
        self.putsheet(i, s[:m.start()] + '<c r="%s"%s><v>%s</v></c>' % (ref, sattr, num) + s[m.end():])

    def set_text(self, i, ref, txt):
        """Escribe texto inline (evita tocar sharedStrings)."""
        s = self.sheet(i)
        m = self._cell(s, ref)
        sm = re.search(r's="(\d+)"', m.group(0))
        sattr = ' s="%s"' % sm.group(1) if sm else ''
        esc = txt.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # xml:space="preserve" es obligatorio si hay saltos de linea o espacios en
        # los bordes; sin eso Excel los descarta y el texto queda en un solo renglon
        sp = ' xml:space="preserve"' if (chr(10) in esc or esc != esc.strip()) else ''
        cell = '<c r="%s"%s t="inlineStr"><is><t%s>%s</t></is></c>' % (ref, sattr, sp, esc)
        self.putsheet(i, s[:m.start()] + cell + s[m.end():])

    # ---------- impresion ----------
    def page_setup(self, i, orientation=None, fitW=1, fitH=0, paper=9):
        s = self.sheet(i)
        m = re.search(r'<pageSetup\b[^>]*/>', s)
        old = m.group(0) if m else ''

        def g(a, d=None):
            mm = re.search(r'%s="([^"]*)"' % a, old)
            return mm.group(1) if mm else d

        orient = orientation or g('orientation', 'portrait')
        attrs = 'paperSize="%d" orientation="%s" fitToWidth="%d" fitToHeight="%d"' % (paper, orient, fitW, fitH)
        rid = g('r:id')
        if rid:
            attrs += ' r:id="%s"' % rid
        new = '<pageSetup %s/>' % attrs
        s = (s[:m.start()] + new + s[m.end():]) if m else s.replace('</worksheet>', new + '</worksheet>')

        if re.search(r'<pageSetUpPr\b[^>]*/>', s):
            s = re.sub(r'<pageSetUpPr\b[^>]*/>', '<pageSetUpPr fitToPage="1"/>', s)
        elif re.search(r'<sheetPr\b[^>]*>', s):
            def fix(mm):
                return (mm.group(1) + '><pageSetUpPr fitToPage="1"/></sheetPr>' if mm.group(2) == '/>'
                        else mm.group(1) + '><pageSetUpPr fitToPage="1"/>')
            s = re.sub(r'(<sheetPr\b[^>]*?)(/>|>)', fix, s, count=1)
        else:
            s = re.sub(r'(<worksheet\b[^>]*>)', r'\1<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr>', s, count=1)
        self.putsheet(i, s)

    def margins(self, i, l, r, t, b, hd=0.2, ft=0.2):
        s = self.sheet(i)
        new = '<pageMargins left="%s" right="%s" top="%s" bottom="%s" header="%s" footer="%s"/>' % (l, r, t, b, hd, ft)
        if '<pageMargins' in s:
            s = re.sub(r'<pageMargins\b[^>]*/>', new, s)
        self.putsheet(i, s)

    def clear_breaks(self, i, rows=True, cols=True):
        s = self.sheet(i)
        if rows:
            s = re.sub(r'<rowBreaks\b.*?</rowBreaks>|<rowBreaks\b[^>]*/>', '', s, flags=re.S)
        if cols:
            s = re.sub(r'<colBreaks\b.*?</colBreaks>|<colBreaks\b[^>]*/>', '', s, flags=re.S)
        self.putsheet(i, s)

    def col_width(self, i, col_idx, width):
        """Fija el ancho de UNA columna, partiendo el rango <col> que la contenga.
        Si ninguna la cubre, inserta un <col> nuevo (creando <cols> si hace falta)."""
        s = self.sheet(i)
        hit = [False]

        def rep(m):
            a = m.group(0)
            lo = int(re.search(r'min="(\d+)"', a).group(1))
            hi = int(re.search(r'max="(\d+)"', a).group(1))
            if not (lo <= col_idx <= hi):
                return a
            hit[0] = True
            mid = re.sub(r'min="\d+"', 'min="%d"' % col_idx, a)
            mid = re.sub(r'max="\d+"', 'max="%d"' % col_idx, mid)
            mid = re.sub(r'width="[^"]*"', 'width="%s"' % width, mid)
            if 'width=' not in mid:
                mid = mid.replace('/>', ' width="%s"/>' % width)
            if 'customWidth' not in mid:
                mid = mid.replace('/>', ' customWidth="1"/>')
            out = ''
            if lo < col_idx:
                out += re.sub(r'max="\d+"', 'max="%d"' % (col_idx - 1), a)
            out += mid
            if hi > col_idx:
                out += re.sub(r'min="\d+"', 'min="%d"' % (col_idx + 1), a)
            return out

        s = re.sub(r'<col\b[^>]*/>', rep, s)
        if not hit[0]:
            node = '<col min="%d" max="%d" width="%s" customWidth="1"/>' % (col_idx, col_idx, width)
            if '<cols>' in s:
                s = s.replace('<cols>', '<cols>' + node, 1)
            else:
                s = re.sub(r'(<sheetData\b)', '<cols>' + node + '</cols>' + r'\1', s, count=1)
        # <cols> DEBE estar ordenado por min ascendente o Excel marca el archivo como dañado
        mc = re.search(r'<cols>(.*?)</cols>', s, re.S)
        if mc:
            nodes = re.findall(r'<col\b[^>]*/>', mc.group(1))
            nodes.sort(key=lambda a: int(re.search(r'min="(\d+)"', a).group(1)))
            s = s[:mc.start()] + '<cols>' + ''.join(nodes) + '</cols>' + s[mc.end():]
        self.putsheet(i, s)

    def print_area(self, i, ref):
        wb = self.x('xl/workbook.xml')
        raw = self.sheets[i][0]
        name = raw.replace('&amp;', '&')
        q = "'%s'" % name if re.search(r'[\s&\-]', name) else name
        q = q.replace('&', '&amp;').replace("'", "&apos;") if '&' in q else q
        node = ('<definedName name="_xlnm.Print_Area" localSheetId="%d">%s!%s</definedName>' % (i, q, ref))
        pat = r'<definedName name="_xlnm\.Print_Area" localSheetId="%d">.*?</definedName>' % i
        if re.search(pat, wb, re.S):
            wb = re.sub(pat, node, wb, flags=re.S)
        elif '<definedNames>' in wb:
            wb = wb.replace('<definedNames>', '<definedNames>' + node, 1)
        else:
            wb = re.sub(r'(</sheets>)', r'\1<definedNames>' + node + '</definedNames>', wb, count=1)
        self.put('xl/workbook.xml', wb)

    def recalc_on_load(self):
        wb = self.x('xl/workbook.xml')
        if '<calcPr' in wb:
            wb = re.sub(r'<calcPr\b[^>]*/>', '<calcPr calcId="191029" fullCalcOnLoad="1"/>', wb)
        else:
            wb = wb.replace('</workbook>', '<calcPr calcId="191029" fullCalcOnLoad="1"/></workbook>')
        self.put('xl/workbook.xml', wb)

    def save(self, dst):
        d = os.path.dirname(dst)
        if d:
            os.makedirs(d, exist_ok=True)
        with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as z:
            for i in self.infos:
                zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
                zi.compress_type, zi.external_attr = i.compress_type, i.external_attr
                z.writestr(zi, self.items[i.filename])


# ---------------- calculo de escala de impresion ----------------
A4_W_IN, A4_H_IN = 8.2677, 11.6929   # 210 x 297 mm


def col_widths(book, i, lo, hi):
    """Anchos (en 'caracteres' Excel) de las columnas lo..hi de la hoja i."""
    s = book.sheet(i)
    m = re.search(r'defaultColWidth="([\d.]+)"', s)
    if m:
        default = float(m.group(1))
    else:
        b = re.search(r'baseColWidth="(\d+)"', s)
        default = float(b.group(1)) + 0.71 if b else 8.43
    w = {c: default for c in range(lo, hi + 1)}
    for node in re.findall(r'<col\b[^>]*/>', s):
        a = int(re.search(r'min="(\d+)"', node).group(1))
        z = int(re.search(r'max="(\d+)"', node).group(1))
        mw = re.search(r'width="([\d.]+)"', node)
        if not mw:
            continue
        for c in range(max(a, lo), min(z, hi) + 1):
            w[c] = float(mw.group(1))
    return w


def needed_scale(book, i, lo, hi, landscape=True, margins=0.25, cap=100, floor=25):
    """Escala % minima para que las columnas lo..hi entren a lo ancho de una A4."""
    total_px = sum(round(v * 7 + 5) for v in col_widths(book, i, lo, hi).values())
    total_in = total_px / 96.0
    page_in = (A4_H_IN if landscape else A4_W_IN) - 2 * margins
    sc = int((page_in / total_in) * 100)
    return max(floor, min(cap, sc)), round(total_in, 2), round(page_in, 2)


def set_scale(book, i, scale, orientation=None, paper=9):
    """Escala fija: apaga fitToPage (Excel lo prioriza) y fija scale."""
    s = book.sheet(i)
    m = re.search(r'<pageSetup\b[^>]*/>', s)
    old = m.group(0) if m else ''
    orient = orientation or (re.search(r'orientation="([^"]*)"', old).group(1) if 'orientation=' in old else 'portrait')
    rid = re.search(r'r:id="([^"]*)"', old)
    attrs = 'paperSize="%d" scale="%d" orientation="%s"' % (paper, scale, orient)
    if rid:
        attrs += ' r:id="%s"' % rid.group(1)
    new = '<pageSetup %s/>' % attrs
    s = (s[:m.start()] + new + s[m.end():]) if m else s.replace('</worksheet>', new + '</worksheet>')
    s = re.sub(r'<pageSetUpPr\b[^>]*/>', '<pageSetUpPr/>', s)
    book.putsheet(i, s)


def set_header(book, i, right=None, center=None, left=None):
    """Encabezado de pagina. Codigos: &P = pagina actual, &N = total. Va DESPUES de pageSetup."""
    s = book.sheet(i)
    parts = ''
    if left:   parts += '&L' + left
    if center: parts += '&C' + center
    if right:  parts += '&R' + right
    # los codigos &L/&C/&R/&P/&N llevan & literal -> hay que escaparlo o el XML es invalido
    node = '<headerFooter><oddHeader>%s</oddHeader></headerFooter>' % parts.replace('&', '&amp;')
    s = re.sub(r'<headerFooter\b.*?</headerFooter>|<headerFooter\b[^>]*/>', '', s, flags=re.S)
    m = re.search(r'<pageSetup\b[^>]*/>', s)
    s = s[:m.end()] + node + s[m.end():]
    book.putsheet(i, s)


def set_first_page(book, i, n):
    """Numera la 1a pagina de la hoja como n (para que &P siga contando desde la caratula)."""
    s = book.sheet(i)
    m = re.search(r'<pageSetup\b[^>]*/>', s)
    a = m.group(0)
    a = re.sub(r'\s*firstPageNumber="[^"]*"', '', a)
    a = re.sub(r'\s*useFirstPageNumber="[^"]*"', '', a)
    a = a.replace('/>', ' firstPageNumber="%d" useFirstPageNumber="1"/>' % n)
    book.putsheet(i, s[:m.start()] + a + s[m.end():])


def clear_header_footer(book, i):
    """Encabezado y pie VACIOS explicitos: sin esto LibreOffice imprime 'Pagina N de M'."""
    s = book.sheet(i)
    s = re.sub(r'<headerFooter\b.*?</headerFooter>|<headerFooter\b[^>]*/>', '', s, flags=re.S)
    node = '<headerFooter><oddHeader></oddHeader><oddFooter></oddFooter></headerFooter>'
    m = re.search(r'<pageSetup\b[^>]*/>', s)
    s = s[:m.end()] + node + s[m.end():]
    book.putsheet(i, s)


def center_h(book, i, horizontal=True, vertical=False):
    """Centra el area de impresion en la pagina. Sin esto el contenido queda pegado
    a la izquierda y el margen de ese lado puede caer bajo el minimo imprimible."""
    s = book.sheet(i)
    node = '<printOptions%s%s/>' % (' horizontalCentered="1"' if horizontal else '',
                                    ' verticalCentered="1"' if vertical else '')
    s = re.sub(r'<printOptions\b[^>]*/>', '', s)
    m = re.search(r'<pageMargins\b[^>]*/>', s)          # printOptions va ANTES de pageMargins
    s = s[:m.start()] + node + s[m.start():]
    book.putsheet(i, s)


def hide_rows(book, i, rows):
    """Oculta filas: NO se imprimen y el contenido no se pierde (reversible).
    Sirve para las filas 'fantasma' que solo tienen el numerito de item y que
    quedan en el MEDIO de la tabla, donde recortar el area de impresion no llega."""
    s = book.sheet(i)
    for r in rows:
        m = re.search(r'<row r="%d"(?: [^>]*)?(?:/>|>)' % r, s)
        if not m:
            continue
        tag = m.group(0)
        if 'hidden=' in tag:
            continue
        nuevo = tag.replace('>', ' hidden="1" customHeight="1">', 1) if not tag.endswith('/>') \
            else tag.replace('/>', ' hidden="1" customHeight="1"/>')
        s = s[:m.start()] + nuevo + s[m.end():]
    book.putsheet(i, s)


def sheet_states(book):
    """{nombre: 'visible'|'hidden'|'veryHidden'} leido de workbook.xml."""
    wb = book.x('xl/workbook.xml')
    out = {}
    for m in re.findall(r'<sheet [^>]*>', wb):
        nm = re.search(r'name="([^"]*)"', m).group(1).replace('&amp;', '&')
        st = re.search(r'state="([^"]*)"', m)
        out[nm] = st.group(1) if st else 'visible'
    return out


def del_print_area(book, i):
    """Borra el area de impresion de una hoja.
    OJO: LibreOffice exporta a PDF las hojas OCULTAS si tienen Print_Area definida.
    Sin area, no las incluye. (Asi se colaron 5 paginas A2 de otro proyecto en el
    1A00807_1: venian de las hojas ocultas HOJA 6..10.)"""
    wb = book.x('xl/workbook.xml')
    pat = r'<definedName name="_xlnm\.Print_Area" localSheetId="%d">.*?</definedName>' % i
    book.put('xl/workbook.xml', re.sub(pat, '', wb, flags=re.S))


def set_footer(book, i, center=None, left=None, right=None):
    """Pie de pagina. &P = pagina actual, &N = total de LA HOJA (no del libro).
    Para numerar contra el total del DOCUMENTO: set_first_page() por hoja y el
    total escrito a mano. Va DESPUES de pageSetup, reemplaza cualquier headerFooter."""
    s = book.sheet(i)
    p = ''
    if left:   p += '&L' + left
    if center: p += '&C' + center
    if right:  p += '&R' + right
    node = ('<headerFooter><oddHeader></oddHeader><oddFooter>%s</oddFooter></headerFooter>'
            % p.replace('&', '&amp;'))
    s = re.sub(r'<headerFooter\b.*?</headerFooter>|<headerFooter\b[^>]*/>', '', s, flags=re.S)
    m = re.search(r'<pageSetup\b[^>]*/>', s)
    book.putsheet(i, s[:m.end()] + node + s[m.end():])


def set_align(book, i, ref, horizontal='center'):
    """Cambia SOLO la alineacion horizontal de una celda, clonando su estilo."""
    s = book.sheet(i)
    m = book._cell(s, ref)
    sm = re.search(r's="(\d+)"', m.group(0))
    if not sm:
        return
    st = book.x('xl/styles.xml')
    mx = re.search(r'(<cellXfs count=")(\d+)(">)(.*?)(</cellXfs>)', st, re.S)
    xfs = re.findall(r'<xf\b[^>]*/>|<xf\b[^>]*>.*?</xf>', mx.group(4), re.S)
    proto = xfs[int(sm.group(1))]
    if '<alignment' in proto:
        nuevo = re.sub(r'horizontal="[^"]*"', 'horizontal="%s"' % horizontal, proto)
        if 'horizontal=' not in proto:
            nuevo = proto.replace('<alignment', '<alignment horizontal="%s"' % horizontal)
    else:
        nuevo = proto.replace('/>', '><alignment horizontal="%s"/></xf>' % horizontal) \
            if proto.endswith('/>') else proto.replace('</xf>', '<alignment horizontal="%s"/></xf>' % horizontal)
        if 'applyAlignment' not in nuevo:
            nuevo = nuevo.replace('<xf ', '<xf applyAlignment="1" ', 1)
    if nuevo in xfs:
        idx = xfs.index(nuevo)
    else:
        idx = len(xfs)
        st = (st[:mx.start()] + mx.group(1) + str(len(xfs) + 1) + mx.group(3)
              + mx.group(4) + nuevo + mx.group(5) + st[mx.end():])
        book.put('xl/styles.xml', st)
    cell = re.sub(r's="\d+"', 's="%d"' % idx, m.group(0))
    book.putsheet(i, s[:m.start()] + cell + s[m.end():])


def make_style(book, proto_idx, font=None, border=None, fill=None, **align):
    """Crea (o reutiliza) un cellXfs clonando proto_idx y cambiando fuente/borde/relleno
    y atributos de <alignment> (horizontal, vertical, textRotation, wrapText).
    Devuelve el indice del estilo."""
    st = book.x('xl/styles.xml')
    m = re.search(r'(<cellXfs count=")(\d+)(">)(.*?)(</cellXfs>)', st, re.S)
    xfs = re.findall(r'<xf\b[^>]*/>|<xf\b[^>]*>.*?</xf>', m.group(4), re.S)
    x = xfs[proto_idx]
    if font is not None:
        x = re.sub(r'fontId="\d+"', 'fontId="%d"' % font, x)
        x = x if 'applyFont' in x else x.replace('<xf ', '<xf applyFont="1" ', 1)
    if border is not None:
        x = re.sub(r'borderId="\d+"', 'borderId="%d"' % border, x)
        x = x if 'applyBorder' in x else x.replace('<xf ', '<xf applyBorder="1" ', 1)
    if fill is not None:
        x = re.sub(r'fillId="\d+"', 'fillId="%d"' % fill, x)
        x = x if 'applyFill' in x else x.replace('<xf ', '<xf applyFill="1" ', 1)
    if align:
        attrs = ' '.join('%s="%s"' % (k, v) for k, v in align.items())
        if '<alignment' in x:
            x = re.sub(r'<alignment[^/]*/>', '<alignment %s/>' % attrs, x)
        elif x.endswith('/>'):
            x = x[:-2] + '><alignment %s/></xf>' % attrs
        else:
            x = x.replace('</xf>', '<alignment %s/></xf>' % attrs)
        x = x if 'applyAlignment' in x else x.replace('<xf ', '<xf applyAlignment="1" ', 1)
    x = x.replace(' quotePrefix="1"', '')
    if x in xfs:
        return xfs.index(x)
    out = (st[:m.start()] + m.group(1) + str(len(xfs) + 1) + m.group(3)
           + m.group(4) + x + m.group(5) + st[m.end():])
    book.put('xl/styles.xml', out)
    return len(xfs)


def count_styles(book, what='cellXfs'):
    st = book.x('xl/styles.xml')
    m = re.search(r'<%s count="(\d+)"' % what, st)
    return int(m.group(1)) if m else 0


def copy_cell_style(book, i, desde, hacia):
    """Aplica a `hacia` el mismo estilo que tiene `desde` (misma hoja).
    Util para completar bordes que faltan en la ultima fila de una tabla."""
    s = book.sheet(i)
    md = book._cell(s, desde)
    if not md:
        return False
    sm = re.search(r's="(\d+)"', md.group(0))
    if not sm:
        return False
    mh = book._cell(s, hacia)
    if not mh:
        # la celda no existe en el XML: hay que crearla dentro de su <row>,
        # respetando el orden por columna (Excel lo exige)
        fila = int(re.search(r'\d+', hacia).group(0))
        colh = re.match(r'[A-Z]+', hacia).group(0)
        mr = re.search(r'<row r="%d"[^>]*/>|<row r="%d"[^>]*>.*?</row>' % (fila, fila), s, re.S)
        if not mr:
            return False
        fila_xml = mr.group(0)
        nueva = '<c r="%s" s="%s"/>' % (hacia, sm.group(1))
        def orden(ref):
            c = re.match(r'[A-Z]+', ref).group(0)
            return (len(c), c)
        celdas = re.findall(r'<c r="([A-Z]+)\d+"[^>]*/>|<c r="([A-Z]+)\d+"[^>]*>.*?</c>', fila_xml, re.S)
        pos = None
        for mc in re.finditer(r'<c r="([A-Z]+)\d+"[^>]*/>|<c r="([A-Z]+)\d+"[^>]*>.*?</c>', fila_xml, re.S):
            cc = mc.group(1) or mc.group(2)
            if orden(cc) > orden(colh):
                pos = mc.start()
                break
        if fila_xml.endswith('/>'):
            fila_xml = fila_xml[:-2] + '>' + nueva + '</row>'
        elif pos is None:
            fila_xml = fila_xml.replace('</row>', nueva + '</row>')
        else:
            fila_xml = fila_xml[:pos] + nueva + fila_xml[pos:]
        book.putsheet(i, s[:mr.start()] + fila_xml + s[mr.end():])
        return True
    cel = mh.group(0)
    cel = (re.sub(r's="\d+"', 's="%s"' % sm.group(1), cel) if 's="' in cel
           else cel.replace('<c r="%s"' % hacia, '<c r="%s" s="%s"' % (hacia, sm.group(1)), 1))
    book.putsheet(i, s[:mh.start()] + cel + s[mh.end():])
    return True


def set_row_breaks(book, i, filas):
    """Saltos de pagina manuales ANTES de cada fila indicada.
    Requiere escala fija (con fitToPage el motor de impresion los ignora).
    Sirve para que una fila logica de varias filas fisicas no quede partida."""
    s = book.sheet(i)
    s = re.sub(r'<rowBreaks\b.*?</rowBreaks>|<rowBreaks\b[^>]*/>', '', s, flags=re.S)
    if filas:
        brks = ''.join('<brk id="%d" max="16383" man="1"/>' % (f - 1) for f in sorted(filas))
        nodo = '<rowBreaks count="%d" manualBreakCount="%d">%s</rowBreaks>' % (len(filas), len(filas), brks)
        m = re.search(r'<headerFooter\b.*?</headerFooter>|<headerFooter\b[^>]*/>', s, re.S)
        if m:
            s = s[:m.end()] + nodo + s[m.end():]
        else:
            m = re.search(r'<pageSetup\b[^>]*/>', s)
            s = s[:m.end()] + nodo + s[m.end():]
    book.putsheet(i, s)


def cortes_por_bloque(src_xlsx, sheet, col_item, fila_ini, fila_fin,
                      alto_util, alto_titulo, default_h=13.2):
    """Devuelve las filas donde conviene cortar pagina para que ningun bloque
    (item que ocupa varias filas) quede partido entre dos hojas."""
    import openpyxl as _op
    ws = _op.load_workbook(src_xlsx)[sheet]
    alto = {}
    for r in range(fila_ini, fila_fin + 1):
        d = ws.row_dimensions.get(r)
        alto[r] = d.height if d and d.height else default_h
    inicios = [r for r in range(fila_ini, fila_fin + 1)
               if ws.cell(r, col_item).value not in (None, "")]
    if not inicios:
        return []
    bloques = []
    for k, r0 in enumerate(inicios):
        r1 = (inicios[k + 1] - 1) if k + 1 < len(inicios) else fila_fin
        bloques.append((r0, sum(alto[x] for x in range(r0, r1 + 1))))
    disponible = alto_util - alto_titulo
    cortes, usado = [], 0.0
    for r0, h in bloques:
        if usado + h > disponible and usado > 0:
            cortes.append(r0)
            usado = h
        else:
            usado += h
    return cortes


def drawing_de_hoja(book, i):
    """Ruta del drawing asociado a la hoja i, o None."""
    rp = 'xl/worksheets/_rels/sheet%d.xml.rels' % (i + 1)
    if rp not in book.items:
        return None
    m = re.search(r'Target="[^"]*?drawings/(drawing\d+\.xml)"', book.x(rp))
    return 'xl/drawings/' + m.group(1) if m else None


def quitar_imagen(book, i, fila_desde, fila_hasta):
    """Elimina del dibujo de la hoja las imagenes ancladas entre esas filas
    (base 0, como el XML). Sirve para sacar un logo repetido sin tocar el resto."""
    ruta = drawing_de_hoja(book, i)
    if not ruta:
        return []
    s = book.x(ruta)
    fuera = []
    pat = r'<xdr:twoCellAnchor.*?</xdr:twoCellAnchor>|<xdr:oneCellAnchor.*?</xdr:oneCellAnchor>'
    def rep(m):
        a = m.group(0)
        fr = re.search(r'<xdr:from>.*?<xdr:row>(\d+)</xdr:row>', a, re.S)
        if fr and fila_desde <= int(fr.group(1)) <= fila_hasta:
            nm = re.search(r'name="([^"]*)"', a)
            fuera.append(nm.group(1) if nm else 'sin nombre')
            return ''
        return a
    book.put(ruta, re.sub(pat, rep, s, flags=re.S))
    return fuera
