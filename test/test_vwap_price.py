import unittest

import numpy as np

from market.orderbook import OrderBook
from price_construction.vwap_price import VWAPPrice


class TestVwapPrice(unittest.TestCase):

    def test_price_compute_1_orderbook(self):
        vwap_mid_price_size = 3
        vwap_spread_size = 3
        vwap_price_constructor = VWAPPrice(vwap_mid_price=vwap_mid_price_size, vwap_spread=vwap_spread_size)

        orderbook = OrderBook(book_id=1, book_size=10)

        bid_prices = [1.0905, 1.0900, 1.0895]
        bid_sizes = np.array([1, 1, 5])

        ask_prices = [1.1005, 1.1010, 1.1015]
        ask_sizes = np.array([1, 1, 5])

        orderbook.update_bid(new_prices=bid_prices, new_sizes=bid_sizes)
        orderbook.update_ask(new_prices=ask_prices, new_sizes=ask_sizes)

        vwap_price_constructor.update(order_book=orderbook)
        actual_mid_price, actual_spread = vwap_price_constructor.calculate_consensus_price()

        expected_bid_price = np.sum(bid_prices * np.array([1, 1, 1])) / vwap_mid_price_size
        expected_ask_price = np.sum(ask_prices * np.array([1, 1, 1])) / vwap_mid_price_size
        expected_mid_price = (expected_bid_price + expected_ask_price) / 2

        expected_bid_price_spread = np.sum(bid_prices * np.array([1, 1, 1])) / vwap_spread_size
        expected_ask_price_spread = np.sum(ask_prices * np.array([1, 1, 1])) / vwap_spread_size
        expected_spread = (expected_ask_price_spread - expected_bid_price_spread)

        self.assertEqual(np.round(expected_spread, 5), np.round(actual_spread, 5))
        self.assertEqual(np.round(expected_mid_price, 5), np.round(actual_mid_price, 5))

    def test_price_compute_1_orderbook_diff_vwap_sizes_1(self):
        vwap_mid_price_size = 3
        vwap_spread_size = 5
        vwap_price_constructor = VWAPPrice(vwap_mid_price=vwap_mid_price_size, vwap_spread=vwap_spread_size)

        orderbook = OrderBook(book_id=1, book_size=10)

        bid_prices = [1.0905, 1.0900, 1.0895]
        bid_sizes = np.array([1, 1, 5])

        ask_prices = [1.1005, 1.1010, 1.1015]
        ask_sizes = np.array([1, 1, 5])

        orderbook.update_bid(new_prices=bid_prices, new_sizes=bid_sizes)
        orderbook.update_ask(new_prices=ask_prices, new_sizes=ask_sizes)

        vwap_price_constructor.update(order_book=orderbook)
        actual_mid_price, actual_spread = vwap_price_constructor.calculate_consensus_price()

        expected_bid_price = np.sum(bid_prices * np.array([1, 1, 1])) / vwap_mid_price_size
        expected_ask_price = np.sum(ask_prices * np.array([1, 1, 1])) / vwap_mid_price_size
        expected_mid_price = (expected_bid_price + expected_ask_price) / 2

        expected_bid_price_spread = np.sum(bid_prices * np.array([1, 1, 3])) / vwap_spread_size
        expected_ask_price_spread = np.sum(ask_prices * np.array([1, 1, 3])) / vwap_spread_size
        expected_spread = (expected_ask_price_spread - expected_bid_price_spread)

        self.assertEqual(np.round(expected_spread, 5), np.round(actual_spread, 5))
        self.assertEqual(np.round(expected_mid_price, 5), np.round(actual_mid_price, 5))

    def test_price_compute_1_orderbook_diff_vwap_sizes_2(self):
        vwap_mid_price_size = 5
        vwap_spread_size = 3
        vwap_price_constructor = VWAPPrice(vwap_mid_price=vwap_mid_price_size, vwap_spread=vwap_spread_size)

        orderbook = OrderBook(book_id=1, book_size=10)

        bid_prices = [1.0905, 1.0900, 1.0895]
        bid_sizes = np.array([1, 1, 5])

        ask_prices = [1.1005, 1.1010, 1.1015]
        ask_sizes = np.array([1, 1, 5])

        orderbook.update_bid(new_prices=bid_prices, new_sizes=bid_sizes)
        orderbook.update_ask(new_prices=ask_prices, new_sizes=ask_sizes)

        vwap_price_constructor.update(order_book=orderbook)
        actual_mid_price, actual_spread = vwap_price_constructor.calculate_consensus_price()

        expected_bid_price = np.sum(bid_prices * np.array([1, 1, 3])) / vwap_mid_price_size
        expected_ask_price = np.sum(ask_prices * np.array([1, 1, 3])) / vwap_mid_price_size
        expected_mid_price = (expected_bid_price + expected_ask_price) / 2

        expected_bid_price_spread = np.sum(bid_prices * np.array([1, 1, 1])) / vwap_spread_size
        expected_ask_price_spread = np.sum(ask_prices * np.array([1, 1, 1])) / vwap_spread_size
        expected_spread = (expected_ask_price_spread - expected_bid_price_spread)

        self.assertEqual(np.round(expected_spread, 5), np.round(actual_spread, 5))
        self.assertEqual(np.round(expected_mid_price, 5), np.round(actual_mid_price, 5))

    def test_price_compute_multiple_orderbooks(self):
        vwap_mid_price_size = 3
        vwap_spread_size = 3
        vwap_price_constructor = VWAPPrice(vwap_mid_price=vwap_mid_price_size, vwap_spread=vwap_spread_size)

        orderbook_1 = OrderBook(book_id=1, book_size=10)
        orderbook_2 = OrderBook(book_id=2, book_size=10)

        bid_prices_1 = np.array([1.0905, 1.0900, 1.0895])
        bid_sizes_1 = np.array([1, 1, 5])

        ask_prices_1 = np.array([1.1005, 1.1010, 1.1015])
        ask_sizes_1 = np.array([1, 1, 5])

        bid_prices_2 = np.array([1.0925, 1.0900, 1.0890])
        bid_sizes_2 = np.array([2, 1, 1])

        ask_prices_2 = np.array([1.1002, 1.1005, 1.1010])
        ask_sizes_2 = np.array([1, 2, 1])

        bid_prices = np.array([1.0925, 1.0905, 1.900, 1.0895, 1.0890])
        bid_sizes = np.array([2, 1, 2, 5, 1])

        ask_prices = np.array([1.1002, 1.1005, 1.1010, 1.1015])
        ask_sizes = np.array([1, 3, 2, 5])

        orderbook_1.update_bid(new_prices=bid_prices_1, new_sizes=bid_sizes_1)
        orderbook_1.update_ask(new_prices=ask_prices_1, new_sizes=ask_sizes_1)
        orderbook_2.update_bid(new_prices=bid_prices_2, new_sizes=bid_sizes_2)
        orderbook_2.update_ask(new_prices=ask_prices_2, new_sizes=ask_sizes_2)

        vwap_price_constructor.update(order_book=orderbook_1)
        vwap_price_constructor.update(order_book=orderbook_2)

        actual_mid_price, actual_spread = vwap_price_constructor.calculate_consensus_price()

        expected_bid_price = np.sum(bid_prices[:2] * np.array([2, 1])) / vwap_mid_price_size
        expected_ask_price = np.sum(ask_prices[:2] * np.array([1, 2])) / vwap_mid_price_size
        expected_mid_price = (expected_bid_price + expected_ask_price) / 2

        expected_bid_price_spread = np.sum(bid_prices[:2] * np.array([2, 1])) / vwap_spread_size
        expected_ask_price_spread = np.sum(ask_prices[:2] * np.array([1, 2])) / vwap_spread_size
        expected_spread = (expected_ask_price_spread - expected_bid_price_spread)

        self.assertEqual(np.round(expected_spread, 5), np.round(actual_spread, 5))
        self.assertEqual(np.round(expected_mid_price, 5), np.round(actual_mid_price, 5))
