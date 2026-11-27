# 표 1: 층 하나의 계산량 비교. 셀프 어텐션 n²·d, 순환층 n·d².
d = 512
for n in (30, 100, 512, 2000):
    sa, rnn = n * n * d, n * d * d
    faster = "셀프 어텐션" if sa < rnn else ("같음" if sa == rnn else "순환층")
    print(f"n={n:5d}  n²·d={sa:>13,}  n·d²={rnn:>13,}  더 적은 쪽: {faster}")
