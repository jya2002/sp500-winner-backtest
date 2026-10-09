import statistics

"""
Funksjoner som måler hvor 
godt en strategi presterer
"""

def calculate_cagr(initial_capital, final_capital, years):
    '''
    gjennomsnittlig årlig
    geometrisk avkastning
    '''
    cagr = (final_capital / initial_capital)** (1 / years) - 1
    return cagr

def calculate_max_drawdown(portfolio_values):
    '''
    Maximum Drawdown (MDD) er 
    det største prosentvise fallet 
    i porteføljeverdi fra en tidligere 
    topp til en senere bunn.

    Det måler risikoen i tradingboten
    '''

    peak = portfolio_values[0]
    max_drawdown = 0

    for value in portfolio_values:
        if value > peak:
            peak = value

        drawdown = (peak - value) / peak

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return max_drawdown


def calculate_volatility(returns):
    '''
    Volatilitet måler hvor mye avkastningen
    varierer over tid. Vi bruker standardavviket
    til de årlige avkastningene.
    '''
    if len(returns) < 2:
        return None
    
    return statistics.stdev(returns)
