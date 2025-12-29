"""
Класс менеджера системы аренды.

Этот модуль содержит реализацию менеджера - сотрудника
с правами управления другими сотрудниками и процессами.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any, Set

from .base_employee import BaseEmployee, Department, EmployeeStatus
from src.utils import constants as const


@dataclass
class Manager(BaseEmployee):
    """
    Класс представляющий менеджера системы аренды.

    Менеджер - это сотрудник с расширенными правами управления
    другими сотрудниками, процессами аренды и отчетностью.

    Attributes:
        subordinates: Множество ID подчиненных сотрудников
        managed_departments: Отделы которыми управляет менеджер
        budget_limit: Лимит бюджета для решений
        approval_limit: Лимит для одобрения расходов
        reports_generated: Количество созданных отчетов
        team_performance_rating: Рейтинг производительности команды
        monthly_goals: Месячные цели
        achieved_goals: Достигнутые цели
    """

    subordinates: Set[str] = field(default_factory=set)
    managed_departments: Set[str] = field(default_factory=set)
    budget_limit: Decimal = Decimal("10000.00")
    approval_limit: Decimal = Decimal("5000.00")
    reports_generated: int = 0
    team_performance_rating: float = 0.0
    monthly_goals: List[str] = field(default_factory=list)
    achieved_goals: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        # Автоматически устанавливаем должность как менеджер
        if 'manager' not in self.position.lower():
            self.position = f"{self.position} Manager"
        if self.budget_limit < 0:
            raise ValueError("Лимит бюджета не может быть отрицательным")
        if self.approval_limit < 0:
            raise ValueError("Лимит одобрения не может быть отрицательным")

    def validate(self) -> bool:
        """
        Валидирует данные менеджера.

        Returns:
            bool: True если валидация успешна
        """
        errors = self.get_validation_errors()
        return len(errors) == 0

    def get_validation_errors(self) -> List[str]:
        """
        Получает список ошибок валидации.

        Returns:
            List[str]: Список ошибок валидации
        """
        errors = super().get_validation_errors()

        if self.budget_limit < 0:
            errors.append("Лимит бюджета не может быть отрицательным")

        if self.approval_limit < 0:
            errors.append("Лимит одобрения не может быть отрицательным")

        if self.reports_generated < 0:
            errors.append("Количество отчетов не может быть отрицательным")

        if not (0.0 <= self.team_performance_rating <= 5.0):
            errors.append("Командный рейтинг должен быть от 0.0 до 5.0")

        return errors

    def add_subordinate(self, employee_id: str) -> None:
        """
        Добавляет подчиненного сотрудника.

        Args:
            employee_id: ID сотрудника
        """
        if employee_id and employee_id != self.employee_id:
            self.subordinates.add(employee_id)
            self.update_timestamp()

    def remove_subordinate(self, employee_id: str) -> None:
        """
        Удаляет подчиненного сотрудника.

        Args:
            employee_id: ID сотрудника
        """
        if employee_id in self.subordinates:
            self.subordinates.remove(employee_id)
            self.update_timestamp()

    def add_managed_department(self, department: str) -> None:
        """
        Добавляет управляемый отдел.

        Args:
            department: Название отдела
        """
        if department and department.strip():
            self.managed_departments.add(department.strip())
            self.update_timestamp()

    def remove_managed_department(self, department: str) -> None:
        """
        Удаляет управляемый отдел.

        Args:
            department: Название отдела
        """
        if department in self.managed_departments:
            self.managed_departments.remove(department)
            self.update_timestamp()

    def can_approve_expense(self, amount: Decimal) -> bool:
        """
        Проверяет может ли менеджер одобрить расход.

        Args:
            amount: Сумма расхода

        Returns:
            bool: True если может одобрить
        """
        return (self.status == EmployeeStatus.ACTIVE and
                amount <= self.approval_limit)

    def approve_expense(self, expense_id: str, amount: Decimal) -> bool:
        """
        Одобряет расход.

        Args:
            expense_id: ID расхода
            amount: Сумма расхода

        Returns:
            bool: True если одобрено
        """
        if self.can_approve_expense(amount):
            # Здесь должна быть логика одобрения расхода
            # Для простоты возвращаем True
            self.update_timestamp()
            return True
        return False

    def update_budget_limit(self, new_limit: Decimal) -> None:
        """
        Обновляет лимит бюджета.

        Args:
            new_limit: Новый лимит бюджета
        """
        if new_limit < 0:
            raise ValueError("Лимит бюджета не может быть отрицательным")

        self.budget_limit = new_limit
        self.update_timestamp()

    def update_approval_limit(self, new_limit: Decimal) -> None:
        """
        Обновляет лимит одобрения расходов.

        Args:
            new_limit: Новый лимит одобрения
        """
        if new_limit < 0:
            raise ValueError("Лимит одобрения не может быть отрицательным")

        self.approval_limit = new_limit
        self.update_timestamp()

    def increment_reports_generated(self) -> None:
        """Увеличивает счетчик созданных отчетов."""
        self.reports_generated += 1
        self.update_timestamp()

    def update_team_performance_rating(self, rating: float) -> None:
        """
        Обновляет командный рейтинг производительности.

        Args:
            rating: Новый рейтинг (0.0 - 5.0)
        """
        if not (0.0 <= rating <= 5.0):
            raise ValueError("Рейтинг должен быть от 0.0 до 5.0")

        self.team_performance_rating = rating
        self.update_timestamp()

    def add_monthly_goal(self, goal: str) -> None:
        """
        Добавляет месячную цель.

        Args:
            goal: Описание цели
        """
        if goal and goal.strip():
            self.monthly_goals.append(goal.strip())
            self.update_timestamp()

    def mark_goal_achieved(self, goal: str) -> None:
        """
        Отмечает цель как достигнутую.

        Args:
            goal: Описание достигнутой цели
        """
        if goal in self.monthly_goals:
            self.monthly_goals.remove(goal)
            self.achieved_goals.append(goal)
            self.update_timestamp()

    def get_management_summary(self) -> Dict[str, Any]:
        """
        Получает сводную информацию о менеджменте.

        Returns:
            Dict[str, Any]: Сводная информация
        """
        return {
            'manager_id': self.employee_id,
            'full_name': self.full_name,
            'department': self.department.value,
            'subordinates_count': len(self.subordinates),
            'managed_departments': list(self.managed_departments),
            'budget_limit': float(self.budget_limit),
            'approval_limit': float(self.approval_limit),
            'reports_generated': self.reports_generated,
            'team_performance_rating': round(self.team_performance_rating, 2),
            'monthly_goals_count': len(self.monthly_goals),
            'achieved_goals_count': len(self.achieved_goals)
        }

    def can_manage_employee(self, employee_id: str) -> bool:
        """
        Проверяет может ли менеджер управлять данным сотрудником.

        Args:
            employee_id: ID сотрудника

        Returns:
            bool: True если может управлять
        """
        return (self.status == EmployeeStatus.ACTIVE and
                employee_id in self.subordinates)

    def get_subordinates_list(self) -> List[str]:
        """
        Получает список ID подчиненных.

        Returns:
            List[str]: Список ID подчиненных
        """
        return list(self.subordinates)

    def get_managed_departments_list(self) -> List[str]:
        """
        Получает список управляемых отделов.

        Returns:
            List[str]: Список управляемых отделов
        """
        return list(self.managed_departments)

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует менеджера в словарь для сериализации.

        Returns:
            Dict[str, Any]: Словарь с данными менеджера
        """
        data = super().to_dict()
        data.update({
            'subordinates': list(self.subordinates),
            'managed_departments': list(self.managed_departments),
            'budget_limit': str(self.budget_limit),
            'approval_limit': str(self.approval_limit),
            'reports_generated': self.reports_generated,
            'team_performance_rating': self.team_performance_rating,
            'monthly_goals': self.monthly_goals,
            'achieved_goals': self.achieved_goals
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Manager':
        """
        Создает менеджера из словаря.

        Args:
            data: Словарь с данными менеджера

        Returns:
            Manager: Новый экземпляр менеджера
        """
        # Преобразуем строковые значения обратно в соответствующие типы
        if 'budget_limit' in data:
            data['budget_limit'] = Decimal(data['budget_limit'])
        if 'approval_limit' in data:
            data['approval_limit'] = Decimal(data['approval_limit'])
        if 'subordinates' in data:
            data['subordinates'] = set(data['subordinates'])
        if 'managed_departments' in data:
            data['managed_departments'] = set(data['managed_departments'])

        return cls(**data)
