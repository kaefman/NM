import math
import numpy as np
import matplotlib.pyplot as plt

def grafics(res, pure, h):
    n = len(res)
    for i in range(n):
        plt.subplot(n, 1, i + 1)
        plt.subplots_adjust(wspace=0.1, hspace=0.6)
        plt.plot(res[i]["Euler"]["x"], res[i]["Euler"]["y"], alpha=0.4, label='Метод Эйлера')
        plt.plot(res[i]["Runge"]["x"], res[i]["Runge"]["y"], alpha=0.4, label='Метод Рунге-Кутта')
        plt.plot(res[i]["Adams"]["x"], res[i]["Adams"]["y"], alpha=0.4, label='Метод Адамса')
        plt.plot(pure[i][0], pure[i][1], alpha=0.4, label='f(x)')

        plt.legend()
        plt.title('h{0} = '.format(i + 1) + str(h[i]))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
    plt.show()

def dif2_fun(x, y, dif_y):
    return ((x - 2)*dif_y + 3*y) / (x - 2)**2

def solve_fun(x):
    return (x - 2)**3 + 1 / (x - 2)

def g(x, y, k):
    return k

def sse(f, y):
    return round(sum([(f_i - y_i) ** 2 for f_i, y_i in zip(f, y)]), 5)

def Real_solve(f, a, b, h):
    x = [i for i in np.arange(a, b + h, h)]
    y = [f(i) for i in x]
    return x, y

def Euler(f, a, b, h, y3, dif_y3):
    n = int((b - a) / h)
    x = [i for i in np.arange(a, b + h, h)]
    y = [y3]
    k = dif_y3
    for i in range(n):
        k += h * f(x[i], y[i], k)
        y.append(y[i] + h * g(x[i], y[i], k))
    return x, y

def RungeKutt(f, a, b, h, y3, dif_y3):
    n = int((b - a) / h)
    x = [i for i in np.arange(a, b + h, h)]
    y = [y3]
    k = [dif_y3]
    for i in range(n):
        K1 = h * g(x[i], y[i], k[i])
        L1 = h * f(x[i], y[i], k[i])
        K2 = h * g(x[i] + 0.5 * h, y[i] + 0.5 * K1, k[i] + 0.5 * L1)
        L2 = h * f(x[i] + 0.5 * h, y[i] + 0.5 * K1, k[i] + 0.5 * L1)
        K3 = h * g(x[i] + 0.5 * h, y[i] + 0.5 * K2, k[i] + 0.5 * L2)
        L3 = h * f(x[i] + 0.5 * h, y[i] + 0.5 * K2, k[i] + 0.5 * L2)
        K4 = h * g(x[i] + h, y[i] + K3, k[i] + L3)
        L4 = h * f(x[i] + h, y[i] + K3, k[i] + L3)
        y.append(y[i] + (K1 + 2 * K2 + 2 * K3 + K4) / 6)
        k.append(k[i] + (L1 + 2 * L2 + 2 * L3 + L4) / 6)
    return x, y, k

def Adams(f, x, y, k, h):
    n = len(x)
    x = x[:4]
    y = y[:4]
    k = k[:4]
    for i in range(3, n - 1):
        k.append(k[i] + h * (55 * f(x[i], y[i], k[i]) -
                             59 * f(x[i - 1], y[i - 1], k[i - 1]) +
                             37 * f(x[i - 2], y[i - 2], k[i - 2]) -
                              9 * f(x[i - 3], y[i - 3], k[i - 3])) / 24)
        y.append(y[i] + h * (55 * g(x[i], y[i], k[i]) -
                             59 * g(x[i - 1], y[i - 1], k[i - 1]) +
                             37 * g(x[i - 2], y[i - 2], k[i - 2]) -
                              9 * g(x[i - 3], y[i - 3], k[i - 3])) / 24)
        x.append(x[i] + h)
    return x, y

