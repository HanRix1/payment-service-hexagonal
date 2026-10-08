from dataclasses import dataclass, field
from typing import Any

from src.payment_service.domain.entities.outbox_event import OutboxEvent
from src.payment_service.domain.entities.payment import Payment
from src.payment_service.domain.value_objects.money import Money
from src.payment_service.ports.uow.unit_of_work import UnitOfWork


@dataclass(frozen=True)
class CreatePaymentDTO:
    """Входные данные для создания платежа."""

    money: Money
    idempotency_key: str
    description: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    webhook_url: str | None = None


class CreatePaymentUseCase:
    """Создать платёж и Outbox-событие в одной транзакции."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, dto: CreatePaymentDTO) -> Payment:
        async with self._uow:
            # 1. Проверка идемпотентности
            existing = await self._uow.payments.get_by_idempotency_key(
                dto.idempotency_key
            )
            if existing is not None:
                return existing

            # 2. Создание Payment
            payment = Payment(
                money=dto.money,
                idempotency_key=dto.idempotency_key,
                description=dto.description,
                metadata=dto.metadata,
                webhook_url=dto.webhook_url,
            )

            # 3. Создание OutboxEvent
            event = OutboxEvent(
                aggregate_id=payment.id,
                event_type="payment.created",
                payload={
                    "payment_id": str(payment.id),
                    "amount": str(payment.money.amount),
                    "currency": payment.money.currency.value,
                },
            )

            # 4. Сохранение в одной транзакции
            await self._uow.payments.add(payment)
            await self._uow.outbox.add(event)
            await self._uow.commit()

            return payment