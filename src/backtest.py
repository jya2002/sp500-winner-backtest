from src.portfolio import calculate_portfolio_value
from src.tax import calculate_profit
from src.tax import calculate_tax
from src.tax import capital_after_tax
from src.winner import find_winner

yearly_returns = {
    2020: 0.50,
    2021: 0.40,
    2022: -0.05,
    2023: 1.80,
    2024: 1.35
}

initial_capital = 10_000
tax_rate = 0.3784

def run_backtest(initial_capital, yearly_returns, tax_rate):
    results = []
    capital = initial_capital
    for year, data in yearly_returns.items():
        ticker = data["ticker"]
        annual_return = data["return"]
        initial_capital = capital
        capital = calculate_portfolio_value(capital, annual_return)
        profit = calculate_profit(initial_capital, capital)
        tax = calculate_tax(profit, tax_rate)
        capital = capital_after_tax(capital, tax)

        year_result = {
            "year": year, 
            "ticker": ticker,
            "starting_capital": initial_capital,
            "annual_return": annual_return,
            "profit": profit, 
            "tax": tax, 
            "ending_capital": capital
        }

        results.append(year_result)    
     
    return results


historical_returns = {
    2020: {
        "AAPL": 0.80,
        "NVDA": 1.20,
        "MSFT": 0.40
    },
    2021: {
        "AAPL": 0.35,
        "NVDA": 1.25,
        "MSFT": 0.50
    },
    2022: {
        "AAPL": -0.27,
        "NVDA": -0.50,
        "MSFT": -0.29
    }
}

def build_strategy_returns(historical_returns, historical_members):
    """
    Investerer i forrige års S&P 500-vinner.
    """
    strategy_returns = {}

    for year, returns in sorted(historical_returns.items()):

        if not returns:
            continue

        if year not in historical_members:
            continue

        eligible_tickers = set(historical_members[year])
        eligible_returns = {}

        for ticker, annual_return in returns.items():
            if ticker in eligible_tickers:
                eligible_returns[ticker] = annual_return

        if not eligible_returns:
            print(f"Advarsel: Ingen gyldige aksjer for {year}")
            continue

        winner, annual_return = find_winner(eligible_returns)
        next_year = year + 1

        if next_year not in historical_returns:
            continue

        if winner not in historical_returns[next_year]:
            print(f"Advarsel: {winner} mangler kursdata for {next_year}")
            continue

        next_year_return = historical_returns[next_year][winner]

        strategy_returns[next_year] = {
            "ticker": winner,
            "return": next_year_return
        }

    return strategy_returns


def buy_and_hold(initial_capital, annual_returns):
    capital = initial_capital

    for year, annual_return in annual_returns.items():
        if annual_return is not None:
            capital = calculate_portfolio_value(capital, annual_return)


    return capital 



