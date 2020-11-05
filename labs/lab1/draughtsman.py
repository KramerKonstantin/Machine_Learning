import matplotlib.pyplot as plt
from f_score import get_f_score
from metric_functions import get_kernel, get_distance


def draw(x, y, max_f_score, window_type, distance_name, kernel_name, h_max):
    print("Max F Scores: " + str(max_f_score))
    print("Window type: " + window_type)
    print("Distance name: " + distance_name)
    print("Kernel name: " + kernel_name)

    is_fixed = window_type == "fixed"
    distance = get_distance(distance_name)
    kernel = get_kernel(kernel_name)

    f1_scores = list()
    for h in range(1, h_max):
        f1_score = get_f_score(x, y, is_fixed, distance, kernel, h)
        f1_scores.append(f1_score)
    plt.plot(range(1, h_max), f1_scores)
    plt.xlabel('Window size')
    plt.ylabel('FScore')
    plt.show()
