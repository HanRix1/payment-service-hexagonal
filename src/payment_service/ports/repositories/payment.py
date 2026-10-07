from typing import Protocol
from uuid import UUID

from src.payment_service.domain.entities.payment import Payment


class PaymentRepository(Protocol):
    async def add(self, payment: Payment) -> None:
        """Сохранить новый платёж."""   
        ...

    async def get_by_id(self, payment_id: UUID) -> Payment | None:
        """Найти платёж по id. Вернуть None, если не найден."""
        ...

    async def get_by_idempotency_key(self, key: str) -> Payment | None:
        """Найти платёж по idempotency key. Вернуть None, если не найден."""
        ...

    async def update(self, payment: Payment) -> None:
        """Обновить существующий платёж."""
        ...
