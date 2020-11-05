def get_predict(test_x, train_x, train_y, is_fixed, h, kernel, distance):
    m = len(train_x)
    train_x = map(lambda x: distance(x, test_x), train_x)
    train_x, train_y = zip(*sorted(zip(train_x, train_y), key=lambda x: x[0]))

    if not is_fixed:
        h = train_x[h]

    best = 0
    t = -1

    for j in range(3):
        s1 = 0
        s2 = 0
        for i in range(m):
            w = kernel(0 if train_x[i] == 0 else (1 if h == 0 else train_x[i] / h))
            s1 += train_y[i][0][j] * w
            s2 += w

        res = 0
        try:
            res = s1 / s2
        except ZeroDivisionError:
            for i in range(m):
                res += train_y[i][0][j]
            res /= len(train_y)

        if res > best:
            best = res
            t = j

    return t


def my_f1_score(cm):
    k = len(cm)
    all = sum([sum(cm[i]) for i in range(k)])
    recall = [0] * k
    precision = [0] * k
    f = [0] * k

    for i in range(k):
        all_in_line = sum(cm[i])
        all_in_column = sum([cm[j][i] for j in range(k)])

        recall[i] = cm[i][i] / all_in_line if all_in_line != 0 else 0
        precision[i] = cm[i][i] / all_in_column if all_in_column != 0 else 0

        weight = all_in_line / all if all != 0 else 0
        f[i] = (2 * recall[i] * precision[i] / (recall[i] + precision[i])) * weight if recall[i] + precision[i] != 0 else 0

    micro_f = sum(f)

    return micro_f


def get_f_score(x, y, is_fixed, distance, kernel, h):
    n = len(x)
    confusion_matrix = [[0] * 3 for _ in range(3)]

    for i in range(n):
        train_x = x.drop(i).values.tolist()
        train_y = y.drop(i).values.tolist()
        test_x = x.iloc[i].values.tolist()
        test_y = y.iloc[i].values.tolist()

        predicted = get_predict(test_x, train_x, train_y, is_fixed, h, kernel, distance)
        actual = test_y[0].index(max(test_y[0]))

        confusion_matrix[predicted][actual] += 1

    return my_f1_score(confusion_matrix)
