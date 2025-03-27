import datetime
from contextlib import closing
import yfinance as yf
import pandas as pd
import pandas_market_calendars as mcal
import numpy_financial as npf

NUM_OF_MARKET_DAYS_IN_A_YEAR = 252
NUM_OF_MONTHS_IN_A_YEAR = 12


def is_market_open(date):
    date = date.date()
    nyse = mcal.get_calendar('NYSE')
    schedule = nyse.schedule(start_date=date, end_date=date)
    return not schedule.empty


def calculate_annualized_irr(daily_investment_amount, closing_prices, portfolio_value):
    total_invested = daily_investment_amount * len(closing_prices)
    cash_flows = [-daily_investment_amount] * len(closing_prices)
    cash_flows.append(portfolio_value)
    irr = npf.irr(cash_flows)

    annual_irr = ((1 + irr) ** NUM_OF_MARKET_DAYS_IN_A_YEAR) - 1
    return annual_irr * 100


def main():

    while True:
        # Define the ticker symbol
        ticker_symbol = input("Please enter the ticker symbol of the stock: ")
        stock_info = yf.Ticker(ticker_symbol)

        company_name = stock_info.info['shortName']

        # Get user input for start and end dates
        start_date_str = input("Enter the start date (YYYY-MM-DD): ")
        end_date_str = input("Enter the end date (YYYY-MM-DD): ")

        frequency = input("Are you planning to invest daily (d), monthly (m), or yearly (y)? ")

        daily_investment_amount = 0.0
        if 'm' in frequency.lower():
            monthly_investment_amount = float(input("Please enter the amount you are planning to invest monthly: $"))
            daily_investment_amount = (monthly_investment_amount * NUM_OF_MONTHS_IN_A_YEAR) / NUM_OF_MARKET_DAYS_IN_A_YEAR
        elif 'y' in frequency.lower():
            yearly_investment_amount = float(input("Please enter the amount you are planning to invest yearly: $"))
            daily_investment_amount = yearly_investment_amount / NUM_OF_MARKET_DAYS_IN_A_YEAR
        else:
            daily_investment_amount = float(input("Please enter the amount you are planning to invest daily: $"))

        # Convert the string input into datetime objects
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        # Ensure that the start date falls on a market day
        while not is_market_open(start_date):
            start_date = start_date - datetime.timedelta(days=1)
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

        today_date = (datetime.datetime.now()).replace(hour=0, minute=0, second=0, microsecond=0)
        ten_days_before_today = (datetime.datetime.now() - datetime.timedelta(days=10)).replace(hour=0, minute=0, second=0, microsecond=0)

        # print(f"\n\n\nStart date: {start_date}; type = {type(start_date)}")
        # print(f"Today's date: {today_date}; type = {type(today_date)}")
        # print(f"10 days before today's date: {ten_days_before_today}; type = {type(ten_days_before_today)}\n\n\n")

        # Fetch the stock data from Yahoo Finance for the specified period
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
        past_ten_days_stock_data = yf.download(ticker_symbol, start=ten_days_before_today, end=today_date)

        # Get the closing prices as a list of floats

        closing_prices = stock_data['Close']

        # print(f'\n\n\nClosing prices = {closing_prices}\n\n\n')
        closing_prices = closing_prices.values.flatten().tolist()
        # print(f'\n\n\nClosing prices after flattening= {closing_prices}\n\n\n')
        past_ten_days_closing_prices = past_ten_days_stock_data['Close'].values.flatten().tolist()

        # Print the closing prices
        # print(f"Closing prices for {company_name}: {closing_prices}")

        # Calculate the average price (Dollar Cost Averaging)
        average_price = sum(closing_prices) / len(closing_prices)

        # Get the latest closing price in the data range
        latest_closing_price = closing_prices[-1]
        todays_closing_price = past_ten_days_closing_prices[-1]

        # Calculate the rate of return based on Dollar Cost Averaging
        rate_of_return = ((latest_closing_price / average_price) - 1) * 100

        num_investment_days = len(closing_prices)

        invested_amount = daily_investment_amount * num_investment_days

        profit = invested_amount * (rate_of_return / 100)

        portfolio_value = invested_amount + profit

        num_of_stocks = portfolio_value / latest_closing_price

        todays_portfolio_value = num_of_stocks * todays_closing_price

        final_today_rate_of_return = ((todays_portfolio_value / invested_amount) - 1)
        final_today_rate_of_return_percent = final_today_rate_of_return * 100
        final_profit = round(invested_amount * final_today_rate_of_return, 2)

        annual_irr_percent = calculate_annualized_irr(daily_investment_amount, closing_prices, todays_portfolio_value)


        # Display the results
        print(f"\nTicker symbol: {ticker_symbol}")
        print(f"Average price of {ticker_symbol} during the time period: ${average_price:.2f}")
        print(f"Price of {ticker_symbol} at the end of the time period: ${latest_closing_price:.2f}")
        print(f"Absolute Rate of return upon daily Dollar Cost Averaging for {company_name} from {start_date.strftime('%b %d, %Y')} to {end_date.strftime('%b %d, %Y')}: {rate_of_return:,.2f}%")
        print(f"Amount invested: ${invested_amount:,.2f}")
        print(f"Profit: ${profit:,.2f}")
        print(f"Portfolio value: ${portfolio_value:,.2f}")
        print(f"Number of stocks: {num_of_stocks:,.3f}")
        if end_date <= today_date:
            print(f"If you had held onto the {company_name} stocks until today, your portfolio value would have been: ${todays_portfolio_value:,.2f} with a net growth of ${final_profit:,} which is {final_today_rate_of_return_percent:,.2f}% of total growth")
            print(f"Annualized Internal Rate of Return = {annual_irr_percent:,.2f}%")

        # Ask the user if they want to continue with another stock
        continue_ = input("Do you wish to know the rate of return for another stock? (y/n): ")
        if 'n' in continue_.lower():
            print("Thank you for trying out Dollar Cost Average Return on Investment Calculator! Have a nice day!")
            break

