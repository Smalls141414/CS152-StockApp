import pandas_datareader as pdr
from datetime import datetime, date, timedelta

NUM_OF_DAYS_IN_A_YEAR = 365
FAT_FIRE_MULTIPLE = 50
PERCENTAGE_MULTIPLIER = 100
INFLATION_TIME_PERIOD = 200


calculate_inflation_adjusted_retirement_amount = lambda retirement_amount, years_until_retirement, annual_inflation_rate: retirement_amount * ((1 + annual_inflation_rate) ** years_until_retirement)
calculate_retirement_amount = lambda annual_expenses : FAT_FIRE_MULTIPLE * annual_expenses
calculate_years_until_retirement = lambda current_age, retirement_age : retirement_age - current_age


def calculate_inflation_rate_over_past_n_years(n=INFLATION_TIME_PERIOD):
    end = date.today()
    start = end - timedelta(days=NUM_OF_DAYS_IN_A_YEAR * n)
    data = pdr.get_data_fred('CPIAUCSL', start, end)
    annual_cpi = data.resample('YE').first()
    inflation_rates = annual_cpi.pct_change()
    start_year = str(start.year)
    end_year = str(end.year)
    inflation_list = inflation_rates[start_year : end_year]['CPIAUCSL'].tolist()[1:]
    average = lambda list_ : (sum(list_) / len(list_))
    average_inflation_rate_over_past_50_years = average(inflation_list)
    print(f'\n\n\naverage inflation rate over past 50 years = {average_inflation_rate_over_past_50_years}\n\n\n')
    return average_inflation_rate_over_past_50_years


def main():
    annual_expenses = float(input("Please enter your estimated annual expenditure (e.g., total yearly spending on living expenses, bills, and discretionary costs): $"))
    current_age = float(input("Please enter your current age: "))
    retirement_age = float(input("Please enter your planned retirement age: "))
    years_until_retirement = calculate_years_until_retirement(current_age, retirement_age)
    retirement_amount_raw = calculate_retirement_amount(annual_expenses)
    inflation_rate = calculate_inflation_rate_over_past_n_years()
    inflation_adjusted_retirement_amount = calculate_inflation_adjusted_retirement_amount(retirement_amount_raw, years_until_retirement, inflation_rate)
    print(f"You would need to have saved a total of ${inflation_adjusted_retirement_amount:,.2f} to retire comfortably {years_until_retirement} years from today (at the time of retirement). This amount is adjusted for inflation of {inflation_rate*PERCENTAGE_MULTIPLIER:,.2f}% based on the average annual inflation in the United States over the past {INFLATION_TIME_PERIOD} years and reflects the future value, not the amount you need to have saved today.")
    print(f"For context, the amount would be worth ${retirement_amount_raw:,.2f} today")

def calculate(annual_expenses, current_age, retirement_age):
    years_until_retirement = calculate_years_until_retirement(current_age, retirement_age)
    retirement_amount_raw = calculate_retirement_amount(annual_expenses)
    inflation_rate = calculate_inflation_rate_over_past_n_years()
    inflation_adjusted_retirement_amount = calculate_inflation_adjusted_retirement_amount(retirement_amount_raw, years_until_retirement, inflation_rate)
    return {'retire_amt': round(inflation_adjusted_retirement_amount, 2), 'retire_years': years_until_retirement, 'inflate_rate': round(inflation_rate*PERCENTAGE_MULTIPLIER, 2), 'time_period': INFLATION_TIME_PERIOD, 'retire_amt_raw': retirement_amount_raw}
