class PaymentError(Exception):
    """Базовове исключение для ошибок платежа"""


class InvalidStatusTransition(PaymentError):
    """Попытка перевсти платеж в недопустимый статус"""

