"""'On GitHub' panel, refreshed daily by .github/workflows/profile.yml (needs GITHUB_TOKEN)."""
from __future__ import annotations

import datetime as dt
import json
import os
import urllib.request

import content as C
from noir import theme as T
from noir.fonts import measure
from noir.svg import DISPLAY, MONO, SANS, Doc

W, P = T.W, T.PAD
PALETTE = ["#00D4FF", "#FFB84D", "#A9BCD8", "#3B82C4", "#6EE7F9", "#5B6B8C"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false) {
      totalCount
      nodes { name stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } }
    }
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}"""


def fetch(login: str, token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": login},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]["user"]


def summarize(user: dict, login: str) -> dict:
    days = [d for w in user["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    current = 0
    for i, d in enumerate(reversed(days)):
        if d["contributionCount"]:
            current += 1
        elif i == 0:  # today may simply be empty so far
            continue
        else:
            break
    langs: dict[str, int] = {}
    repos = [r for r in user["repositories"]["nodes"] if r["name"].lower() != login.lower()]
    for r in repos:
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])
    shown = [(n, s / total) for n, s in top[:5]]
    rest = 1 - sum(f for _, f in shown)
    if rest > 0.005:
        shown.append(("Other", rest))
    return {
        "contributions": user["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "current": current, "longest": longest, "repos": len(repos),
        "stars": sum(r["stargazerCount"] for r in repos), "langs": shown,
    }


def panel() -> Doc | None:
    token = os.environ.get("GITHUB_TOKEN")
    login = os.environ.get("GITHUB_LOGIN", C.LOGIN)
    stats = None
    if token:
        try:
            stats = summarize(fetch(login, token), login)
        except Exception as exc:  # keep the last good panel
            print("github stats unavailable:", exc)
            return None
    H = 262
    d = Doc(W, H, "On GitHub", "GitHub activity: contributions, streaks, repositories and languages.", radius=26)
    d.glow(W * 0.92, 0, 420, 220, T.CYAN, 0.10)
    d.label(P, 56, "04", "On GitHub", W - P - 190)
    stamp = dt.datetime.utcnow().strftime("Updated %d %b %Y") if stats else "Updating daily"
    d.mono(stamp, W - P, 56, 10.5, T.MUTED, 0.14, anchor="end")
    items = [
        (stats and f"{stats['contributions']:,}", "Contributions, last year", T.CYAN),
        (stats and f"{stats['current']}d", "Current streak", T.FG),
        (stats and f"{stats['longest']}d", "Longest streak", T.FG),
        (stats and str(stats["repos"]), "Public repositories", T.AMBER),
    ]
    colw = (W - 2 * P) / 4
    for i, (val, lab, color) in enumerate(items):
        x = P + i * colw + (18 if i else 0)
        if i:
            d.rect(P + i * colw - 1, 92, 1, 62, fill=T.HAIR)
        d.text(val or "—", x, 132, DISPLAY, 34, color, -0.04)
        d.mono(lab, x, 156, 10, T.MUTED, 0.1)
    # languages bar
    by = 192
    d.mono("Languages", P, by - 4, 10, T.MUTED, 0.14)
    bx, bw = P + 104, W - 2 * P - 104
    d.define("lbclip", f'<clipPath id="lbclip"><rect x="{bx}" y="{by - 12}" width="{bw}" height="9" rx="4.5"/></clipPath>')
    d.rect(bx, by - 12, bw, 9, 4.5, fill="rgba(150,180,230,.08)")
    langs = stats["langs"] if stats else []
    with d.group('clip-path="url(#lbclip)"'):
        cx = bx
        for k, (name, frac) in enumerate(langs):
            seg = bw * frac
            d.rect(cx, by - 12, max(seg - 2, 0), 9, fill=PALETTE[k % len(PALETTE)])
            cx += seg
    lx, ly = P, by + 30
    for k, (name, frac) in enumerate(langs):
        label = f"{name} {frac * 100:.0f}%"
        lw = measure(label, SANS, 13) + 12
        if lx + lw + 14 > W - P:
            break
        d.add(f'<circle cx="{lx + 4}" cy="{ly - 4.5}" r="4" fill="{PALETTE[k % len(PALETTE)]}"/>')
        d.text(name, lx + 14, ly, SANS, 13, T.BODY)
        d.text(f"{frac * 100:.0f}%", lx + 14 + measure(name, SANS, 13) + 6, ly, MONO, 11, T.MUTED)
        lx += lw + 30
    return d
