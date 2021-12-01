from common.loader import Loader


def checksum_row(row):
    return max(row) - min(row)


def checksum(matrix):
    return sum([checksum_row(row) for row in matrix])


def checksum_mod_row(row):
    for i in row:
        for j in row:
            if (i != j) & (i % j == 0):
                return i // j


def checksum_mod(matrix):
    return sum([checksum_mod_row(row) for row in matrix])


mat = Loader.load_matrix("test_data.txt", delimiter='\\s+', numeric=True)
print(checksum(mat))

mat = Loader.load_matrix("input.txt", delimiter='\\s+', numeric=True)
print(checksum(mat))

mat = Loader.load_matrix("test_data_2.txt", delimiter='\\s+', numeric=True)
print(checksum_mod(mat))

mat = Loader.load_matrix("input.txt", delimiter='\\s+', numeric=True)
print(checksum_mod(mat))