import requests
import logging
import json
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

def write_results_to_json(data, filename_prefix, directory):
    # Check if the directory exists; if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = f"{directory}/{filename_prefix}.json"
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_json_data(filename_prefix, directory="data"):
    filename = f"{directory}/{filename_prefix}.json"
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)




def simulate_momentum_accumulative_strategy(rsi_data, price_data, rsi_buy_threshold, rsi_sell_threshold):
    capital = 10000  # Starting capital
    capital_per_trade = 200  # Capital allocated per trade
    shares_held = []  # List to track (number of shares, buy price) tuples
    total_profit = 0
    trade_count = 0
    
    dates = sorted(set(rsi_data.keys()) & set(price_data.keys()))
    buy_count = 0
    
    for date in dates:
        rsi_value = float(rsi_data[date]['RSI'])
        price = float(price_data[date])
        
        if rsi_value < rsi_buy_threshold and capital >= capital_per_trade:
            buy_count += 1
            shares_bought = capital_per_trade // price
            if shares_bought > 0:  # Ensure shares can be bought
                shares_held.append((shares_bought, price))
                capital -= shares_bought * price
                #print(f"Bought on {date} at {price}, shares: {shares_bought}, rsi: {rsi_value}")
        
        elif rsi_value > rsi_sell_threshold and shares_held:
            total_shares = sum(shares for shares, _ in shares_held)
            total_buy_cost = sum(shares * buy_price for shares, buy_price in shares_held)
            profit = total_shares * price - total_buy_cost
            total_profit += profit
            capital += total_shares * price
            shares_held.clear()  # Clear the list of shares held
            trade_count += 1
            print(f"Sold all on {date} at {price}, Profit: {profit}, rsi: {rsi_value}")
    
    profit_percentage = (total_profit / 10000) * 100    
    return {
        "Final Capital": capital,
        "Total Profit": total_profit,
        "Buy Count": buy_count,
        "Sell Count": trade_count,
        "Profit Percentage": profit_percentage
    }


def test_different_thresholds(companies, buy_thresholds, sell_thresholds):
    results = []

    for buy_threshold in buy_thresholds:
        for sell_threshold in sell_thresholds:
            if buy_threshold >= sell_threshold:
                # This condition is skipped because buy_threshold should be less than sell_threshold
                continue

            total_profit = 0
            for company in companies:
                rsi_data = load_json_data(f'{company}_rsi')
                price_data = load_json_data(f'{company}_price')

                strategy_result = simulate_momentum_accumulative_strategy(rsi_data, price_data, buy_threshold, sell_threshold)
                total_profit += strategy_result["Total Profit"]

            results.append({
                "Buy Threshold": buy_threshold,
                "Sell Threshold": sell_threshold,
                "Total Profit": total_profit
            })

    # Sort the results by "Total Profit" in descending order
    results = sorted(results, key=lambda x: x["Total Profit"], reverse=True)
    return results

# if __name__ == "__main__":
#     companies = ['MSFT', 'AAPL', 'NVDA', 'GOOG', 'AMZN', 'META', 'BRK-B', 'LLY', 'TSM', 'AVGO', 'JPM', 'V', 'NVO', 'TSLA']
    
#     # Define ranges for buy and sell thresholds to test
#     buy_thresholds = range(75, 90, 1)  # Example: 20, 25, 30
#     sell_thresholds = range(75, 90, 1)  # Example: 65, 70, 75

#     # Run the simulations with different threshold combinations
#     ranked_results = test_different_thresholds(companies, buy_thresholds, sell_thresholds)

#     # Display the ranked results
#     for result in ranked_results:
#         print(result)


# Example usage
if __name__ == "__main__":
    companies = ['MSFT', 'AAPL', 'NVDA', 'GOOG', 'AMZN', 'META', 'BRK-B', 'LLY', 'TSM', 'AVGO', 'JPM', 'V', 'NVO', 'TSLA']
    profit = 0
    for company in companies:
        #rsi_data = clean_sort_rsi_data_past_10_years(rsi_dataf(company))
        #price_data = clean_sort_historical_data_for_closing_past_10_years(historical_data(company))
        #write_results_to_json(rsi_data, f'{company}_rsi', "data/rsi")
        #write_results_to_json(price_data, f'{company}_price, "data/price")
        rsi_data = load_json_data(f'{company}_rsi')
        price_data = load_json_data(f'{company}_price')
        strategy_result = simulate_momentum_accumulative_strategy(rsi_data, price_data, 84, 85)
        profit += strategy_result["Total Profit"]
        print(f"For {company}: {strategy_result}")
    
    print(f"Total profit across all companies: {profit}")
