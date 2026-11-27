# Attention Is All You Need 원문 해설서

Vaswani 외(2017) 「[Attention Is All You Need](https://arxiv.org/abs/1706.03762)」(arXiv v7)를 **원문 순서대로** 읽는 학습안내서입니다. 초록부터 7절과 부록까지 10개 장으로 나눴습니다.

- 사이트: `dist/index.html` (GitHub Pages에서는 저장소 첫 화면이 `dist/`로 이어짐)
- 논문 큰 그림: `figs/bigpicture.svg` · 편집 원본 `diagrams/bigpicture_pages.json`
- 장별 큰 그림: `figs/c01_bigpicture.svg` ~ `c10_bigpicture.svg` · 편집 원본 `diagrams/chapter_maps_pages.json` (10페이지)

## 📘 교육용 HTML 공통 제작 규칙

이 저장소의 교육자료는 [Yuul-Jung 교육용 HTML 공통 표준](https://github.com/Yuul-Jung/rule_md/tree/main/web/education-html)을 적용합니다.

- [제작 규칙](https://github.com/Yuul-Jung/rule_md/blob/main/web/education-html/STANDARD.md)
- [다른 저장소 적용 안내](https://github.com/Yuul-Jung/rule_md/blob/main/web/education-html/INTEGRATION.md)
- [기준 디자인 사례](https://github.com/Yuul-Jung/ai-agent-engineering)

공통 책장 이미지, 컴팩트한 상단 배너, 좌측 전체 장/절 탐색, 모바일 메뉴, 파일 버전 및 검증 기준을 따릅니다. `build.py`, `assets/site.js`, `assets/site.css` 1~11절은 rule_md `028248a` 사본이고, `site.css` 12절(해설서 읽기 보조)만 이 저장소에서 더했습니다.

## 구성

| 장 | 원문 | 내용 |
|---|---|---|
| 1 | 초록 | 논문 정보 · 논문 큰 그림 · 초록의 주장 다섯 가지 |
| 2 | §1 | 서론 · RNN의 차례 계산 |
| 3 | §2 | 배경 · 합성곱 모델의 경로 길이 |
| 4 | §3 · §3.1 | 원문 그림 1 · 인코더·디코더 6층 · 잔차 + LayerNorm · 한 칸 밀기 |
| 5 | §3.2 | 원문 그림 2 · 식 (1) · √dk · 멀티헤드 · 세 가지 쓰임과 마스크 |
| 6 | §3.3–3.5 | FFN 식 (2) · 임베딩 공유 · 사인·코사인 위치 · 가중치 수 |
| 7 | §4 | 표 1 · 계산량 · 순차 연산 · 최대 경로 |
| 8 | §5 | 데이터 · 하드웨어 · Adam과 식 (3) · Dropout · Label Smoothing |
| 9 | §6 | 표 2 · 표 3 · 표 4 |
| 10 | §7 · 부록 | 결론 · 원문 그림 3 · 그 뒤의 흐름 (논문 밖 내용) |

장마다: 이 장의 큰 그림(전체 지도 + 장별 큰 그림) → 쉬운 풀이 표 → 절마다 「이 절에서 할 일」 · 원문 요지 · 그림 · 「쉽게 말하면」 → 「이 장 정리」 · 「자주 하는 오해」.

## 폴더

| 경로 | 내용 |
|---|---|
| `content_src/chNN.md` | 장별 원고 (번호는 `@`, `#`로 비워 둠) |
| `content/chNN.md` | 번호를 붙인 원고 (`tools/number.py` 생성물) |
| `code/ex*.py` · `code/ex*.out` | 숫자 검증 예제와 실제 실행 출력 (Python 3 · NumPy) |
| `figs/` | 그림 47개(SVG) · 원문 그림 3개(PNG) |
| `diagrams/bigpicture_pages.json` | 논문 큰 그림, [svg-flow-editor](https://github.com/Yuul-Jung/svg-flow-editor) 형식 |
| `diagrams/chapter_maps_pages.json` | 장별 큰 그림 10페이지, 같은 형식 |
| `tools/make_figs.py` · `tools/svglib.py` | 그림 생성 |
| `tools/make_bigpicture.py` · `tools/make_chapter_maps.py` | 논문·장별 큰 그림 JSON 생성 |
| `tools/export_editor_svg.py` | 편집기에 불러와 품질 검사 후 SVG 내보내기 (여러 페이지 지원) |
| `build.py` · `embed_svg.py` · `assets/` | rule_md 생성기 · 꾸밈과 그림 넣기 · 스타일 |
| `dist/` | 배포용 HTML 11개 (첫 화면 + 10장 `_v05`, 그림 내장) · `dist/code/` 본문에서 여는 예제 |
| `code/ch*_example_*.py` | 본문 링크용 예제 이름. 같은 번호의 `ex*.py`와 바이트가 같음(`ch05_example_04.py`만 따로) |
| `requirements.txt` | 예제 의존성 (numpy) |
| `검증기록/` | 통합본 v13 장별·최종 검증 기록과 분리 배포 검증 기록 v14 |

## 다시 만들기

> **주의 (v05):** `dist/`의 v05 HTML은 원문 해설서·쉬운 해설서 통합본 v13에서 원문 해설서만 분리한 배포본(v14 검증)을 그대로 넣은 것입니다. `content_src/` 원고는 아직 v02 기준이라 v05 본문 수정이 들어 있지 않습니다. 원고를 v05에 맞추기 전에 `build_all.sh`나 `build.py`를 실행하면 `dist/`가 v02 내용으로 돌아갑니다.

```bash
python -m pip install mistune numpy matplotlib
./tools/build_all.sh          # 예제 실행 → 그림 → 번호 → HTML → 그림 넣기
# 큰 그림 SVG까지 다시 내보낼 때 (playwright · Chrome 필요)
FLOW_EDITOR=../svg-flow-editor/index.html ./tools/build_all.sh
```

큰 그림을 고칠 때:

1. [svg-flow-editor](https://yuul-jung.github.io/svg-flow-editor/)에서 `diagrams/bigpicture_pages.json`을 불러와 고치고 JSON으로 저장합니다.
2. SVG를 다시 내보냅니다 (편집기 `index.html` 경로 필요, playwright · Chrome 사용).

```bash
python tools/export_editor_svg.py ../svg-flow-editor/index.html diagrams/bigpicture_pages.json figs/bigpicture.svg
python tools/export_editor_svg.py ../svg-flow-editor/index.html diagrams/chapter_maps_pages.json 'figs/c{n}_bigpicture.svg'
```

편집기의 `svgString()`은 제목 선택용 상자(`.heading-hit`)를 SVG에 남깁니다. fill이 없어 편집기 밖에서 검은 상자로 보이므로, 내보내기 도구가 이 상자를 지웁니다.

## 원문 사용

1. 원문 첫 줄의 허락 문구(출처를 밝히면 학술·보도 목적으로 표와 그림 사용 가능)에 따라 원문 그림 1~3과 표 1~4를 출처와 함께 싣습니다.
2. 본문 문장은 옮겨 싣지 않고 우리말 요지로 다시 썼습니다.

## 검증 (v05)

| 항목 | 판정 | 내용 |
|---|---|---|
| 내부 링크 | 통과 | 11쪽의 장·절·이전/다음·예제 링크 대상 확인 (`dist/code/` 포함) |
| 예제 실행 | 통과 | `code/*.py` 21개 실행. `ex*.out` 10개는 v02 출력과 같음 |
| 바뀐 예제 | 통과 | `ex05_variance.py` 주석, `ex08_lrate.py` step ≥ 1 검사 추가. 출력 변화 없음 |
| 화면 | 통과 | 1366 · 390px에서 11쪽 가로 넘침 0, 깨진 그림 0, 콘솔 오류 0, 좌측 목차 생성 |
| 개인정보·로컬 경로 | 통과 | 전자우편·전화·로컬 경로 문자열 없음 |
| 원고 동기화 | 미검증 | `content_src/`는 v02 기준, v05 본문과 맞추지 않음 |
| GitHub Pages 실제 배포 | 미검증 | 저장소 Pages 설정 후 확인 필요 |

이전 판의 검증 기록은 `검증기록/`에 있습니다.

## 검증 (v02)

| 항목 | 판정 | 내용 |
|---|---|---|
| 숫자 대조 | 통과 | 5절·6절 하이퍼파라미터, 표 2·3·4 값을 원문 v7 텍스트와 대조 |
| 예제 실행 | 통과 | `code/ex*.py` 10개 실행, 출력은 `.out` 그대로 수록 |
| 원문 숫자 재계산 | 통과 | 각주 4 분산 = dk, 식 (3) 최고점 6.99e-4, 표 2 FLOPs 3.28e18 · 2.30e19 |
| 가중치 수 | 근사 | base 63.1M (표 3: 65M), big 214.2M (표 3: 213M). 어휘 크기 등 가정 포함 |
| 화면 | 통과 | 1366 · 390 · 320px 가로 넘침 0, 그림 깨짐 0, 콘솔 오류 0, 내부 링크 정상 |
| 큰 그림 | 통과 | svg-flow-editor `inspectDiagramQuality()` 지적 0건 (논문 1페이지 + 장별 10페이지) |
| GitHub Pages 실제 배포 | 미검증 | 저장소 Pages 설정 후 확인 필요 |

원문 확인 사항: 영→프 BLEU는 초록·표 2가 41.8, 6.1절 본문이 41.0입니다. 해설서는 표 2를 기준으로 하고 두 값을 함께 밝혔습니다.

## 변경 이력

| 판 | 내용 |
|---|---|
| v05 | 통합본 v13에서 분리한 원문 해설서 v14 배포본 반영: 용어 풀이를 정의 중심으로 고침, 절마다 논문 근거·한계 문장 보강(예: 2장 순차 의존성과 연산량, 세 종류의 어텐션, 학습과 추론의 차이), 예제 링크 `code/ch*_example_*.py`, 검증 기록 추가 |
| v02 | 장마다 「이 장은 이런 순서로 이야기합니다」 글 목록을 svg-flow-editor 장별 큰 그림으로 바꿈 (원문 위치 → 핵심·근거 → 볼 그림·코드) |
| v01 | 첫 게시: 원문 순서 10개 장, 논문 큰 그림, 숫자 검증 예제 10개 |
