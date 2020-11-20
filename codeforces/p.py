K1, K2 = map(int, input().split())
N = int(input())

D = {}
X1 = [0] * K1
X2 = [0] * K2
for _ in range(N):
    x1, x2 = map(int, input().split())
    i1 = x1 - 1
    i2 = x2 - 1
    i3 = (i1, i2)

    X1[i1] += 1
    X2[i2] += 1

    if D.get(i3) is not None:
        D[i3] += 1
    else:
        D[i3] = 1

answer = N
for (i1, i2), p in D.items():
    answer += (p * N / (X1[i1] * X2[i2]) - 2) * p

print(answer)
