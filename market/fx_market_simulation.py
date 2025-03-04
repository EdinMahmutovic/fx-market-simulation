import random
from typing import Dict, List

from market.market_maker import MarketMaker
from market.market_taker import MarketTaker
from market.orderbook import OrderBook
from price_construction.price_crossing import PriceCrossing
from price_construction.vwap_price import VWAPPrice
from util.currency_pair import CurrencyPair
from util.side import Side


class FXMarketSimulation:
    def __init__(self, currency_pairs: List[CurrencyPair]):
        self.currency_pairs = currency_pairs
        # Ensure that required pairs for crossing exist.
        # For instance, to price GBP/SEK, include GBP/USD.
        self.order_books: Dict[CurrencyPair, OrderBook] = {
            cp: OrderBook(currency_pair=cp, book_size=10) for cp in currency_pairs
        }
        # Create a price production mechanism.
        self.price_production = VWAPPrice(vwap_mid_price=3, vwap_spread=3)
        for cp, ob in self.order_books.items():
            self.price_production.update(ob)
        # Create a PriceCrossing instance.
        self.price_crossing = PriceCrossing(currency_pairs, self.price_production)
        # Create one MarketMaker that will price all currency pairs.
        self.market_maker = MarketMaker(target_currency_pairs=currency_pairs,
                                        price_crossing=self.price_crossing,
                                        risk_factor=random.uniform(0.5, 1.5))

    def run(self, steps: int = 10):
        for step in range(steps):
            print(f"\n--- Step {step} ---")
            # MarketMaker places orders on every currency pair.
            self.market_maker.place_orders(self.order_books)
            # Print consensus prices and strategies.
            for cp, ob in self.order_books.items():
                mid, spread = self.price_production.calculate_consensus_price_for(cp)
                strat = self.price_crossing.get_pricing_strategy(cp)
                strat_str = strat["strategy"]
                if strat_str == "cross":
                    strat_str += f" via pivot {strat['pivot']}"
                print(f"{cp}: Mid = {mid:.4f}, Spread = {spread:.4f}, Strategy = {strat_str}")
            # Random market takers execute orders on random pairs.
            for cp, ob in self.order_books.items():
                side = random.choice(list(Side))
                taker = MarketTaker(side, size=random.uniform(1, 5))
                price, size = taker.place_order(ob)
                print(f"MarketTaker {side.value} on {cp}: Executed {size:.2f} at {price:.4f}")
