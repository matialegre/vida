#!/usr/bin/env python3
"""resolve_doc_conflicts.py — pre-resuelve los conflictos SOLO-docs de la cola de merge.

Complementa a ``merge_queue_status.py``: aquel *clasifica* la cola y descubrio el hallazgo
que la des-asusta — de los branches ``nocturno/*`` que dan CONFLICTO, casi todos chocan en
UN unico archivo de bitacora (``QUE_FALTA.md``), no en firmware. Ese conflicto es trivial:
se resuelve tomando AMBOS lados (cada nocturno agrega su propia linea ``EN BRANCH ...``).

Pero "trivial" no es "gratis": alguien tiene que sentarse a resolver 8 merges a mano. Este
tool hace ese trabajo mecanico de antemano y deja, por cada branch, el ``QUE_FALTA.md`` ya
fusionado (union 3-way, sin marcadores de conflicto) listo para que un humano lo REVISE y lo
aplique en la sesion de drenaje. Convierte "8 merges manuales" en "8 revisar-y-copiar".

Es un GENERADOR, no un evaluador: NO mergea nada, NO toca los repos de trabajo (solo
``git show``/``merge-base``/``merge-file`` sobre archivos temporales) y escribe unicamente
dentro de MATI-HQ. La resolucion es un CANDIDATO — el humano la revisa antes de aplicar.

Por que union y no "tomar theirs": ``main`` puede haber avanzado su ``QUE_FALTA.md`` despues
de que nacio el branch (otro nocturno ya mergeado). Tomar theirs pisaria ese avance. La union
3-way (``git merge-file --union``) conserva las lineas nuevas de AMBOS lados: es exactamente
"tomar ambos lados" hecho bien.

Solo procesa branches cuyos archivos en conflicto son TODOS docs (``collision_kind == 'doc'``).
Si un branch choca en codigo/config/SQL, este tool lo SALTEA y lo deja para revision humana
real (lo marca en el reporte) — jamas auto-resuelve codigo.

Uso
---
    python tools/resolve_doc_conflicts.py            # escribe resoluciones + reporte a stdout
    python tools/resolve_doc_conflicts.py --check    # dry-run: solo lista, no escribe archivos
    python tools/resolve_doc_conflicts.py --repo C:/Proyectos/galgas
    python tools/resolve_doc_conflicts.py --outdir COLA_MERGE_RESOLUCIONES
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile

# Reutiliza la logica ya testeada de la cola de merge (git helpers + clasificacion doc/codigo).
# Import robusto para correr como script (tools/ en el path) y como modulo (tools.test_*).
try:
    from tools import merge_queue_status as mq
except ImportError:  # ejecutado directamente: el dir del script esta en sys.path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import merge_queue_status as mq

DEFAULT_OUTDIR = "COLA_MERGE_RESOLUCIONES"


def safe_name(branch: str) -> str:
    """Nombre de branch -> nombre de carpeta seguro (sin '/', ':' ni espacios).

    ``nocturno/local-2026-07-11-x`` -> ``nocturno__local-2026-07-11-x``. Funcion pura.
    """
    out = []
    for ch in branch:
        out.append(ch if (ch.isalnum() or ch in "-_.") else "_")
    return "".join(out).strip("_") or "branch"


def is_resolvable(conflict_files: list) -> bool:
    """True si el conflicto es 100% docs (se puede pre-resolver por union). Funcion pura.

    Lista vacia => False: 'clean' no pasa por aca, y sin archivos no hay nada que resolver.
    """
    if not conflict_files:
        return False
    return mq.collision_kind(conflict_files) == "doc"


def _show_to_file(repo: str, rev: str, path: str, dest: str) -> None:
    """Vuelca el blob ``rev:path`` a ``dest``. Si no existe en ese rev, deja ``dest`` vacio
    (caso de un archivo agregado en ambos lados => sin version base)."""
    proc = subprocess.run(
        ["git", "-C", repo, "show", f"{rev}:{path}"],
        capture_output=True,
    )
    with open(dest, "wb") as f:
        if proc.returncode == 0:
            f.write(proc.stdout)
        # rc!=0 => el path no existe en ese rev: base/ours/theirs vacio, merge-file lo maneja.


def union_merge_file(repo: str, base_ref: str, branch: str, path: str) -> tuple[bool, str]:
    """Union 3-way de ``path`` entre main (ours), la merge-base (base) y ``branch`` (theirs).

    Devuelve (ok, texto_fusionado). ``ok`` refleja que ``git merge-file --union`` no reporto
    error de I/O (con --union el rc de conflicto textual es 0 igual: no hay marcadores). NO
    toca el repo: extrae los 3 blobs a temporales y fusiona ahi.
    """
    rc, mbase = mq.git(repo, "merge-base", mq.main_branch(repo) or base_ref, branch)
    base_rev = mbase if rc == 0 and mbase else base_ref
    tmpdir = tempfile.mkdtemp(prefix="rdc_")
    ours = os.path.join(tmpdir, "ours")
    base = os.path.join(tmpdir, "base")
    theirs = os.path.join(tmpdir, "theirs")
    try:
        _show_to_file(repo, mq.main_branch(repo) or base_ref, path, ours)
        _show_to_file(repo, base_rev, path, base)
        _show_to_file(repo, branch, path, theirs)
        # merge-file -p --union <ours> <base> <theirs>: union en las zonas en conflicto
        # (conserva lineas de ambos lados, sin marcadores <<<<). -p => salida a stdout.
        proc = subprocess.run(
            ["git", "merge-file", "-p", "--union", ours, base, theirs],
            capture_output=True,
        )
        text = proc.stdout.decode("utf-8", errors="replace")
        # rc>=0 son conflictos resueltos por union; rc<0 (=-1 en git) es error real de I/O.
        ok = proc.returncode >= 0
        return ok, text
    finally:
        for p in (ours, base, theirs):
            try:
                os.remove(p)
            except OSError:
                pass
        try:
            os.rmdir(tmpdir)
        except OSError:
            pass


def drain_commands(repo: str, branch: str, main: str, files: list, res_dir_abs: str) -> list:
    """Comandos EXACTOS que un humano corre para drenar el branch usando la resolucion ya
    generada. Funcion pura (solo arma strings). NO se ejecutan aca."""
    cmds = [
        f'cd "{repo}"',
        f"git checkout {main}",
        f"git merge --no-ff --no-commit {branch}   # conflicto esperado en: {', '.join(files)}",
    ]
    for path in files:
        src = os.path.join(res_dir_abs, path).replace("\\", "/")
        cmds.append(f'cp "{src}" "{path}"   # resolucion candidata (revisar antes)')
    cmds.append(f"git add {' '.join(files)}")
    cmds.append('git commit --no-edit   # cierra el merge')
    return cmds


def build_plan(repos: list, outdir: str, write: bool) -> list:
    """Recorre los repos, arma la resolucion de cada branch CONFLICTO-solo-docs y (si write)
    escribe los archivos fusionados bajo ``outdir/<repo>/<branch>/<path>``."""
    plan = []
    for repo in repos:
        rc, _ = mq.git(repo, "rev-parse", "--git-dir")
        if rc != 0:
            continue
        main = mq.main_branch(repo)
        if main is None:
            continue
        repo_name = repo.rstrip("/").rsplit("/", 1)[-1]
        for branch in mq.nocturno_branches(repo):
            res = mq.merge_result(repo, main, branch)
            if res.get("clean"):
                continue
            cf = res.get("conflict_files", [])
            entry = {
                "repo": repo,
                "repo_name": repo_name,
                "branch": branch,
                "main": main,
                "conflict_files": cf,
                "resolvable": is_resolvable(cf),
                "files_written": [],
                "errors": [],
            }
            if entry["resolvable"]:
                res_dir = os.path.join(outdir, repo_name, safe_name(branch))
                for path in cf:
                    ok, text = union_merge_file(repo, main, branch, path)
                    if not ok:
                        entry["errors"].append(f"merge-file fallo en {path}")
                        continue
                    if write:
                        dest = os.path.join(res_dir, path)
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        with open(dest, "w", encoding="utf-8", newline="\n") as f:
                            f.write(text)
                    entry["files_written"].append(path)
                entry["res_dir_abs"] = os.path.abspath(res_dir)
            plan.append(entry)
    return plan


def render_markdown(plan: list, write: bool) -> str:
    out = ["# Resoluciones candidatas de la cola de merge (solo-docs)", ""]
    out.append(
        "> Generado por `tools/resolve_doc_conflicts.py`. Para cada branch `nocturno/*` que "
        "da **CONFLICTO solo en docs** (`QUE_FALTA.md` y similares), deja el archivo ya "
        "fusionado por **union 3-way** (toma ambos lados, sin marcadores) listo para revisar."
    )
    out.append("> **Es un candidato, no un merge**: revisar el archivo antes de aplicarlo. "
               "El tool no toca los repos ni ejecuta los comandos de drenaje.")
    out.append("")
    resolvables = [e for e in plan if e["resolvable"]]
    skipped = [e for e in plan if not e["resolvable"]]
    out.append(
        f"**{len(resolvables)} branches pre-resueltos** (solo-docs) · "
        f"**{len(skipped)} salteados** (tocan codigo — revision humana real)."
    )
    if not write:
        out.append("")
        out.append("_(modo `--check`: no se escribio ningun archivo)_")
    out.append("")

    if resolvables:
        out.append("## Pre-resueltos — revisar y aplicar")
        for e in resolvables:
            out.append("")
            out.append(f"### `{e['repo_name']}` · `{e['branch']}`")
            out.append(f"- Conflicto en: {', '.join('`'+f+'`' for f in e['conflict_files'])}")
            if e["errors"]:
                out.append(f"- ⚠️ Errores: {'; '.join(e['errors'])}")
            if write and e["files_written"]:
                out.append(f"- Resolucion escrita en: `{e['res_dir_abs']}`")
            out.append("- Drenaje sugerido (correr a mano, tras revisar la resolucion):")
            out.append("")
            out.append("```bash")
            out.extend(drain_commands(e["repo"], e["branch"], e["main"],
                                      e["files_written"] or e["conflict_files"],
                                      e.get("res_dir_abs", "")))
            out.append("```")

    if skipped:
        out.append("")
        out.append("## Salteados — conflicto toca codigo, NO auto-resolver")
        out.append("| Repo | Branch | Archivos en conflicto |")
        out.append("|---|---|---|")
        for e in skipped:
            files = ", ".join(e["conflict_files"]) or "?"
            out.append(f"| {e['repo_name']} | `{e['branch']}` | {files} |")
    out.append("")
    return "\n".join(out)


def parse_args(argv: list) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Pre-resuelve los conflictos solo-docs de la cola de merge.")
    p.add_argument("--repo", action="append", dest="repos", help="repo puntual (repetible). Default: los 4.")
    p.add_argument("--outdir", default=DEFAULT_OUTDIR, help=f"carpeta de salida (default: {DEFAULT_OUTDIR}).")
    p.add_argument("--check", action="store_true", help="dry-run: lista sin escribir archivos.")
    return p.parse_args(argv)


def main(argv: list) -> int:
    args = parse_args(argv)
    repos = args.repos or mq.DEFAULT_REPOS
    plan = build_plan(repos, args.outdir, write=not args.check)
    print(render_markdown(plan, write=not args.check))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
