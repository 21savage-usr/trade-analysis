import requests
import logging
import os
from datetime import datetime, timedelta



# Configuration Setup for Alpha Vantage API
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set the ALPHA_VANTAGE_API_KEY environment variable.")
base_url = 'https://www.alphavantage.co/'


# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def rsi_dataf(symbol):
    url = f'{base_url}query?function=RSI&symbol={symbol}&interval=daily&time_period=14&series_type=open&apikey={api_key}' # this means the daily difference evry 14 days
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: %s", errh)
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: %s", errc)
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: %s", errt)
    except requests.exceptions.RequestException as err:
        logging.error("Other Error: %s", err)


def clean_sort_rsi_data_past_10_years(raw_rsi_data):
    # Extracting the relevant part of the response
    rsi_time_series = raw_rsi_data.get("Technical Analysis: RSI", {})

    # Define the cutoff date for 10 years ago
    cutoff_date = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')

    # Filtering dates to keep only the last 10 years
    filtered_dates = {date: rsi_time_series[date] for date in rsi_time_series if date >= cutoff_date}

    # Sorting the filtered dates
    sorted_rsi_data = {date: filtered_dates[date] for date in sorted(filtered_dates)}

    return sorted_rsi_data



def historical_data(symbol):
    url = f'{base_url}query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}' # this means the daily difference evry 14 days
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: %s", errh)
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: %s", errc)
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: %s", errt)
    except requests.exceptions.RequestException as err:
        logging.error("Other Error: %s", err)


def clean_sort_historical_data_for_closing_past_10_years(raw_price_data):
    # Extracting the relevant part of the response
    price_time_series = raw_price_data.get("Time Series (Daily)", {})

    # Define the cutoff date for 10 years ago
    cutoff_date = (datetime.now() - timedelta(days=365 * 10)).strftime('%Y-%m-%d')

    # Filtering dates to keep only the last 10 years
    filtered_dates = {date: price_time_series[date] for date in price_time_series if date >= cutoff_date}

    # Sorting the filtered dates and preparing the sorted data for closing prices
    sorted_closing_data = {date: filtered_dates[date].get("4. close", None) for date in sorted(filtered_dates)}

    return sorted_closing_data