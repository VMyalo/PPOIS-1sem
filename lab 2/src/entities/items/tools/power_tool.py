"""
Класс электроинструментов.

Этот модуль содержит реализацию электроинструментов.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from .base_tool import BaseTool, ToolType


@dataclass
class PowerTool(BaseTool):
    """
    Класс представляющий электроинструменты.

    Attributes:
        voltage: Напряжение
        motor_type: Тип двигателя
        rpm: Обороты в минуту
        battery_capacity: Емкость батареи
        charging_time_hours: Время зарядки
    """

    voltage: int = 220
    motor_type: str = "electric"
    rpm: Optional[int] = None
    battery_capacity: Optional[int] = None  # mAh
    charging_time_hours: Optional[float] = None

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.tool_type = ToolType.POWER_TOOL
        self.requires_power = True

    def get_power_specs(self) -> Dict[str, Any]:
        """
        Получает спецификации питания.

        Returns:
            Dict[str, Any]: Спецификации питания
        """
        return {
            'voltage': self.voltage,
            'motor_type': self.motor_type,
            'rpm': self.rpm,
            'battery_capacity': self.battery_capacity,
            'charging_time_hours': self.charging_time_hours
        }
