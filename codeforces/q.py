from math import log


K1, K2 = map(int, input().split())
N = int(input())

D = {}
X = [0] * K1
Y = [0] * K2
for _ in range(N):
    x, y = map(int, input().split())
    i1 = x - 1
    i2 = y - 1
    i3 = (i1, i2)

    X[i1] += 1

    if D.get(i3) is not None:
        D[i3] += 1
    else:
        D[i3] = 1

answer = 0
for (i1, _), p in D.items():
    answer -= p * log(p / X[i1]) / N

print(answer)
