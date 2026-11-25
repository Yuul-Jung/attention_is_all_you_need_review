# 표 3 base·big 행의 params(×10^6)를 3.1~3.4절의 크기로 다시 세어 본다.
# 가정: 어휘 37000 공유(5.1절), 입력·출력 임베딩과 출력 Linear 가 한 행렬을 공유(3.4절),
#       모든 Linear 에 bias 있음, LayerNorm 은 gain·bias 2개 벡터.
V, N = 37000, 6


def count(d, d_ff):
    attn = 4 * (d * d + d)                      # W^Q, W^K, W^V, W^O (+bias)
    ffn = (d * d_ff + d_ff) + (d_ff * d + d)    # 식 (2)의 W1,b1,W2,b2
    ln = 2 * d                                  # LayerNorm 하나
    enc_layer = attn + ffn + 2 * ln             # 서브층 2개
    dec_layer = 2 * attn + ffn + 3 * ln         # 서브층 3개
    emb = V * d                                 # 공유 임베딩 1개
    return enc_layer, dec_layer, emb, N * enc_layer + N * dec_layer + emb


for name, d, d_ff, paper in (("base", 512, 2048, 65), ("big", 1024, 4096, 213)):
    enc, dec, emb, total = count(d, d_ff)
    print(f"[{name}] 인코더 층 {enc:,} · 디코더 층 {dec:,} · 임베딩 {emb:,}")
    print(f"[{name}] 합계 {total:,} ≈ {total / 1e6:.1f} ×10^6  (표 3: {paper} ×10^6)")
