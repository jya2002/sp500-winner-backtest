import yfinance as yf

tickers = ["AVB", "EQR", "BK", "EA"]

for ticker in tickers:
    stock = yf.Ticker(ticker)

    data = stock.history(
        start="2020-01-01",
        end="2021-01-01",
        auto_adjust=True
    )

    print(f"\n{ticker}")
    print("Antall rader:", len(data))

    if not data.empty:
        print(data.head(2))