# cantorian_set.py

from typing import Any, List, Union
import copy


class CantorianSet:
    """Неориентированное канторовское множество.

    Класс реализует структуру данных, представляющую собой вложенные множества,
    которые могут быть сформированы из строкового представления в формате,
    похожем на JSON или Python-литералы множеств.
    Пример: "{a, b, c, {a, b}, {}, {a, {c}}}".
    """

    def __init__(self, data: Union[str, List[Any]] = None):
        """Инициализирует экземпляр класса.

        Args:
            data: Строка, представляющая множество в виде текста,
                  или список элементов, который будет преобразован в множество.
                  Если None, создается пустое множество.
        """
        self._elements = set()
        if isinstance(data, str):
            self._parse_string(data)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, CantorianSet):
                    self._elements.add(item)
                else:
                    self._elements.add(item)

    def _parse_string(self, s: str) -> None:
        """Разбирает строку и заполняет внутреннее множество.

        Args:
            s: Строка, содержащая представление множества.
        """
        # Удаляем пробелы в начале и конце
        s = s.strip()
        if not (s.startswith('{') and s.endswith('}')):
            raise ValueError("Строка должна начинаться с '{' и заканчиваться на '}'")

        # Убираем внешние скобки
        content = s[1:-1].strip()

        if not content:  # Пустое множество
            return

        # Разбираем содержимое
        elements = self._split_elements(content)
        for elem_str in elements:
            elem_str = elem_str.strip()
            if elem_str.startswith('{') and elem_str.endswith('}'):
                # Это вложенное множество
                nested_set = CantorianSet(elem_str)
                self._elements.add(nested_set)
            else:
                # Это простой элемент (строка, число и т.д.)
                # Попробуем распознать как число, иначе оставим как строку
                try:
                    # Попробуем как целое число
                    value = int(elem_str)
                except ValueError:
                    try:
                        # Попробуем как число с плавающей точкой
                        value = float(elem_str)
                    except ValueError:
                        # Оставляем как строку (удаляем кавычки, если есть)
                        if elem_str.startswith('"') and elem_str.endswith('"'):
                            value = elem_str[1:-1]
                        elif elem_str.startswith("'") and elem_str.endswith("'"):
                            value = elem_str[1:-1]
                        else:
                            value = elem_str
                self._elements.add(value)

    def _split_elements(self, s: str) -> List[str]:
        """Разбивает строку на отдельные элементы, учитывая вложенные скобки.

        Args:
            s: Строка с элементами, разделенными запятыми.

        Returns:
            Список строк, каждый элемент которого — один элемент множества.
        """
        elements = []
        current_element = ""
        bracket_level = 0

        for char in s:
            if char == '{':
                bracket_level += 1
                current_element += char
            elif char == '}':
                bracket_level -= 1
                current_element += char
            elif char == ',' and bracket_level == 0:
                elements.append(current_element)
                current_element = ""
            else:
                current_element += char

        # Добавляем последний элемент
        if current_element:
            elements.append(current_element)

        return elements

    def add(self, element: Any) -> None:
        """Добавляет элемент в множество.

        Args:
            element: Элемент, который нужно добавить. Может быть любым объектом,
                     включая другой экземпляр CantorianSet.
        """
        self._elements.add(element)

    def remove(self, element: Any) -> None:
        """Удаляет элемент из множества.

        Args:
            element: Элемент, который нужно удалить.

        Raises:
            KeyError: Если элемент не найден в множестве.
        """
        self._elements.remove(element)

    def __contains__(self, item: Any) -> bool:
        """Проверяет, содержит ли множество заданный элемент.

        Args:
            item: Элемент для проверки.

        Returns:
            True, если элемент присутствует в множестве, False в противном случае.
        """
        return item in self._elements

    def __len__(self) -> int:
        """Возвращает количество элементов в множестве.

        Returns:
            Количество элементов.
        """
        return len(self._elements)

    def __str__(self) -> str:
        """Возвращает строковое представление множества.

        Returns:
            Строковое представление множества в виде "{элемент1, элемент2, ...}".
        """
        elements_str = []
        for elem in self._elements:
            if isinstance(elem, CantorianSet):
                elements_str.append(str(elem))
            else:
                elements_str.append(repr(elem))
        return "{" + ", ".join(elements_str) + "}"

    def __repr__(self) -> str:
        """Возвращает строковое представление для отладки.

        Returns:
            Строковое представление, которое может быть использовано для создания
            нового экземпляра.
        """
        return f"CantorianSet({list(self._elements)})"

    def __eq__(self, other: Any) -> bool:
        """Сравнивает два множества на равенство.

        Args:
            other: Другой объект для сравнения.

        Returns:
            True, если множества равны, False в противном случае.
        """
        if not isinstance(other, CantorianSet):
            return False
        # Поэлементное сравнение
        if len(self) != len(other):
            return False
        for elem in self._elements:
            found = False
            for other_elem in other._elements:
                if isinstance(elem, CantorianSet) and isinstance(other_elem, CantorianSet):
                    if elem == other_elem:
                        found = True
                        break
                elif elem == other_elem:
                    found = True
                    break
            if not found:
                return False
        return True

    def __ne__(self, other: Any) -> bool:
        """Сравнивает два множества на неравенство.

        Args:
            other: Другой объект для сравнения.

        Returns:
            True, если множества не равны, False в противном случае.
        """
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Позволяет использовать экземпляр в качестве ключа словаря.

        Возвращает хеш, основанный на строковом представлении множества.
        """
        return hash(str(self))

    def to_list(self) -> List[Any]:
        """Преобразует множество в список.

        Returns:
            Список элементов множества.
        """
        return list(self._elements)

    def is_empty(self) -> bool:
        """Проверяет, является ли множество пустым.

        Returns:
            True, если множество пустое, False в противном случае.
        """
        return len(self) == 0

    def __copy__(self) -> 'CantorianSet':
        """Создает поверхностную копию множества.

        Returns:
            Новый экземпляр CantorianSet, содержащий копии элементов (поверхностное копирование).
        """
        import copy # Импортируем внутри функции, чтобы избежать циклической зависимости при старте модуля
        new_set = CantorianSet()
        for elem in self._elements:
            # Добавляем копию элемента, а не сам элемент
            new_set.add(copy.copy(elem))
        return new_set

    def __deepcopy__(self, memo: dict) -> 'CantorianSet':
        """Создает глубокую копию множества.

        Args:
            memo: Словарь для отслеживания уже скопированных объектов (для избежания циклов).

        Returns:
            Новый экземпляр CantorianSet, содержащий копии всех элементов.
        """
        new_set = CantorianSet()
        for elem in self._elements:
            if isinstance(elem, CantorianSet):
                new_set.add(copy.deepcopy(elem, memo))
            else:
                new_set.add(copy.deepcopy(elem, memo))
        return new_set

    def __iter__(self):
        """Возвращает итератор по элементам множества.

        Returns:
            Итератор по внутреннему множеству _elements.
        """
        # Возвращаем итератор от внутреннего объекта set
        return iter(self._elements)