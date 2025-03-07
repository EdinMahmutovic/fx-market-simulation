import random
from typing import Dict, List

from price_construction.price_production import PriceProduction
from util.currency_pair import CurrencyPair


class PriceCrossing:
    """
    Encapsulates the pricing strategy for each target CurrencyPair.
    For each target pair, it decides if pricing is "direct" (use its own order book)
    or "cross" (price via two other pairs using a pivot).
    """
    def __init__(self, target_currency_pairs: List[CurrencyPair], price_production: PriceProduction):
        self.target_currency_pairs = target_currency_pairs
        self.price_production = price_production
        self.strategy_map: Dict[CurrencyPair, dict] = {}
        # Candidate pivots (common currencies)
        self.candidate_pivots = ["USD", "EUR", "GBP"]
        self.initialize_strategy()

    def initialize_strategy(self):
        for cp in self.target_currency_pairs:
            # 50% chance for direct pricing.
            if random.random() < 0.5:
                self.strategy_map[cp] = {"strategy": "direct"}
            else:
                # Choose a pivot that is not in the pair.
                possible_pivots = [p for p in self.candidate_pivots if p != cp.base and p != cp.quote]
                if possible_pivots:
                    pivot = random.choice(possible_pivots)
                    # For cross pricing of A/B using pivot X, require that A/X and X/B are available.
                    pair1 = CurrencyPair(cp.base, pivot)
                    pair2 = CurrencyPair(pivot, cp.quote)
                    if pair1 in self.target_currency_pairs and pair2 in self.target_currency_pairs:
                        self.strategy_map[cp] = {"strategy": "cross", "pivot": pivot}
                    else:
                        self.strategy_map[cp] = {"strategy": "direct"}
                else:
                    self.strategy_map[cp] = {"strategy": "direct"}

    def get_pricing_strategy(self, target: CurrencyPair) -> dict:
        return self.strategy_map.get(target, {"strategy": "direct"})

    def generate_mid_price(self, target: CurrencyPair) -> float:
        strat = self.get_pricing_strategy(target)
        if strat["strategy"] == "direct":
            mid, _ = self.price_production.calculate_pair_price(target)
            if mid is None:
                mid, _ = self.price_production.calculate_consensus_price()
            return mid
        else:
            # Cross pricing: for target A/B using pivot X, require A/X and X/B.
            pivot = strat["pivot"]
            pair1 = CurrencyPair(target.base, pivot)
            pair2 = CurrencyPair(pivot, target.quote)
            mid1, _ = self.price_production.calculate_pair_price(pair1)
            mid2, _ = self.price_production.calculate_pair_price(pair2)
            if mid1 is None or mid2 is None:
                mid, _ = self.price_production.calculate_pair_price(target)
                if mid is None:
                    mid, _ = self.price_production.calculate_consensus_price()
                return mid
            else:
                # For crossing, assume A/B = (A/X) * (X/B)
                return mid1 * mid2
