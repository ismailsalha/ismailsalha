"""A tiny SVG document builder with the portfolio's primitives (labels, pills, tags, chips…)."""
from __future__ import annotations

import base64
import html
from contextlib import contextmanager
from pathlib import Path

from . import theme as T
from .fonts import arabic_runs, face, measure, tokens, wrap
from .icons import FILLED, LINE

MONO = ("mono", 500)
SANS = ("sans", 400)
SANS_M = ("sans", 500)
DISPLAY = ("display", 800)

BASE_CSS = (
    "@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}"
    "@keyframes fade{from{opacity:0}to{opacity:1}}"
    "@keyframes pop{from{opacity:0;transform:scale(.86)}to{opacity:1;transform:none}}"
    "@keyframes ping{0%{transform:scale(1);opacity:.7}75%,100%{transform:scale(2.8);opacity:0}}"
    ".rise{animation:rise .9s cubic-bezier(.16,1,.3,1) both}"
    ".fade{animation:fade 1.2s ease both}"
    ".pop{animation:pop .8s cubic-bezier(.16,1,.3,1) both;transform-box:fill-box;transform-origin:center}"
    ".ping{animation:ping 2.4s cubic-bezier(0,0,.2,1) infinite;transform-box:fill-box;transform-origin:center}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


class Doc:
    def __init__(self, w: float, h: float, title: str, desc: str = "", radius: float = 24, ground: str = T.BG):
        self.w, self.h, self.title, self.desc = w, h, title, desc
        self.radius, self.ground = radius, ground
        self.defs: list[str] = []
        self.body: list[str] = []
        self.css: list[str] = []
        self._glyphs: dict = {}
        self._n = 0
        self._def_keys: set[str] = set()

    # ── plumbing ──────────────────────────────────────────────────────────
    def id(self, prefix: str = "d") -> str:
        self._n += 1
        return f"{prefix}{self._n}"

    def add(self, s: str) -> "Doc":
        self.body.append(s)
        return self

    def define(self, key: str, s: str) -> str:
        if key not in self._def_keys:
            self._def_keys.add(key)
            self.defs.append(s)
        return key

    def animate(self) -> None:
        if BASE_CSS not in self.css:
            self.css.append(BASE_CSS)

    @contextmanager
    def group(self, attrs: str = ""):
        self.body.append(f"<g {attrs}>" if attrs else "<g>")
        yield
        self.body.append("</g>")

    def _ref(self, f, gid: int) -> str:
        k = (f.key, gid)
        if k not in self._glyphs:
            ref = f"g{len(self._glyphs):x}"
            self._glyphs[k] = ref
            self.defs.append(f'<path id="{ref}" d="{f.path(gid)}"/>')
        return self._glyphs[k]

    # ── text ──────────────────────────────────────────────────────────────
    def text(self, s, x, y, font=SANS, size=16, fill=T.BODY, tracking=0.0, anchor="start", attrs="",
             glyph_attrs=None, stroke=None, stroke_w=1.5, upper=False) -> float:
        if upper:
            s = s.upper()
        f = face(*font)
        gl = f.shape(s)
        sc = size / f.upem
        tu = tracking * f.upem
        w = (sum(g[1] for g in gl) + tu * max(len(gl) - 1, 0)) * sc
        if anchor == "end":
            x -= w
        elif anchor == "middle":
            x -= w / 2
        parts, pen = [], 0.0
        for i, (gid, adv, xo, yo) in enumerate(gl):
            if f.path(gid):
                extra = glyph_attrs(i) if glyph_attrs else ""
                ya = f' y="{-yo}"' if yo else ""
                parts.append(f'<use href="#{self._ref(f, gid)}" x="{round(pen + xo)}"{ya}{extra}/>')
            pen += adv + tu
        if stroke is None:
            paint = f' fill="{fill}"'
        else:
            paint = f' fill="none" stroke="{stroke}" stroke-width="{stroke_w / sc:.0f}" stroke-linejoin="round"'
        self.body.append(f'<g transform="translate({x:.1f} {y:.1f}) scale({sc:.5f})"{paint}{attrs}>{"".join(parts)}</g>')
        return w

    def text_ar(self, s, x, y, size=16, fill=T.FG, weight=600, anchor="end", attrs="") -> float:
        """Right-to-left Arabic line (with Latin digits) drawn as outlines. Returns its width."""
        runs = []
        total = 0.0
        for f, chunk, direction in arabic_runs(s, weight):
            gl = f.shape(chunk, direction=direction)
            sc = size / f.upem
            w = sum(g[1] for g in gl) * sc
            runs.append((f, gl, sc, w))
            total += w
        if anchor == "end":
            x -= total
        elif anchor == "middle":
            x -= total / 2
        pen = x
        out = []
        for f, gl, sc, w in runs:
            parts, adv_u = [], 0.0
            for gid, adv, xo, yo in gl:
                if f.path(gid):
                    ya = f' y="{-yo}"' if yo else ""
                    parts.append(f'<use href="#{self._ref(f, gid)}" x="{round(adv_u + xo)}"{ya}/>')
                adv_u += adv
            if parts:
                out.append(f'<g transform="translate({pen:.1f} {y:.1f}) scale({sc:.5f})">{"".join(parts)}</g>')
            pen += w
        self.body.append(f'<g fill="{fill}"{attrs}>{"".join(out)}</g>')
        return total

    def mono(self, s, x, y, size=11.5, fill=T.MUTED, tracking=0.12, anchor="start", weight=500, attrs="") -> float:
        return self.text(s.upper(), x, y, ("mono", weight), size, fill, tracking, anchor, attrs)

    def lines(self, text, x, y, width, font=SANS, size=15, lh=24, fill=T.BODY, max_lines=None) -> int:
        ls = wrap(text, font, size, width)
        if max_lines and len(ls) > max_lines:
            raise ValueError(f"text needs {len(ls)} lines (max {max_lines}): {text[:40]}…")
        for i, line in enumerate(ls):
            self.text(line, x, y + i * lh, font, size, fill)
        return len(ls)

    def para(self, runs, x, y, width, size=15, lh=25, font=SANS, fill=T.BODY) -> int:
        """Rich paragraph: runs = [(text, font|None, fill|None)]. Returns the number of lines."""
        toks = tokens([(t, f or font, c or fill) for t, f, c in runs])
        sw = measure(" ", font, size)
        lines, line, lw = [], [], 0.0
        for tk in toks:
            w = measure(tk["t"], tk["font"], size)
            gap = sw if (tk["sp"] and line) else 0.0
            if line and tk["sp"] and lw + gap + w > width:
                lines.append(line)
                line, lw, gap = [], 0.0, 0.0
            line.append((tk, lw + gap))
            lw += gap + w
        if line:
            lines.append(line)
        for li, ln in enumerate(lines):
            i = 0
            while i < len(ln):
                tk, ox = ln[i]
                s, j = tk["t"], i + 1
                while j < len(ln) and ln[j][0]["font"] == tk["font"] and ln[j][0]["fill"] == tk["fill"]:
                    s += (" " if ln[j][0]["sp"] else "") + ln[j][0]["t"]
                    j += 1
                self.text(s, x + ox, y + li * lh, tk["font"], size, tk["fill"])
                i = j
        return len(lines)

    # ── shapes ────────────────────────────────────────────────────────────
    def rect(self, x, y, w, h, r=0, fill="none", stroke=None, sw=1, attrs="") -> None:
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        rr = f' rx="{r}"' if r else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{rr} fill="{fill}"{st}{attrs}/>')

    def glow_def(self, color: str, opacity: float, key: str | None = None) -> str:
        key = key or f"rg{color[1:]}{int(opacity * 100)}"
        self.define(key, f'<radialGradient id="{key}"><stop offset="0" stop-color="{color}" stop-opacity="{opacity}"/>'
                         f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')
        return key

    def glow(self, cx, cy, rx, ry, color=T.CYAN, opacity=0.14, attrs="") -> None:
        g = self.glow_def(color, opacity)
        self.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#{g})"{attrs}/>')

    def dot(self, cx, cy, r=3.5, color=T.CYAN, halo=True, attrs="") -> None:
        if halo:
            g = self.glow_def(color, 0.55)
            self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 3.2:.1f}" fill="url(#{g})"/>')
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}"{attrs}/>')

    def live_dot(self, cx, cy, r=4, color=T.CYAN) -> None:
        self.animate()
        self.add(f'<circle class="ping" cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')
        self.dot(cx, cy, r, color)

    def icon(self, name, x, y, size=16, color=T.FG, sw=2) -> None:
        s = size / 24
        if name in FILLED:
            self.add(f'<path transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" fill="{color}" d="{FILLED[name]}"/>')
        else:
            self.add(f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" fill="none" stroke="{color}" '
                     f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{LINE[name]}</g>')

    def image(self, uri, x, y, w, h, clip=None, preserve="xMidYMid slice", attrs="") -> None:
        cp = f' clip-path="url(#{clip})"' if clip else ""
        self.add(f'<image href="{uri}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
                 f'preserveAspectRatio="{preserve}"{cp}{attrs}/>')

    # ── portfolio components ──────────────────────────────────────────────
    def label(self, x, y, index: str, text: str, rule_to: float | None = None) -> None:
        """Section header "● 01  ABOUT ────" (nn-label)."""
        self.dot(x + 3.5, y - 4, 3.5)
        w = self.mono(index, x + 17, y, 12, T.CYAN, 0.16)
        w2 = self.mono(text, x + 17 + w + 12, y, 12, T.MUTED, 0.16)
        if rule_to:
            x0 = x + 17 + w + 12 + w2 + 16
            gid = self.define("rule", '<linearGradient id="rule"><stop offset="0" stop-color="#96B4E6" stop-opacity=".28"/>'
                                      '<stop offset="1" stop-color="#96B4E6" stop-opacity="0"/></linearGradient>')
            self.rect(x0, y - 4.5, rule_to - x0, 1, fill=f"url(#{gid})")

    def badge(self, x, y, text, warm=False, live=False, anchor="start", h=30) -> float:
        """Accent pill (nn-badge): 'Open to opportunities', project type."""
        dotw = 18 if live else 0
        tw = measure(text.upper(), MONO, 11.5, 0.1)
        w = tw + 26 + dotw
        if anchor == "end":
            x -= w
        c = T.AMBER if warm else T.CYAN
        self.rect(x, y, w, h, h / 2, fill=f"{c}14", stroke=f"{c}61")
        if live:
            self.live_dot(x + 16, y + h / 2, 3.5, c)
        self.mono(text, x + 13 + dotw, y + h / 2 + 4, 11.5, T.FG, 0.1)
        return w

    def tag(self, x, y, text, h=28) -> float:
        """Square-ish mono stack tag (nn-tag)."""
        tw = measure(text, MONO, 11.5)
        w = tw + 22
        self.rect(x, y, w, h, 8, fill="none", stroke=T.HAIR)
        self.text(text, x + 11, y + h / 2 + 4, MONO, 11.5, T.BODY)
        return w

    def chip(self, x, y, text, h=30, size=13.5) -> float:
        """Rounded skill chip (nn-chip)."""
        tw = measure(text, SANS, size)
        w = tw + 24
        self.rect(x, y, w, h, h / 2, fill="rgba(150,180,230,.03)", stroke=T.HAIR)
        self.text(text, x + 12, y + h / 2 + size * 0.36, SANS, size, T.BODY)
        return w

    def flow(self, items, x, y, maxw, kind="tag", gap=8, row_gap=8) -> float:
        """Lay out tags/chips left to right, wrapping. Returns the height used."""
        h = 28 if kind == "tag" else 30
        cx, cy = x, y
        for it in items:
            iw = (measure(it, MONO, 11.5) + 22) if kind == "tag" else (measure(it, SANS, 13.5) + 24)
            if cx > x and cx + iw > x + maxw:
                cx, cy = x, cy + h + row_gap
            (self.tag if kind == "tag" else self.chip)(cx, cy, it)
            cx += iw + gap
        return cy + h - y

    def outline_number(self, s, x, y, size, color=T.CYAN_STROKE, sw=1.6) -> float:
        return self.text(s, x, y, DISPLAY, size, stroke=color, stroke_w=sw, tracking=-0.06)

    def arrow_button(self, cx, cy, r=22, filled=False) -> None:
        if filled:
            self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{T.CYAN}"/>')
            self.icon("arrow", cx - 9, cy - 9, 18, T.ON_CYAN)
        else:
            self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(150,180,230,.06)" stroke="rgba(150,180,230,.22)"/>')
            self.icon("arrow", cx - 9, cy - 9, 18, T.FG)

    # ── output ────────────────────────────────────────────────────────────
    def render(self) -> str:
        r = self.radius
        clip = f'<clipPath id="frame"><rect width="{self.w}" height="{self.h}" rx="{r}"/></clipPath>'
        css = f"<style>{''.join(self.css)}</style>" if self.css else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
            f'role="img" aria-labelledby="title desc"><title id="title">{esc(self.title)}</title>'
            f'<desc id="desc">{esc(self.desc)}</desc>{css}<defs>{clip}{"".join(self.defs)}</defs>'
            f'<g clip-path="url(#frame)"><rect width="{self.w}" height="{self.h}" fill="{self.ground}"/>{"".join(self.body)}</g>'
            f'<rect x=".5" y=".5" width="{self.w - 1}" height="{self.h - 1}" rx="{r - .5}" fill="none" stroke="{T.HAIR}"/></svg>'
        )

    def save(self, path: Path) -> int:
        data = self.render()
        Path(path).write_text(data, encoding="utf-8")
        return len(data.encode())
