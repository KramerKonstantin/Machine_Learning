K = int(input())
CM = []
for i in range(K):
    CM.append(list(map(int, input().split())))

ALL = sum([sum(CM[i]) for i in range(K)])
RECALL = [0] * K
PRECISION = [0] * K
F = [0] * K

for i in range(K):
    ALL_IN_LINE = sum(CM[i])
    ALL_IN_COLUMN = sum([CM[j][i] for j in range(K)])

    RECALL[i] = CM[i][i] / ALL_IN_LINE if ALL_IN_LINE != 0 else 0
    PRECISION[i] = CM[i][i] / ALL_IN_COLUMN if ALL_IN_COLUMN != 0 else 0

    weight = ALL_IN_LINE / ALL if ALL != 0 else 0
    F[i] = (2 * RECALL[i] * PRECISION[i] / (RECALL[i] + PRECISION[i])) * weight if RECALL[i] + PRECISION[i] != 0 else 0
    RECALL[i] *= weight
    PRECISION[i] *= weight

SUM_R = sum(RECALL)
SUM_P = sum(PRECISION)
MACRO_F = (2 * SUM_R * SUM_P / (SUM_R + SUM_P)) if SUM_R + SUM_P != 0 else 0
MICRO_F = sum(F)

print(MACRO_F)
print(MICRO_F)
