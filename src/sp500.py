from pathlib import Path
import pandas as pd
import requests
from io import StringIO

def get_sp500_tickers():
    """
    Returnerer en liste over aksjesymbolene
    til selskapene i S&P 500.
    """

    url = "https://en.wikipedia.org/w/index.php?title=List_of_S%26P_500_companies&action=render"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    print("Status:", response.status_code)
    print("HTML-lengde:", len(response.text))

    print(
        "Finnes endringsseksjonen?",
        "Selected changes to the list of S&P 500 components"
        in response.text
    )

    print("Antall HTML-tabeller:", response.text.count("<table"))
    tables = pd.read_html(StringIO(response.text))

    df = tables[0]
    tickers = df["Symbol"].tolist()

    formatted_tickers = []

    for ticker in tickers:
        formatted_ticker = ticker.replace(".", "-")
        formatted_tickers.append(formatted_ticker)

    return formatted_tickers

def get_sp500_changes():
    """
    Henter historiske tillegg og fjerninger
    fra S&P 500.
    """
    pass


def get_sp500_tickers_for_year(year):
    """
    Rekonstruerer indeksmedlemmer
    per 31. desember i angitt år.
    """
    project_root = Path(__file__).resolve().parent.parent

    csv_path = project_root / "data" / "sp_500_historical_components.csv"

    df = pd.read_csv(csv_path)
    
    df["date"] = pd.to_datetime(df["date"])

    target_date = pd.Timestamp(f"{year}-12-31")

    historical_df = df[df["date"] <= target_date]
    if historical_df.empty:
        return []

    latest_row_idx = historical_df["date"].idxmax()
    latest_row = historical_df.loc[latest_row_idx]

    tickers_string = latest_row["tickers"]

    tickers_list = tickers_string.split(",")

    formatted_tickers = []

    for ticker in tickers_list:
        formatted_ticker = ticker.replace(".", "-").strip()
        formatted_tickers.append(formatted_ticker)

    return formatted_tickers


if __name__ == "__main__":
    for year in range(2020, 2026):
        tickers = get_sp500_tickers_for_year(year)

        print(f"{year}: {len(tickers)} aksjer")
        print("Første 10:", tickers[:10])
  