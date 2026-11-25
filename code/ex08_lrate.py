# 식 (3): lrate = d_model^-0.5 · min(step^-0.5, step · warmup^-1.5)
d_model, warmup = 512, 4000


def lrate(step):
    return d_model ** -0.5 * min(step ** -0.5, step * warmup ** -1.5)


for step in (1, 1000, 2000, 4000, 8000, 16000, 100000):
    print(f"step={step:6d}  lrate={lrate(step):.2e}")
