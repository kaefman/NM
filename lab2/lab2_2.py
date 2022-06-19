import math
import numpy as np
import matplotlib.pyplot as plt

def nul_matrix(matrix, n):
    line_mat2 = []
    for i in range(n):
        for j in range(n):
            line_mat2.append(int(0))
        else:
            matrix.append(line_mat2)
            line_mat2 = []

def grafic():
    x = np.linspace(-10, 10, 200)
    y1 = [gfunction1(i) for i in x]
    y2 = [gfunction2(i) for i in x]
    y3 = [gfunction3(i) for i in x]
    plt.title("График исходной системы функций")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    plt.plot(x, y1, x, y2, x, y3)
    plt.show()

def gfunction1(x):
    try:
        return (1 + math.sqrt(-4*x**2 + 5)) / 2
    except ValueError:
        return 0

def gfunction2(x):
    try:
        return (1 - math.sqrt(-4*x**2 + 5)) / 2
    except ValueError:
        return 0

def gfunction3(x):
    return (x + 1)**2 - 1

def function1(x, y):
    return x**2 - y + y**2 - 1

def function2(x, y):
    return x - math.sqrt(y + 1) + 1

def dif_fun1x(x, y):
    return 2*x

def dif_fun1y(x, y):
    return 2*y - 1

def dif_fun2x(x, y):
    return 1

def dif_fun2y(x, y):
    return 1/2 / math.sqrt(y + 1)

def det(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]

def fA1(x0, A1):
    A1[0][0] = function1(x0[0], x0[1])
    A1[1][0] = function2(x0[0], x0[1])
    A1[0][1] = dif_fun1y(x0[0], x0[1])
    A1[1][1] = dif_fun2y(x0[0], x0[1])
    return A1

def fA2(x0, A2):
    A2[0][0] = dif_fun1x(x0[0], x0[1])
    A2[1][0] = dif_fun2x(x0[0], x0[1])
    A2[0][1] = function1(x0[0], x0[1])
    A2[1][1] = function2(x0[0], x0[1])
    return A2

def norma(x):
    return max(abs(x[0]), abs(x[1]))

def fJ(x0, J):
    J[0][0] = dif_fun1x(x0[0], x0[1])
    J[1][0] = dif_fun2x(x0[0], x0[1])
    J[0][1] = dif_fun1y(x0[0], x0[1])
    J[1][1] = dif_fun2y(x0[0], x0[1])
    return J

def Newton(x0, e):
    count = 1
    A1, A2, J = [], [], []
    nul_matrix(A1, 2)
    nul_matrix(A2, 2)
    nul_matrix(J, 2)
    A1 = fA1(x0, A1)
    A2 = fA2(x0, A2)
    J = fJ(x0, J)
    x1 = [x0[0] - det(A1) / det(J), x0[1] - det(A2) / det(J)]
    while norma([x1[0] - x0[0], x1[1] - x0[1]]) > e:
        x0 = x1
        A1 = fA1(x0, A1)
        A2 = fA2(x0, A2)
        J = fJ(x0, J)
        x1 = [x0[0] - det(A1) / det(J), x0[1] - det(A2) / det(J)]
        count += 1
    return [x1, count]

def fi1(x, y):
    return math.sqrt(y + 1) - 1

def fi2(x, y):
    return math.sqrt(y - x**2 + 1)

def dif_fi1x(x, y):
    return 0

def dif_fi1y(x, y):
    return 1/2 / math.sqrt(y + 1)

def dif_fi2x(x, y):
    return x / math.sqrt(y - x**2 + 1)

def dif_fi2y(x, y):
    return 1/2 / math.sqrt(y - x**2 + 1)

def get_fi_dif(x0, fi_dif):
    nul_matrix(fi_dif, 2)
    fi_dif[0][0] = dif_fi1x(x0[0], x0[1])
    fi_dif[0][1] = dif_fi1y(x0[0], x0[1])
    fi_dif[1][0] = dif_fi2x(x0[0], x0[1])
    fi_dif[1][1] = dif_fi2y(x0[0], x0[1])
    return fi_dif

def get_q(fi_dif):
    return max(abs(fi_dif[0][0]) + abs(fi_dif[0][1]), abs(fi_dif[1][0]) + abs(fi_dif[1][1]))

def simple_iteration(x0, e):
    count, fi_dif, q = 1, [], 0
    fi_dif = get_fi_dif(x0, fi_dif)
    q = get_q(fi_dif)
    x1 = [fi1(x0[0], x0[1]), fi2(x0[0], x0[1])]
    while q/(1-q)*norma([x1[0] - x0[0], x1[1] - x0[1]]) > e:
        x0 = x1
        x1 = [fi1(x0[0], x0[1]), fi2(x0[0], x0[1])]
        count += 1
    return [x1, count]

def main():
    e = float(input("Введите точность вычислений: "))
    grafic()
    x0 = input("Введите начальное приближение: ").split()
    x0[0], x0[1] = float(x0[0]), float(x0[1])
    answer, count = Newton(x0, e)
    print("Метод Ньютона")
    print("Положительный корень уравнения - x* = ({0}, {1}). Количество итераций - {2}.".format(answer[0], answer[1], count))
    print("Проверка метода Ньютона:\nf1({0}) = {1}\nf2({2}) = {3}".format(answer[0], function1(answer[0], answer[1]), answer[1], function2(answer[0], answer[1])))
    answer, count = simple_iteration(x0, e)
    print("Метод простых итераций")
    print("Положительный корень уравнения - x* = ({0}, {1}). Количество итераций - {2}.".format(answer[0], answer[1], count))
    print("Проверка метода простых итераций:\nf1({0}) = {1}\nf2({2}) = {3}".format(answer[0], function1(answer[0], answer[1]), answer[1], function2(answer[0], answer[1])))

if __name__ == "__main__":
    main()