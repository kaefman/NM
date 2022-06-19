import sys
import matplotlib.pyplot as plt
import numpy as np

def grafics(X1, X2):
    x = np.linspace(0, 1.5, 100)
    y1 = [Lagrange(X1, i) for i in x]
    y2 = [function(i) for i in x]
    y3 = [Newton(X1, i) for i in x]
    y4 = [function(i) for i in X1]
    y5 = [Lagrange(X2, i) for i in x]
    y6 = [Newton(X2, i) for i in x]
    y7 = [function(i) for i in X2]
    plt.subplot(2, 2, 1)
    plt.grid()
    plt.plot(x, y1, label = 'Лагранж')
    plt.plot(x, y2, label = 'f(x)')
    plt.scatter(X1, y4, c="r", label = 'Точки финкции1')
    plt.legend()
    plt.subplot(2, 2, 2)
    plt.grid()
    plt.plot(x, y3, label = 'Ньютон')
    plt.plot(x, y2, label = 'f(x)')
    plt.scatter(X1, y4, c="r", label = 'Точки финкции1')
    plt.legend()
    plt.subplot(2, 2, 3)
    plt.grid()
    plt.plot(x, y5, label = 'Лагранж')
    plt.plot(x, y2, label = 'f(x)')
    plt.scatter(X2, y7, c="r", label = 'Точки финкции2')
    plt.legend()
    plt.subplot(2, 2, 4)
    plt.grid()
    plt.plot(x, y6, label = 'Ньютон')
    plt.plot(x, y2, label = 'f(x)')
    plt.scatter(X2, y7, c="r", label = 'Точки финкции2')
    plt.legend()
    plt.show()

def errorMessage():
    print("Использование:\n"
    "{0} --load <testFile>\tзагрузка списков из файла\n"
    "{0} --runtime\t\tнабор списков от руки\n".format(sys.argv[0]))
    sys.exit(1)

def nul_matrix(matrix, n):
    line_mat2 = []
    for i in range(n):
        for j in range(n):
            line_mat2.append(int(0))
        else:
            matrix.append(line_mat2)
            line_mat2 = []

def input_points(X1, X2, X3):
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
                X2 = i.split()
                count += 1
                continue
            if count == 3:
                X3 = float(i)
    elif sys.argv[1] == "--runtime" and len(sys.argv) == 2:
        X1 = input("Введите список значений X1: ").split()
        X2 = input("Введите список значений X2: ").split()
        X3 = float(input("Введите значение X*: "))
    else:
        errorMessage()
    for i in range(len(X1)):
        X1[i] = float(X1[i])
    for i in range(len(X2)):
        X2[i] = float(X2[i])
    return [X1, X2, X3]

def function(x):
    return 1/x + x

def fun_w(X, i, x0):
    mult_w = 1
    for j in range(len(X)):
        if j == i:
            continue
        mult_w *= x0 - X[j]
    return mult_w

def com_w(X, i):
    mult_w = 1
    for j in range(len(X)):
        if j == i:
            continue
        mult_w *= X[i] - X[j]
    return mult_w 

def show_polynom_L(X):
    print("\nПолином Логранжа: ", end = "")
    for i in range(len(X)):
        k = function(X[i]) / com_w(X, i)
        buf = X.copy()
        buf.pop(i)
        if i == 0:
            print("({0}(x - {1})(x - {2})(x - {3}))".format(k, buf[0], buf[1], buf[2]), end = " ")
        else:
            print("+ ({0}(x - {1})(x - {2})(x - {3}))".format(k, buf[0], buf[1], buf[2]), end = " ")
    print("\n")

def Lagrange(X, x0):
    sum_lagr = 0
    for i in range(len(X)):
        sum_lagr += function(X[i]) / com_w(X, i) * fun_w(X, i, x0)
    return sum_lagr

def new_func(fun1, fun2, j, k):
    return (fun1 - fun2) / (j - k)

def get_fun_mat(A, X):
    nul_matrix(A, len(X))
    for i in range(len(X)):
        A[i][i] = function(X[i])
    for i in range(1, len(X)):
        j = i
        k = 0
        while j < len(X):
            A[j][k] = new_func(A[j][k + 1], A[j - 1][k], X[j], X[k])
            j += 1
            k += 1
    return A

def mult_koef(X, x0, i):
    m_k = 1
    for i in range(i):
        m_k *= x0 - X[i]
    return m_k

def show_polynom_N(X):
    fun_mat = []
    fun_mat = get_fun_mat(fun_mat, X)
    print("\nПолином Ньютона: ", end = "")
    print("({0}) + ({1})(x - {2}) + ({3})(x - {2})(x - {4}) + ({5})(x - {2})(x - {4})(x - {6})".format(function(X[0]), fun_mat[1][0], X[0], fun_mat[2][0], X[1], fun_mat[3][0], X[2]))
    print("\n")

def Newton(X, x0):
    fun_mat, sum_newton = [], function(X[0])
    fun_mat = get_fun_mat(fun_mat, X)
    for i in range(1, len(X)):
        sum_newton += mult_koef(X, x0, i) * fun_mat[i][0]
    return sum_newton

def main():
    X1, X2, X3 = [], [], 0
    X1, X2, X3 = input_points(X1, X2, X3)
    lagr = Lagrange(X1, X3)
    newt = Newton(X1, X3)
    y = function(X3)
    error1 = y - lagr
    error2 = y - newt
    print("Список точек:\t", X1)
    show_polynom_L(X1)
    show_polynom_N(X1)
    print("Значение по Лагранжу:\t", lagr)
    print("Значение по Ньютону\t", newt)
    print("Реальное значение:\t", y)
    print("Абсолютная погрешность по Логранжу:\t", error1)
    print("Абсолютная погрешность по Ньютону:\t", error2)
    lagr = Lagrange(X2, X3)
    newt = Newton(X2, X3)
    error1 = y - lagr
    error2 = y - newt
    print("\nСписок точек:\t", X2)
    show_polynom_L(X2)
    show_polynom_N(X2)
    print("Значение по Лагранжу:\t", lagr)
    print("Значение по Ньютону\t", newt)
    print("Реальное значение:\t", y)
    print("Абсолютная погрешность по Логранжу:\t", error1)
    print("Абсолютная погрешность по Ньютону:\t", error2)
    grafics(X1, X2)

if __name__ == "__main__":
    main()