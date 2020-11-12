from core import *


N = 3


for n in range(N):
    print("N =", n + 1)
    parts = read_parts(n + 1)

    best_alpha = get_best_alpha(parts)

    if n == 0:
        draw_roc(parts, best_alpha)

    # get_lambda(parts, best_alpha)

    draw_accuracy_from_lambda(parts, best_alpha)
    print()
