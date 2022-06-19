import sys
import lab1_1 as bibl

def nul_vector(b, n):
    for i in range(n):
        b.append(int(0))

def progonka(A, b, n):
    P, Q, X = [], [], []
    nul_vector(P, n)
    nul_vector(Q, n)
    nul_vector(X, n)
    P[0], Q[0] = -A[0][1] / A[0][0], b[0] / A[0][0]
    for i in range(1, n - 1):
        P[i] = -A[i][i + 1] / (A[i][i] + A[i][i - 1] * P[i - 1])
        Q[i] = (b[i] - A[i][i - 1] * Q[i - 1]) / (A[i][i] + A[i][i - 1] * P[i - 1])
    Q[n - 1] = (b[n - 1] - A[n - 1][n - 2] * Q[n - 2]) / (A[n - 1][n - 1] + A[n - 1][n - 2] * P[n - 2])
    X[n - 1] = Q[n - 1]
    i = n - 2
    '''
    print("Вектор b:\n", b, "\n")
    print("Вектор P:\n", P, "\n")
    print("Вектор Q:\n", Q, "\n")
    '''
    while i > -1:
        X[i] = P[i] * X[i + 1] + Q[i]
        i -= 1
    return X 

if __name__ == "__main__":
    
    matrix_A0, matrix_A_b0, vector_b, line_mat1 = [], [], [], []
    max = 1
    lst = bibl.input_matrix(matrix_A0, matrix_A_b0, vector_b, line_mat1, max)
    matrix_A0, matrix_A_b0, vector_b, line_mat1, max = lst

    print("Матрица A:")
    bibl.print_matrix(matrix_A0)
    print("Решение СЛАУ:\n", progonka(matrix_A0, vector_b, max), "\n")