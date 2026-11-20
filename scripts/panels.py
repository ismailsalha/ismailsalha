"""The profile README, panel by panel. Each function returns a Doc (one SVG)."""
from __future__ import annotations

import datetime as dt
import math
from pathlib import Path

import content as C
from noir import theme as T
from noir.fonts import face, measure, wrap
from noir.svg import DISPLAY, MONO, SANS, SANS_M, Doc, data_uri

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT / "scripts" / "media"
W, P, HALF = T.W, T.PAD, T.HALF
BOLD = ("sans", 500)


def media(name: str) -> str:
    return data_uri(MEDIA / name, "image/webp")


def md_runs(text: str):
    """'**bold**' → [(text, font, fill)]."""
    runs = []
    for i, part in enumerate(text.split("**")):
        if part:
            runs.append((part, BOLD, T.FG) if i % 2 else (part, None, None))
    return runs


def fit(text, font, width, tracking=0.0):
    return width / measure(text, font, 1.0, tracking)


def cap(font, size):
    return face(*font).cap * size / 1000


def card_bg(d: Doc, glow_x=0.85):
    gid = d.define("cardbg", '<linearGradient id="cardbg" x1="0" y1="0" x2="1" y2="1">'
                             '<stop offset="0" stop-color="#0E1A33"/><stop offset=".55" stop-color="#0A1222"/>'
                             '<stop offset="1" stop-color="#090F1E"/></linearGradient>')
    d.rect(0, 0, d.w, d.h, fill=f"url(#{gid})")
    d.glow(d.w * glow_x, 0, d.w * 0.75, d.h * 0.6, T.CYAN, 0.10)


