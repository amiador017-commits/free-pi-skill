#!/usr/bin/env python3
"""free-pi preflight picker: the only sanctioned row generator for this skill.

Discovery is read-only. It uses the user's own local free-pi token and never
prints it. Every model of a tier becomes exactly one row -- the script asserts
rows == models and exits non-zero if they disagree, so a truncated tier can
never be rendered.

Usage:
  pi_picker.py --json                          # all three tiers as JSON
  pi_picker.py --tier defense --widget [--out FILE]
  pi_picker.py --tier defense --table          # markdown table, no-preview hosts
  pi_picker.py --tier defense --shortcuts      # <=4 clarify choice strings

Exit codes: 0 ok, 2 discovery/auth/offline failure (fall back to the /model
probe described in SKILL.md), 3 row-count assertion failure.
"""

import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request

TIERS = ("free_unlimited", "free_at_capacity", "defense")
DEFENSE_CUTOFF = 20.0
PREFS_PATH = os.path.expanduser("~/.free-pi/agent/hermes-prefs.json")


def discover():
    cred_path = os.path.expanduser("~/.free-pi/agent/credentials.json")
    with open(cred_path, encoding="utf-8") as fh:
        token = json.load(fh)["token"]
    base = os.environ.get("FREEPI_BASE_URL", "https://api.freepi.ai").rstrip("/")
    req = urllib.request.Request(
        base + "/client-version", headers={"Authorization": "Bearer " + token}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def classify(models):
    tiers = {t: [] for t in TIERS}
    for m in models:
        name = m.get("name", "")
        hit = re.search(r"~([\d.]+)x usage", name)
        usage = float(hit.group(1)) if hit else None
        label = name.split("\u00b7")[0].strip()
        cost = name.split("\u00b7", 1)[1].strip() if "\u00b7" in name else ""
        if "Free Unlimited" in name:
            tier, credits = "free_unlimited", "0 credit"
        elif m.get("section") == "defense" or (usage is not None and usage >= DEFENSE_CUTOFF):
            tier, credits = "defense", cost
        else:
            tier, credits = "free_at_capacity", cost
        tiers[tier].append({"id": m["id"], "name": label, "usage": usage, "cost": credits})
    for tier in TIERS:
        rows = tiers[tier]
        if tier == "free_unlimited":
            rows.sort(key=lambda r: r["id"])
        else:
            rows.sort(key=lambda r: (r["usage"] is None, r["usage"] or 0.0, r["id"]))
    return tiers


def usage_label(value):
    return "free" if value is None else f"{value:g}x"


def last_pick(tier):
    try:
        with open(PREFS_PATH, encoding="utf-8") as fh:
            prefs = json.load(fh)
    except (OSError, ValueError):
        return None
    return prefs.get("model") if prefs.get("tier") == tier else None


def table_rows(rows):
    for i, r in enumerate(rows, 1):
        yield i, r["name"], r["id"], usage_label(r["usage"]), r["cost"]


def emit_table(rows, tier):
    lines = [f"{tier} \u2014 {len(rows)} models", "",
             "| # | Model | Exact id | Usage | Cost |", "|---|---|---|---|---|"]
    for num, name, mid, usage, cost in table_rows(rows):
        lines.append(f"| {num} | {name} | `{mid}` | {usage} | {cost} |")
    lines.append("")
    lines.append("Answer with the row number or the exact id.")
    return "\n".join(lines)


def emit_widget(rows, tier):
    max_usage = max([r["usage"] or 0.0 for r in rows] + [1.0])
    cells = []
    for num, name, mid, usage, cost in table_rows(rows):
        raw = next((r["usage"] for r in rows if r["id"] == mid), None)
        pct = 0 if raw is None else min(100.0, raw / max_usage * 100.0)
        cells.append(
            '<li><button data-hermes-send="prompt" '
            f'data-hermes-send-value="free-pi model: {html.escape(mid)}">'
            f'<span class="n">{num}</span>'
            f'<span class="nm">{html.escape(name)}</span>'
            f'<span class="id"><code>{html.escape(mid)}</code></span>'
            f'<span class="bar"><i style="width:{pct:.0f}%"></i></span>'
            f'<span class="u">{usage}</span>'
            f'<span class="c">{html.escape(cost)}</span></button></li>'
        )
    body = "".join(cells)
    return (
        '<!doctype html><meta charset="utf-8">\n'
        "<style>\n"
        "  body{font:14px/1.45 var(--app-font, system-ui);color:var(--foreground)}\n"
        "  .hd{display:flex;align-items:baseline;gap:8px;margin:2px 0 10px}\n"
        "  .hd b{font-size:15px}\n"
        "  .hd span{color:var(--muted-foreground);font-size:12.5px}\n"
        "  ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px}\n"
        "  button{width:100%;display:grid;gap:10px;align-items:center;text-align:left;\n"
        "    grid-template-columns:22px minmax(140px,1.2fr) minmax(140px,1.3fr) 70px 46px minmax(84px,1fr);\n"
        "    background:var(--card);border:1px solid var(--border);border-radius:8px;\n"
        "    padding:8px 10px;color:inherit;font:inherit;cursor:pointer}\n"
        "  button:hover{border-color:var(--foreground)}\n"
        "  .n,.id code,.c,.hd span{color:var(--muted-foreground)}\n"
        "  .id code,.c{font-size:12px}\n"
        "  .bar{height:5px;border-radius:3px;background:var(--accent);opacity:.35;overflow:hidden}\n"
        "  .bar i{display:block;height:100%;background:var(--foreground);opacity:.9}\n"
        "  .u{text-align:right;font-variant-numeric:tabular-nums}\n"
        "  .ft{margin:10px 0 0;color:var(--muted-foreground);font-size:12.5px}\n"
        "</style>\n"
        f'<div class="hd"><b>{html.escape(tier)}</b>'
        f"<span>{len(rows)} models \u00b7 usage ascending \u00b7 click a row to pick</span></div>\n"
        f"<ul>{body}</ul>\n"
        '<p class="ft">Type a row number or the exact id in chat; both work.</p>\n'
    )


def emit_shortcuts(rows, tier, limit=4):
    picked = last_pick(tier)
    ordered = [r for r in rows if r["id"] == picked] + [r for r in rows if r["id"] != picked]
    out = []
    for r in ordered[:limit]:
        suffix = " (Recommended)" if r["id"] == picked or (picked is None and r is ordered[0]) else ""
        out.append(f'{r["name"]} ({r["id"]}) - {r["cost"]}{suffix}')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", choices=TIERS)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--json", action="store_true")
    mode.add_argument("--widget", action="store_true")
    mode.add_argument("--table", action="store_true")
    mode.add_argument("--shortcuts", action="store_true")
    ap.add_argument("--out", help="widget output path (default ./free-pi-picker.html)")
    args = ap.parse_args()

    try:
        tiers = classify(discover()["models"])
    except (urllib.error.URLError, OSError, ValueError, KeyError) as exc:
        print(f"discovery failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("fall back to the /model probe PTY described in SKILL.md; never guess from memory.",
              file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(tiers, ensure_ascii=False, indent=2))
        return 0

    if not args.tier:
        print("--tier is required for --widget/--table/--shortcuts", file=sys.stderr)
        return 2

    rows = tiers[args.tier]
    if args.shortcuts:
        print(json.dumps(emit_shortcuts(rows, args.tier), ensure_ascii=False, indent=2))
        return 0

    payload = emit_widget(rows, args.tier) if args.widget else emit_table(rows, args.tier)

    emitted = payload.count('data-hermes-send="prompt"') if args.widget else len(
        re.findall(r"^\| \d+ \|", payload, re.M))
    if emitted != len(rows):
        print(f"ASSERTION FAILED: rows_emitted={emitted} models={len(rows)}", file=sys.stderr)
        return 3

    if args.widget:
        dest = os.path.abspath(args.out or "free-pi-picker.html")
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(payload)
        print(f"widget={dest} rows={emitted} models={len(rows)} ok=true")
    else:
        print(payload)
        print(f"# rows={emitted} models={len(rows)} ok=true", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
