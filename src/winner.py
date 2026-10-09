"""
Identifiserer aksjen med høyest avkastning.
"""
returns = {
    "AAPL": 0.30,
    "NVDA": 0.82,
    "MSFT": 0.18,
    "AMZN": -0.05,
    "META": 0.44
}

def find_winner(returns):
    winner = None
    highest_return = float("-inf")
    for ticker, annual_return in returns.items():
        if annual_return > highest_return:
            highest_return = annual_return
            winner = ticker

    return winner, highest_return

winner, annual_return = find_winner(returns)
