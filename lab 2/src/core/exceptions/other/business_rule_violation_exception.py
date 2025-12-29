"""
Исключение, возникающее при нарушении бизнес-правил.
"""

from typing import Optional, Dict, Any

from ..base_exception import RentalSystemException


class BusinessRuleViolationException(RentalSystemException):
    """
    Исключение, возникающее при нарушении бизнес-правил.

    Выбрасывается когда операция нарушает бизнес-логику
    или правила работы системы.
    """

    def __init__(self, message: str = "Нарушение бизнес-правила",
                 rule_name: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        """
        Инициализирует исключение нарушения бизнес-правил.

        Args:
            message: Сообщение об ошибке
            rule_name: Название нарушенного правила
            context: Контекст нарушения правила
        """
        super().__init__(message, "BUSINESS_RULE_VIOLATION",
                         {'rule_name': rule_name, 'context': context})
        self.rule_name = rule_name
        self.context = context or {}