def Point_Romberg(dict_):
    k = dict_[0]['h'] / dict_[1]['h']
    Y1 = [yi for xi, yi in zip(dict_[0]['Euler']['x'], dict_[0]['Euler']['y']) if xi in dict_[1]['Euler']['x']]
    Y2 = [yi for xi, yi in zip(dict_[1]['Euler']['x'], dict_[1]['Euler']['y']) if xi in dict_[0]['Euler']['x']]
    Euler = [y1 + (y2 - y1) / (k ** 2 - 1) for y1, y2 in zip(Y1, Y2)]
    X_ex = [xi for xi in dict_[0]['Euler']['x'] if xi in dict_[1]['Euler']['x']]
    Y_ex = [solve_fun(i) for i in X_ex]
    for i in range(len(Euler)):
        Euler[i] = abs(Euler[i] - Y_ex[i])
    Y1 = [yi for xi, yi in zip(dict_[0]['Runge']['x'], dict_[0]['Runge']['y']) if xi in dict_[1]['Runge']['x']]
    Y2 = [yi for xi, yi in zip(dict_[1]['Runge']['x'], dict_[1]['Runge']['y']) if xi in dict_[0]['Runge']['x']]
    runge = [y1 + (y2 - y1) / (k ** 2 - 1) for y1, y2 in zip(Y1, Y2)]
    X_ex = [xi for xi in dict_[0]['Runge']['x'] if xi in dict_[1]['Runge']['x']]
    Y_ex = [solve_fun(i) for i in X_ex]
    for i in range(len(runge)):
        runge[i] = abs(runge[i] - Y_ex[i])
    Y1 = [yi for xi, yi in zip(dict_[0]['Adams']['x'], dict_[0]['Adams']['y']) if xi in dict_[1]['Adams']['x']]
    Y2 = [yi for xi, yi in zip(dict_[1]['Adams']['x'], dict_[1]['Adams']['y']) if xi in dict_[0]['Adams']['x']]
    Adams = [y1 + (y2 - y1) / (k ** 2 - 1) for y1, y2 in zip(Y1, Y2)]
    X_ex = [xi for xi in dict_[0]['Adams']['x'] if xi in dict_[1]['Adams']['x']]
    Y_ex = [solve_fun(i) for i in X_ex]
    for i in range(len(Adams)):
        Adams[i] = abs(Adams[i] - Y_ex[i])
    return {'Euler': Euler, 'Runge': runge, 'Adams': Adams}

def main():
    a, b = 3, 4
    h = 0.1
    y3, dif_y3 = 2, 2
    res, pure = [], []
    steps = [h, h/5]
    for h in steps:
        print(f"Текущий шаг: {h}")
        print("Метод Эйлера:")
        x_eul, y_eul = Euler(dif2_fun, a, b, h, y3, dif_y3)
        for x, y in zip(x_eul, y_eul):
            print(f'x = {round(x, 4)}, y = {y}')
        print()
        print("Метод Рунге-Кутта:")
        x_rung, y_rung, k_rung = RungeKutt(dif2_fun, a, b, h, y3, dif_y3)
        for x, y in zip(x_rung, y_rung):
            print(f'x = {round(x, 4)}, y = {y}')
        print()
        print("Метод Адамса:")
        x_ad, y_ad = Adams(dif2_fun, x_rung, y_rung, k_rung, h)
        for x, y in zip(x_ad, y_ad):
            print(f'x = {round(x, 4)}, y = {y}')
        print()
        print("Реальное решение:")
        x_real, y_real = Real_solve(solve_fun, a, b, h)
        for x, y in zip(x_real, y_real):
            print(f'x = {round(x, 4)}, y = {y}')
        print()
        pure.append((x_real, y_real))
        res.append({
                    "h": h,
                    "Euler": {'x': x_eul, 'y': y_eul},
                    "Runge": {'x': x_rung, 'y': y_rung},
                    "Adams": {'x': x_ad, 'y': y_ad},
                    })
    err = Point_Romberg(res)
    print("Оценка погрешности Рунге-Ромберга")
    print("Метод Эйлера:      {0}".format(err['Euler']))
    print("Метод Рунге-Кутта: {0}".format(err['Runge']))
    print("Метод Адамcа:      {0}".format(err['Adams']))
    grafics(res, pure, steps)

if __name__ == '__main__':
    main()