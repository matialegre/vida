#!/usr/bin/env python3
"""merge_queue_status.py — vista fresca y CORRECTA de la cola de merge de branches nocturnos.

Regenera con git en vivo el estado de cada branch ``nocturno/*`` de los repos de Matias
frente al ``main`` de HOY. Reemplaza el mantenimiento a mano de ``COLA_MERGE_NOCTURNOS.md``
(que en 3 dias ya driftea: le faltan branches nuevos y arrastra clasificaciones viejas).

Metrica CLAVE (la razon de existir de este tool)
------------------------------------------------
Para saber "que le hace un merge de este branch a main" NO se usa ``git diff main..branch``
(two-dot): ese diff muestra las adiciones POSTERIORES de main como falsos "borrados" y llevo
a marcar como toxicos ("borran misiones/") branches que en realidad mergean limpios y aditivos.

Lo correcto es simular el merge 3-way real:

    tree = git merge-tree --write-tree main <branch>     # arbol resultante del merge
    git diff --name-status main <tree>                    # lo que el merge REALMENTE le hace a main

Asi ``-D`` (borrados) y ``-M`` (modificados) reflejan el impacto real sobre main, no un
artefacto del diff de tips. ``merge-tree --write-tree`` escribe objetos al object-store pero
NO toca refs ni working-tree: el tool es 100% de solo lectura (sin checkout/merge/reset).

Uso
---
    python tools/merge_queue_status.py                 # markdown a stdout (default: los 4 repos)
    python tools/merge_queue_status.py --json          # salida machine-readable
    python tools/merge_queue_status.py --repo C:/Proyectos/galgas   # un repo puntual
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

# Repos de Matias (main como rama de integracion). Rutas del MAPA_PROYECTOS.
DEFAULT_REPOS = [
    "C:/Proyectos/galgas",
    "C:/Proyectos/datalogger",
    "C:/Proyectos/frioseguro",
    "C:/Proyectos/cosechador",
]

# Extensiones que casi nunca deben entrar a main (artefactos de build).
BUILD_EXTS = (".bin", ".elf", ".map", ".hex", ".o", ".a", ".uf2", ".bootloader")


def git(repo: str, *args: str) -> tuple[int, str]:
    """Corre git en `repo` sin shell. Devuelve (returncode, stdout stripeado)."""
    proc = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout.strip()


def main_branch(repo: str) -> str | None:
    """Rama de integracion: 'main' si existe, si no 'master'."""
    for name in ("main", "master"):
        rc, _ = git(repo, "rev-parse", "--verify", "--quiet", f"refs/heads/{name}")
        if rc == 0:
            return name
    return None


def nocturno_branches(repo: str) -> list[str]:
    rc, out = git(repo, "branch", "--list", "nocturno/*", "--format=%(refname:short)")
    if rc != 0 or not out:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def merge_result(repo: str, base: str, branch: str) -> dict:
    """Simula el merge 3-way de `branch` en `base` y mide su impacto REAL sobre base.

    Devuelve: clean(bool), conflict_files, y si es limpio: added/modified/deleted
    (listas de paths) + binaries (paths con contenido binario o extension de build).
    """
    rc, out = git(repo, "merge-tree", "--write-tree", "--name-only", base, branch)
    lines = out.splitlines()
    tree = lines[0] if lines else ""
    if rc != 0:
        # rc==1 => conflicto; la 1ra linea es el OID del arbol, el resto los archivos en conflicto.
        return {"clean": False, "conflict_files": [l for l in lines[1:] if l.strip()]}

    added, modified, deleted = [], [], []
    _, ns = git(repo, "diff", "--name-status", base, tree)
    for row in ns.splitlines():
        parts = row.split("\t")
        if len(parts) < 2:
            continue
        status, path = parts[0], parts[-1]
        if status.startswith("A"):
            added.append(path)
        elif status.startswith("M"):
            modified.append(path)
        elif status.startswith("D"):
            deleted.append(path)

    # Binarios: numstat marca binario con '-\t-\t<path>'; ademas flageamos extensiones de build.
    binaries = []
    _, num = git(repo, "diff", "--numstat", base, tree)
    for row in num.splitlines():
        cols = row.split("\t")
        if len(cols) < 3:
            continue
        adds, dels, path = cols[0], cols[1], cols[-1]
        if (adds == "-" and dels == "-") or path.lower().endswith(BUILD_EXTS):
            binaries.append(path)

    return {
        "clean": True,
        "conflict_files": [],
        "added": added,
        "modified": modified,
        "deleted": deleted,
        "binaries": sorted(set(binaries)),
    }


def analyze(repo: str, base: str, branch: str) -> dict:
    _, behind = git(repo, "rev-list", "--count", f"{branch}..{base}")
    _, ahead = git(repo, "rev-list", "--count", f"{base}..{branch}")
    res = merge_result(repo, base, branch)
    res["behind"] = int(behind or 0)
    res["ahead"] = int(ahead or 0)
    res["branch"] = branch
    return res


def find_subsumed(repo: str, branches: list[str]) -> dict[str, list[str]]:
    """branch -> lista de otros branches que lo CONTIENEN (es su ancestro => subsumido)."""
    subsumed: dict[str, list[str]] = {}
    for a in branches:
        for b in branches:
            if a == b:
                continue
            rc, _ = git(repo, "merge-base", "--is-ancestor", a, b)
            if rc == 0:  # a es ancestro de b => a esta subsumido en b
                subsumed.setdefault(a, []).append(b)
    return subsumed


def classify(a: dict, subsumers: list[str]) -> tuple[str, str]:
    """Funcion PURA: (etiqueta, nota) segun las metricas. Testeable sin git.

    Prioridad de senales (de mas peligrosa a mas segura):
      YA-EN-MAIN      -> no tiene commits mas alla de main (rama huerfana/ya mergeada, no-op)
      CONFLICTO       -> merge-tree con conflicto textual (resolver a mano)
      BORRA-ARCHIVOS  -> el merge eliminaria archivos trackeados de main (revisar SI o SI)
      BINARIOS        -> arrastra artefactos de build al arbol
      SUBSUMIDO       -> es ancestro de otro branch pendiente (drenar solo el otro)
      REVISAR-STALE   -> limpio y sin borrar, pero modifica archivos desde una base vieja
      LIMPIO-ADITIVO  -> limpio, solo agrega: drenaje mecanico seguro
    """
    if a.get("ahead", 0) == 0:
        return "YA-EN-MAIN", "sin commits mas alla de main — nada que mergear, borrar la rama"
    if not a.get("clean"):
        n = len(a.get("conflict_files", []))
        return "CONFLICTO", f"{n} archivo(s) en conflicto — resolver a mano"
    if a.get("deleted"):
        d = a["deleted"]
        return "BORRA-ARCHIVOS", f"el merge borraria {len(d)} archivo(s): {', '.join(d[:4])}"
    if a.get("binaries"):
        return "BINARIOS", f"arrastra {len(a['binaries'])} binario(s)/artefacto(s) de build"
    if subsumers:
        return "SUBSUMIDO", f"ancestro de {', '.join(subsumers)} — drenar solo ese"
    if a.get("modified") and a.get("behind", 0) > 0:
        m = a["modified"]
        return "REVISAR-STALE", (
            f"limpio+aditivo pero modifica {len(m)} archivo(s) desde base {a['behind']} atras: "
            f"{', '.join(m[:4])} — revisar que no reviertan main"
        )
    return "LIMPIO-ADITIVO", "solo agrega archivos — drenaje mecanico seguro"


def render_markdown(report: list[dict]) -> str:
    out = ["# Estado de la cola de merge (regenerado con git en vivo)", ""]
    out.append(
        "> Generado por `tools/merge_queue_status.py`. Metrica de merge = arbol 3-way real "
        "(`merge-tree --write-tree`) diffeado contra main, NO `diff main..branch`."
    )
    out.append("> Solo lectura: el tool no hace checkout/merge/reset ni toca refs.")
    out.append("")
    total = sum(len(r["branches"]) for r in report)
    out.append(f"**{total} branches nocturnos** en {len(report)} repos.")
    out.append("")
    for r in report:
        out.append(f"## {r['repo']}  ·  main={r['main']} ({r['main_commits']} commits)")
        if r.get("error"):
            out.append(f"⚠️ {r['error']}")
            out.append("")
            continue
        if not r["branches"]:
            out.append("_sin branches nocturnos_")
            out.append("")
            continue
        out.append("| Branch | Atras | Merge | +A | ~M | -D | Estado | Nota |")
        out.append("|---|--:|---|--:|--:|--:|---|---|")
        for b in r["branches"]:
            label, note = b["status"], b["note"]
            merge = "CONFLICTO" if not b["clean"] else "limpio"
            adds = len(b.get("added", [])) if b["clean"] else "-"
            mods = len(b.get("modified", [])) if b["clean"] else "-"
            dels = len(b.get("deleted", [])) if b["clean"] else "-"
            name = b["branch"].replace("nocturno/local-", "…")
            out.append(
                f"| `{name}` | {b['behind']} | {merge} | {adds} | {mods} | {dels} | "
                f"**{label}** | {note} |"
            )
        out.append("")
    return "\n".join(out)


def build_report(repos: list[str]) -> list[dict]:
    report = []
    for repo in repos:
        rc, _ = git(repo, "rev-parse", "--git-dir")
        if rc != 0:
            report.append({"repo": repo, "error": "no es un repo git", "branches": [], "main": "?", "main_commits": 0})
            continue
        base = main_branch(repo)
        if base is None:
            report.append({"repo": repo, "error": "sin main/master", "branches": [], "main": "?", "main_commits": 0})
            continue
        _, mc = git(repo, "rev-list", "--count", base)
        branches = nocturno_branches(repo)
        subsumed = find_subsumed(repo, branches)
        analyzed = []
        for br in branches:
            a = analyze(repo, base, br)
            a["status"], a["note"] = classify(a, subsumed.get(br, []))
            analyzed.append(a)
        report.append(
            {"repo": repo, "main": base, "main_commits": int(mc or 0), "branches": analyzed}
        )
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Estado en vivo de la cola de merge de branches nocturnos.")
    p.add_argument("--repo", action="append", dest="repos", help="repo puntual (repetible). Default: los 4.")
    p.add_argument("--json", action="store_true", help="salida JSON en vez de markdown.")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    repos = args.repos or DEFAULT_REPOS
    report = build_report(repos)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
