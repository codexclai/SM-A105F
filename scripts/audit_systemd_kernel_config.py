#!/usr/bin/env python3
"""Audit a Linux .config against systemd v257's published kernel needs."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CORE_REQUIRED = (
    "CONFIG_DEVTMPFS", "CONFIG_CGROUPS", "CONFIG_INOTIFY_USER",
    "CONFIG_SIGNALFD", "CONFIG_TIMERFD", "CONFIG_EPOLL", "CONFIG_UNIX",
    "CONFIG_NET", "CONFIG_SYSFS", "CONFIG_PROC_FS", "CONFIG_FHANDLE",
)
REQUIRED_OFF = ("CONFIG_SYSFS_DEPRECATED", "CONFIG_FW_LOADER_USER_HELPER")
RECOMMENDED_EMPTY = ("CONFIG_UEVENT_HELPER_PATH",)
SERVICE_SANDBOX = ("CONFIG_NET_NS", "CONFIG_USER_NS")
RECOMMENDED = (
    "CONFIG_IPV6", "CONFIG_AUTOFS_FS", "CONFIG_TMPFS_XATTR",
    "CONFIG_TMPFS_POSIX_ACL", "CONFIG_EXT4_FS_POSIX_ACL", "CONFIG_SECCOMP",
    "CONFIG_SECCOMP_FILTER", "CONFIG_KCMP", "CONFIG_NET_SCHED",
    "CONFIG_NET_SCH_FQ_CODEL", "CONFIG_CGROUP_SCHED",
    "CONFIG_FAIR_GROUP_SCHED", "CONFIG_CFS_BANDWIDTH", "CONFIG_BPF",
    "CONFIG_BPF_SYSCALL", "CONFIG_BPF_JIT", "CONFIG_CGROUP_BPF",
)


def parse_config(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        disabled = re.fullmatch(r"# (CONFIG_[A-Za-z0-9_]+) is not set", line.strip())
        if disabled:
            values[disabled.group(1)] = "n"
            continue
        match = re.fullmatch(r'(CONFIG_[A-Za-z0-9_]+)=(.*)', line.strip())
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"')
    return values


def audit_config(values: dict[str, str]) -> dict:
    enabled = lambda name: values.get(name) == "y"
    available = lambda name: values.get(name) in ("y", "m")
    missing = [name for name in CORE_REQUIRED if not enabled(name)]
    incorrectly_enabled = [name for name in REQUIRED_OFF if enabled(name)]
    legacy_helpers = [name for name in RECOMMENDED_EMPTY if values.get(name, "")]
    sandbox_gaps = [name for name in SERVICE_SANDBOX if not enabled(name)]
    recommended_missing = [name for name in RECOMMENDED if not available(name)]
    return {
        "systemd_baseline": "v257",
        "core_missing": missing,
        "required_disabled_options_enabled": incorrectly_enabled,
        "legacy_hotplug_helpers_configured": legacy_helpers,
        "service_sandbox_gaps": sandbox_gaps,
        "recommended_missing": recommended_missing,
        "core_requirements_pass": not missing and not incorrectly_enabled,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="Linux kernel .config")
    args = parser.parse_args()
    result = audit_config(parse_config(args.config.read_text(errors="replace")))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["core_requirements_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
