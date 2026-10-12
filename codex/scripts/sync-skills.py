#!/usr/bin/env python3
"""Compare or deploy only the reviewed skills listed in config/personal-skills.json."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config/personal-skills.json"
IGNORED = {"__pycache__", ".git"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def files_in(folder):
    if folder.is_symlink():
        raise ValueError(f"Refusing symlinked skill folder: {folder}")
    result = {}
    if not folder.exists():
        return result
    if not folder.is_dir():
        raise ValueError(f"Expected a skill directory: {folder}")
    for path in folder.rglob("*"):
        relative = path.relative_to(folder)
        if any(part in IGNORED for part in relative.parts) or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise ValueError(f"Refusing symlink within skill: {path}")
        if path.is_file():
            result[relative.as_posix()] = path.read_bytes()
    return result


def atomically_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".skill-sync-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def deployment_lock(state_path):
    state_path.parent.mkdir(parents=True, exist_ok=True)
    lock = state_path.with_suffix(".lock")
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError(f"Deployment lock exists: {lock}; check whether its PID is active or the earlier deployment was interrupted")
    try:
        with os.fdopen(descriptor, "w") as stream:
            stream.write(str(os.getpid()))
        yield
    finally:
        lock.unlink()


def plan(target_home, state, manifest):
    if manifest.get("schema_version") != 1:
        raise ValueError("Unsupported manifest schema")
    plans = []
    used = set()
    for skill in manifest["skills"]:
        name = skill["name"]
        location = skill["windows_root"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name in used:
            raise ValueError("Invalid or duplicate personal skill name")
        used.add(name)
        if location not in {".agents/skills", ".codex/skills"}:
            raise ValueError("Target must be a user skill root")
        source = ROOT / ".agents" / "skills" / name
        if skill["source"] != f".agents/skills/{name}":
            raise ValueError("Source must be this repository's named personal skill")
        target = target_home / location / name
        # A link in a parent can redirect an otherwise innocent target.
        if any(part.is_symlink() for part in [target_home, target_home / location.split("/")[0], target.parent]):
            raise ValueError(f"Refusing linked destination root: {target}")
        expected = files_in(source)
        if "SKILL.md" not in expected:
            raise ValueError(f"Missing canonical SKILL.md: {name}")
        current = files_in(target)
        previous = state.get("skills", {}).get(name)
        expected_hashes = {path: digest(data) for path, data in expected.items()}
        current_hashes = {path: digest(data) for path, data in current.items()}
        conflicts = []
        if previous:
            if previous.get("target") != f"{location}/{name}":
                conflicts.append("destination changed since the previous deployment")
            owned = previous.get("files", {})
            for relative in owned:
                if relative in expected_hashes and relative not in current_hashes:
                    conflicts.append(f"installed file removed independently: {relative}")
            for relative, checksum in current_hashes.items():
                if relative not in owned:
                    conflicts.append(f"unmanaged file: {relative}")
                elif checksum != owned[relative] and checksum != expected_hashes.get(relative):
                    conflicts.append(f"installed file edited independently: {relative}")
        elif current and current_hashes != expected_hashes:
            conflicts.append("existing folder differs from the source and is not managed")
        write = [relative for relative in expected if current_hashes.get(relative) != expected_hashes[relative]]
        remove = [relative for relative in current if relative not in expected]
        plans.append({"name": name, "source": source, "target": target, "target_id": f"{location}/{name}", "expected": expected,
                      "hashes": expected_hashes, "observed": current_hashes,
                      "write": write, "remove": remove, "conflicts": conflicts})
    return plans


def read_state(path):
    if not path.exists():
        return {"schema_version": 1, "skills": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("skills"), dict):
        raise ValueError("Invalid deployment state")
    return data


def run(args):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    state_path = args.target_home / ".codex/public-dotfiles-skill-sync/state.json"
    if state_path.is_symlink() or state_path.parent.is_symlink():
        raise ValueError("Refusing symlinked deployment state")
    state = read_state(state_path)
    plans = plan(args.target_home, state, manifest)
    report = {"mode": "apply" if args.apply else "check", "skills": [
        {"name": item["name"], "target": str(item["target"]),
         "status": "conflict" if item["conflicts"] else ("differs" if item["write"] or item["remove"] else "matches"),
         "write": item["write"], "remove": item["remove"], "conflicts": item["conflicts"]} for item in plans]}
    if any(item["conflicts"] for item in plans):
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2
    if not args.apply:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1 if any(item["write"] or item["remove"] for item in plans) else 0
    with deployment_lock(state_path):
        # Re-read after acquiring the lock: another cooperating chat may have deployed.
        state = read_state(state_path)
        plans = plan(args.target_home, state, manifest)
        if any(item["conflicts"] for item in plans):
            raise ValueError("Installed files changed before deployment; re-run check")
        # Refuse all mutations if any observation has changed. No --force path.
        for item in plans:
            observed = {relative: digest(data) for relative, data in files_in(item["target"]).items()}
            if observed != item["observed"]:
                raise ValueError(f"Destination changed during planning: {item['name']}")
        for item in plans:
            for relative in item["write"]:
                atomically_write(item["target"] / relative, item["expected"][relative])
            for relative in item["remove"]:
                (item["target"] / relative).unlink()
            state["skills"][item["name"]] = {"target": item["target_id"], "files": item["hashes"]}
        # The state belongs outside Git and records exactly the delivered bytes.
        atomically_write(state_path, (json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode())
    report["mode"] = "applied"
    report["scope"] = "Manifest-owned user skills only. Provider packages, credentials and links are untouched."
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Deploy; otherwise only compare")
    parser.add_argument("--home", dest="target_home", type=Path,
                        required=True)
    args = parser.parse_args()
    args.target_home = args.target_home.expanduser().absolute()
    if args.target_home.resolve() == ROOT.parent or ROOT.parent in args.target_home.resolve().parents:
        parser.error("A private user home must be outside the public checkout")
    try:
        return run(args)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"status": "blocked", "error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
