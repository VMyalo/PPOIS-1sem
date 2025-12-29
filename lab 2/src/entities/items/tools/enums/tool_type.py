"""
Перечисление для типов инструментов.
"""

from enum import Enum


class ToolType(Enum):
    """
    Типы инструментов.

    Определяет категории инструментов для аренды.
    """

    HAND_TOOL = "hand_tool"
    POWER_TOOL = "power_tool"
    MEASURING_TOOL = "measuring_tool"
    CUTTING_TOOL = "cutting_tool"
    FASTENING_TOOL = "fastening_tool"
