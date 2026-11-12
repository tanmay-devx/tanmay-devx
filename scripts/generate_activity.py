#!/usr/bin/env python3
"""Generate an isometric 3D GitHub contribution activity SVG from live GitHub data."""

from __future__ import annotations

import datetime as dt
import html as html_lib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

USERNAME = os.environ.get("GITHUB_USERNAME", "tanmay-devx")
OUTPUT_PATH = Path(os.environ.get("ACTIVITY_SVG_PATH", "assets/activity.svg"))
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))

LEVEL_MAP = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}

BAR_STYLES = {
    1: {
        "left": "#0A331E",
        "right": "#072415",
        "top": "#0E4429",
        "top_stroke": "#165935",
        "filter": "",
    },
    2: {
        "left": "#005226",
        "right": "#003A19",
        "top": "#006D32",
        "top_stroke": "#0A833E",
        "filter": "",
    },
    3: {
        "left": "#1D8232",
        "right": "#156124",
        "top": "#26A641",
        "top_stroke": "#34BC52",
        "filter": ' filter="url(#subtleGlow)"',
    },
    4: {
        "left": "#2BB544",
        "right": "#208A33",
        "top": "#39D353",
        "top_stroke": "#4AE364",
        "filter": ' filter="url(#neonGlow)"',
    },
}


