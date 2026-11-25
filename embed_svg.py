#!/usr/bin/env python3
"""build.py 다음에 실행하는 마무리 단계 (글자는 바꾸지 않음).

1) 읽기 보조: 그림 → 액자(figure), '이 절에서 할 일'·'쉽게 말하면' → 상자,
   작은 제목 번호 → 꼬리표, 표 → 좌우 이동 틀, '식' 문단 → 수식 상자.
2) INDEX 의 '전체 학습 테크트리' 절 첫머리에 논문 큰 그림(bigpicture.svg)을 넣는다.
3) <img src="figs/이름.svg|png"> 를 data URI 로 바꿔 HTML 한 파일로 보이게 한다.
   (표준 생성기의 마크다운 변환기는 data URI 를 막으므로 변환 뒤에 넣는다.)
"""
import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
count = {}


def sub(pat, rep, h, key, flags=0):
    h2, k = re.subn(pat, rep, h, flags=flags)
    count[key] = count.get(key, 0) + k
    return h2


def pretty(h):
    cap = r'((?:쉬운 그림|그림|원문 그림) \d+(?:\.\d+)?\.|큰 그림\.)'
    h = sub(r'<p>(<img src="figs/[^>]+/>)</p>\s*<p><strong>' + cap + r'</strong>(.*?)</p>',
            r'<figure class="fig"><div class="fig-in">\1</div><figcaption><b>\2</b>\3</figcaption></figure>',
            h, '그림 액자', re.S)
    h = sub(r'<p>(<img src="figs/[^>]+/>)</p>', r'<figure class="fig"><div class="fig-in">\1</div></figure>',
            h, '그림 액자(설명 없음)')
    h = sub(r'<h4>\d\d-\d+ 이 절에서 할 일</h4>\s*(<ol>.*?</ol>)',
            r'<div class="box todo"><div class="box-t">이 절에서 할 일</div>\1</div>', h, '할 일 상자', re.S)
    h = sub(r'<blockquote>\s*<p><strong>쉽게 말하면</strong>(.*?)</p>\s*</blockquote>',
            r'<div class="box say"><div class="box-t">쉽게 말하면</div><p>\1</p></div>', h, '쉽게 말하면 상자', re.S)

    def head(m):
        tag, num, t = m.group(1), m.group(2), m.group(3)
        kinds = (('쉽게 읽기', 'easy'), ('자주 하는 오해', 'warn'), ('이 장 정리', 'sum'),
                 ('코드', 'codeh'), ('원문', 'paper'))
        cls = next((c for k, c in kinds if k in t), '')
        return f'<{tag} class="sh {cls}"><span class="sub">{num}</span>{t}</{tag}>'
    h = sub(r'<(h[34])>(\d\d-\d+) (.*?)</h[34]>', head, h, '작은 제목 꼬리표')
    h = sub(r'(<table>.*?</table>)', r'<div class="tbl">\1</div>', h, '표 틀', re.S)
    h = sub(r'<p>(<strong>코드 \d+</strong> · .*?)</p>', r'<p class="meta">\1</p>', h, '코드 머리말', re.S)
    h = sub(r'<p>(<strong>실행 결과 \d+</strong>.*?)</p>', r'<p class="meta out">\1</p>', h, '실행 결과 머리말', re.S)
    h = sub(r'<div class="codeblock"><div class="codebar"><span>FORMULA</span>.*?<pre><code>(.*?)</code></pre></div>',
            r'<div class="formula" role="math">\1</div>', h, '수식 상자', re.S)
    return h


def index_bigpicture(h):
    fig = ('<figure class="fig"><div class="fig-in"><img class="wide" src="figs/bigpicture.svg" '
           'alt="논문 큰 그림: 초록부터 7절까지 원문 순서, 핵심 내용과 숫자, 해설서 1~10장 대응"/></div>'
           '<figcaption><b>큰 그림.</b> 왼쪽 세로줄이 논문을 읽는 순서입니다. '
           '가운데는 그 부분의 핵심, 오른쪽은 해설서 장입니다.</figcaption></figure>')
    return sub(r'(<section class="section" id="roadmap"><h2>.*?</h2>)', lambda m: m.group(1) + fig, h, 'INDEX 큰 그림')


n = 0
for p in sorted((ROOT / 'dist').glob('*.html')):
    h = pretty(p.read_text(encoding='utf-8'))
    if p.name == 'index.html':
        h = index_bigpicture(h)

    def embed(m):
        global n
        n += 1
        name = m.group(1)
        mime = 'image/svg+xml' if name.endswith('.svg') else 'image/png'
        raw = (ROOT / 'figs' / name).read_bytes()
        return f'src="data:{mime};base64,' + base64.b64encode(raw).decode() + '"'
    h = re.sub(r'src="figs/([\w-]+\.(?:svg|png))"', embed, h)
    assert 'src="figs/' not in h, p.name
    p.write_text(h, encoding='utf-8')
print('꾸민 곳:', ' · '.join(f'{k} {v}' for k, v in count.items()))
print('그림', n, '개를 HTML 안에 넣었습니다')
