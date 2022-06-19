import sys
import math
import lab1_1 as bibl
import lab1_2 as bibl2

max_iter = 50

def get_C(A):
    C = []
    bibl.nul_matrix(C, len(A))
    for i in range(len(A)):
        for j in range(i, len(A)):
            if i == j:
                C[i][j] = 1
            else:
                C[i][j] = A[i][j]
    return C 

def zeydel(A, b, n, e):
    x0, x1, iter = [], [], 0
    for i in b:
        x1.append(i)
    bibl2.nul_vector(x0, n)
    C = get_C(A)
    epsil = epsilon(x0, x1, C, A, n)
    while epsil > e and iter < max_iter:
        for i in range(n):
            x0[i] = x1[i]
        for i in range(n):
            sum = 0
            for j in range(n):
                sum += A[i][j] * x1[j]
            x1[i] = b[i] + sum
        epsil = epsilon(x0, x1, C, A, n)
        iter += 1
    return [x1, iter]

def nul_matrix(A, n, m):
    for i in range(n):
        line_mat = []
        for j in range(m):
            line_mat.append(int(0))
        A.append(line_mat)

def multiplication(A, x, n):
    result = []
    for i in range(n):
        sum = 0
        for j in range(n):
            sum += A[i][j] * x[j]
        result.append(sum)
    return(result)

def vector_minus(A, B):
    result = []
    for i in range(len(A)):
        result.append(A[i] - B[i])
    return result

def norma_c(A, n, m):
    max = 0
    if n == 1:
        for i in range(m):
            if max < abs(A[i]):
                max = abs(A[i])
        return max
    else:    
        for i in range(n):
            sum = 0
            for j in range(m):
                sum += abs(A[i][j])
            if max < sum:
                max = sum
        return max

def vector_plus(A, B):
    result = []
    for i in range(len(A)):
        result.append(A[i] + B[i])
    return result

def epsilon(x0, x1, C, alpha, n):
    try:
        e = norma_c(vector_minus(x1, x0), 1, n) * norma_c(C, n, n) / (1 - norma_c(alpha, n, n))
        return e
    except ZeroDivisionError:
        e = norma_c(vector_minus(x1, x0), 1, n)
        return e

def common_iterations(A, b, n, e):
    iter, x1, x0 = 0, b, []
    bibl2.nul_vector(x0, n)
    epsil = epsilon(x0, x1, A, A, n)
    while epsil > e and iter < max_iter:
        x0 = x1
        x1 = vector_plus(b, multiplication(A, x0, n))
        epsil = epsilon(x0, x1, A, A, n)
        iter += 1
    return [x1, iter]
        

def equal_form(A, b, n):
    equal_matrix, equal_b = [], []
    bibl.nul_matrix(equal_matrix, n)
    bibl2.nul_vector(equal_b, n)
    for i in range(n):
        equal_b[i] = b[i] / float(A[i][i])
        for j in range(n):
            if i == j:
                equal_matrix[i][j] = 0
            else:
                equal_matrix[i][j] = -float(A[i][j]) / float(A[i][i])
    return [equal_matrix, equal_b]

if __name__ == "__main__":

    matrix_A0, matrix_A_b0, vector_b, line_mat1 = [], [], [], []
    max = 1
    lst = bibl.input_matrix(matrix_A0, matrix_A_b0, vector_b, line_mat1, max)
    e = float(input("Задайте точность: "))
    matrix_A0, matrix_A_b0, vector_b, line_mat1, max = lst
    bibl.swap_maximum(matrix_A0, vector_b, max)
    equal_matrix, equal_b = equal_form(matrix_A0, vector_b, max)
    result, iter = common_iterations(equal_matrix, equal_b, max, e)

    print("\nМатрица A:")
    bibl.print_matrix(matrix_A0)
    print("Вектор b:\n" + str(vector_b) + "\n")
    print("Матрица alpha:")
    bibl.print_matrix(equal_matrix)
    print("Вектор betta:\n" + str(equal_b) + "\n")
    print("Решение СЛАУ методом простых итераций:\n" + str(result))
    print("Количество итераций:", iter)

    result, iter = zeydel(equal_matrix, equal_b, max, e)

    print("\nРешение СЛАУ методом Зейделя:\n" + str(result))
    print("Количество итераций:", iter)