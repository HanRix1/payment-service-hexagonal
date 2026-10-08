from typing import Any, Protocol


class WebhookSender(Protocol):
    """Контракт отправки webhook-уведомлений."""

    async def send(self, url: str, payload: dict[str, Any]) -> bool:
        """Отправить POST-запрос на url с payload.

        Возвращает True, если доставлено успешно (2xx).
        Возвращает False при любой ошибке: сетевой, таймауте, 4xx, 5xx.
        """
        ...