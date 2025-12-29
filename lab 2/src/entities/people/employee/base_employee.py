"""
Базовый класс для сотрудников системы аренды.

Этот модуль содержит базовую реализацию для всех типов сотрудников:
обычных сотрудников, менеджеров и администраторов.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any

from ..base_person import BasePerson
from .enums.employee_status import EmployeeStatus
from .enums.department import Department
from src.utils import constants as const


@dataclass
class BaseEmployee(BasePerson):
    """
    Базовый класс для всех сотрудников системы.

    Этот класс предоставляет общую функциональность для всех типов сотрудников
    системы аренды предметов.

    Attributes:
        employee_id: Внутренний ID сотрудника
        department: Отдел сотрудника
        position: Должность
        salary: Зарплата
        hire_date: Дата приема на работу
        status: Статус сотрудника
        manager_id: ID менеджера
        performance_rating: Рейтинг производительности
        completed_tasks: Количество выполненных задач
        location_id: ID места работы
        work_schedule: График работы
        emergency_contact: Контакт для экстренных случаев
        certifications: Сертификаты и квалификации
    """

    employee_id: str = ""
    department: Department = Department.ADMINISTRATION
    position: str = ""
    salary: Decimal = Decimal("0.00")
    hire_date: Optional[datetime] = None
    status: EmployeeStatus = EmployeeStatus.ACTIVE
    manager_id: Optional[str] = None
    performance_rating: float = 0.0
    completed_tasks: int = 0
    location_id: Optional[str] = None
    work_schedule: Optional[str] = None
    emergency_contact: Optional[str] = None
    certifications: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        if not self.employee_id:
            raise ValueError("ID сотрудника обязателен")
        if not self.position:
            raise ValueError("Должность обязательна")
        if self.salary < 0:
            raise ValueError("Зарплата не может быть отрицательной")

    @property
    def years_of_service(self) -> float:
        """
        Стаж работы в годах.

        Returns:
            float: Стаж работы
        """
        if not self.hire_date:
            return 0.0
        return (datetime.now() - self.hire_date).days / 365.25

    @property
    def is_manager(self) -> bool:
        """
        Проверяет является ли сотрудник менеджером.

        Returns:
            bool: True если является менеджером
        """
        return self.position.lower() in ['manager', 'менеджер', 'директор']

    def validate(self) -> bool:
        """
        Валидирует данные сотрудника.

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

        if not self.employee_id or len(self.employee_id.strip()) == 0:
            errors.append("ID сотрудника не может быть пустым")

        if not self.position or len(self.position.strip()) == 0:
            errors.append("Должность не может быть пустой")

        if self.salary < 0:
            errors.append("Зарплата не может быть отрицательной")

        if self.hire_date and self.hire_date > datetime.now():
            errors.append("Дата приема на работу не может быть в будущем")

        if not (0.0 <= self.performance_rating <= 5.0):
            errors.append("Рейтинг производительности должен быть от 0.0 до 5.0")

        if self.completed_tasks < 0:
            errors.append("Количество выполненных задач не может быть отрицательным")

        return errors

    def update_performance_rating(self, rating: float) -> None:
        """
        Обновляет рейтинг производительности.

        Args:
            rating: Новый рейтинг (0.0 - 5.0)
        """
        if not (0.0 <= rating <= 5.0):
            raise ValueError("Рейтинг должен быть от 0.0 до 5.0")

        self.performance_rating = rating
        self.update_timestamp()

    def increment_completed_tasks(self) -> None:
        """Увеличивает счетчик выполненных задач."""
        self.completed_tasks += 1
        self.update_timestamp()

    def update_salary(self, new_salary: Decimal) -> None:
        """
        Обновляет зарплату сотрудника.

        Args:
            new_salary: Новая зарплата
        """
        if new_salary < 0:
            raise ValueError("Зарплата не может быть отрицательной")

        self.salary = new_salary
        self.update_timestamp()

    def change_department(self, new_department: Department) -> None:
        """
        Изменяет отдел сотрудника.

        Args:
            new_department: Новый отдел
        """
        self.department = new_department
        self.update_timestamp()

    def change_position(self, new_position: str) -> None:
        """
        Изменяет должность сотрудника.

        Args:
            new_position: Новая должность
        """
        if not new_position or len(new_position.strip()) == 0:
            raise ValueError("Должность не может быть пустой")

        self.position = new_position.strip()
        self.update_timestamp()

    def set_manager(self, manager_id: str) -> None:
        """
        Устанавливает менеджера для сотрудника.

        Args:
            manager_id: ID менеджера
        """
        self.manager_id = manager_id
        self.update_timestamp()

    def update_work_schedule(self, schedule: str) -> None:
        """
        Обновляет график работы.

        Args:
            schedule: Новый график работы
        """
        self.work_schedule = schedule
        self.update_timestamp()

    def add_certification(self, certification: str) -> None:
        """
        Добавляет сертификат/квалификацию.

        Args:
            certification: Название сертификата
        """
        if certification and certification.strip():
            cert = certification.strip()
            if cert not in self.certifications:
                self.certifications.append(cert)
                self.update_timestamp()

    def remove_certification(self, certification: str) -> None:
        """
        Удаляет сертификат/квалификацию.

        Args:
            certification: Название сертификата
        """
        if certification in self.certifications:
            self.certifications.remove(certification)
            self.update_timestamp()

    def update_emergency_contact(self, contact: str) -> None:
        """
        Обновляет контакт для экстренных случаев.

        Args:
            contact: Контактная информация
        """
        self.emergency_contact = contact
        self.update_timestamp()

    def terminate_employment(self) -> None:
        """Увольняет сотрудника."""
        self.status = EmployeeStatus.TERMINATED
        self.is_active = False
        self.update_timestamp()

    def put_on_leave(self) -> None:
        """Отправляет сотрудника в отпуск."""
        self.status = EmployeeStatus.ON_LEAVE
        self.update_timestamp()

    def reactivate_employee(self) -> None:
        """Возвращает сотрудника к работе."""
        self.status = EmployeeStatus.ACTIVE
        self.is_active = True
        self.update_timestamp()

    def can_manage_employees(self) -> bool:
        """
        Проверяет может ли сотрудник управлять другими сотрудниками.

        Returns:
            bool: True если может управлять
        """
        return self.is_manager and self.status == EmployeeStatus.ACTIVE

    def get_employee_summary(self) -> Dict[str, Any]:
        """
        Получает сводную информацию о сотруднике.

        Returns:
            Dict[str, Any]: Сводная информация
        """
        return {
            'employee_id': self.employee_id,
            'full_name': self.full_name,
            'department': self.department.value,
            'position': self.position,
            'status': self.status.value,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'years_of_service': round(self.years_of_service, 1),
            'performance_rating': round(self.performance_rating, 2),
            'completed_tasks': self.completed_tasks,
            'is_manager': self.is_manager
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует сотрудника в словарь для сериализации.

        Returns:
            Dict[str, Any]: Словарь с данными сотрудника
        """
        data = super().to_dict()
        data.update({
            'employee_id': self.employee_id,
            'department': self.department.value,
            'position': self.position,
            'salary': str(self.salary),
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'status': self.status.value,
            'manager_id': self.manager_id,
            'performance_rating': self.performance_rating,
            'completed_tasks': self.completed_tasks,
            'location_id': self.location_id,
            'work_schedule': self.work_schedule,
            'emergency_contact': self.emergency_contact,
            'certifications': self.certifications
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseEmployee':
        """
        Создает сотрудника из словаря.

        Args:
            data: Словарь с данными сотрудника

        Returns:
            BaseEmployee: Новый экземпляр сотрудника
        """
        # Преобразуем строковые значения обратно в соответствующие типы
        if 'salary' in data:
            data['salary'] = Decimal(data['salary'])
        if 'hire_date' in data and data['hire_date']:
            data['hire_date'] = datetime.fromisoformat(data['hire_date'])
        if 'department' in data:
            data['department'] = Department(data['department'])
        if 'status' in data:
            data['status'] = EmployeeStatus(data['status'])

        return cls(**data)
