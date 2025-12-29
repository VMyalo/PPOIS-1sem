"""
Базовый класс для оборудования.

Этот модуль содержит базовую реализацию для различного
оборудования, доступного для аренды в системе.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any

from ..base_item import BaseItem, ItemStatus, ItemCondition
from .enums.equipment_type import EquipmentType
from .enums.power_source import PowerSource
from src.utils import constants as const


@dataclass
class BaseEquipment(BaseItem):
    """
    Базовый класс для всего оборудования.

    Этот класс предоставляет общую функциональность для различного
    оборудования: камер, дронов, спортивного инвентаря и т.д.

    Attributes:
        equipment_type: Тип оборудования
        brand: Бренд производителя
        model: Модель оборудования
        power_source: Источник питания
        battery_life_hours: Время работы от батареи в часах
        weight_kg: Вес в килограммах
        dimensions_cm: Размеры в сантиметрах (Д x Ш x В)
        requires_assembly: Требуется сборка
        assembly_instructions: Инструкции по сборке
        technical_specs: Технические характеристики
        compatible_accessories: Совместимые аксессуары
    """

    equipment_type: EquipmentType = EquipmentType.CAMERA
    brand: str = ""
    model: str = ""
    power_source: PowerSource = PowerSource.BATTERY
    battery_life_hours: Optional[float] = None
    weight_kg: Optional[float] = None
    dimensions_cm: Optional[str] = None  # "30x20x15"
    requires_assembly: bool = False
    assembly_instructions: Optional[str] = None
    technical_specs: Dict[str, Any] = field(default_factory=dict)
    compatible_accessories: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.category = const.CATEGORY_EQUIPMENT
        if not self.brand:
            raise ValueError("Бренд оборудования обязателен")
        if not self.model:
            raise ValueError("Модель оборудования обязательна")

    def validate(self) -> bool:
        """
        Валидирует состояние оборудования.

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

        if not self.brand or len(self.brand.strip()) == 0:
            errors.append("Бренд оборудования не может быть пустым")

        if not self.model or len(self.model.strip()) == 0:
            errors.append("Модель оборудования не может быть пустой")

        if self.battery_life_hours is not None and self.battery_life_hours <= 0:
            errors.append("Время работы от батареи должно быть положительным")

        if self.weight_kg is not None and self.weight_kg <= 0:
            errors.append("Вес оборудования должен быть положительным")

        if self.assembly_instructions and len(self.assembly_instructions) > const.MAXIMUM_TEXT_LENGTH:
            errors.append(f"Инструкции по сборке не могут превышать {const.MAXIMUM_TEXT_LENGTH} символов")

        return errors

    def requires_power_source(self) -> bool:
        """
        Проверяет требуется ли источнику питания оборудование.

        Returns:
            bool: True если требуется питание
        """
        return self.power_source != PowerSource.MANUAL

    def get_battery_status(self) -> Optional[str]:
        """
        Получает статус батареи.

        Returns:
            Optional[str]: Статус батареи или None если нет батареи
        """
        if self.power_source == PowerSource.BATTERY and self.battery_life_hours:
            return f"Время работы: {self.battery_life_hours} часов"
        return None

    def add_technical_spec(self, key: str, value: Any) -> None:
        """
        Добавляет техническую характеристику.

        Args:
            key: Название характеристики
            value: Значение характеристики
        """
        if key and key.strip():
            self.technical_specs[key.strip()] = value
            self.update_timestamp()

    def remove_technical_spec(self, key: str) -> None:
        """
        Удаляет техническую характеристику.

        Args:
            key: Название характеристики
        """
        if key in self.technical_specs:
            del self.technical_specs[key]
            self.update_timestamp()

    def add_compatible_accessory(self, accessory: str) -> None:
        """
        Добавляет совместимый аксессуар.

        Args:
            accessory: Название аксессуара
        """
        if accessory and accessory.strip():
            acc = accessory.strip()
            if acc not in self.compatible_accessories:
                self.compatible_accessories.append(acc)
                self.update_timestamp()

    def remove_compatible_accessory(self, accessory: str) -> None:
        """
        Удаляет совместимый аксессуар.

        Args:
            accessory: Название аксессуара
        """
        if accessory in self.compatible_accessories:
            self.compatible_accessories.remove(accessory)
            self.update_timestamp()

    def get_equipment_info(self) -> Dict[str, Any]:
        """
        Получает информацию об оборудовании.

        Returns:
            Dict[str, Any]: Информация об оборудовании
        """
        return {
            'equipment_id': self.entity_id,
            'type': self.equipment_type.value,
            'brand': self.brand,
            'model': self.model,
            'name': self.name,
            'power_source': self.power_source.value,
            'battery_life_hours': self.battery_life_hours,
            'weight_kg': self.weight_kg,
            'dimensions_cm': self.dimensions_cm,
            'requires_assembly': self.requires_assembly,
            'status': self.status.value,
            'condition': self.condition.value,
            'daily_rate': float(self.daily_rate)
        }

    def calculate_transport_cost(self, distance_km: float) -> Decimal:
        """
        Рассчитывает стоимость транспортировки.

        Args:
            distance_km: Расстояние в километрах

        Returns:
            Decimal: Стоимость транспортировки
        """
        if not self.weight_kg:
            return Decimal("0.00")

        # Простая формула: стоимость зависит от веса и расстояния
        base_rate = Decimal("0.50")  # базовая стоимость за кг/км
        return Decimal(str(distance_km)) * self.weight_kg * base_rate

    def requires_special_transport(self) -> bool:
        """
        Проверяет требуется ли специальный транспорт.

        Returns:
            bool: True если требуется специальный транспорт
        """
        return self.weight_kg and self.weight_kg > 20  # вес более 20 кг

    def get_maintenance_schedule(self) -> Dict[str, Any]:
        """
        Получает график обслуживания.

        Returns:
            Dict[str, Any]: График обслуживания
        """
        return {
            'last_maintenance': self.last_maintenance_date.isoformat() if self.last_maintenance_date else None,
            'next_maintenance_due': None,  # Можно рассчитать на основе использования
            'maintenance_interval_days': const.MAINTENANCE_CHECK_INTERVAL_DAYS,
            'requires_specialist': self.equipment_type in [EquipmentType.DRONE, EquipmentType.AUDIO_EQUIPMENT]
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует оборудование в словарь для сериализации.

        Returns:
            Dict[str, Any]: Словарь с данными оборудования
        """
        data = super().to_dict()
        data.update({
            'equipment_type': self.equipment_type.value,
            'brand': self.brand,
            'model': self.model,
            'power_source': self.power_source.value,
            'battery_life_hours': self.battery_life_hours,
            'weight_kg': self.weight_kg,
            'dimensions_cm': self.dimensions_cm,
            'requires_assembly': self.requires_assembly,
            'assembly_instructions': self.assembly_instructions,
            'technical_specs': self.technical_specs,
            'compatible_accessories': self.compatible_accessories
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseEquipment':
        """
        Создает оборудование из словаря.

        Args:
            data: Словарь с данными оборудования

        Returns:
            BaseEquipment: Новый экземпляр оборудования
        """
        # Преобразуем строковые значения обратно в соответствующие типы
        if 'equipment_type' in data:
            data['equipment_type'] = EquipmentType(data['equipment_type'])
        if 'power_source' in data:
            data['power_source'] = PowerSource(data['power_source'])

        # Вызываем родительский from_dict для корректной десериализации
        return super().from_dict(data)
