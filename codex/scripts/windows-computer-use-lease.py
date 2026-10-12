#!/usr/bin/env python3
"""Cooperative, expiring host lease for official Windows Computer Use calls.

This coordinates cooperating chats only. It does not send UI input, call a
provider, change approvals, or stop any process. Use native Windows Python.
"""

import argparse
from contextlib import contextmanager
import json
import math
import msvcrt
import os
from pathlib import Path
import sys
import time
import uuid

WAIT_SECONDS = 90


def valid_expiry(value):
    if isinstance(value, bool):
        raise ValueError("Invalid expiry")
    expiry = float(value)
    if not math.isfinite(expiry):
        raise ValueError("Invalid expiry")
    return expiry


def current_state(raw, now):
    if not isinstance(raw, dict):
        raise ValueError("Lease state must be an object")
    state = {}
    current = raw.get("owner")
    if current is not None:
        current = str(uuid.UUID(current))
        expires = valid_expiry(raw["expiresAt"])
        if expires > now:
            state.update(owner=current, expiresAt=expires)
    queue = raw.get("waiters", [])
    if not isinstance(queue, list):
        raise ValueError("Waiters must be a list")
    waiters, seen = [], set()
    for waiter in queue:
        waiting_owner = str(uuid.UUID(waiter["owner"]))
        expiry = valid_expiry(waiter["expiresAt"])
        if waiting_owner in seen:
            raise ValueError("Duplicate waiter")
        seen.add(waiting_owner)
        if expiry > now and waiting_owner != state.get("owner"):
            waiters.append({"owner": waiting_owner, "expiresAt": expiry})
    if waiters:
        state["waiters"] = waiters
    if "pause" in raw:
        pause = raw["pause"]
        if not isinstance(pause, dict):
            raise ValueError("Pause must be an object")
        pause_owner = str(uuid.UUID(pause["owner"]))
        since = valid_expiry(pause["since"])
        # A human-work pause invalidates old leases and observations. It does
        # not expire: elapsed time is not permission to use the computer again.
        allowed = pause.get("allowedOwners", [])
        if not isinstance(allowed, list):
            raise ValueError("Allowed owners must be a list")
        allowed = list(dict.fromkeys(str(uuid.UUID(item)) for item in allowed))
        pause = {"owner": pause_owner, "since": since}
        if allowed:
            pause["allowedOwners"] = allowed
        # A task-specific human resume preserves the global stop and still
        # requires a fresh, exclusive lease. A new pause revokes exceptions.
        if state.get("owner") not in allowed:
            state.pop("owner", None)
            state.pop("expiresAt", None)
        state["pause"] = pause
        permitted_waiters = [item for item in state.get("waiters", []) if item["owner"] in allowed]
        if permitted_waiters:
            state["waiters"] = permitted_waiters
        else:
            state.pop("waiters", None)
    return state


def enqueue(state, owner, now):
    waiters = state.setdefault("waiters", [])
    for waiter in waiters:
        if waiter["owner"] == owner:
            waiter["expiresAt"] = now + WAIT_SECONDS
            return
    waiters.append({"owner": owner, "expiresAt": now + WAIT_SECONDS})


def remove_waiter(state, owner):
    waiters = [w for w in state.get("waiters", []) if w["owner"] != owner]
    if waiters:
        state["waiters"] = waiters
    else:
        state.pop("waiters", None)


