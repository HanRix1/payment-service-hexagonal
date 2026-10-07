from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from src.payment_service.domain.exceptions.payment import InvalidStatusTransition
from src.payment_service.domain.value_objects.money import Money
from src.payment_service.domain.value_objects.payment_status import PaymentStatus


@dataclass
class Payment:
    money: Money
    idempotency_key: str
    id: UUID = field(default_factory=uuid4)
    description: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    webhook_url: str | None = None
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    processed_at: datetime | None = None

    def mark_succeeded(self, processed_at: datetime) -> None:
        self._transition_to(PaymentStatus.SUCCEEDED, processed_at)

    def mark_failed(self, processed_at: datetime) -> None:
        self._transition_to(PaymentStatus.FAILED, processed_at)

    def _transition_to(self, new_status: PaymentStatus, processed_at: datetime) -> None:
        if self.status != PaymentStatus.PENDING:
            raise InvalidStatusTransition(
                f"Cannot transition from {self.status} to {new_status}"
            )
        self.status = new_status
        self.processed_at = processed_at