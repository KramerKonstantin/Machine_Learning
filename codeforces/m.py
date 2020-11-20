N = int(input())

X = []
Y = []
for i in range(N):
    x, y = map(int, input().split())
    X.append((x, i))
    Y.append((y, i))

for index, (x, i) in enumerate(sorted(X)):
    X[i] = index

for index, (y, i) in enumerate(sorted(Y)):
    Y[i] = index

numerator = 6 * sum([(X[i] - Y[i]) ** 2 for i in range(N)])
denominator = N * (N - 1) * (N + 1)

print(1 - numerator / denominator)
