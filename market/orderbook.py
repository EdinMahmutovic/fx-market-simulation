import numpy as np


class OrderBook:
    def __init__(self, book_id: int, book_size: int = 10):
        self.__book_id: int = book_id
        self.__book_size: int = book_size

        self.__bid_prices: np.array = np.zeros(book_size)
        self.__bid_sizes: np.array = np.zeros(book_size)

        self.__ask_prices: np.array = np.zeros(book_size)
        self.__ask_sizes: np.array = np.zeros(book_size)

    def get_id(self):
        return self.__book_id

    def get_book_size(self):
        return self.__book_size

    def update_bid(self, new_prices: np.array, new_sizes: np.array):
        self.__bid_prices = new_prices
        self.__bid_sizes = new_sizes

    def update_ask(self, new_prices: np.array, new_sizes: np.array):
        self.__ask_prices = new_prices
        self.__ask_sizes = new_sizes

    def get_bid_prices(self):
        return self.__bid_prices

    def get_bid_sizes(self):
        return self.__bid_sizes

    def get_ask_prices(self):
        return self.__ask_prices

    def get_ask_sizes(self):
        return self.__ask_sizes
