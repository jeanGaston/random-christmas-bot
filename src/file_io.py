import csv
import os
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

def load_exclusions():
    """
    Load exclusion pairs from a CSV file.
    :return: A set of tuples representing invalid combinations (giver, receiver).
    """
    exclusions = set()
    current_year = date.today().year
    try:
        file_name = f"{CSV_PATH}/{CSV_PREFIX}_exclusions.csv"
        with open(file_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    exclusions.add(tuple(row))
    except FileNotFoundError:
        print(f"Exclusion file not found: {file_name}. No exclusions will be applied.")
    return exclusions

def save_csv(data, year):
    """
    Save the new draw results to a CSV file named with the current year.
    :param data: New draw data.
    :param year: The current year for naming the file.
    """
    os.makedirs(CSV_PATH, exist_ok=True)
    file_name = f"{CSV_PATH}/{CSV_PREFIX}_{year}.csv"
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def load_year(year):
    """Load raw CSV rows for a specific year, or [] if the file doesn't exist."""
    file_name = f"{CSV_PATH}/{CSV_PREFIX}_{year}.csv"
    try:
        with open(file_name, "r", encoding='utf-8') as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        return []

def add_participant(name, email):
    """Append a participant (name, email) to the current year's CSV file."""
    current_year = date.today().year
    os.makedirs(CSV_PATH, exist_ok=True)
    file_name = f"{CSV_PATH}/{CSV_PREFIX}_{current_year}.csv"
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name, email])

def remove_participant(name):
    """Remove a participant by name from the current year's CSV file."""
    participants = [p for p in load_participants() if p[0] != name]
    save_csv(participants, date.today().year)

def add_exclusion(giver, receiver):
    """Append a (giver, receiver) pair to the exclusions CSV file."""
    os.makedirs(CSV_PATH, exist_ok=True)
    file_name = f"{CSV_PATH}/{CSV_PREFIX}_exclusions.csv"
    with open(file_name, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([giver, receiver])

def remove_exclusion(giver, receiver):
    """Remove a (giver, receiver) pair from the exclusions CSV file."""
    exclusions = {pair for pair in load_exclusions() if pair != (giver, receiver)}
    os.makedirs(CSV_PATH, exist_ok=True)
    file_name = f"{CSV_PATH}/{CSV_PREFIX}_exclusions.csv"
    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(exclusions)