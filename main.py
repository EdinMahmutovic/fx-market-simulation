import random

from market.fx_market_simulation import FXMarketSimulation
from util.currency_pair import CurrencyPair

if __name__ == '__main__':
    # Initiate currency pairs
    currency_pairs = [
        CurrencyPair("EUR", "USD"),
        CurrencyPair("GBP", "USD"),
        CurrencyPair("EUR", "SEK"),
        CurrencyPair("EUR", "NOK"),
        CurrencyPair("EUR", "DKK"),
        CurrencyPair("USD", "SEK"),
        CurrencyPair("USD", "NOK"),
        CurrencyPair("USD", "DKK"),
        CurrencyPair("GBP", "SEK"),
        CurrencyPair("GBP", "NOK"),
        CurrencyPair("GBP", "DKK"),
    ]
    # Create and run the simulation
    simulation = FXMarketSimulation(currency_pairs)
    simulation.run(steps=5)
