#!/usr/bin/env bash
# 전체 다시 만들기: 예제 실행 → 그림 → 번호 → HTML → 그림 넣기
set -euo pipefail
cd "$(dirname "$0")/.."
for f in code/ex*.py; do
  python3 "$f" > "${f%.py}.out"
done
python3 tools/make_figs.py
python3 tools/make_bigpicture.py
python3 tools/make_chapter_maps.py
# 큰 그림 SVG 는 svg-flow-editor 로 내보낸다: FLOW_EDITOR=../svg-flow-editor/index.html ./tools/build_all.sh
if [ -n "${FLOW_EDITOR:-}" ]; then
  python3 tools/export_editor_svg.py "$FLOW_EDITOR" diagrams/bigpicture_pages.json figs/bigpicture.svg
  python3 tools/export_editor_svg.py "$FLOW_EDITOR" diagrams/chapter_maps_pages.json 'figs/c{n}_bigpicture.svg'
fi
python3 tools/number.py
python3 build.py
python3 embed_svg.py
