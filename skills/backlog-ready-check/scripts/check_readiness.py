#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Applies the Definition of Ready / Flow Entry to the top of the backlog and groups items into mutually exclusive buckets.

Interface:
    python scripts/check_readiness.py backlog.json          # readable summary (stdout)
    python scripts/check_readiness.py backlog.json --json    # JSON only (stdout)
    python scripts/check_readiness.py --help

Input schema in references/dor.md. The substance assessment (useful description/AC) is
done by the model in the booleans; the script aggregates and applies the counting rules.
Supports `scrum` and `kanban` with `points` or `tshirt_size`/`size`.
In Kanban, estimate/size is optional by default (`require_estimate: false`).
Exit codes: 0 = OK; 2 = usage error or invalid input.
"""

import json
import sys


def require_schema(data, known, main_key, ctx):
    """Two-layer input guard.

    1. If no recognised key is present, the payload does not match the
       schema -> ValueError (exit 2). Catches the case where the layer that
       normalises the Jira data produces an object with the wrong keys.
    2. If the main collection is missing, it is likewise a schema error.
       If it is present but empty, that is a legitimate result, but it returns a warning:
       zero results can mean "nothing to report" or "the query found
       nothing", and the script cannot tell the two apart.
    """
    present = [k for k in known if k in data]
    if not present:
        raise ValueError(
            f"the payload does not match the {ctx} schema. "
            f"Keys received: {sorted(data.keys()) or 'none'}. "
            f"Expected (at least one): {sorted(known)}."
        )
    if main_key not in data:
        raise ValueError(
            f"missing required key '{main_key}' in the {ctx} input. "
            f"Keys received: {sorted(data.keys())}."
        )
    return []


def analyse(data):
    warnings = require_schema(
        data, {"board", "delivery_model", "estimate_mode", "team_estimate_ceiling",
               "size_ceiling", "epic_required", "require_estimate", "issues",
               "require_dependencies_identified", "require_testable"},
        "issues", "backlog-ready-check")
    delivery_model = str(data.get("delivery_model") or "scrum").lower()
    if delivery_model not in {"scrum", "kanban"}:
        delivery_model = "scrum"
        warnings.append("Unknown delivery model; assumed `scrum` for compatibility.")

    estimate_mode = data.get("estimate_mode")
    if estimate_mode is None:
        estimate_mode = "story_points" if delivery_model == "scrum" else "tshirt_size"
    estimate_mode = str(estimate_mode).lower()

    ceiling = data.get("team_estimate_ceiling")
    size_ceiling = data.get("size_ceiling")
    epic_required = data.get("epic_required", True)
    require_estimate = data.get("require_estimate")
    if require_estimate is None:
        require_estimate = delivery_model == "scrum"
    require_deps = data.get("require_dependencies_identified", False)
    require_testable = data.get("require_testable", False)
    issues = data.get("issues", []) or []
    if not issues:
        warnings.append(
            "Zero stories in the input. Confirm the board and the JQL for the top of the backlog / queue — an empty backlog "
            "is almost always a query that returned nothing, not a refined backlog."
        )

    ready, to_refine, to_split = [], [], []
    per_issue = []

    for i in issues:
        gaps = []
        if not i.get("has_description"):
            gaps.append("description")
        if not i.get("has_acceptance_criteria"):
            gaps.append("acceptance criteria")

        if require_estimate:
            if delivery_model == "kanban":
                if i.get("size") is None and i.get("tshirt_size") is None:
                    gaps.append("size / T-shirt size")
            elif i.get("points") is None:
                gaps.append("estimate")

        if epic_required and not i.get("has_epic"):
            gaps.append("epic")
        if require_deps and not i.get("has_dependencies_identified"):
            gaps.append("dependencies identified")
        if require_testable and not i.get("is_testable"):
            gaps.append("testable")

        oversize = False
        if delivery_model == "kanban":
            size_value = i.get("tshirt_size") or i.get("size")
            if size_value is not None and size_ceiling is not None:
                try:
                    size_order = {"xs": 1, "s": 2, "m": 3, "l": 4, "xl": 5, "xxl": 6}
                    size_value_clean = str(size_value).strip().lower()
                    size_ceiling_clean = str(size_ceiling).strip().lower()
                    if size_value_clean in size_order and size_ceiling_clean in size_order:
                        oversize = size_order[size_value_clean] > size_order[size_ceiling_clean]
                    else:
                        oversize = False
                except (TypeError, ValueError):
                    oversize = False
        else:
            if ceiling is not None and i.get("points") is not None:
                try:
                    oversize = float(i["points"]) > float(ceiling)
                except (TypeError, ValueError):
                    oversize = False

        notes = []
        if not epic_required and not i.get("has_epic"):
            notes.append("no epic (informational)")
        if not require_estimate:
            if delivery_model == "kanban" and i.get("size") is None and i.get("tshirt_size") is None:
                notes.append("no size (informational)")
            elif delivery_model == "scrum" and i.get("points") is None:
                notes.append("no estimate (informational)")
        if oversize:
            if delivery_model == "kanban":
                notes.append(f"size ({i.get('tshirt_size') or i.get('size')}) above the ceiling ({size_ceiling}) — split candidate in flow")
            else:
                notes.append(f"points ({i.get('points')}) above the ceiling ({ceiling}) — split candidate")

        entry = {
            "key": i.get("key"), "title": i.get("title"),
            "points": i.get("points"), "size": i.get("tshirt_size") or i.get("size"),
            "gaps": gaps, "notes": notes, "oversize": oversize,
            "delivery_model": delivery_model,
        }
        per_issue.append(entry)

        # each story in a single bucket. Gaps take precedence.
        if gaps:
            entry["bucket"] = "to_refine"
            to_refine.append(entry)
        elif oversize:
            entry["bucket"] = "to_split"
            to_split.append(entry)
        else:
            entry["bucket"] = "ready"
            ready.append(entry)

    to_refine.sort(key=lambda e: len(e["gaps"]))

    return {
        "board": data.get("board"),
        "config": {
            "delivery_model": delivery_model,
            "estimate_mode": estimate_mode,
            "epic_required": epic_required,
            "require_dependencies_identified": require_deps,
            "require_testable": require_testable,
            "require_estimate": require_estimate,
            "team_estimate_ceiling": ceiling,
            "size_ceiling": size_ceiling,
        },
        "summary": {"total": len(issues), "ready": len(ready),
                    "to_refine": len(to_refine), "to_split": len(to_split)},
        "ready": ready, "to_refine": to_refine, "to_split": to_split, "per_issue": per_issue,
        "warnings": warnings,
    }


def render(r):
    lines = []
    lines.append(f"BACKLOG / FLOW READINESS — {r.get('board') or '(board)'}")
    s = r["summary"]
    lines.append(f"Total: {s['total']}  ·  Ready: {s['ready']}  ·  To refine: {s['to_refine']}  ·  To split / prepare for flow: {s['to_split']}  (exclusive buckets: they sum to the total)")
    cfg = r["config"]
    lines.append(f"(mode: {cfg.get('delivery_model') or 'scrum'})")
    lines.append(f"(epic required: {'yes' if cfg['epic_required'] else 'no'})")
    lines.append(f"(estimate/size required: {'yes' if cfg.get('require_estimate') else 'no'})")
    lines.append("")

    if r.get("warnings"):
        lines.append("WARNINGS — read before reporting")
        for w in r["warnings"]:
            lines.append(f"  !! {w}")
        lines.append("")

    lines.append("READY FOR THE NEXT STEP")
    for e in r["ready"]:
        lines.append(f"- {e['key']} {e['title'] or ''}".rstrip())
    if not r["ready"]:
        lines.append("- (none)")
    lines.append("")

    lines.append("TO REFINE (fewest gaps first)")
    for e in r["to_refine"]:
        falta = ", ".join(e["gaps"]) if e["gaps"] else "—"
        extra = f"  [{'; '.join(e['notes'])}]" if e["notes"] else ""
        lines.append(f"- {e['key']} {e['title'] or ''} — missing: {falta}{extra}".rstrip())
    if not r["to_refine"]:
        lines.append("- (none)")
    lines.append("")

    lines.append("SPLIT CANDIDATES / Size out of fit (large, but no other gaps)")
    for e in r["to_split"]:
        lines.append(f"- {e['key']} {e['title'] or ''} — {'; '.join(e['notes'])}".rstrip())
    if not r["to_split"]:
        lines.append("- (none)")
    return "\n".join(lines)


USAGE = """check_readiness.py — backlog readiness scan (DoR).

