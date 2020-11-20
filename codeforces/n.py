def get_distance(a):
    l = len(a)
    a.sort()
    distance = 0
    for i in range(1, l):
        distance += i * (l - i) * (a[i] - a[i - 1])

    return distance


K = int(input())
N = int(input())

X = []
Y = [[] for _ in range(K)]
for _ in range(N):
    x, y = map(int, input().split())
    X.append(x)
    Y[y - 1].append(x)

inter_class_distance = get_distance(X)
intra_class_distance = 0
for y in Y:
    intra_class_distance += get_distance(y)

print(intra_class_distance * 2)
print((inter_class_distance - intra_class_distance) * 2)
