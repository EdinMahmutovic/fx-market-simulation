import numpy as np

from util.currency_pair import CurrencyPair


class OrderBook:
    def __init__(self, currency_pair: CurrencyPair, book_size: int = 10):
        self.currency_pair = currency_pair
        self.book_size = book_size
        self.bid_prices = np.zeros(book_size)
        self.bid_sizes = np.zeros(book_size)
        self.ask_prices = np.zeros(book_size)
        self.ask_sizes = np.zeros(book_size)

    def update_bid(self, new_prices, new_sizes):
        self.bid_prices = np.array(new_prices)
        self.bid_sizes = np.array(new_sizes)

    def update_ask(self, new_prices, new_sizes):
        self.ask_prices = np.array(new_prices)
        self.ask_sizes = np.array(new_sizes)

    def get_bid_prices(self):
        return self.bid_prices

    def get_bid_sizes(self):
        return self.bid_sizes

    def get_ask_prices(self):
        return self.ask_prices

    def get_ask_sizes(self):
        return self.ask_sizes

    def get_currency_pair(self):
        return self.currency_pair