Usage:
    python scripts/check_readiness.py backlog.json [--json]

Arguments:
    backlog.json   stories from the top of the backlog with the DoR booleans
                   (schema in references/dor.md)

Options:
    --json       write only the JSON to stdout
    -h, --help   show this help

Exit codes:
    0  success
    2  usage error or invalid input
"""


def main(argv):
    args = argv[1:]
    if "-h" in args or "--help" in args:
        print(USAGE.strip())
        return 0
    as_json = "--json" in args
    unknown = [a for a in args if a.startswith("-") and a != "--json"]
    if unknown:
        print(f"Error: unknown option: {unknown[0]}", file=sys.stderr)
        print("Expected: --json or --help. Run with --help for the interface.", file=sys.stderr)
        return 2
    positional = [a for a in args if not a.startswith("-")]
    if len(positional) != 1:
        print(f"Error: expected 1 input file, got {len(positional)}.", file=sys.stderr)
        print("Try: python scripts/check_readiness.py backlog.json   (--help for the interface)", file=sys.stderr)
        return 2

    path = positional[0]
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {path} (line {exc.lineno}, column {exc.colno}): {exc.msg}", file=sys.stderr)
        print("Expected: a JSON object matching the schema in the skill reference.", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print(f"Error: the input must be a JSON object, got {type(data).__name__}.", file=sys.stderr)
        return 2

    try:
        result = analyse(data)
    except ValueError as exc:
        print(f"Error: invalid input. {exc}", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
