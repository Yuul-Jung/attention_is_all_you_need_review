# 6.1절·각주 5: 학습 FLOPs ≈ 학습 시간 × GPU 수 × GPU 1개의 지속 성능(P100 = 9.5 TFLOPS)
p100 = 9.5e12
gpus = 8
base_sec = 12 * 3600          # 5.2절: base 12시간
big_sec = 3.5 * 24 * 3600     # 5.2절: big 3.5일

print(f"base: {base_sec * gpus * p100:.2e} FLOPs  (표 2: 3.3e18)")
print(f"big : {big_sec * gpus * p100:.2e} FLOPs  (표 2: 2.3e19)")
