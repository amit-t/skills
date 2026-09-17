#!/usr/bin/env python3
"""Stage 5 promote/reject (spec C6, D4): move a review-queue candidate into the
skill library or into rejection, updating registry.json.

- accept/edit: copy the rendered SKILL.md (status-patched per the C6 ladder) and
  the candidate.json into <skill-dir>/<name>/, upsert the registry entry, and
  move the queue folder to <queue>/promoted/<id>.
- reject: move the queue folder to <queue>/rejected/<id>, write reason.txt, and
  append a suppressed_task_types entry.

registry.json is created on first use with the D4 skeleton. CLI errors (missing
candidate id, missing queue folder) print one line to stderr and exit 1 -- never
a traceback.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s2s_common import load_config, now_iso, read_json, write_json

_REGISTRY_SKELETON = {
    "extractor_version": "1.0",
    "skills": {},
    "suppressed_task_types": [],
    "runs": [],
}

_STATUS_LINE_RE = re.compile(r"(?m)^(\s*status:\s*).+$")


class PromoteError(Exception):
    """Raised for CLI-facing failures: missing candidate id, missing queue folder,
    missing rendered files, unknown action. Caught by main() and printed as a
    single stderr line with exit code 1 (no traceback)."""


def _status_for(supporting_sessions, cfg):
    """C6 ladder: >=validated_min -> validated; >=provisional_min -> provisional;
    otherwise a reviewer accept still yields provisional (C6 row 2)."""
    recurrence_cfg = (cfg or {}).get("recurrence") or {}
    validated_min = recurrence_cfg.get("validated_min_sessions", 30)
    provisional_min = recurrence_cfg.get("provisional_min_sessions", 20)
    supporting_sessions = supporting_sessions or 0

    if supporting_sessions >= validated_min:
        return "validated"
    if supporting_sessions >= provisional_min:
        return "provisional"
    return "provisional"


def _patch_status_line(skill_md_text, status):
    """Patch the metadata `status:` frontmatter line in place to the ladder status."""
    patched, count = _STATUS_LINE_RE.subn(r"\g<1>%s" % status, skill_md_text, count=1)
    if count == 0:
        raise PromoteError("rendered SKILL.md has no 'status:' frontmatter line to patch")
    return patched


def _load_or_init_registry(registry_path):
    registry_path = Path(registry_path)
    if registry_path.is_file():
        return read_json(registry_path)
    return json.loads(json.dumps(_REGISTRY_SKELETON))


def _relative_to_registry(path, registry_path):
    registry_dir = Path(registry_path).resolve().parent
    return os.path.relpath(str(Path(path).resolve()), start=str(registry_dir))


def _require_queue_dir(queue_dir, candidate_id):
    src_dir = Path(queue_dir) / candidate_id
    if not src_dir.is_dir():
        raise PromoteError("no such candidate in queue: %s" % candidate_id)
    return src_dir


def _promote_accept_or_edit(candidate_id, action, queue_dir, skill_dir, registry_path, cfg):
    src_dir = _require_queue_dir(queue_dir, candidate_id)

    candidate_path = src_dir / "candidate.json"
    skill_md_path = src_dir / "SKILL.md"
    if not candidate_path.is_file():
        raise PromoteError("missing candidate.json in queue folder: %s" % src_dir)
    if not skill_md_path.is_file():
        raise PromoteError("missing rendered SKILL.md in queue folder: %s" % src_dir)

    candidate = read_json(candidate_path)
    name = candidate.get("name")
    if not name:
        raise PromoteError("candidate.json is missing 'name': %s" % candidate_path)

    evidence = candidate.get("evidence") or {}
    supporting_sessions = evidence.get("supporting_sessions", 0)
    status = _status_for(supporting_sessions, cfg)

    dest_dir = Path(skill_dir) / name
    dest_dir.mkdir(parents=True, exist_ok=True)

    skill_md_text = _patch_status_line(skill_md_path.read_text(encoding="utf-8"), status)
    dest_skill_md = dest_dir / "SKILL.md"
    dest_skill_md.write_text(skill_md_text, encoding="utf-8")
    shutil.copyfile(candidate_path, dest_dir / ".candidate.json")

    registry = _load_or_init_registry(registry_path)
    registry.setdefault("skills", {})
    existing = registry["skills"].get(name) or {}
    now = now_iso()
    session_ids = [s.get("session_id") for s in evidence.get("sessions") or []]

    registry["skills"][name] = {
        "path": _relative_to_registry(dest_skill_md, registry_path),
        "status": status,
        "version": candidate.get("version", "1.0"),
        "task_type": candidate.get("task_type", ""),
        "trigger_description": (candidate.get("trigger") or {}).get("description", ""),
        "supporting_sessions": session_ids,
        "created_at": existing.get("created_at", now),
        "updated_at": now,
        "superseded_by": None,
        "human_edited": True if action == "edit" else existing.get("human_edited", False),
    }
    write_json(registry_path, registry)

    promoted_dir = Path(queue_dir) / "promoted"
    promoted_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src_dir), str(promoted_dir / candidate_id))

    return {"ok": True, "status": status, "skill_dir": str(dest_dir)}


def _promote_reject(candidate_id, queue_dir, registry_path, reason, cfg):
    src_dir = _require_queue_dir(queue_dir, candidate_id)

    task_type = None
    candidate_path = src_dir / "candidate.json"
    if candidate_path.is_file():
        task_type = read_json(candidate_path).get("task_type")

    rejected_dir = Path(queue_dir) / "rejected"
    rejected_dir.mkdir(parents=True, exist_ok=True)
    dest_dir = rejected_dir / candidate_id
    shutil.move(str(src_dir), str(dest_dir))

    reason_text = reason or "unspecified"
    (dest_dir / "reason.txt").write_text(reason_text + "\n", encoding="utf-8")

    registry = _load_or_init_registry(registry_path)
    suppress_days = ((cfg or {}).get("review") or {}).get("reject_suppress_days", 30)
    until = (
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=suppress_days)
    ).isoformat()
    registry.setdefault("suppressed_task_types", []).append(
        {"task_type": task_type, "until": until, "reason": reason_text}
    )
    write_json(registry_path, registry)

    return {"ok": True, "rejected_dir": str(dest_dir)}


def cmd_promote(candidate_id, action, queue_dir, skill_dir, registry_path, reason, cfg):
    """Dispatch accept/edit/reject. Raises PromoteError for any CLI-facing failure."""
    if action in ("accept", "edit"):
        return _promote_accept_or_edit(candidate_id, action, queue_dir, skill_dir, registry_path, cfg)
    if action == "reject":
        return _promote_reject(candidate_id, queue_dir, registry_path, reason, cfg)
    raise PromoteError("unknown action: %s" % action)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Promote (accept/edit) or reject a review-queue candidate (Stage 5)."
    )
    parser.add_argument("candidate_id")
    parser.add_argument("action", choices=["accept", "edit", "reject"])
    parser.add_argument("--queue", required=True, help="review-queue directory")
    parser.add_argument("--skill-dir", required=True, help="destination skill library directory")
    parser.add_argument("--registry", required=True, help="path to registry.json")
    parser.add_argument("--reason", default=None, help="reject reason (default: 'unspecified')")
    parser.add_argument("--config", default=None, help="path to a user config.json")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    cfg = load_config(args.config)
    try:
        result = cmd_promote(
            args.candidate_id, args.action, args.queue, args.skill_dir, args.registry, args.reason, cfg,
        )
    except PromoteError as exc:
        print("promote: %s" % exc, file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
