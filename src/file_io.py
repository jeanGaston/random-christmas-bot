import csv

def open_csv(file_name):
    """Open the CSV file and return its contents as a list of rows"""
    with open(file_name, "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)

def save_csv(data, file_name):
    """Save the updated draw results to the CSV file"""
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