@contextmanager
def state_lock(directory):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "lease.lock").open("a+b") as lock:
        lock.seek(0, 2)
        if lock.tell() == 0:
            lock.write(b"\0")
            lock.flush()
        lock.seek(0)
        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        try:
            yield
        finally:
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("acquire", "renew", "release", "cancel", "status", "pause", "resume", "resume-task"),
                        help="pause blocks grants until its owner explicitly resumes; cancel removes only the caller's waiting place")
    parser.add_argument("--owner", type=uuid.UUID, help="The calling chat's actual thread ID")
    parser.add_argument("--seconds", type=int, default=180)
    parser.add_argument("--namespace", default="windows-computer-use", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if sys.platform != "win32":
        parser.error("Use native Windows Python.")
    if args.action != "status" and args.owner is None:
        parser.error("--owner is required")
    if not 15 <= args.seconds <= 300:
        parser.error("--seconds must be between 15 and 300")
    if args.namespace != "windows-computer-use" and not args.namespace.startswith("test-"):
        parser.error("Only the host namespace or an isolated test namespace is allowed")
    if not all(c.isalnum() or c == "-" for c in args.namespace):
        parser.error("Invalid namespace")
    sys.stdout.reconfigure(encoding="utf-8")
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve(strict=True)
    directory = codex_home / ".tmp" / args.namespace
    state_path = directory / "lease.json"
    owner = str(args.owner) if args.owner is not None else None
    try:
        with state_lock(directory):
            now = time.time()
            raw = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
            state = current_state(raw, now)
            current = state.get("owner")
            live = current is not None
            pause = state.get("pause")
            result = {"action": args.action}
            if args.action == "status":
                result["held"] = live
            elif args.action == "pause":
                if pause is not None and pause["owner"] != owner:
                    result.update(ok=False, reason="paused by another chat on the user's instruction")
                else:
                    state = {"pause": {"owner": owner, "since": now}}
                    result["ok"] = True
            elif args.action == "resume-task":
                # Use only after the human explicitly resumes this exact task.
                # This is coordination, not provider approval or a UI bypass.
                if pause is not None:
                    allowed = pause.setdefault("allowedOwners", [])
                    if owner not in allowed:
                        allowed.append(owner)
                result["ok"] = True
            elif args.action == "resume":
                if pause is not None and pause["owner"] != owner:
                    result.update(ok=False, reason="only the pause owner can resume after the user's permission")
                else:
                    state.pop("pause", None)
                    result["ok"] = True
            elif pause is not None and owner not in pause.get("allowedOwners", []) and args.action in ("acquire", "renew"):
                result.update(ok=False, reason="paused on the user's instruction; continue work without Computer Use")
            elif args.action == "cancel":
                remove_waiter(state, owner)
                result["ok"] = True
            elif args.action == "release":
                if live and current != owner:
                    result.update(ok=False, reason="held by another chat")
                else:
                    state.pop("owner", None)
                    state.pop("expiresAt", None)
                    remove_waiter(state, owner)
                    result["ok"] = True
            elif args.action == "renew":
                if not live or current != owner:
                    result.update(ok=False, reason="caller has no live lease; acquire again before any Windows call")
                else:
                    state["expiresAt"] = now + args.seconds
                    result["ok"] = True
            else:
                waiters = state.get("waiters", [])
                if live and current != owner:
                    enqueue(state, owner, now)
                    result.update(ok=False, reason="held by another chat")
                elif not live and waiters and waiters[0]["owner"] != owner:
                    enqueue(state, owner, now)
                    result.update(ok=False, reason="another chat is first in queue")
                else:
                    remove_waiter(state, owner)
                    state.update(owner=owner, expiresAt=now + args.seconds)
                    result["ok"] = True
            waiters = state.get("waiters", [])
            position = next((i + 1 for i, w in enumerate(waiters) if w["owner"] == owner), None)
            result.update(owner=state.get("owner"), expiresAt=state.get("expiresAt"),
                          nextOwner=waiters[0]["owner"] if waiters else None,
                          queueLength=len(waiters))
            pause = state.get("pause")
            result.update(paused=pause is not None,
                          pauseOwner=pause["owner"] if pause else None,
                          pausedSince=pause["since"] if pause else None,
                          taskResumed=pause is not None and owner in pause.get("allowedOwners", []))
            if args.action == "acquire" and position is not None:
                result.update(queuePosition=position, queueExpiresAt=waiters[position - 1]["expiresAt"])
            if state != raw:
                temporary = directory / "lease.next"
                temporary.write_text(json.dumps(state) + "\n", encoding="utf-8")
                os.replace(temporary, state_path)
            print(json.dumps(result))
            return 0 if result.get("ok", True) else 2
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        # A busy state lock or corrupt state never grants an implicit lease.
        print(json.dumps({"ok": False, "reason": "lease state unavailable", "error": str(error)}))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
