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
from merge_queue_status import classify


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


if __name__ == "__main__":
    unittest.main()
