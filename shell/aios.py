#!/usr/bin/env python3
"""AIOS Phase-0 shell.

Talk to the machine in short English. Only allowlisted actions run.
This is a userspace face, not a kernel.
"""

from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USE_ADB = os.environ.get("AIOS_ADB", "0") == "1"
ADB_SERIAL = os.environ.get("ANDROID_SERIAL", "")

# Intent keywords -> argv. Keep this tiny and explicit.
ACTIONS = {
    "who": ["id"],
    "id": ["id"],
    "kernel": ["uname", "-a"],
    "uname": ["uname", "-a"],
    "os": ["uname", "-a"],
    "linux": ["uname", "-a"],
    "ps": ["ps", "-A"],
    "processes": ["ps", "-A"],
    "mounts": ["mount"],
    "disk": ["df", "-h"],
    "pwd": ["pwd"],
    "help": None,
    "quit": None,
    "exit": None,
}


def run(argv: list[str]) -> str:
    if USE_ADB:
        prefix = ["adb"]
        if ADB_SERIAL:
            prefix += ["-s", ADB_SERIAL]
        prefix += ["shell"]
        cmd = prefix + argv
    else:
        cmd = argv
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    except FileNotFoundError:
        return f"missing binary: {cmd[0]}\n"
    except subprocess.TimeoutExpired:
        return "timed out\n"
    out = (p.stdout or "") + (p.stderr or "")
    return out if out.endswith("\n") else out + "\n"


def match(line: str) -> str | None:
    text = line.strip().lower()
    if not text:
        return ""
    for key, argv in ACTIONS.items():
        if key in text.split() or text == key:
            if key in {"quit", "exit"}:
                return None
            if key == "help" or text in {"help", "?"}:
                keys = ", ".join(sorted(k for k in ACTIONS if k not in {"help", "quit", "exit"}))
                return f"allowlisted intents: {keys}\nset AIOS_ADB=1 to run on the emulator via adb\n"
            assert argv is not None
            return run(argv)
    return (
        "refused: no allowlisted intent.\n"
        "type help. AIOS will not run free-form shell as root.\n"
    )


def main() -> int:
    target = "adb shell" if USE_ADB else "this host"
    print(f"AIOS phase-0  target={target}  (not a kernel)")
    print("type help, or quit")
    while True:
        try:
            line = input("aios> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        result = match(line)
        if result is None:
            return 0
        if result:
            sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
