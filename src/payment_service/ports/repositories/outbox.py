from typing import Protocol, Sequence
from uuid import UUID

from src.payment_service.domain.entities.outbox_event import OutboxEvent


class OutboxRepository(Protocol):
    async def add(self, event: OutboxEvent) -> None:
        """Сохранить новое событие."""
        ...

    async def get_pending(self, limit: int) -> Sequence[OutboxEvent]:
        """Получить неопубликованные события (статус pending), не более limit штук."""
        ...

    async def update(self, event: OutboxEvent) -> None:
        """Обновить существующее событие."""
        ...