# 3.2.2절: h=8, d_k=d_v=d_model/h=64. 헤드를 나눠도 투영 가중치 수는 한 헤드 전체 크기와 같다.
d_model, h = 512, 8
d_k = d_v = d_model // h

# 헤드 8개의 W_i^Q, W_i^K, W_i^V 를 모두 더한 개수
split = h * (d_model * d_k + d_model * d_k + d_model * d_v)
# 헤드 1개를 d_model 크기 그대로 쓸 때
single = 3 * d_model * d_model
# 출력 투영 W^O 의 크기: (h*d_v) x d_model
w_o = (h * d_v) * d_model

print("d_k = d_v =", d_k)
print("헤드 8개 투영 합 :", split)
print("단일 헤드 투영   :", single)
print("W^O              :", w_o, f"= ({h * d_v} x {d_model})")
