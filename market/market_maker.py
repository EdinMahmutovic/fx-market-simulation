import random
from typing import Dict, List

from market.orderbook import OrderBook
from price_construction.price_crossing import PriceCrossing
from util.currency_pair import CurrencyPair


class MarketMaker:
    def __init__(self, target_currency_pairs: List[CurrencyPair],
                 price_crossing: PriceCrossing,
                 risk_factor: float = 1.0):
        """
        target_currency_pairs: List of all currency pairs to be priced.
        price_crossing: Instance of PriceCrossing that encapsulates pricing strategies.
        risk_factor: Influences how aggressively prices are skewed.
        """
        self.target_currency_pairs = target_currency_pairs
        self.price_crossing = price_crossing
        self.risk_factor = risk_factor

    def generate_bid_ask(self, target: CurrencyPair) -> (float, float):
        mid = self.price_crossing.generate_mid_price(target)
        # Apply a small random skew scaled by risk_factor.
        skew = random.uniform(0.0001, 0.001) * self.risk_factor
        bid_price = mid - skew
        ask_price = mid + skew
        return bid_price, ask_price

    def place_orders(self, order_books: Dict[CurrencyPair, OrderBook]):
        for cp in self.target_currency_pairs:
            ob = order_books.get(cp)
            if ob is None:
                continue
            bid_price, ask_price = self.generate_bid_ask(cp)
            # For simplicity, fixed sizes.
            ob.update_bid([bid_price], [10])
            ob.update_ask([ask_price], [10])
            # Update the price production mechanism.
            self.price_crossing.price_production.update(ob)
