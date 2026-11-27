import numpy as np
# 토큰 3개, 모델 특징 4개, 헤드 2개, 헤드 특징 2개
X = np.array([[1., 0., 1., 0.], [0., 1., 0., 1.], [1., 1., 0., 0.]])
I = np.eye(4)
heads = []
for i in range(2):
    Wq = I[:, 2*i:2*i+2]
    Wk = Wq[:, ::-1]  # 교육용: 열 순서를 바꾼 별도 투영
    Wv = Wq * 2       # 교육용: 별도 값 투영
    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    S = Q @ K.T / np.sqrt(2)
    E = np.exp(S - S.max(axis=1, keepdims=True))
    A = E / E.sum(axis=1, keepdims=True)
    H = A @ V
    assert np.allclose(A.sum(axis=1), 1)
    print(f"head {i+1}: Q={Q.shape}, S={S.shape}, H={H.shape}")
    heads.append(H)
C = np.concatenate(heads, axis=1)
Wo = I[:, ::-1]  # 교육용 출력 투영
Y = C @ Wo
assert Y.shape == X.shape
print("Y =", np.round(Y, 3))