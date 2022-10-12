from abc import ABCMeta, abstractmethod


class SizeException(Exception):
    pass


class Worker:
    def __init__(self):
        self._account = 0

    def take_salary(self, int):
        self._account += int

    @staticmethod
    def get_matrix(path_in):
        """
        Read matrix from .txt file

        Parameters
        ----------
        path_in : str
            The path to the file


        Returns
        -------
        matrix : list
            Matrix from file
        """
        with open(path_in) as inp_file:
            inp_data = inp_file.read()
        # STRINGS TO MATRIX
        m_strings = inp_data.split('\n')
        matrix_1 = []
        i = 0
        while i < len(m_strings) != '':
            matrix_1.append(m_strings[i].split(' '))
            i += 1
        return matrix_1

    @staticmethod
    def print_matrix(matrix_res):
        """
        Print matrix to the screen

        Parameters
        ----------
        matrix_res : list
            The matrix that is to be written
        """
        for i in range(len(matrix_res)):
            print(' '.join(str(num) for num in matrix_res[i]))

    @abstractmethod
    def do_work(self, filename1, filename2):
        pass

    def __str__(self):
        return str(self._account)


class Pupa(Worker):
    def do_work(self, filename1, filename2):
        """
        Summation matrices

        Parameters
        ----------
        filename1 : str
            Path to first matrix
        filename2 : str
            Path to second matrix
        """
        matrix_1 = self.get_matrix(filename1)
        matrix_2 = self.get_matrix(filename2)
        if len(matrix_1) != len(matrix_2) or len(matrix_1[0]) != len(matrix_2[0]):
            raise SizeException("Incorrect matrix sizes")
        matrix_res = []
        sum_m = 0

        for i in range(len(matrix_1)):
            matrix_res.append([])
            for j in range(len(matrix_2[0])):
                matrix_res[i].append(float(matrix_1[i][j]) + float(matrix_2[i][j]))
        self.print_matrix(matrix_res)


class Lupa(Worker):
    def do_work(self, filename1, filename2):
        """
        Subtraction matrices

        Parameters
        ----------
        filename1 : str
            Path to first matrix
        filename2 : str
            Path to second matrix
        """
        matrix_1 = self.get_matrix(filename1)
        matrix_2 = self.get_matrix(filename2)
        if len(matrix_1) != len(matrix_2) or len(matrix_1[0]) != len(matrix_2[0]):
            raise SizeException("Incorrect matrix sizes")
        matrix_res = []
        sum_m = 0

        for i in range(len(matrix_1)):
            matrix_res.append([])
            for j in range(len(matrix_2[0])):
                matrix_res[i].append(float(matrix_1[i][j]) - float(matrix_2[i][j]))
        self.print_matrix(matrix_res)


class Accountant:
    @staticmethod
    def give_salary(worker):
        match worker:
            case Lupa():
                worker.take_salary(12)
            case Pupa():
                worker.take_salary(10)


accountant = Accountant()
pupa = Pupa()
pupa.do_work("first.txt", "second.txt")
lupa = Lupa()
lupa.do_work("first.txt", "second.txt")
accountant.give_salary(pupa)
accountant.give_salary(lupa)
print(f"Lupa: {lupa}")
print(f"Pupa: {pupa}")
