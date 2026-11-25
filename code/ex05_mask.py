# 3.2.3절: 디코더 셀프 어텐션의 마스크. 미래 칸 점수를 -inf 로 바꾼 뒤 softmax 한다.
import numpy as np

np.set_printoptions(precision=3, suppress=True)

scaled = np.array([[0.5, 1.0, 2.0],
                   [1.0, 0.5, 1.0],
                   [2.0, 1.0, 0.5]])
n = scaled.shape[0]

# 대각선 위쪽(자기보다 뒤 위치)만 True 인 표
future = np.triu(np.ones((n, n), dtype=bool), k=1)
masked = np.where(future, -np.inf, scaled)

e = np.exp(masked - masked.max(axis=-1, keepdims=True))
weights = e / e.sum(axis=-1, keepdims=True)

print("가리기 전 점수 =\n", scaled)
print("가린 점수 =\n", masked)
print("가중치 =\n", weights)
