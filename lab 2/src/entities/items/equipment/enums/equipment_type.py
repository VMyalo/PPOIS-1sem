"""
Перечисление для типов оборудования.
"""

from enum import Enum


class EquipmentType(Enum):
    """
    Типы оборудования.

    Определяет категории оборудования для аренды.
    """

    CAMERA = "camera"
    DRONE = "drone"
    SPORT_EQUIPMENT = "sport_equipment"
    AUDIO_EQUIPMENT = "audio_equipment"
    VIDEO_EQUIPMENT = "video_equipment"
    LIGHTING_EQUIPMENT = "lighting_equipment"
