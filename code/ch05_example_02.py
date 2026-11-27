# 내적 분산 각주: q, k 성분이 평균 0, 분산 1 이면 q·k 의 분산은 d_k 가 된다. 그래서 sqrt(d_k) 로 나눈다.
import numpy as np

rng = np.random.default_rng(0)


def softmax(x):
    e = np.exp(x - x.max())
    return e / e.sum()


for d_k in (4, 64, 512):
    q = rng.standard_normal((100_000, d_k))
    k = rng.standard_normal((100_000, d_k))
    dots = (q * k).sum(axis=1)
    print(f"d_k={d_k:4d}  q·k 분산={dots.var():8.2f}  "
          f"sqrt(d_k)로 나눈 뒤 분산={(dots / np.sqrt(d_k)).var():5.2f}")

# 같은 크기 차이라도 점수가 크면 softmax 가 한 칸으로 쏠린다
d_k = 64
scores = rng.standard_normal(8) * np.sqrt(d_k)   # 나누지 않은 점수 (표준편차 8 정도)
print("나누지 않음 :", np.round(softmax(scores), 3))
print("sqrt(d_k)로 나눔:", np.round(softmax(scores / np.sqrt(d_k)), 3))