def fetch_via_graphql(username: str, token: str) -> tuple[list[list[dict]], int]:
    """Fetch 52-week contribution calendar via GitHub GraphQL API."""
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
                contributionLevel
              }
            }
          }
        }
      }
    }
    """
    payload = json.dumps({"query": query, "variables": {"login": username}}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "tanmay-devx-activity-sync",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")

    calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks: list[list[dict]] = []
    for week in calendar["weeks"]:
        days = []
        for d in week["contributionDays"]:
            days.append(
                {
                    "date": d["date"],
                    "count": int(d["contributionCount"]),
                    "level": LEVEL_MAP.get(d["contributionLevel"], 0),
                }
            )
        weeks.append(days)
    return weeks, int(calendar["totalContributions"])


def fetch_via_public_html(username: str) -> tuple[list[list[dict]], int]:
    """Fallback parser for GitHub's public contributions calendar HTML."""
    url = f"https://github.com/users/{username}/contributions"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; activity-sync/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode("utf-8")

    tip_counts: dict[str, int] = {}
    for target_id, tip_text in re.findall(
        r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>([^<]+)</tool-tip>', body
    ):
        clean_text = html_lib.unescape(tip_text).strip()
        if clean_text.startswith("No contributions"):
            tip_counts[target_id] = 0
        else:
            m = re.match(r"([\d,]+)\s+contribution", clean_text)
            tip_counts[target_id] = int(m.group(1).replace(",", "")) if m else 0

    cell_pattern = re.compile(r"<td\b([^>]*\bContributionCalendar-day\b[^>]*)>")
    entries: list[tuple[int, int, dict]] = []
    for attrs in cell_pattern.findall(body):
        date_m = re.search(r'\bdata-date="([^"]+)"', attrs)
        id_m = re.search(r'\bid="([^"]+)"', attrs)
        level_m = re.search(r'\bdata-level="(\d+)"', attrs)
        if not (date_m and id_m and level_m):
            continue
        cell_id = id_m.group(1)
        pos_m = re.search(r"-(\d+)-(\d+)$", cell_id)
        if pos_m:
            row_idx = int(pos_m.group(1))
            col_idx = int(pos_m.group(2))
        else:
            parsed_date = dt.date.fromisoformat(date_m.group(1))
            row_idx = (parsed_date.weekday() + 1) % 7
            col_idx = len(entries) // 7
        entries.append(
            (
                col_idx,
                row_idx,
                {
                    "date": date_m.group(1),
                    "count": tip_counts.get(cell_id, 0),
                    "level": int(level_m.group(1)),
                },
            )
        )

    if not entries:
        raise RuntimeError(f"Could not parse contribution cells from {url}")

    weeks_dict: dict[int, list[tuple[int, dict]]] = {}
    for col_idx, row_idx, day_info in entries:
        weeks_dict.setdefault(col_idx, []).append((row_idx, day_info))

    weeks: list[list[dict]] = []
    for col_idx in sorted(weeks_dict):
        col_days = [d for _, d in sorted(weeks_dict[col_idx], key=lambda item: item[0])]
        weeks.append(col_days)

    total_match = re.search(r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year", body)
    day_sum = sum(d["count"] for w in weeks for d in w)
    total = int(total_match.group(1).replace(",", "")) if total_match else day_sum
    return weeks, max(total, day_sum)


def compute_stats(weeks: list[list[dict]], total_reported: int) -> dict[str, int]:
    """Compute summary metrics across all calendar days."""
    days = sorted(
        (d for w in weeks for d in w),
        key=lambda d: d["date"],
    )
    longest_streak = 0
    current_streak = 0
    best_day = 0
    active_days = 0

    for d in days:
        count = d["count"]
        if count > 0:
            active_days += 1
            current_streak += 1
            if current_streak > longest_streak:
                longest_streak = current_streak
            if count > best_day:
                best_day = count
        else:
            current_streak = 0

    return {
        "total": total_reported,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "active_days": active_days,
    }


def iso_center(col: int, row: int) -> tuple[float, float]:
    """Project (week_col, day_row) onto the isometric SVG grid."""
    cx = 77.0 + col * 15.6 + row * 3.6
    cy = 335.0 + col * 0.45 + row * 7.0
    return cx, cy


def render_svg(weeks: list[list[dict]], stats: dict[str, int], synced_label: str) -> str:
    """Render the full 3D isometric contribution SVG string."""
    rx = 5.6
    ry = 3.2
    best_day = max(1, stats["best_day"])

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 480" width="100%" height="100%">',
        "<defs>",
        "  <style>",
        '    .serif-title { font-family: Georgia, "Times New Roman", serif; font-size: 29px; fill: #F0F6FC; font-weight: normal; }',
        '    .card-title { font-family: Georgia, "Times New Roman", serif; font-size: 25px; fill: #F0F6FC; font-weight: normal; }',
        '    .stat-number { font-family: Georgia, "Times New Roman", serif; font-size: 32px; fill: #F0F6FC; font-weight: normal; letter-spacing: -0.5px; }',
        "    .mono-tag { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11px; fill: #8B949E; font-weight: 500; }",
        "    .mono-lbl { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 9.5px; fill: #8B949E; font-weight: 600; letter-spacing: 1.2px; }",
        "    .mono-axis { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 9.5px; fill: #6E7681; font-weight: 500; }",
        "    @keyframes todayPulse {",
        "      0%, 100% { opacity: 0.7; }",
        "      50% { opacity: 1; }",
        "    }",
        "    .today-dot { animation: todayPulse 2.4s infinite ease-in-out; }",
        "  </style>",
        '  <filter id="neonGlow" x="-30%" y="-30%" width="160%" height="160%">',
        '    <feDropShadow dx="0" dy="0" stdDeviation="4.5" flood-color="#39D353" flood-opacity="0.55"/>',
        "  </filter>",
        '  <filter id="subtleGlow" x="-20%" y="-20%" width="140%" height="140%">',
        '    <feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="#39D353" flood-opacity="0.35"/>',
        "  </filter>",
        "</defs>",
        '<rect width="1040" height="480" fill="#0D1117" rx="12"/>',
        '<text x="45" y="38" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="14" font-weight="bold" fill="#39D353">06</text>',
        '<text x="75" y="38" class="serif-title">Activity</text>',
        '<line x1="45" y1="47" x2="95" y2="47" stroke="#39D353" stroke-width="2"/>',
        '<text x="995" y="38" class="mono-tag" text-anchor="end">auto-synced from GitHub</text>',
        '<rect x="45" y="60" width="950" height="405" rx="10" fill="#11161D" stroke="#30363D" stroke-width="1.2"/>',
        '<text x="75" y="96" class="card-title">The last 52 weeks</text>',
        f'<text x="965" y="92" class="mono-tag" text-anchor="end" fill="#6E7681">SYNCED {synced_label}</text>',
        '<text x="812" y="116" class="mono-tag" text-anchor="end">less</text>',
        '<rect x="820" y="108" width="9" height="9" rx="1.5" fill="#161B22" stroke="#21262D" stroke-width="0.5"/>',
        '<rect x="834" y="108" width="9" height="9" rx="1.5" fill="#0E4429" stroke="#165935" stroke-width="0.5"/>',
        '<rect x="848" y="108" width="9" height="9" rx="1.5" fill="#006D32" stroke="#0A833E" stroke-width="0.5"/>',
        '<rect x="862" y="108" width="9" height="9" rx="1.5" fill="#26A641" stroke="#34BC52" stroke-width="0.5"/>',
        '<rect x="876" y="108" width="9" height="9" rx="1.5" fill="#39D353" stroke="#4AE364" stroke-width="0.5"/>',
        '<text x="896" y="116" class="mono-tag">more</text>',
        f'<text x="75" y="136" class="stat-number">{stats["total"]:,}</text>',
        '<text x="75" y="152" class="mono-lbl">CONTRIBUTIONS</text>',
        f'<text x="220" y="136" class="stat-number">{stats["longest_streak"]}d</text>',
        '<text x="220" y="152" class="mono-lbl">LONGEST STREAK</text>',
        f'<text x="365" y="136" class="stat-number">{stats["best_day"]}</text>',
        '<text x="365" y="152" class="mono-lbl">BEST DAY</text>',
        f'<text x="510" y="136" class="stat-number">{stats["active_days"]}</text>',
        '<text x="510" y="152" class="mono-lbl">ACTIVE DAYS</text>',
        '<g opacity="0.6">',
    ]

    # Base grid cells
    for col_idx, week in enumerate(weeks):
        for row_idx in range(len(week)):
            cx, cy = iso_center(col_idx, row_idx)
            pts = (
                f"{cx:.1f},{cy - ry:.1f} "
                f"{cx + rx:.1f},{cy:.1f} "
                f"{cx:.1f},{cy + ry:.1f} "
                f"{cx - rx:.1f},{cy:.1f}"
            )
            lines.append(
                f'<polygon points="{pts}" fill="#141922" stroke="#1D2430" stroke-width="0.5"/>'
            )
    lines.append("</g>")

    # 3D bars in painter's order (sorted by base Y so front bars overlap rear bars)
    bars: list[tuple[float, int, int, dict]] = []
    for col_idx, week in enumerate(weeks):
        for row_idx, day in enumerate(week):
            if day["count"] > 0:
                _, cy = iso_center(col_idx, row_idx)
                bars.append((cy, col_idx, row_idx, day))

    bars.sort(key=lambda item: (item[0], item[1]))

    for _, col_idx, row_idx, day in bars:
        count = day["count"]
        level = day["level"]
        if level <= 0:
            ratio = count / best_day
            level = 4 if ratio > 0.7 else 3 if ratio > 0.4 else 2 if ratio > 0.15 else 1
        level = min(4, max(1, level))
        style = BAR_STYLES[level]

        cx, cy = iso_center(col_idx, row_idx)
        h = 6.0 + ((count / best_day) ** 0.78) * 86.0
        top_y = cy - h

        left_pts = (
            f"{cx - rx:.1f},{top_y:.1f} "
            f"{cx:.1f},{top_y + ry:.1f} "
            f"{cx:.1f},{cy + ry:.1f} "
            f"{cx - rx:.1f},{cy:.1f}"
        )
        right_pts = (
            f"{cx + rx:.1f},{top_y:.1f} "
            f"{cx:.1f},{top_y + ry:.1f} "
            f"{cx:.1f},{cy + ry:.1f} "
            f"{cx + rx:.1f},{cy:.1f}"
        )
        top_pts = (
            f"{cx:.1f},{top_y - ry:.1f} "
            f"{cx + rx:.1f},{top_y:.1f} "
            f"{cx:.1f},{top_y + ry:.1f} "
            f"{cx - rx:.1f},{top_y:.1f}"
        )

        lines.append(
            f'<polygon points="{left_pts}" fill="{style["left"]}" stroke="#0D1117" stroke-width="0.3"/>'
        )
        lines.append(
            f'<polygon points="{right_pts}" fill="{style["right"]}" stroke="#0D1117" stroke-width="0.3"/>'
        )
        lines.append(
            f'<polygon points="{top_pts}" fill="{style["top"]}" stroke="{style["top_stroke"]}" stroke-width="0.5"{style["filter"]}/>'
        )

    # Month axis labels positioned cleanly along bottom edge
    month_positions: list[tuple[int, str]] = []
    seen_month = None
    for col_idx, week in enumerate(weeks):
        if not week:
            continue
        first_day = dt.date.fromisoformat(week[0]["date"])
        month_key = (first_day.year, first_day.month)
        if month_key != seen_month:
            seen_month = month_key
            month_positions.append((col_idx, first_day.strftime("%b").upper()))

    filtered_months: list[tuple[int, str]] = []
    for col_idx, label in month_positions:
        if filtered_months and col_idx - filtered_months[-1][0] < 3:
            # Prefer newer month if too close at very start of grid
            if len(filtered_months) == 1 and filtered_months[0][0] == 0:
                filtered_months[0] = (col_idx, label)
            continue
        filtered_months.append((col_idx, label))

    for col_idx, label in filtered_months:
        cx, cy = iso_center(col_idx, 6)
        lines.append(
            f'<text x="{cx + 3.6:.1f}" y="{cy + 23.0:.1f}" class="mono-axis" text-anchor="middle">{label}</text>'
        )

    lines.extend(
        [
            '<text x="920" y="445" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="11" font-weight="bold" fill="#39D353" text-anchor="end">today</text>',
            '<circle cx="932" cy="441.5" r="4" fill="#39D353" class="today-dot" filter="url(#neonGlow)"/>',
            "</svg>",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    stats_token = os.environ.get("GH_STATS_TOKEN")
    fallback_token = os.environ.get("GITHUB_TOKEN")
    weeks: list[list[dict]]
    total_reported: int

    if stats_token:
        try:
            weeks, total_reported = fetch_via_graphql(USERNAME, stats_token)
        except Exception as exc:  # noqa: BLE001
            print(f"GraphQL fetch failed ({exc}); falling back to public calendar.", file=sys.stderr)
            weeks, total_reported = fetch_via_public_html(USERNAME)
    else:
        try:
            weeks, total_reported = fetch_via_public_html(USERNAME)
        except Exception as exc:  # noqa: BLE001
            if not fallback_token:
                raise
            print(f"Public HTML fetch failed ({exc}); falling back to GraphQL.", file=sys.stderr)
            weeks, total_reported = fetch_via_graphql(USERNAME, fallback_token)

    stats = compute_stats(weeks, total_reported)
    now_ist = dt.datetime.now(IST)
    synced_label = now_ist.strftime("%d %b %Y").upper()

    svg_content = render_svg(weeks, stats, synced_label)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(svg_content, encoding="utf-8")

    print(
        f"Generated {OUTPUT_PATH} for {USERNAME}: "
        f"total={stats['total']}, longest_streak={stats['longest_streak']}d, "
        f"best_day={stats['best_day']}, active_days={stats['active_days']}, "
        f"synced={synced_label}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
