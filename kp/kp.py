import sys
import random

def Generate(name):
    lines_index, columns_index, values = [], [], []
    matrix_size = random.randint(100, 500)
    for i in range(matrix_size):
        for j in range(i, matrix_size):
            lines_index.append(i)
            columns_index.append(j)
            values.append(random.randint(0, 500))
    for i in range(round(len(lines_index) / 2)):
        j = random.randint(0, len(lines_index) - i)
        lines_index.pop(j)
        columns_index.pop(j)
        values.pop(j)
    lines_index = " ".join(map(str, lines_index)) + "\n\n"
    columns_index = " ".join(map(str, columns_index)) + "\n\n"
    values = " ".join(map(str, values))
    print(matrix_size)
    print(lines_index)
    file = open(name, "w")
    file.write(lines_index)
    file.write(columns_index)
    file.write(values)
    file.close()

def main():
    if len(sys.argv) != 3:
        ErrorMessage()
    else:
        if sys.argv[1] == "--generate":
            Generate(sys.argv[2])
        elif sys.argv[1] == "--load":
            Lancosh(sys.argv[2])
        elif sys.argv[1] == "--test":
            Test(sys.argv[2])
        else:
            ErrorMessage()

def ErrorMessage():
    print("Использование:\n"
    "{0} --generate <nameFile>\tгенерация разреженной матрицы в файл\n"
    "{0} --load <testFile>\t\tзагрузка матрицы из файла\n"
    "{0} --test <testFile>\t\tсравнение метода Ланцоша с QR разложением\n".format(sys.argv[0]))
    sys.exit(1)    

if __name__ == "__main__":
    main()