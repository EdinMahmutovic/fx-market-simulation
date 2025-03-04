from typing import Dict

import numpy as np

from market.orderbook import OrderBook


class VWAPPrice:
    def __init__(self, vwap_mid_price: int, vwap_spread: int):
        self.vwap_mid_price: int = vwap_mid_price
        self.vwap_spread: int = vwap_spread
        self.order_books: Dict[int, OrderBook] = dict()

    def update(self, order_book: OrderBook):
        book_id = order_book.get_id()
        if book_id not in self.order_books.keys():
            book_size = order_book.get_book_size()
            self.order_books[book_id] = OrderBook(book_id=book_id, book_size=book_size)

        self.order_books[book_id].update_ask(new_prices=order_book.get_ask_prices(),
                                             new_sizes=order_book.get_ask_sizes())
        self.order_books[book_id].update_bid(new_prices=order_book.get_bid_prices(),
                                             new_sizes=order_book.get_bid_sizes())

    def calculate_consensus_price(self):
        # Combine all bid and ask prices and sizes from all order books into lists first
        combined_bid_prices = []
        combined_bid_sizes = []
        combined_ask_prices = []
        combined_ask_sizes = []

        for order_book in self.order_books.values():
            combined_bid_prices.extend(order_book.get_bid_prices())
            combined_bid_sizes.extend(order_book.get_bid_sizes())
            combined_ask_prices.extend(order_book.get_ask_prices())
            combined_ask_sizes.extend(order_book.get_ask_sizes())

        # Convert combined lists into numpy arrays for better performance
        combined_bid_prices = np.array(combined_bid_prices)
        combined_bid_sizes = np.array(combined_bid_sizes)
        combined_ask_prices = np.array(combined_ask_prices)
        combined_ask_sizes = np.array(combined_ask_sizes)

        # Sort the bids (highest first) and asks (lowest first)
        bid_index_sorted = np.argsort(combined_bid_prices)[::-1]
        ask_index_sorted = np.argsort(combined_ask_prices)

        combined_bid_prices = combined_bid_prices[bid_index_sorted]
        combined_bid_sizes = combined_bid_sizes[bid_index_sorted]
        combined_ask_prices = combined_ask_prices[ask_index_sorted]
        combined_ask_sizes = combined_ask_sizes[ask_index_sorted]

        # Accumulate sizes
        accum_bid_sizes = np.cumsum(combined_bid_sizes)
        accum_ask_sizes = np.cumsum(combined_ask_sizes)

        # Calculate the VWAP for the bid prices and ask prices using vectorized logic
        bid_mask_mid = accum_bid_sizes <= self.vwap_mid_price
        ask_mask_mid = accum_ask_sizes <= self.vwap_mid_price

        # Calculate the VWAP for the bid prices and ask prices using vectorized logic
        bid_mask_spread = accum_bid_sizes <= self.vwap_spread
        ask_mask_spread = accum_ask_sizes <= self.vwap_spread

        # Ensure that the remaining size is only calculated if the mask is not empty
        bid_remaining_size_mid = 0
        bid_remaining_size_spread = 0
        ask_remaining_size_mid = 0
        ask_remaining_size_spread = 0

        if np.any(~bid_mask_mid):
            # If the accumulated size exceeds vwap_mid_price, calculate the remaining size for the last bid
            bid_remaining_size_mid = np.clip(self.vwap_mid_price - accum_bid_sizes[bid_mask_mid][-1], 0, None)

        if np.any(~bid_mask_spread):
            # If the accumulated size exceeds vwap_mid_price, calculate the remaining size for the last bid
            bid_remaining_size_spread = np.clip(self.vwap_spread - accum_bid_sizes[bid_mask_spread][-1], 0, None)

        if np.any(~ask_mask_mid):
            # If the accumulated size exceeds vwap_mid_price, calculate the remaining size for the last ask
            ask_remaining_size_mid = np.clip(self.vwap_mid_price - accum_ask_sizes[ask_mask_mid][-1], 0, None)

        if np.any(~ask_mask_spread):
            # If the accumulated size exceeds vwap_mid_price, calculate the remaining size for the last ask
            ask_remaining_size_spread = np.clip(self.vwap_spread - accum_ask_sizes[ask_mask_spread][-1], 0, None)

        # Calculate the weighted sum of prices and sizes for VWAP
        weighted_bid_price = np.sum(combined_bid_prices[bid_mask_mid] * combined_bid_sizes[bid_mask_mid])
        if np.any(~bid_mask_mid):
            weighted_bid_price += combined_bid_prices[bid_mask_mid][-1] * bid_remaining_size_mid

        weighted_ask_price = np.sum(combined_ask_prices[ask_mask_mid] * combined_ask_sizes[ask_mask_mid])
        if np.any(~ask_mask_mid):
            weighted_ask_price += combined_ask_prices[ask_mask_mid][-1] * ask_remaining_size_mid

        total_bid_size = np.sum(combined_bid_sizes[bid_mask_mid]) + bid_remaining_size_mid
        total_ask_size = np.sum(combined_ask_sizes[ask_mask_mid]) + ask_remaining_size_mid

        # Calculate the consensus mid price (VWAP)
        consensus_mid_price = (weighted_bid_price + weighted_ask_price) / (total_bid_size + total_ask_size) \
            if (total_bid_size + total_ask_size) > 0 else 0.0

        # Calculate the consensus spread: weighted ask price - weighted bid price
        weighted_bid_price_spread = np.sum(combined_bid_prices[bid_mask_spread] * combined_bid_sizes[bid_mask_spread])
        if np.any(~bid_mask_spread):
            weighted_bid_price_spread += combined_bid_prices[~bid_mask_spread][0] * bid_remaining_size_spread

        weighted_ask_price_spread = np.sum(combined_ask_prices[ask_mask_spread] * combined_ask_sizes[ask_mask_spread])
        if np.any(~ask_mask_spread):
            weighted_ask_price_spread += combined_ask_prices[~ask_mask_spread][0] * ask_remaining_size_spread

        total_bid_size_spread = np.sum(combined_bid_sizes[bid_mask_spread]) + bid_remaining_size_spread
        total_ask_size_spread = np.sum(combined_ask_sizes[ask_mask_spread]) + ask_remaining_size_spread

        weighted_bid_price_spread = weighted_bid_price_spread / total_bid_size_spread
        weighted_ask_price_spread = weighted_ask_price_spread / total_ask_size_spread

        consensus_spread = weighted_ask_price_spread - weighted_bid_price_spread

        return consensus_mid_price, consensus_spread
