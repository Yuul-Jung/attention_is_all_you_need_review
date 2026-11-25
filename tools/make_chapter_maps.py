#!/usr/bin/env python3
"""장마다 '이 장의 큰 그림'을 svg-flow-editor 다중 페이지 JSON 하나로 만든다.

출력: diagrams/chapter_maps_pages.json (10페이지, 편집기 '불러오기'로 열어 고칠 수 있음)
SVG 는 tools/export_editor_svg.py 가 페이지마다 figs/c01_bigpicture.svg … 로 내보낸다.
열 구성: 원문 위치(왼쪽) → 핵심·근거(가운데) → 해설서에서 볼 곳(오른쪽).
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "diagrams"
OUT.mkdir(exist_ok=True)

# 장: (제목, [(이름, 원문 위치, 핵심, 근거·숫자, 볼 곳 1, 볼 곳 2), ...])  — 원문 순서 그대로
CHAPTERS = [
    ("1장 · 논문 한눈에 · 초록", [
        ("논문 정보", "첫 쪽", "8명 공동 기여 · NIPS 2017 · arXiv v7", "원문 그림·표는 허락 문구에 따라 수록", "표", "기본 정보"),
        ("논문 큰 그림", "초록 ~ §7", "왜 → 무엇을 → 얼마나, 세 덩어리", "원문 순서 = 해설서 장 순서", "그림 2", "큰 그림"),
        ("초록 ①②", "초록", "순환·합성곱을 빼고 어텐션만 쓴다", "인코더·디코더 구조는 그대로", "그림 3", "차례 vs 병렬"),
        ("초록 ③④⑤", "초록", "BLEU 28.4 · 41.8 · 학습 3.5일", "구문 분석에도 통함 (F1 92.7)", "그림 4", "숫자 네 개"),
    ]),
    ("2장 · 서론 · 순환 모델의 한계", [
        ("문단 1", "§1", "당시 최고 모델: RNN · LSTM · GRU", "번역·언어 모델의 표준", "원문 요지", "문단 1"),
        ("문단 2", "§1", "ht = f(ht−1, xt) → 문장 안 병렬 불가", "긴 문장 · 메모리 한계로 더 심각", "그림 2", "차례 계산"),
        ("문단 3", "§1", "어텐션: 거리와 상관없이 연결", "그러나 RNN에 붙여서 씀", "그림 3", "2017년 전후"),
        ("문단 4", "§1", "어텐션만 쓰는 Transformer 제안", "P100 GPU 8장 · 12시간 학습", "원문 요지", "문단 4"),
    ]),
    ("3장 · 배경 · 앞선 시도들", [
        ("합성곱 모델", "§2", "병렬은 되지만 먼 위치는 여러 단계", "ConvS2S 선형 · ByteNet 로그", "그림 2", "경로 단계"),
        ("Transformer", "§2", "어느 두 위치든 1단계로 연결", "대가: 평균 흐려짐 → 멀티헤드로 보완", "그림 2", "평균 흐려짐"),
        ("셀프 어텐션", "§2", "한 시퀀스 안의 위치끼리 참고", "독해·요약·함의 판단에 이미 사용", "표", "어텐션 비교"),
        ("이 논문의 자리", "§2", "셀프 어텐션만으로 만든 첫 변환 모델", "RNN·합성곱 없이 입력·출력 표현 계산", "원문 요지", "마지막 문단"),
    ]),
    ("4장 · 전체 구조 · 인코더와 디코더", [
        ("인코더·디코더", "§3 도입", "인코더: x → z 한꺼번에", "디코더: y를 하나씩 (자기회귀)", "그림 2", "자기회귀"),
        ("원문 그림 1", "§3", "아래에서 위로 상자 ①~⑩", "임베딩 → 어텐션 → FFN → Softmax", "원문 그림 1", "그림 3 한글판"),
        ("인코더", "§3.1", "6층 · 서브층 2개 · 폭 512", "LayerNorm( x + Sublayer(x) )", "그림 4", "잔차 연결"),
        ("디코더", "§3.1", "서브층 3개 · 인코더 출력 참고", "마스크 + 한 칸 밀기 → 앞만 봄", "그림 5", "한 칸 밀기"),
    ]),
    ("5장 · 어텐션", [
        ("어텐션이란", "§3.2", "쿼리와 키로 비율 → 값의 가중합", "출력 = 값들을 비율대로 섞은 것", "그림 2", "찾아보기"),
        ("식 (1)", "§3.2.1", "softmax( QKᵀ / √dk ) · V", "MatMul → Scale → SoftMax → MatMul", "그림 3", "코드 1"),
        ("√dk 로 나누기", "§3.2.1", "q·k 분산 = dk → 나누면 1", "softmax 쏠림과 작은 기울기 방지", "그림 4", "코드 2"),
        ("멀티헤드", "§3.2.2", "64칸 × 8개 → 이어 붙여 512", "계산량은 512칸 한 개와 같음", "그림 5", "코드 3"),
        ("세 가지 쓰임", "§3.2.3", "인코더 셀프 · 디코더 셀프 · 인코더-디코더", "디코더는 미래 칸을 −∞로 가림", "그림 6·7", "코드 4"),
    ]),
    ("6장 · FFN · 임베딩 · 위치 인코딩", [
        ("FFN", "§3.3", "512 → 2048 → 512 · ReLU · 식 (2)", "위치마다 같은 가중치, 층마다 다름", "그림 2", "위치별 FFN"),
        ("임베딩", "§3.4", "한 행렬을 세 곳에서 공유", "임베딩에는 √512를 곱함", "그림 3", "가중치 공유"),
        ("위치 인코딩", "§3.5", "사인·코사인을 임베딩에 더함", "파장 2π ~ 10000·2π · 위치 이동 = 회전", "그림 4·5", "코드 1"),
        ("숫자 확인", "표 3", "base 약 63M · big 약 214M", "표 3의 65M · 213M과 근사", "코드 2", "가중치 수"),
    ]),
    ("7장 · 왜 셀프 어텐션인가", [
        ("기준 세 가지", "§4", "계산량 · 순차 연산 · 최대 경로 길이", "짧은 경로가 먼 관계 학습에 유리", "표", "기준"),
        ("표 1", "§4", "셀프 어텐션: 순차 O(1) · 경로 O(1)", "대가: 층 계산량 O(n²·d)", "표 1", "네 가지 층"),
        ("vs 순환층", "§4", "n < d 이면 계산도 더 적음", "긴 입력은 이웃 r칸만 보기 (과제)", "그림 2·3", "코드 1"),
        ("vs 합성곱층", "§4", "끝까지 닿는 데 여러 층 필요", "비용은 순환층의 약 k배", "표", "합성곱 비교"),
        ("덤", "§4", "헤드마다 다른 일 → 해석하기 쉬움", "어텐션 분포 예는 부록에", "10장", "원문 그림 3"),
    ]),
    ("8장 · 학습 방법", [
        ("데이터", "§5.1", "영→독 450만 쌍 · 영→프 3600만 문장", "배치당 원문·번역문 각 약 25000 토큰", "표", "데이터"),
        ("하드웨어", "§5.2", "P100 GPU 8장", "base 10만 단계 12시간 · big 30만 단계 3.5일", "표", "학습 시간"),
        ("최적화기", "§5.3", "Adam · 식 (3) · warmup 4000", "4000단계에서 최고 약 7.0×10⁻⁴", "그림 2", "코드 1"),
        ("규제", "§5.4", "Dropout 0.1 · Label Smoothing 0.1", "스무딩: 퍼플렉시티는 나빠지고 BLEU는 좋아짐", "그림 3", "코드 2"),
    ]),
    ("9장 · 결과", [
        ("번역 점수", "§6.1", "영→독 28.4 · 영→프 41.8 (표 2)", "base도 영→독 기존 최고보다 높음", "표 2", "그림 2"),
        ("학습 비용", "§6.1", "시간 × GPU 수 × 9.5 TFLOPS", "base 3.3×10¹⁸ · big 2.3×10¹⁹", "코드 1", "비용 추정"),
        ("변형 실험", "§6.2", "헤드 8~16 · dk 크게 · 모델은 클수록", "Dropout 필수 · 위치 방식은 무관", "표 3", "그림 3"),
        ("구문 분석", "§6.3", "4층 · d_model 1024", "WSJ만 91.3 · 준지도 92.7", "표 4", "구문 분석"),
    ]),
    ("10장 · 결론과 그 뒤", [
        ("결론", "§7", "어텐션만으로 된 첫 변환 모델", "더 빠른 학습 · 번역 최고 기록", "원문 요지", "결론"),
        ("앞으로의 계획", "§7", "다른 과제 · 다른 모달리티 · 덜 순차적 생성", "큰 입력에는 지역 어텐션", "표", "계획 세 가지"),
        ("부록", "부록", "헤드마다 다른 일 · 먼 위치를 1단계로", "making → more difficult", "원문 그림 3", "그림 설명"),
        ("그 뒤 (논문 밖)", "2018 ~", "인코더만 BERT·ViT · 디코더만 GPT", "둘 다 T5 · BART · Whisper", "그림 2", "세 갈래"),
    ]),
]

NAVY = dict(textColor="#172439", subTextColor="#273e5e", strokeColor="#1F3A5F",
            fill="none", fontMain=23, fontSub=18, strokeWidth=3.5, preset="navy")
DARK = dict(textColor="#ffffff", subTextColor="#dceaff", strokeColor="#102944",
            fill="#1f3a5f", fontMain=23, fontSub=18, strokeWidth=3.5, preset="dark")
BLUE = dict(textColor="#163457", subTextColor="#325477", strokeColor="#205184",
            fill="#eaf3ff", fontMain=23, fontSub=18, strokeWidth=3, preset="blue")
EDGE = dict(route="auto", strokeColor="#5A1E1E", strokeWidth=3.5, arrowSize=16, labelFont=17)

X1, W1 = 190, 300     # 원문 위치
X2, W2 = 790, 760     # 핵심 · 근거
X3, W3 = 1335, 230    # 해설서에서 볼 곳
Y0, DY, H = 196, 106, 80


def page(no, title, rows):
    nodes, edges = [], []
    for i, (name, where, core, detail, ref1, ref2) in enumerate(rows):
        y = Y0 + i * DY
        common = dict(type="rect", y=y, h=H, pad=6, padY=4, textAlign="center", autoFit=False)
        nodes.append(dict(id=f"s{i + 1}", x=X1, w=W1, title=name, sub=where, **common, **DARK))
        nodes.append(dict(id=f"c{i + 1}", x=X2, w=W2, title=core, sub=detail, **common, **NAVY))
        nodes.append(dict(id=f"g{i + 1}", x=X3, w=W3, title=ref1, sub=ref2, **common, **BLUE))
        edges.append(dict(id=f"h{i + 1}", **{"from": f"s{i + 1}", "to": f"c{i + 1}"},
                          fp="right", tp="left", label="", **EDGE))
        edges.append(dict(id=f"k{i + 1}", **{"from": f"c{i + 1}", "to": f"g{i + 1}"},
                          fp="right", tp="left", label="", **EDGE))
        if i:
            edges.append(dict(id=f"v{i}", **{"from": f"s{i}", "to": f"s{i + 1}"},
                              fp="bottom", tp="top", label="", **EDGE))
    return dict(
        version=3, chapter=f"AIAYN-{no:02d}", verification="PAPER_TEXT_CHECKED",
        pageTitle=f"{no}장 큰 그림",
        title=f"{title} · 이 장의 큰 그림",
        subtitle="원문 위치 → 핵심과 근거 → 해설서에서 볼 그림·코드 · 왼쪽 세로줄이 읽는 순서",
        width=1480, height=Y0 + (len(rows) - 1) * DY + H // 2 + 34,
        headings=dict(title=dict(x=740, y=52, w=1100, h=56, size=33, align="center", autoFit=True),
                      subtitle=dict(x=740, y=102, w=1200, h=38, size=19, align="center", autoFit=True)),
        settings=dict(fontMain=23, fontSub=18, stroke=3.5, gap=40, pad=6, padY=4, defaultPreset="navy"),
        nodes=nodes, edges=edges)


pages = [page(i + 1, t, rows) for i, (t, rows) in enumerate(CHAPTERS)]
doc = dict(version=3, format="soc-flow-pages", chapter="AIAYN-CH", activePage=0, pages=pages)
(OUT / "chapter_maps_pages.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
print("페이지", len(pages), "· 노드", sum(len(p["nodes"]) for p in pages))
