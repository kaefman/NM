import sys
import math
import lab1_4 as bibl4
import lab1_5 as bibl5

def input_matrix(matrix_A0, matrix_A_b0, vector_b, line_mat1, max):
    if len(sys.argv) < 2:
        errorMessage()
    if sys.argv[1] == "--load":
        if len(sys.argv) < 3:
            errorMessage()
        try:
            test_file = open(sys.argv[2], 'r')
        except FileNotFoundError:
            print("Файл {0} не найден. Исключение типа FileBotFoundError.".format(sys.argv[2]))
            quit()
        temp = test_file.read().splitlines()
        for i in temp:
            matrix_A_b0.append(i.split())
    elif sys.argv[1] == "--runtime":
        while True:
            line = input()
            if not line:
                break
            matrix_A_b0.append(line.split())
    #Обработка знаков матрицы        
    for i in matrix_A_b0:
        for j in i:
            count = i.index(j)
            if j == "+":
                i.remove("+")
            if j == "-":
                i[count + 1] = "-" + i[count + 1]
                i.remove("-")
            if j == "=":
                i.remove("=")
    #поиск максимального значения ^ и разбиение на значения матрицы
    for i  in matrix_A_b0:
        count = 1
        for j in i:
            try: 
                vector_b.append(float(j))
            except:  
                ind = j.find("x")
                id = int(j[ind + 2 :])
                if id > max:
                    max = id
                if id == count and j[: ind] == "":
                    line_mat1.append("1")
                elif id == count and j[: ind] == "-":
                    line_mat1.append("-1")
                elif id == count:
                    line_mat1.append(j[: ind])
                else:
                    while id != count:
                        line_mat1.append("0")
                        count += 1
                    else:
                        if id == count and j[: ind] == "":
                            line_mat1.append("1")
                        elif id == count and j[: ind] == "-":
                            line_mat1.append("-1")
                        elif id == count:
                            line_mat1.append(j[: ind])
                count += 1
        else:
            matrix_A0.append(line_mat1)
            line_mat1 = []
    #Дозополнение матрицы 0, для приведение к виду n x n
    for i in matrix_A0:
        if len(i) < max:
            while len(i) < max:
                i.append("0")
    return [matrix_A0, matrix_A_b0, vector_b, line_mat1, max]

def inverseLU(L, U, n, P):
    inverseA = []
    nul_matrix(inverseA, n)
    i = n - 1
    j = n - 1
    while i > -1 and j > -1:
        sum = 0
        for k in range(i + 1, n):
            sum += U[i][k] * inverseA[k][i]
        inverseA[i][j] = 1 / U[i][j] * (1 - sum)
        i -= 1
        while i > -1:
            sum = 0
            for k in range(i + 1, n):
                sum += U[i][k] * inverseA[k][j]
            inverseA[i][j] = -1 / U[i][i] * sum
            i -= 1
        i = j
        j -= 1
        while j > -1:
            sum = 0
            for k in range(j + 1, n):
                sum += inverseA[i][k] * L[k][j]    
            inverseA[i][j] = -sum
            j -= 1
        j = i -1 
        i -= 1
    inverseA = bibl4.matrix_multiplication(P, inverseA, n, n, n)
    print_matrix(inverseA)

def solveLU(L, U, n, b):
    Y = []
    Y.append(float(b[0]))
    X = []
    for i in range(1, n):
        sum = 0
        for j in range(i):
            sum += float(Y[j]) * float(L[i][j])
        Y.append(float(b[i]) - sum)
    #print(Y)
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

def swap_maximum(A, B, n):
    P = bibl5.get_E(n)
    for j in range(n - 1):
        i = j + 1
        while i < n:
            if abs(float(A[j][j])) < abs(float(A[i][j])):
                A[j], A[i] = A[i], A[j]
                B[j], B[i] = B[i], B[j]
                P[i], P[j] = P[j], P[i]
            i += 1
    return P

def determinant(matrix, n):
    det = 1
    for i in range(n):
        det = matrix[i][i] * det
    return det

def nul_matrix(matrix, n):
    line_mat2 = []
    for i in range(n):
        for j in range(n):
            line_mat2.append(int(0))
        else:
            matrix.append(line_mat2)
            line_mat2 = []

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
            #print_matrix(A) пошаговая проверка
            k += 1    

def print_matrix(matrix):
    for i in matrix:
        j = 0
        while j < len(i):
            i[j] = round(float(i[j]), 3)
            j += 1
        print(i) 
    print("")

def errorMessage():
    print("Использование:\n"
    "{0} --load <testFile>\tзагрузка матрицы из файла\n"
    "{0} --runtime\t\tнабор матрицы от руки. Пустая линия - конец ввода\n".format(sys.argv[0]))
    sys.exit(1)

if __name__ == "__main__":

    matrix_A0, matrix_A_b0, vector_b, line_mat1, matrix_U, matrix_L = [], [], [], [], [], []
    max = 1
    lst = input_matrix(matrix_A0, matrix_A_b0, vector_b, line_mat1, max)
    matrix_A0, matrix_A_b0, vector_b, line_mat1, max = lst

    #Зануление матриц L U
    nul_matrix(matrix_L, max)
    nul_matrix(matrix_U, max)

    print("Матрица A:")
    print_matrix(matrix_A0)
    print("Вектор b:\n" + str(vector_b) + "\n")
    #Переставляем строки
    P = swap_maximum(matrix_A0, vector_b, max)

    print("Матрица A(после перестановок):")
    print_matrix(matrix_A0)
    print("Вектор b(после перестановок):\n" + str(vector_b) + "\n")
    LU(matrix_A0, matrix_L, matrix_U, max)
    print("Матрица U:")
    print_matrix(matrix_U)
    print("Матрица L:")  
    print_matrix(matrix_L)
    det = determinant(matrix_U, max)
    print("Определитель А: " + str(det) + "\n")
    print("Обратная матрица к A:\n")
    inverseLU(matrix_L, matrix_U, max, P)
    b = bibl4.transpon([solveLU(matrix_L, matrix_U, max, vector_b)], max, 1)
    b = bibl4.transpon(bibl4.matrix_multiplication(P, b, max, max, 1), 1, max)
    print("Решение СЛАУ:\n" + str(b[0]) + "\n")