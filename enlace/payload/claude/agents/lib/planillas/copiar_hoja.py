# -*- coding: utf-8 -*-
"""Copia una hoja COMPLETA de un .xlsx a otro: estilos, imagenes y area de impresion.

El problema: los indices de estilo (s="N") son locales a cada libro. Copiar el XML
de una hoja sin remapear produce una hoja con formatos random. Aca se anexan los
estilos del origen al final de los del destino y se desplazan los indices.
Las cadenas compartidas se convierten a inlineStr para no tocar sharedStrings.
"""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlsxfix import Book


def _bloque(xml, tag):
    m = re.search(r'<%s[^>]*>(.*?)</%s>' % (tag, tag), xml, re.S)
    if m:
        return m.group(1), m.start(), m.end()
    m = re.search(r'<%s[^>]*/>' % tag, xml)
    return ('', m.start(), m.end()) if m else ('', -1, -1)


def _items(bloque, tag):
    return re.findall(r'<%s\b[^>]*/>|<%s\b[^>]*>.*?</%s>' % (tag, tag, tag), bloque, re.S)


def _merge_lista(dst_xml, src_xml, cont, hijo):
    """Anexa los <hijo> del origen al <cont> del destino. Devuelve (xml_nuevo, offset)."""
    d, ds, de = _bloque(dst_xml, cont)
    s, _, _ = _bloque(src_xml, cont)
    if not s:
        return dst_xml, 0
    off = len(_items(d, hijo))
    nuevos = d + s
    total = off + len(_items(s, hijo))
    if ds < 0:
        return dst_xml, 0
    return (dst_xml[:ds] + '<%s count="%d">' % (cont, total) + nuevos + '</%s>' % cont
            + dst_xml[de:]), off


