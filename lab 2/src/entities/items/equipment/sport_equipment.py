"""
Класс спортивного оборудования для аренды.

Этот модуль содержит реализацию спортивного оборудования.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from .base_equipment import BaseEquipment, EquipmentType, PowerSource
from .enums.sport_type import SportType


@dataclass
class SportEquipment(BaseEquipment):
    """
    Класс представляющий спортивное оборудование.

    Attributes:
        sport_type: Тип спорта
        skill_level: Уровень сложности (beginner, intermediate, advanced)
        age_range: Возрастной диапазон
        max_weight_kg: Максимальный вес пользователя
        requires_supervision: Требуется ли supervision
        safety_rating: Рейтинг безопасности (1-5)
        maintenance_interval_hours: Интервал обслуживания в часах
    """

    sport_type: SportType = SportType.INDIVIDUAL_SPORTS
    skill_level: str = "beginner"
    age_range: str = "18+"
    max_weight_kg: Optional[float] = None
    requires_supervision: bool = False
    safety_rating: int = 3
    maintenance_interval_hours: int = 50

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.equipment_type = EquipmentType.SPORT_EQUIPMENT
        self.name = f"{self.brand} {self.model}"
        self.description = f"Спортивное оборудование для {self.sport_type.value}"

    def is_suitable_for_user(self, user_age: int, user_weight: float, user_skill: str) -> bool:
        """
        Проверяет подходит ли оборудование пользователю.

        Args:
            user_age: Возраст пользователя
            user_weight: Вес пользователя
            user_skill: Уровень навыков

        Returns:
            bool: True если подходит
        """
        # Проверка возраста
        if self.age_range == "18+":
            if user_age < 18:
                return False
        elif self.age_range == "16+":
            if user_age < 16:
                return False

        # Проверка веса
        if self.max_weight_kg and user_weight > self.max_weight_kg:
            return False

        # Проверка уровня навыков
        skill_levels = ["beginner", "intermediate", "advanced"]
        user_level_idx = skill_levels.index(user_skill) if user_skill in skill_levels else 0
        equip_level_idx = skill_levels.index(self.skill_level) if self.skill_level in skill_levels else 0

        return user_level_idx >= equip_level_idx

    def get_safety_warnings(self) -> List[str]:
        """
        Получает предупреждения безопасности.

        Returns:
            List[str]: Список предупреждений
        """
        warnings = []

        if self.requires_supervision:
            warnings.append("Требуется supervision")

        if self.safety_rating < 3:
            warnings.append("Низкий рейтинг безопасности")

        if self.skill_level == "advanced":
            warnings.append("Требуются продвинутые навыки")

        return warnings

    def calculate_wear_and_tear(self, usage_hours: int) -> float:
        """
        Рассчитывает износ оборудования.

        Args:
            usage_hours: Время использования в часах

        Returns:
            float: Процент износа
        """
        wear_rate = 100.0 / self.maintenance_interval_hours
        return min(100.0, usage_hours * wear_rate)
