#!/usr/bin/env bash
# 전체 다시 만들기: 예제 실행 → 그림 → 번호 → HTML → 그림 넣기
set -euo pipefail
cd "$(dirname "$0")/.."
for f in code/ex*.py; do
  python3 "$f" > "${f%.py}.out"
done
python3 tools/make_figs.py
python3 tools/number.py
python3 build.py
python3 embed_svg.py
