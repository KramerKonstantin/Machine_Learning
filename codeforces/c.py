from math import sqrt, cos, exp, pi


def get_distance(distance_name):
    def manhattan(a, b):
        rv = 0
        for i in range(len(b)):
            rv += abs(a[i] - b[i])
        return rv

    def euclidean(a, b):
        rv = 0
        for i in range(len(b)):
            rv += (a[i] - b[i]) ** 2
        return sqrt(rv)

    def chebyshev(a, b):
        rv = -1
        for i in range(len(b)):
            rv = max(rv, abs(a[i] - b[i]))
        return rv

    return {
        'manhattan': manhattan,
        'euclidean': euclidean,
        'chebyshev': chebyshev
    }[distance_name]


def get_kernel(kernel_name):
    def uniform(a):
        return 0.5 if (abs(a) < 1) else 0.0

    def triangular(a):
        return (1 - abs(a)) if (abs(a) < 1) else 0.0

    def epanechnikov(a):
        return (1 - a ** 2) * 3 / 4 if (abs(a) < 1) else 0.0

    def quartic(a):
        return ((1 - a ** 2) ** 2) * 15 / 16 if (abs(a) < 1) else 0.0

    def triweight(a):
        return ((1 - a ** 2) ** 3) * 35 / 32 if (abs(a) < 1) else 0.0

    def tricube(a):
        return ((1 - abs(a ** 3)) ** 3) * 70 / 81 if (abs(a) < 1) else 0.0

    def gaussian(a):
        return exp(-0.5 * (a ** 2)) / sqrt(pi * 2)

    def cosine(a):
        return pi / 4 * cos(pi / 2 * a) if (abs(a) < 1) else 0.0

    def logistic(a):
        return 1 / (exp(a) + 2 + exp(-a))

    def sigmoid(a):
        return 2 / pi * (1 / (exp(a) + exp(-a)))

    return {
        'uniform': uniform,
        'triangular': triangular,
        'epanechnikov': epanechnikov,
        'quartic': quartic,
        'triweight': triweight,
        'tricube': tricube,
        'gaussian': gaussian,
        'cosine': cosine,
        'logistic': logistic,
        'sigmoid': sigmoid
    }[kernel_name]


N, M = map(int, input().split())
d = [([0] * M) for i in range(N)]
target_value = [0] * N
for i in range(N):
    cur_line = list(map(int, input().split()))
    for j in range(M):
        d[i][j] = cur_line[j]
    target_value[i] = cur_line[M]
q = list(map(int, input().split()))
distance = get_distance(input())
kernel = get_kernel(input())
window_type = input()
h = int(input())

distances = list(map(lambda x: (distance(x, q)), d))
sorted_distances = sorted(list(zip(distances, [i for i in range(N)])), key=lambda x: x[0])

h = h if window_type == 'fixed' else sorted_distances[h][0]

s1 = 0
s2 = 0
for i in range(N):
    w = kernel(0 if sorted_distances[i][0] == 0 else (1 if h == 0 else sorted_distances[i][0] / h))
    s1 += target_value[sorted_distances[i][1]] * w
    s2 += w

res = 0
try:
    res = s1 / s2
except ZeroDivisionError:
    res = sum(target_value) / len(target_value)

print(res)
