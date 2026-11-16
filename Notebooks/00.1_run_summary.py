"""
00.1_run_summary.py
Run at the END of a notebook (after 00.0_setup_workspace_env.py was run at the
start). Prints the CDR, the version of every third-party package the notebook
imported, and the total wall-clock runtime, so they are saved in the notebook's
output.

Usage, as the last code cell of a notebook:
    %run -i ./00.1_run_summary.py

Packages are detected from the notebook's own executed cells (import and from
... import statements), so only packages the notebook actually imports are
listed, and the list updates itself when imports change. Standard-library
modules are skipped. To report a custom list instead, set PACKAGES first, using
pip package names (for example "matplotlib-venn", not "matplotlib_venn"):
    PACKAGES = ["pandas", "polars", "numpy", "scipy"]
    %run -i ./00.1_run_summary.py
Tools that are not Python imports (for example SBayesRC or the SAIGE Docker
image tag) are not detected and should be recorded manually.
"""

import ast as _ast
import datetime as _dt
import importlib.metadata as _md
import importlib.util as _iu
import os as _os
import sys as _sys
import time as _time


def _imported_packages():
    """Return {distribution name: version} for third-party packages imported
    in the notebook's executed cells."""
    try:
        from IPython import get_ipython
        ip = get_ipython()
        cells = list(ip.user_ns.get("In", []))
        transform = ip.input_transformer_manager.transform_cell
    except Exception:
        return None  # not running under IPython/Jupyter

    stdlib = set(getattr(_sys, "stdlib_module_names", ()))
    targets = []  # (top-level name, [full dotted names to try])
    for src in cells:
        try:
            tree = _ast.parse(transform(src))
        except Exception:
            continue
        for node in _ast.walk(tree):
            if isinstance(node, _ast.Import):
                for a in node.names:
                    targets.append((a.name.split(".")[0], [a.name]))
            elif isinstance(node, _ast.ImportFrom) and node.level == 0 and node.module:
                full = [f"{node.module}.{a.name}" for a in node.names] + [node.module]
                targets.append((node.module.split(".")[0], full))

    pkg_map = _md.packages_distributions()  # top-level module -> [dists]
    found = {}
    for top, fulls in targets:
        if top in stdlib or top in ("IPython", "__main__"):
            continue
        if top not in pkg_map:  # older Python: fall back to the import name as the package name
            for cand in (top, top.replace("_", "-")):
                try:
                    found[_md.metadata(cand)["Name"]] = _md.version(cand)
                    break
                except Exception:
                    continue
            continue
        dists = pkg_map[top]
        chosen = None
        if len(dists) == 1:
            chosen = dists[0]
        else:  # namespace package (e.g., google.*): match by file location
            for full in fulls:
                try:
                    origin = _iu.find_spec(full).origin
                except Exception:
                    continue
                if not origin:
                    continue
                for d in dists:
                    try:
                        files = _md.distribution(d).files or []
                        base = _md.distribution(d)
                        if any(str(base.locate_file(f)) == origin for f in files):
                            chosen = d
                            break
                    except Exception:
                        continue
                if chosen:
                    break
        if chosen:
            try:
                found[chosen] = _md.version(chosen)
            except Exception:
                pass
    return dict(sorted(found.items(), key=lambda kv: kv[0].lower()))


print("Run summary")
print("  CDR:", _os.environ.get("WORKSPACE_CDR", "not set").split(".")[-1])
print("  Python:", _sys.version.split()[0])

if "PACKAGES" in globals():  # custom list
    for _p in PACKAGES:
        try:
            print(f"  {_p}: {_md.version(_p)}")
        except _md.PackageNotFoundError:
            print(f"  {_p}: not installed (check the pip package name)")
else:
    _found = _imported_packages()
    if _found is None:
        print("  Packages: not detected (run inside Jupyter, or set PACKAGES)")
    else:
        for _p, _v in _found.items():
            print(f"  {_p}: {_v}")

if "_NB_START" in globals():
    _el = _time.time() - _NB_START
    print("  Notebook start:", globals().get("_NB_START_STR", "unknown"))
    print("  Notebook end:  ", _dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    print(f"  Wall-clock runtime: {_el/3600:.2f} h ({_el/60:.1f} min)")
else:
    print("  Runtime unavailable: run 00.0_setup_workspace_env.py at the start of the notebook.")

for _n in ("_ast", "_dt", "_md", "_iu", "_os", "_sys", "_time", "_imported_packages",
           "_found", "_p", "_v", "_el", "_n"):
    globals().pop(_n, None)
