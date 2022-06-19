import sys

def errorMessage():
    print("Использование:\n"
    "{0} --load <testFile>\tзагрузка списков из файла\n"
    "{0} --runtime\t\tнабор списков от руки\n".format(sys.argv[0]))
    sys.exit(1)

def input_points(X, Y, x):
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
                Y = i.split()
                count += 1
                continue
            if count == 3:
                x = float(i)
    elif sys.argv[1] == "--runtime" and len(sys.argv) == 2:
        X = input("Введите список значений X: ").split()
        Y = input("Введите список значений Y: ").split()
        x = float(input("Введите Х*: "))
    else:
        errorMessage()
    for i in range(len(X)):
        X[i] = float(X[i])
    for i in range(len(Y)):
        Y[i] = float(Y[i])
    return [X, Y, x]

def position(X, x):
    pos = 0
    for i in X:
        if i > x:
            break
        pos += 1
    return pos

def diff(X, Y, x):
    pos = position(X, x)
    r_y = (Y[pos] - Y[pos - 1]) / (X[pos] - X[pos - 1])
    l_y = (Y[pos - 1] - Y[pos - 2]) / (X[pos - 1] - X[pos - 2])
    res1 = l_y + (r_y - l_y) / (X[pos] - X[pos - 2]) * (2*x - X[pos -2] - X[pos -1])
    res2 = 2 * (r_y - l_y) / (X[pos] - X[pos -2])
    return [res1, res2]

def main():
    X, Y, x = [], [], 0
    X, Y, x = input_points(X, Y, x)
    res1, res2 = diff(X, Y, x)
    print("1-ая производная от Х* = {0}:\t{1}".format(x, res1))
    print("2-ая производная от Х* = {0}:\t{1}".format(x, res2))

if __name__ == "__main__":
    main()