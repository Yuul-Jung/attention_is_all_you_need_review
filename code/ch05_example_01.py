# 식 (1) Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V 를 작은 숫자로 직접 계산한다.
import numpy as np

np.set_printoptions(precision=3, suppress=True)

# 토큰 3개, d_k = d_v = 4 인 작은 예 (숫자는 설명용으로 정한 값)
Q = np.array([[1.0, 0.0, 1.0, 0.0],
              [0.0, 1.0, 0.0, 1.0],
              [1.0, 1.0, 0.0, 0.0]])
K = np.array([[1.0, 0.0, 1.0, 0.0],
              [0.0, 1.0, 0.0, 1.0],
              [1.0, 1.0, 1.0, 1.0]])
V = np.array([[10.0, 0.0, 0.0, 0.0],
              [0.0, 10.0, 0.0, 0.0],
              [0.0, 0.0, 10.0, 0.0]])
d_k = K.shape[1]


def softmax(x):
    # 행마다 최댓값을 빼고 계산해 exp가 넘치지 않게 한다 (결과는 같음)
    e = np.exp(x - x.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


scores = Q @ K.T                     # ① MatMul: 질문과 명찰의 내적
scaled = scores / np.sqrt(d_k)       # ② Scale: sqrt(d_k)=2 로 나눔
weights = softmax(scaled)            # ③ SoftMax: 행마다 합이 1인 비율
out = weights @ V                    # ④ MatMul: 비율대로 V를 섞음

print("QK^T =\n", scores)
print("나누기 sqrt(d_k) =\n", scaled)
print("가중치(행 합 = 1) =\n", weights)
print("행 합 =", weights.sum(axis=1))
print("출력 =\n", out)
