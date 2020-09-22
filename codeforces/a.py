N, M, K = map(int, input().split())
C = list(map(int, input().split()))

a = sorted([(C[i], i + 1) for i in range(N)], key=lambda x: x[0])

parts = [[] for i in range(K)]
for i in range(N):
    parts[i % K].append(a[i][1])

for part in parts:
    print(len(part), *sorted(part))

