class CurrencyPair:
    """
    Represents a currency pair, e.g., EUR/USD.
    """
    def __init__(self, base, quote):
        self.base = base
        self.quote = quote

    def __str__(self):
        return f"{self.base}/{self.quote}"

    def __eq__(self, other):
        if isinstance(other, CurrencyPair):
            return self.base == other.base and self.quote == other.quote
        return False

    def __hash__(self):
        return hash((self.base, self.quote))

    def as_tuple(self):
        return self.base, self.quote
