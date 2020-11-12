import os
from bayes import train, classify
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


PATH = "messages/part"
COUNT_PARTS = 10
SPAM = "spmsg"
LEGIT = "legit"


def read_parts(n):
    parts = []
    for i in range(COUNT_PARTS):
        path = PATH + str(i + 1)
        part = []

        names = os.listdir(path)
        for name in names:
            file = open(path + "/" + name, 'r')
            subject = file.readline().split()[1:]
            file.readline()
            body = file.readline().split()

            subject_n_gram = []
            for j in range(len(subject) - n + 1):
                n_gram = []
                for t in range(n):
                    n_gram.append(subject[j + t])

                subject_n_gram.append(n_gram)

            body_n_gram = []
            for j in range(len(body) - n + 1):
                n_gram = []
                for t in range(n):
                    n_gram.append(body[j + t])

                body_n_gram.append(n_gram)

            words = subject_n_gram + body_n_gram

            if SPAM in name:
                part.append((SPAM, words))
            else:
                part.append((LEGIT, words))

        parts.append(part)

    return parts


def get_best_alpha(parts):
    best_accuracy = 0
    best_alpha = 0

    for alpha_degree in range(0, 10):
        alpha = 1 / (10 ** alpha_degree)
        sum_accuracy_score = 0

        for d_test in parts:
            d_train = []
            predict = []
            answer = []

            for part in parts:
                if part != d_test:
                    d_train = d_train + part

            bayes = train(d_train)

            for answer_class, message in d_test:
                predict_class, _ = classify(bayes, message, 1, 1, alpha)
                predict.append(int(predict_class == SPAM))
                answer.append(int(answer_class == SPAM))

            sum_accuracy_score += accuracy_score(predict, answer)

        accuracy = sum_accuracy_score / COUNT_PARTS
        if best_accuracy < accuracy:
            best_accuracy = accuracy
            best_alpha = alpha

        print('alpha:', alpha, 'accuracy:', accuracy)

    print("__________________________________________")
    print("Best alpha:", best_alpha)
    print("Best accuracy:", best_accuracy)
    print("__________________________________________")

    return best_alpha


def draw_roc(parts, alpha):
    d_train = []

    for part in parts:
        d_train = d_train + part

    bayes = train(d_train)

    roc_c = []
    roc_pred = []
    count_y = 0
    count_x = 0
    for answer_class, message in d_train:
        predict_class, pred = classify(bayes, message, 1, 1, alpha)

        if predict_class == answer_class:
            count_y += 1
            roc_c.append(True)
        else:
            count_x += 1
            roc_c.append(False)

        roc_pred.append(pred)

    roc_c, roc_pred = zip(*sorted(zip(roc_c, roc_pred), key=lambda x: x[1]))

    if count_y == 0:
        count_y = 1

    if count_x == 0:
        count_x = 1

    shag_x = 1 / count_x
    shag_y = 1 / count_y
    X = []
    Y = []
    x = 0
    y = 0
    X.append(x)
    Y.append(y)
    for t in roc_c:
        if t:
            y += shag_y
        else:
            x += shag_x

        X.append(x)
        Y.append(y)

    plt.plot(X, Y)
    plt.show()


def get_lambda(parts, alpha):
    for i in range(0, 101, 5):
        lambda_legit = 10 ** i
        sum_accuracy_score = 0
        cnt = 0
        for test in parts:
            d_tran = []
            predict = []
            answer = []

            for part in parts:
                if part != test:
                    d_tran = d_tran + part

            bayes = train(d_tran)

            for answer_class, message in test:
                predict_class, _ = classify(bayes, message, 1, lambda_legit, alpha)
                predict.append(int(predict_class == SPAM))
                answer.append(int(answer_class == SPAM))

                if predict_class == SPAM and answer_class == LEGIT:
                    cnt += 1

            sum_accuracy_score += accuracy_score(predict, answer)

        print("cnt:", cnt, "lambda:", 10 ** i)


def draw_accuracy_from_lambda(parts, alpha):
    all_lambda_legit = []
    all_accuracy = []

    for i in range(0, 101, 5):
        lambda_legit = 10 ** i
        sum_accuracy_score = 0

        for test in parts:
            d_train = []
            predict = []
            answer = []

            for part in parts:
                if part != test:
                    d_train = d_train + part

            bayes = train(d_train)

            for answer_class, message in test:
                predict_class, _ = classify(bayes, message, 1, lambda_legit, alpha)
                predict.append(int(predict_class == SPAM))
                answer.append(int(answer_class == SPAM))

            sum_accuracy_score += accuracy_score(predict, answer)

        accuracy = sum_accuracy_score / COUNT_PARTS
        all_lambda_legit.append(i)
        all_accuracy.append(accuracy)
        print("lambda:", lambda_legit, "accuracy:", accuracy)

    plt.plot(all_lambda_legit, all_accuracy)
    plt.xlabel('10^x lambda legit')
    plt.ylabel('Accuracy')
    plt.show()