def estimation(ticker_symbol, start_date_str, end_date_str, investment, frequency):
    stock_info = yf.Ticker(ticker_symbol)

    company_name = stock_info.info['shortName']

    daily_investment_amount = 0.0
    if 'm' in frequency.lower():
        monthly_investment_amount = investment
        daily_investment_amount = (monthly_investment_amount * NUM_OF_MONTHS_IN_A_YEAR) / NUM_OF_MARKET_DAYS_IN_A_YEAR
    elif 'y' in frequency.lower():
        yearly_investment_amount = investment
        daily_investment_amount = yearly_investment_amount / NUM_OF_MARKET_DAYS_IN_A_YEAR
    else:
        daily_investment_amount = investment

    # Convert the string input into datetime objects
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    # Ensure that the start date falls on a market day
    while not is_market_open(start_date):
        start_date = start_date - datetime.timedelta(days=1)
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

    today_date = (datetime.datetime.now()).replace(hour=0, minute=0, second=0, microsecond=0)
    ten_days_before_today = (datetime.datetime.now() - datetime.timedelta(days=10)).replace(hour=0, minute=0, second=0, microsecond=0)

    # Fetch the stock data from Yahoo Finance for the specified period
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    past_ten_days_stock_data = yf.download(ticker_symbol, start=ten_days_before_today, end=today_date)

    # Get the closing prices as a list of floats

    closing_prices = stock_data['Close']

    # print(f'\n\n\nClosing prices = {closing_prices}\n\n\n')
    closing_prices = closing_prices.values.flatten().tolist()
    # print(f'\n\n\nClosing prices after flattening= {closing_prices}\n\n\n')
    past_ten_days_closing_prices = past_ten_days_stock_data['Close'].values.flatten().tolist()

    # Calculate the average price (Dollar Cost Averaging)
    average_price = sum(closing_prices) / len(closing_prices)

    # Get the latest closing price in the data range
    latest_closing_price = closing_prices[-1]
    todays_closing_price = past_ten_days_closing_prices[-1]

    # Calculate the rate of return based on Dollar Cost Averaging
    rate_of_return = ((latest_closing_price / average_price) - 1) * 100

    num_investment_days = len(closing_prices)

    invested_amount = daily_investment_amount * num_investment_days

    profit = invested_amount * (rate_of_return / 100)

    portfolio_value = invested_amount + profit

    num_of_stocks = portfolio_value / latest_closing_price

    todays_portfolio_value = num_of_stocks * todays_closing_price

    final_today_rate_of_return = ((todays_portfolio_value / invested_amount) - 1)
    final_today_rate_of_return_percent = final_today_rate_of_return * 100
    final_profit = round(invested_amount * final_today_rate_of_return, 2)

    annual_irr_percent = calculate_annualized_irr(daily_investment_amount, closing_prices, todays_portfolio_value)
    
    # Return Results
    return {'ticker': ticker_symbol, 'avg_price': round(average_price, 2), 'end_price': round(latest_closing_price, 2), 'abs_return': round(rate_of_return, 2), 'amount_inv': round(invested_amount, 2), 'profit': round(profit, 2), 'value': round(portfolio_value, 2), 'stocks': round(num_of_stocks, 2), 'today_value': round(todays_portfolio_value, 2), 'final_profit': final_profit, 'final_return': round(final_today_rate_of_return_percent, 2), 'ann_return': round(annual_irr_percent, 2)}

if __name__ == "__main__":
    main()