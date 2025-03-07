from abc import ABC, abstractmethod
from typing import Tuple

from market.orderbook import OrderBook
from util.currency_pair import CurrencyPair


class PriceProduction(ABC):
    @abstractmethod
    def update(self, order_book: OrderBook):
        pass

    @abstractmethod
    def calculate_consensus_price(self) -> Tuple[float, float]:
        """
        Calculate the consensus price from all order books.
        Returns (consensus_mid_price, consensus_spread)
        """
        pass

    @abstractmethod
    def calculate_pair_price(self, currency_pair: CurrencyPair) -> Tuple[float, float]:
        """
        Calculate the consensus (weighted) mid price and spread for the specified currency pair's order book.
        Returns (mid_price, spread)
        """
        pass
