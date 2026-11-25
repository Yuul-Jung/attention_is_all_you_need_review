#!/usr/bin/env python3
"""svg-flow-editor(index.html)에 JSON 을 불러와 도면 품질 검사 후 SVG 로 내보낸다.

사용: python tools/export_editor_svg.py <편집기 index.html> <도면 JSON> <출력 SVG>
  - 페이지가 여럿이면 출력 이름의 {n} 을 페이지 번호(01, 02, …)로 바꿔 페이지마다 저장한다.
    예: figs/c{n}_bigpicture.svg
편집기의 '불러오기'·'페이지 이동'·'도면 품질 검사'·'SVG 저장'과 같은 함수를 그대로 부른다.
"""
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

editor, src = (Path(a).resolve() for a in sys.argv[1:3])
pattern = sys.argv[3]
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 1600, "height": 1000})
    pg.on("dialog", lambda d: d.dismiss())
    pg.goto(editor.as_uri())
    pg.wait_for_timeout(500)
    pg.set_input_files("#loadJSON", str(src))
    pg.wait_for_timeout(800)
    count = pg.evaluate("pageBook.length")
    for i in range(count):
        if i:
            pg.evaluate(f"goToPage({i})")
            pg.wait_for_timeout(300)
        title = pg.evaluate("scene.title")
        findings = pg.evaluate("(()=>(inspectDiagramQuality()||[]).map(x=>x.message))()")
        svg = pg.evaluate("svgString()")
        # 편집기 svgString() 은 제목 선택용 투명 상자(.heading-hit)를 남긴다.
        # fill 속성이 없어 편집기 밖에서는 검은 상자로 보이므로 내보낼 때 뺀다.
        svg = re.sub(r'<rect[^>]*class="heading-hit"[^>]*/>', "", svg)
        out = Path(pattern.replace("{n}", f"{i + 1:02d}"))
        out.write_text(svg, encoding="utf-8")
        bad += len(findings)
        print(f"[{i + 1}/{count}] {out.name} · {title} · 품질 검사 지적 {len(findings)}")
        for m in findings:
            print("     ", m)
    b.close()
sys.exit(1 if bad else 0)
