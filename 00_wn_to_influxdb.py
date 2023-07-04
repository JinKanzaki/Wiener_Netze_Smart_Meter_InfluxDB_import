import csv
import datetime
import time
import os

input_file = 'input.csv'
timestamps = 'timestamps.csv'
timestamps_unix = 'timestamps_unix.csv'
output_file = 'output.csv'
data_file = 'data.csv'
file_list = ['timestamps.csv', 'timestamps_unix.csv', 'data.csv', 'input.csv']

def remove_first_row(input_file):
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    data = data[1:]  # Exclude the first row
    
    with open(input_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def count_rows(input_file):
    global no_of_rows
    
    with open(input_file, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        no_of_rows = len(rows)

def remove_double_semicolon(input_file):
    with open(input_file, 'r', newline='') as file:
        rows = csv.reader(file)
        updated_rows = []

        for row in rows:
            updated_row = [cell.replace(';;', '') for cell in row]
            updated_rows.append(updated_row)

    with open(input_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

def replace_comma_with_dot(input_file):
    with open(input_file, 'r', newline='') as file:
        lines = file.readlines()

    with open(input_file, 'w', newline='') as file:
        for line in lines:
            updated_line = line.replace(',', '.')
            file.write(updated_line)

def change_delimiter(input_file):
    with open(input_file, 'r', newline='') as file:
        rows = csv.reader(file, delimiter=';')
        data = [','.join(row) for row in rows]

    with open(input_file, 'w', newline='') as file:
        file.writelines('\n'.join(data))

def extract_time_columns(input_file, timestamps):
    with open(input_file, 'r', newline='') as file:
        rows = csv.reader(file)
        extracted_data = [[row[0], row[2]] for row in rows]

    with open(timestamps, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(extracted_data)

def timestamps_to_unix(timestamps, timestamps_unix):

    # Open the input and output files
    with open(timestamps, 'r', encoding='utf-8-sig') as csv_input, open(timestamps_unix, 'w', encoding='utf-8-sig', newline='') as csv_output:
        reader = csv.reader(csv_input)
        writer = csv.writer(csv_output)

        # Iterate over each row in the input file
        for row in reader:
            date_str = row[0]
            time_str = row[1]

            # Combine the date and time strings into a single datetime object
            datetime_str = f"{date_str} {time_str}"
            datetime_obj = datetime.datetime.strptime(datetime_str, "%d.%m.%Y %H:%M:%S")

            # Convert the datetime object to a Unix timestamp
            unix_timestamp = int(time.mktime(datetime_obj.timetuple()))

            # Write the Unix timestamp to the output file
            writer.writerow([unix_timestamp])

def create_output_csv(output_file, rows):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for _ in range(rows):
            row = ['kWh', 'entity_id=15_min_energy_usage']
            writer.writerow(row)

def create_data_csv(input_file, timestamps_unix, data_file):
    with open(input_file, 'r', newline='') as input_file, \
            open(timestamps_unix, 'r', newline='') as timestamps, \
            open(data_file, 'w', newline='') as data:

        input_file_reader = csv.reader(input_file)
        timestamps_reader = csv.reader(timestamps)
        data_writer = csv.writer(data, delimiter= ' ')

        for input_file_row, timestamp_row in zip(input_file_reader, timestamps_reader):
            data_row = ['Unit=kWh', input_file_row[3], timestamp_row[0]]
            data_writer.writerow(data_row)

def append_value_to_column(data_file):
    with open(data_file, 'r', newline='') as file:
        rows = csv.reader(file, delimiter= ' ')
        data = [row[:1] + ['value=' + row[1]] + row[2:] for row in rows]

    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter= ' ')
        writer.writerows(data)

def data_into_output(data_file, output_file):
    with open(data_file, 'r', newline='') as data_file, open(output_file, 'r', newline='') as output_file:
        data_reader = csv.reader(data_file)
        output_reader = csv.reader(output_file)
        output_data = list(output_reader)

        if len(output_data) == 0:
            print("Error: output.csv is empty.")
            return

        for i, row in enumerate(data_reader):
            if i < len(output_data):
                output_data[i].insert(3, row[0])
            else:
                print("Error: data.csv has more rows than output.csv.")
                return

    with open('output.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(output_data)

def delete_intermediate_files(file_list):
    for file in file_list:
        if os.path.exists(file):
            os.remove(file)


remove_first_row(input_file)
count_rows(input_file)
remove_double_semicolon(input_file)
replace_comma_with_dot (input_file)
change_delimiter(input_file)
extract_time_columns(input_file, timestamps)
timestamps_to_unix(timestamps, timestamps_unix)
create_output_csv(output_file, no_of_rows)
create_data_csv(input_file, timestamps_unix, data_file)
append_value_to_column(data_file)
data_into_output(data_file, output_file)
delete_intermediate_files(file_list)