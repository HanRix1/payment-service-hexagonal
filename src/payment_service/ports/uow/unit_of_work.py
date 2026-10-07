from typing import Protocol

from src.payment_service.ports.repositories.outbox import OutboxRepository
from src.payment_service.ports.repositories.payment import PaymentRepository


class UnitOfWork(Protocol):
    payments: PaymentRepository
    outbox: OutboxRepository

    async def __aenter__(self) -> "UnitOfWork":
        ...

    async def __aexit__(
        self, 
        exc_type: type[BaseException] | None, 
        exc: BaseException | None, 
        tb: object | None
    ) -> None:
        ...

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...