def dot_grid(d: Doc, x, y, w, h, key="dg"):
    d.define(key + "p", f'<pattern id="{key}p" width="16" height="16" patternUnits="userSpaceOnUse">'
                        '<circle cx="8" cy="8" r="1" fill="#96B4E6" fill-opacity=".18"/></pattern>')
    d.define(key + "g", f'<radialGradient id="{key}g" cx=".5" cy=".3" r=".6"><stop offset=".2" stop-color="#fff"/>'
                        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
    d.define(key + "m", f'<mask id="{key}m"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{key}g)"/></mask>')
    d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{key}p)" mask="url(#{key}m)"/>')


def line_grid(d: Doc, step=72, opacity=0.035):
    d.define("lgp", f'<pattern id="lgp" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
                    f'<path d="M{step} 0V{step}M0 {step}H{step}" stroke="#96B4E6" stroke-opacity="{opacity}" fill="none"/></pattern>')
    d.add(f'<rect width="{d.w}" height="{d.h}" fill="url(#lgp)"/>')


def arch_path(x, y, w, h, rb):
    rx, ry = w / 2, h * 0.3793
    return (f"M{x:.1f} {y + ry:.1f}A{rx:.1f} {ry:.1f} 0 0 1 {x + w:.1f} {y + ry:.1f}V{y + h - rb:.1f}"
            f"A{rb} {rb} 0 0 1 {x + w - rb:.1f} {y + h:.1f}H{x + rb:.1f}A{rb} {rb} 0 0 1 {x:.1f} {y + h - rb:.1f}Z")


def delay(s: float) -> str:
    return f'style="animation-delay:{s:.2f}s"'


# ── 1. Hero ──────────────────────────────────────────────────────────────────
def hero() -> Doc:
    H = 704
    d = Doc(W, H, f"{C.NAME} — {C.ROLE}", f"{C.INTRO} Focus: {', '.join(C.FOCUS)}. Open to {', '.join(C.OPEN_TO).lower()}.", radius=26)
    d.animate()
    d.css.append(
        "@keyframes up{from{transform:translateY(1150px)}to{transform:none}}"
        ".gl use{animation:up 1.05s cubic-bezier(.16,1,.3,1) both}"
        "@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}"
        ".float{animation:float 6s ease-in-out infinite}"
        "@keyframes trace{0%{transform:translateY(0);opacity:0}15%,85%{opacity:1}100%{transform:translateY(300px);opacity:0}}"
        ".trace{animation:trace 5.5s linear infinite}"
    )
    line_grid(d)
    d.glow(W * 0.70, H * 0.47, 360, 320, T.CYAN, 0.15)
    d.glow(W * 0.08, H * 0.92, 260, 160, T.AMBER, 0.07)

    # top row
    with d.group(f'class="rise" {delay(0.02)}'):
        d.badge(P, 30, "Open to opportunities", live=True)
        locw = d.mono(C.LOCATION, W - P, 50, 11.5, T.MUTED, 0.12, anchor="end")
        d.text_ar(C.NAME_AR, W - P - locw - 16, 52, 21, T.AMBER, 600)
    d.rect(P, 82, W - 2 * P, 1, fill=T.HAIR)

    # arched portrait (behind the masthead)
    ax, ay, aw, ah, rb = 500, 150, 264, 440, 30
    cx = ax + aw / 2
    arch = arch_path(ax, ay, aw, ah, rb)
    d.define("archclip", f'<clipPath id="archclip"><path d="{arch}"/></clipPath>')
    d.define("archbg", f'<radialGradient id="archbg" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1" '
                       f'gradientTransform="matrix({1.3 * aw:.1f} 0 0 {0.75 * ah:.1f} {cx:.1f} {ay})">'
                       '<stop offset="0" stop-color="#12264A"/><stop offset=".45" stop-color="#0B1630"/>'
                       '<stop offset="1" stop-color="#070B16"/></radialGradient>')
    d.define("archfade", f'<linearGradient id="archfade" x1="0" y1="{ay}" x2="0" y2="{ay + ah}" gradientUnits="userSpaceOnUse">'
                         '<stop offset=".66" stop-color="#070B16" stop-opacity="0"/><stop offset=".84" stop-color="#070B16" stop-opacity=".45"/>'
                         '<stop offset="1" stop-color="#070B16" stop-opacity=".85"/></linearGradient>')
    with d.group(f'class="rise" {delay(0.25)}'):
        d.glow(cx, ay + ah / 2 + 40, 250, 330, T.CYAN, 0.20)
        e = 8.5
        d.add(f'<path d="{arch_path(ax - e, ay - e, aw + 2 * e, ah + 2 * e, rb + e)}" fill="#070B16" fill-opacity=".85" stroke="#00D4FF" stroke-opacity=".14"/>')
        d.add(f'<path d="{arch}" fill="url(#archbg)"/>')
        with d.group('clip-path="url(#archclip)"'):
            d.glow(cx, ay + ah * 0.30, aw * 0.46 * 1.4, ah * 0.34 * 1.4, T.CYAN, 0.34)
            d.glow(cx, ay + ah * 0.62, aw * 0.8, ah * 0.5, T.CYAN, 0.10)
            dot_grid(d, ax, ay, aw, ah)
            pw = aw * 1.08
            ph = pw * 700 / 470
            d.image(media("portrait.webp"), cx - pw / 2, ay + 50, pw, ph)
            d.rect(ax, ay, aw, ah, fill="url(#archfade)")
        d.add(f'<path d="{arch}" fill="none" stroke="#00D4FF" stroke-opacity=".45"/>')

    # circuit traces beside the arch
    for i, tx in enumerate((ax - 20, ax + aw + 20)):
        y0, y1 = ay + 120, ay + ah - 24
        d.add(f'<path d="M{tx} {y0}V{y1}" stroke="#00D4FF" stroke-opacity=".32" stroke-width="1.4" stroke-dasharray="1 6" stroke-linecap="round"/>')
        for ny in (y0, (y0 + y1) / 2 + (18 if i else -18), y1):
            d.add(f'<circle cx="{tx}" cy="{ny:.0f}" r="2.2" fill="#00D4FF" fill-opacity=".7"/>')
        with d.group(f'class="trace" {delay(1.6 + i * 2.6)}'):
            d.dot(tx, y0, 2.4, T.CYAN)

    # masthead
    name = "ISMAIL SALHA"
    fs = fit(name, DISPLAY, W - 2 * P - 30, -0.045)
    ch = cap(DISPLAY, fs)
    base = 112 + ch
    fc = face(*DISPLAY).cap
    d.define("mast", f'<linearGradient id="mast" gradientUnits="userSpaceOnUse" x1="0" y1="{-fc * 1.15:.0f}" x2="0" y2="{fc * 0.12:.0f}">'
                     '<stop offset=".25" stop-color="#FFFFFF"/><stop offset="1" stop-color="#A9BCD8"/></linearGradient>')
    d.define("nameclip", f'<clipPath id="nameclip"><rect x="0" y="{base - ch - 40:.0f}" width="{W}" height="{ch + 46:.0f}"/></clipPath>')
    with d.group('clip-path="url(#nameclip)"'):
        with d.group('class="gl"'):
            nw = d.text(name, P, base, DISPLAY, fs, "url(#mast)", -0.045,
                        glyph_attrs=lambda i: f' style="animation-delay:{0.08 + i * 0.045:.3f}s"')
    with d.group(f'class="pop" {delay(0.7)}'):
        d.dot(P + nw + 16, base - 9, 8.5, T.AMBER)

    # left column
    y = base + 60
    with d.group(f'class="rise" {delay(0.45)}'):
        for i, ln in enumerate(wrap(C.ROLE, BOLD, 25, 330)):
            d.text(ln, P, y + i * 32, BOLD, 25, T.FG)
    y += 76
    with d.group(f'class="rise" {delay(0.55)}'):
        colx = (P, P + 196)
        for i, item in enumerate(C.FOCUS):
            fx, fy = colx[i % 2], y + (i // 2) * 30
            warm = i == len(C.FOCUS) - 1
            d.dot(fx + 3, fy - 4, 3, T.AMBER if warm else T.CYAN)
            lines = wrap(item.upper(), MONO, 11.5, 190) if measure(item.upper(), MONO, 11.5, 0.12) > 200 else [item.upper()]
            for k, ln in enumerate(lines):
                d.mono(ln, fx + 15, fy + k * 16, 11.5, T.BODY, 0.12)
    y += 74
    with d.group(f'class="rise" {delay(0.65)}'):
        n = d.lines(C.INTRO, P, y, 410, SANS, 15.5, 26, T.BODY)
    y += (n - 1) * 26 + 46
    with d.group(f'class="rise" {delay(0.75)}'):
        d.mono("Open to", P, y, 10.5, T.MUTED, 0.16)
        d.rect(P, y + 10, 410, 1, fill=T.HAIR)
        ox = P
        for letter, item in zip("ABC", C.OPEN_TO):
            d.mono(letter, ox, y + 34, 10, T.AMBER, 0.1)
            iw = d.text(item, ox, y + 56, ("sans", 600), 15, T.FG)
            ox += iw + 28

    # tool chips on the arch edges (float gently)
    chips = [(C.HERO_CHIPS[0], ax, 0.42), (C.HERO_CHIPS[1], ax + aw, 0.46), (C.HERO_CHIPS[2], ax, 0.73), (C.HERO_CHIPS[3], ax + aw, 0.80)]
    for i, (label, ex, rel) in enumerate(chips):
        tw = measure(label, MONO, 11.5)
        cw, chh = tw + 38, 28
        x0, y0 = ex - cw / 2, ay + ah * rel - chh / 2
        with d.group(f'class="pop" {delay(1.0 + i * 0.12)}'):
            with d.group(f'class="float" style="animation-delay:{-i * 1.6:.1f}s"'):
                d.rect(x0, y0, cw, chh, chh / 2, fill="rgba(11,18,34,.92)", stroke="rgba(0,212,255,.32)")
                d.dot(x0 + 14, y0 + chh / 2, 3, T.CYAN, halo=False)
                d.text(label, x0 + 25, y0 + chh / 2 + 4, MONO, 11.5, T.FG)

    # stats strip
    sy = 606
    d.rect(P, sy, W - 2 * P, 1, fill=T.HAIR)
    colw = (W - 2 * P) / 4
    for i, (val, lab, tone) in enumerate(C.HERO_STATS):
        x = P + i * colw
        with d.group(f'class="rise" {delay(1.05 + i * 0.1)}'):
            if i:
                d.rect(x - 1, sy + 18, 1, 58, fill=T.HAIR)
            vx = x + (18 if i else 0)
            if tone == "outline":
                d.text(val, vx, sy + 52, DISPLAY, 30, stroke=T.CYAN, stroke_w=1.3, tracking=-0.04)
            else:
                d.text(val, vx, sy + 52, DISPLAY, 30, T.AMBER if tone == "amber" else T.FG, -0.04)
            d.mono(lab, vx, sy + 76, 10, T.MUTED, 0.1)
    return d


# ── CTA buttons ──────────────────────────────────────────────────────────────
def button(label: str, filled: bool, icon: str = "arrow") -> Doc:
    h = 52
    tw = measure(label, BOLD, 16)
    w = round(tw + 30 + 30 + (10 if icon else 0))
    d = Doc(w, h, label, label, radius=h / 2, ground=T.CYAN if filled else "#0B1222")
    if not filled:
        d.glow(w * 0.5, 0, w * 0.7, h, T.CYAN, 0.10)
    d.text(label, 30, h / 2 + 5.6, BOLD, 16, T.ON_CYAN if filled else T.FG)
    if icon:
        d.icon(icon, 30 + tw + 12, h / 2 - 8, 16, T.ON_CYAN if filled else T.CYAN, 2.2)
    return d


# ── 2. Marquee ───────────────────────────────────────────────────────────────
def marquee() -> Doc:
    H = 150
    d = Doc(W, H, "Toolkit", "Tools: " + ", ".join(C.MARQUEE_TOOLS) + ". Areas: " + ", ".join(C.MARQUEE_AREAS) + ".", radius=26)
    d.animate()

    def sequence(items, font, size, sep, gap, upper=False):
        out, x = [], 0.0
        for it in items:
            t = it.upper() if upper else it
            w = measure(t, font, size, -0.02)
            out.append(("t", t, x))
            x += w + gap
            out.append(("s", sep, x - gap / 2))
        return out, x

    def draw(seq, L, reps, y, font, size, color, stroke=None, sepcolor=None):
        for r in range(reps):
            off = r * L
            for kind, val, x in seq:
                if kind == "t":
                    if stroke:
                        d.text(val, off + x, y, font, size, stroke=stroke, stroke_w=1.1, tracking=-0.02)
                    else:
                        d.text(val, off + x, y, font, size, color, -0.02)
                elif val == "+":
                    d.add(f'<path d="M{off + x - 6:.1f} {y - 8:.1f}h12M{off + x:.1f} {y - 14:.1f}v12" stroke="{sepcolor}" stroke-width="2.4" stroke-linecap="round"/>')
                else:
                    cxs, cys = off + x, y - 8
                    d.add(f'<path d="M{cxs:.1f} {cys - 7:.1f}Q{cxs:.1f} {cys:.1f} {cxs + 7:.1f} {cys:.1f}Q{cxs:.1f} {cys:.1f} {cxs:.1f} {cys + 7:.1f}'
                          f'Q{cxs:.1f} {cys:.1f} {cxs - 7:.1f} {cys:.1f}Q{cxs:.1f} {cys:.1f} {cxs:.1f} {cys - 7:.1f}Z" fill="{sepcolor}"/>')

    back, Lb = sequence(C.MARQUEE_AREAS, ("display", 700), 19, "*", 56, upper=True)
    front, Lf = sequence(C.MARQUEE_TOOLS, ("display", 700), 21, "+", 52)
    d.css.append(f"@keyframes mqb{{to{{transform:translateX(-{Lb:.1f}px)}}}}.mqb{{animation:mqb 48s linear infinite}}"
                 f"@keyframes mqf{{from{{transform:translateX(-{Lf:.1f}px)}}to{{transform:none}}}}.mqf{{animation:mqf 40s linear infinite}}")
    # back band
    with d.group(f'transform="rotate(3.2 {W / 2} {H / 2})"'):
        d.rect(-60, H / 2 - 18, W + 120, 50, fill="#0C1528", stroke="rgba(150,180,230,.10)")
        with d.group('class="mqb"'):
            draw(back, Lb, math.ceil((W + 2 * Lb) / Lb) + 1, H / 2 + 15, ("display", 700), 19, None,
                 stroke="rgba(242,246,252,.42)", sepcolor="rgba(0,212,255,.55)")
    # front band
    d.glow(W / 2, H / 2 + 6, W * 0.6, 50, T.CYAN, 0.30)
    with d.group(f'transform="rotate(-2.6 {W / 2} {H / 2})"'):
        d.rect(-60, H / 2 - 34, W + 120, 56, fill=T.CYAN)
        with d.group('class="mqf"'):
            draw(front, Lf, math.ceil((W + 2 * Lf) / Lf) + 1, H / 2 + 2, ("display", 700), 21, T.ON_CYAN,
                 sepcolor="rgba(3,18,27,.55)")
    return d


# ── 3. About ─────────────────────────────────────────────────────────────────
def about() -> Doc:
    H = 640
    d = Doc(W, H, "About — Engineer. Developer. Data Thinker.", " ".join(p.replace("**", "") for p in C.ABOUT), radius=26)
    d.glow(W * 0.9, 0, 420, 260, T.CYAN, 0.10)
    d.label(P, 58, "01", "About", W - P)
    fs, step = 52, 58
    y = 140
    d.text("Engineer.", P, y, DISPLAY, fs, T.FG, -0.05)
    d.text("Developer.", P + 74, y + step, DISPLAY, fs, stroke=T.FG, stroke_w=1.4, tracking=-0.05)
    w1 = d.text("Data", P + 148, y + 2 * step, DISPLAY, fs, T.CYAN, -0.05)
    d.text(" Thinker.", P + 148 + w1, y + 2 * step, DISPLAY, fs, T.FG, -0.05)

    # bio: two columns
    top = 336
    colw = (W - 2 * P - 44) / 2
    yy = top
    for ptxt in C.ABOUT[:2]:
        n = d.para(md_runs(ptxt), P, yy, colw, 15.5, 26)
        yy += n * 26 + 14
    rx = P + colw + 44
    n = d.para(md_runs(C.ABOUT[2]), rx, top, colw, 15.5, 26)

    # profile card
    cy = top + n * 26 + 10
    cw, chh = colw, 92
    d.rect(rx, cy, cw, chh, 18, fill="rgba(11,18,34,.85)", stroke=T.HAIR)
    d.glow(rx + cw * 0.15, cy + chh, cw * 0.6, chh, T.CYAN, 0.08)
    av = 56
    d.define("avclip", f'<clipPath id="avclip"><rect x="{rx + 18}" y="{cy + 18}" width="{av}" height="{av}" rx="16"/></clipPath>')
    d.image(media("avatar.webp"), rx + 18, cy + 18, av, av, clip="avclip")
    d.rect(rx + 18, cy + 18, av, av, 16, fill="none", stroke="rgba(0,212,255,.45)")
    nx = rx + 18 + av + 16
    nw = d.text(C.NAME, nx, cy + 42, ("display", 700), 15, T.FG, -0.02)
    d.text_ar(C.NAME_AR, nx + nw + 10, cy + 43, 15, T.AMBER, 600, anchor="start")
    d.mono("IEEE Student Member", nx, cy + 62, 10, T.MUTED, 0.1)
    d.mono("GDGoC Al-Aqsa Core Team", nx, cy + 78, 10, T.MUTED, 0.1)
    d.h = max(yy - 14 - 26 + 8, cy + chh) + 40
    return d


# ── 4. Toolkit ───────────────────────────────────────────────────────────────
def toolkit() -> Doc:
    gap = 16
    cw = (W - 2 * P - gap) / 2
    ch = 150
    H = 74 + 2 * ch + gap + 34
    d = Doc(W, H, "Toolkit — 4 groups", "; ".join(f"{t}: {', '.join(items)}" for _, t, _, items in C.TOOLKIT), radius=26)
    d.mono("Toolkit", P, 48, 11.5, T.MUTED, 0.16)
    d.mono("4 groups", W - P, 48, 11.5, T.MUTED, 0.16, anchor="end")
    for i, (code, title, icon, items) in enumerate(C.TOOLKIT):
        x = P + (i % 2) * (cw + gap)
        y = 74 + (i // 2) * (ch + gap)
        d.rect(x, y, cw, ch, 18, fill="#0B1222", stroke=T.HAIR)
        d.glow(x + cw * 0.85, y, cw * 0.6, ch * 0.6, T.CYAN, 0.10)
        d.mono(code, x + 20, y + 30, 11, T.AMBER if i == 3 else T.CYAN, 0.12)
        d.icon(icon, x + cw - 38, y + 16, 18, T.MUTED, 1.8)
        d.text(title, x + 20, y + 62, ("display", 700), 16, T.FG, -0.02)
        d.flow(items, x + 20, y + 80, cw - 40, kind="chip", gap=7, row_gap=7)
    return d


# ── 5. Selected work ─────────────────────────────────────────────────────────
def work_header() -> Doc:
    H = 210
    d = Doc(W, H, "Selected work", "Projects: real datasets, honest evaluation and interfaces built for real people.", radius=26)
    d.glow(W * 0.15, H, 380, 180, T.CYAN, 0.08)
    d.label(P, 56, "02", "Projects", W - P)
    w = d.text("Selected work", P, 132, DISPLAY, 52, T.FG, -0.05)
    d.dot(P + w + 12, 126, 6.5, T.CYAN)
    d.text("Real datasets, honest evaluation and interfaces built for real people.", P, 176, SANS, 15.5, T.BODY)
    lw = measure("All repositories", BOLD, 15)
    d.text("All repositories", W - P - 26 - lw, 176, BOLD, 15, T.FG)
    d.icon("arrow", W - P - 18, 163, 16, T.CYAN, 2.2)
    return d


def meta_row(d: Doc, x, y, meta, role=None):
    cx = x
    for kind, label in meta:
        if kind == "lock":
            d.icon("lock", cx, y - 11, 13, T.MUTED, 2)
            cx += 19
        elif kind == "github":
            d.icon("github", cx, y - 11, 13, T.MUTED)
            cx += 19
        else:
            d.dot(cx + 4, y - 4.5, 3.6, T.AMBER, halo=False)
            cx += 14
        cx += d.text(label, cx, y, SANS, 13.5, T.MUTED) + 18
    if role:
        d.icon("users", x, y + 15, 14, T.AMBER, 2)
        d.text(role, x + 21, y + 26, SANS, 13.5, T.AMBER)


def metrics(d: Doc, x, y, width, items, size=30, label_size=10):
    n = len(items)
    colw = width / n
    d.rect(x, y, width, 1, fill=T.HAIR)
    for i, it in enumerate(items):
        val, lab = it[0], it[1]
        tone = it[2] if len(it) > 2 else "fg"
        color = {"cyan": T.CYAN, "amber": T.AMBER}.get(tone, T.FG)
        mx = x + i * colw
        d.text(val, mx, y + 24 + size * 0.75, DISPLAY, size, color, -0.04)
        d.mono(lab, mx, y + 24 + size * 0.75 + 22, label_size, T.MUTED, 0.1)


def featured() -> Doc:
    p = C.FEATURED
    H = 586
    d = Doc(W, H, f"{p['num']} {p['title']} — {p['kind']}", p["text"], radius=28)
    card_bg(d)
    lx, lw = P, 430
    d.outline_number(p["num"], lx, 112, 84)
    d.badge(lx + lw, 66, p["kind"], anchor="end")
    d.text(p["title"], lx, 168, DISPLAY, 34, T.FG, -0.04)
    meta_row(d, lx, 200, p["meta"], p["role"])
    n = d.lines(p["text"], lx, 262, lw, SANS, 14.5, 24, T.BODY)
    ty = 262 + (n - 1) * 24 + 22
    th = d.flow(p["stack"], lx, ty, lw)
    cy = ty + th + 34
    d.text(p["cta"], lx, cy + 5, BOLD, 15, T.FG)
    d.arrow_button(lx + measure(p["cta"], BOLD, 15) + 30, cy, 16)

    # right column: banner + channels
    rx, rw = 492, W - P - 492
    d.define("bnclip", f'<clipPath id="bnclip"><rect x="{rx}" y="40" width="{rw}" height="{rw * 225 / 720:.1f}" rx="14"/></clipPath>')
    bh = rw * 225 / 720
    d.rect(rx - 10, 30, rw + 20, 300, 20, fill="rgba(7,11,22,.55)", stroke=T.HAIR)
    d.image(media("radar-banner.webp"), rx, 40, rw, bh, clip="bnclip")
    yy = 40 + bh + 30
    d.mono("Telegram channels", rx, yy, 10.5, T.MUTED, 0.14)
    d.mono(str(len(p["channels"])), rx + rw, yy, 10.5, T.MUTED, 0.14, anchor="end")
    yy += 14
    for i, (img, name, handle) in enumerate(p["channels"]):
        ry = yy + i * 50
        d.rect(rx, ry, rw, 42, 12, fill="rgba(150,180,230,.03)", stroke=T.HAIR)
        cid = f"ch{i}"
        d.define(cid, f'<clipPath id="{cid}"><circle cx="{rx + 26}" cy="{ry + 21}" r="13"/></clipPath>')
        d.image(media(f"{img}.webp"), rx + 13, ry + 8, 26, 26, clip=cid)
        d.text(name, rx + 50, ry + 26, BOLD, 13.5, T.FG)
        d.text(handle, rx + rw - 14, ry + 25.5, MONO, 11, T.MUTED, anchor="end")

    my = max(cy + 40, 30 + 300 + 30)
    metrics(d, P, my, W - 2 * P, p["metrics"], 32)
    d.h = my + 112
    return d


def nashrati_art(d: Doc, x, y, w, h):
    d.rect(x, y, w, h, 16, fill="rgba(7,11,22,.6)", stroke=T.HAIR)
    d.glow(x + w * 0.3, y + h, w * 0.7, h * 0.6, T.CYAN, 0.10)

    def window(wx, wy, ww, label, img, cid):
        ih = ww * 325 / 660
        hh = 22
        d.rect(wx, wy, ww, ih + hh, 10, fill="#0B1222", stroke="rgba(150,180,230,.18)")
        for k in range(3):
            d.add(f'<circle cx="{wx + 12 + k * 9}" cy="{wy + 11}" r="2.6" fill="#96B4E6" fill-opacity=".35"/>')
        d.text(label, wx + 42, wy + 15, SANS, 10.5, T.MUTED)
        d.define(cid, f'<clipPath id="{cid}"><rect x="{wx + 1}" y="{wy + hh}" width="{ww - 2}" height="{ih - 1:.1f}" rx="0"/></clipPath>')
        d.image(media(img), wx + 1, wy + hh, ww - 2, ih - 1, clip=cid)

    window(x + 16, y + 16, w * 0.74, "Landing page", "nashrati-landing.webp", "nw1")
    window(x + w * 0.30, y + h * 0.43, w * 0.66, "Editor's review queue", "nashrati-dashboard.webp", "nw2")


def solar_art(d: Doc, x, y, w, h):
    d.rect(x, y, w, h, 16, fill="rgba(7,11,22,.6)", stroke=T.HAIR)
    d.glow(x + w, y, w * 0.8, h * 0.7, T.AMBER, 0.12)
    # header
    d.add(f'<circle cx="{x + 30}" cy="{y + 26}" r="14" fill="#FFB84D" fill-opacity=".15"/>')
    d.icon("sun", x + 21, y + 17, 18, T.AMBER, 2)
    d.text("Solar Power bot", x + 52, y + 24, BOLD, 13, T.FG)
    d.text("bot", x + 52, y + 38, MONO, 10, T.MUTED)
    d.icon("bot", x + w - 32, y + 17, 16, T.MUTED, 2)
    d.rect(x, y + 52, w, 1, fill=T.HAIR)
    # morning bubble (RTL, sits on the right)
    bw = w - 52
    bx, by = x + w - 16 - bw, y + 66
    lh = 21
    rows = C.SOLAR_MORNING
    bh = 16 + len(rows) * lh + 18
    d.rect(bx, by, bw, bh, 14, fill="#101A30", stroke=T.HAIR)
    ry = by + 26
    for icon, text, strong in rows:
        rx = bx + bw - 14
        if icon:
            d.icon(icon, rx - 14, ry - 12, 14, T.AMBER, 2)
        if text == "bars":
            # 7 ▂▄▆▇██▇▆▄▂ 5, drawn
            bx0 = rx - 22
            d.text("7", bx0, ry, MONO, 10.5, T.MUTED, anchor="end")
            cx = bx0 - 12
            for lvl in C.SOLAR_LEVELS:
                bhh = 15 * lvl / 8
                d.rect(cx - 6, ry - bhh, 6, bhh, 1.5, fill=T.AMBER, attrs=f' fill-opacity="{0.45 + lvl / 16:.2f}"')
                cx -= 9
            d.text("5", cx - 4, ry, MONO, 10.5, T.MUTED, anchor="end")
        else:
            d.text_ar(text, rx - 22, ry, 13, T.FG if strong else T.BODY, 800 if strong else 600)
        ry += lh
    d.text("06:30", bx + 14, by + bh - 10, MONO, 10, T.MUTED)
    # evening bubble
    ey = by + bh + 10
    eh = 86
    d.rect(bx, ey, bw, eh, 14, fill="#101A30", stroke=T.HAIR)
    d.icon("moon", bx + bw - 28, ey + 11, 14, T.CYAN, 2)
    d.text_ar(C.SOLAR_EVENING, bx + bw - 36, ey + 24, 13, T.FG, 800)
    gw = (bw - 28 - 6) / 2
    for k, ans in enumerate(C.SOLAR_ANSWERS):
        col, row = k % 2, k // 2
        gx = bx + bw - 14 - (col + 1) * gw - col * 6
        gy = ey + 36 + row * 24
        d.rect(gx, gy, gw, 20, 7, fill="rgba(0,212,255,.10)")
        d.text_ar(ans, gx + gw / 2, gy + 14.5, 11.5, T.CYAN, 600, anchor="middle")
    return ey + eh


def product(p: dict, H: int) -> Doc:
    d = Doc(HALF, H, f"{p['num']} {p['title']} — {p['kind']}", p["text"], radius=28)
    card_bg(d)
    x, w = 28, HALF - 56
    d.outline_number(p["num"], x, 86, 64)
    d.badge(HALF - 28, 42, p["kind"], warm=p["key"] == "solar", anchor="end")
    art_h = 300
    if p["key"] == "nashrati":
        nashrati_art(d, x, 108, w, art_h)
    else:
        solar_art(d, x, 108, w, art_h)
    y = 108 + art_h + 52
    d.text(p["title"], x, y, DISPLAY, 26, T.FG, -0.04)
    meta_row(d, x, y + 30, p["meta"], p["role"])
    n = d.lines(p["text"], x, y + 88, w, SANS, 14, 23, T.BODY)
    ty = y + 88 + (n - 1) * 23 + 20
    th = d.flow(p["stack"], x, ty, w)
    metrics(d, x, H - 112, w, p["metrics"], 24, 9.5)
    return d


def products():
    # measure both, use the taller height for both cards
    def height(p):
        n = len(wrap(p["text"], SANS, 14, HALF - 56))
        rows = 1
        cx = 0
        for it in p["stack"]:
            iw = measure(it, MONO, 11.5) + 22
            if cx and cx + iw > HALF - 56:
                rows, cx = rows + 1, 0
            cx += iw + 8
        return 108 + 300 + 52 + 88 + (n - 1) * 23 + 20 + rows * 36 + 18 + 112
    H = max(height(p) for p in C.PRODUCTS)
    return [product(p, H) for p in C.PRODUCTS]


def repo_card(p: dict, H: int) -> Doc:
    d = Doc(HALF, H, f"{p['num']} {p['title']} — {p['kind']}", p["text"], radius=28)
    card_bg(d)
    x, w = 28, HALF - 56
    d.outline_number(p["num"], x, 76, 52)
    d.badge(HALF - 28, 34, p["kind"], anchor="end")
    tl = wrap(p["title"], DISPLAY, 20, w)
    y = 122
    for i, ln in enumerate(tl):
        d.text(ln, x, y + i * 27, DISPLAY, 20, T.FG, -0.04)
    y += (len(tl) - 1) * 27 + 30
    meta = [("github", "Public repo")] + ([("dot", p["lang"])] if p["lang"] else [])
    meta_row(d, x, y, meta)
    n = d.lines(p["text"], x, y + 34, w, SANS, 14, 23, T.BODY)
    ty = y + 34 + (n - 1) * 23 + 20
    d.flow(p["stack"], x, ty, w)
    metrics(d, x, H - 128, w, [(v, l) for v, l in p["metrics"]], 21, 9.5)
    d.text("View on GitHub", x, H - 30, BOLD, 13.5, T.FG)
    d.icon("arrow", x + measure("View on GitHub", BOLD, 13.5) + 6, H - 42, 14, T.CYAN, 2.2)
    return d


def repos():
    def height(p):
        tl = len(wrap(p["title"], DISPLAY, 20, HALF - 56))
        n = len(wrap(p["text"], SANS, 14, HALF - 56))
        rows, cx = 1, 0
        for it in p["stack"]:
            iw = measure(it, MONO, 11.5) + 22
            if cx and cx + iw > HALF - 56:
                rows, cx = rows + 1, 0
            cx += iw + 8
        return 122 + (tl - 1) * 27 + 30 + 34 + (n - 1) * 23 + 20 + rows * 36 + 24 + 128
    out = []
    for pair in (C.REPOS[0:2], C.REPOS[2:4]):
        H = max(height(p) for p in pair)
        out += [repo_card(p, H) for p in pair]
    return out


# ── 6. Experience ────────────────────────────────────────────────────────────
def experience() -> Doc:
    gap = 16
    cw = (W - 2 * P - gap) / 2

    def card_h(e):
        tl = len(wrap(e["title"], DISPLAY, 21, cw - 120))
        n = len(wrap(e["text"], SANS, 13.5, cw - 44))
        rows, cx = 1, 0
        for it in e["tags"]:
            iw = measure(it, MONO, 11.5) + 22
            if cx and cx + iw > cw - 44:
                rows, cx = rows + 1, 0
            cx += iw + 8
        return 108 + (tl - 1) * 26 + 28 + (n - 1) * 21 + 16 + rows * 36 + 18

    ch = max(card_h(e) for e in C.EXPERIENCE)
    H = 220 + ch + 36
    d = Doc(W, H, "Experience & Activities", "; ".join(f"{e['title']}, {e['org']}: {e['text']}" for e in C.EXPERIENCE), radius=26)
    d.glow(W * 0.1, 0, 380, 220, T.CYAN, 0.09)
    d.label(P, 56, "03", "Experience", W - P)
    d.text("Experience &", P, 128, DISPLAY, 46, T.FG, -0.05)
    d.text("Activities", P, 180, DISPLAY, 46, stroke=T.FG, stroke_w=1.3, tracking=-0.05)
    d.lines("Community is part of the craft: workshops, tech events and professional growth alongside other engineers.",
            W - P - 290, 126, 290, SANS, 14.5, 23, T.BODY)
    for i, e in enumerate(C.EXPERIENCE):
        x, y = P + i * (cw + gap), 220
        tone = T.AMBER if e["warm"] else T.CYAN
        d.rect(x, y, cw, ch, 20, fill="#0B1222", stroke=T.HAIR)
        d.glow(x + cw * 0.8, y + 110, 140, 110, tone, 0.10)
        d.dot(x + 22, y + 24, 3.2, tone)
        d.mono("Current", x + 34, y + 28, 10.5, T.FG, 0.14)
        d.mono(e["code"], x + cw - 22, y + 28, 10.5, T.MUTED, 0.14, anchor="end")
        d.rect(x, y + 46, cw, 1, fill=T.HAIR)
        d.mono(e["org"], x + 22, y + 78, 10.5, tone, 0.06)
        tl = wrap(e["title"], DISPLAY, 21, cw - 120)
        for k, ln in enumerate(tl):
            d.text(ln, x + 22, y + 108 + k * 26, DISPLAY, 21, T.FG, -0.04)
        ty = y + 108 + (len(tl) - 1) * 26 + 28
        n = d.lines(e["text"], x + 22, ty, cw - 44, SANS, 13.5, 21, T.BODY)
        d.flow(e["tags"], x + 22, ty + (n - 1) * 21 + 16, cw - 44)
        # small art
        axx, ayy = x + cw - 58, y + 90
        if e["art"] == "network":
            nodes = [(0, -24), (-22, -8), (22, -8), (-14, 19), (14, 19), (0, 0)]
            for nx, ny in nodes[:-1]:
                d.add(f'<path d="M{axx} {ayy}L{axx + nx} {ayy + ny}" stroke="#00D4FF" stroke-opacity=".45"/>')
            d.add(f'<circle cx="{axx}" cy="{ayy}" r="30" fill="none" stroke="#00D4FF" stroke-opacity=".18" stroke-dasharray="2 4"/>')
            for nx, ny in nodes[:-1]:
                d.add(f'<circle cx="{axx + nx}" cy="{ayy + ny}" r="4" fill="#0B1222" stroke="#00D4FF" stroke-opacity=".8"/>')
            d.dot(axx, ayy, 5, T.CYAN)
        else:
            pts = " ".join(f"{axx - 36 + k * 3:.1f},{ayy + 10 * math.sin(k / 3.2):.1f}" for k in range(25))
            d.add(f'<polyline points="{pts}" fill="none" stroke="#FFB84D" stroke-opacity=".75" stroke-width="1.6"/>')
            d.add(f'<circle cx="{axx}" cy="{ayy}" r="34" fill="none" stroke="#FFB84D" stroke-opacity=".18" stroke-dasharray="2 4"/>')
            d.dot(axx + 3, ayy + 10 * math.sin(13 / 3.2), 5, T.AMBER)
    return d


# ── 7. Contact ───────────────────────────────────────────────────────────────
def contact() -> Doc:
    H = 330
    d = Doc(W, H, "Let's build something intelligent.", C.CONTACT_TEXT, radius=26)
    d.glow(W * 0.85, H, 420, 260, T.CYAN, 0.16)
    d.glow(W * 0.98, H, 200, 140, T.AMBER, 0.08)
    d.label(P, 56, "05", "Contact", 420)
    d.badge(W - P, 36, "Open to opportunities", live=True, anchor="end")
    d.text("Let’s build", P, 128, DISPLAY, 46, T.FG, -0.05)
    d.text("something", P, 178, DISPLAY, 46, T.FG, -0.05)
    d.text("intelligent.", P, 228, DISPLAY, 46, T.CYAN, -0.05)
    d.lines(C.CONTACT_TEXT, 470, 140, W - P - 470, SANS, 15, 25, T.BODY)
    d.icon("pin", P, H - 58, 14, T.AMBER, 2)
    d.mono(C.LOCATION, P + 22, H - 46, 10.5, T.MUTED, 0.14)
    return d


def channel(icon, label, value) -> Doc:
    h = 76
    d = Doc(HALF, h, f"{label}: {value}", f"{label}: {value}", radius=20, ground="#0B1222")
    d.glow(HALF * 0.1, h, HALF * 0.5, h, T.CYAN, 0.08)
    d.rect(18, 18, 40, 40, 12, fill="rgba(0,212,255,.08)", stroke="rgba(0,212,255,.25)")
    d.icon(icon, 29, 29, 18, T.CYAN, 2)
    d.mono(label, 74, 33, 10, T.MUTED, 0.14)
    d.text(value, 74, 55, BOLD, 15, T.FG)
    d.arrow_button(HALF - 40, h / 2, 17)
    return d


# ── 8. Footer ────────────────────────────────────────────────────────────────
def footer() -> Doc:
    H = 250
    d = Doc(W, H, "Designed & built with care.", f"© {dt.date.today().year} {C.NAME} · {C.ROLE} · {C.LOCATION}", radius=26)
    d.glow(W / 2, H, W * 0.55, H * 0.7, T.CYAN, 0.08)
    d.rect(P, 26, 36, 36, 10, fill="#0A0F1E", stroke=T.HAIR2)
    d.text("IS", P + 7.5, 49.5, DISPLAY, 13, "#F0EEE9", -0.02)
    d.add(f'<circle cx="{P + 30}" cy="{36}" r="2.6" fill="#00D4FF"/>')
    d.text("Designed & built with care.", P + 52, 49, SANS, 14.5, T.BODY)
    d.text(C.PORTFOLIO.replace("https://", ""), W - P, 49, MONO, 11.5, T.MUTED, anchor="end")
    # full-bleed Arabic signature
    probe = Doc(10, 10, "")
    fs = (W - 2 * P) / probe.text_ar(C.NAME_AR, 0, 0, 1, "#000", 800)
    d.text_ar(C.NAME_AR, W / 2, 178, fs, "#121C31", 800, anchor="middle")
    d.rect(P, 200, W - 2 * P, 1, fill=T.HAIR)
    y = 228
    d.mono(f"© {dt.date.today().year} {C.NAME}", P, y, 10, T.MUTED, 0.14)
    d.mono(C.ROLE, W / 2, y, 10, T.MUTED, 0.14, anchor="middle")
    d.mono(C.LOCATION, W - P, y, 10, T.AMBER, 0.14, anchor="end")
    return d
