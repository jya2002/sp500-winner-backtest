
import matplotlib.pyplot as plt


def plot_portfolio(strategy_values, spy_values, years):

    plt.figure(figsize=(10, 6))

    plt.plot(
        years,
        strategy_values,
        marker="o",
        label="Tradingbot (etter årlig skatt)"
    )

    plt.plot(
        years,
        spy_values,
        marker="o",
        label="S&P 500 / SPY (før sluttskatt)"
    )

    plt.xlabel("År")
    plt.ylabel("Porteføljeverdi (kr)")
    plt.title("S&P 1-strategien vs S&P 500")

    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()
