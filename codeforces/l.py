from math import sqrt


N = int(input())

X = []
Y = []
for _ in range(N):
    x, y = map(int, input().split())
    X.append(x)
    Y.append(y)

average_x = sum(X) / N
average_y = sum(Y) / N

numerator = 0
sum_x = 0
sum_y = 0
for i in range(N):
    _x = X[i] - average_x
    _y = Y[i] - average_y
    numerator += _x * _y
    sum_x += _x ** 2
    sum_y += _y ** 2

denominator = sqrt(sum_x * sum_y)

print(numerator / denominator if denominator > 0 else 0)
