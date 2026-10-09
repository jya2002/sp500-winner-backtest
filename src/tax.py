'''
Estimerer norsk skatt etter 
gjeldende skatteregler

'''

def calculate_profit(initial_capital, final_capital):
    profit = final_capital - initial_capital
    return profit


def calculate_tax(profit, tax_rate):
    if profit <= 0:
        return 0

    tax = profit * tax_rate
    return tax

def capital_after_tax(final_capital, tax):
    current_capital = final_capital - tax

    return current_capital