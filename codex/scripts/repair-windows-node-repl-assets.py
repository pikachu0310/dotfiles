#!/usr/bin/env python3
"""Diagnose missing asset directories held by the official Windows node_repl.

Run on native Windows. Only --repair creates directories. The provider writes
its own assets on the next ordinary tool call; this script never writes them.
No UI input, process restart, privilege elevation, or configuration changes.
"""

import argparse
import ctypes
from ctypes import wintypes as wt
import json
import os
from pathlib import Path
import re
import sys
import tomllib


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repair", action="store_true")
    args = parser.parse_args()
    if sys.platform != "win32":
        parser.error("Use native Windows Python, not WSL Python.")
    if ctypes.sizeof(ctypes.c_void_p) != 8:
        parser.error("Use 64-bit Windows Python for the installed runtime.")
    sys.stdout.reconfigure(encoding="utf-8")
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    config = tomllib.loads((codex_home / "config.toml").read_text(encoding="utf-8"))
    configured = Path(config["mcp_servers"]["node_repl"]["command"]).resolve(strict=True)
    if configured.name.lower() != "node_repl.exe" or not re.search(
        r"\\OpenAI\\Codex\\runtimes\\cua_node\\[^\\]+\\bin\\node_repl\.exe$",
        str(configured), re.I,
    ):
        parser.error("The configured node_repl is not the installed official app runtime.")
    temp_root = Path(os.environ["TEMP"]).resolve(strict=True)
    pattern = re.compile(re.escape(str(temp_root).encode()) + rb"\\\.tmp[A-Za-z0-9]{6}")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)

    class ProcessEntry(ctypes.Structure):
        _fields_ = [
            ("dwSize", wt.DWORD), ("cntUsage", wt.DWORD), ("th32ProcessID", wt.DWORD),
            ("th32DefaultHeapID", ctypes.c_size_t), ("th32ModuleID", wt.DWORD),
            ("cntThreads", wt.DWORD), ("th32ParentProcessID", wt.DWORD),
            ("pcPriClassBase", wt.LONG), ("dwFlags", wt.DWORD), ("szExeFile", wt.WCHAR * 260),
        ]

    class MemoryInfo(ctypes.Structure):
        _fields_ = [
            ("BaseAddress", ctypes.c_void_p), ("AllocationBase", ctypes.c_void_p),
            ("AllocationProtect", wt.DWORD), ("PartitionId", wt.WORD),
            ("RegionSize", ctypes.c_size_t), ("State", wt.DWORD),
            ("Protect", wt.DWORD), ("Type", wt.DWORD),
        ]

    def bind(name, parameters, result):
        function = getattr(kernel, name)
        function.argtypes = parameters
        function.restype = result
        return function

    snapshot = bind("CreateToolhelp32Snapshot", [wt.DWORD, wt.DWORD], wt.HANDLE)
    first = bind("Process32FirstW", [wt.HANDLE, ctypes.POINTER(ProcessEntry)], wt.BOOL)
    next_process = bind("Process32NextW", [wt.HANDLE, ctypes.POINTER(ProcessEntry)], wt.BOOL)
    open_process = bind("OpenProcess", [wt.DWORD, wt.BOOL, wt.DWORD], wt.HANDLE)
    close = bind("CloseHandle", [wt.HANDLE], wt.BOOL)
    image_path = bind("QueryFullProcessImageNameW", [wt.HANDLE, wt.DWORD, wt.LPWSTR, ctypes.POINTER(wt.DWORD)], wt.BOOL)
    query = bind("VirtualQueryEx", [wt.HANDLE, ctypes.c_void_p, ctypes.POINTER(MemoryInfo), ctypes.c_size_t], ctypes.c_size_t)
    read = bind("ReadProcessMemory", [wt.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)], wt.BOOL)
    exit_code = bind("GetExitCodeProcess", [wt.HANDLE, ctypes.POINTER(wt.DWORD)], wt.BOOL)
    session_id = bind("ProcessIdToSessionId", [wt.DWORD, ctypes.POINTER(wt.DWORD)], wt.BOOL)
    current_session = wt.DWORD()
    if not session_id(os.getpid(), ctypes.byref(current_session)):
        raise ctypes.WinError(ctypes.get_last_error())

    process_snapshot = snapshot(2, 0)
    if process_snapshot == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    candidates = []
    try:
        entry = ProcessEntry()
        entry.dwSize = ctypes.sizeof(entry)
        available = first(process_snapshot, ctypes.byref(entry))
        while available:
            if entry.szExeFile.lower() == "node_repl.exe":
                candidates.append(entry.th32ProcessID)
            available = next_process(process_snapshot, ctypes.byref(entry))
    finally:
        close(process_snapshot)

    missing = restored = inspected = 0
    for pid in candidates:
        process_session = wt.DWORD()
        if not session_id(pid, ctypes.byref(process_session)) or process_session.value != current_session.value:
            continue
        # Read/query rights only; no debug privilege or process-write access.
        handle = open_process(0x410, False, pid)
        if not handle:
            print(json.dumps({"pid": pid, "skipped": "process not readable", "error": ctypes.get_last_error()}))
            continue
        try:
            filename = ctypes.create_unicode_buffer(32768)
            length = wt.DWORD(len(filename))
            if not image_path(handle, 0, filename, ctypes.byref(length)):
                continue
            if os.path.normcase(filename.value) != os.path.normcase(str(configured)):
                continue
            inspected += 1
            address = 0
            paths = set()
            while address < 0x7FFFFFFFFFFF:
                info = MemoryInfo()
                if not query(handle, ctypes.c_void_p(address), ctypes.byref(info), ctypes.sizeof(info)):
                    break
                base, size = info.BaseAddress or 0, info.RegionSize
                # Only readable private allocations. Never save or print memory.
                if info.State == 0x1000 and info.Type == 0x20000 and not info.Protect & 0x101 and size < 64 * 1024 * 1024:
                    for offset in range(0, size, 1024 * 1024):
                        count = min(size - offset, 1024 * 1024)
                        buffer = ctypes.create_string_buffer(count)
                        actual = ctypes.c_size_t()
                        if read(handle, ctypes.c_void_p(base + offset), buffer, count, ctypes.byref(actual)):
                            data = buffer.raw[:actual.value]
                            paths.update(match.decode() for match in pattern.findall(data))
                            paths.update(match.decode() for match in pattern.findall(data.replace(b"\x00", b"")))
                if base + size <= address:
                    break
                address = base + size
            if len(paths) != 1:
                print(json.dumps({"pid": pid, "skipped": "asset directory is not unique", "candidateCount": len(paths)}))
                continue
            asset_path = Path(paths.pop())
            if asset_path.parent != temp_root or not re.fullmatch(r"\.tmp[A-Za-z0-9]{6}", asset_path.name):
                continue
            live = wt.DWORD()
            if not exit_code(handle, ctypes.byref(live)) or live.value != 259:
                continue
            was_missing = not asset_path.exists()
            if not was_missing and not asset_path.is_dir():
                print(json.dumps({"pid": pid, "skipped": "asset path exists but is not a directory"}))
                continue
            missing += was_missing
            if was_missing and args.repair:
                asset_path.mkdir()  # No parents, files, or existing directory changes.
                restored += 1
            print(json.dumps({"pid": pid, "assetDirectory": str(asset_path), "missing": was_missing, "restored": was_missing and args.repair}))
        finally:
            close(handle)
    print(json.dumps({"inspected": inspected, "missing": missing, "restored": restored, "repair": args.repair}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
