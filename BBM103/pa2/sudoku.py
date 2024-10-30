import sys

def create_allnumber(input_file):
    # This function creates a list called all_number containing all the numbers from the input file.
    all_number = []
    for number in input_file:
        for number1 in str(number).split():
            all_number.append(number1)
    return all_number

def count_of_zeros(all_number):
    # This function returns the count of zeros in the all_number list, representing how many steps there are.
    count_of_zeros = all_number.count("0")
    return count_of_zeros

def create_rows(all_number):
    # This function creates a list called rows, containing a list of all rows.
    rows = []
    for rows_point in range(9):
        # Every 9 elements represent 1 row.
        rows.append(all_number[rows_point * 9:(rows_point + 1) * 9])
    return rows

def create_column(rows):
    # This function creates a list called columns, containing a list of all columns.
    columns = []
    for column_index in range(9):
        column = []
        for row in rows:
            # Rows are used to find column values. The first column contains the 1st element of each row.
            column.append(row[column_index])
        columns.append(column)
    return columns

def box_value(rows, rows_index, columns_index):
    # This function creates a list called box_values, containing a list of all 9x9 boxes and returns which box the index is in.
    box_values = []
    box_row = (rows_index // 3) * 3
    box_column = (columns_index // 3) * 3
    for box_i in range(box_row, box_row + 3):
        for box_j in range(box_column, box_column + 3):
            # Rows are used to find column values.
            box_values.append(rows[box_i][box_j])
    return box_values

def which_possibility(possibility_number, rows, rows_index, columns, columns_index, box_values):
    # This function checks if there is a value in the possibility numbers.
    result = [x for x in possibility_number if x not in rows[rows_index]]
    result1 = [x for x in result if x not in columns[columns_index]]
    result2 = [x for x in result1 if x not in box_values]
    return result2

def create_steps(rows):
    # This function creates solutions for each step.
    last = []
    for last_row in rows:
        for last_row1 in last_row:
            last.append(last_row1)
    last_str = ""
    for last_index in range(len(last)):
        last_str += last[last_index]
        last_str += " "
        if (last_index + 1) % 9 == 0:
            last_str = last_str.strip()
            last_str += "\n"
    return last_str

def create_solution(all_number, rows, possibility_number, columns):
    # This function creates output.
    solution_step = []
    for how_many_steps in range(count_of_zeros(all_number)):
        outer_break = False
        for rows_index in range(9):
            for columns_index in range(9):
                if not rows[rows_index][columns_index] in possibility_number:
                    box_values = box_value(rows, rows_index, columns_index)
                    result2 = which_possibility(possibility_number, rows, rows_index, columns, columns_index,
                                                box_values)
                    if len(result2) == 1:
                        rows[rows_index][columns_index] = result2[0]
                        columns[columns_index][rows_index] = result2[0]
                        last_str = create_steps(rows)
                        step = "------------------\nStep {0} - {1} @ R{2}C{3}\n------------------\n{4}".format(
                            how_many_steps + 1, result2[0], rows_index + 1, columns_index + 1, last_str)
                        solution_step.append(step)
                        outer_break = True
                        break
            if outer_break:
                break
    return "".join(solution_step).strip() + "\n------------------"

def main():
    input_file = open(sys.argv[1], "r")
    output_file = open(sys.argv[2], "w")

    possibility_number = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    all_number = create_allnumber(input_file)
    rows = create_rows(all_number)
    columns = create_column(rows)
    output_file.write(create_solution(all_number, rows, possibility_number, columns))

    input_file.close()
    output_file.flush()
    output_file.close()

if __name__ == "__main__":
    main()
