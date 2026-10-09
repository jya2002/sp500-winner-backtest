
from src.backtest import run_backtest, build_strategy_returns, buy_and_hold
from src.market_data import get_bulk_historical_returns
from src.tax import calculate_profit, calculate_tax, capital_after_tax
from src.metrics import calculate_max_drawdown, calculate_volatility
from src.sp500 import get_sp500_tickers_for_year
from src.portfolio import calculate_portfolio_value
from src.visualization import plot_portfolio


START_YEAR = 2020
END_YEAR = 2025
INITIAL_CAPITAL = 10_000
TAX_RATE = 0.3784


def load_historical_members():
    """Henter historiske S&P 500-medlemmer."""

    historical_members = {}

    for year in range(START_YEAR, END_YEAR + 1):
        tickers = get_sp500_tickers_for_year(year)
        historical_members[year] = tickers

        print(f"{year}: {len(tickers)} indeksmedlemmer")

    return historical_members


def collect_tickers(historical_members):
    """Samler alle unike tickere."""

    all_tickers = set()

    for tickers in historical_members.values():
        all_tickers.update(tickers)

    all_tickers = sorted(all_tickers)

    print("\nTotalt antall unike aksjer:", len(all_tickers))

    return all_tickers


def report_missing_tickers(historical_members, historical_returns):
    """Rapporterer manglende historiske kursdata."""

    missing_tickers = set()

    for year, members in historical_members.items():
        available = historical_returns.get(year, {})

        missing = [
            ticker
            for ticker in members
            if ticker not in available
        ]

        missing_tickers.update(missing)

        print(
            f"{year}: "
            f"{len(members) - len(missing)}/{len(members)} "
            "medlemmer med kursdata"
        )

    print(
        "\nTotalt antall unike manglende tickere:",
        len(missing_tickers)
    )

    return sorted(missing_tickers)


def calculate_spy_results(spy_annual_returns):
    """Beregner SPY-porteføljen før og etter sluttskatt."""

    capital = INITIAL_CAPITAL
    spy_values = [capital]

    for year in sorted(spy_annual_returns):
        annual_return = spy_annual_returns[year]

        capital = calculate_portfolio_value(
            capital,
            annual_return
        )

        spy_values.append(capital)

    profit = calculate_profit(INITIAL_CAPITAL, capital)
    tax = calculate_tax(profit, TAX_RATE)
    after_tax = capital_after_tax(capital, tax)

    return spy_values, after_tax


def main():

    # 1. Historiske indeksmedlemmer
    historical_members = load_historical_members()

    # 2. Samle alle aksjene
    all_tickers = collect_tickers(historical_members)

    # 3. Hent historisk avkastning fra Yahoo Finance
    historical_returns = get_bulk_historical_returns(
        all_tickers,
        START_YEAR,
        END_YEAR
    )

    # 4. Kontroller manglende data
    missing_tickers = report_missing_tickers(
        historical_members,
        historical_returns
    )

    # 5. Bygg strategien
    strategy_returns = build_strategy_returns(
        historical_returns,
        historical_members
    )

    # 6. Kjør backtest
    backtest_results = run_backtest(
        INITIAL_CAPITAL,
        strategy_returns,
        TAX_RATE
    )

    if not backtest_results:
        print("Ingen resultater fra backtesten.")
        return

    # 7. Hent SPY-avkastning
    spy_returns = get_bulk_historical_returns(
        ["SPY"],
        START_YEAR + 1,
        END_YEAR
    )

    spy_annual_returns = {}

    for year, returns in spy_returns.items():
        if "SPY" in returns:
            spy_annual_returns[year] = returns["SPY"]

    # 8. Sjekk at begge porteføljene dekker samme år
    strategy_years = [
        result["year"]
        for result in backtest_results
    ]

    expected_years = list(
        range(START_YEAR + 1, END_YEAR + 1)
    )

    if strategy_years != expected_years:
        print(
            "\nAdvarsel: Strategien mangler ett eller flere år."
        )
        print("Forventet:", expected_years)
        print("Faktisk:", strategy_years)
        print("Avbryter sammenligningen.")
        return

    if sorted(spy_annual_returns) != strategy_years:
        print(
            "\nAdvarsel: SPY og strategien har ulik årsdekning."
        )
        print("Strategi:", strategy_years)
        print("SPY:", sorted(spy_annual_returns))
        print("Avbryter sammenligningen.")
        return

    # 9. Vis tradingbotens årsresultater
    print("\n--- ÅRLIGE RESULTATER ---")

    for result in backtest_results:
        print(
            f'{result["year"]}: '
            f'{result["ticker"]} | '
            f'{result["annual_return"] * 100:.2f}% | '
            f'{result["ending_capital"]:.2f} kr'
        )

    # 10. Beregn SPY-resultater
    spy_values, spy_after_tax = calculate_spy_results(
        spy_annual_returns
    )

    strategy_final_capital = backtest_results[-1][
        "ending_capital"
    ]

    print("\n--- RESULTATER ETTER SKATT ---")
    print(f"Tradingbot: {strategy_final_capital:.2f} kr")
    print(f"S&P 500:    {spy_after_tax:.2f} kr")

    # 11. Porteføljeverdier
    strategy_values = [INITIAL_CAPITAL]

    for result in backtest_results:
        strategy_values.append(
            result["ending_capital"]
        )

    # 12. Risikomålinger
    mdd = calculate_max_drawdown(strategy_values)

    annual_returns = [
        result["annual_return"]
        for result in backtest_results
    ]

    volatility = calculate_volatility(annual_returns)

    print("\n--- RISIKO ---")
    print(f"Maximum Drawdown (årsslutt): {mdd:.2%}")
    print(f"Volatilitet (årlig): {volatility:.2%}")

    # 13. Visualisering
    years = [START_YEAR] + strategy_years

    plot_portfolio(
        strategy_values,
        spy_values,
        years
    )


if __name__ == "__main__":
    main()
