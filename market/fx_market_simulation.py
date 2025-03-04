import random

from market.market_maker import MarketMaker
from market.market_taker import MarketTaker
from market.orderbook import OrderBook
from price_construction.vwap_price import VWAPPrice
from util.side import Side


class FXMarketSimulation:
    def __init__(self, currency_pairs: list):
        self.currency_pairs = currency_pairs
        # Create an OrderBook for each currency pair
        self.order_books = {pair: OrderBook(book_id=i, book_size=10) for i, pair in enumerate(currency_pairs)}
        # Create a general price production mechanism (VWAPPrice in this case)
        self.price_production = VWAPPrice(vwap_mid_price=3, vwap_spread=3)
        # Create a MarketMaker for each currency pair
        self.market_makers = {
            pair: MarketMaker(pair, price_production=self.price_production, risk_factor=random.uniform(0.5, 1.5))
            for pair in currency_pairs
        }

    def run(self, steps: int = 10):
        for step in range(steps):
            print(f"\n--- Step {step} ---")
            # Market makers place orders on their respective order books
            for pair, mm in self.market_makers.items():
                ob = self.order_books[pair]
                mm.place_orders(ob)
                consensus_mid, consensus_spread = self.price_production.calculate_consensus_price()
                print(f"{pair}: Consensus Mid = {consensus_mid:.4f}, Consensus Spread = {consensus_spread:.4f}")
            # Random market takers place orders on a random pair's order book
            for pair, ob in self.order_books.items():
                order_type = random.choice(list(Side))
                taker = MarketTaker(order_type, size=random.uniform(1, 5))
                price, size = taker.place_order(ob)
                print(f"MarketTaker {order_type.value} on {pair}: Executed {size:.2f} at {price:.4f}")
