import math
import copy


def matrix_product(a, b):
    c = [[0] * len(b[0]) for _ in range(len(a))]

    for i in range(len(a)):
        for j in range(len(b[0])):
            for t in range(len(a[0])):
                c[i][j] += a[i][t] * b[t][j]

    return c


def transpose(a):
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]


def get_df(a):
    a.out_df = [[0] * a.c for _ in range(a.r)]
    for df in a.input_df:
        for i in range(a.r):
            for j in range(a.c):
                a.out_df[i][j] += df[i][j]


class Node:
    def __init__(self):
        super().__init__()
        self.input_df = []
        self.values = []
        self.r = None
        self.c = None
        self.out_df = None

    def calculate(self):
        pass

    def back(self):
        pass


class Var(Node):
    def __init__(self, r, c):
        super().__init__()
        self.r = r
        self.c = c

    def calculate(self):
        pass

    def back(self):
        get_df(self)


class Tnh(Node):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.r = x.r
        self.c = x.c

    def calculate(self):
        self.values = list(map(lambda row: list(map(math.tanh, row)), self.x.values))

    def back(self):
        get_df(self)

        df = copy.deepcopy(self.out_df)
        for i in range(self.r):
            for j in range(self.c):
                x = self.values[i][j]
                df[i][j] *= (1 - x ** 2)

        self.x.input_df.append(df)


class Rlu(Node):
    def __init__(self, alpha, x):
        super().__init__()
        self.alpha = alpha
        self.x = x
        self.r = x.r
        self.c = x.c

    def calculate(self):
        self.values = list(map(lambda row: list(map(lambda x: self.alpha * x if x < 0 else x, row)), self.x.values))

    def back(self):
        get_df(self)

        df = copy.deepcopy(self.out_df)
        for i in range(self.r):
            for j in range(self.c):
                x = self.x.values[i][j]
                df[i][j] *= self.alpha if x < 0 else 1

        self.x.input_df.append(df)


class Mul(Node):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
        self.r = a.r
        self.c = b.c

    def calculate(self):
        self.values = matrix_product(self.a.values, self.b.values)

    def back(self):
        get_df(self)

        self.a.input_df.append(matrix_product(self.out_df, transpose(self.b.values)))
        self.b.input_df.append(matrix_product(transpose(self.a.values), self.out_df))


class Sum(Node):
    def __init__(self, u):
        super().__init__()
        self.u = u
        self.r = u[0].r
        self.c = u[0].c

    def calculate(self):
        self.values = copy.deepcopy(self.u[0].values)
        for u_i in self.u[1:]:
            for i in range(self.r):
                for j in range(self.c):
                    self.values[i][j] += u_i.values[i][j]

    def back(self):
        get_df(self)

        for u_i in self.u:
            u_i.input_df.append(self.out_df)


class Had(Node):
    def __init__(self, u):
        super().__init__()
        self.u = u
        self.r = u[0].r
        self.c = u[0].c

    def calculate(self):
        self.values = copy.deepcopy(self.u[0].values)
        for u_i in self.u[1:]:
            for i in range(self.r):
                for j in range(self.c):
                    self.values[i][j] *= u_i.values[i][j]

    def back(self):
        get_df(self)

        l = len(self.u)
        for index1 in range(l):
            u_i1 = self.u[index1]
            df = copy.deepcopy(self.out_df)
            for index2 in range(l):
                u_i2 = self.u[index2]
                if index1 != index2:
                    for i in range(self.r):
                        for j in range(self.c):
                            df[i][j] *= u_i2.values[i][j]

            u_i1.input_df.append(df)


N, M, K = map(int, input().split())

nodes = []
for _ in range(M):
    s = input().split()
    r = int(s[1])
    c = int(s[2])

    node = Var(r, c)
    nodes.append(node)

for _ in range(N - M):
    s = input().split()
    node_type = s[0]

    if node_type == "tnh":
        x = nodes[int(s[1]) - 1]
        node = Tnh(x)
        nodes.append(node)
    elif node_type == "rlu":
        alpha = 1 / int(s[1])
        x = nodes[int(s[2]) - 1]
        node = Rlu(alpha, x)
        nodes.append(node)
    elif node_type == "mul":
        a = nodes[int(s[1]) - 1]
        b = nodes[int(s[2]) - 1]
        node = Mul(a, b)
        nodes.append(node)
    elif node_type == "sum":
        u = [nodes[int(u_i) - 1] for u_i in s[2:]]
        node = Sum(u)
        nodes.append(node)
    elif node_type == "had":
        u = [nodes[int(u_i) - 1] for u_i in s[2:]]
        node = Had(u)
        nodes.append(node)

for i in range(M):
    node = nodes[i]
    for _ in range(node.r):
        node.values.append(list(map(int, input().split())))

for i in range(N - K, N):
    node = nodes[i]
    df = []
    for _ in range(node.r):
        df.append(list(map(int, input().split())))

    node.input_df.append(df)

for node in nodes:
    node.calculate()

for node in reversed(nodes):
    node.back()

for i in range(N - K, N):
    for row in nodes[i].values:
        print(*row, sep=' ')

for i in range(M):
    for row in nodes[i].out_df:
        print(*row, sep=' ')
