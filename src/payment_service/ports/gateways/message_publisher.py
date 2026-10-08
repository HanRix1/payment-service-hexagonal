from typing import Any, Protocol


class MessagePublisher(Protocol):
    """Контракт публикации сообщений в очередь."""

    async def publish(self, queue: str, payload: dict[str, Any]) -> None:
        """Опубликовать сообщение в указанную очередь.

        Бросает исключение, если публикация не удалась.
        """
        ...