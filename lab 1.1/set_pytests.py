# set_pytests.py

import pytest
from cantorian_set import CantorianSet
import copy

def test_init_empty_string():
    """Тест инициализации пустого множества из строки."""
    cs = CantorianSet("{}")
    assert len(cs) == 0
    assert cs.is_empty()

def test_init_empty_list():
    """Тест инициализации пустого множества из пустого списка."""
    cs = CantorianSet([])
    assert len(cs) == 0
    assert cs.is_empty()

def test_init_empty_none():
    """Тест инициализации пустого множества без аргументов."""
    cs = CantorianSet()
    assert len(cs) == 0
    assert cs.is_empty()

def test_init_with_simple_elements():
    """Тест инициализации множества с простыми элементами."""
    cs = CantorianSet("{a, b, c}")
    assert len(cs) == 3
    assert "a" in cs
    assert "b" in cs
    assert "c" in cs

def test_init_with_nested_sets():
    """Тест инициализации множества с вложенными множествами."""
    cs = CantorianSet("{a, {b, c}, {d}}")
    assert len(cs) == 3

    found_nested_b_c = False
    found_nested_d = False
    for elem in cs:
        if isinstance(elem, CantorianSet):
            if len(elem) == 2 and "b" in elem and "c" in elem:
                found_nested_b_c = True
            elif len(elem) == 1 and "d" in elem:
                found_nested_d = True
    assert found_nested_b_c
    assert found_nested_d

def test_init_with_numbers():
    """Тест инициализации множества с числовыми элементами."""
    cs = CantorianSet("{1, 2.5, 3}")
    assert len(cs) == 3
    assert 1 in cs
    assert 2.5 in cs
    assert 3 in cs

def test_init_with_mixed_types():
    """Тест инициализации множества с элементами разных типов."""
    cs = CantorianSet("{1, a, 2.5, {x, y}}")
    assert len(cs) == 4
    assert 1 in cs
    assert "a" in cs
    assert 2.5 in cs

    found_nested = False
    for elem in cs:
        if isinstance(elem, CantorianSet):
            if len(elem) == 2 and "x" in elem and "y" in elem:
                found_nested = True
                break
    assert found_nested

def test_add_element():
    """Тест добавления элемента."""
    cs = CantorianSet("{}")
    cs.add("new_element")
    assert "new_element" in cs
    assert len(cs) == 1

def test_remove_element():
    """Тест удаления элемента."""
    cs = CantorianSet("{a, b, c}")
    cs.remove("b")
    assert "b" not in cs
    assert len(cs) == 2

def test_remove_element_not_found():
    """Тест удаления несуществующего элемента (должно вызвать KeyError)."""
    cs = CantorianSet("{a, b, c}")
    with pytest.raises(KeyError):
        cs.remove("d")

def test_contains():
    """Тест оператора in (__contains__)."""
    cs = CantorianSet("{a, {b, c}}")
    assert "a" in cs
    assert "d" not in cs

    nested_cs = CantorianSet("{b, c}")
    assert nested_cs in cs

def test_len():
    """Тест получения длины (__len__)."""
    cs = CantorianSet("{}")
    assert len(cs) == 0

    cs = CantorianSet("{a, b, c}")
    assert len(cs) == 3

def test_str():
    """Тест строкового представления (__str__)."""
    cs = CantorianSet("{}")
    assert str(cs) == "{}"

    # Тестирование строкового представления. Порядок элементов в множестве не фиксирован,
    # поэтому проверим, что все ожидаемые элементы присутствуют в строке.
    cs2 = CantorianSet("{a, b, c}")
    str_repr = str(cs2)
    assert "a" in str_repr
    assert "b" in str_repr
    assert "c" in str_repr
    assert str_repr.startswith("{")
    assert str_repr.endswith("}")

def test_repr():
    """Тест строкового представления для отладки (__repr__)."""
    cs = CantorianSet("{a, b}")
    repr_str = repr(cs)
    # Проверим, что repr содержит название класса
    assert "CantorianSet" in repr_str

