import sys
import lab1_1 as bibl
import lab1_3 as bibl3
import math

def find_lyam(A, n):
    res = []
    for i in range(n):
        res.append(round(A[i][i], 3))
    return res

def t(A, n):
    sum = 0
    for i in range(n):
        for j in range(i+ 1, n):
            sum += A[i][j] ** 2
    sum = math.sqrt(sum)
    return sum


def transpon(A, n, m):
    result = []
    for i in range(n):
        vector = []
        for j in range(m):
            vector.append(A[j][i])
        result.append(vector)
    return result


def nul_matrix(A, n, m):
    for i in range(n):
        line_mat = []
        for j in range(m):
            line_mat.append(0)
        A.append(line_mat)

def matrix_multiplication(A, B, n, m, k):
    result = []
    nul_matrix(result, n, k)
    for i in range(n):
        for t in range(k):
            sum = 0
            for j in range(m):
                sum += A[i][j] * B[j][t]
            result[i][t] = sum
    return result

def find_fi(A, i, j):
    fi = 1 /2 * math.atan(2 * A[i][j] / (A[i][i] - A[j][j]))
    return fi

def matrix_U(A, max_i, max_j, fi, n):
    U = []
    bibl.nul_matrix(U, n)
    for i in  range(n):
        U[i][i] = 1
    U[max_i][max_i] = round(math.cos(fi), 2)
    U[max_j][max_j] = round(math.cos(fi), 2)
    U[max_i][max_j] = round(-math.sin(fi), 2)
    U[max_j][max_i] = round(math.sin(fi), 2)
    return U

def find_max(A, n):
    max = 0
    for i in range(n):
        for j in range(i+ 1, n):
            if abs(A[i][j]) > max:
                max = abs(A[i][j])
                max_i, max_j = i, j
    return [max_i, max_j]

def input_matrix():
    A, n, j = [], 0, 0
    if len(sys.argv) < 2:
        bibl.errorMessage()
    if sys.argv[1] == "--load":
        if len(sys.argv) < 2:
            bibl.errorMessage()
        try:
            test_file = open(sys.argv[2], 'r')
        except FileNotFoundError:
            print("Файл {0} не найден. Исключение типа FileBotFoundError.".format(sys.argv[2]))
            quit()
        temp = test_file.read().splitlines()
        for i in temp:
            A.append(i.split())
    elif sys.argv[1] == "--runtime":
        while True:
            line = input()
            if not line:
                break
            A.append(line.split())        
    for i in A:
        n += 1
    for i in range(n):
        for j in range(n):
            A[i][j] = float(A[i][j])
    return [n, A]

if __name__ == "__main__":
    n, A = input_matrix()
    iter = 0
    e = float(input("Задайте точность: "))
    while t(A, n) > e and iter < bibl3.max_iter:
        max_i, max_j = find_max(A, n)
        fi = find_fi(A, max_i, max_j)
        U = matrix_U(A, max_i, max_j, fi, n)
        A = matrix_multiplication(transpon(U, n, n), matrix_multiplication(A, U, n, n, n), n, n, n)
        if iter > 0:
            vectors = matrix_multiplication(vectors, U, n, n, n)
        else:
            vectors = U
        iter += 1
    lyambda = find_lyam(A, n)
    print("\nМатрица A:")
    bibl.print_matrix(A)
    print("Количество итераций: ", iter)
    print("\nСобственные значения:", lyambda)
    print("\nМатрица собственных векторов:")
    bibl.print_matrix(vectors)