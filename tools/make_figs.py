#!/usr/bin/env python3
"""해설서 그림을 모두 만든다: python tools/make_figs.py  →  figs/*.svg

1) 상자·화살표 도식은 svglib 로 직접 그린다 (글자가 그대로 남아 선명함).
2) 수치 그래프는 matplotlib 로 그린다. 글자는 윤곽선(path)으로 바꿔 글꼴이 없어도 보이게 한다.
수치는 모두 논문 표·식 또는 code/ex*.py 실행 결과에서 가져온다.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from svglib import C, Svg, WARN  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "figs"
OUT.mkdir(exist_ok=True)

CHAPTERS = [
    ("01", "초록", "논문 한눈에"), ("02", "§1", "서론"), ("03", "§2", "배경"),
    ("04", "§3·3.1", "전체 구조"), ("05", "§3.2", "어텐션"), ("06", "§3.3–3.5", "FFN·임베딩·위치"),
    ("07", "§4", "왜 셀프 어텐션"), ("08", "§5", "학습"), ("09", "§6", "결과"),
    ("10", "§7·부록", "결론과 그 뒤"),
]


# ─────────────────────────────────────────────────────────────
# 장마다 첫머리에 넣는 '전체 지도': 논문 순서 10칸 중 지금 장을 강조
# ─────────────────────────────────────────────────────────────
def chapter_map(cur):
    s = Svg(f"z{cur}_map", 780, 196)
    s.text(14, 20, "논문 순서대로 읽는 10개 장", 14, C["ink3"], 600, anchor="start")
    bw, bh, gap = 140, 62, 13
    for i, (no, sec, name) in enumerate(CHAPTERS):
        r, c = divmod(i, 5)
        x, y = 14 + c * (bw + gap), 38 + r * (bh + 22)
        on = no == cur
        s.rect(x, y, bw, bh, C["soft"] if on else "#fff", C["accent"] if on else C["line"],
               8, 2.6 if on else 1.2)
        s.text(x + 12, y + 18, no, 13, C["accent"], 700, anchor="start", mono=True)
        s.text(x + bw - 10, y + 18, sec, 11.5, C["ink3"], 500, anchor="end")
        s.text(x + bw / 2, y + 42, name, 14.5, C["ink"] if on else C["ink2"], 700 if on else 500)
        if c < 4:
            s.arrow(x + bw + 1, y + bh / 2, x + bw + gap - 1, y + bh / 2, color=C["line"], sw=1.4)
    s.line([(14 + 4 * 153 + 70, 38 + bh), (14 + 4 * 153 + 70, 38 + bh + 11),
            (14 + 70, 38 + bh + 11), (14 + 70, 38 + bh + 21)], color=C["line"], sw=1.4)
    s.save(OUT)


# ─────────────────────────────────────────────────────────────
# 1장
# ─────────────────────────────────────────────────────────────
def f01_seq_vs_parallel():
    s = Svg("f01_seq_vs_parallel", 780, 350)
    toks = ["x1", "x2", "x3", "x4", "x5"]
    # 위: 순환 모델
    s.text(20, 20, "① 순환 모델(RNN): 한 칸씩 차례로", 16, C["ink"], 700, anchor="start")
    for i, t in enumerate(toks):
        x = 60 + i * 140
        s.box(x, 66, 70, 40, f"h{i + 1}", C["gray"], C["gray_s"], mono=True)
        s.box(x + 10, 132, 50, 30, t, "#fff", C["line"], 13, mono=True)
        s.arrow(x + 35, 132, x + 35, 108)
        if i:
            s.arrow(x - 70, 86, x - 2, 86, color=C["red"])
        s.badge(x + 35, 50, str(i + 1), C["red"], size=11)
    s.text(390, 182, "앞 칸 계산이 끝나야 다음 칸을 시작합니다 → 5번 기다림", 14, C["red"], 600)
    # 아래: Transformer
    s.text(20, 216, "② Transformer: 모든 칸을 한꺼번에", 16, C["ink"], 700, anchor="start")
    xs = [95 + i * 140 for i in range(5)]
    for i, a in enumerate(xs):
        for b in xs[i + 1:]:
            mid = (a + b) / 2
            s.raw(f'<path d="M {a} 264 Q {mid} {256 - (b - a) * 0.06} {b} 264" fill="none" '
                  f'stroke="{C["accent"]}" stroke-width="1.3" opacity="0.55"/>')
    for i, x in enumerate(xs):
        s.box(x - 35, 264, 70, 40, toks[i], C["soft"], C["accent"], mono=True)
    s.text(390, 328, "모든 쌍을 한 번에 비교합니다 → 기다림 없이 병렬 계산", 14, C["accent"], 600)
    s.save(OUT)


def f01_results():
    s = Svg("f01_results", 780, 200)
    cards = [
        ("28.4", "BLEU · 영어→독일어", "앙상블 포함 기존 최고보다 2 이상 높음"),
        ("41.8", "BLEU · 영어→프랑스어", "단일 모델 최고 기록 (본문 6.1절은 41.0)"),
        ("3.5일", "GPU 8장 학습 시간", "big 모델 · 기존 모델 비용의 일부"),
        ("91.3 / 92.7", "영어 구문 분석 F1", "번역 말고 다른 과제에도 통함"),
    ]
    for i, (big, what, note) in enumerate(cards):
        x = 12 + i * 192
        s.rect(x, 14, 180, 170, "#fff", C["line"], 10, 1.4)
        s.rect(x, 14, 180, 8, C["accent"], C["accent"], 3, 0.1)
        s.text(x + 90, 70, big, 30 if len(big) < 6 else 23, C["accent"], 700)
        s.text(x + 90, 114, what, 13.5, C["ink"], 600)
        words = note.split(" · ") if " · " in note else [note]
        if len(words) == 1 and len(note) > 14:
            cut = note.rfind(" ", 0, 15)
            words = [note[:cut], note[cut + 1:]]
        for j, w in enumerate(words):
            s.text(x + 90, 144 + j * 19, w, 12, C["ink3"])
    s.save(OUT)


# ─────────────────────────────────────────────────────────────
# 2장
# ─────────────────────────────────────────────────────────────
def f02_rnn_chain():
    s = Svg("f02_rnn_chain", 780, 250)
    n = 6
    for i in range(n):
        x = 40 + i * 120
        lab = "h0" if i == 0 else ("ht" if i == n - 1 else f"h{i}")
        s.box(x, 60, 74, 46, lab, C["gray"], C["gray_s"], 16, mono=True)
        if i:
            s.arrow(x - 46, 83, x - 2, 83, color=C["red"], sw=2.2)
            xl = "xt" if i == n - 1 else f"x{i}"
            s.box(x + 12, 150, 50, 32, xl, "#fff", C["line"], 13, mono=True)
            s.arrow(x + 37, 150, x + 37, 108)
    s.text(390, 30, "ht = f( ht−1 , xt ) : 앞 상태와 지금 입력으로 다음 상태를 만든다", 15, C["ink"], 600)
    s.text(390, 214, "같은 문장 안에서는 h1 → h2 → … 순서를 건너뛸 수 없다 (병렬 불가)", 14, C["red"], 600)
    s.text(390, 236, "문장이 길수록 기다림이 길고, 메모리 때문에 여러 문장을 한꺼번에 묶기도 어렵다", 13, C["ink3"])
    s.save(OUT)


def f02_attention_rnn():
    s = Svg("f02_attention_rnn", 780, 250)
    # 왼쪽: 2017년 전 (RNN + 어텐션)
    s.rect(14, 14, 366, 222, C["paper"], C["line"], 10, 1.2)
    s.text(197, 38, "2017년 전: RNN + 어텐션", 15, C["ink"], 700)
    for i in range(4):
        x = 34 + i * 86
        s.box(x, 110, 60, 38, f"h{i + 1}", C["gray"], C["gray_s"], 13, mono=True)
        if i:
            s.arrow(x - 26, 129, x - 2, 129, color=C["red"])
    s.box(127, 182, 140, 36, "어텐션", C["attn"], C["attn_s"], 14)
    for i in range(4):
        s.arrow(64 + i * 86, 150, 197, 182, color=C["attn_s"], sw=1.2)
    s.text(197, 70, "뼈대는 여전히 차례 계산", 13, C["red"], 600)
    # 오른쪽: Transformer
    s.rect(400, 14, 366, 222, C["soft"], C["accent"], 10, 1.4)
    s.text(583, 38, "이 논문: 어텐션만", 15, C["accent"], 700)
    for i in range(4):
        x = 420 + i * 86
        s.box(x, 110, 60, 38, f"x{i + 1}", "#fff", C["accent"], 13, mono=True)
    s.box(493, 182, 180, 36, "셀프 어텐션", C["attn"], C["attn_s"], 14)
    for i in range(4):
        s.arrow(450 + i * 86, 150, 583, 182, color=C["attn_s"], sw=1.2)
    s.text(583, 70, "순환을 빼고 어텐션이 뼈대", 13, C["accent"], 600)
    s.save(OUT)


# ─────────────────────────────────────────────────────────────
# 3장
# ─────────────────────────────────────────────────────────────
def f03_path_ops():
    s = Svg("f03_path_ops", 780, 330)
    s.text(390, 20, "위치 1과 위치 9를 잇는 데 필요한 계산 단계 (개념도)", 15, C["ink"], 700)
    rows = [
        ("ConvS2S", "거리에 비례 (선형)", [(1, 3), (3, 5), (5, 7), (7, 9)], C["red"]),
        ("ByteNet", "거리의 로그에 비례", [(1, 2), (2, 4), (4, 9)], C["attn_s"]),
        ("Transformer", "거리와 상관없이 1단계", [(1, 9)], C["accent"]),
    ]
    for r, (name, rule, hops, col) in enumerate(rows):
        y = 70 + r * 92
        s.text(16, y + 20, name, 15, C["ink"], 700, anchor="start")
        s.text(16, y + 42, rule, 12.5, col, 600, anchor="start")
        for p in range(1, 10):
            x = 170 + (p - 1) * 66
            on = p in (1, 9)
            s.circle(x, y + 50, 13, C["soft"] if on else "#fff", C["accent"] if on else C["line"], 1.4)
            s.text(x, y + 51, str(p), 12, C["ink2"], 600)
        for a, b in hops:
            xa, xb = 170 + (a - 1) * 66, 170 + (b - 1) * 66
            mid = (xa + xb) / 2
            hgt = y + 34 - min(30, (b - a) * 5)
            s.raw(f'<path d="M {xa} {y + 37} Q {mid} {hgt - 10} {xb - 4} {y + 37}" fill="none" '
                  f'stroke="{col}" stroke-width="2.2" marker-end="url(#ah{col.lstrip("#")})"/>')
            s._mid(col)
        s.text(764, y + 50, f"{len(hops)}단계", 14, col, 700, anchor="end")
    s.save(OUT)


# ─────────────────────────────────────────────────────────────
# 4장
# ─────────────────────────────────────────────────────────────
def f04_encdec():
    s = Svg("f04_encdec", 780, 250)
    s.text(16, 22, "번역 예: 영어 문장 → 독일어 문장", 14, C["ink3"], 600, anchor="start")
    for i, t in enumerate(["I", "love", "you"]):
        s.box(16, 50 + i * 44, 70, 34, t, "#fff", C["line"], 14)
        s.arrow(88, 67 + i * 44, 118, 67 + i * 44)
    s.box(120, 50, 150, 122, "인코더", C["ffn"], C["ffn_s"], 18, sub="(x1 … xn) → z")
    for i in range(3):
        s.box(300, 50 + i * 44, 64, 34, f"z{i + 1}", C["soft"], C["accent"], 14, mono=True)
        s.arrow(272, 67 + i * 44, 298, 67 + i * 44)
    s.box(420, 50, 150, 122, "디코더", C["attn"], C["attn_s"], 18, sub="z 와 앞서 만든 y")
    s.arrow(366, 111, 418, 111)
    outs = ["Ich", "liebe", "dich"]
    for i, t in enumerate(outs):
        s.box(620, 50 + i * 44, 80, 34, t, "#fff", C["line"], 14)
        s.badge(718, 67 + i * 44, str(i + 1), size=11)
    s.arrow(572, 111, 618, 111)
    # 자기회귀 되먹임
    s.line([(660, 186), (660, 212), (495, 212), (495, 174)], color=C["red"], sw=2)
    s.text(578, 230, "만든 단어를 다시 넣어 다음 단어를 만든다 (자기회귀)", 13, C["red"], 600)
    s.text(195, 200, "입력 전체를 한꺼번에 읽음", 13, C["ffn_s"], 600)
    s.save(OUT)


def f04_arch_ko():
    """원문 그림 1을 한글 이름으로 다시 그린 개념도."""
    s = Svg("f04_arch_ko", 780, 700)
    # 인코더
    ex, dx, bw = 90, 430, 210
    s.rect(ex - 20, 300, bw + 40, 250, C["paper"], C["ink2"], 12, 1.6)
    s.text(ex - 34, 425, "N=6", 15, C["ink"], 700, anchor="end")
    s.text(ex + bw / 2, 286, "인코더 층 (같은 층 6개)", 14, C["ffn_s"], 700)
    s.box(ex, 480, bw, 48, "멀티헤드 셀프 어텐션", C["attn"], C["attn_s"], 14)
    s.box(ex, 444, bw, 28, "더하기 & 정규화", C["norm"], C["norm_s"], 13)
    s.box(ex, 360, bw, 48, "피드포워드 (FFN)", C["ffn"], C["ffn_s"], 14)
    s.box(ex, 324, bw, 28, "더하기 & 정규화", C["norm"], C["norm_s"], 13)
    s.arrow(ex + bw / 2, 528 + 22, ex + bw / 2, 530)
    s.arrow(ex + bw / 2, 480, ex + bw / 2, 474)
    s.arrow(ex + bw / 2, 444, ex + bw / 2, 410)
    s.arrow(ex + bw / 2, 360, ex + bw / 2, 354)
    # 잔차
    s.line([(ex + bw / 2, 541), (ex - 10, 541), (ex - 10, 458), (ex - 2, 458)], color=C["norm_s"], sw=1.5)
    s.line([(ex + bw / 2, 420), (ex - 10, 420), (ex - 10, 338), (ex - 2, 338)], color=C["norm_s"], sw=1.5)
    # 인코더 입력
    s.box(ex + 30, 620, bw - 60, 40, "입력 임베딩", C["emb"], C["emb_s"], 14)
    s.circle(ex + bw / 2, 584, 11)
    s.text(ex + bw / 2, 585, "+", 18, C["ink"], 700)
    s.text(ex - 6, 584, "위치 인코딩", 12.5, C["ink2"], 600, anchor="end")
    s.arrow(ex - 2, 584, ex + bw / 2 - 12, 584, color=C["ink3"], sw=1.3)
    s.arrow(ex + bw / 2, 620, ex + bw / 2, 597)
    s.arrow(ex + bw / 2, 573, ex + bw / 2, 551)
    s.text(ex + bw / 2, 684, "입력 문장 (영어)", 13, C["ink2"], 600)
    s.arrow(ex + bw / 2, 674, ex + bw / 2, 662)
    # 디코더
    s.rect(dx - 20, 150, bw + 40, 400, C["paper"], C["ink2"], 12, 1.6)
    s.text(dx + bw + 34, 360, "N=6", 15, C["ink"], 700, anchor="start")
    s.text(dx - 30, 160, "디코더 층 (같은 층 6개)", 14, C["attn_s"], 700, anchor="end")
    s.box(dx, 480, bw, 48, "가린 멀티헤드\n셀프 어텐션", C["attn"], C["attn_s"], 13.5)
    s.box(dx, 444, bw, 28, "더하기 & 정규화", C["norm"], C["norm_s"], 13)
    s.box(dx, 330, bw, 48, "멀티헤드 어텐션\n(인코더-디코더)", C["attn"], C["attn_s"], 13.5)
    s.box(dx, 294, bw, 28, "더하기 & 정규화", C["norm"], C["norm_s"], 13)
    s.box(dx, 210, bw, 48, "피드포워드 (FFN)", C["ffn"], C["ffn_s"], 14)
    s.box(dx, 174, bw, 28, "더하기 & 정규화", C["norm"], C["norm_s"], 13)
    cx = dx + bw / 2
    for y1, y2 in ((550, 530), (480, 474), (444, 380), (330, 324), (294, 260), (210, 204)):
        s.arrow(cx, y1, cx, y2)
    for ya, yb in ((541, 458), (420, 308), (272, 188)):
        s.line([(cx, ya), (dx + bw + 10, ya), (dx + bw + 10, yb), (dx + bw + 2, yb)],
               color=C["norm_s"], sw=1.5)
    # 인코더 출력 → 디코더 중간
    s.line([(ex + bw / 2, 324), (ex + bw / 2, 312), (345, 312), (345, 400),
            (dx + 40, 400), (dx + 40, 381)], color=C["accent"], sw=2.2)
    s.text(392, 290, "인코더 출력 z → K, V", 13, C["accent"], 700, anchor="end")
    # 디코더 입력
    s.box(dx + 30, 620, bw - 60, 40, "출력 임베딩", C["emb"], C["emb_s"], 14)
    s.circle(cx, 584, 11)
    s.text(cx, 585, "+", 18, C["ink"], 700)
    s.text(dx + bw + 6, 584, "위치 인코딩", 12.5, C["ink2"], 600, anchor="start")
    s.arrow(dx + bw + 2, 584, cx + 12, 584, color=C["ink3"], sw=1.3)
    s.arrow(cx, 620, cx, 597)
    s.arrow(cx, 573, cx, 551)
    s.text(cx, 684, "지금까지의 출력 (한 칸 밀림)", 13, C["ink2"], 600)
    s.arrow(cx, 674, cx, 662)
    # 맨 위
    s.box(dx + 40, 92, bw - 80, 30, "Linear", C["lin"], C["lin_s"], 14)
    s.box(dx + 40, 50, bw - 80, 30, "Softmax", C["soft_g"], C["soft_g_s"], 14)
    s.arrow(cx, 174, cx, 124)
    s.arrow(cx, 92, cx, 82)
    s.arrow(cx, 50, cx, 34)
    s.text(cx, 20, "다음 단어 확률", 13, C["ink2"], 600)
    s.save(OUT)


def f04_sublayer():
    s = Svg("f04_sublayer", 780, 200)
    s.box(20, 76, 70, 44, "x", "#fff", C["line"], 18, mono=True)
    s.box(150, 76, 190, 44, "Sublayer(x)", C["attn"], C["attn_s"], 15, mono=True)
    s.text(245, 140, "어텐션 또는 FFN", 12.5, C["ink3"])
    s.circle(400, 98, 16)
    s.text(400, 99, "+", 22, C["ink"], 700)
    s.box(460, 76, 150, 44, "LayerNorm", C["norm"], C["norm_s"], 15, mono=True)
    s.box(670, 76, 90, 44, "출력", "#fff", C["line"], 15)
    s.arrow(92, 98, 148, 98)
    s.arrow(342, 98, 382, 98)
    s.arrow(418, 98, 458, 98)
    s.arrow(612, 98, 668, 98)
    s.line([(120, 98), (120, 40), (400, 40), (400, 80)], color=C["accent"], sw=2.2)
    s.text(260, 28, "잔차 연결: x 를 그대로 옆길로 보내 더함", 13.5, C["accent"], 700)
    s.text(390, 178, "출력 = LayerNorm( x + Sublayer(x) )   ·   모든 값의 폭 d_model = 512", 15, C["ink"], 600)
    s.save(OUT)


def f04_shift():
    s = Svg("f04_shift", 780, 236)
    labels_in = ["〈시작〉", "Ich", "liebe", "dich"]
    labels_out = ["Ich", "liebe", "dich", "〈끝〉"]
    s.text(16, 40, "디코더 입력", 14, C["ink2"], 700, anchor="start")
    s.text(16, 40 + 28, "(한 칸 오른쪽으로 밂)", 11.5, C["ink3"], anchor="start")
    s.text(16, 176, "맞혀야 할 답", 14, C["ink2"], 700, anchor="start")
    for i in range(4):
        x = 190 + i * 140
        s.box(x, 32, 110, 42, labels_in[i], C["emb"], C["emb_s"], 15)
        s.box(x, 156, 110, 42, labels_out[i], C["soft_g"], C["soft_g_s"], 15)
        s.arrow(x + 55, 76, x + 55, 154)
        s.text(x + 55, 18, f"위치 {i + 1}", 12, C["ink3"], 600)
    s.text(470, 222, "위치 i 의 답은 i 보다 앞에 있는 출력만 보고 맞힌다 (한 칸 밀기 + 뒤 가리기)", 13.5, C["red"], 600)
    s.save(OUT)


# ─────────────────────────────────────────────────────────────
# 5장
# ─────────────────────────────────────────────────────────────
def f05_lookup():
    s = Svg("f05_lookup", 780, 290)
    s.box(20, 110, 110, 52, "쿼리 q", C["soft"], C["accent"], 16, sub="무엇을 찾나")
    keys = [("키 k1", "값 v1", 0.70), ("키 k2", "값 v2", 0.20), ("키 k3", "값 v3", 0.10)]
    for i, (k, v, w) in enumerate(keys):
        y = 30 + i * 84
        s.box(210, y, 96, 50, k, C["norm"], C["norm_s"], 15, sub="명찰")
        s.box(340, y, 96, 50, v, C["ffn"], C["ffn_s"], 15, sub="내용")
        s.arrow(132, 136, 208, y + 25, color=C["accent"], sw=1.4)
        s.text(498, y + 25, f"× {w:.2f}", 16, C["attn_s"], 700)
        s.arrow(438, y + 25, 470, y + 25, color=C["line"])
        s.arrow(530, y + 25, 600, 136, color=C["attn_s"], sw=1 + w * 4)
    s.text(498, 270, "q 와 각 k 가 잘 맞는 정도 → 비율 (합 1)", 12.5, C["attn_s"], 600)
    s.box(604, 110, 160, 52, "출력", C["attn"], C["attn_s"], 16, sub="값들의 가중합")
    s.save(OUT)


def _grid(s, x, y, m, title, cell=46, fmt="{:.2f}", shade=None, masked=None, size=13):
    s.text(x + cell * m.shape[1] / 2, y - 14, title, 13, C["ink"], 700)
    for r in range(m.shape[0]):
        for c in range(m.shape[1]):
            v = m[r, c]
            fill = "#fff"
            if masked is not None and masked[r, c]:
                fill = "#D9DAD5"
            elif shade is not None:
                a = max(0.0, min(1.0, float(v) / shade))
                fill = f"rgba(70,53,177,{0.08 + 0.55 * a:.2f})"
            s.raw(f'<rect x="{x + c * cell}" y="{y + r * cell}" width="{cell}" height="{cell}" '
                  f'fill="{fill}" stroke="{C["line"]}" stroke-width="1"/>')
            txt = "−∞" if np.isinf(v) else fmt.format(v)
            s.text(x + c * cell + cell / 2, y + r * cell + cell / 2, txt, size, C["ink"], 500, mono=True)


def f05_sdpa_steps():
    Q = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 1, 0, 0]], float)
    K = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 1, 1, 1]], float)
    sc = Q @ K.T
    scl = sc / 2
    e = np.exp(scl - scl.max(1, keepdims=True))
    w = e / e.sum(1, keepdims=True)
    s = Svg("f05_sdpa_steps", 780, 260)
    cell = 44
    xs = [20, 222, 424]
    _grid(s, xs[0], 60, sc, "① MatMul: QKᵀ", cell, "{:.0f}")
    _grid(s, xs[1], 60, scl, "② Scale: ÷√dk (=2)", cell, "{:.1f}")
    _grid(s, xs[2], 60, w, "③ SoftMax (행 합 1)", cell, "{:.2f}", shade=0.5, size=12)
    for x in xs[:2]:
        s.arrow(x + 3 * cell + 8, 126, x + 3 * cell + 62, 126, color=C["accent"], sw=2.2)
    s.arrow(xs[2] + 3 * cell + 8, 126, 620, 126, color=C["accent"], sw=2.2)
    s.box(622, 90, 146, 72, "④ MatMul\n가중치 × V", C["attn"], C["attn_s"], 14)
    s.text(390, 222, "행 = 쿼리(읽는 위치) · 열 = 키(참고할 위치). 셋째 행은 k3 을 가장 많이(0.45) 참고", 13.5,
           C["ink2"], 600)
    s.text(390, 246, "숫자는 code/ex05_scaled_dot_product.py 실행 결과", 12, C["ink3"])
    s.save(OUT)


def f05_mask():
    sc = np.array([[0.5, 1, 2], [1, 0.5, 1], [2, 1, 0.5]])
    fut = np.triu(np.ones((3, 3), bool), 1)
    mk = np.where(fut, -np.inf, sc)
    e = np.exp(mk - mk.max(1, keepdims=True))
    w = e / e.sum(1, keepdims=True)
    s = Svg("f05_mask", 780, 250)
    cell = 52
    _grid(s, 30, 58, sc, "가리기 전 점수", cell, "{:.1f}")
    _grid(s, 290, 58, mk, "미래 칸을 −∞ 로", cell, "{:.1f}", masked=fut)
    _grid(s, 550, 58, w, "SoftMax 뒤 가중치", cell, "{:.2f}", shade=1.0, masked=fut)
    s.arrow(30 + 3 * cell + 10, 136, 280, 136, color=C["accent"], sw=2.2)
    s.arrow(290 + 3 * cell + 10, 136, 540, 136, color=C["accent"], sw=2.2)
    s.text(390, 232, "e^(−∞) = 0 이므로 회색 칸(자기보다 뒤)의 가중치는 정확히 0", 14, C["red"], 600)
    s.save(OUT)


def f05_mha():
    s = Svg("f05_mha", 780, 380)
    s.box(20, 160, 110, 56, "입력", "#fff", C["line"], 15, sub="512칸")
    heads = 8
    for i in range(heads):
        y = 22 + i * 42
        if i == 6:
            continue
        lab = f"헤드 {heads if i == 7 else i + 1}"
        if i == 5:
            s.text(396, y + 30, "⋮", 22, C["ink3"], 700)
            continue
        s.box(180, y, 120, 32, "Q·K·V 투영", C["lin"], C["lin_s"], 12.5)
        s.box(326, y, 140, 32, f"{lab} 어텐션", C["attn"], C["attn_s"], 12.5)
        s.text(492, y + 16, "64칸", 12, C["ink3"], 600)
        s.arrow(132, 188, 178, y + 16, color=C["line"], sw=1.2)
        s.arrow(302, y + 16, 324, y + 16, sw=1.3)
        s.arrow(512, y + 16, 548, 188, color=C["line"], sw=1.2)
    s.box(550, 150, 96, 76, "Concat\n(이어 붙임)", "#FFF6C9", "#B98300", 13.5, sub="8×64=512")
    s.box(670, 160, 96, 56, "Wᴼ\n투영", C["lin"], C["lin_s"], 13.5)
    s.arrow(648, 188, 668, 188)
    s.text(390, 368, "h = 8 · dk = dv = 512 / 8 = 64 · 헤드마다 다른 투영 가중치를 배운다", 14, C["ink"], 600)
    s.save(OUT)


def f05_three_uses():
    s = Svg("f05_three_uses", 780, 300)
    panels = [
        ("① 인코더 셀프 어텐션", "Q·K·V: 인코더 앞 층", "모든 위치를 봄", "enc"),
        ("② 디코더 셀프 어텐션", "Q·K·V: 디코더 앞 층", "자기와 앞만 봄 (마스크)", "dec"),
        ("③ 인코더-디코더 어텐션", "Q: 디코더 · K·V: 인코더 출력", "입력 문장 전체를 봄", "cross"),
    ]
    for i, (t, src, see, kind) in enumerate(panels):
        x = 12 + i * 256
        s.rect(x, 12, 244, 276, C["paper"], C["line"], 10, 1.2)
        s.text(x + 122, 36, t, 14.5, C["ink"], 700)
        s.text(x + 122, 62, src, 12, C["ink2"], 600)
        s.text(x + 122, 268, see, 13, C["accent"] if kind != "dec" else C["red"], 700)
        n = 4
        top_col = C["ffn"] if kind == "enc" else C["attn"]
        bot_col = C["ffn"] if kind in ("enc", "cross") else C["attn"]
        top_s = C["ffn_s"] if kind == "enc" else C["attn_s"]
        bot_s = C["ffn_s"] if kind in ("enc", "cross") else C["attn_s"]
        for p in range(n):
            px = x + 32 + p * 56
            s.box(px - 18, 92, 36, 30, f"{p + 1}", top_col, top_s, 13, mono=True)
            s.box(px - 18, 212, 36, 30, f"{p + 1}", bot_col, bot_s, 13, mono=True)
        q = 2  # 세 번째 위치가 읽는 모습
        qx = x + 32 + q * 56
        for p in range(n):
            px = x + 32 + p * 56
            ok = not (kind == "dec" and p > q)
            s.arrow(px, 210, qx, 125, color=C["accent"] if ok else "#C9CCC4", sw=1.8 if ok else 1.2,
                    dash=None if ok else "4 4")
    s.save(OUT)


# ─────────────────────────────────────────────────────────────
# 6장
# ─────────────────────────────────────────────────────────────
def f06_ffn():
    s = Svg("f06_ffn", 780, 290)
    s.text(390, 20, "FFN(x) = max(0, x·W1 + b1)·W2 + b2", 16, C["ink"], 700, mono=True)
    for p in range(4):
        x = 30 + p * 190
        s.box(x, 236, 140, 36, f"위치 {p + 1} · 512", "#fff", C["line"], 13)
        s.box(x, 172, 140, 34, "W1 : 512 → 2048", C["ffn"], C["ffn_s"], 12.5)
        s.box(x + 20, 122, 100, 30, "ReLU", "#FFF6C9", "#B98300", 12.5)
        s.box(x, 68, 140, 34, "W2 : 2048 → 512", C["ffn"], C["ffn_s"], 12.5)
        s.arrow(x + 70, 236, x + 70, 208)
        s.arrow(x + 70, 172, x + 70, 154)
        s.arrow(x + 70, 122, x + 70, 104)
        s.arrow(x + 70, 68, x + 70, 44)
    s.save(OUT)


def f06_share():
    s = Svg("f06_share", 780, 250)
    s.box(290, 92, 200, 70, "가중치 행렬 W", C["soft"], C["accent"], 17, sub="어휘 약 37000 × 512")
    uses = [(30, 20, "입력 임베딩", "× √512 곱함", C["emb"], C["emb_s"]),
            (30, 170, "출력 임베딩", "× √512 곱함", C["emb"], C["emb_s"]),
            (570, 92, "Softmax 앞 Linear", "512 → 어휘 점수", C["lin"], C["lin_s"])]
    for x, y, a, b, f, st in uses:
        s.box(x, y, 180, 60, a, f, st, 15, sub=b)
    s.arrow(288, 115, 212, 52, color=C["accent"], sw=2)
    s.arrow(288, 140, 212, 198, color=C["accent"], sw=2)
    s.arrow(492, 127, 568, 122, color=C["accent"], sw=2)
    s.text(390, 236, "한 행렬을 세 곳에서 함께 쓴다 → 가중치 수가 줄고, 단어 표현이 한 가지로 맞춰짐", 13.5, C["ink2"], 600)
    s.save(OUT)


def f06_rotate():
    s = Svg("f06_rotate", 780, 270)
    cx, cy, r = 160, 140, 96
    s.circle(cx, cy, r, "#fff", C["line"], 1.4)
    s.arrow(cx - r - 14, cy, cx + r + 18, cy, color=C["line"], sw=1)
    s.arrow(cx, cy + r + 14, cx, cy - r - 18, color=C["line"], sw=1)
    s.text(cx + r + 26, cy + 14, "sin", 12, C["ink3"])
    s.text(cx + 18, cy - r - 22, "cos", 12, C["ink3"])
    a1, a2 = 0.55, 1.45
    import math
    p1 = (cx + r * math.sin(a1), cy - r * math.cos(a1))
    p2 = (cx + r * math.sin(a2), cy - r * math.cos(a2))
    s.arrow(cx, cy, *p1, color=C["accent"], sw=2.2)
    s.arrow(cx, cy, *p2, color=C["red"], sw=2.2)
    s.text(p1[0] + 34, p1[1] - 8, "pos", 13, C["accent"], 700, mono=True)
    s.text(p2[0] + 34, p2[1] + 4, "pos+k", 13, C["red"], 700, mono=True)
    s.raw(f'<path d="M {cx + 40 * math.sin(a1)} {cy - 40 * math.cos(a1)} A 40 40 0 0 1 '
          f'{cx + 40 * math.sin(a2)} {cy - 40 * math.cos(a2)}" fill="none" stroke="{C["attn_s"]}" stroke-width="2"/>')
    s.text(cx + 64, cy - 30, "k·ω 만큼 회전", 12.5, C["attn_s"], 700, anchor="start")
    lines = [
        "칸 한 쌍 (2i, 2i+1) = (sin(pos·ω), cos(pos·ω))",
        "위치를 k 만큼 옮기기 = 같은 각도 k·ω 만큼 돌리기",
        "돌리기는 pos 와 상관없는 고정 행렬 곱 → 선형 변환",
        "그래서 모델이 '몇 칸 떨어졌나'를 배우기 쉽다고 봄",
    ]
    for i, t in enumerate(lines):
        s.text(330, 70 + i * 42, t, 14.5, C["ink"] if i < 3 else C["accent"], 600 if i < 3 else 700,
               anchor="start")
    s.save(OUT)


def f07_restricted():
    s = Svg("f07_restricted", 780, 200)
    n, q, r = 13, 6, 5
    for p in range(n):
        x = 40 + p * 54
        inwin = abs(p - q) <= r // 2
        s.box(x, 110, 40, 36, str(p + 1), C["soft"] if inwin else "#fff",
              C["accent"] if inwin else C["line"], 13, mono=True)
        if inwin and p != q:
            s.arrow(40 + q * 54 + 20, 98, x + 20, 108, color=C["accent"], sw=1.6)
    s.box(40 + q * 54 - 10, 46, 60, 40, "읽는 위치", C["attn"], C["attn_s"], 11.5)
    s.arrow(40 + q * 54 + 20, 86, 40 + q * 54 + 20, 108, color=C["accent"], sw=1.6)
    lx = 40 + (q - r // 2) * 54 - 6
    s.rect(lx, 102, r * 54 + 2, 52, "none", C["accent"], 8, 1.6, dash="6 4")
    s.text(lx + (r * 54) / 2, 172, f"이웃 r = {r} 칸만 봄", 13.5, C["accent"], 700)
    s.text(390, 192, "계산량 O(r·n·d) 로 줄지만 먼 위치까지 경로가 O(n/r) 로 길어짐 (논문: 앞으로 연구)", 12.5, C["ink3"])
    s.save(OUT)


# ─────────────────────────────────────────────────────────────
# 8장
# ─────────────────────────────────────────────────────────────
def f08_dropout():
    s = Svg("f08_dropout", 780, 220)
    s.text(16, 22, "① 서브층마다", 14, C["ink"], 700, anchor="start")
    s.box(20, 50, 60, 40, "x", "#fff", C["line"], 16, mono=True)
    s.box(120, 50, 140, 40, "Sublayer(x)", C["attn"], C["attn_s"], 13.5, mono=True)
    s.box(296, 50, 110, 40, "Dropout", "#FDE2DC", C["red"], 14, weight=700)
    s.circle(450, 70, 14)
    s.text(450, 71, "+", 20, C["ink"], 700)
    s.box(494, 50, 130, 40, "LayerNorm", C["norm"], C["norm_s"], 14, mono=True)
    s.arrow(82, 70, 118, 70)
    s.arrow(262, 70, 294, 70)
    s.arrow(408, 70, 434, 70)
    s.arrow(466, 70, 492, 70)
    s.line([(100, 70), (100, 30), (450, 30), (450, 54)], color=C["norm_s"], sw=1.5)
    s.text(16, 136, "② 스택 맨 아래", 14, C["ink"], 700, anchor="start")
    s.box(20, 160, 130, 40, "임베딩", C["emb"], C["emb_s"], 14)
    s.box(190, 160, 130, 40, "위치 인코딩", "#fff", C["line"], 14)
    s.circle(360, 180, 14)
    s.text(360, 181, "+", 20, C["ink"], 700)
    s.box(404, 160, 110, 40, "Dropout", "#FDE2DC", C["red"], 14, weight=700)
    s.arrow(152, 180, 344, 180, color=C["line"])
    s.arrow(322, 180, 344, 180)
    s.arrow(376, 180, 402, 180)
    s.arrow(516, 180, 560, 180)
    s.text(660, 180, "인코더·디코더로", 13, C["ink2"], 600)
    s.text(700, 70, "base: Pdrop = 0.1", 14, C["red"], 700)
    s.save(OUT)


# ─────────────────────────────────────────────────────────────
# 10장
# ─────────────────────────────────────────────────────────────
def f10_family():
    s = Svg("f10_family", 780, 340)
    s.box(300, 14, 180, 56, "Transformer", C["soft"], C["accent"], 18, weight=700, sub="2017 · 인코더 + 디코더")
    cols = [
        (20, "인코더만 사용", "이해: 분류·검색·임베딩", C["ffn"], C["ffn_s"],
         [("BERT", "2018"), ("RoBERTa", "2019"), ("ViT (이미지)", "2020")]),
        (280, "디코더만 사용", "생성: 다음 토큰 예측", C["attn"], C["attn_s"],
         [("GPT", "2018"), ("GPT-2", "2019"), ("GPT-3 → 오늘의 LLM", "2020~")]),
        (540, "인코더 + 디코더", "변환: 번역·요약", C["norm"], C["norm_s"],
         [("T5", "2019"), ("BART", "2019"), ("Whisper (음성)", "2022")]),
    ]
    for x, t, sub, f, st, models in cols:
        s.line([(390, 70), (390, 92), (x + 110, 92), (x + 110, 108)], color=C["ink3"], sw=1.6)
        s.box(x, 110, 220, 52, t, f, st, 15, weight=700, sub=sub)
        for j, (m, yr) in enumerate(models):
            y = 186 + j * 50
            s.rect(x + 10, y, 200, 38, "#fff", st, 8, 1.3)
            s.text(x + 22, y + 19, m, 14, C["ink"], 600, anchor="start")
            s.text(x + 200, y + 19, yr, 12, C["ink3"], 500, anchor="end", mono=True)
            if j:
                s.arrow(x + 110, y - 12, x + 110, y - 1, color=st, sw=1.4)
            else:
                s.arrow(x + 110, 162, x + 110, y - 1, color=st, sw=1.4)
    s.save(OUT)


# ─────────────────────────────────────────────────────────────
# matplotlib 그래프
# ─────────────────────────────────────────────────────────────
def mpl_setup():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for f in font_manager.findSystemFonts():
        if "NotoSansCJK-Regular" in f or "NotoSansCJKkr-Regular" in f:
            font_manager.fontManager.addfont(f)
    plt.rcParams.update({
        "font.family": ["Noto Sans CJK JP", "Noto Sans CJK KR", "DejaVu Sans"],
        "svg.fonttype": "path", "axes.unicode_minus": False, "font.size": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#8A8F98", "axes.labelcolor": C["ink"],
        "xtick.color": C["ink2"], "ytick.color": C["ink2"], "svg.hashsalt": "tf",
    })
    return plt


def savefig(plt, fig, name):
    fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)


def m05_softmax(plt):
    rng = np.random.default_rng(0)
    for d in (4, 64, 512):     # ex05_variance.py 와 같은 난수 순서를 따라감
        rng.standard_normal((100_000, d))
        rng.standard_normal((100_000, d))
    sc = rng.standard_normal(8) * 8

    def sm(x):
        e = np.exp(x - x.max())
        return e / e.sum()

    fig, ax = plt.subplots(1, 2, figsize=(9, 2.9), sharey=True)
    for a, w, t, col in ((ax[0], sm(sc), "나누지 않은 점수 → 한 칸에 몰림", C["red"]),
                         (ax[1], sm(sc / 8), "√dk 로 나눈 점수 → 고르게 퍼짐", C["accent"])):
        a.bar(range(1, 9), w, color=col)
        a.set_title(t, fontsize=12, color=C["ink"])
        a.set_xticks(range(1, 9))
        a.set_xlabel("키 위치")
        a.set_ylim(0, 1.05)
    ax[0].set_ylabel("softmax 가중치")
    savefig(plt, fig, "m05_softmax")


def m06_pe(plt):
    d, P = 128, 64
    pos = np.arange(P)[:, None]
    i = np.arange(d // 2)[None, :]
    ang = pos / 10000 ** (2 * i / 512)
    pe = np.zeros((P, d))
    pe[:, 0::2], pe[:, 1::2] = np.sin(ang), np.cos(ang)
    fig, ax = plt.subplots(figsize=(9, 3.6))
    im = ax.imshow(pe, aspect="auto", cmap="PuOr", vmin=-1, vmax=1)
    ax.set_xlabel("칸 번호 (d_model = 512 중 앞 128칸)")
    ax.set_ylabel("위치 pos")
    ax.set_title("사인·코사인 위치 인코딩: 왼쪽 칸은 빨리, 오른쪽 칸은 천천히 바뀐다", fontsize=12)
    fig.colorbar(im, ax=ax, fraction=0.03)
    savefig(plt, fig, "m06_pe")


def m07_complexity(plt):
    d = 512
    n = np.array([10, 30, 100, 300, 512, 1000, 3000])
    fig, ax = plt.subplots(figsize=(8.4, 3.4))
    ax.plot(n, n * n * d, "o-", color=C["accent"], label="셀프 어텐션  n²·d")
    ax.plot(n, n * d * d, "s-", color=C["red"], label="순환층  n·d²")
    ax.axvline(512, color="#8A8F98", ls="--", lw=1)
    ax.text(530, 3e6, "n = d = 512 에서 같음", color=C["ink2"])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("문장 길이 n (토큰 수)")
    ax.set_ylabel("층 하나의 계산량")
    ax.set_title("d = 512 일 때: n < d 이면 셀프 어텐션이 더 적게 계산", fontsize=12)
    ax.legend(frameon=False)
    savefig(plt, fig, "m07_complexity")


def m08_lrate(plt):
    st = np.arange(1, 100001)
    lr = 512 ** -0.5 * np.minimum(st ** -0.5, st * 4000 ** -1.5)
    fig, ax = plt.subplots(figsize=(8.4, 3.2))
    ax.plot(st, lr * 1e3, color=C["accent"], lw=2)
    ax.axvline(4000, color=C["red"], ls="--", lw=1)
    ax.annotate("warmup_steps = 4000\n최고 7.0×10⁻⁴", xy=(4000, 0.699), xytext=(16000, 0.62),
                arrowprops=dict(arrowstyle="->", color=C["red"]), color=C["red"])
    ax.text(60000, 0.24, "그 뒤 1/√step 로 줄어듦", color=C["ink2"])
    ax.set_xlabel("학습 단계 step (base: 100,000단계)")
    ax.set_ylabel("학습률 (×10⁻³)")
    savefig(plt, fig, "m08_lrate")


def m09_bleu(plt):
    rows = [("ByteNet", 23.75, None), ("GNMT + RL", 24.6, 2.3e19), ("ConvS2S", 25.16, 9.6e18),
            ("MoE", 26.03, 2.0e19), ("GNMT + RL 앙상블", 26.30, 1.8e20), ("ConvS2S 앙상블", 26.36, 7.7e19),
            ("Transformer base", 27.3, 3.3e18), ("Transformer big", 28.4, 2.3e19)]
    names = [r[0] for r in rows]
    cols = [C["accent"] if "Transformer" in n else "#B9BCC4" for n in names]
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.6), gridspec_kw={"width_ratios": [1.15, 1]})
    ax[0].barh(names, [r[1] for r in rows], color=cols)
    ax[0].set_xlim(22, 29)
    ax[0].set_xlabel("BLEU (영어→독일어, 높을수록 좋음)")
    for i, r in enumerate(rows):
        ax[0].text(r[1] + 0.08, i, f"{r[1]}", va="center", fontsize=10)
    have = [r for r in rows if r[2]]
    ax[1].barh([r[0] for r in have], [r[2] for r in have],
               color=[C["accent"] if "Transformer" in r[0] else "#B9BCC4" for r in have])
    ax[1].set_xscale("log")
    ax[1].set_xlabel("학습 비용 FLOPs (로그 눈금, 낮을수록 좋음)")
    ax[1].set_yticklabels([])
    fig.suptitle("표 2 영어→독일어: 더 높은 점수를 더 적은 비용으로", fontsize=12.5)
    fig.tight_layout()
    savefig(plt, fig, "m09_bleu")


def m09_heads(plt):
    h = [1, 4, 8, 16, 32]
    bleu = [24.9, 25.5, 25.8, 25.8, 25.4]
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    ax.plot(h, bleu, "o-", color=C["accent"], lw=2)
    for x, y in zip(h, bleu):
        ax.text(x, y + 0.08, f"{y}", ha="center")
    ax.set_xscale("log", base=2)
    ax.set_xticks(h, [f"h={x}\ndk={512 // x}" for x in h])
    ax.set_ylim(24.6, 26.2)
    ax.set_ylabel("BLEU (dev)")
    ax.set_title("표 3 (A): 계산량은 그대로 두고 헤드 수만 바꿈", fontsize=12)
    savefig(plt, fig, "m09_heads")


def main():
    for no, _, _ in CHAPTERS:
        chapter_map(no)
    for f in (f01_seq_vs_parallel, f01_results, f02_rnn_chain, f02_attention_rnn, f03_path_ops,
              f04_encdec, f04_arch_ko, f04_sublayer, f04_shift, f05_lookup, f05_sdpa_steps, f05_mask,
              f05_mha, f05_three_uses, f06_ffn, f06_share, f06_rotate, f07_restricted, f08_dropout,
              f10_family):
        f()
    plt = mpl_setup()
    for f in (m05_softmax, m06_pe, m07_complexity, m08_lrate, m09_heads, m09_bleu):
        f(plt)
    print("그림", len(list(OUT.glob("*.svg"))), "개")
    if WARN:
        print("경고", len(WARN), "건")
        for w in WARN:
            print("  ", w)


if __name__ == "__main__":
    main()
