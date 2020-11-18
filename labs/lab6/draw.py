import numpy as np
import matplotlib.pyplot as plt
from ada_boost import AdaBoost
from sklearn.metrics import accuracy_score


def draw_boost(X, Y, ada_boost):
    x_min, y_min = np.amin(X, axis=0)
    x_max, y_max = np.amax(X, axis=0)
    x, y = np.meshgrid(np.arange(x_min, x_max, 0.005), np.arange(y_min, y_max, 0.005))
    dots = np.column_stack([x.reshape((-1)), y.reshape((-1))])
    predict = ada_boost.predict(dots)

    N_x, N_y = X[Y == -1].T
    P_x, P_y = X[Y == 1].T

    P_x_back = []
    P_y_back = []
    N_x_back = []
    N_y_back = []
    for i in range(len(dots)):
        if predict[i] == 1:
            P_x_back.append(dots[i][0])
            P_y_back.append(dots[i][1])

        if predict[i] == -1:
            N_x_back.append(dots[i][0])
            N_y_back.append(dots[i][1])

    plt.scatter(N_x_back, N_y_back, marker='.', color='#FFAAAA')
    plt.scatter(P_x_back, P_y_back, marker='.', color='#AAFFAA')
    plt.scatter(N_x, N_y, marker='_', color='red')
    plt.scatter(P_x, P_y, marker='+', color='green')
    plt.show()

def draw_dependency(X, Y):
    x = []
    y = []
    for i in range(1, 100):
        x.append(i)
        ada_boost = AdaBoost(X, Y, i)
        y.append(accuracy_score(ada_boost.predict(X), Y))

    plt.plot(x, y)
    plt.show()
