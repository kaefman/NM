import matplotlib.pyplot as plt
import numpy as np
import math

def function(x):
    try:
        return math.sqrt(x + 2) - 2 * math.cos(x)
    except ValueError:
        print("Значения аргумента функции не удовлетворяют ОДЗ")
        quit()

def dif_fun(x):
    return 1 / 2 / math.sqrt(x + 2) + 2 * math.sin(x)

def dif2_fun(x):
    return -1 / 4 * math.pow((x + 2), -3 / 2) + 2 * math.cos(x)

def grafic():
    x = np.linspace(-2, 10, 100)
    y = [function(i) for i in x]
    plt.title("График исходной функции")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    plt.plot(x, y) 
    plt.show()

def test_Newton(x):
    if (function(x) * dif2_fun(x) <= 0):
        print("Выбранная точка не удовлеворяет условию: f(x)*f''(x)>0")
        quit()

def fi(x):
    return math.acos(1 / 2 * math.sqrt(x + 2))

def dif_fi(x):
    return 1/4 * math.pow((x + 2), -1/2) * -1 / math.sqrt(1 - 1/4 * (x + 2))

def simple_iteration(x, a, b, e):
    q = max(abs(dif_fi(a)), abs(dif_fi(b)))
    count = 1
    x2 = fi(x)
    while (q / (1 - q) * abs(x2 - x)) > e:
        x = x2
        x2 = fi(x)
        count += 1
    return [x2, count]

def Newton(x, e):
    count = 1
    x2 = x - function(x)/dif_fun(x)
    while abs(x2 - x) > e:
        x = x2
        x2 = x - function(x)/dif_fun(x)
        count += 1
    return [x2, count]

def main():
    epsil = float(input("Введите точность вычислений: "))
    grafic()
    x0 = float(input("Введите начальную точку, определённую графически: "))
    a, b = input("Введите границы отрезка, определённые графичеки: ").split()
    test_Newton(x0)
    answer, count = Newton(x0, epsil)
    print("Метод Ньютона")
    print("Положительный корень уравнения - {0}. Количество итераций - {1}.".format(answer, count))
    print("Проверка метода Ньютона: f({0}) = {1}".format(answer, function(answer)))
    answer, count = simple_iteration(x0, float(a), float(b), epsil)
    print("Метод простых итераций")
    print("Положительный корень уравнения - {0}. Количество итераций - {1}.".format(answer, count))
    print("Проверка метода простых итераций: f({0}) = {1}".format(answer, function(answer)))

if __name__ == "__main__":
    main()