from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from src.payment_service.domain.value_objects.outbox_status import OutboxStatus
from src.payment_service.domain.exceptions.outbox import InvalidOutboxTransition


@dataclass
class OutboxEvent:
    aggregate_id: UUID
    event_type: str
    payload: dict[str, Any]
    id: UUID = field(default_factory=uuid4)
    status: OutboxStatus = OutboxStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    published_at: datetime | None = None

    def mark_published(self, published_at: datetime) -> None:
        self._transition_to(OutboxStatus.PUBLISHED, published_at)

    def mark_failed(self, published_at: datetime) -> None:
        self._transition_to(OutboxStatus.FAILED, published_at)

    def _transition_to(self, new_status: OutboxStatus, published_at: datetime) -> None:
        if self.status != OutboxStatus.PENDING:
            raise InvalidOutboxTransition(
                f"Cannot transition from {self.status} to {new_status}"
            )
        self.status = new_status
        self.published_at = published_at