def test_equality():
    """Тест равенства множеств (__eq__)."""
    cs1 = CantorianSet("{a, b, c}")
    cs2 = CantorianSet("{c, b, a}")  # Порядок не важен
    assert cs1 == cs2

    cs3 = CantorianSet("{a, b, d}")
    assert cs1 != cs3

def test_equality_with_nested():
    """Тест равенства множеств с вложенными структурами."""
    cs1 = CantorianSet("{a, {b, c}}")
    cs2 = CantorianSet("{a, {c, b}}")
    assert cs1 == cs2

    cs3 = CantorianSet("{a, {b, d}}")
    assert cs1 != cs3

def test_inequality():
    """Тест неравенства (__ne__)."""
    cs1 = CantorianSet("{a, b}")
    cs2 = CantorianSet("{c, d}")
    assert cs1 != cs2

def test_hash():
    """Тест вычисления хеша (__hash__)."""
    cs1 = CantorianSet("{a, b}")
    cs2 = CantorianSet("{b, a}")
    # Множества равны, значит, их хеши должны быть равны
    assert hash(cs1) == hash(cs2)

    # Проверим, что хеш можно использовать в словаре
    d = {cs1: "value1"}
    assert cs2 in d # cs2 равен cs1, значит, ключ должен быть найден
    assert d[cs2] == "value1"

def test_to_list():
    """Тест преобразования в список."""
    cs = CantorianSet("{a, b, c}")
    list_repr = cs.to_list()
    assert len(list_repr) == 3
    # Проверим, что все элементы из множества присутствуют в списке
    for elem in cs:
        assert elem in list_repr

def test_is_empty():
    """Тест проверки на пустоту."""
    cs = CantorianSet("{}")
    assert cs.is_empty()

    cs.add("element")
    assert not cs.is_empty()

def test_copy():
    """Тест поверхностного копирования (__copy__)."""
    original = CantorianSet("{a, {b, c}}")
    copied = copy.copy(original)

    assert original == copied
    assert original is not copied # Это разные объекты

    # Изменение копии не должно влиять на оригинал
    # (для вложенных объектов, как CantorianSet, это будет поверхностное копирование)
    original_nested = None
    for elem in original:
        if isinstance(elem, CantorianSet):
            original_nested = elem
            break

    copied_nested = None
    for elem in copied:
        if isinstance(elem, CantorianSet):
            copied_nested = elem
            break

    # Объекты вложенных множеств также будут разными
    assert original_nested is not copied_nested
    # Но элементы внутри вложенного множества будут теми же объектами (поверхностное копирование)
    # В нашем случае, это строки "b" и "c", которые неизменяемы, это нормально.

    copied.add("new_to_copied")
    assert "new_to_copied" not in original

def test_deepcopy():
    """Тест глубокого копирования (__deepcopy__)."""
    original = CantorianSet("{a, {b, c}}")
    deep_copied = copy.deepcopy(original)

    assert original == deep_copied
    assert original is not deep_copied

    # Найдем вложенное множество в оригинале и копии
    original_nested = None
    for elem in original:
        if isinstance(elem, CantorianSet):
            original_nested = elem
            break

    deep_copied_nested = None
    for elem in deep_copied:
        if isinstance(elem, CantorianSet):
            deep_copied_nested = elem
            break

    # Объекты вложенных множеств должны быть разными
    assert original_nested is not deep_copied_nested

    # Изменение вложенного множества в копии не влияет на оригинал
    deep_copied_nested.add("new_to_nested_copied")
    assert "new_to_nested_copied" not in original_nested

def test_invalid_string_format():
    """Тест обработки неверного формата строки."""
    with pytest.raises(ValueError):
        CantorianSet("invalid_format")
    with pytest.raises(ValueError):
        CantorianSet("{a, b") # Незакрытая скобка
    with pytest.raises(ValueError):
        CantorianSet("a, b}") # Неправильная строка


