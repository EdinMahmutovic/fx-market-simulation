from market.orderbook import OrderBook
from util.side import Side


class MarketTaker:
    def __init__(self, order_type: Side, size: float):
        self.order_type = order_type
        self.size = size

    def place_order(self, order_book: OrderBook):
        if self.order_type == Side.BUY:
            # For BUY, execute at the best ask
            best_ask = order_book.get_ask_prices()[0]
            return best_ask, self.size
        elif self.order_type == Side.SELL:
            # For SELL, execute at the best bid
            best_bid = order_book.get_bid_prices()[0]
            return best_bid, self.size
        return None, 0
