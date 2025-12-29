"""
Класс предметов одежды.

Этот модуль содержит реализацию предметов одежды для аренды.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from ..base_item import BaseItem, ItemStatus, ItemCondition
from .enums.clothing_size import ClothingSize
from .enums.clothing_type import ClothingType
from src.utils import constants as const


@dataclass
class ClothingItem(BaseItem):
    """
    Класс представляющий предметы одежды.

    Attributes:
        clothing_type: Тип одежды
        size: Размер
        color: Цвет
        material: Материал
        gender: Пол (male, female, unisex)
        season: Сезон
        waterproof: Водонепроницаемый
        care_instructions: Инструкции по уходу
        brand: Бренд
        style: Стиль
    """

    clothing_type: ClothingType = ClothingType.CASUAL
    size: ClothingSize = ClothingSize.M
    color: str = "black"
    material: str = "cotton"
    gender: str = "unisex"
    season: str = "all"
    waterproof: bool = False
    care_instructions: Optional[str] = None
    brand: str = ""
    style: str = "classic"

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.category = const.CATEGORY_CLOTHING
        self.name = f"{self.brand} {self.material} {self.clothing_type.value}"

    def is_suitable_for_weather(self, temperature_c: float, is_raining: bool) -> bool:
        """
        Проверяет подходит ли одежда для погоды.

        Args:
            temperature_c: Температура в градусах Цельсия
            is_raining: Идет ли дождь

        Returns:
            bool: True если подходит
        """
        if is_raining and not self.waterproof:
            return False

        if self.season == "winter" and temperature_c > 10:
            return False

        if self.season == "summer" and temperature_c < 15:
            return False

        return True

    def get_clothing_specs(self) -> Dict[str, Any]:
        """
        Получает спецификации одежды.

        Returns:
            Dict[str, Any]: Спецификации одежды
        """
        return {
            'clothing_type': self.clothing_type.value,
            'size': self.size.value,
            'color': self.color,
            'material': self.material,
            'gender': self.gender,
            'season': self.season,
            'waterproof': self.waterproof,
            'brand': self.brand,
            'style': self.style
        }