def copiar_hoja(src_path, src_idx, dst_path, out_path, nuevo_nombre=None, al_principio=True):
    src, dst = Book(src_path), Book(dst_path)
    s_xml = src.sheet(src_idx)
    nombre = nuevo_nombre or src.sheets[src_idx][0]

    # ---------- 1) estilos ----------
    ds, ss = dst.x('xl/styles.xml'), src.x('xl/styles.xml')
    ds, off_font = _merge_lista(ds, ss, 'fonts', 'font')
    ds, off_fill = _merge_lista(ds, ss, 'fills', 'fill')
    ds, off_bord = _merge_lista(ds, ss, 'borders', 'border')
    ds, off_csxf = _merge_lista(ds, ss, 'cellStyleXfs', 'xf')

    # los xf del origen deben apuntar a los indices ya desplazados
    s_cellxfs, _, _ = _bloque(ss, 'cellXfs')
    xfs_src = _items(s_cellxfs, 'xf')
    fix = []
    for x in xfs_src:
        x = re.sub(r'fontId="(\d+)"', lambda m: 'fontId="%d"' % (int(m.group(1)) + off_font), x)
        x = re.sub(r'fillId="(\d+)"', lambda m: 'fillId="%d"' % (int(m.group(1)) + off_fill), x)
        x = re.sub(r'borderId="(\d+)"', lambda m: 'borderId="%d"' % (int(m.group(1)) + off_bord), x)
        x = re.sub(r'xfId="(\d+)"', lambda m: 'xfId="%d"' % (int(m.group(1)) + off_csxf), x)
        fix.append(x)
    d_cellxfs, cs, ce = _bloque(ds, 'cellXfs')
    off_xf = len(_items(d_cellxfs, 'xf'))
    ds = (ds[:cs] + '<cellXfs count="%d">' % (off_xf + len(fix)) + d_cellxfs + ''.join(fix)
          + '</cellXfs>' + ds[ce:])
    dst.put('xl/styles.xml', ds)

    # ---------- 2) cadenas compartidas -> inline ----------
    try:
        sst = src.x('xl/sharedStrings.xml')
        cadenas = [re.sub(r'<rPh.*?</rPh>|<phoneticPr[^>]*/>', '', t, flags=re.S)
                   for t in _items(sst, 'si')]
        cadenas = [re.sub(r'^<si>|</si>$', '', c) for c in cadenas]
    except KeyError:
        cadenas = []

    def a_inline(m):
        cel = m.group(0)
        mv = re.search(r'<v>(\d+)</v>', cel)
        if not mv:
            return cel
        i = int(mv.group(1))
        cont = cadenas[i] if i < len(cadenas) else '<t></t>'
        cel = cel.replace(' t="s"', ' t="inlineStr"')
        return re.sub(r'<v>\d+</v>', '<is>%s</is>' % cont, cel)

    s_xml = re.sub(r'<c\b[^>]*t="s"[^>]*>.*?</c>', a_inline, s_xml, flags=re.S)
    # remapear indices de estilo
    s_xml = re.sub(r'(<(?:c|row|col)\b[^>]*?)s="(\d+)"',
                   lambda m: '%ss="%d"' % (m.group(1), int(m.group(2)) + off_xf), s_xml)

    # ---------- 3) imagenes y drawing ----------
    s_rels_p = 'xl/worksheets/_rels/sheet%d.xml.rels' % (src_idx + 1)
    if s_rels_p in src.items:
        rels = src.x(s_rels_p)
        dr = re.search(r'Target="[^"]*drawing(\d+)\.xml"', rels)
        if dr:
            n_draw = len([k for k in dst.items if re.match(r'xl/drawings/drawing\d+\.xml$', k)]) + 1
            d_xml = src.x('xl/drawings/drawing%s.xml' % dr.group(1))
            d_rels = src.x('xl/drawings/_rels/drawing%s.xml.rels' % dr.group(1))
            n_med = len([k for k in dst.items if k.startswith('xl/media/')])
            mapa = {}
            for m in re.finditer(r'Id="(rId\d+)"[^>]*Target="[^"]*?/([^/"]+)"', d_rels):
                rid, arch = m.group(1), m.group(2)
                ext = arch.rsplit('.', 1)[-1]
                n_med += 1
                nuevo = 'image%d.%s' % (n_med, ext)
                dst.items['xl/media/' + nuevo] = src.items['xl/media/' + arch]
                mapa[arch] = nuevo
            for viejo, nuevo in mapa.items():
                d_rels = d_rels.replace('/' + viejo, '/' + nuevo)
            dst.items['xl/drawings/drawing%d.xml' % n_draw] = d_xml.encode('utf8')
            dst.items['xl/drawings/_rels/drawing%d.xml.rels' % n_draw] = d_rels.encode('utf8')
            nueva_rel = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                         '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                         '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/'
                         '2006/relationships/drawing" Target="../drawings/drawing%d.xml"/></Relationships>'
                         % n_draw)
            dst._rel_hoja = nueva_rel
            s_xml = re.sub(r'<drawing[^>]*/>', '<drawing r:id="rId1"/>', s_xml)
        else:
            dst._rel_hoja = None
    else:
        dst._rel_hoja = None

    # ---------- 4) registrar la hoja ----------
    n_sheet = max([int(m.group(1)) for m in
                   (re.match(r'xl/worksheets/sheet(\d+)\.xml$', k) for k in dst.items) if m] + [0]) + 1
    ruta = 'xl/worksheets/sheet%d.xml' % n_sheet
    dst.items[ruta] = s_xml.encode('utf8')
    if getattr(dst, '_rel_hoja', None):
        dst.items['xl/worksheets/_rels/sheet%d.xml.rels' % n_sheet] = dst._rel_hoja.encode('utf8')

    wr = dst.x('xl/_rels/workbook.xml.rels')
    rid = 'rId%d' % (max([int(x) for x in re.findall(r'Id="rId(\d+)"', wr)] + [0]) + 1)
    wr = wr.replace('</Relationships>',
                    '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/'
                    '2006/relationships/worksheet" Target="worksheets/sheet%d.xml"/></Relationships>'
                    % (rid, n_sheet))
    dst.put('xl/_rels/workbook.xml.rels', wr)

    wb = dst.x('xl/workbook.xml')
    sid = max([int(x) for x in re.findall(r'sheetId="(\d+)"', wb)] + [0]) + 1
    nodo = '<sheet name="%s" sheetId="%d" r:id="%s"/>' % (nombre.replace('&', '&amp;'), sid, rid)
    wb = (wb.replace('<sheets>', '<sheets>' + nodo, 1) if al_principio
          else wb.replace('</sheets>', nodo + '</sheets>'))
    dst.put('xl/workbook.xml', wb)

    ct = dst.x('[Content_Types].xml')
    add = ('<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="application/vnd.openxmlformats-'
           'officedocument.spreadsheetml.worksheet+xml"/>' % n_sheet)
    if getattr(dst, '_rel_hoja', None):
        add += ('<Override PartName="/xl/drawings/drawing%d.xml" ContentType="application/vnd.openxml'
                'formats-officedocument.drawing+xml"/>' % n_draw)
    for ext in ('emf', 'wmf', 'png', 'jpeg'):
        if 'Extension="%s"' % ext not in ct:
            tipo = {'emf': 'image/x-emf', 'wmf': 'image/x-wmf',
                    'png': 'image/png', 'jpeg': 'image/jpeg'}[ext]
            add = '<Default Extension="%s" ContentType="%s"/>' % (ext, tipo) + add
    dst.put('[Content_Types].xml', ct.replace('</Types>', add + '</Types>'))

    # el orden de infos define el orden del zip; agregamos las partes nuevas
    import zipfile
    presentes = {i.filename for i in dst.infos}
    for k in dst.items:
        if k not in presentes:
            zi = zipfile.ZipInfo(k, date_time=(2026, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            dst.infos.append(zi)
    dst.save(out_path)
    return n_sheet