def test_init_with_quoted_strings():
    """Тест инициализации с элементами в кавычках."""
    cs = CantorianSet('{ "hello", \'world\', item }')
    assert len(cs) == 3
    assert "hello" in cs
    assert "world" in cs
    assert "item" in cs

def test_split_elements_complex():
    """Тест метода _split_elements с вложенными структурами."""
    cs = CantorianSet() # Создаем пустой объект для вызова метода
    # Тестируем строку с вложенными скобками
    s = "a, {b, {c, d}}, e"
    result = cs._split_elements(s)
    expected = ["a", " {b, {c, d}}", " e"] # Пробелы сохраняются как есть
    assert result == expected

def test_parse_string_with_quoted_elements():
    """Тест _parse_string с кавычками."""
    cs = CantorianSet()
    s = '{ "quoted_str", \'single_quoted\', unquoted }'
    cs._parse_string(s)
    assert len(cs) == 3
    assert "quoted_str" in cs
    assert "single_quoted" in cs
    assert "unquoted" in cs

def test_hash_consistency():
    """Тест, что хеш одинаков для равных объектов."""
    s1 = "{a, b}"
    s2 = "{b, a}" # Порядок разный, но множества равны
    cs1 = CantorianSet(s1)
    cs2 = CantorianSet(s2)
    assert cs1 == cs2
    assert hash(cs1) == hash(cs2)

def test_hash_with_nested_sets():
    """Тест хеша для вложенных множеств."""
    cs1 = CantorianSet("{x, {y, z}}")
    cs2 = CantorianSet("{x, {z, y}}") # Вложенное множество с другим порядком
    assert cs1 == cs2
    assert hash(cs1) == hash(cs2)

def test_copy_with_nested_cantorian_sets():
    """Тест поверхностного копирования с вложенными CantorianSet."""
    original = CantorianSet("{a, {b, {c}}}")
    copied = copy.copy(original)

    assert original == copied
    assert original is not copied

    # Проверим, что вложенные CantorianSet'ы тоже скопированы (поверхностно)
    original_nested_level1 = None
    original_nested_level2 = None
    for elem in original:
        if isinstance(elem, CantorianSet):
            original_nested_level1 = elem
            for sub_elem in elem:
                if isinstance(sub_elem, CantorianSet):
                    original_nested_level2 = sub_elem
                    break
            break

    copied_nested_level1 = None
    copied_nested_level2 = None
    for elem in copied:
        if isinstance(elem, CantorianSet):
            copied_nested_level1 = elem
            for sub_elem in elem:
                if isinstance(sub_elem, CantorianSet):
                    copied_nested_level2 = sub_elem
                    break
            break

    assert original_nested_level1 is not copied_nested_level1
    assert original_nested_level2 is not copied_nested_level2

def test_deepcopy_with_nested_cantorian_sets():
    """Тест глубокого копирования с вложенными CantorianSet."""
    original = CantorianSet("{a, {b, {c}}}")
    deep_copied = copy.deepcopy(original)

    assert original == deep_copied
    assert original is not deep_copied

    # Проверим, что вложенные CantorianSet'ы тоже скопированы (глубоко)
    original_nested_level1 = None
    original_nested_level2 = None
    for elem in original:
        if isinstance(elem, CantorianSet):
            original_nested_level1 = elem
            for sub_elem in elem:
                if isinstance(sub_elem, CantorianSet):
                    original_nested_level2 = sub_elem
                    break
            break

    deep_copied_nested_level1 = None
    deep_copied_nested_level2 = None
    for elem in deep_copied:
        if isinstance(elem, CantorianSet):
            deep_copied_nested_level1 = elem
            for sub_elem in elem:
                if isinstance(sub_elem, CantorianSet):
                    deep_copied_nested_level2 = sub_elem
                    break
            break

    assert original_nested_level1 is not deep_copied_nested_level1
    assert original_nested_level2 is not deep_copied_nested_level2

    # Проверим изоляцию - изменение вложенного в копии не влияет на оригинал
    deep_copied_nested_level2.add("new_deep")
    assert "new_deep" not in original_nested_level2

