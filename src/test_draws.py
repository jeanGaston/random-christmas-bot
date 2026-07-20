import csv
from typing import List, Tuple, Set

from env import CSV_PATH, CSV_PREFIX

# Load CSV data from a file
def load_csv(filepath: str) -> List[List[str]]:
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [row for row in reader]

# Extract giver-receiver pairs from data
def extract_pairs(data: List[List[str]]) -> Set[Tuple[str, str]]:
    pairs = set()
    for record in data:
        giver = record[0]
        recipients = record[2:]  # Recipients start from the third column
        pairs.update((giver, recipient) for recipient in recipients)
    return pairs

# Generalized function to check conflicts between years, including current draw as a list
def check_conflicts(csv_path: str, csv_prefix: str, years: List[int], current_year_draw: List[List[str]] = None) -> None:
    # Load data and extract pairs for each specified year
    pairs_by_year = {}
    for year in years:
        file_path = f"{csv_path}/{csv_prefix}_{year}.csv"
        year_data = load_csv(file_path)
        pairs_by_year[year] = extract_pairs(year_data)
    
    # Add current year’s draw if provided
    if current_year_draw:
        pairs_by_year['current'] = extract_pairs(current_year_draw)
    
    # Check for conflicts across all pairs of years
    year_keys = list(pairs_by_year.keys())
    for i, year1 in enumerate(year_keys):
        for year2 in year_keys[i+1:]:
            conflicts = pairs_by_year[year1].intersection(pairs_by_year[year2])
            if conflicts:
                print(f"Conflicts found between {year1} and {year2}:")
                for conflict in conflicts:
                    print(conflict)
            else:
                print(f"No conflicts between {year1} and {year2}.")

if __name__ == "__main__":
    # Example usage: adjust years_to_check to whichever history years you want to verify.
    years_to_check = [2022, 2023, 2024]

    # Current year's draw passed as a list
    current_year_draw = [
        ["Alice", "alice@example.com", "Bob", "Charlie"],
        ["Bob", "bob@example.com", "Alice", "David"],
        ["Charlie", "charlie@example.com", "David", "Alice"]
    ]

    check_conflicts(CSV_PATH, CSV_PREFIX, years_to_check, current_year_draw)
