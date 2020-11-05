import pandas as pd


def get_minmax(dataset):
    minmax = list()
    for i in range(len(dataset[0])):
        value_min = dataset[:, i].min()
        value_max = dataset[:, i].max()
        minmax.append([value_min, value_max])

    return minmax


def normalize(dataset, minmax):
    for row in dataset:
        for i in range(len(row)):
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])

    return dataset


def get_data(file_path):
    dataset = pd.read_csv(file_path)

    dataset['class'] = dataset['class'].apply(lambda name: {
            1: [1.0, 0.0, 0.0],
            2: [0.0, 1.0, 0.0],
            3: [0.0, 0.0, 1.0]
        }[name])

    data_values = dataset[dataset.columns[1:]].values.astype(float)

    min_max = get_minmax(data_values)

    x = pd.DataFrame(normalize(data_values, min_max))
    y = pd.DataFrame(dataset['class'].values)

    return x, y
