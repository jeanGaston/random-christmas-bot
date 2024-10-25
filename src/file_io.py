import csv
from datetime import date
from env import CSV_PREFIX, CSV_PATH

def load_history(years):
    """
    Load participant data from multiple CSV files based on the specified history years.
    :param years: Number of years of history to load.
    :return: A list of all historical draw data.
    """
    current_year = date.today().year
    history_data = []

    # Load data for each of the past specified years
    for i in range(1, years + 1):
        
        try:
            year = current_year - i
            file_name = f"{CSV_PATH}/{CSV_PREFIX}_{year}.csv"
            with open(file_name, "r", encoding='utf-8') as file:
                reader = csv.reader(file)
                history_data.extend(list(reader))  # Add each year's data
        except FileNotFoundError:
            print(f"No historical file found for year {year}, skipping.")
            continue           

    return history_data

def load_participants():
    """
    Load participant data from the current year CSV file.
    :return: A list of all historical draw data.
    """
    current_year = date.today().year
    participants_data = []
    try:
        file_name = f"{CSV_PATH}/{CSV_PREFIX}_{current_year}.csv"
        print(file_name)
        with open(file_name, "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            participants_data.extend(list(reader))  # Add each year's data
    except FileNotFoundError:
        print(f"No  file found for year {current_year}, skipping.")
                    

    return participants_data

def save_csv(data, year):
    """
    Save the new draw results to a CSV file named with the current year.
    :param data: New draw data.
    :param year: The current year for naming the file.
    """
    file_name = f"{CSV_PATH}/{CSV_PREFIX}_{year}.csv"
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)