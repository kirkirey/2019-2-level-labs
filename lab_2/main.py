"""
Labour work #2. Levenshtein distance.
"""


def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    matrix = []
    if type(num_rows) is not int or type(num_cols) is not int:
        return matrix
    else:
        for i in range(num_rows):
            this_row = []
            for j in range(num_cols):
                this_row.append(0)
            matrix.append(this_row)
        return matrix


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    if type(edit_matrix) is list:
        edit_matrix = tuple(edit_matrix)
    if type(add_weight) is not int or type(remove_weight) is not int or edit_matrix is () or [] in edit_matrix:
        return list(edit_matrix)
    count = 0
    for i in edit_matrix:  # заполнение первого столбца
        i[0] = count
        count += remove_weight
    for i in range(len(edit_matrix[0]) - 1):  # заполнение первой строчки
        edit_matrix[0][i + 1] = edit_matrix[0][i] + add_weight
    return list(edit_matrix)


def minimum_value(numbers: tuple) -> int:
    minimum = numbers[0]
    for i in numbers:
        if i < minimum:
            minimum = i
    return minimum


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    if type(add_weight) is not int or type(remove_weight) is not int or type(substitute_weight) is not int or type(
            original_word) is not str or type(target_word) is not str:
        return list(edit_matrix)
    for i in range(len(edit_matrix) - 1):  # строка:   edit_matrix[i]  элемент:    edit_matrix[i][j]
        for j in range(len(edit_matrix[i]) - 1):  # (len(*)-1) потому что я изменяю [i+1][j+1]
            vertical = edit_matrix[i][j + 1] + remove_weight
            horizontal = edit_matrix[i + 1][j] + add_weight
            if original_word[i] == target_word[j]:
                diagonal = edit_matrix[i][j]
            else:
                diagonal = edit_matrix[i][j] + substitute_weight
            edit_matrix[i + 1][j + 1] = minimum_value(tuple([vertical, horizontal, diagonal]))
    return list(edit_matrix)


def find_distance(original_word: str,
                  target_word: str,
                  add_weight: int,
                  remove_weight: int,
                  substitute_weight: int) -> int:
    if type(add_weight) is not int or type(remove_weight) is not int or type(substitute_weight) is not int or type(
            original_word) is not str or type(target_word) is not str:
        return -1
    matrix = generate_edit_matrix(len(original_word) + 1, len(target_word) + 1)
    matrix = initialize_edit_matrix(tuple(matrix), add_weight, remove_weight)
    matrix = fill_edit_matrix(tuple(matrix), add_weight, remove_weight, substitute_weight, original_word, target_word)
    return matrix[len(original_word)][len(target_word)]


def save_to_csv(edit_matrix: tuple, path_to_file: str) -> None:
    with open(path_to_file, 'w') as file:
        for row_mat in edit_matrix:
            row_doc = []
            for i in row_mat:
                row_doc += str(i)
            row_doc = ','.join(row_doc)
            file.write(row_doc + '\n')
    return


def load_from_csv(path_to_file: str) -> list:
    matrix = []
    with open(path_to_file, 'r') as file:
        rows_doc = file.readlines()
        for row_doc in rows_doc:
            row_mat = []
            for i in row_doc.split(','):
                row_mat.append(int(i))
            matrix.append(row_mat)
    return list(matrix)
