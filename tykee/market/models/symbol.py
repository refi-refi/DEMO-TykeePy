from enum import Enum


class Symbol(Enum):
    """Enum for Symbol."""

    EURGBP = (1, 5)
    EURJPY = (2, 3)
    EURUSD = (3, 5)
    GBPJPY = (4, 3)
    GBPUSD = (5, 5)
    USDJPY = (6, 3)

    def __str__(self):
        """Return string representation of Symbol."""
        return self.name

    @classmethod
    def from_str(cls, name):
        """Construct Symbol from string."""
        return cls[name.upper()]

    @classmethod
    def default_symbol(cls):
        """Return default symbol."""
        return cls.EURGBP

    @property
    def index(self):
        """Return Symbol's index that matches Database index."""
        return self.value[0]

    @property
    def digits(self):
        """Return number of digits after decimal point for the current symbol prices."""
        return self.value[1]
