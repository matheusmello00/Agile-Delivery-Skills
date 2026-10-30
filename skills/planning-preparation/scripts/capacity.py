#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Crosses capacity with velocity and builds a candidate scope for planning.

Interface:
    python scripts/capacity.py planning.json          # readable summary (stdout)
    python scripts/capacity.py planning.json --json    # JSON only (stdout)
    python scripts/capacity.py --help

Input schema in references/capacity.md. Historical velocity is the empirical basis;
availability (absences x relative focus x headcount) adjusts it. Without velocity, no
points range is invented. Exit codes: 0 = OK; 2 = usage error or invalid input.
"""

import json
import sys

# Valid range and typical range of the focus factor. Outside the valid range it is an
# input error; outside the typical range it is a warning, because the value is self-reported.
FOCUS_HARD_MIN, FOCUS_HARD_MAX = 0.1, 1.0
FOCUS_TYPICAL_MIN, FOCUS_TYPICAL_MAX = 0.5, 0.9


def require_schema(data, known, main_key, ctx):
    """Two-layer input guard.

    1. If no recognised key is present, the payload does not match the
       schema -> ValueError (exit 2). Catches the case where the layer that
       normalises Jira data produces an object with the wrong keys.
    2. If the main collection is absent, it is likewise a schema error.
       If it is present and empty, it is a legitimate result, but a warning is returned:
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
    require_schema(
        data, {"team", "sprint_name", "people", "sprint_days", "absences_person_days", "focus_factor",
               "baseline_focus", "people_in_prior_sprints", "prior_velocities", "ready_stories",
               "allow_extrapolation"}, "ready_stories", "planning-preparation")
    people = float(data.get("people") or 0)
    sprint_days = float(data.get("sprint_days") or 0)
    absences = float(data.get("absences_person_days") or 0)
    focus = float(data.get("focus_factor") if data.get("focus_factor") is not None else 0.7)
    baseline_focus = float(data.get("baseline_focus") if data.get("baseline_focus") is not None else 0.7)
    people_prior = data.get("people_in_prior_sprints")
    allow_extrapolation = bool(data.get("allow_extrapolation", False))

    prior = [float(v) for v in (data.get("prior_velocities") or []) if v is not None]
    velocity_avg = sum(prior) / len(prior) if prior else None

    notes = []
    warnings = []

    # The focus factor is the fraction of the team's time dedicated to the sprint: above
    # 1.0 it has no meaning. Without validation, an optimistic value would extrapolate the
    # range above any delivery already recorded.
    for label, value in (("focus_factor", focus), ("baseline_focus", baseline_focus)):
        if not (FOCUS_HARD_MIN <= value <= FOCUS_HARD_MAX):
            raise ValueError(
                f"{label} = {value} is outside the valid range [{FOCUS_HARD_MIN}, {FOCUS_HARD_MAX}]. "
                "The focus factor is the fraction of time dedicated to the sprint and cannot exceed 1.0. "
                f"Typical range: {FOCUS_TYPICAL_MIN}-{FOCUS_TYPICAL_MAX} (see references/capacity.md)."
            )
    if not (FOCUS_TYPICAL_MIN <= focus <= FOCUS_TYPICAL_MAX):
        warnings.append(
            f"Focus factor {focus} outside the typical range {FOCUS_TYPICAL_MIN}-{FOCUS_TYPICAL_MAX} "
            "declared in references/capacity.md — confirm with the team before using this range."
        )
    if people <= 0 or sprint_days <= 0:
        warnings.append(
            f"Capacity not provided (people={people:.0f}, days={sprint_days:.0f}) — the range "
            "below has no capacity basis. Fill it in before deciding scope."
        )

    gross_person_days = people * sprint_days
    net_person_days = max(gross_person_days - absences, 0)
    effective_person_days = net_person_days * focus  # diagnostic, not the origin of the range

    # --- availability ratios: absences, relative focus, headcount ---
    absence_ratio = (net_person_days / gross_person_days) if gross_person_days > 0 else None
    focus_ratio = (focus / baseline_focus) if baseline_focus > 0 else 1.0
    headcount_ratio = None
    if people_prior not in (None, 0):
        headcount_ratio = people / float(people_prior)
        if abs(headcount_ratio - 1.0) > 1e-9:
            notes.append(
                f"Headcount changed vs the velocity sprints ({people:.0f} now vs {float(people_prior):.0f}) "
                f"— range adjusted by {headcount_ratio:.2f}x."
            )
    if abs(focus_ratio - 1.0) > 1e-9:
        notes.append(f"Focus factor {focus} differs from the assumed one ({baseline_focus}) — adjustment of {focus_ratio:.2f}x.")

    availability = 1.0
    for r in (absence_ratio, focus_ratio, headcount_ratio):
        if r is not None:
            availability *= r

    # --- range: observed min-max x availability; without velocity none is invented ---
    rng = None
    method = None
    high_extrapolated = None
    if velocity_avg is not None and prior:
        lo_base, hi_base = min(prior), max(prior)
        low = round(lo_base * availability)
        high_raw = round(hi_base * availability)
        high = high_raw
        capped = False
        # Deliberate asymmetry: adjusting down is prudence, adjusting up is
        # a bet. The ceiling is only exceeded with explicit authorisation.
        if availability > 1.0 and high_raw > hi_base:
            if allow_extrapolation:
                high_extrapolated = True
                warnings.append(
                    f"The upper bound ({high_raw} pts) exceeds the best recorded delivery ({hi_base:g} pts). "
                    "Extrapolation authorised by allow_extrapolation — confirm with the team before committing."
                )
            else:
                high = round(hi_base)
                capped = True
                high_extrapolated = False
                warnings.append(
                    f"Upper bound capped at the best recorded delivery ({hi_base:g} pts): the availability "
                    f"adjustment ({availability * 100:.0f}%) pointed to {high_raw} pts. Adjusting down "
                    "is prudence, adjusting up is a bet. To extrapolate, pass allow_extrapolation: true."
                )
        if high < low:
            low, high = high, low
        rng = {"low": low, "high": high}
        method = ("observed min–max of the last %d sprints (%g–%g), adjusted by availability %.0f%%"
                  % (len(prior), lo_base, hi_base, availability * 100))
        if capped:
            method += " (upper bound capped at the historical maximum)"
    else:
        notes.append(
            "No velocity history — no points range is proposed (story points do not derive from days). "
            "Ask the team how much it delivered in recent sprints."
        )

    # --- candidate scope (break; respects rank) ---
    stories = data.get("ready_stories", []) or []
    if not stories:
        warnings.append(
            "Zero ready stories in the input. Confirm the board and the top-of-backlog JQL — without ready "
            "stories there is no scope to propose, and a seemingly empty backlog is almost always a query "
            "that returned nothing."
        )
    estimated = [s for s in stories if s.get("points") is not None]
    unestimated = [s for s in stories if s.get("points") is None]

    candidate, queue = [], []
    total = 0.0
    scope_cap = rng["high"] if rng is not None else None
    if rng is not None and prior and availability > 1.0:
        # The proposal does not materialise the extrapolation: it fills up to the history.
        scope_cap = min(rng["high"], round(max(prior)))
        if scope_cap < rng["high"]:
            notes.append(
                f"Candidate scope limited to {scope_cap} pts (historical maximum), although the range "
                f"goes up to {rng['high']} pts — the excess stayed in next in queue."
            )
    if rng is not None:
        stopped = False
        for s in estimated:
            pv = float(s["points"])
            if not stopped and total + pv <= scope_cap:
                candidate.append(s)
                total += pv
            else:
                stopped = True
                queue.append(s)
    else:
        # no range: there is no fitted scope; list by rank as queue
        queue = list(estimated)

    return {
        "team": data.get("team"),
        "sprint_name": data.get("sprint_name"),
        "capacity": {
            "people": people, "sprint_days": sprint_days, "absences_person_days": absences,
            "focus_factor": focus, "baseline_focus": baseline_focus,
            "effective_person_days_diagnostic": round(effective_person_days, 1),
            "absence_ratio": round(absence_ratio, 2) if absence_ratio is not None else None,
            "focus_ratio": round(focus_ratio, 2),
            "headcount_ratio": round(headcount_ratio, 2) if headcount_ratio is not None else None,
            "availability": round(availability, 2),
        },
        "velocity_avg": round(velocity_avg, 1) if velocity_avg is not None else None,
        "velocity_observed": {"min": min(prior), "max": max(prior)} if prior else None,
        "recommended_range_points": rng,
        "range_method": method,
        "high_extrapolated": high_extrapolated,
        "allow_extrapolation": allow_extrapolation,
        "scope_cap_points": scope_cap,
        "candidate_scope": {"stories": candidate, "total_points": round(total, 1)},
        "queue": queue,
        "unestimated": unestimated,
        "warnings": warnings,
        "notes": notes,
    }


