#!/usr/bin/env python3
"""Tests offline de la logica de clasificacion de merge_queue_status.

Solo cubren la funcion PURA `classify` (no toca git). El resto del tool es integracion
con git en vivo y se verifica corriendolo contra los repos reales (ver el diario de la noche).

    python -m unittest tools.test_merge_queue_status   (desde MATI-HQ)
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from merge_queue_status import classify, is_doc, collision_kind


def clean(**kw):
    base = {"clean": True, "behind": 0, "ahead": 1, "conflict_files": [],
            "added": [], "modified": [], "deleted": [], "binaries": []}
    base.update(kw)
    return base


class TestClassify(unittest.TestCase):
    def test_limpio_aditivo(self):
        label, _ = classify(clean(added=["tools/x.py", "docs/x.md"]), [])
        self.assertEqual(label, "LIMPIO-ADITIVO")

    def test_conflicto_gana_sobre_todo(self):
        a = {"clean": False, "ahead": 1, "conflict_files": ["QUE_FALTA.md", "b.py"]}
        label, note = classify(a, [])
        self.assertEqual(label, "CONFLICTO")
        self.assertIn("2", note)

    def test_borra_archivos_es_peligro(self):
        # Aunque tambien agregue y modifique, si el merge borra, gana BORRA-ARCHIVOS.
        label, note = classify(clean(added=["a.py"], deleted=["misiones/sel.py", "misiones/lab.py"]), [])
        self.assertEqual(label, "BORRA-ARCHIVOS")
        self.assertIn("2", note)

    def test_borra_pierde_contra_conflicto(self):
        a = {"clean": False, "ahead": 1, "conflict_files": ["x"]}
        label, _ = classify(a, [])
        self.assertEqual(label, "CONFLICTO")

    def test_binarios(self):
        label, _ = classify(clean(added=["src.ino"], binaries=["build/x.bin", "build/x.elf"]), [])
        self.assertEqual(label, "BINARIOS")

    def test_binarios_pierde_contra_borra(self):
        label, _ = classify(clean(deleted=["z.py"], binaries=["build/x.bin"]), [])
        self.assertEqual(label, "BORRA-ARCHIVOS")

    def test_subsumido(self):
        label, note = classify(clean(added=["a"]), ["nocturno/local-2026-07-22-readme-drift"])
        self.assertEqual(label, "SUBSUMIDO")
        self.assertIn("07-22", note)

    def test_subsumido_pierde_contra_binarios(self):
        # Un branch subsumido que ademas arrastra binarios: la senal mas dura (binarios) manda.
        label, _ = classify(clean(binaries=["x.bin"]), ["otro-branch"])
        self.assertEqual(label, "BINARIOS")

    def test_revisar_stale_si_modifica_desde_base_vieja(self):
        # Limpio, sin borrar, sin binarios, no subsumido, pero modifica y esta atras => REVISAR-STALE.
        label, note = classify(clean(behind=6, modified=["fw/a.py", "fw/b.py"]), [])
        self.assertEqual(label, "REVISAR-STALE")
        self.assertIn("6", note)

    def test_modifica_pero_al_dia_es_aditivo(self):
        # behind=0: aunque modifique, no es "stale" (arranco del main de hoy) => LIMPIO-ADITIVO.
        label, _ = classify(clean(behind=0, modified=["a.py"]), [])
        self.assertEqual(label, "LIMPIO-ADITIVO")

    def test_ya_en_main_gana_sobre_subsumido(self):
        # Rama huerfana en el tip de main (ahead=0): no-op, aunque sea ancestro de otras.
        label, _ = classify(clean(ahead=0), ["otra", "otra2"])
        self.assertEqual(label, "YA-EN-MAIN")

    def test_ahead_cero_no_pisa_conflicto_imposible(self):
        # Un branch sin commits nuevos no puede conflictuar; ahead=0 manda y es no-op.
        label, _ = classify(clean(ahead=0), [])
        self.assertEqual(label, "YA-EN-MAIN")

    def test_conflicto_solo_docs_es_trivial(self):
        # El caso real de galgas: todos conflictuan solo en QUE_FALTA.md.
        a = {"clean": False, "ahead": 1, "conflict_files": ["QUE_FALTA.md"]}
        label, note = classify(a, [])
        self.assertEqual(label, "CONFLICTO")
        self.assertIn("SOLO docs", note)
        self.assertIn("QUE_FALTA.md", note)

    def test_conflicto_codigo_pide_revision(self):
        a = {"clean": False, "ahead": 1, "conflict_files": ["firmware/main.py"]}
        _, note = classify(a, [])
        self.assertIn("CODIGO", note)

    def test_conflicto_mixto(self):
        a = {"clean": False, "ahead": 1, "conflict_files": ["QUE_FALTA.md", "config.h"]}
        _, note = classify(a, [])
        self.assertIn("doc+codigo", note)

    def test_stale_solo_docs_tag(self):
        _, note = classify(clean(behind=2, modified=["QUE_FALTA.md", "README.md"]), [])
        self.assertIn("solo docs", note)


class TestIsDoc(unittest.TestCase):
    def test_markdown_y_texto(self):
        for p in ("QUE_FALTA.md", "docs/x.md", "notas.txt", "README", "CHANGELOG"):
            self.assertTrue(is_doc(p), p)

    def test_carpeta_docs_cualquier_extension(self):
        self.assertTrue(is_doc("docs/diagrama.svg"))
        self.assertTrue(is_doc("firmware/docs/api.html"))

    def test_codigo_config_sql_no_son_doc(self):
        for p in ("firmware/main.py", "config.h", "web/App.jsx", "migration.sql", "eco.py"):
            self.assertFalse(is_doc(p), p)


class TestCollisionKind(unittest.TestCase):
    def test_vacio_es_doc(self):
        self.assertEqual(collision_kind([]), "doc")

    def test_todos_doc(self):
        self.assertEqual(collision_kind(["QUE_FALTA.md", "README.md"]), "doc")

    def test_todos_codigo(self):
        self.assertEqual(collision_kind(["a.py", "b.ino"]), "codigo")

    def test_mixto(self):
        self.assertEqual(collision_kind(["QUE_FALTA.md", "a.py"]), "mixto")


if __name__ == "__main__":
    unittest.main()
