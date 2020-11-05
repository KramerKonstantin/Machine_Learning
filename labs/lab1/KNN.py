from math import sqrt
from read_data import get_data
from metric_functions import get_kernel, get_distance
from f_score import get_f_score
from draughtsman import draw


filename = 'dataset_191_wine.csv'

X, Y = get_data(filename)

h_max = int(sqrt(abs(len(X))))

DISTANCE_NAMES = ['manhattan', 'euclidean', 'chebyshev']
KERNEL_NAMES = ['uniform', 'triangular', 'epanechnikov', 'quartic']
WINDOW_TYPES = ['fixed', 'variable']

max_f_score = -1
win_kernel = ""
win_distance = ""
win_window = ""

for window_type in WINDOW_TYPES:
    print('Window type: ' + window_type)
    is_fixed = window_type == 'fixed'

    for distance_name in DISTANCE_NAMES:
        print('    ' * 1 + 'Distance function: ' + distance_name)
        distance = get_distance(distance_name)

        for kernel_name in KERNEL_NAMES:
            print('    ' * 2 + 'Kernel function: ' + kernel_name)
            kernel = get_kernel(kernel_name)

            for h in range(1, h_max):
                print('    ' * 3 + 'Window size: ' + str(h))
                f1_score = get_f_score(X, Y, is_fixed, distance, kernel, h)
                print('    ' * 3 + 'F1 score: ' + str(f1_score))

                if f1_score >= max_f_score:
                    max_f_score = f1_score
                    win_kernel = kernel_name
                    win_distance = distance_name
                    win_window = window_type
    print("\n")

draw(X, Y, max_f_score, win_window, win_distance, win_kernel, h_max)
