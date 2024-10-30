import sys
def create_value_dict():
    # Read values from the input file and create a dictionary
    with open(sys.argv[1], "r") as input_file:
        rows = [line.split() for line in input_file]
    # Create a dictionary with (row, column) as keys and values from the file
    value_dict = {(rows_index + 1, columns_index + 1): rows[rows_index][columns_index] for rows_index in range(len(rows)) for columns_index in range(len(rows[0]))}
    return value_dict, rows

def create_columns(rows):
    # Create columns from rows
    columns = [[row[column_index] for row in rows] for column_index in range(len(rows[0]))]
    # Sort columns, '*' will be moved to the end
    for inner_list in columns:
        inner_list.sort(key=lambda x: x == '*', reverse=True)
    return columns

def check_is_sort(value_dict, rows):
    # Check if the board is in a valid state (no adjacent equal numbers)
    for index in range(1, len(rows) + 1):
        for index_2 in range(1, len(rows[0]) + 1):
            # Define neighbors for the current position (right, down, left, up)
            check_list = [(index + 1, index_2), (index, index_2 + 1), (index - 1, index_2), (index, index_2 - 1)]
            for check in range(4):
                if check_list[check] in value_dict:
                    if value_dict[index, index_2] == value_dict[check_list[check]] and (value_dict[check_list[check]] and value_dict[index, index_2] != "*"):
                        return True
    return False

def create_table(rows, value_dict):
    # Create a printable table from the dictionary
    table = [[' ' for _ in row] for row in rows]
    for key, value in value_dict.items():
        table[key[0] - 1][key[1] - 1] = value
    table_string = ""
    for row in table:
        # Convert the table to a string for printing
        row_string = ' '.join([' ' if cell == '*' else str(cell) for cell in row])
        table_string += row_string.rstrip() + '\n'
    return table_string

def check_neighbor_equals(row, column, value_dict):
    equals_dict = {}
    print_statment = True
    if (row, column) in value_dict:
        if value_dict[row, column] != "*":
            # Define neighbors for the current position (right, down, left, up)
            check_list = [(row + 1, column), (row, column + 1), (row - 1, column), (row, column - 1)]
            for check in range(4):
                if check_list[check] in value_dict:
                    if value_dict[check_list[check]] == value_dict[row, column] and (value_dict[check_list[check]] != "*"):
                        equals_dict[check_list[check]] = value_dict[check_list[check]]
            if equals_dict == {}:
                # No movement happened, print a message
                print("No movement happened. Try again.\n")
        else:
            print("Please enter a correct size!\n")
            print_statment = False
    else:
        print("Please enter a correct size!\n")
        print_statment = False
    return equals_dict, print_statment

def equals_index(input_value_row, input_value_column, value_dict, score):
    # Find all connected equals and update the score
    all_equals_dict, print_statment = check_neighbor_equals(input_value_row, input_value_column, value_dict)
    while True:
        all_equals_dict2 = {}
        for neighbor_row, neighbor_column in all_equals_dict:
            all_equals_dict1, print_statment = check_neighbor_equals(neighbor_row, neighbor_column, value_dict)
            all_equals_dict2.update(all_equals_dict1)

        all_equals_dict3 = all_equals_dict.copy()
        all_equals_dict.update(all_equals_dict2)
        if all_equals_dict3 == all_equals_dict:
            break
    for value in all_equals_dict.values():
        score += int(value)

    all_equals_dict = {key: "*" for key in all_equals_dict}
    value_dict.update(all_equals_dict)
    return all_equals_dict, score, value_dict, print_statment

def update_rows(rows, value_dict):
    # Update rows based on the value_dict
    for key, value in value_dict:
        rows[int(key) - 1][int(value) - 1] = value_dict[key, value]
    return rows

def update_value_dict(columns, value_dict):
    # Update value_dict based on columns
    for index in range(len(columns)):
        for index2 in range(len(columns[0])):
            value_dict[index2 + 1, index + 1] = columns[index][index2]
    return value_dict

def remove_empty_rows_and_columns(rows,score):
    # Remove empty rows and columns and update the value_dict

    rows_to_remove = [index for index, row in enumerate(rows) if all(element == '*' for element in row)]
    for row_index in reversed(rows_to_remove):
        del rows[row_index]
    if not rows:
        print("Your score is: ", score, "\n")
        print("Game over")
        sys.exit()
    columns_to_remove = [index for index, column in enumerate(create_columns(rows)) if
                         all(element == '*' for element in column)]
    for column_index in reversed(columns_to_remove):
        for row in rows:
            del row[column_index]

    value_dict = update_value_dict(create_columns(rows), {})
    return rows, value_dict

def main():
    value_dict, rows = create_value_dict()
    score = 0
    print(create_table(rows, value_dict))
    print("Your score is: ", score, "\n")
    while True:
        if not check_is_sort(value_dict, rows):
            print("Game over")
            break
        else:
            input_value_row, input_value_column = [int(x) for x in input("Please enter a row and a column number: ").split()]
            print(" ")
            all_equals_dict, score, value_dict, print_statment = equals_index(input_value_row, input_value_column, value_dict, score)
            rows = update_rows(rows, value_dict)
            columns = create_columns(rows)
            value_dict = update_value_dict(columns, value_dict)
            rows = update_rows(rows, value_dict)
            rows, value_dict = remove_empty_rows_and_columns(rows,score)
            if print_statment:
                print(create_table(rows, value_dict))
                print("Your score is: ", score, "\n")

if __name__ == "__main__":
    main()
