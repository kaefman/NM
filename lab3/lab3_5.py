import sys

def function(x):
    return x*(49 - x**2)**(1/2)

def errorMessage():
    print("Использование:\n"
    "{0} --load <testFile>\tзагрузка списков из файла\n"
    "{0} --runtime\t\tнабор списков от руки\n".format(sys.argv[0]))
    sys.exit(1)

def input_points():
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
        x1, x2, h1, h2 = test_file.read().split()
        x1 = float(x1)
        x2 = float(x2)
        h1 = float(h1)
        h2 = float(h2)
    elif sys.argv[1] == "--runtime" and len(sys.argv) == 2:
        x1 = float(input("Введите x1: "))
        x2 = float(input("Введите x2: "))
        h1 = float(input("Введите h1: "))
        h2 = float(input("Введите h2: "))
    else:
        errorMessage()
    return [x1, x2, h1, h2]

def Rectangle(x1, x2, h):
    integ = 0
    while x1 <= x2 - h:
        integ += h * function((x1 + x1 + h) / 2)
        x1 += h
    return integ

def Trapezoid(x1, x2, h):
    integ = 0
    while x1 <= x2 - h:
        integ += h * 1/2 * (function(x1) + function(x1 + h))
        x1 += h
    return integ

def Simpson(x1, x2, h):
    integ = 0
    while x1 <= x2 - 2*h:
        integ += h/3 * (function(x1) + 4*function(x1 + h) + function(x1 + 2 * h))
        x1 += 2*h
    return integ

def Rumberg(integ1, integ2, h1, h2, p):
    k = h2 / h1
    return abs((integ1 - integ2) / (k ** p - 1))

def main():
    x1, x2, h1, h2 =  input_points()
    integ_r1 = Rectangle(x1, x2, h1)
    integ_t1 = Trapezoid(x1, x2, h1)
    integ_s1 = Simpson(x1, x2, h1)
    print("Результаты шага({0}):\tПрямоугольник\t\tТрапеция\t\t\tСимпсон".format(h1))
    print("\t\t\t", integ_r1, "\t", integ_t1, "\t", integ_s1)
    integ_r2 = Rectangle(x1, x2, h2)
    integ_t2 = Trapezoid(x1, x2, h2)
    integ_s2 = Simpson(x1, x2, h2)
    print("Результаты шага({0}):\tПрямоугольник\t\tТрапеция\t\t\tСимпсон".format(h2))
    print("\t\t\t", integ_r2, "\t", integ_t2, "\t", integ_s2)
    err1 = Rumberg(integ_r1, integ_r2, h1, h2, 1)
    err2 = Rumberg(integ_t1, integ_t2, h1, h2, 1)
    err3 = Rumberg(integ_s1, integ_s2, h1, h2, 2)
    print("\nРунге-Ромберг:\t\t", err1, "\t", err2, "\t", err3)

if __name__ == "__main__":
    main()