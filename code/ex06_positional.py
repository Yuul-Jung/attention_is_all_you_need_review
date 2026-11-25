# 3.5절: 사인·코사인 위치 인코딩을 만들고 두 성질을 확인한다.
import numpy as np

np.set_printoptions(precision=3, suppress=True)
d_model = 512


def pe(pos):
    i = np.arange(d_model // 2)
    angle = pos / (10000 ** (2 * i / d_model))
    v = np.zeros(d_model)
    v[0::2] = np.sin(angle)   # 짝수 칸 2i
    v[1::2] = np.cos(angle)   # 홀수 칸 2i+1
    return v


# ① 앞쪽 네 칸 값: 위치마다 다른 무늬가 된다
for pos in range(4):
    print(f"pos={pos}  앞 4칸 = {pe(pos)[:4]}")

# ② 파장: 2π 에서 10000·2π 쪽으로 등비로 늘어난다
i = np.array([0, 1, 128, 255])
wave = 2 * np.pi * 10000 ** (2 * i / d_model)
print("i =", i, " 파장 =", np.round(wave, 2))

# ③ 위치를 k 만큼 옮기는 것은 칸 쌍마다 같은 회전(선형 변환)이다
pos, k = 7, 3
i = np.arange(d_model // 2)
w = 1 / (10000 ** (2 * i / d_model))
s, c = pe(pos)[0::2], pe(pos)[1::2]
s_new = s * np.cos(k * w) + c * np.sin(k * w)
c_new = c * np.cos(k * w) - s * np.sin(k * w)
moved = np.zeros(d_model)
moved[0::2], moved[1::2] = s_new, c_new
print("회전으로 만든 PE(10) 와 직접 계산한 PE(10) 의 최대 차이 =",
      f"{np.abs(moved - pe(pos + k)).max():.1e}")
