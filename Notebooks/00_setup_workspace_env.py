"""
00_setup_workspace_env.py
Run this at the top of every notebook in the Practical Considerations repository.

It sets, for the current All of Us Researcher Workbench workspace:
    GOOGLE_CLOUD_PROJECT   the workspace Google project ID
    WORKSPACE_BUCKET       gs:// path of the workspace bucket
    WORKSPACE_CDR          BigQuery dataset of the attached CDR (also set as an
                           environment variable)
    WORKSPACE_DIR          local folder where the workspace bucket is mounted
                           (use for savefig / write_csv, which cannot write gs://)
and it starts a wall-clock timer (_NB_START) and prints the machine you are
running on, so the run can be reported (see Supplementary Table 8).

Usage, as the first line of the first code cell of a notebook (the script sits
next to the notebooks in Notebooks/). Use -i so the script runs in the notebook's
own namespace; without it, BUCKET_ID_PATTERN and the timer are not shared:
    %run -i ./00_setup_workspace_env.py

At the end of the notebook, run 00.1_run_summary.py to print the CDR version,
package versions, and total runtime:
    PACKAGES = ["pandas", "polars"]
    %run -i ./00.1_run_summary.py

The workspace bucket is detected automatically (the CONTROLLED, non-temporary
GCS bucket resource). No bucket name or pattern is required. Only if your
workspace has more than one such bucket do you need to choose one, by setting
BUCKET_ID_PATTERN before running this script:
    BUCKET_ID_PATTERN = "my_bucket_name"
    %run -i ./00_setup_workspace_env.py
Without it, the first bucket is used and a warning listing all candidates is
printed.
"""

import datetime
import json
import os
import re
import subprocess
import sys
import time

# Google Cloud package fixes. Both upgrades use --no-deps so protobuf and the
# other packages are left untouched, and both must happen BEFORE any google.*
# package is imported:
#   google-api-core >= 2.26 : the preinstalled bigquery_storage_v1 calls
#                             api_core.check_python_version(), which older
#                             google-api-core versions do not have (AttributeError
#                             on "from google.cloud import bigquery").
#   grpcio >= 1.83.0        : removes the "grpcio < 1.83.0 / post-quantum"
#                             FutureWarning printed by the Google packages.
# If either is already loaded in this kernel, restart the kernel after this
# script finishes and re-run.
def _fix_google_packages(reqs=("google-api-core>=2.26", "grpcio>=1.83.0")):
    try:
        import importlib
        import importlib.metadata as md
        from packaging.requirements import Requirement
        todo = []
        for spec in reqs:
            r = Requirement(spec)
            try:
                ok = r.specifier.contains(md.version(r.name), prereleases=True)
            except md.PackageNotFoundError:
                ok = False
            if not ok:
                todo.append(spec)
        if not todo:
            return
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
                               "--no-deps", "--upgrade", *todo])
        importlib.invalidate_caches()
        print("Upgraded:", todo)
        if any(m in sys.modules for m in ("grpc", "google.api_core")):
            print("RESTART THE KERNEL and re-run: google packages were already "
                  "loaded in this kernel, so the upgrade takes effect after a restart.")
    except Exception as e:  # never fail the notebook over this
        print("Google package upgrade skipped:", e)


_fix_google_packages()


# Start the notebook timer (read by 00.1_run_summary.py)
_NB_START = time.time()
_NB_START_STR = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

# Optional: only needed if the workspace has more than one matching bucket
_BUCKET_ID_PATTERN = globals().get("BUCKET_ID_PATTERN")


def _wb(*args):
    """Run a wb command and return parsed JSON."""
    cmd = ["wb", *args, "--format=json"]
    result = subprocess.check_output(cmd, text=True, timeout=300)
    return json.loads(result)


# Get workspace info
_workspace = _wb("workspace", "describe")
GOOGLE_CLOUD_PROJECT = _workspace["googleProjectId"]

# Get resources
_resources = _wb("resource", "list")

# WORKSPACE_BUCKET
_EXCLUDE_SUBSTRINGS = ("temporary", "temp", "staging")

_bucket_resources = [
    r for r in _resources
    if r.get("resourceType") == "GCS_BUCKET"
    and r.get("stewardshipType", "CONTROLLED") == "CONTROLLED"
    and not any(s in r.get("id", "") for s in _EXCLUDE_SUBSTRINGS)
]

