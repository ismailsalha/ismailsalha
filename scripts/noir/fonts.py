"""Text → SVG outlines.

GitHub serves README images from raw.githubusercontent.com / camo, where an SVG can't load web
fonts. So every glyph is shaped with HarfBuzz (kerning, Arabic joining) and drawn as a path:
each glyph outline is stored once in <defs> and placed with <use>.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).resolve().parent.parent / "fonts"

FILES = {
    ("display", 500): "Unbounded-500.ttf",
    ("display", 700): "Unbounded-700.ttf",
    ("display", 800): "Unbounded-800.ttf",
    ("sans", 400): "ReadexPro-400.ttf",
    ("sans", 500): "ReadexPro-500.ttf",
    ("sans", 600): "ReadexPro-600.ttf",
    ("mono", 500): "JetBrainsMono-500.ttf",
    ("mono", 700): "JetBrainsMono-700.ttf",
    ("arabic", 600): "CairoArabic-600.ttf",
    ("arabic", 800): "CairoArabic-800.ttf",
    ("arabic-latin", 600): "CairoLatin-600.ttf",  # digits and ASCII punctuation inside Arabic lines
}


def _ntos(v: float) -> str:
    return str(int(round(v)))


class Face:
    def __init__(self, path: Path):
        data = path.read_bytes()
        self.key = path.stem
        self.hb_font = hb.Font(hb.Face(hb.Blob(data)))
        self.tt = TTFont(path)
        self.upem = self.tt["head"].unitsPerEm
        self.glyphset = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()
        os2 = self.tt["OS/2"]
        self.cap = getattr(os2, "sCapHeight", 0) or int(self.upem * 0.7)
        self.xheight = getattr(os2, "sxHeight", 0) or int(self.upem * 0.5)
        self._paths: dict[int, str] = {}

    def shape(self, text: str, features: dict | None = None, direction: str | None = None):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        if direction:
            buf.direction = direction
        hb.shape(self.hb_font, buf, features or {})
        return [(i.codepoint, p.x_advance, p.x_offset, p.y_offset) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]

    def path(self, gid: int) -> str:
        if gid not in self._paths:
            pen = SVGPathPen(self.glyphset, ntos=_ntos)
            self.glyphset[self.order[gid]].draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))  # y down
            self._paths[gid] = pen.getCommands()
        return self._paths[gid]


@lru_cache(maxsize=None)
def face(kind: str, weight: int) -> Face:
    return Face(FONT_DIR / FILES[(kind, weight)])


def measure(text: str, font: tuple[str, int], size: float, tracking: float = 0.0) -> float:
    f = face(*font)
    gl = f.shape(text)
    adv = sum(g[1] for g in gl) + tracking * f.upem * max(len(gl) - 1, 0)
    return adv * size / f.upem


def wrap(text: str, font, size: float, width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        cand = f"{cur} {w}" if cur else w
        if cur and measure(cand, font, size) > width:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def arabic_runs(text: str, weight: int = 600):
    """Split an Arabic line into visual-order runs [(face, chars, direction)].

    A minimal bidi pass for a right-to-left paragraph: Arabic letters are R, Latin letters and digits
    are L, neutrals take R unless they sit between two L characters. Characters the Arabic face
    lacks (digits, '!', ':') fall back to Cairo's Latin face."""
    fa, fl = face("arabic", weight), face("arabic-latin", 600)
    cov = fa.tt.getBestCmap()

    def kind(ch: str) -> str:
        o = ord(ch)
        if 0x0590 <= o <= 0x08FF or 0xFB1D <= o <= 0xFEFC:
            return "R"
        return "L" if (ch.isdigit() or ch.isalpha()) else "N"

    kinds = [kind(c) for c in text]
    dirs = []
    for i, k in enumerate(kinds):
        if k != "N":
            dirs.append(k)
            continue
        prev = next((kinds[j] for j in range(i - 1, -1, -1) if kinds[j] != "N"), "R")
        nxt = next((kinds[j] for j in range(i + 1, len(kinds)) if kinds[j] != "N"), "R")
        dirs.append("L" if prev == nxt == "L" else "R")
    runs: list[list] = []
    for ch, d in zip(text, dirs):
        f = fa if ord(ch) in cov else fl
        if runs and runs[-1][2] == d and runs[-1][0] is f:
            runs[-1][1] += ch
        else:
            runs.append([f, ch, d])
    # group into same-direction sequences, then reorder for an RTL paragraph
    seqs: list[list] = []
    for r in runs:
        if seqs and seqs[-1][0][2] == r[2]:
            seqs[-1].append(r)
        else:
            seqs.append([r])
    visual = []
    for seq in reversed(seqs):
        visual.extend(reversed(seq) if seq[0][2] == "R" else seq)
    return [(f, s, "rtl" if d == "R" else "ltr") for f, s, d in visual]


def tokens(runs):
    """[(text, font, fill)] → words that remember whether a space came before them."""
    out = []
    space = False
    for text, font, fill in runs:
        for m in re.finditer(r"\s+|\S+", text):
            t = m.group()
            if t.isspace():
                space = True
                continue
            out.append({"t": t, "font": font, "fill": fill, "sp": space})
            space = False
    return out
