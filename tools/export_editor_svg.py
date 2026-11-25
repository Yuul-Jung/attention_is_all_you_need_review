#!/usr/bin/env python3
"""svg-flow-editor(index.html)에 JSON 을 불러와 도면 품질 검사 후 SVG 로 내보낸다.

사용: python tools/export_editor_svg.py <편집기 index.html> <도면 JSON> <출력 SVG>
편집기의 '불러오기'·'도면 품질 검사'·'SVG 저장'과 같은 함수를 그대로 부른다.
"""
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

editor, src, out = (Path(a).resolve() for a in sys.argv[1:4])
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 1600, "height": 1000})
    pg.on("dialog", lambda d: d.dismiss())
    pg.goto(editor.as_uri())
    pg.wait_for_timeout(500)
    pg.set_input_files("#loadJSON", str(src))
    pg.wait_for_timeout(800)
    title = pg.evaluate("scene.title")
    findings = pg.evaluate("(()=>{const f=inspectDiagramQuality();return (f||[]).map(x=>x.message)})()")
    svg = pg.evaluate("svgString()")
    b.close()
# 편집기 svgString() 은 제목 선택용 투명 상자(.heading-hit)를 남긴다.
# fill 속성이 없어 편집기 밖에서는 검은 상자로 보이므로 내보낼 때 뺀다.
svg, removed = re.subn(r'<rect[^>]*class="heading-hit"[^>]*/>', "", svg)
out.write_text(svg, encoding="utf-8")
print("제목 선택용 상자 제거:", removed)
print("도면:", title)
print("품질 검사 지적:", len(findings))
for m in findings:
    print("  ", m)
