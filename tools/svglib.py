"""해설서 그림(SVG)을 만드는 작은 도구.

상자·화살표·글자만 쓰는 단순한 도식용이다. 글자 폭을 어림해 상자 밖으로
넘치면 경고를 모아 두었다가 make_figs.py 끝에서 한꺼번에 보여 준다.
"""
from html import escape

FONT = ("'IBM Plex Sans KR','Malgun Gothic','Apple SD Gothic Neo',"
        "'Noto Sans CJK KR','Noto Sans KR',sans-serif")
MONO = "'IBM Plex Mono',Consolas,'Courier New',monospace"

# 색: STANDARD 2절 강조색(보라)과 원문 그림 1의 상자 색 계열
C = {
    "ink": "#172439", "ink2": "#273E5E", "ink3": "#676D78", "line": "#C9CCC4",
    "accent": "#4635B1", "soft": "#EDEAFA", "yellow": "#FFD24A", "paper": "#F7F7F4",
    "attn": "#FCE3C7", "attn_s": "#C77A1F",      # 어텐션 (원문: 주황)
    "ffn": "#D3ECF7", "ffn_s": "#2C7DA0",        # 피드포워드 (원문: 하늘색)
    "norm": "#EEF5C6", "norm_s": "#7C8C1C",      # Add & Norm (원문: 연두)
    "emb": "#F9DCE1", "emb_s": "#B04A5E",        # 임베딩 (원문: 분홍)
    "lin": "#E1E3F3", "lin_s": "#5B5F97",        # Linear
    "soft_g": "#DDF0E1", "soft_g_s": "#3C8C55",  # Softmax
    "gray": "#EEEFEA", "gray_s": "#8A8F98",
    "navy": "#1F3A5F", "edge": "#5A1E1E",
    "red": "#B0412A", "green": "#2F7D4F",
}

WARN = []


def text_width(s, size):
    """글자 폭 어림값(px). 한글 1.0, 영문·숫자 0.58, 공백 0.3 배."""
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            w += 1.0
        elif ch == " ":
            w += 0.3
        elif ch in "ilj.,:;|'!·":
            w += 0.32
        elif ch in "mwMW":
            w += 0.85
        else:
            w += 0.58
    return w * size


class Svg:
    def __init__(self, name, w, h, bg="#FFFFFF"):
        self.name, self.w, self.h = name, w, h
        self.items = []
        if bg:
            self.items.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}"/>')

    # ── 기본 요소 ──────────────────────────────────────────
    def rect(self, x, y, w, h, fill="#fff", stroke=None, rx=3, sw=1.8, dash=None):
        st = stroke or C["navy"]
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                          f'fill="{fill}" stroke="{st}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=15, color=None, weight=400, anchor="middle", mono=False,
             italic=False):
        fam = MONO if mono else FONT
        it = ' font-style="italic"' if italic else ""
        self.items.append(
            f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color or C["ink"]}" text-anchor="{anchor}" dominant-baseline="middle"{it}>'
            f'{escape(s)}</text>')
        w = text_width(s, size)
        left = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        if left < -1 or left + w > self.w + 1:
            WARN.append(f"{self.name}: 글자가 그림 밖으로 나감 → '{s}'")

    def box(self, x, y, w, h, label, fill="#fff", stroke=None, size=15, color=None,
            weight=500, sub=None, sub_size=12, rx=3, sw=1.8, mono=False):
        self.rect(x, y, w, h, fill, stroke, rx, sw)
        lines = label.split("\n")
        n = len(lines) + (1 if sub else 0)
        lh = size * 1.3
        top = y + h / 2 - (n - 1) * lh / 2
        for i, ln in enumerate(lines):
            self.text(x + w / 2, top + i * lh, ln, size, color, weight, mono=mono)
            if text_width(ln, size) > w - 10:
                WARN.append(f"{self.name}: 상자 폭 부족 → '{ln}' ({text_width(ln, size):.0f} > {w - 10})")
        if sub:
            yy = top + len(lines) * lh
            self.text(x + w / 2, yy, sub, sub_size, C["ink3"], 400)
            if text_width(sub, sub_size) > w - 10:
                WARN.append(f"{self.name}: 상자 폭 부족 → '{sub}'")

    def line(self, pts, color=None, sw=2.0, arrow=True, dash=None):
        col = color or C["edge"]
        d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
        mk = f' marker-end="url(#ah{self._mid(col)})"' if arrow else ""
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        self.items.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}"'
                          f' stroke-linejoin="round"{ds}{mk}/>')

    def arrow(self, x1, y1, x2, y2, **kw):
        self.line([(x1, y1), (x2, y2)], **kw)

    def raw(self, s):
        self.items.append(s)

    _markers = {}

    def _mid(self, col):
        key = col.lstrip("#")
        self._markers[key] = col
        return key

    def circle(self, cx, cy, r, fill="#fff", stroke=None, sw=1.6):
        self.items.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
                          f'stroke="{stroke or C["ink2"]}" stroke-width="{sw}"/>')

    def badge(self, x, y, s, fill=None, color="#fff", size=13):
        """둥근 번호표 ①②… 대신 쓰는 작은 원 번호."""
        self.circle(x, y, size * 0.85, fill or C["accent"], fill or C["accent"], 1)
        self.text(x, y + 0.5, s, size, color, 700)

    def title(self, s, y=24, size=17):
        self.text(self.w / 2, y, s, size, C["ink"], 700)

    # ── 저장 ──────────────────────────────────────────────
    def save(self, folder):
        defs = "".join(
            f'<marker id="ah{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" '
            f'markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{v}"/></marker>'
            for k, v in self._markers.items())
        body = "\n".join(self.items)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
               f'viewBox="0 0 {self.w} {self.h}" role="img"><defs>{defs}</defs>\n{body}\n</svg>\n')
        (folder / f"{self.name}.svg").write_text(svg, encoding="utf-8")
        Svg._markers = {}
