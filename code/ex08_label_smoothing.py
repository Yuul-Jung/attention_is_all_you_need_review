# 5.4절: label smoothing ε_ls = 0.1. 정답에 1.0 대신 0.9 근처를 주고 나머지를 고루 나눈다.
# 아래는 흔히 쓰는 방식(정답 1-ε, 나머지 ε/(V-1))의 예. 논문은 정확한 분배식을 적지 않았다.
eps, V = 0.1, 5          # 설명용으로 어휘를 5개로 줄임
answer = 2

target = [eps / (V - 1)] * V
target[answer] = 1 - eps
print("원-핫 목표   :", [1.0 if i == answer else 0.0 for i in range(V)])
print("스무딩 목표  :", [round(t, 3) for t in target], " 합 =", round(sum(target), 6))
