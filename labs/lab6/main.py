import pandas as pd
from sklearn.metrics import accuracy_score
from ada_boost import AdaBoost
from draw import draw_dependency, draw_boost


PATH_CHIPS = 'data/chips.csv'
PATH_GEYSER = 'data/geyser.csv'


def get_data(file_path):
    dataset = pd.read_csv(file_path)
    dataset['class'] = dataset['class'].apply(lambda x: {
        'P': 1,
        'N': -1
    }[x])

    x = dataset.values[:, :-1]
    y = dataset.values[:, -1]

    return x, y

def do_boost(x, y, m):
    ada_boost = AdaBoost(x, y, m)
    accuracy = accuracy_score(ada_boost.predict(x), y)

    print("Шаг бустинга:", m)
    print("Точность:", accuracy)
    print()

    draw_boost(x, y, ada_boost)


# chips
X, Y = get_data(PATH_CHIPS)
draw_dependency(X, Y)
for t in [1, 2, 3, 5, 8, 13, 21, 34, 55]:
    do_boost(X, Y, t)

# geyser
# X, Y = get_data(PATH_GEYSER)
# draw_dependency(X, Y)
# for t in [1, 2, 3, 5, 8, 13, 21, 34, 55]:
#     do_boost(X, Y, t)
