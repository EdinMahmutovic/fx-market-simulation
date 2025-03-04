from typing import Dict

import numpy as np

from market.orderbook import OrderBook
from util.currency_pair import CurrencyPair


class VWAPPrice:
    def __init__(self, vwap_mid_price: int, vwap_spread: int):
        self.vwap_mid_price = vwap_mid_price
        self.vwap_spread = vwap_spread
        # Dictionary keyed by CurrencyPair
        self.order_books: Dict[CurrencyPair, OrderBook] = {}

    def update(self, order_book: OrderBook):
        cp = order_book.get_currency_pair()
        self.order_books[cp] = order_book

    def calculate_consensus_price(self):
        # Combine all bid and ask prices and sizes from all order books.
        combined_bid_prices = []
        combined_bid_sizes = []
        combined_ask_prices = []
        combined_ask_sizes = []
        for ob in self.order_books.values():
            combined_bid_prices.extend(ob.get_bid_prices())
            combined_bid_sizes.extend(ob.get_bid_sizes())
            combined_ask_prices.extend(ob.get_ask_prices())
            combined_ask_sizes.extend(ob.get_ask_sizes())
        # Convert lists to numpy arrays
        combined_bid_prices = np.array(combined_bid_prices)
        combined_bid_sizes = np.array(combined_bid_sizes)
        combined_ask_prices = np.array(combined_ask_prices)
        combined_ask_sizes = np.array(combined_ask_sizes)

        # For simplicity here we compute simple weighted averages.
        bid_weighted_avg = np.sum(combined_bid_prices * combined_bid_sizes) / np.sum(combined_bid_sizes)
        ask_weighted_avg = np.sum(combined_ask_prices * combined_ask_sizes) / np.sum(combined_ask_sizes)

        consensus_mid_price = (bid_weighted_avg + ask_weighted_avg) / 2
        consensus_spread = ask_weighted_avg - bid_weighted_avg

        return consensus_mid_price, consensus_spread
