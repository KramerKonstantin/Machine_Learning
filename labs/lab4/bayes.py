from collections import defaultdict
from math import log


SPAM = "spmsg"
LEGIT = "legit"


def train(data):
    classes = defaultdict(lambda: 0)
    freq = defaultdict(lambda: 0)
    count_word = defaultdict(lambda: 0)

    for label, message in data:
        classes[label] += len(message)

        for word in message:
            freq[label, tuple(word)] += 1.0
            count_word[tuple(word)] += 1.0

    for c in classes:
        classes[c] /= len(data)

    return classes, freq, count_word


def classify(classifier, message, lambda_spam, lambda_legit, alpha):
    classes, freq, count_word = classifier
    probability_spam = log(classes[SPAM]) + log(lambda_spam)
    probability_legit = log(classes[LEGIT]) + log(lambda_legit)

    for word in message:
        probability_spam += log((freq[SPAM, tuple(word)] + alpha) / (count_word[tuple(word)] + alpha * len(count_word)))
        probability_legit += log((freq[LEGIT, tuple(word)] + alpha) / (count_word[tuple(word)] + alpha * len(count_word)))

    s = probability_spam / (probability_spam + probability_legit)
    l = probability_legit / (probability_spam + probability_legit)

    if probability_spam > probability_legit:
        return SPAM, s

    return LEGIT, l
