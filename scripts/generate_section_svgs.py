#!/usr/bin/env python3
"""Generate cohesive dark-theme animated SVGs for Executive Summary, Headers, and Credentials."""

from __future__ import annotations

import html
import xml.etree.ElementTree as ET
import xml.parsers.expat as expat
from pathlib import Path

ASSETS_DIR = Path("assets")


def write_svg(filename: str, content: str) -> None:
    raw = content.encode("utf-8")
    assert b"@import" not in raw and b"<script" not in raw.lower()
    ET.fromstring(raw)
    expat.ParserCreate().Parse(raw, True)
    out = ASSETS_DIR / filename
    out.write_bytes(raw)
    print(f"Generated {out} ({len(raw)} bytes)")


def render_section_header(num: str, title: str, right_tag: str, delay_offset: str = "0s") -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 62" width="100%" height="100%">
<defs>
  <style>
    .num {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 14px; font-weight: 700; fill: #39D353; }}
    .title {{ font-family: Georgia, "Times New Roman", serif; font-size: 28px; fill: #F0F6FC; font-weight: normal; letter-spacing: -0.2px; }}
    .tag {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11px; fill: #8B949E; font-weight: 500; }}
    @keyframes beamSweep {{
      0%   {{ transform: translateX(-180px); opacity: 0; }}
      15%  {{ opacity: 1; }}
      85%  {{ opacity: 1; }}
      100% {{ transform: translateX(1040px); opacity: 0; }}
    }}
    .beam {{ animation: beamSweep 5.5s infinite cubic-bezier(0.4, 0, 0.2, 1); animation-delay: {delay_offset}; }}
  </style>
  <linearGradient id="beamGrad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#39D353" stop-opacity="0"/>
    <stop offset="50%" stop-color="#39D353" stop-opacity="0.95"/>
    <stop offset="100%" stop-color="#58A6FF" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="ruleClip">
    <rect x="0" y="53" width="1040" height="2"/>
  </clipPath>
</defs>
<text x="6" y="38" class="num">{html.escape(num)}</text>
<text x="36" y="38" class="title">{html.escape(title)}</text>
<text x="1034" y="37" class="tag" text-anchor="end">{html.escape(right_tag)}</text>
<line x1="6" y1="54" x2="1034" y2="54" stroke="#21262D" stroke-width="1.5"/>
<line x1="6" y1="54" x2="62" y2="54" stroke="#39D353" stroke-width="2"/>
<g clip-path="url(#ruleClip)">
  <rect x="0" y="53" width="180" height="2" fill="url(#beamGrad)" class="beam"/>
</g>
</svg>
"""


def render_executive_summary() -> str:
    pillars = [
        (
            "01",
            "BACKEND & DISTRIBUTED SYSTEMS",
            "Decoupled, event-driven service architectures",
            "Node.js · NestJS · RabbitMQ · PostgreSQL",
            24,
            78,
            "-0.4s",
        ),
        (
            "02",
            "PROCESS SANDBOXING & SECURITY",
            "Isolated execution of untrusted workloads",
            "Rootless Podman · Dropped Caps · Linux cgroups",
            528,
            78,
            "-6.4s",
        ),
        (
            "03",
            "DEFENSIVE ENGINEERING",
            "Fault tolerance beyond superficial abstractions",
            "Manual ACKs · Circuit Breakers · Bounded Streams",
            24,
            196,
            "-4.4s",
        ),
        (
            "04",
            "CLOUD & INFRASTRUCTURE",
            "Reproducible, declarative production environments",
            "AWS (EC2, S3, IAM, VPC) · Terraform · Docker",
            528,
            196,
            "-2.4s",
        ),
    ]

    base_cards = []
    active_cards = []
    for num, label, desc, stack, x, y, delay in pillars:
        base_cards.append(
            f"""<g>
  <rect x="{x}" y="{y}" width="488" height="102" rx="8" fill="#161B22" stroke="#30363D" stroke-width="1"/>
  <rect x="{x + 14}" y="{y + 20}" width="3" height="62" rx="1.5" fill="#26A641"/>
  <text x="{x + 28}" y="{y + 31}" class="card-tag" fill="#39D353">{num}&#160;&#160;{html.escape(label)}</text>
  <text x="{x + 28}" y="{y + 55}" class="card-desc" fill="#C9D1D9">{html.escape(desc)}</text>
  <text x="{x + 28}" y="{y + 78}" class="card-stack" fill="#8B949E">{html.escape(stack)}</text>
</g>"""
        )
        active_cards.append(
            f"""<g class="pillar-active" style="animation-delay: {delay};">
  <rect x="{x}" y="{y}" width="488" height="102" rx="8" fill="#0D2218" stroke="#39D353" stroke-width="1.5" filter="url(#execGlow)"/>
  <rect x="{x + 14}" y="{y + 20}" width="3" height="62" rx="1.5" fill="#39D353"/>
  <text x="{x + 28}" y="{y + 31}" class="card-tag" fill="#56D364">{num}&#160;&#160;{html.escape(label)}</text>
  <text x="{x + 28}" y="{y + 55}" class="card-desc" fill="#F0F6FC">{html.escape(desc)}</text>
  <text x="{x + 28}" y="{y + 78}" class="card-stack" fill="#A5D6A7">{html.escape(stack)}</text>
  <circle cx="{x + 468}" cy="{y + 24}" r="3.5" fill="#39D353"/>
</g>"""
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 322" width="100%" height="100%">
<defs>
  <style>
    .num {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 14px; font-weight: 700; fill: #39D353; }}
    .title {{ font-family: Georgia, "Times New Roman", serif; font-size: 28px; fill: #F0F6FC; font-weight: normal; letter-spacing: -0.2px; }}
    .tag {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11px; fill: #8B949E; font-weight: 500; }}
    .card-tag {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10.5px; font-weight: 700; letter-spacing: 1.3px; }}
    .card-desc {{ font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 14px; font-weight: 600; }}
    .card-stack {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11.5px; font-weight: 500; }}
    @keyframes pillarFocus {{
      0%   {{ opacity: 0; }}
      5%   {{ opacity: 1; }}
      22%  {{ opacity: 1; }}
      30%  {{ opacity: 0; }}
      100% {{ opacity: 0; }}
    }}
    @keyframes beamSweep {{
      0%   {{ transform: translateX(-180px); opacity: 0; }}
      20%  {{ opacity: 0.9; }}
      80%  {{ opacity: 0.9; }}
      100% {{ transform: translateX(1040px); opacity: 0; }}
    }}
    .pillar-active {{ animation: pillarFocus 8s infinite ease-in-out; }}
    .beam {{ animation: beamSweep 6s infinite ease-in-out; }}
  </style>
  <filter id="execGlow" x="-8%" y="-15%" width="116%" height="130%">
    <feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#39D353" flood-opacity="0.3"/>
  </filter>
  <linearGradient id="execBeam" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#39D353" stop-opacity="0"/>
    <stop offset="50%" stop-color="#39D353" stop-opacity="0.9"/>
    <stop offset="100%" stop-color="#58A6FF" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="execClip">
    <rect x="24" y="55" width="992" height="2"/>
  </clipPath>
</defs>
<rect width="1040" height="322" rx="12" fill="#0D1117" stroke="#21262D" stroke-width="1"/>
<text x="24" y="40" class="num">01</text>
<text x="54" y="40" class="title">Executive Summary</text>
<text x="1016" y="39" class="tag" text-anchor="end">core engineering focus</text>
<line x1="24" y1="56" x2="1016" y2="56" stroke="#21262D" stroke-width="1.2"/>
<line x1="24" y1="56" x2="80" y2="56" stroke="#39D353" stroke-width="2"/>
<g clip-path="url(#execClip)">
  <rect x="0" y="55" width="180" height="2" fill="url(#execBeam)" class="beam"/>
</g>
{"".join(base_cards)}
{"".join(active_cards)}
</svg>
"""


def render_credential_card(
    badge_text: str,
    title: str,
    subtitle: str,
    cta_text: str | None,
    accent: str,
    icon_paths: str,
    delay: str,
    wide: bool = False,
) -> str:
    w = 1040 if wide else 504
    h = 132 if wide else 156
    title_y = 66 if wide else 70
    sub_y = 92 if wide else 96
    cta_y = 114 if wide else 134

    if cta_text:
        cta_block = (
            f'<text x="26" y="{cta_y}" class="cta" fill="{accent}">'
            f"{html.escape(cta_text)} &#8594;</text>"
        )
    else:
        cta_block = (
            f'<text x="26" y="{cta_y}" class="cta" fill="#8B949E">'
            "NATIONAL HACKATHON RECOGNITION</text>"
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
<defs>
  <style>
    .badge {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10px; font-weight: 700; letter-spacing: 1.2px; }}
    .title {{ font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 17px; font-weight: 700; fill: #F0F6FC; }}
    .sub {{ font-family: "Segoe UI", Ubuntu, -apple-system, sans-serif; font-size: 12.5px; font-weight: 400; fill: #9CA3AF; }}
    .cta {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; }}
    @keyframes cardShimmer {{
      0%   {{ transform: translateX(-220px); opacity: 0; }}
      15%  {{ opacity: 0.32; }}
      55%  {{ opacity: 0.32; }}
      70%  {{ transform: translateX({w + 220}px); opacity: 0; }}
      100% {{ transform: translateX({w + 220}px); opacity: 0; }}
    }}
    @keyframes borderPulse {{
      0%, 100% {{ stroke-opacity: 0.35; }}
      50%      {{ stroke-opacity: 0.85; }}
    }}
    .shimmer {{ animation: cardShimmer 7.5s infinite ease-in-out; animation-delay: {delay}; }}
    .pulse-border {{ animation: borderPulse 5s infinite ease-in-out; animation-delay: {delay}; }}
  </style>
  <linearGradient id="shimmerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="{accent}" stop-opacity="0"/>
    <stop offset="50%" stop-color="{accent}" stop-opacity="0.18"/>
    <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="cardClip">
    <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="9"/>
  </clipPath>
</defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="9" fill="#0D1117" stroke="#30363D" stroke-width="1"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="9" fill="none" stroke="{accent}" stroke-width="1.2" class="pulse-border"/>
<g clip-path="url(#cardClip)">
  <g transform="skewX(-18)">
    <rect x="0" y="0" width="180" height="{h}" fill="url(#shimmerGrad)" class="shimmer"/>
  </g>
</g>
<rect x="1" y="20" width="3" height="{h - 40}" rx="1.5" fill="{accent}"/>
<g transform="translate(26, 20)">
  {icon_paths}
</g>
<text x="56" y="34" class="badge" fill="{accent}">{html.escape(badge_text)}</text>
<text x="26" y="{title_y}" class="title">{html.escape(title)}</text>
<text x="26" y="{sub_y}" class="sub">{html.escape(subtitle)}</text>
{cta_block}
</svg>
"""


def main() -> None:
    write_svg(
        "executive-summary.svg",
        render_executive_summary(),
    )
    write_svg(
        "header-projects.svg",
        render_section_header("02", "Key Engineering Projects", "production systems · architecture", "-1.2s"),
    )
    write_svg(
        "header-credentials.svg",
        render_section_header("03", "Verified Credentials & Honors", "aws certified · national hackathons", "-2.5s"),
    )

    cloud_icon = '<path d="M16.5 14H5.8a3.8 3.8 0 0 1-.4-7.58A5.2 5.2 0 0 1 15.6 5.4a4.2 4.2 0 0 1 .9 8.6Z" fill="none" stroke="#58A6FF" stroke-width="1.8" stroke-linejoin="round"/>'
    ai_icon = '<circle cx="10" cy="10" r="4" fill="none" stroke="#39D353" stroke-width="1.8"/><path d="M10 1v3m0 12v3M1 10h3m12 0h3M3.6 3.6l2.2 2.2m8.4 8.4 2.2 2.2m0-12.8-2.2 2.2m-8.4 8.4-2.2 2.2" stroke="#39D353" stroke-width="1.5" stroke-linecap="round"/>'
    trophy_icon = '<path d="M5 3h10v5a5 5 0 0 1-10 0V3Zm0 2H2.5a1.5 1.5 0 0 0 0 3H5m10-3h2.5a1.5 1.5 0 0 1 0 3H15M10 13v4m-3.5 1h7" fill="none" stroke="#F59E0B" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
    medal_icon = '<circle cx="10" cy="12" r="5.5" fill="none" stroke="#39D353" stroke-width="1.7"/><path d="M7 2.5 9.2 6.8m3.8-4.3L10.8 6.8" stroke="#39D353" stroke-width="1.7" stroke-linecap="round"/>'
    grad_icon = '<path d="M1 7.5 10 3l9 4.5-9 4.5L1 7.5Zm3.5 2v4.2c0 1.4 2.5 2.8 5.5 2.8s5.5-1.4 5.5-2.8V9.5" fill="none" stroke="#A371F7" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'

    write_svg(
        "cred-aws-cloud.svg",
        render_credential_card(
            "AMAZON WEB SERVICES · CERTIFIED",
            "AWS Certified Cloud Practitioner",
            "Core cloud infrastructure, IAM security & Well-Architected principles",
            "VERIFY AWS CREDENTIAL",
            "#58A6FF",
            cloud_icon,
            "-0.5s",
        ),
    )
    write_svg(
        "cred-aws-ai.svg",
        render_credential_card(
            "AMAZON WEB SERVICES · CERTIFIED",
            "AWS Certified AI Practitioner",
            "ML pipelines, cloud AI services & responsible AI governance",
            "VERIFY AWS CREDENTIAL",
            "#39D353",
            ai_icon,
            "-2.0s",
        ),
    )
    write_svg(
        "cred-innotech.svg",
        render_credential_card(
            "1ST PLACE · 400+ PARTICIPANTS",
            "Innotech Hackathon — 1st Place Winner",
            "Ranked 1st presenting CodVidya's asynchronous judging architecture",
            None,
            "#F59E0B",
            trophy_icon,
            "-3.5s",
        ),
    )
    write_svg(
        "cred-nit.svg",
        render_credential_card(
            "TOP 10 · 100+ TEAMS NATIONWIDE",
            "NIT Jalandhar Hackathon — Finalist",
            "Selected in Top 10 out of 100+ engineering teams in a 36-hour sprint",
            None,
            "#39D353",
            medal_icon,
            "-5.0s",
        ),
    )
    write_svg(
        "cred-aws-genai.svg",
        render_credential_card(
            "AWS ACADEMY GRADUATE · VERIFIED BADGE",
            "AWS Academy Graduate — Generative AI Foundations",
            "Demonstrated proficiency in large language model architectures and cloud-hosted inference pipelines",
            "VERIFY CREDLY BADGE",
            "#A371F7",
            grad_icon,
            "-1.2s",
            wide=True,
        ),
    )


if __name__ == "__main__":
    main()
