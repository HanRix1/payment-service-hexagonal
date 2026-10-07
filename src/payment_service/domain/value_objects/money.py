from dataclasses import dataclass
from decimal import Decimal

from src.payment_service.domain.value_objects.currency import Currency


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: Currency

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("amount must be positive")
        if self.amount.as_tuple().exponent < -2:
            raise ValueError("amount must have at most 2 decimal places")
