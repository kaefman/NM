import sys
import math
import lab1_1 as bibl
import lab1_4 as bibl4

max_iter = 50

def chislo(alpha, A, n, m):
    for i in range(n):
        for j in range(m):
            A[i][j] = A[i][j] * alpha
    return A

def matrix_minus(A, B, n, m):
    res = []
    bibl4.nul_matrix(res, n, m)
    for i in range(n):
        for j in range(m):
            res[i][j] = A[i][j] - B[i][j]
    return res

def matrix_plus(A, B, n, m):
    res = []
    bibl4.nul_matrix(res, n, m)
    for i in range(n):
        for j in range(m):
            res[i][j] = A[i][j] + B[i][j]
    return res

def get_haus(v, n):
    E = get_E(n)
    VTV = bibl4.matrix_multiplication(bibl4.transpon(v, 1, n), v, 1, n, 1)
    VVT = bibl4.matrix_multiplication(v, bibl4.transpon(v, 1, n), n, 1, n)
    CHD = 2 / VTV[0][0]
    CHDM = chislo(CHD, VVT, n, n)
    H = matrix_minus(E, CHDM, n, n)
    #print("H:")
    #bibl.print_matrix(H)
    return H

def get_E(n):
    E = []
    bibl.nul_matrix(E, n)
    for i in range(n):
        E[i][i] = 1
    return E

def sign(x):
    if x < 0:
        return -1
    else:
        return 1

def get_v(A, n, k):
    v = []
    for i in range(k):
        v.append([0])
    sum = 0
    for i in range(k, n):
        sum += A[i][k] ** 2
    sum = math.sqrt(sum)
    v.append([A[k][k] + sign(A[k][k]) * sum])
    for i in range(k + 1, n):
        v.append([A[i][k]])
    #print("v:")
    #bibl.print_matrix(v)
    return v

def get_QR(R, n):
    k = 0
    Q = get_E(n)
    while k < n - 1:
        v = get_v(R, n, k)
        H = get_haus(v, n)
        R = bibl4.matrix_multiplication(H, R, n, n, n)
        Q = bibl4.matrix_multiplication(Q, H, n, n, n)
        k += 1
    return [Q, R]

def kritik(A, n, e, i):
    sum = 0
    for j in range(i + 1, n):
        sum += A[j][i] ** 2 
    sum = math.sqrt(sum)
    if sum > e and iter < max_iter:
        return True
    else:
        return False

def get_solve(A, n, e):
    res = []
    k = 0
    while k < n - 1:
        if not(kritik(A, n, e, k)):
            res.append(A[k][k])
            k += 1
        else:
            res.append(get_korni(A, k, k + 1)[0])
            res.append(get_korni(A, k, k + 1)[1])
            k += 2
    return res

def get_korni(A, i, j):
    a = 1
    b = -(A[i][i] + A[j][j])
    c = (A[i][i] * A[j][j] - A[i][j] * A[j][i])
    D = b ** 2 - 4 * a * c
    x1 = -b / 2 * a
    D = math.sqrt(abs(D)) / 2
    x2 = str(x1) + str(" + ") + str(D) + str("i")
    x3 = str(x1) + str(" - ") + str(D) + str("i")
    return [x2, x3]

if __name__ == "__main__":
 
    iter = 0
    n, A = bibl4.input_matrix()
    e = float(input("Задайте точность: "))
    print("\nМатрица A:")
    bibl.print_matrix(A)
    while kritik(A, n, e, 0):
        Q, R = get_QR(A, n)
        #print("Номер итерации: " + str(iter) + "\n")
        #print("Матрица A:")
        #bibl.print_matrix(A)
        #print("Матрица Q:")
        #bibl.print_matrix(Q)
        #print("Матрица R:")
        #bibl.print_matrix(R)
        A = bibl4.matrix_multiplication(R, Q, n, n, n)
        iter += 1
    print("Матрица A({0}):".format(iter))
    bibl.print_matrix(A)
    print("Собственные значения:")
    print(get_solve(A, n, e))