from abc import ABC, abstractmethod


class PriceProduction(ABC):
    @abstractmethod
    def update(self, order_book):
        pass

    @abstractmethod
    def calculate_consensus_price(self):
        """Return (consensus_mid_price, consensus_spread)"""
        pass
