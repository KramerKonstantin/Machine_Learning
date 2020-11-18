import numpy as np
from sklearn.tree import DecisionTreeClassifier


class AdaBoost:
    def __init__(self, x, y, t):
        self.classifiers = []
        self.alphas = []

        N = len(x)
        D = np.ones(N) / N

        for _ in range(t):
            i = np.random.choice(N, N, p=D)
            classifier = DecisionTreeClassifier(max_depth=2).fit(x[i], y[i])
            self.classifiers.append(classifier)

            y_predict = classifier.predict(x)
            weighted_error = 0
            for i in range(len(y)):
                if y[i] != y_predict[i]:
                    weighted_error += D[i]
            alpha = 0.5 * np.log((1 - weighted_error) / weighted_error)
            self.alphas.append(alpha)

            D *= np.exp(-alpha * y * y_predict)
            D /= np.sum(D)

    def predict(self, x):
        return np.sign(sum([self.alphas[i] * self.classifiers[i].predict(x) for i in range(len(self.classifiers))]))
