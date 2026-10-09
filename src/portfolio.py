
'''
Beregner realisert gevinst/tap.

'''

def calculate_portfolio_value(capital, annual_return):
    new_capital = (capital * annual_return) + capital

    return new_capital