def test_init_with_list_of_cantorian_sets():
    """Тест инициализации из списка, содержащего CantorianSet."""
    nested1 = CantorianSet("{x, y}")
    nested2 = CantorianSet("{z}")
    cs = CantorianSet([nested1, nested2, "standalone"])
    assert len(cs) == 3
    assert nested1 in cs
    assert nested2 in cs
    assert "standalone" in cs

def test_str_with_empty_sets():
    """Тест строкового представления с пустыми множествами."""
    cs = CantorianSet("{a, {}, {b, {}}}")
    str_repr = str(cs)
    # Проверим, что строка содержит ожидаемые элементы и пустые множества
    assert "a" in str_repr
    assert "{}" in str_repr # Пустое множество
    # Сложно проверить вложенное "{}" точно, но общая структура должна быть

def test_repr_detailed():
    """Тест детального repr."""
    cs = CantorianSet("{1, a}")
    repr_str = repr(cs)
    assert "CantorianSet" in repr_str
    # repr использует list(self._elements), порядок не фиксирован, проверим содержание
    assert "1" in repr_str or "'1'" in repr_str # Может быть '1' или 1
    assert "a" in repr_str or "'a'" in repr_str

def test_iter():
    """Тест итерации (__iter__)."""
    elements = ["x", "y", CantorianSet("{z}")]
    cs = CantorianSet() # Создаем пустое
    for elem in elements:
        cs.add(elem)

    iterated_elements = []
    for item in cs: # Используем __iter__
        iterated_elements.append(item)

    assert len(iterated_elements) == 3
    for elem in elements:
        assert elem in iterated_elements

def test_init_invalid_string_format():
    """Тест исключения при неверном формате строки."""
    with pytest.raises(ValueError):
        CantorianSet("not_a_set")
    with pytest.raises(ValueError):
        CantorianSet("{unclosed")
    with pytest.raises(ValueError):
        CantorianSet("unclosed}")

def test_parse_string_with_float_numbers():
    """Тест _parse_string с числами с плавающей точкой."""
    cs = CantorianSet("{1.1, 2.2, 3}")
    assert len(cs) == 3
    assert 1.1 in cs
    assert 2.2 in cs
    assert 3 in cs

def test_parse_string_with_only_numbers():
    """Тест _parse_string только с числами."""
    cs = CantorianSet("{1, 2, 3, 4.5, 6.7}")
    assert len(cs) == 5
    assert 1 in cs
    assert 2 in cs
    assert 3 in cs
    assert 4.5 in cs
    assert 6.7 in cs

def test_parse_string_with_mixed_types_and_quotes():
    """Тест _parse_string с разными типами и кавычками."""
    cs = CantorianSet('{1, "str", 2.5, {nested}, \'single\'}')
    assert len(cs) == 5
    assert 1 in cs
    assert "str" in cs
    assert 2.5 in cs
    assert "single" in cs
    found_nested = False
    for elem in cs:
        if isinstance(elem, CantorianSet) and len(elem) == 1 and "nested" in elem:
            found_nested = True
            break
    assert found_nested

def test_ne_with_equal_sets():
    """Тест __ne__ с равными множествами."""
    cs1 = CantorianSet("{a, b}")
    cs2 = CantorianSet("{b, a}")
    assert not (cs1 != cs2) # cs1 != cs2 должно быть False

def test_ne_with_unequal_sets():
    """Тест __ne__ с неравными множествами."""
    cs1 = CantorianSet("{a, b}")
    cs2 = CantorianSet("{a, c}")
    assert cs1 != cs2 # cs1 != cs2 должно быть True

def test_ne_with_non_cantorian_set():
    """Тест __ne__ с не-CantorianSet объектом."""
    cs = CantorianSet("{a}")
    assert cs != "not a set"
    assert cs != 123
    assert cs != ["not", "a", "set"]
