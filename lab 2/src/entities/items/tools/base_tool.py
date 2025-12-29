"""
Базовый класс для инструментов.

Этот модуль содержит базовую реализацию для различных
инструментов, доступных для аренды в системе.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from ..base_item import BaseItem, ItemStatus, ItemCondition
from .enums.tool_type import ToolType
from .enums.material_type import MaterialType
from src.utils import constants as const


@dataclass
class BaseTool(BaseItem):
    """
    Базовый класс для всех инструментов.

    Этот класс предоставляет общую функциональность для различного
    инструмента: ручных инструментов, электроинструментов и т.д.

    Attributes:
        tool_type: Тип инструмента
        material: Материал изготовления
        weight_grams: Вес в граммах
        dimensions_mm: Размеры в миллиметрах
        handle_type: Тип рукоятки
        requires_power: Требуется ли питание
        power_rating_watts: Мощность в ваттах
        battery_type: Тип батареи
        safety_features: Функции безопасности
        usage_instructions: Инструкции по использованию
        maintenance_schedule: График обслуживания
    """

    tool_type: ToolType = ToolType.HAND_TOOL
    material: MaterialType = MaterialType.STEEL
    weight_grams: Optional[int] = None
    dimensions_mm: Optional[str] = None  # "200x50x30"
    handle_type: Optional[str] = None
    requires_power: bool = False
    power_rating_watts: Optional[int] = None
    battery_type: Optional[str] = None
    safety_features: List[str] = field(default_factory=list)
    usage_instructions: Optional[str] = None
    maintenance_schedule: Optional[str] = None

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.category = const.CATEGORY_TOOLS

    def validate(self) -> bool:
        """
        Валидирует состояние инструмента.

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

        if self.requires_power and not self.power_rating_watts:
            errors.append("Для электроинструментов требуется указать мощность")

        if self.weight_grams is not None and self.weight_grams <= 0:
            errors.append("Вес должен быть положительным")

        return errors

    def is_power_tool(self) -> bool:
        """
        Проверяет является ли инструмент электроинструментом.

        Returns:
            bool: True если является электроинструментом
        """
        return self.requires_power

    def get_power_requirements(self) -> Optional[Dict[str, Any]]:
        """
        Получает требования к питанию.

        Returns:
            Optional[Dict[str, Any]]: Требования к питанию или None
        """
        if not self.requires_power:
            return None

        return {
            'power_rating_watts': self.power_rating_watts,
            'battery_type': self.battery_type,
            'voltage_requirements': '220V' if not self.battery_type else 'Battery powered'
        }

    def add_safety_feature(self, feature: str) -> None:
        """
        Добавляет функцию безопасности.

        Args:
            feature: Функция безопасности
        """
        if feature and feature.strip():
            feat = feature.strip()
            if feat not in self.safety_features:
                self.safety_features.append(feat)
                self.update_timestamp()

    def requires_training(self) -> bool:
        """
        Проверяет требуется ли обучение для использования.

        Returns:
            bool: True если требуется обучение
        """
        return (self.is_power_tool() or
                self.tool_type in [ToolType.CUTTING_TOOL, ToolType.FASTENING_TOOL])

    def get_maintenance_info(self) -> Dict[str, Any]:
        """
        Получает информацию об обслуживании.

        Returns:
            Dict[str, Any]: Информация об обслуживании
        """
        return {
            'schedule': self.maintenance_schedule or 'После каждого использования',
            'requires_special_tools': self.is_power_tool(),
            'estimated_cost': '$50' if self.is_power_tool() else '$20',
            'last_maintenance': self.last_maintenance_date.isoformat() if self.last_maintenance_date else None
        }
