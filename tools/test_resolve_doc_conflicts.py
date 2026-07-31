#!/usr/bin/env python3
"""Tests offline de resolve_doc_conflicts.

Cubren las funciones PURAS (safe_name, is_resolvable, drain_commands). La union real
(union_merge_file / build_plan) es integracion con git en vivo y se verifica corriendo el
tool contra los repos reales (ver el diario de la noche).

    python -m unittest tools.test_resolve_doc_conflicts   (desde MATI-HQ)
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolve_doc_conflicts import (
    safe_name, is_resolvable, drain_commands, en_branch_refs, dedup_en_branch,
)


class TestSafeName(unittest.TestCase):
    def test_slash_y_dos_puntos_se_reemplazan(self):
        self.assertEqual(safe_name("nocturno/local-2026-07-11-x"),
                         "nocturno_local-2026-07-11-x")

    def test_conserva_guiones_puntos_underscores(self):
        self.assertEqual(safe_name("a-b_c.d"), "a-b_c.d")

    def test_espacios_y_simbolos(self):
        self.assertEqual(safe_name("feat: x y"), "feat__x_y")

    def test_nunca_vacio(self):
        self.assertEqual(safe_name("///"), "branch")

    def test_no_empieza_ni_termina_en_underscore(self):
        self.assertEqual(safe_name("/x/"), "x")


class TestIsResolvable(unittest.TestCase):
    def test_solo_docs_es_resolvable(self):
        self.assertTrue(is_resolvable(["QUE_FALTA.md"]))
        self.assertTrue(is_resolvable(["QUE_FALTA.md", "README.md"]))

    def test_codigo_no_es_resolvable(self):
        self.assertFalse(is_resolvable(["firmware/main.py"]))

    def test_mixto_no_es_resolvable(self):
        # Un solo archivo de codigo alcanza para exigir revision humana.
        self.assertFalse(is_resolvable(["QUE_FALTA.md", "config.h"]))

    def test_vacio_no_es_resolvable(self):
        self.assertFalse(is_resolvable([]))


class TestDrainCommands(unittest.TestCase):
    def setUp(self):
        self.cmds = drain_commands(
            "C:/Proyectos/galgas",
            "nocturno/local-2026-07-11-x",
            "main",
            ["QUE_FALTA.md"],
            "C:/HQ/RES/galgas/nocturno_local-2026-07-11-x",
        )

    def test_incluye_checkout_main_y_merge(self):
        joined = "\n".join(self.cmds)
        self.assertIn("git checkout main", joined)
        self.assertIn("git merge --no-ff --no-commit nocturno/local-2026-07-11-x", joined)

    def test_copia_la_resolucion_y_luego_add_commit(self):
        joined = "\n".join(self.cmds)
        self.assertIn("QUE_FALTA.md", joined)
        self.assertIn("git add QUE_FALTA.md", joined)
        # add y commit van DESPUES del cp (orden de resolucion de conflicto).
        i_cp = next(i for i, c in enumerate(self.cmds) if c.startswith("cp "))
        i_add = next(i for i, c in enumerate(self.cmds) if c.startswith("git add"))
        i_commit = next(i for i, c in enumerate(self.cmds) if c.startswith("git commit"))
        self.assertLess(i_cp, i_add)
        self.assertLess(i_add, i_commit)

    def test_no_mergea_ni_pushea_solo(self):
        # El tool nunca debe sugerir push/force/reset: el drenaje lo cierra un commit local.
        joined = "\n".join(self.cmds)
        for peligro in ("push", "--force", "reset --hard"):
            self.assertNotIn(peligro, joined)

    def test_multiples_archivos(self):
        cmds = drain_commands("R", "b", "main", ["QUE_FALTA.md", "README.md"], "/res")
        joined = "\n".join(cmds)
        self.assertIn("git add QUE_FALTA.md README.md", joined)
        self.assertEqual(sum(1 for c in cmds if c.startswith("cp ")), 2)


class TestEnBranchRefs(unittest.TestCase):
    def test_detecta_anotacion_con_markdown_y_backtick(self):
        txt = "    - 🔀 **EN BRANCH** `nocturno/local-2026-07-29-vpp` (pendiente)"
        self.assertEqual(en_branch_refs(txt), {"nocturno/local-2026-07-29-vpp": [0]})

    def test_multiples_lineas_mismo_branch(self):
        txt = ("a\n"
               "EN BRANCH `nocturno/local-x`\n"
               "b\n"
               "EN BRANCH nocturno/local-x otra redaccion\n")
        self.assertEqual(en_branch_refs(txt), {"nocturno/local-x": [1, 3]})

    def test_sin_anotaciones(self):
        self.assertEqual(en_branch_refs("solo texto\nsin branches"), {})


class TestDedupEnBranch(unittest.TestCase):
    def test_escenario_07_29_descarta_variante_del_branch(self):
        # main (ours) ya documenta el branch con SU redaccion; el branch trae otra.
        ours = ("2. Validacion\n"
                "    - EN BRANCH `nocturno/local-2026-07-29-vpp`: version de MAIN\n"
                "3. Test\n")
        # union 3-way: quedaron las dos anotaciones (falso duplicado).
        union = ("2. Validacion\n"
                 "    - EN BRANCH `nocturno/local-2026-07-29-vpp`: version de MAIN\n"
                 "    - EN BRANCH `nocturno/local-2026-07-29-vpp`: version del BRANCH\n"
                 "3. Test\n")
        out, dropped = dedup_en_branch(union, ours)
        self.assertEqual(len(dropped), 1)
        self.assertIn("version del BRANCH", dropped[0])
        # conserva EXACTAMENTE la linea de main, una sola vez.
        self.assertEqual(out.count("version de MAIN"), 1)
        self.assertNotIn("version del BRANCH", out)
        self.assertTrue(out.endswith("\n"))

    def test_sin_duplicado_no_toca_nada(self):
        txt = ("1. x\n"
               "    - EN BRANCH `nocturno/local-a`: unica\n"
               "2. y\n")
        out, dropped = dedup_en_branch(txt, txt)
        self.assertEqual(dropped, [])
        self.assertEqual(out, txt)

    def test_ninguna_coincide_con_main_deja_la_primera(self):
        # caso raro: ninguna de las dos anotaciones esta en main -> dedup puro, deja la 1a.
        ours = "sin anotaciones de branch\n"
        union = ("EN BRANCH `nocturno/local-a`: primera\n"
                 "EN BRANCH `nocturno/local-a`: segunda\n")
        out, dropped = dedup_en_branch(union, ours)
        self.assertEqual(len(dropped), 1)
        self.assertIn("segunda", dropped[0])
        self.assertIn("primera", out)

    def test_no_borra_bullets_de_branches_distintos(self):
        ours = "EN BRANCH `nocturno/local-a`: main-a\n"
        union = ("EN BRANCH `nocturno/local-a`: main-a\n"
                 "EN BRANCH `nocturno/local-b`: nuevo-b\n")
        out, dropped = dedup_en_branch(union, ours)
        self.assertEqual(dropped, [])
        self.assertIn("nuevo-b", out)
        self.assertIn("main-a", out)


if __name__ == "__main__":
    unittest.main()
