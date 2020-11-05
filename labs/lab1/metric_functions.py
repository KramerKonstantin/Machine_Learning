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
