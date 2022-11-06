import argparse
import numpy as np


def method1(real, sint, p):
    np.random.seed(1818)
    rands = np.random.rand(len(real))
    res = np.where(rands > args.p, real, sint)
    return res


def method2(real, sint, p):
    np.random.seed(1818)
    matrix_2d = np.column_stack((real, sint))
    return np.apply_along_axis(lambda arr: arr[0] if np.random.rand() > p else arr[1], 1, matrix_2d)


def method3(real, sint, p):
    np.random.seed(1818)
    matrix_2d = np.column_stack((real, sint))
    return np.array(list((map(lambda arr: arr[0] if np.random.rand() > p else arr[1], matrix_2d))))


parser = argparse.ArgumentParser(description='Argparsing')
parser.add_argument("-path1", type=str,
                    help="input file 1", default="file_1.txt")
parser.add_argument("-path2", type=str,
                    help="input file 1", default="file_2.txt")
parser.add_argument("-p", type=str,
                    help="probability", default=0.2)
args = parser.parse_args()
with open(args.path1) as inp_file:
    inp_data = inp_file.read()
    real_data = list(map(int, inp_data.split(' ')))
with open(args.path2) as inp_file:
    inp_data = inp_file.read()
    sint_data = list(map(int, inp_data.split(' ')))
print(method1(real_data, sint_data, args.p))
print(method2(real_data, sint_data, args.p))
print(method3(real_data, sint_data, args.p))
