import sys
import matplotlib.pyplot as plt
import numpy as np

flag = 0

def grafic(X, Fun):
    x = np.linspace(0.1, 1.7 - sys.float_info.epsilon, 100)
    y1 = [get_res(X, Fun, i)[0] for i in x]
    fig, ax = plt.subplots()
    ax.grid()
    ax.plot(x, y1, label = 'Сплайн')
    ax.scatter(X, Fun, c="r", label = 'Точки финкции')
    ax.legend()
    fig.set_figheight(5)
    fig.set_figwidth(8)
    plt.show()

def nul_matrix(matrix, n):
    line_mat2 = []
    for i in range(n):
        for j in range(n):
            line_mat2.append(int(0))
        else:
            matrix.append(line_mat2)
            line_mat2 = []

def nul_vector(b, n):
    for i in range(n):
        b.append(int(0))

def progonka(A, b, n):
    P, Q, X = [], [], []
    nul_vector(P, n)
    nul_vector(Q, n)
    nul_vector(X, n)
    P[0], Q[0] = -A[0][1] / A[0][0], b[0] / A[0][0]
    for i in range(1, n - 1):
        P[i] = -A[i][i + 1] / (A[i][i] + A[i][i - 1] * P[i - 1])
        Q[i] = (b[i] - A[i][i - 1] * Q[i - 1]) / (A[i][i] + A[i][i - 1] * P[i - 1])
    Q[n - 1] = (b[n - 1] - A[n - 1][n - 2] * Q[n - 2]) / (A[n - 1][n - 1] + A[n - 1][n - 2] * P[n - 2])
    X[n - 1] = Q[n - 1]
    i = n - 2
    while i > -1:
        X[i] = P[i] * X[i + 1] + Q[i]
        i -= 1
    return X

def errorMessage():
    print("Использование:\n"
    "{0} --load <testFile>\tзагрузка списков из файла\n"
    "{0} --runtime\t\tнабор списков от руки\n".format(sys.argv[0]))
    sys.exit(1)

def input_points(X1, Fun, X2):
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        errorMessage()
    if sys.argv[1] == "--load":
        if len(sys.argv) != 3:
            errorMessage()
        try:
            test_file = open(sys.argv[2], 'r')
        except FileNotFoundError:
            print("Файл {0} не найден. Исключение типа FileBotFoundError.".format(sys.argv[2]))
            quit()
        temp = test_file.read().splitlines()
        count = 1
        for i in temp:
            if count == 1:
                X1 = i.split()
                count += 1
                continue
            if count == 2:
                Fun = i.split()
                count += 1
                continue
            if count == 3:
                X2 = float(i)
    elif sys.argv[1] == "--runtime" and len(sys.argv) == 2:
        X1 = input("Введите список значений X1: ").split()
        X2 = input("Введите список значений Fun: ").split()
        X3 = float(input("Введите значение X*: "))
    else:
        errorMessage()
    for i in range(len(X1)):
        X1[i] = float(X1[i])
    for i in range(len(Fun)):
        Fun[i] = float(Fun[i])
    return [X1, Fun, X2]

def h_func(i, X):
    return X[i] - X[i - 1] 

def get_Ab(A, b, X, Fun):
    A[0][0] = 2 * (h_func(1, X) + h_func(2, X))
    A[0][1] = h_func(2, X)
    b[0] = 3 * ((Fun[2] - Fun[1]) / h_func(2, X) - (Fun[1] - Fun[0]) / h_func(1, X))
    k = 1
    for i in range(3, len(X) - 1):
        A[k][k - 1] = h_func(i - 1, X)
        A[k][k] = 2 * (h_func(i - 1, X) + h_func(i, X))
        A[k][k + 1] = h_func(i, X)
        b[k] = 3 * ((Fun[i] - Fun[i - 1]) / h_func(i, X) - (Fun[i - 1] - Fun[i - 2]) / h_func(i - 1, X))
        k += 1
    A[len(b) - 1][len(b) - 2] = h_func(len(b), X)
    A[len(b) - 1][len(b) - 1] = 2 * (h_func(len(b), X) + h_func(len(b) + 1, X))
    b[len(b) - 1] = 3 * ((Fun[len(b)+1] - Fun[len(b)]) / h_func(len(b)+1, X) - (Fun[len(b)] - Fun[len(b) - 1]) / h_func(len(b), X))
    return [A, b]

def position(X1, X2):
    count = 0
    for i in X1:
        if i > X2:
            break
        count += 1
    return count - 1

def show_spline(a, b, c, d, x):
    print("Сплайн как мат. объект:")
    for i in range(len(x) - 1):
        print("Отрезок [({0}), ({1})]:\t".format(x[i], x[i + 1]), end = "")
        print("({0}) + ({1})(x - {4}) + ({2})(x - {4})^2 + ({3})(x - {4})^3".format(a[i], b[i], c[i], d[i], x[i]))

def spline(a, b, c, d, x, x0):
    return a + b*(x0 - x) + c*(x0 - x)**2 + d*(x0 - x)**3

def get_res(X1, Fun, X2):
    A, b, c_koef, a_koef = [], [], [0], [Fun[i] for i in range(len(Fun) - 1)]
    nul_vector(b, len(X1) - 2)
    nul_matrix(A, len(X1) - 2)
    A, b = get_Ab(A, b, X1, Fun)
    c_koef = c_koef + progonka(A, b, len(b))
    b_koef = [(Fun[i + 1] - Fun[i]) / h_func(i + 1, X1) - 1/3 * h_func(i + 1, X1) * (c_koef[i + 1] + 2 * c_koef[i]) for i in range(len(c_koef) - 1)]
    d_koef = [(c_koef[i + 1] - c_koef[i]) / 3 / h_func(i + 1, X1) for i in range(len(c_koef) - 1)]
    b_koef.append((Fun[len(Fun) - 1] - Fun[len(Fun) - 2]) / h_func(len(Fun) - 1, X1) - 2/3 * h_func(len(Fun) - 1, X1) * c_koef[len(c_koef) - 1])
    d_koef.append((-1) * c_koef[len(c_koef) - 1] / 3 / h_func(len(c_koef), X1))
    pos = position(X1, X2)
    res = spline(a_koef[pos], b_koef[pos], c_koef[pos], d_koef[pos], X1[pos], X2)
    return [res, a_koef, b_koef, c_koef, d_koef]

def main():
    X1, Fun, X2 = [], [], 0
    X1, Fun, X2 = input_points(X1, Fun, X2)
    if X2 < X1[0] or X2 > X1[len(X1) - 1]:
        print("Искомое значение не находится между узлов интерполяции")
        quit()
    answer, a, b, c, d = get_res(X1, Fun, X2)
    show_spline(a, b, c, d, X1)
    print("Значение сплайна в точке X* = {0}:\t{1}".format(X2, answer))
    grafic(X1, Fun)

if __name__ == "__main__":
    main()