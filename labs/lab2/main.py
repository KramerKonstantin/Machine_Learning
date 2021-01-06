import numpy as np
import matplotlib.pyplot as plt
from math import sqrt


DATA_PATH = "resources/"
NUM_DATA = 7
MAX_ITER = 2000


class Dataset(object):
    def __init__(self, X, Y, M):
        self.X = X
        self.Y = Y
        self.M = M


def get_dataset(file, M):
    N = int(file.readline())

    X = []
    Y = []

    for _ in range(N):
        s = [int(e) for e in file.readline().split()]
        x = s[:M]
        x.append(1)
        X.append(x)
        Y.append(s[M])

    return Dataset(X, Y, M + 1)


def get_data(path):
    file = open(path, "r")
    M = int(file.readline())

    d_train = get_dataset(file, M)
    d_test = get_dataset(file, M)

    return d_train, d_test


def sgd_num_iter(dataset, num_iter):
    X = np.array(dataset.X)
    Y = np.array(dataset.Y)
    M = dataset.M
    W = np.random.normal(-1.0 / (2.0 * M), 1.0 / (2.0 * M), M)

    for _ in range(num_iter):
        W -= (10 ** (-19)) * X.T.dot((X.dot(W) - Y) * 2)

    return W


def sgd(dataset):
    X = np.array(dataset.X)
    Y = np.array(dataset.Y)
    M = dataset.M
    W = np.random.normal(-1.0 / (2.0 * M), 1.0 / (2.0 * M), M)

    Q = np.sum((Y - X.dot(W)) ** 2) / Y.size
    I = 0
    while Q > 0.0001 and I < MAX_ITER:
        W -= (10 ** (-19)) * X.T.dot((X.dot(W) - Y) * 2)
        Q = np.sum((Y - X.dot(W)) ** 2) / Y.size
        I += 1

    return W


def svd(dataset):
    X = np.array(dataset.X)
    Y = np.array(dataset.Y)

    return np.matmul(np.linalg.pinv(X), Y)


def nrmse(dataset, W):
    X = np.array(dataset.X)
    Y = np.array(dataset.Y)

    return sqrt(np.sum((Y - (X @ W)) ** 2) / Y.size) / (np.max(Y) - np.min(Y))


for i in range(NUM_DATA):
    print("Dataset #" + str(i + 1))

    train, test = get_data(DATA_PATH + str(i + 1) + ".txt")

    gradient_descent_nrmse = nrmse(test, sgd(train))
    print("Gradient Descent NRMSE: '" + str(gradient_descent_nrmse) + "'")

    svd_nrmse = nrmse(test, svd(train))
    print("SVD NRMSE: '" + str(svd_nrmse) + "'")

for i in range(NUM_DATA):
    train, test = get_data(DATA_PATH + str(i + 1) + ".txt")
    gradient_descent_nrmse_train = []
    gradient_descent_nrmse_test = []

    for iter_number in range(0, 2000, 100):
        gradient_descent_nrmse_train.append(nrmse(train, sgd_num_iter(train, iter_number)))
        gradient_descent_nrmse_test.append(nrmse(test, sgd_num_iter(test, iter_number)))

    plt.plot(range(0, 2000, 100), gradient_descent_nrmse_train, range(0, 2000, 100), gradient_descent_nrmse_test)
    plt.ylabel('Gradient Descent NRMSE')
    plt.xlabel('Number of iterations')
    plt.title('Dataset #' + str(i + 1))
    plt.legend(('Train', 'Test'), loc='upper right')
    plt.show()
