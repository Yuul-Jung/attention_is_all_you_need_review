#!/usr/bin/env python3
"""논문 큰 그림(1페이지)을 svg-flow-editor JSON 형식으로 만든다.

출력: diagrams/bigpicture_pages.json  (편집기 '불러오기'로 열어 고칠 수 있음)
SVG 는 tools/export_editor_svg.py 가 편집기에서 직접 내보낸다.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "diagrams"
OUT.mkdir(exist_ok=True)

ROWS = [  # (단계, 원문 위치, 핵심, 숫자·근거, 장)
    ("제안", "초록", "순환·합성곱 없이 어텐션만 쓰는 Transformer", "더 좋은 번역 · 더 짧은 학습 시간", "논문 한눈에"),
    ("문제", "§1 서론", "순환 모델은 한 칸씩 차례로 계산", "문장 안에서 병렬 계산 불가 · 어텐션도 RNN에 붙여 씀", "서론"),
    ("앞선 시도", "§2 배경", "합성곱 모델도 먼 위치를 잇는 데 여러 단계", "ConvS2S 선형 · ByteNet 로그 · Transformer 1단계", "배경"),
    ("전체 구조", "§3 · §3.1", "인코더 6층 + 디코더 6층 · 폭 512", "서브층마다 잔차 연결 + LayerNorm", "전체 구조"),
    ("어텐션", "§3.2", "softmax(QKᵀ/√dk)·V · 헤드 8개 × 64칸", "인코더 셀프 · 디코더 가린 셀프 · 인코더-디코더", "어텐션"),
    ("나머지 부품", "§3.3 · §3.4 · §3.5", "FFN 512→2048→512 · 임베딩 공유 · 사인 위치", "위치마다 같은 FFN · 순서 정보는 더해서 넣음", "FFN·임베딩·위치"),
    ("근거", "§4", "셀프 어텐션: 순차 단계 O(1) · 최대 경로 O(1)", "층 계산량 O(n²·d) · n < d 이면 순환층보다 적음", "왜 셀프 어텐션"),
    ("학습", "§5", "WMT 2014 · P100 GPU 8장 · base 12시간", "Adam + warmup 4000 · Dropout 0.1 · 스무딩 0.1", "학습"),
    ("결과", "§6", "BLEU 영→독 28.4 · 영→프 41.8", "표 3 변형 실험 · 영어 구문 분석 F1 92.7", "결과"),
    ("결론", "§7 · 부록", "어텐션만으로 번역 최고 · 다른 분야로 확장 예고", "그 뒤: BERT(인코더) · GPT(디코더) · ViT(이미지)", "결론과 그 뒤"),
]

NAVY = dict(textColor="#172439", subTextColor="#273e5e", strokeColor="#1F3A5F",
            fill="none", fontMain=23, fontSub=18, strokeWidth=3.5, preset="navy")
DARK = dict(textColor="#ffffff", subTextColor="#dceaff", strokeColor="#102944",
            fill="#1f3a5f", fontMain=23, fontSub=18, strokeWidth=3.5, preset="dark")
BLUE = dict(textColor="#163457", subTextColor="#325477", strokeColor="#205184",
            fill="#eaf3ff", fontMain=23, fontSub=18, strokeWidth=3, preset="blue")
EDGE = dict(route="auto", strokeColor="#5A1E1E", strokeWidth=3.5, arrowSize=16, labelFont=17)

X1, W1 = 190, 300     # 단계
X2, W2 = 790, 760     # 핵심 내용
X3, W3 = 1335, 230    # 해설서 장
Y0, DY, H = 196, 106, 80

nodes, edges = [], []
for i, (step, where, core, detail, ch) in enumerate(ROWS):
    y = Y0 + i * DY
    common = dict(type="rect", y=y, h=H, pad=6, padY=4, textAlign="center", autoFit=False)
    nodes.append(dict(id=f"s{i + 1}", x=X1, w=W1, title=step, sub=where, **common, **DARK))
    nodes.append(dict(id=f"c{i + 1}", x=X2, w=W2, title=core, sub=detail, **common, **NAVY))
    nodes.append(dict(id=f"g{i + 1}", x=X3, w=W3, title=f"{i + 1}장", sub=ch, **common, **BLUE))
    edges.append(dict(id=f"h{i + 1}", **{"from": f"s{i + 1}", "to": f"c{i + 1}"}, fp="right", tp="left",
                      label="", **EDGE))
    edges.append(dict(id=f"k{i + 1}", **{"from": f"c{i + 1}", "to": f"g{i + 1}"}, fp="right", tp="left",
                      label="", **EDGE))
    if i:
        edges.append(dict(id=f"v{i}", **{"from": f"s{i}", "to": f"s{i + 1}"}, fp="bottom", tp="top",
                          label="", **EDGE))

page = dict(
    version=3, chapter="AIAYN-00", verification="PAPER_TEXT_CHECKED",
    pageTitle="논문 큰 그림",
    title="Attention Is All You Need (2017) · 논문 큰 그림",
    subtitle="원문 순서 → 핵심 내용과 숫자 → 해설서 장 · 왼쪽 세로줄이 논문을 읽는 순서",
    width=1480, height=Y0 + 9 * DY + H // 2 + 34,
    headings=dict(title=dict(x=740, y=52, w=1100, h=56, size=33, align="center", autoFit=True),
                  subtitle=dict(x=740, y=102, w=1200, h=38, size=19, align="center", autoFit=True)),
    settings=dict(fontMain=23, fontSub=18, stroke=3.5, gap=40, pad=6, padY=4, defaultPreset="navy"),
    nodes=nodes, edges=edges)

doc = dict(version=3, format="soc-flow-pages", chapter="AIAYN-00", activePage=0, pages=[page])
(OUT / "bigpicture_pages.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
print("노드", len(nodes), "· 연결선", len(edges), "· 캔버스", page["width"], "x", page["height"])
