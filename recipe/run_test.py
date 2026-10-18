from sys import exit
from subprocess import call
from pathlib import Path

COV_FAIL_UNDER = 95
REPORT = [
    "coverage",
    "report",
    "--show-missing",
    "--skip-covered",
    f"--fail-under={COV_FAIL_UNDER}",
]
PYTEST = ["pytest", "-vv", "--tb=long", "--color=yes", "pytest_beartype_test"]
COMBINE = ["coverage", "combine"]
RUN = ["coverage", "run", "--branch", "--source=pytest_beartype", "-m"]
COV_RC = [
    "[run]",
    "patch = subprocess",
]

EXCURSIONS = [
    [],
    ["--beartype-packages", "pytest_beartype"],
    ["--beartype-packages", "pytest"],
    [
        "--beartype-packages",
        "*",
        "--beartype-skip-packages",
        "pytest",
        "-k",
        "not weather_bad_usage",
    ],
]
CMDS = [
    *[[*RUN, *PYTEST, *ex] for ex in EXCURSIONS],
    COMBINE,
    REPORT,
    ["mypy", "-p", "pytest_beartype"],
]


def do(args: list[str]) -> int:
    print(">>>", *args, flush=True)
    rc = call(args)
    if rc:
        print("!!! FAIL", rc, *args, flush=True)
    return rc


if __name__ == "__main__":
    Path(".coveragerc").write_text("\n".join(COV_RC), encoding="utf-8")
    exit(any(map(do, CMDS)) or 0)
