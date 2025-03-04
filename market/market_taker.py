import random

from market.orderbook import OrderBook
from price_construction.price_production import PriceProduction
from util.currency_pair import CurrencyPair


class MarketMaker:
    def __init__(self, currency_pair: CurrencyPair, price_production: PriceProduction, risk_factor=1):
        self.currency_pair = currency_pair
        self.price_production = price_production
        self.risk_factor = risk_factor
        self.inventory = 0  # Could be used for risk management adjustments

    def generate_bid_ask(self):
        consensus_mid, _ = self.price_production.calculate_consensus_price()
        # Adjust skew based on risk (this is a very simple example)
        skew = random.uniform(0.0001, 0.001) * self.risk_factor
        bid_price = consensus_mid - skew
        ask_price = consensus_mid + skew
        return bid_price, ask_price

    def place_orders(self, order_book: OrderBook):
        bid_price, ask_price = self.generate_bid_ask()
        order_book.update_bid([bid_price], [10])
        order_book.update_ask([ask_price], [10])
        self.price_production.update(order_book)