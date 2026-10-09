import yfinance as yf

'''
Beregner totalavkastningen til 
hver aksje for året.

'''
# kurs ved starten av året, kurs ved slutten av året

prices = {
    "AAPL": [185.64, 243.85],
    "NVDA": [49.52, 134.29],
    "MSFT": [376.04, 421.50],
    "AMZN": [151.94, 219.39]
}

def calculate_returns(prices):
    returns = {}

    for ticker, price in prices.items():
        annual_return = (price[1] - price[0]) / price[0]
        returns[ticker] = annual_return

    return returns

calculate_returns(prices)

def get_historical_prices(ticker, start_date, end_date):
    '''
    Henter historiske aksjedata
    '''
    stock = yf.Ticker(ticker)
    data = stock.history(
        start=start_date, 
        end=end_date, 
        auto_adjust=True)
    if data.empty:
        return None


    return data

def calculate_annual_return(data):
    '''
    Beregn årlig avkastning

    '''
    annual_return = (data["Close"].iloc[-1] - data["Close"].iloc[0]) / data["Close"].iloc[0] 
    
    return annual_return


def get_multiple_returns(tickers, start_date, end_date):
    returns = {}

    for ticker in tickers:
        data = get_historical_prices(ticker, start_date, end_date)

        if data is not None:
            annual_return = calculate_annual_return(data)
            returns[ticker] = annual_return

    return returns

def get_historical_returns(tickers, start_year, end_year):
    historical_returns = {}

    for year in range(start_year, end_year + 1):
        start_date = f"{year}-01-01"
        end_date = f"{year + 1}-01-01"

        yearly_returns = get_multiple_returns(tickers, start_date, end_date)

        historical_returns[year] = yearly_returns

    return historical_returns

def calculate_multiple_annual_returns(close_prices):
    start_prices = close_prices.iloc[0]
    end_prices = close_prices.iloc[-1]

    returns = (end_prices - start_prices) / start_prices

    return returns



def get_bulk_historical_returns(tickers, start_year, end_year):
    data = yf.download(
        tickers,
        start=f"{start_year - 1}-01-01",        
        end=f"{end_year + 1}-01-01",
        auto_adjust=True,
        progress=False
    )

    close_prices = data["Close"]

    historical_returns = {}

    for year in range(start_year, end_year + 1):
        prices_year = close_prices[close_prices.index.year == year]
        previous_year_prices = close_prices[close_prices.index.year == year - 1]

        if prices_year.empty or previous_year_prices.empty:
            historical_returns[year] = {}
            continue


        last_price_prev_year = previous_year_prices.iloc[-1]
        last_price_curr_year = prices_year.iloc[-1]

        valid_tickers = last_price_prev_year.dropna().index.intersection(
            last_price_curr_year.dropna().index
        )
        print(f"{year}: {len(valid_tickers)} gyldige aksjer")
        
        if len(valid_tickers) == 0:
            historical_returns[year] = {}
            continue

        start_prices = last_price_prev_year[valid_tickers]
        end_prices = last_price_curr_year[valid_tickers]

        valid_start = start_prices > 0

        start_prices = start_prices[valid_start]
        end_prices = end_prices[valid_start]

        yearly_returns = (end_prices - start_prices) / start_prices

        historical_returns[year] = yearly_returns.to_dict()
        
    return historical_returns



if __name__ == "__main__":
    data = yf.download(
        ["AAPL", "MSFT", "NVDA"],
        start="2020-01-01",
        end="2022-01-01",
        auto_adjust=True,
        progress=False
    )

    historical_returns = get_bulk_historical_returns(
    ["AAPL", "MSFT", "NVDA"],
    2021,
    2025
    )

    for year, returns in historical_returns.items():
        print(year, returns)