import numpy as np


def get_vector(matrix):
    vector = []
    height = matrix.shape[0]
    width = matrix.shape[1]

    for h in range(height):
        for w in range(width):
            vector.append(matrix[h, w])

    return vector


def get_toggle_matrix(matrix, i, j):
    t = np.zeros_like(matrix)

    adj = [[0, 0], [0, -1], [-1, 0], [0, 1], [1, 0]]
    for di, dj in adj:
        if (0 <= i + di < t.shape[1]) and (0 <= j + dj < t.shape[0]):
            t[i + di, j + dj] = 1

    return t


def get_augmented_matrix(cells):
    matrix = np.zeros(shape=(cells.shape[0] * cells.shape[1], cells.shape[0] * cells.shape[1] + 1), dtype=int)

    for i in range(cells.shape[0]):
        for j in range(cells.shape[1]):
            index = i * cells.shape[1] + j
            t = get_toggle_matrix(cells, i, j)
            matrix[:, index] = get_vector(t)
    matrix[:, -1] = get_vector(cells)

    return matrix


def find_leftmost_nonzero_column(matrix):
    for i in range(matrix.shape[1]):
        if np.count_nonzero(matrix[:, i]) != 0:
            return i
    return -1


def forward_phase(matrix, row=0):
    if row == matrix.shape[0]:
        return

    pivot_column = find_leftmost_nonzero_column(matrix[row:, :])
    if pivot_column == -1:
        return

    # interchange two rows to have a nonzero element in the pivot position if needed
    if matrix[row, pivot_column] == 0:
        appropriate_row = row
        while matrix[appropriate_row, pivot_column] == 0:
            appropriate_row += 1
        matrix[[row, appropriate_row]] = matrix[[appropriate_row, row]]

    # use row replacement operations to create zeros in all positions below the pivot
    for i in range(row + 1, matrix.shape[0]):
        ratio = int(matrix[i, pivot_column] / matrix[row, pivot_column])
        matrix[i] -= matrix[row] * ratio
        matrix[i] %= 2

    forward_phase(matrix, row + 1)


def get_solution_vector(matrix):
    for row in matrix:
        if (row[:-1] == 0).all() and row[-1] != 0:
            return None

    vector = np.zeros(shape=(matrix.shape[0]), dtype=int)
    for i in range(matrix.shape[0] - 1, -1, -1):
        vector[i] = matrix[i, matrix.shape[1] - 1]

        for j in range(i + 1, matrix.shape[0]):
            vector[i] -= matrix[i, j] * vector[j]

        vector[i] %= 2

    return vector


def print_solution(cells):
    matrix = get_augmented_matrix(cells)
    forward_phase(matrix)
    answer = get_solution_vector(matrix)

    if answer is None:
        print("There is no solution :(")
    else:
        for i in range(len(answer)):
            if answer[i] == 1:
                x = i % cells.shape[1]
                y = i // cells.shape[1]
                print(f'click on block [{y + 1}, {x + 1}]')
