K = int(input())
N = int(input())

X = [[] for _ in range(K)]
for _ in range(N):
    x, y = map(int, input().split())
    X[x - 1].append(y)

answer = 0.0
for x in X:
    l = len(x)
    if l != 0:
        average = sum(x) / l
        answer += sum([(x[i] - average) ** 2 for i in range(l)]) / N

print(answer)
