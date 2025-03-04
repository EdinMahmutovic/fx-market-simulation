import random
from typing import Dict

from market.market_maker import MarketMaker
from market.market_taker import MarketTaker
from market.orderbook import OrderBook
from price_construction.vwap_price import VWAPPrice
from util.currency_pair import CurrencyPair
from util.side import Side


class FXMarketSimulation:
    def __init__(self, currency_pairs):
        """
        currency_pairs: List of CurrencyPair instances.
        """
        self.currency_pairs = currency_pairs
        # Create an OrderBook for each currency pair
        self.order_books: Dict[CurrencyPair, OrderBook] = {
            cp: OrderBook(currency_pair=cp, book_size=10) for cp in currency_pairs
        }
        # Create a general price production mechanism (VWAPPrice here)
        self.price_production = VWAPPrice(vwap_mid_price=3, vwap_spread=3)
        # Create a MarketMaker for each currency pair
        self.market_makers: Dict[CurrencyPair, MarketMaker] = {
            cp: MarketMaker(currency_pair=cp, price_production=self.price_production, risk_factor=random.uniform(0.5, 1.5))
            for cp in currency_pairs
        }

    def run(self, steps: int = 10):
        for step in range(steps):
            print(f"\n--- Step {step} ---")
            # Each market maker places orders on its order book
            for cp, mm in self.market_makers.items():
                ob = self.order_books[cp]
                mm.place_orders(ob)
                consensus_mid, consensus_spread = self.price_production.calculate_consensus_price()
                print(f"{cp}: Consensus Mid = {consensus_mid:.4f}, Consensus Spread = {consensus_spread:.4f}")
            # Random market takers place orders on random currency pairs
            for cp, ob in self.order_books.items():
                order_type = random.choice(list(Side))
                taker = MarketTaker(order_type, size=random.uniform(1, 5))
                price, size = taker.place_order(ob)
                print(f"MarketTaker {order_type.value} on {cp}: Executed {size:.2f} at {price:.4f}")
