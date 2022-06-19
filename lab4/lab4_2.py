import math
import numpy as np
import matplotlib.pyplot as plt
from lab4_1 import RungeKutt

def grafics(ans, exact, h):
    n = len(ans)
    for i in range(n):
        plt.subplot(n, 1, i + 1)
        plt.subplots_adjust(wspace=0.1, hspace=0.6)
        plt.plot(ans[i]["Shooting"]["x"], ans[i]["Shooting"]["y"], alpha=0.4, label = "Метод Стрельбы")
        plt.plot(ans[i]["FD"]["x"], ans[i]["FD"]["y"], alpha=0.4, label = "Конечно-разностный метод")
        plt.plot(exact[i][0], exact[i][1], alpha=0.4, label = "f(x)")
        plt.legend()
        plt.title('h{0} = '.format(i + 1) + str(h[i]))
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
    plt.show()

def func(x, y, dif_y):
    return 2*y / (x**2 * (x + 1))

def g(x, y, k):
    return k

def p(x):
    return 0

def q(x):
    return -2 / x**2  / (x + 1)

def Real_solve(x):
    return -1 + 2/x + 2*(x+1)/x * math.log(abs(x + 1), math.e)

def f(x):
    return 0

def first(x, y, x0):
    i = 0
    while i < len(x) - 1 and x[i + 1] < x0:
        i += 1
    return (y[i + 1] - y[i]) / (x[i + 1] - x[i])

def stop(y, y1, eps):
    if abs(y[-1] - y1) > eps:
        return True
    else:
        return False

def newN(n_last, n, ans_last, ans, b, y1):
    x, y = ans_last[0], ans_last[1]
    phi_last = y[-1] - y1
    x, y = ans[0], ans[1]
    phi = y[-1] - y1
    return n - (n - n_last) / (phi - phi_last) * phi

def Shooting(a, b, y0, y1, h, eps):
    n_last = 1
    n = 0.8
    dif_y = n_last
    ans_last = RungeKutt(func, a, b, h, n_last, dif_y)[:2]
    dif_y = n
    ans = RungeKutt(func, a, b, h, n, dif_y)[:2]
    while stop(ans[1], y1, eps):
        n, n_last = newN(n_last, n, ans_last, ans, b, y1), n
        ans_last = ans
        dif_y = n
        ans = RungeKutt(func, a, b, h, y0, dif_y)[:2]
    return ans

def tma(a, b, c, d, shape):
    p = [-c[0] / b[0]]
    q = [d[0] / b[0]]
    x = [0] * (shape + 1)
    for i in range(1, shape):
        p.append(-c[i] / (b[i] + a[i] * p[i - 1]))
        q.append((d[i] - a[i] * q[i - 1]) / (b[i] + a[i] * p[i - 1]))
    for i in reversed(range(shape)):
        x[i] = p[i] * x[i + 1] + q[i]
    return x[:-1]

def FiniteDifference(a, b, alpha, beta, delta, gamma, y0, y1, h):
    n = int((b - a) / h)
    x = [i for i in np.arange(a, b + h, h)]
    A = [0] + [1 - p(x[i]) * h / 2 for i in range(0, n - 1)] + [-gamma]
    B = [alpha * h - beta] + [q(x[i]) * h ** 2 - 2 for i in range(0, n - 1)] + [delta * h + gamma]
    C = [beta] + [1 + p(x[i]) * h / 2 for i in range(0, n - 1)] + [0]
    D = [y0 * h] + [f(x[i]) * h ** 2 for i in range(0, n - 1)] + [y1 * h]
    y = tma(A, B, C, D, len(A))
    return x, y

def Point_Romberg(ans, exact):
    k = ans[0]['h'] / ans[1]['h']
    Y1 = [yi for xi, yi in zip(ans[0]['Shooting']['x'], ans[0]['Shooting']['y']) if xi in ans[1]['Shooting']['x']]
    Y2 = [yi for xi, yi in zip(ans[1]['Shooting']['x'], ans[1]['Shooting']['y']) if xi in ans[0]['Shooting']['x']]
    shoot_err = [y1 + (y2 - y1) / (k ** 2 - 1) for y1, y2 in zip(Y1, Y2)]
    X_ex = [xi for xi in ans[0]['Shooting']['x'] if xi in ans[1]['Shooting']['x']]
    Y_ex = [Real_solve(i) for i in X_ex]
    for i in range(len(shoot_err)):
        shoot_err[i] = abs(shoot_err[i] - Y_ex[i])
    Y1 = [yi for xi, yi in zip(ans[0]['FD']['x'], ans[0]['FD']['y']) if xi in ans[1]['FD']['x']]
    Y2 = [yi for xi, yi in zip(ans[1]['FD']['x'], ans[1]['FD']['y']) if xi in ans[0]['FD']['x']]
    fd_err = [y1 + (y2 - y1) / (k ** 2 - 1) for y1, y2 in zip(Y1, Y2)]
    X_ex = [xi for xi in ans[0]['FD']['x'] if xi in ans[1]['FD']['x']]
    Y_ex = [Real_solve(i) for i in X_ex]
    for i in range(len(fd_err)):
        fd_err[i] = abs(fd_err[i] - Y_ex[i])
    return {'Shooting': shoot_err, 'FD': fd_err}

def sse(f, y):
    return sum([(f_i - y_i) ** 2 for f_i, y_i in zip(f, y)])

def main():
    a, b = 1, 2
    alpha, delta, gamma, beta = 1, 1, 0, 0
    y0 = 1 + 4*math.log(2, math.e)
    y1 = 3*math.log(3, math.e)
    step = 1 / 10
    eps = 1e-5
    res, res2, ans = [], [], []
    steps = [step, step / 2]
    i = 0
    for h in steps:
        print(f'Текущий шаг: {h}')
        print('Метод стрельбы')
        res.append(Shooting(a, b, y0, y1, h, eps))
        for x, y in zip(res[i][0], res[i][1]):
            print(f'x: {round(x, 5)}, y:', y)
        print()
        print('Конечно-разностный метод')
        res2.append(FiniteDifference(a, b, alpha, beta, delta, gamma, y0, y1, h))
        for x, y in zip(res2[i][0], res2[i][1]):
            print(f'x: {round(x, 5)}, y:', y)
        print()
        ans.append({
            "h": h,
            "Shooting": {'x': res[i][0],  'y': res[i][1]},
            "FD":       {'x': res2[i][0], 'y': res2[i][1]}
        })
        i += 1
    exact = []
    for h in steps:
        x_ex = [i for i in np.arange(a, b + h, h)]
        y_ex = [Real_solve(i) for i in x_ex]
        exact.append((x_ex, y_ex))
    err = Point_Romberg(ans, exact)
    print("Оценка погрешности Рунге-Ромберга")
    print('Метод стрельбы:           {}'.format(err['Shooting']))
    print('Конечно разностный метод: {}'.format(err['FD']))
    grafics(ans, exact, steps)

if __name__ == '__main__':
    main()