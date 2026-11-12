#!/usr/bin/env python3
"""Sync live LeetCode, Codeforces, GitHub Streak, and GitHub Stats SVG cards."""

from __future__ import annotations

import datetime as dt
import html as html_lib
import json
import math
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_activity import fetch_via_graphql, fetch_via_public_html  # noqa: E402

GH_USERNAME = os.environ.get("GITHUB_USERNAME", "tanmay-devx")
LC_USERNAME = os.environ.get("LEETCODE_USERNAME", "tanmay041")
CF_USERNAME = os.environ.get("CODEFORCES_USERNAME", "tanmay0412")
ASSETS_DIR = Path(os.environ.get("ASSETS_DIR", "assets"))
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))


def http_get_bytes(url: str, headers: dict[str, str] | None = None, timeout: int = 20) -> bytes:
    """Fetch raw bytes with a standard User-Agent header."""
    merged_headers = {"User-Agent": "tanmay-devx-profile-sync/1.0"}
    if headers:
        merged_headers.update(headers)
    req = urllib.request.Request(url, headers=merged_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def http_get_json(url: str, headers: dict[str, str] | None = None) -> dict | list:
    """Fetch and decode JSON from an HTTP endpoint."""
    return json.loads(http_get_bytes(url, headers=headers).decode("utf-8"))


def save_valid_svg(path: Path, content: str | bytes) -> None:
    """Validate XML well-formedness before writing an SVG asset."""
    raw = content.encode("utf-8") if isinstance(content, str) else content
    if b"@import" in raw or b"<script" in raw.lower():
        raise ValueError(f"Unsafe construct detected in SVG for {path}")
    ET.fromstring(raw)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def sync_leetcode_card() -> bool:
    """Download the live LeetCode dark SVG card."""
    url = f"https://leetcard.jacoblin.cool/{LC_USERNAME}?theme=dark&cache=60"
    try:
        raw = http_get_bytes(url)
        save_valid_svg(ASSETS_DIR / "card-leetcode.svg", raw)
        print(f"Synced card-leetcode.svg ({len(raw)} bytes)")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: LeetCode sync failed ({exc}); keeping existing card if present.", file=sys.stderr)
        return False


def fetch_codeforces_stats() -> dict:
    """Fetch live Codeforces user info, rating history, and solved stats."""
    info_resp = http_get_json(f"https://codeforces.com/api/user.info?handles={CF_USERNAME}")
    user = info_resp["result"][0]

    rating_resp = http_get_json(f"https://codeforces.com/api/user.rating?handle={CF_USERNAME}")
    rated_contests = len(rating_resp.get("result", []))

    status_resp = http_get_json(f"https://codeforces.com/api/user.status?handle={CF_USERNAME}")
    submissions = status_resp.get("result", [])
    solved = {
        (sub["problem"].get("contestId"), sub["problem"].get("index"))
        for sub in submissions
        if sub.get("verdict") == "OK" and "problem" in sub
    }

    return {
        "handle": user.get("handle", CF_USERNAME),
        "rank": user.get("rank", "Unrated").title(),
        "max_rank": user.get("maxRank", "Unrated").title(),
        "rating": int(user.get("rating", 0)),
        "max_rating": int(user.get("maxRating", 0)),
        "rated_contests": rated_contests,
        "solved": len(solved),
        "submissions": len(submissions),
        "friend_of": int(user.get("friendOfCount", 0)),
        "contribution": int(user.get("contribution", 0)),
    }


def render_codeforces_svg(cf: dict, synced_tag: str) -> str:
    """Render a clean dark Codeforces stats SVG matching GitHub dark mode."""
    rows = [
        ("Contest Rating:", str(cf["rating"]), "#A371F7"),
        ("Max Contest Rating:", str(cf["max_rating"]), "#A371F7"),
        ("Rated Contests:", str(cf["rated_contests"]), "#58A6FF"),
        ("Problems Solved:", str(cf["solved"]), "#39D353"),
        ("Submissions:", str(cf["submissions"]), "#79C0FF"),
        ("Friend of:", str(cf["friend_of"]), "#39D353"),
        ("Contribution:", str(cf["contribution"]), "#D2A8FF"),
    ]
    handle_esc = html_lib.escape(cf["handle"])
    subtitle_esc = html_lib.escape(f"{cf['rank']} (max: {cf['max_rank']})")

    row_svg = []
    start_y = 92
    for idx, (label, val, accent) in enumerate(rows):
        y = start_y + idx * 21
        row_svg.append(
            f'<circle cx="28" cy="{y - 4}" r="3.5" fill="{accent}"/>'
            f'<text x="42" y="{y}" class="cf-lbl">{html_lib.escape(label)}</text>'
            f'<text x="468" y="{y}" class="cf-val" text-anchor="end">{html_lib.escape(val)}</text>'
        )

    return "\n".join(
        [
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 495 240" width="100%" height="100%">',
            "<defs>",
            "  <style>",
            '    .cf-handle { font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 20px; font-weight: 700; fill: #58A6FF; }',
            '    .cf-sub { font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 13px; font-weight: 600; fill: #8B949E; }',
            '    .cf-lbl { font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 13.5px; font-weight: 600; fill: #3FB950; }',
            '    .cf-val { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13.5px; font-weight: 700; fill: #56D364; }',
            "    .cf-sync { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 9.5px; fill: #6E7681; }",
            "  </style>",
            "</defs>",
            '<rect width="495" height="240" rx="8" fill="#0D1117" stroke="#30363D" stroke-width="1"/>',
            '<rect x="24" y="25" width="4" height="11" rx="1" fill="#F2C94C"/>',
            '<rect x="30" y="19" width="4" height="17" rx="1" fill="#2F80ED"/>',
            '<rect x="36" y="27" width="4" height="9" rx="1" fill="#EB5757"/>',
            f'<text x="50" y="34" class="cf-handle">{handle_esc}</text>',
            f'<text x="468" y="31" class="cf-sync" text-anchor="end">SYNCED {html_lib.escape(synced_tag)}</text>',
            f'<text x="24" y="58" class="cf-sub">{subtitle_esc}</text>',
            '<line x1="24" y1="68" x2="471" y2="68" stroke="#21262D" stroke-width="1"/>',
            *row_svg,
            "</svg>",
            "",
        ]
    )


def format_date_range(start_iso: str, end_iso: str) -> str:
    """Format a compact streak date range like 'Oct 21 - Nov 12'."""
    s = dt.date.fromisoformat(start_iso)
    e = dt.date.fromisoformat(end_iso)
    if s == e:
        return s.strftime("%b %-d") if os.name != "nt" else s.strftime("%b %d")
    if s.year != e.year:
        return f"{s.strftime('%b %d, %Y')} - {e.strftime('%b %d, %Y')}"
    return f"{s.strftime('%b %d').replace(' 0', ' ')} - {e.strftime('%b %d').replace(' 0', ' ')}"


def collect_lifetime_github_data(token: str | None) -> tuple[dict, dict[str, int], str]:
    """Fetch GitHub user profile, multi-year daily contribution counts, and repo metrics."""
    gh_headers = {"Accept": "application/vnd.github+json"}
    if token:
        gh_headers["Authorization"] = f"Bearer {token}"

    user = http_get_json(f"https://api.github.com/users/{GH_USERNAME}", headers=gh_headers)
    created_date = dt.date.fromisoformat(user["created_at"][:10])
    today = dt.datetime.now(IST).date()

    repos: list[dict] = []
    page = 1
    while page <= 10:
        batch = http_get_json(
            f"https://api.github.com/users/{GH_USERNAME}/repos?per_page=100&page={page}",
            headers=gh_headers,
        )
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    total_stars = sum(int(r.get("stargazers_count", 0)) for r in repos)

    prs_count = 0
    issues_count = 0
    try:
        prs_count = int(
            http_get_json(
                f"https://api.github.com/search/issues?q=author:{GH_USERNAME}+type:pr",
                headers=gh_headers,
            ).get("total_count", 0)
        )
        issues_count = int(
            http_get_json(
                f"https://api.github.com/search/issues?q=author:{GH_USERNAME}+type:issue",
                headers=gh_headers,
            ).get("total_count", 0)
        )
    except Exception:  # noqa: BLE001
        pass

    daily_counts: dict[str, int] = {}
    yearly_totals: dict[int, int] = {}
    for year in range(created_date.year, today.year + 1):
        from_d = f"{year}-01-01"
        to_d = f"{year}-12-31"
        weeks, yr_total = fetch_via_public_html(GH_USERNAME, from_d, to_d)
        yearly_totals[year] = yr_total
        for week in weeks:
            for day in week:
                d_str = day["date"]
                daily_counts[d_str] = max(daily_counts.get(d_str, 0), int(day["count"]))

    stats_token = os.environ.get("GH_STATS_TOKEN")
    if stats_token:
        try:
            gql_weeks, _ = fetch_via_graphql(GH_USERNAME, stats_token)
            for week in gql_weeks:
                for day in week:
                    d_str = day["date"]
                    daily_counts[d_str] = max(daily_counts.get(d_str, 0), int(day["count"]))
        except Exception as exc:  # noqa: BLE001
            print(f"GraphQL merge skipped: {exc}", file=sys.stderr)

    commits_this_year = yearly_totals.get(today.year, 0)
    try:
        commit_search = http_get_json(
            f"https://api.github.com/search/commits?q=author:{GH_USERNAME}+author-date:>={today.year}-01-01",
            headers=gh_headers,
        )
        commits_this_year = max(int(commit_search.get("total_count", 0)), 0) or commits_this_year
    except Exception:  # noqa: BLE001
        pass

    github_summary = {
        "stars": total_stars,
        "commits_year": commits_this_year,
        "year": today.year,
        "prs": prs_count,
        "issues": issues_count,
        "public_repos": int(user.get("public_repos", len(repos))),
        "contributed_year": yearly_totals.get(today.year, 0),
        "lifetime_contributions": sum(daily_counts.values()),
        "created_label": created_date.strftime("%b %d, %Y").replace(" 0", " "),
    }
    return github_summary, daily_counts, today.isoformat()


def compute_streaks(daily_counts: dict[str, int], today_iso: str) -> dict:
    """Compute lifetime total, current active streak, and longest streak."""
    ordered = sorted((d, c) for d, c in daily_counts.items() if d <= today_iso)
    total = sum(c for _, c in ordered)

    longest = 0
    longest_start = ""
    longest_end = ""
    run = 0
    run_start = ""
    prev_date: dt.date | None = None

    for d_str, count in ordered:
        cur_date = dt.date.fromisoformat(d_str)
        if prev_date and (cur_date - prev_date).days > 1:
            run = 0
        if count > 0:
            if run == 0:
                run_start = d_str
            run += 1
            if run >= longest:
                longest = run
                longest_start = run_start
                longest_end = d_str
        else:
            run = 0
        prev_date = cur_date

    # Current streak: walk backwards from today (or yesterday if today has 0 so far)
    today_date = dt.date.fromisoformat(today_iso)
    check_date = today_date
    if daily_counts.get(today_iso, 0) == 0:
        yesterday = (today_date - dt.timedelta(days=1)).isoformat()
        if daily_counts.get(yesterday, 0) > 0:
            check_date = today_date - dt.timedelta(days=1)

    curr = 0
    curr_end = check_date.isoformat() if daily_counts.get(check_date.isoformat(), 0) > 0 else ""
    curr_start = curr_end
    while daily_counts.get(check_date.isoformat(), 0) > 0:
        curr += 1
        curr_start = check_date.isoformat()
        check_date -= dt.timedelta(days=1)

    return {
        "total": total,
        "current": curr,
        "current_range": format_date_range(curr_start, curr_end) if curr > 0 else "No active streak",
        "longest": longest,
        "longest_range": format_date_range(longest_start, longest_end) if longest > 0 else "-",
    }


def render_streak_svg(streaks: dict, created_label: str, synced_tag: str) -> str:
    """Render GitHub Streak SVG card in dark GitHub theme."""
    total_str = f"{streaks['total']:,}"
    curr_str = str(streaks["current"])
    long_str = str(streaks["longest"])

    return "\n".join(
        [
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 495 195" width="100%" height="100%">',
            "<defs>",
            "  <style>",
            '    .st-big { font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 28px; font-weight: 700; fill: #58A6FF; }',
            '    .st-curr { font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 28px; font-weight: 700; fill: #F0F6FC; }',
            '    .st-lbl { font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 13.5px; font-weight: 600; fill: #58A6FF; }',
            '    .st-sub { font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 11.5px; font-weight: 500; fill: #3FB950; }',
            "    .st-sync { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 9px; fill: #6E7681; }",
            "  </style>",
            "</defs>",
            '<rect width="495" height="195" rx="8" fill="#0D1117" stroke="#30363D" stroke-width="1"/>',
            f'<text x="480" y="18" class="st-sync" text-anchor="end">SYNCED {html_lib.escape(synced_tag)}</text>',
            '<line x1="165" y1="30" x2="165" y2="165" stroke="#21262D" stroke-width="1"/>',
            '<line x1="330" y1="30" x2="330" y2="165" stroke="#21262D" stroke-width="1"/>',
            f'<text x="82.5" y="88" class="st-big" text-anchor="middle">{html_lib.escape(total_str)}</text>',
            '<text x="82.5" y="122" class="st-lbl" text-anchor="middle">Total Contributions</text>',
            f'<text x="82.5" y="145" class="st-sub" text-anchor="middle">{html_lib.escape(created_label)} - Present</text>',
            '<circle cx="247.5" cy="74" r="37" fill="none" stroke="#58A6FF" stroke-width="5"/>',
            '<circle cx="247.5" cy="36" r="11" fill="#0D1117"/>',
            '<path d="M247.5 26 C249.5 30 253 32.5 253 36.5 C253 39.8 250.5 42.2 247.5 42.2 C244.5 42.2 242 39.8 242 36.5 C242 34.2 243.3 32 244.8 30.8 C244.6 32.5 245.5 33.4 246.3 33.4 C247.2 33.4 247.5 31.8 247.5 26 Z" fill="#FF9900"/>',
            f'<text x="247.5" y="84" class="st-curr" text-anchor="middle">{html_lib.escape(curr_str)}</text>',
            '<text x="247.5" y="135" class="st-lbl" text-anchor="middle">Current Streak</text>',
            f'<text x="247.5" y="157" class="st-sub" text-anchor="middle">{html_lib.escape(streaks["current_range"])}</text>',
            f'<text x="412.5" y="88" class="st-big" text-anchor="middle">{html_lib.escape(long_str)}</text>',
            '<text x="412.5" y="122" class="st-lbl" text-anchor="middle">Longest Streak</text>',
            f'<text x="412.5" y="145" class="st-sub" text-anchor="middle">{html_lib.escape(streaks["longest_range"])}</text>',
            "</svg>",
            "",
        ]
    )


def compute_rank(gh: dict) -> tuple[str, float]:
    """Compute a normalized GitHub rank label and ring progress (0..1)."""
    score = (
        min(gh["commits_year"], 1200) * 0.04
        + min(gh["contributed_year"], 1500) * 0.02
        + min(gh["public_repos"], 50) * 0.6
        + gh["prs"] * 1.5
        + gh["issues"] * 0.8
        + gh["stars"] * 2.0
    )
    if score >= 45:
        return "A+", 0.86
    if score >= 30:
        return "A", 0.78
    if score >= 20:
        return "B+", 0.68
    return "B", 0.56


def render_github_stats_svg(gh: dict, synced_tag: str) -> str:
    """Render My GitHub Statistics SVG card in dark GitHub theme."""
    rank_label, progress = compute_rank(gh)
    radius = 38
    circumference = 2 * math.pi * radius
    dash_offset = circumference * (1.0 - progress)

    rows = [
        ("Total Stars:", str(gh["stars"]), "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"),
        (f"Total Commits ({gh['year']}):", str(gh["commits_year"]), "M1.643 3.143.427 1.927A.25.25 0 0 0 .604 5.4h2.592a.25.25 0 0 0 .177-.33L2.157 3.143a.25.25 0 0 0-.514 0ZM8 2.5a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11ZM4 8a4 4 0 1 1 8 0 4 4 0 0 1-8 0Z"),
        (f"Contributions ({gh['year']}):", str(gh["contributed_year"]), "M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0Zm.75 4.75a.75.75 0 0 0-1.5 0v3.5c0 .199.079.39.22.53l2.25 2.25a.75.75 0 1 0 1.06-1.06l-2.03-2.03V4.75Z"),
        ("Total PRs &amp; Issues:", f"{gh['prs']} / {gh['issues']}", "M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Z"),
        ("Public Repositories:", str(gh["public_repos"]), "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8Z"),
    ]

    row_svg = []
    for idx, (lbl, val, path_d) in enumerate(rows):
        y = 66 + idx * 25
        row_svg.append(
            f'<g transform="translate(24, {y - 12}) scale(0.9)"><path d="{path_d}" fill="#58A6FF"/></g>'
            f'<text x="46" y="{y}" class="gh-lbl">{lbl}</text>'
            f'<text x="285" y="{y}" class="gh-val" text-anchor="end">{html_lib.escape(val)}</text>'
        )

    return "\n".join(
        [
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 495 195" width="100%" height="100%">',
            "<defs>",
            "  <style>",
            '    .gh-title { font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 17px; font-weight: 700; fill: #58A6FF; }',
            '    .gh-lbl { font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 13px; font-weight: 600; fill: #C9D1D9; }',
            '    .gh-val { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; font-weight: 700; fill: #F0F6FC; }',
            '    .gh-rank { font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 24px; font-weight: 800; fill: #F0F6FC; }',
            "    .gh-sync { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 9px; fill: #6E7681; }",
            "  </style>",
            "</defs>",
            '<rect width="495" height="195" rx="8" fill="#0D1117" stroke="#30363D" stroke-width="1"/>',
            '<text x="24" y="34" class="gh-title">My GitHub Statistics</text>',
            f'<text x="475" y="24" class="gh-sync" text-anchor="end">SYNCED {html_lib.escape(synced_tag)}</text>',
            *row_svg,
            '<circle cx="400" cy="108" r="38" fill="none" stroke="#1F2937" stroke-width="7"/>',
            f'<circle cx="400" cy="108" r="38" fill="none" stroke="#58A6FF" stroke-width="7" stroke-linecap="round" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{dash_offset:.2f}" transform="rotate(-90 400 108)"/>',
            f'<text x="400" y="116" class="gh-rank" text-anchor="middle">{html_lib.escape(rank_label)}</text>',
            "</svg>",
            "",
        ]
    )


def main() -> int:
    synced_tag = dt.datetime.now(IST).strftime("%d %b %Y").upper()

    # 1. LeetCode
    sync_leetcode_card()

    # 2. Codeforces
    try:
        cf_stats = fetch_codeforces_stats()
        cf_svg = render_codeforces_svg(cf_stats, synced_tag)
        save_valid_svg(ASSETS_DIR / "card-codeforces.svg", cf_svg)
        print(
            f"Synced card-codeforces.svg: rating={cf_stats['rating']}, "
            f"solved={cf_stats['solved']}, submissions={cf_stats['submissions']}"
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: Codeforces sync failed ({exc}); keeping existing card if present.", file=sys.stderr)

    # 3 & 4. GitHub Streak + GitHub Stats
    token = os.environ.get("GH_STATS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    try:
        gh_summary, daily_counts, today_iso = collect_lifetime_github_data(token)
        streaks = compute_streaks(daily_counts, today_iso)

        streak_svg = render_streak_svg(streaks, gh_summary["created_label"], synced_tag)
        save_valid_svg(ASSETS_DIR / "card-streak.svg", streak_svg)

        gh_svg = render_github_stats_svg(gh_summary, synced_tag)
        save_valid_svg(ASSETS_DIR / "card-github.svg", gh_svg)

        print(
            f"Synced card-streak.svg & card-github.svg: total={streaks['total']}, "
            f"current_streak={streaks['current']}d ({streaks['current_range']}), "
            f"longest_streak={streaks['longest']}d, commits_{gh_summary['year']}={gh_summary['commits_year']}"
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: GitHub stats sync failed ({exc}); keeping existing cards if present.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
