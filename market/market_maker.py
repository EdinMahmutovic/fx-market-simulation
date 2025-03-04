import random

from market.orderbook import OrderBook
from util.currency_pair import CurrencyPair


class MarketMaker:
    def __init__(self, currency_pair: CurrencyPair, price_production, risk_factor=1):
        """
        currency_pair: CurrencyPair instance representing the market.
        price_production: General price production mechanism (e.g., VWAPPrice).
        risk_factor: Influences how aggressively prices are skewed.
        """
        self.currency_pair = currency_pair
        self.price_production = price_production
        self.risk_factor = risk_factor

    def generate_bid_ask(self):
        # Get consensus price from the price production mechanism
        consensus_mid, _ = self.price_production.calculate_consensus_price()
        # Introduce a small skew based on risk factor (this can be refined)
        skew = random.uniform(0.0001, 0.001) * self.risk_factor
        bid_price = consensus_mid - skew
        ask_price = consensus_mid + skew
        return bid_price, ask_price

    def place_orders(self, order_book: OrderBook):
        bid_price, ask_price = self.generate_bid_ask()
        # For simplicity, we use fixed sizes (e.g., 10M)
        order_book.update_bid([bid_price], [10])
        order_book.update_ask([ask_price], [10])
        # Update the price production with the new order book data
        self.price_production.update(order_book)