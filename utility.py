import json
import os
from datetime import datetime

def write_results_to_json(data, filename_prefix, directory):
    # Check if the directory exists; if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = f"{directory}/{filename_prefix}.json"
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_json_data(filename_prefix, directory, start_date, data_type):
    """
    Load and filter data from a JSON file starting from a specific date.

    Parameters:
    - filename_prefix: The prefix of the filename to load.
    - directory: The directory where the file is located.
    - start_date: A string representing the start date in YYYY-MM-DD format. Data from this date onwards will be loaded.
    - data_type: The type of data being loaded ('price' or 'RSI') to handle different data structures.

    Returns:
    - A list of dictionaries with data from the specified start date onwards, with consistent format.
    """
    filename = f"{directory}/{filename_prefix}.json"
    filtered_data = []

    # Convert start_date string to datetime object for comparison
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        # Process according to data type
        if data_type == 'price':
            for date, price in data.items():
                item_date = datetime.strptime(date, '%Y-%m-%d')
                if item_date >= start_date_dt:
                    filtered_data.append({"date": date, "value": price})
        elif data_type == 'RSI':
            for date, details in data.items():
                item_date = datetime.strptime(date, '%Y-%m-%d')
                if item_date >= start_date_dt:
                    filtered_data.append({"date": date, "value": details["RSI"]})

    return filtered_data

