import argparse


class SizeException(Exception):
    pass


def get_matrices(path_in):
    """
    Read matrix from .txt file

    Parameters
    ----------
    path_in : str
        The path to the file


    Returns
    -------
    matrix_1 : list
        First matrix from file
    matrix_2 : list
        Second matrix from file
    """
    with open(path_in) as inp_file:
        inp_data = inp_file.read()
    # STRINGS TO MATRICES
    m_strings = inp_data.split('\n')
    matrix_1 = []
    matrix_2 = []
    i = 0
    while m_strings[i] != '':
        matrix_1.append(m_strings[i].split(' '))
        i += 1
    i += 1
    while i < len(m_strings):
        if m_strings[i] != '':
            matrix_2.append(m_strings[i].split(' '))
        i += 1
    nulls = len(matrix_2) // 2
    for i in range(len(matrix_1)):
        matrix_1[i] += ['0' for j in range(nulls)]
    for i in range(nulls):
        matrix_1.append(['0' for j in range(len(matrix_1) + nulls)])
    return matrix_1, matrix_2


def convolution(matrix_1, matrix_2):
    """
    Convolve matrices

    Parameters
    ----------
    matrix_1 : list
        Left matrix
    matrix_2 : list
        Right matrix (kernel)

    Returns
    -------
    matrix_res : list
        Result matrix
    """
    if len(matrix_1) < len(matrix_2):
        raise SizeException("Incorrect matrix sizes")
    nulls = len(matrix_2) // 2
    matrix_res = []
    try:
        for i in range(len(matrix_1) - nulls):
            matrix_res.append([])
            for j in range(len(matrix_1[0]) - nulls):
                sum_m = 0
                for k in range(-1, len(matrix_2) - 1):
                    for m in range(-1, len(matrix_2[0]) - 1):
                        print(f"{matrix_1[i + k][j + m]} * {matrix_2[k + 1][m + 1]}")
                        sum_m += float(matrix_1[i + k][j + m]) * float(matrix_2[k + 1][m + 1])
                matrix_res[i].append(sum_m)
        return matrix_res
    except IndexError:
        raise SizeException("Incorrect matrix sizes")


def write_matrix(matrix_res, path_out):
    """
    Write matrix to .txt file

    Parameters
    ----------
    matrix_res : list
        The matrix that is to be written
    path_out : str
        The path to the file
    """
    with open(path_out, 'w+') as f:
        for i in range(len(matrix_res)):
            f.write(' '.join(str(num) for num in matrix_res[i]) + '\n')


parser = argparse.ArgumentParser(description='Matrix convolution')
parser.add_argument("-path_in", type=str,
                    help="input file", default="input.txt")
parser.add_argument("-path_out", type=str,
                    help="output file", default="output.txt")
args = parser.parse_args()
matr1, matr2 = get_matrices(args.path_in)
print(matr1)
try:
    write_matrix(convolution(matr1, matr2), args.path_out)
except SizeException:
    print("Error. Please check the sizes of the matrices.")