def render(r):
    lines = []
    lines.append(f"PLANNING PREPARATION — {r.get('team') or '(team)'}  ·  {r.get('sprint_name') or ''}".rstrip())
    c = r["capacity"]
    lines.append("")
    lines.append("CAPACITY")
    lines.append(f"- People: {c['people']:.0f} · Days: {c['sprint_days']:.0f} · Absences: {c['absences_person_days']:.0f} p-d · Focus: {c['focus_factor']} (base {c['baseline_focus']})")
    lines.append(f"- Effective person-days (diagnostic): {c['effective_person_days_diagnostic']}")
    parts = [f"absences {int(c['absence_ratio']*100)}%" if c['absence_ratio'] is not None else None,
             f"focus {c['focus_ratio']}x" if abs(c['focus_ratio']-1.0) > 1e-9 else None,
             f"headcount {c['headcount_ratio']}x" if c['headcount_ratio'] is not None else None]
    parts = [p for p in parts if p]
    disp = f"  ({', '.join(parts)})" if parts else ""
    lines.append(f"- Availability vs normal sprint: {int(c['availability']*100)}%{disp}")
    if r["velocity_avg"] is not None:
        vo = r["velocity_observed"]
        lines.append(f"- Velocity: average {r['velocity_avg']} · observed {vo['min']:g}–{vo['max']:g} pts")
    else:
        lines.append("- Velocity: (no history)")
    if r["recommended_range_points"]:
        rr = r["recommended_range_points"]
        lines.append(f"- Reasonable commitment range: {rr['low']}–{rr['high']} pts")
        lines.append(f"  method: {r['range_method']}")
    else:
        lines.append("- Range: not proposed (velocity missing — see Notes)")
    lines.append("")

    cs = r["candidate_scope"]
    if r["recommended_range_points"]:
        lines.append(f"CANDIDATE SCOPE — total {cs['total_points']} pts")
        for s in cs["stories"]:
            lines.append(f"- {s.get('key')} {s.get('title') or ''} — {s.get('points')} pts".rstrip())
        if not cs["stories"]:
            lines.append("- (no story fit within the limit)")
        lines.append("")
        if r["queue"]:
            lines.append("NEXT IN QUEUE (by rank)")
            for s in r["queue"]:
                lines.append(f"- {s.get('key')} {s.get('title') or ''} — {s.get('points')} pts".rstrip())
            lines.append("")
    else:
        lines.append("READY STORIES (by rank — scope to be decided with the team)")
        for s in r["queue"]:
            lines.append(f"- {s.get('key')} {s.get('title') or ''} — {s.get('points')} pts".rstrip())
        lines.append("")

    if r["unestimated"]:
        lines.append("UNESTIMATED (not in scope until estimated)")
        for s in r["unestimated"]:
            lines.append(f"- {s.get('key')} {s.get('title') or ''}".rstrip())
        lines.append("")

    if r["warnings"]:
        lines.append("WARNINGS — read before committing")
        for w in r["warnings"]:
            lines.append(f"  !! {w}")
        lines.append("")

    if r["notes"]:
        lines.append("NOTES")
        for n in r["notes"]:
            lines.append(f"- {n}")
    return "\n".join(lines)


USAGE = """capacity.py — capacity, velocity and candidate scope.

Usage:
    python scripts/capacity.py planning.json [--json]

Arguments:
    planning.json   team capacity, prior velocities and ready stories
                    (schema in references/capacity.md)

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
        print(f"Error: expected 1 input file, received {len(positional)}.", file=sys.stderr)
        print("Try: python scripts/capacity.py planning.json   (--help for the interface)", file=sys.stderr)
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
        print(f"Error: the input must be a JSON object, received {type(data).__name__}.", file=sys.stderr)
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