if _BUCKET_ID_PATTERN:
    _bucket_resources = [
        r for r in _bucket_resources
        if _BUCKET_ID_PATTERN in r.get("id", "")
    ]

if not _bucket_resources:
    _available = [r.get("id") for r in _resources if r.get("resourceType") == "GCS_BUCKET"]
    raise ValueError(
        "No matching bucket found"
        + (f" for pattern '{_BUCKET_ID_PATTERN}'" if _BUCKET_ID_PATTERN else "")
        + f". Available bucket resource ids: {_available}"
    )

_bucket_resources.sort(key=lambda r: r.get("id", ""))
if len(_bucket_resources) > 1:
    _ids = [r.get("id") for r in _bucket_resources]
    print(f"WARNING: multiple candidate buckets found: {_ids}. "
          f"Using '{_ids[0]}'. Set BUCKET_ID_PATTERN before running this "
          "script to choose a different one.")

WORKSPACE_BUCKET = f"gs://{_bucket_resources[0]['bucketName']}"

# WORKSPACE_CDR
_bq_resources = [
    r for r in _resources
    if r.get("resourceType") in {"BQ_DATASET", "BIGQUERY_DATASET"}
]

_CDR_RE = re.compile(r"^C(\d{4})Q(\d+)R(\d+)$")
_cdr_candidates = []

for r in _bq_resources:
    m = _CDR_RE.match(r.get("datasetId", ""))
    if m:
        _cdr_candidates.append(
            (tuple(int(g) for g in m.groups()),
             f"{r['projectId']}.{r['datasetId']}")
        )

if not _cdr_candidates:
    raise ValueError("No matching CDR dataset found")

_cdr_candidates.sort(reverse=True)
WORKSPACE_CDR = _cdr_candidates[0][1]

os.environ["WORKSPACE_CDR"] = WORKSPACE_CDR

if len(_cdr_candidates) > 1:
    print("multiple CDRs attached; using latest:",
          [c[1].split(".")[-1] for c in _cdr_candidates])

# Environment type and machine details (for reporting)
ENVIRONMENT = "Dataproc (Spark)" if os.path.isdir("/home/dataproc") else "Standard (Jupyter)"

# Local mount point of the workspace bucket: <prefix>/<bucket resource id>
_prefix = "/home/dataproc/workspace" if os.path.isdir("/home/dataproc") else "/home/jupyter/workspace"
WORKSPACE_DIR = f"{_prefix}/{_bucket_resources[0]['id']}"


def _cmd_line(cmd, idx):
    try:
        return subprocess.check_output(cmd, text=True).splitlines()[idx].strip()
    except Exception as e:  # reporting only; never fail the notebook
        return f"unavailable ({e})"


_machine_cpus = os.cpu_count()
_machine_mem = _cmd_line(["free", "-g"], 1)
_machine_disk = _cmd_line(["df", "-h", "/home"], -1)

# The project ID and bucket name identify the workspace, so they are set but
# not printed. Only the CDR release ID (e.g., C2025Q4R6) is shown.
CDR_DATASET_ID = WORKSPACE_CDR.split(".")[-1]
print("Workspace environment set (GOOGLE_CLOUD_PROJECT, WORKSPACE_BUCKET, WORKSPACE_CDR)")
print("  CDR:", CDR_DATASET_ID)
print("Run record:")
print("  Notebook start:", _NB_START_STR)
print("  Environment:", ENVIRONMENT)
print("  Python:", sys.version.split()[0])
print("  CPUs:", _machine_cpus)
print("  Memory (GB, 'free -g' Mem row):", _machine_mem)
print("  Disk (/home):", _machine_disk)

# Clean up internal helper objects so they don't clutter the notebook's
# global namespace (_NB_START and _NB_START_STR are kept for the run summary)
for _name in ("_wb", "_workspace", "_resources", "_bucket_resources",
              "_bq_resources", "_CDR_RE", "_cdr_candidates",
              "_BUCKET_ID_PATTERN", "_EXCLUDE_SUBSTRINGS", "_cmd_line",
              "_machine_cpus", "_machine_mem", "_machine_disk", "_prefix",
              "_fix_google_packages", "_name"):
    globals().pop(_name, None)
