#!/usr/bin/env python3
"""CLI: locate and load sessions for one host adapter, writing a sessions+errors JSON file.

Per-file/per-ref load failures are collected into the "errors" list rather than
aborting the run. An unknown --host exits 2 with a JSON error naming the hosts
that are actually available (never a traceback).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from adapters import ADAPTERS
from s2s_common import load_config, write_json


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Load sessions via a host adapter.")
    parser.add_argument("--host", required=True, help="adapter host name, e.g. generic")
    parser.add_argument("--config", default=None, help="path to a user config.json")
    parser.add_argument("--paths", nargs="*", default=None, help="glob patterns of session files")
    parser.add_argument("--lookback-days", type=int, default=None)
    parser.add_argument("--max", type=int, default=None, help="max sessions to load")
    parser.add_argument("--out", required=True, help="output JSON path")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if args.host not in ADAPTERS:
        error = {
            "error": "unknown_host",
            "host": args.host,
            "available_hosts": sorted(ADAPTERS.keys()),
        }
        print(json.dumps(error), file=sys.stderr)
        return 2

    config = load_config(args.config)
    if args.paths is not None:
        config["paths"] = args.paths
    if args.lookback_days is not None:
        config.setdefault("filter", {})["lookback_days"] = args.lookback_days
    if args.max is not None:
        config.setdefault("filter", {})["max_sessions_per_run"] = args.max

    adapter = ADAPTERS[args.host]()

    sessions = []
    errors = []
    try:
        refs = adapter.locate(config)
    except Exception as exc:
        refs = []
        errors.append({"ref": None, "error": str(exc)})

    if args.max is not None:
        refs = refs[: args.max]

    for ref in refs:
        try:
            session = adapter.load(ref, config)
            sessions.append(session.to_dict())
        except Exception as exc:
            errors.append({"ref": str(ref), "error": str(exc)})

    write_json(args.out, {"sessions": sessions, "errors": errors})
    return 0


if __name__ == "__main__":
    sys.exit(main())
