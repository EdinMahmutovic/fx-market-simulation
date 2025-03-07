import numpy as np
from typing import Dict, Tuple

from market.orderbook import OrderBook
from price_construction.price_production import PriceProduction
from util.currency_pair import CurrencyPair


class VWAPPrice(PriceProduction):
    def __init__(self, vwap_mid_price: int, vwap_spread: int):
        self.vwap_mid_price = vwap_mid_price
        self.vwap_spread = vwap_spread
        # order_books is a dict keyed by CurrencyPair
        self.order_books: Dict[CurrencyPair, OrderBook] = {}

    def update(self, order_book: OrderBook):
        cp = order_book.get_currency_pair()
        self.order_books[cp] = order_book

    def calculate_consensus_price(self) -> Tuple[float, float]:
        # Global consensus: compute weighted averages across all order books.
        combined_bid_prices = []
        combined_bid_sizes = []
        combined_ask_prices = []
        combined_ask_sizes = []
        for ob in self.order_books.values():
            combined_bid_prices.extend(ob.get_bid_prices())
            combined_bid_sizes.extend(ob.get_bid_sizes())
            combined_ask_prices.extend(ob.get_ask_prices())
            combined_ask_sizes.extend(ob.get_ask_sizes())
        combined_bid_prices = np.array(combined_bid_prices)
        combined_bid_sizes = np.array(combined_bid_sizes)
        combined_ask_prices = np.array(combined_ask_prices)
        combined_ask_sizes = np.array(combined_ask_sizes)
        bid_weighted_avg = np.sum(combined_bid_prices * combined_bid_sizes) / np.sum(combined_bid_sizes)
        ask_weighted_avg = np.sum(combined_ask_prices * combined_ask_sizes) / np.sum(combined_ask_sizes)
        consensus_mid_price = (bid_weighted_avg + ask_weighted_avg) / 2
        consensus_spread = ask_weighted_avg - bid_weighted_avg
        return consensus_mid_price, consensus_spread

    def calculate_pair_price(self, currency_pair: CurrencyPair) -> Tuple[float, float]:
        ob = self.order_books.get(currency_pair)
        if ob is None:
            return None, None

        bid_prices = ob.get_bid_prices()
        bid_sizes = ob.get_bid_sizes()
        ask_prices = ob.get_ask_prices()
        ask_sizes = ob.get_ask_sizes()

        if np.sum(bid_sizes) == 0 or np.sum(ask_sizes) == 0:
            return None, None

        bid_weighted_avg = np.sum(bid_prices * bid_sizes) / np.sum(bid_sizes)
        ask_weighted_avg = np.sum(ask_prices * ask_sizes) / np.sum(ask_sizes)
        mid = (bid_weighted_avg + ask_weighted_avg) / 2
        spread = ask_weighted_avg - bid_weighted_avg

        return mid, spread
