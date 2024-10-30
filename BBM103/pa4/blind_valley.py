import sys
def read_input():
    with open(sys.argv[1], "r") as file:
        lines = file.readlines()
        # Extracting values from the first four lines
        highs_row = list(map(int, lines[0].split())) # Left heights
        bases_row = list(map(int, lines[1].split())) # Right bases
        highs_col = list(map(int, lines[2].split())) # Top heights
        bases_col = list(map(int, lines[3].split())) # Bottom bases
        # Extracting the puzzle grid
        rows = [list(line.strip().split()) for line in lines[4:]]
        columns = []

        # Creating columns from the rows
        for column_index in range(len(rows[0])):
            column = []
            for row in rows:
                column.append(row[column_index])
            columns.append(column)
        # Initializing empty tables
        table_row = [[' ' for _ in range(len(row))] for row in rows] # Empty rows
        table_column = [[' ' for _ in range(len(column1))] for column1 in columns] #empty columns

        input_data = {'highs_row': highs_row,'bases_row': bases_row,'highs_col': highs_col,'bases_col': bases_col,'rows': rows,'columns': columns,'table_row':table_row,'table_column':table_column}
        return input_data

def solve_puzzle(highs_row, bases_row, highs_col, bases_col, rows, columns, table_row, table_column):
    # Find the next empty cell to fill
    current_row, current_column = find_empty_cell(table_row, table_column)
    available_cases = ['H', 'B', 'N']

    for tile in available_cases:
        # Check if placing the tile in the current cell is valid
        if check_neighbors(rows, current_row, current_column, tile, table_row):
            # Place the tile and update tables
            table_row[current_row][current_column] = tile
            table_column[current_column][current_row] = tile
            table_row, table_column = fill_general(rows, table_row, table_column, current_row, current_column)

            # Check if the puzzle is solved
            if sum(row.count(' ') for row in table_row) == 0:
                if is_solution(highs_row, bases_row, highs_col, bases_col, table_row, table_column):
                    return table_row  # Puzzle solved, return the result
                else:
                    # Puzzle not solved, backtrack
                    table_row[current_row][current_column] = ' '
                    table_column[current_column][current_row] = ' '
                    table_row, table_column = fill_general(rows, table_row, table_column, current_row,
                                                            current_column)
            else:
                # Continue solving recursively
                result = solve_puzzle(highs_row, bases_row, highs_col, bases_col, rows, columns, table_row,
                                      table_column)
                if result:
                    return result
            # Backtrack
            table_row[current_row][current_column] = ' '
            table_column[current_column][current_row] = ' '
            table_row, table_column = fill_general(rows, table_row, table_column, current_row,
                                                    current_column)
        else:
            continue
    return None  # No solution found

def is_solution(highs_row, bases_row, highs_col, bases_col, table_row, table_column):
    # Check if the current configuration is a valid solution
    for i, row in enumerate(table_row):
        high_count = row.count('H')
        base_count = row.count('B')
        if highs_row[i] != -1 and high_count != highs_row[i]:
            return False
        if bases_row[i] != -1 and base_count != bases_row[i]:
            return False

    for j, col in enumerate(table_column):
        high_count = col.count('H')
        base_count = col.count('B')
        if highs_col[j] != -1 and high_count != highs_col[j]:
            return False
        if bases_col[j] != -1 and base_count != bases_col[j]:
            return False
    return True

def find_empty_cell(table_row, table_column):
    # Find the next empty cell in the tables
    for i in range(len(table_row)):
        for j in range(len(table_column)):
            if table_row[i][j] == ' ':
                return i, j

def check_neighbors(rows, current_row, current_column, value, table_row):
    # Check if placing the specified value in the current cell is valid based on neighbors
    if value != " " and value != "N":
        if current_column < len(rows[0]) - 1 and table_row[current_row][current_column + 1] == value:
            return False

        if current_column > 0 and table_row[current_row][current_column - 1] == value:
            return False

        if current_row > 0 and table_row[current_row - 1][current_column] == value:
            return False

        if current_row < len(rows) - 1 and table_row[current_row + 1][current_column] == value:
            return False

        if rows[current_row][current_column] == "L":
            if value == "H":
                return check_neighbors(rows, current_row, current_column + 1, "B", table_row)
            if value == "B":
                return check_neighbors(rows, current_row, current_column + 1, "H", table_row)

        if rows[current_row][current_column] == "U":
            if value == "H":
                return check_neighbors(rows, current_row + 1, current_column, "B", table_row)
            if value == "B":
                return check_neighbors(rows, current_row + 1, current_column, "H", table_row)

    return True

def fill_general(rows, table_row, table_column, current_row, current_column):
    # Fill the tables based on the rules
    if rows[current_row][current_column] == "L":
        if table_row[current_row][current_column] == "H" and check_neighbors(rows, current_row, current_column + 1,
                                                                             "B", table_row):
            table_row[current_row][current_column + 1] = "B"
            table_column[current_column + 1][current_row] = "B"

        elif table_row[current_row][current_column] == "B" and check_neighbors(rows, current_row, current_column + 1,
                                                                               "H", table_row):
            table_row[current_row][current_column + 1] = "H"
            table_column[current_column + 1][current_row] = "H"

        elif table_row[current_row][current_column] == "N":
            table_row[current_row][current_column + 1] = "N"
            table_column[current_column + 1][current_row] = "N"

        elif table_row[current_row][current_column] == " ":
            table_row[current_row][current_column + 1] = " "
            table_column[current_column + 1][current_row] = " "

        else:
            table_row[current_row][current_column] = " "

    elif rows[current_row][current_column] == "U":
        if table_row[current_row][current_column] == "H" and check_neighbors(rows, current_row + 1, current_column,
                                                                             "B", table_row):
            table_row[current_row + 1][current_column] = "B"
            table_column[current_column][current_row + 1] = "B"

        elif table_row[current_row][current_column] == "B" and check_neighbors(rows, current_row + 1, current_column,
                                                                               "H", table_row):
            table_row[current_row + 1][current_column] = "H"
            table_column[current_column][current_row + 1] = "H"

        elif table_row[current_row][current_column] == "N":
            table_row[current_row + 1][current_column] = "N"
            table_column[current_column][current_row + 1] = "N"

        elif table_row[current_row][current_column] == " ":
            table_row[current_row + 1][current_column] = " "
            table_column[current_column][current_row + 1] = " "

        else:
            table_row[current_row][current_column] = " "

    return table_row, table_column

def print_solution(table_row):
    # Generate a string representation of the solution
    rows = []
    for i, row in enumerate(table_row):
        row_str = " ".join(row)
        rows.append(row_str)
    return "\n".join(rows)

def main():
    # Main function to execute the puzzle solving
    input_data = read_input()
    highs_row = input_data['highs_row']
    bases_row = input_data['bases_row']
    highs_col = input_data['highs_col']
    bases_col = input_data['bases_col']
    rows = input_data['rows']
    columns = input_data['columns']
    table_row = input_data['table_row']
    table_column = input_data['table_column']
    table_row = solve_puzzle(highs_row, bases_row, highs_col, bases_col, rows, columns, table_row, table_column)
    output_file = open(sys.argv[2], "w")

    if table_row:
        # Write the solution to the output file
        output_file.write(print_solution(table_row))
    else:
        output_file.write("No solution!")

if __name__ == "__main__":
    # Run the main function when the script is executed
    main()

