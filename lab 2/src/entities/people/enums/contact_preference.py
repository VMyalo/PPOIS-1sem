"""
Перечисление для предпочтений контактов.
"""

from enum import Enum


class ContactPreference(Enum):
    """
    Предпочтения по контактам.

    Определяет предпочтительные способы связи с пользователем.
    """

    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    PHONE = "phone"
