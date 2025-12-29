"""
Класс камеры для аренды.

Этот модуль содержит реализацию камеры как предмета аренды.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from .base_equipment import BaseEquipment, EquipmentType, PowerSource
from .enums.camera_type import CameraType
from .enums.sensor_size import SensorSize
from src.utils import constants as const


@dataclass
class Camera(BaseEquipment):
    """
    Класс представляющий камеру для аренды.

    Камера - это специализированное оборудование для фото и видеосъемки,
    доступное для аренды в системе.

    Attributes:
        camera_type: Тип камеры
        sensor_size: Размер сенсора
        megapixels: Разрешение в мегапикселях
        max_iso: Максимальная чувствительность ISO
        has_video: Поддержка видео
        max_video_resolution: Максимальное разрешение видео
        lens_mount: Байонет объектива
        included_lens: Комплектный объектив
        memory_card_type: Тип карты памяти
        battery_type: Тип батареи
        tripod_mount: Крепление для штатива
    """

    camera_type: CameraType = CameraType.DSLR
    sensor_size: SensorSize = SensorSize.APS_C
    megapixels: float = 24.0
    max_iso: int = 25600
    has_video: bool = True
    max_video_resolution: Optional[str] = None  # "4K", "1080p" и т.д.
    lens_mount: Optional[str] = None
    included_lens: Optional[str] = None
    memory_card_type: Optional[str] = None  # "SD", "CF", "XQD" и т.д.
    battery_type: Optional[str] = None
    tripod_mount: str = "standard"  # 1/4 дюйма

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.equipment_type = EquipmentType.CAMERA
        self.name = f"{self.brand} {self.model}"
        self.description = f"Камера {self.camera_type.value} с сенсором {self.sensor_size.value}"

        # Добавляем технические характеристики
        self._update_technical_specs()

    def _update_technical_specs(self) -> None:
        """Обновляет технические характеристики камеры."""
        self.technical_specs.update({
            'camera_type': self.camera_type.value,
            'sensor_size': self.sensor_size.value,
            'megapixels': self.megapixels,
            'max_iso': self.max_iso,
            'has_video': self.has_video,
            'max_video_resolution': self.max_video_resolution,
            'lens_mount': self.lens_mount,
            'memory_card_type': self.memory_card_type,
            'battery_type': self.battery_type
        })

    def validate(self) -> bool:
        """
        Валидирует состояние камеры.

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

        if self.megapixels <= 0:
            errors.append("Разрешение должно быть положительным")

        if self.max_iso <= 0:
            errors.append("Максимальное ISO должно быть положительным")

        return errors

    def supports_4k_video(self) -> bool:
        """
        Проверяет поддерживает ли камера 4K видео.

        Returns:
            bool: True если поддерживает 4K
        """
        return (self.has_video and
                self.max_video_resolution and
                '4k' in self.max_video_resolution.lower())

    def get_max_video_resolution_info(self) -> Optional[str]:
        """
        Получает информацию о максимальном разрешении видео.

        Returns:
            Optional[str]: Информация о разрешении видео
        """
        if not self.has_video:
            return None
        return self.max_video_resolution or "1080p"

    def requires_lens(self) -> bool:
        """
        Проверяет требуется ли объектив для камеры.

        Returns:
            bool: True если требуется объектив
        """
        return not self.included_lens

    def is_professional_grade(self) -> bool:
        """
        Проверяет является ли камера профессионального уровня.

        Returns:
            bool: True если профессиональная
        """
        return (self.camera_type in [CameraType.DSLR, CameraType.CINEMA] and
                self.sensor_size == SensorSize.FULL_FRAME and
                self.megapixels >= 24)

    def calculate_video_recording_time(self) -> Optional[int]:
        """
        Рассчитывает время записи видео в минутах.

        Returns:
            Optional[int]: Время записи в минутах или None
        """
        if not self.has_video or not self.battery_life_hours:
            return None

        # Предполагаем, что запись видео потребляет в 2 раза больше энергии
        video_battery_life = self.battery_life_hours / 2
        return int(video_battery_life * 60)  # в минутах

    def get_lens_compatibility(self) -> List[str]:
        """
        Получает список совместимых объективов.

        Returns:
            List[str]: Список совместимых объективов
        """
        if not self.lens_mount:
            return []

        # Простая логика определения совместимости
        compatibility = [self.lens_mount]
        if self.lens_mount == "Canon EF":
            compatibility.extend(["Canon EF-S", "Canon EF-M"])
        elif self.lens_mount == "Nikon F":
            compatibility.extend(["Nikon DX"])
        elif self.lens_mount == "Sony E":
            compatibility.extend(["Sony FE"])

        return compatibility

    def estimate_storage_needs(self, recording_time_minutes: int) -> Dict[str, Any]:
        """
        Оценивает потребности в хранилище для записи.

        Args:
            recording_time_minutes: Время записи в минутах

        Returns:
            Dict[str, Any]: Информация о потребностях в хранилище
        """
        if not self.has_video:
            return {'error': 'Камера не поддерживает видео'}

        # Примерные расчеты (в GB)
        bitrate_4k = 7  # GB в час для 4K
        bitrate_1080p = 3  # GB в час для 1080p
        bitrate_720p = 1.5  # GB в час для 720p

        resolution = self.max_video_resolution or "1080p"
        if '4k' in resolution.lower():
            hourly_rate = bitrate_4k
        elif '1080' in resolution.lower():
            hourly_rate = bitrate_1080p
        else:
            hourly_rate = bitrate_720p

        hours = recording_time_minutes / 60
        estimated_gb = hours * hourly_rate

        return {
            'resolution': resolution,
            'recording_time_minutes': recording_time_minutes,
            'estimated_storage_gb': round(estimated_gb, 2),
            'recommended_card_capacity_gb': max(32, estimated_gb * 2)  # с запасом
        }

    def get_camera_features(self) -> List[str]:
        """
        Получает список особенностей камеры.

        Returns:
            List[str]: Список особенностей
        """
        features = []

        if self.supports_4k_video():
            features.append("4K видео")
        elif self.has_video:
            features.append("HD видео")

        if self.is_professional_grade():
            features.append("Профессиональный уровень")

        if self.sensor_size == SensorSize.FULL_FRAME:
            features.append("Полноформатный сенсор")

        if self.max_iso >= 51200:
            features.append("Высокая чувствительность ISO")

        if self.megapixels >= 50:
            features.append("Высокое разрешение")

        return features

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует камеру в словарь для сериализации.

        Returns:
            Dict[str, Any]: Словарь с данными камеры
        """
        data = super().to_dict()
        data.update({
            'camera_type': self.camera_type.value,
            'sensor_size': self.sensor_size.value,
            'megapixels': self.megapixels,
            'max_iso': self.max_iso,
            'has_video': self.has_video,
            'max_video_resolution': self.max_video_resolution,
            'lens_mount': self.lens_mount,
            'included_lens': self.included_lens,
            'memory_card_type': self.memory_card_type,
            'battery_type': self.battery_type,
            'tripod_mount': self.tripod_mount
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Camera':
        """
        Создает камеру из словаря.

        Args:
            data: Словарь с данными камеры

        Returns:
            Camera: Новый экземпляр камеры
        """
        # Преобразуем строковые значения обратно в соответствующие типы
        if 'camera_type' in data:
            data['camera_type'] = CameraType(data['camera_type'])
        if 'sensor_size' in data:
            data['sensor_size'] = SensorSize(data['sensor_size'])

        # Вызываем родительский from_dict для корректной десериализации
        return super().from_dict(data)
