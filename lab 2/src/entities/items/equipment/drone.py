"""
Класс дрона для аренды.

Этот модуль содержит реализацию дрона как предмета аренды.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from .base_equipment import BaseEquipment, EquipmentType, PowerSource
from .enums.drone_category import DroneCategory
from src.utils import constants as const


@dataclass
class Drone(BaseEquipment):
    """
    Класс представляющий дрон для аренды.

    Дрон - это специализированное оборудование для аэросъемки,
    доступное для аренды в системе.

    Attributes:
        drone_category: Категория дрона
        max_flight_time_minutes: Максимальное время полета в минутах
        max_altitude_meters: Максимальная высота полета в метрах
        max_speed_kmh: Максимальная скорость в км/ч
        camera_resolution: Разрешение камеры
        gps_enabled: GPS включен
        follow_me_mode: Режим следования
        return_home_feature: Функция возврата домой
        flight_controller: Тип контроллера полета
        propeller_count: Количество пропеллеров
        remote_controller_range_meters: Дальность управления в метрах
    """

    drone_category: DroneCategory = DroneCategory.STANDARD
    max_flight_time_minutes: int = 20
    max_altitude_meters: int = 120
    max_speed_kmh: int = 50
    camera_resolution: Optional[str] = None  # "4K", "1080p" и т.д.
    gps_enabled: bool = True
    follow_me_mode: bool = False
    return_home_feature: bool = True
    flight_controller: Optional[str] = None
    propeller_count: int = 4
    remote_controller_range_meters: int = 1000

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.equipment_type = EquipmentType.DRONE
        self.name = f"{self.brand} {self.model} Drone"
        self.description = f"Дрон категории {self.drone_category.value}"

        # Дроны обычно работают от батареи
        if self.power_source == PowerSource.BATTERY:
            self.battery_life_hours = self.max_flight_time_minutes / 60

        # Добавляем технические характеристики
        self._update_technical_specs()

    def _update_technical_specs(self) -> None:
        """Обновляет технические характеристики дрона."""
        self.technical_specs.update({
            'drone_category': self.drone_category.value,
            'max_flight_time_minutes': self.max_flight_time_minutes,
            'max_altitude_meters': self.max_altitude_meters,
            'max_speed_kmh': self.max_speed_kmh,
            'camera_resolution': self.camera_resolution,
            'gps_enabled': self.gps_enabled,
            'follow_me_mode': self.follow_me_mode,
            'return_home_feature': self.return_home_feature,
            'propeller_count': self.propeller_count,
            'remote_controller_range_meters': self.remote_controller_range_meters
        })

    def validate(self) -> bool:
        """
        Валидирует состояние дрона.

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

        if self.max_flight_time_minutes <= 0:
            errors.append("Время полета должно быть положительным")

        if self.max_altitude_meters <= 0:
            errors.append("Максимальная высота должна быть положительной")

        if self.max_speed_kmh <= 0:
            errors.append("Максимальная скорость должна быть положительной")

        if self.propeller_count < 3:
            errors.append("Количество пропеллеров должно быть не менее 3")

        if self.remote_controller_range_meters <= 0:
            errors.append("Дальность управления должна быть положительной")

        return errors

    def can_fly_in_weather(self, wind_speed_kmh: float, visibility_meters: float) -> bool:
        """
        Проверяет можно ли летать в данных погодных условиях.

        Args:
            wind_speed_kmh: Скорость ветра в км/ч
            visibility_meters: Видимость в метрах

        Returns:
            bool: True если можно летать
        """
        # Простые ограничения для безопасности
        max_wind = 30 if self.drone_category == DroneCategory.INDUSTRIAL else 20
        min_visibility = 500  # метров

        return wind_speed_kmh <= max_wind and visibility_meters >= min_visibility

    def calculate_flight_range(self) -> Dict[str, Any]:
        """
        Рассчитывает дальность полета дрона.

        Returns:
            Dict[str, Any]: Информация о дальности полета
        """
        # Простой расчет на основе скорости и времени полета
        max_distance_km = (self.max_speed_kmh * self.max_flight_time_minutes) / 60

        return {
            'max_distance_km': round(max_distance_km, 2),
            'controller_range_km': self.remote_controller_range_meters / 1000,
            'effective_range_km': min(max_distance_km, self.remote_controller_range_meters / 1000),
            'max_altitude_meters': self.max_altitude_meters
        }

    def requires_pilot_license(self) -> bool:
        """
        Проверяет требуется ли лицензия пилота для управления.

        Returns:
            bool: True если требуется лицензия
        """
        return (self.weight_kg and self.weight_kg > 0.25) or self.drone_category in [DroneCategory.PROFESSIONAL, DroneCategory.INDUSTRIAL]

    def get_safety_features(self) -> List[str]:
        """
        Получает список функций безопасности.

        Returns:
            List[str]: Список функций безопасности
        """
        features = []

        if self.gps_enabled:
            features.append("GPS")

        if self.return_home_feature:
            features.append("Возврат домой")

        if self.follow_me_mode:
            features.append("Режим следования")

        features.extend([
            "Автоматическая посадка при низком заряде",
            "Защита от столкновений",
            "Стабилизация полета"
        ])

        return features

    def estimate_battery_usage(self, flight_time_minutes: int) -> Dict[str, Any]:
        """
        Оценивает использование батареи.

        Args:
            flight_time_minutes: Время полета в минутах

        Returns:
            Dict[str, Any]: Информация об использовании батареи
        """
        if not self.battery_life_hours:
            return {'error': 'Информация о батарее недоступна'}

        total_battery_minutes = self.battery_life_hours * 60
        usage_percentage = (flight_time_minutes / total_battery_minutes) * 100

        return {
            'flight_time_minutes': flight_time_minutes,
            'battery_usage_percentage': min(100, round(usage_percentage, 1)),
            'remaining_time_minutes': max(0, total_battery_minutes - flight_time_minutes),
            'can_complete_flight': usage_percentage <= 100
        }

    def get_flight_restrictions(self) -> Dict[str, Any]:
        """
        Получает ограничения полета.

        Returns:
            Dict[str, Any]: Ограничения полета
        """
        return {
            'max_altitude_meters': self.max_altitude_meters,
            'max_flight_time_minutes': self.max_flight_time_minutes,
            'requires_line_of_sight': True,
            'no_fly_zones': ['Аэропорты', 'Военные объекты', 'Государственные учреждения'],
            'min_age_requirement': 18 if self.requires_pilot_license() else 14,
            'license_required': self.requires_pilot_license()
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует дрон в словарь для сериализации.

        Returns:
            Dict[str, Any]: Словарь с данными дрона
        """
        data = super().to_dict()
        data.update({
            'drone_category': self.drone_category.value,
            'max_flight_time_minutes': self.max_flight_time_minutes,
            'max_altitude_meters': self.max_altitude_meters,
            'max_speed_kmh': self.max_speed_kmh,
            'camera_resolution': self.camera_resolution,
            'gps_enabled': self.gps_enabled,
            'follow_me_mode': self.follow_me_mode,
            'return_home_feature': self.return_home_feature,
            'flight_controller': self.flight_controller,
            'propeller_count': self.propeller_count,
            'remote_controller_range_meters': self.remote_controller_range_meters
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Drone':
        """
        Создает дрон из словаря.

        Args:
            data: Словарь с данными дрона

        Returns:
            Drone: Новый экземпляр дрона
        """
        # Преобразуем строковые значения обратно в соответствующие типы
        if 'drone_category' in data:
            data['drone_category'] = DroneCategory(data['drone_category'])

        return cls(**data)
