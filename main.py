from utility import load_json_data
from utility import write_results_to_json


def simulate_momentum_accumulative_strategy(rsi_data, price_data, rsi_buy_threshold, rsi_sell_threshold):
    capital = 10000  # Starting capital
    capital_per_trade = 200  # Capital allocated per trade
    shares_held = []  # List to track (number of shares, buy price) tuples
    total_profit = 0
    trade_count = 0
    buy_count = 0

    # Create a dictionary for easy access to price by date
    price_by_date = {item['date']: float(item['value']) for item in price_data}
    
    # Iterate through RSI data since it drives buy/sell decisions
    for item in rsi_data:
        date = item['date']
        rsi_value = float(item['value'])
        # Ensure the date exists in price data before proceeding
        if date in price_by_date:
            price = price_by_date[date]
            
            if rsi_value < rsi_buy_threshold and capital >= capital_per_trade:
                buy_count += 1
                shares_bought = capital_per_trade // price
                if shares_bought > 0:  # Ensure shares can be bought
                    shares_held.append((shares_bought, price))
                    capital -= shares_bought * price
            
            elif rsi_value > rsi_sell_threshold and shares_held:
                total_shares = sum(shares for shares, _ in shares_held)
                total_buy_cost = sum(shares * buy_price for shares, buy_price in shares_held)
                profit = total_shares * price - total_buy_cost
                total_profit += profit
                capital += total_shares * price
                shares_held.clear()  # Clear the list of shares held
                trade_count += 1
    
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
                rsi_data = load_json_data(f'{company}_rsi', 'data/rsi/', '2014-01-01', 'RSI')
                price_data = load_json_data(f'{company}_price', 'data/price/', '2014-01-01', 'price')

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



if __name__ == "__main__":
    companies = ['MSFT', 'AAPL', 'NVDA', 'GOOG', 'AMZN', 'META', 'BRK-B', 'LLY', 'TSM', 'AVGO', 'JPM', 'V', 'NVO', 'TSLA']
    
    # Define ranges for buy and sell thresholds to test
    buy_thresholds = range(75, 90, 1)  # Example: 20, 25, 30
    sell_thresholds = range(75, 90, 1)  # Example: 65, 70, 75

    # Run the simulations with different threshold combinations
    ranked_results = test_different_thresholds(companies, buy_thresholds, sell_thresholds)

    # Display the ranked results
    for result in ranked_results:
        print(result)


# # Example usage
# if __name__ == "__main__":
#     companies = ['MSFT', 'AAPL', 'NVDA', 'GOOG', 'AMZN', 'META', 'BRK-B', 'LLY', 'TSM', 'AVGO', 'JPM', 'V', 'NVO', 'TSLA']
#     profit = 0
#     for company in companies:
#         #rsi_data = clean_sort_rsi_data_past_10_years(rsi_dataf(company))
#         #price_data = clean_sort_historical_data_for_closing_past_10_years(historical_data(company))
#         #write_results_to_json(rsi_data, f'{company}_rsi', "data/rsi")
#         #write_results_to_json(price_data, f'{company}_price, "data/price")
#         rsi_data = load_json_data(f'{company}_rsi')
#         price_data = load_json_data(f'{company}_price')
#         strategy_result = simulate_momentum_accumulative_strategy(rsi_data, price_data, 84, 85)
#         profit += strategy_result["Total Profit"]
#         print(f"For {company}: {strategy_result}")
    
#     print(f"Total profit across all companies: {profit}")
