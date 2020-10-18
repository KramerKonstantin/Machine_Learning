from math import log, exp


K = int(input())
lambda_c = list(map(int, input().split()))
alpha = int(input())
D_train = [{} for _ in range(K)]
C_count = [0 for _ in range(K)]
unique_words = set()
Q = 2

N = int(input())
for _ in range(N):
    line = input().split()
    C = int(line[0]) - 1
    L = int(line[1])
    words = set(line[2:])

    C_count[C] += 1

    for word in words:
        D_train[C].setdefault(word, 0)
        D_train[C][word] += 1

        unique_words.add(word)

M = int(input())
for _ in range(M):
    line = input().split()
    L = line[0]
    words = set(line[1:])

    answer = [0.0] * K
    for i in range(K):
        if C_count[i] != 0:
            answer[i] += log(C_count[i] / N * lambda_c[i])

            denominator = Q * alpha + C_count[i]
            for word in unique_words:
                if word in D_train[i]:
                    nominator = D_train[i][word] + alpha
                else:
                    nominator = alpha

                if word in words:
                    answer[i] += log(nominator) - log(denominator)
                else:
                    answer[i] += log(denominator - nominator) - log(denominator)

    MAX = max(answer)
    for i in range(K):
        answer[i] = exp(answer[i] - MAX) if (C_count[i] != 0) else 0

    SUM = sum(answer)
    for i in range(K):
        answer[i] = answer[i] / SUM

    print(*answer)
