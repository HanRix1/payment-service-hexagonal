class OutboxError(Exception):
    """Базовое исключение для ошибок Outbox."""


class InvalidOutboxTransition(OutboxError):
    """Попытка перевести событие в недопустимый статус."""
