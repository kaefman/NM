import sys
import matplotlib.pyplot as plt
import numpy as np

def find_polinom(a_koef, x):
    sum = 0
    for i in range(len(a_koef)):
        sum += a_koef[i] * x ** i
    return sum

def grafics(X, Fun, a_koef1, a_koef2):
    x = np.linspace(0.1, 2.1, 100)
    y1 = [find_polinom(a_koef1, i) for i in x]
    y2 = [find_polinom(a_koef2, i) for i in x]
    fig, ax = plt.subplots()
    ax.grid()
    ax.plot(x, y1, label = 'Многочлен 1-ой степени')
    ax.plot(x, y2, label = 'Многочлен 2-ой степени')
    ax.scatter(X, Fun, c="r", label = 'Точки финкции')
    ax.legend()
    fig.set_figheight(5)
    fig.set_figwidth(8)
    plt.show()

def errorMessage():
    print("Использование:\n"
    "{0} --load <testFile>\tзагрузка списков из файла\n"
    "{0} --runtime\t\tнабор списков от руки\n".format(sys.argv[0]))
    sys.exit(1)

def input_points(X, Fun):
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
                X = i.split()
                count += 1
                continue
            if count == 2:
                Fun = i.split()
                count += 1
    elif sys.argv[1] == "--runtime" and len(sys.argv) == 2:
        X = input("Введите список значений X: ").split()
        Fun = input("Введите список значений Fun: ").split()
    else:
        errorMessage()
    for i in range(len(X)):
        X[i] = float(X[i])
    for i in range(len(Fun)):
        Fun[i] = float(Fun[i])
    return [X, Fun]

def print_polynom(a_koef):
    for i in range(len(a_koef)):
        if i == 0:
            print(a_koef[i], end = " ")
        else:
            print("+ " + str(a_koef[i]) + "*x^" + str(i), end = " ")
    print("")

def nul_vector(b, n):
    for i in range(n):
        b.append(int(0))

def nul_matrix(matrix, n):
    line_mat2 = []
    for i in range(n):
        for j in range(n):
            line_mat2.append(int(0))
        else:
            matrix.append(line_mat2)
            line_mat2 = []

def sum_X(X, k):
    sum = 0
    for i in range(len(X)):
        sum += X[i] ** k
    return sum

def sum_Fun(Fun, X, k):
    sum = 0
    for i in range(len(Fun)):
        sum += Fun[i] * X[i] ** k
    return sum

def get_Ab(A, b, p, X, Fun):
    nul_matrix(A, p+1)
    nul_vector(b, p+1)
    for i in range(len(A)):
        for j in range(len(A)):
            if i == 0 and j == 0:
                A[i][j] = len(Fun)
                continue
            A[i][j] = sum_X(X, i + j)
        b[i] = sum_Fun(Fun, X, i)
    return [A, b]

def LU(A, L, U, n):
    for i in range(n):
        j = i
        while j < n:
            U[i][j] = A[i][j]
            L[j][i] = float(A[j][i]) / float(A[i][i])
            j += 1
        k = i
        while k < n - 1:
            j = i
            koef = float(A[k + 1][i]) / float(A[i][i])
            while j < n:
                A[k + 1][j] = float(A[k + 1][j]) - koef * float(A[i][j])
                j += 1
            k += 1 

def solveLU(L, U, n, b):
    Y = []
    Y.append(float(b[0]))
    X = []
    for i in range(1, n):
        sum = 0
        for j in range(i):
            sum += float(Y[j]) * float(L[i][j])
        Y.append(float(b[i]) - sum)
    #Зануляем вектор
    for i in range(n):
        X.append(float(0))
    i = n - 1
    while i > -1:
        sum = 0
        for j in range(i + 1, n):
            sum += U[i][j] * X[j]
        X[i] = float(1 / U[i][i] * (Y[i] - sum))
        i -= 1
    return X

def Gaus(A, b):
    L, U = [], []
    nul_matrix(L, len(A))
    nul_matrix(U, len(A))
    LU(A, L, U, len(A))
    res = solveLU(L, U, len(A), b)
    return res

def MNK(X, Fun, p):
    A, b, a_koef = [], [], []
    A, b = get_Ab(A, b, p, X, Fun)
    a_koef = Gaus(A, b)
    return a_koef

def get_sum_error(a_koef, X, Fun):
    sum = 0
    for i in range(len(X)):
        sum += (find_polinom(a_koef, X[i]) - Fun[i])**2
    return sum

def main():
    X, Fun, a_koef1, a_koef2, sum_error = [], [], [], [], 0
    X, Fun = input_points(X, Fun)
    print("Многочлен 1-ой степени:")
    a_koef1 = MNK(X, Fun, 1)
    print_polynom(a_koef1)
    sum_error = get_sum_error(a_koef1, X, Fun)
    print("Сумма квадратов ошибок:\t", sum_error)
    print("Многочлен 2-ой степени:")
    a_koef2 = MNK(X, Fun, 2)
    print_polynom(a_koef2)
    sum_error = get_sum_error(a_koef2, X, Fun)
    print("Сумма квадратов ошибок:\t", sum_error)
    grafics(X, Fun, a_koef1, a_koef2)

if __name__ == "__main__":
    main()