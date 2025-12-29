"""
Класс ручных инструментов.

Этот модуль содержит реализацию ручных инструментов.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from .base_tool import BaseTool, ToolType


@dataclass
class HandTool(BaseTool):
    """
    Класс представляющий ручные инструменты.

    Attributes:
        grip_type: Тип хвата
        blade_material: Материал лезвия
        handle_material: Материал рукоятки
        adjustable: Регулируемый
    """

    grip_type: str = "standard"
    blade_material: Optional[str] = None
    handle_material: Optional[str] = None
    adjustable: bool = False

    def __post_init__(self):
        """Инициализация после создания объекта."""
        super().__post_init__()
        self.tool_type = ToolType.HAND_TOOL
        self.requires_power = False

    def get_tool_specs(self) -> Dict[str, Any]:
        """
        Получает спецификации инструмента.

        Returns:
            Dict[str, Any]: Спецификации
        """
        return {
            'grip_type': self.grip_type,
            'blade_material': self.blade_material,
            'handle_material': self.handle_material,
            'adjustable': self.adjustable,
            'weight_grams': self.weight_grams
        }
