# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 10:40:58 2024

@author: Nhu Ngo and Sri Bhamidipati
"""

# Extract word
def extract_word(input_file, word):
    lines_list = []
    extracted_list = []
    
    with open(input_file, 'r') as infile:
        for line in infile:
            lines_list.append(line.strip())  # Store each line in the list
            
    # Extract characters between index 25 and 26 for each line
    for line in lines_list:
        if (word == "B"):
            if (line[0:1] == word): 
                extracted_list.append(line)  
        else:
            if (line[0:2] == word):
                extracted_list.append(line)  

    return extracted_list

# create B
extracted_list_B = extract_word('cme.20210709.c.pa2',"B")
print(len(extracted_list_B));

# check the first half in the first table
first_list = []
for line in extracted_list_B:
    if (line[5:7] == "CL" and line[15:18] == 'FUT'):
        first_list.append(line)

print(len(first_list))

# check the second half in the first table
second_list = []
for line in extracted_list_B:
    if (line[5:8] == 'LO ' and line[99:102] == 'CL ' and line[15:18] == 'OOF'):
        second_list.append(line)

print(len(second_list))

# Run the list for 81
extracted_81 = extract_word('cme.20210709.c.pa2',"81")
print(len(extracted_81));

# check the first FUT
# check the second Call/Put
fut_list = []
C_list = []
P_list = []
        
for line in extracted_81:
    if (line[5:8] == "CL " and line[15:17] == "CL" and line[25:28] == 'FUT'):
        fut_list.append(line)
    if (line[5:8] == "LO " and line[15:17] == "CL" and line[25:29] == 'OOFC'):
        C_list.append(line)
    if (line[5:8] == "LO " and line[15:17] == "CL" and line[25:29] == 'OOFP'):
        P_list.append(line)
        
print(len(fut_list))
print(len(C_list))
print(len(P_list))

# Change date
from datetime import datetime

def is_date_in_range(date_str):
    # Convert the input date string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m")
    
    # Convert the start and end date strings to datetime objects
    start_date = datetime.strptime("2021-09", "%Y-%m")
    end_date = datetime.strptime("2023-12", "%Y-%m")
    
    # Return True if the date is within range, otherwise False
    return start_date <= date_obj <= end_date

# Create the first table
def parse_cme_file(output_file):
    # Set to store extracted and valid rows
    data_to_write = set()
    data2 = set()
    
    for line in first_list:
        # Extract the date and future date
        date = line[18:22] + "-" + line[22:24]
        result = is_date_in_range(date)

        future_date = line[91:95] + "-" + line[95:97]
        contract_type = line[15:18].capitalize()

        if result:
            # Collect the necessary parts for writing to the file later
            row_data = (
                line[5:7],   # Futures Code
                date,        # Contract Expiration Date (first date)
                contract_type, # Contract Type
                future_date + "-" + line[97:99]  # Future Date (future date)
            )
            data_to_write.add(row_data)

    # Sort the collected data first by 'date'
    sorted_data = sorted(data_to_write, key=lambda x: (x[1]))

    for line in second_list:
        # Extract the date and future date
        date = line[18:22] + "-" + line[22:24]
        result = is_date_in_range(date)

        future_date = line[91:95] + "-" + line[95:97]
        
        if result:
            # Collect the necessary parts for writing to the file later
            row_data = (
                line[99:101],   # Futures Code
                date,        # Contract Expiration Date (first date)
                "Opt", # Contract Type
                "   ",
                "LO",
                future_date + "-" + line[97:99]  # Future Date (future date)
            )
            data2.add(row_data)
    # Sort the collected data first by 'date'
    sorted_data2 = sorted(data2, key=lambda x: (x[1]))

    # Write the sorted data to the output file
    with open(output_file, 'w') as outfile:

        header = [["Futures", "Contract", "Contract", "Futures", "Options", "Options"],
                  ["Code", "Month", "Type", "Exp Date", "Code", "Exp Date"],
                  ["-------", "--------", "--------", "--------", "-------", "--------"]]

        for row in header:
            for column in row:
                line = f"{row[0]:12}" \
                       f"{row[1]:12}" \
                       f"{row[2]:12}" \
                       f"{row[3]:12}" \
                       f"{row[4]:12}" \
                       f"{row[5]:12}\n"
            outfile.write(line)

        # Write each sorted row from the first dataset
        for row in sorted_data:
            line = f"{row[0]:12}" \
                   f"{row[1]:12}" \
                   f"{row[2]:12}" \
                   f"{row[3]:12}\n"
            outfile.write(line)

        # Write each sorted row from the second dataset
        for row in sorted_data2:
            line = f"{row[0]:12}" \
                   f"{row[1]:12}" \
                   f"{row[2]:12}" \
                   f"{row[3]:12}" \
                   f"{row[4]:12}" \
                   f"{row[5]:12}\n"
            outfile.write(line)

# Print the second table
def format_sort_81(output_file):
    # Set to store extracted and valid rows
    data_to_write = set()
    data2 = set()
    
    for line in fut_list:
        # Extract the date
        contract_date = line[29:33] + "-" + line[33:35]
        result = is_date_in_range(contract_date)
        futures_code = line[15:17]
        
        contract_type = line[25:28].capitalize()
        
        settlement_price = round(float(line[108:122]) / 100.0, 2) 
        strike_price = ""

        if result:
            # Collect the necessary parts for writing to the file later
            row_data = (
                futures_code,   # Futures Code
                contract_date,        # Contract Expiration Date (first date)
                contract_type, # Contract Type
                strike_price,
                settlement_price
            )
            data_to_write.add(row_data)

    # Sort the collected data first by 'date'
    sorted_data = sorted(data_to_write, key=lambda x: (x[1]))

    second_list_81 = C_list + P_list
    
    for line in second_list_81:
        # Extract the date
        contract_date = line[29:33] + "-" + line[33:35]
        result = is_date_in_range(contract_date)
        
        futures_code = line[15:17]
        
        contract_type = 'Call' if line[28] == 'C' else 'Put'
        
        settlement_price = round(float(line[108:122]) / 100.0, 2)
        strike_price = round(float(line[47:54]) / 1000.0, 2)

        if result:
            # Collect the necessary parts for writing to the file later
            row_data = (
                futures_code,   # Futures Code
                contract_date,        # Contract Expiration Date (first date)
                contract_type, # Contract Type (call/put)
                strike_price,
                settlement_price
            )
            data2.add(row_data)
        
    # Sort the collected data first by 'date' and settlement price
    sorted_data2 = sorted(data2, key=lambda x: (x[1], x[4]))
                          
    # Write the sorted data to the output file
    with open(output_file, 'a') as outfile:

        header = [["Futures", "Contract", "Contract", "Strike", "Settlement"],
                  ["Code", "Month", "Type", "Price", "Price"],
                  ["-------", "--------", "--------", "--------", "-------"]]

        for row in header:
            for column in row:
                line = f"{row[0]:12}" \
                       f"{row[1]:12}" \
                       f"{row[2]:12}" \
                       f"{row[3]:12}" \
                       f"{row[4]:12}\n"
            outfile.write(line)
        

        # Write each sorted row from the first dataset
        for row in sorted_data:
            line = f"{row[0]:12}" \
                   f"{row[1]:12}" \
                   f"{row[2]:12}" \
                   f"{row[3]:10}" \
                   f"{row[4]:11}\n"
            outfile.write(line)

        # Write each sorted row from the second dataset
        for row in sorted_data2:
            line = f"{row[0]:12}" \
                   f"{row[1]:12}" \
                   f"{row[2]:12}" \
                   f"{row[3]:10}" \
                   f"{row[4]:11}\n"
            outfile.write(line)

# Name the output file
output_file = 'CL_expirations_and_settlements.txt'
parse_cme_file(output_file)
format_sort_81(output_file)