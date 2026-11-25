#!/usr/bin/env python3
"""content_src/chNN.md → content/chNN.md : 번호를 자동으로 붙인다.

- '### @ 제목', '#### @ 제목'  → '### NN-k 제목' (NN = '##' 절 번호, k = 절 안 순번)
- '**그림 #.**'                → '**그림 k.**' (장 안 순번)
- '{{code:이름}}'              → code/이름.py 와 code/이름.out 을 '코드 k'·'실행 결과 k' 로 넣음
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def convert(text):
    out, sec, k, fig, code = [], -1, 0, 0, 0
    for line in text.splitlines():
        if line.startswith("## "):
            sec += 1
            k = 0
        m = re.match(r"^(#{3,4}) @ (.+)$", line)
        if m:
            k += 1
            line = f"{m.group(1)} {sec:02d}-{k} {m.group(2)}"
        while "**그림 #.**" in line:
            fig += 1
            line = line.replace("**그림 #.**", f"**그림 {fig}.**", 1)
        m = re.match(r"^\{\{code:([\w]+)\}\}$", line.strip())
        if m:
            code += 1
            name = m.group(1)
            src = (ROOT / "code" / f"{name}.py").read_text(encoding="utf-8").rstrip()
            res = (ROOT / "code" / f"{name}.out").read_text(encoding="utf-8").rstrip()
            out += [f"**코드 {code}** · `code/{name}.py` · Python 3 · NumPy · 검증: 실행함", "",
                    "```python", src, "```", "",
                    f"**실행 결과 {code}** · 위 코드를 실제로 실행한 출력", "", "```text", res, "```"]
            continue
        out.append(line)
    return "\n".join(out) + "\n"


for p in sorted((ROOT / "content_src").glob("ch*.md")):
    (ROOT / "content" / p.name).write_text(convert(p.read_text(encoding="utf-8")), encoding="utf-8")
    print("번호 붙임:", p.name)
