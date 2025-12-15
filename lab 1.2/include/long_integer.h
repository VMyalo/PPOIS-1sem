// long_integer.h
#ifndef LONG_INTEGER_H_
#define LONG_INTEGER_H_

#include <iostream>
#include <string>
#include <vector>
#include <stdexcept>

/**
 * @brief Класс для представления и арифметики длинных целых чисел со знаком.
 *
 * Поддерживает числа произвольной длины (ограничены только доступной памятью).
 * Все операции выполняются без использования встроенных целочисленных типов
 * (таких как `long long`), что гарантирует корректность для любых значений.
 *
 * Число хранится в виде вектора десятичных цифр в обратном порядке
 * (младшая цифра — по индексу 0), и отдельного флага знака.
 */
class LongInteger {
 public:
  /**
   * @brief Конструктор по умолчанию.
   *
   * Создаёт объект, представляющий число `0`.
   *
   * @code
   * LongInteger a; // a == 0
   * @endcode
   */
  LongInteger();

  /**
   * @brief Конструктор из строкового представления.
   *
   * Инициализирует объект числом, заданным в виде строки.
   * Поддерживаются:
   * - положительные числа: `"123"`
   * - отрицательные числа: `"-456"`
   * - явный плюс: `"+789"`
   * - ведущие нули: `"00123"` → `123`
   * - ноль: `"0"`, `"-0"`, `"+0"` → `0`
   *
   * @param str Строка, содержащая корректное целое число.
   * @throws std::invalid_argument если строка пуста, содержит недопустимые символы
   *         или состоит только из знака.
   *
   * @code
   * LongInteger a("123");    // 123
   * LongInteger b("-456");   // -456
   * LongInteger c("+0");     // 0
   * @endcode
   */
  explicit LongInteger(const std::string& str);

  /**
   * @brief Конструктор копирования.
   *
   * Создаёт независимую копию другого объекта `LongInteger`.
   *
   * @param other Объект для копирования.
   */
  LongInteger(const LongInteger& other);

  /**
   * @brief Оператор присваивания.
   *
   * Присваивает текущему объекту значение другого объекта.
   *
   * @param other Объект-источник.
   * @return Ссылка на текущий объект после присваивания.
   */
  LongInteger& operator=(const LongInteger& other);

  /**
   * @brief Деструктор.
   *
   * Уничтожает объект. Реализован по умолчанию.
   */
  ~LongInteger() = default;

  // --- Арифметические операторы ---

  /**
   * @brief Оператор сложения.
   *
   * Возвращает сумму двух длинных целых чисел.
   *
   * @param other Второе слагаемое.
   * @return Результат сложения.
   */
  LongInteger operator+(const LongInteger& other) const;

  /**
   * @brief Оператор сложения с присваиванием.
   *
   * Добавляет к текущему объекту значение другого объекта.
   *
   * @param other Второе слагаемое.
   * @return Ссылка на текущий объект.
   */
  LongInteger& operator+=(const LongInteger& other);

  /**
   * @brief Оператор вычитания.
   *
   * Возвращает разность текущего и другого числа.
   *
   * @param other Вычитаемое.
   * @return Результат вычитания.
   */
  LongInteger operator-(const LongInteger& other) const;

  /**
   * @brief Оператор вычитания с присваиванием.
   *
   * Вычитает из текущего объекта значение другого объекта.
   *
   * @param other Вычитаемое.
   * @return Ссылка на текущий объект.
   */
  LongInteger& operator-=(const LongInteger& other);

  /**
   * @brief Оператор умножения.
   *
   * Возвращает произведение двух длинных целых чисел.
   *
   * @param other Множитель.
   * @return Результат умножения.
   */
  LongInteger operator*(const LongInteger& other) const;

  /**
   * @brief Оператор умножения с присваиванием.
   *
   * Умножает текущий объект на значение другого объекта.
   *
   * @param other Множитель.
   * @return Ссылка на текущий объект.
   */
  LongInteger& operator*=(const LongInteger& other);

  /**
   * @brief Оператор деления.
   *
   * Возвращает частное от деления текущего числа на другое.
   * Деление выполняется с **усечением к нулю** (как в C++ для встроенных типов).
   *
   * @param other Делитель.
   * @return Результат деления.
   * @throws std::domain_error если `other` равно нулю.
   *
   * @note Например: `7 / 3 == 2`, `-7 / 3 == -2`.
   */
  LongInteger operator/(const LongInteger& other) const;

  /**
   * @brief Оператор деления с присваиванием.
   *
   * Делит текущий объект на значение другого объекта.
   *
   * @param other Делитель.
   * @return Ссылка на текущий объект.
   * @throws std::domain_error если `other` равно нулю.
   */
  LongInteger& operator/=(const LongInteger& other);

  /**
   * @brief Оператор взятия остатка (modulo).
   *
   * Возвращает остаток от деления текущего числа на другое.
   * Знак результата совпадает со знаком делимого (как в C++).
   *
   * @param other Делитель.
   * @return Остаток от деления.
   * @throws std::domain_error если `other` равно нулю.
   *
   * @note Например: `7 % 3 == 1`, `-7 % 3 == -1`.
   */
  LongInteger operator%(const LongInteger& other) const;

  /**
   * @brief Оператор взятия остатка с присваиванием.
   *
   * Присваивает текущему объекту остаток от деления на другое число.
   *
   * @param other Делитель.
   * @return Ссылка на текущий объект.
   * @throws std::domain_error если `other` равно нулю.
   */
  LongInteger& operator%=(const LongInteger& other);

  // --- Инкремент и декремент ---

  /**
   * @brief Префиксный инкремент.
   *
   * Увеличивает число на 1 и возвращает ссылку на обновлённый объект.
   * 
   * @return Ссылка на текущий объект после увеличения.
   */
  LongInteger& operator++();

  /**
   * @brief Постфиксный инкремент.
   *
   * Увеличивает число на 1, но возвращает **копию до изменения**.
   *
   * @return Копия объекта до увеличения.
   */
  LongInteger operator++(int);

  /**
   * @brief Префиксный декремент.
   *
   * Уменьшает число на 1 и возвращает ссылку на обновлённый объект.
   *
   * @return Ссылка на текущий объект после уменьшения.
   */
  LongInteger& operator--();

  /**
   * @brief Постфиксный декремент.
   *
   * Уменьшает число на 1, но возвращает **копию до изменения**.
   *
   * @return Копия объекта до уменьшения.
   */
  LongInteger operator--(int);

  // --- Операторы сравнения ---

  /**
   * @brief Проверка на равенство.
   *
   * @param other Число для сравнения.
   * @return `true`, если числа равны; иначе `false`.
   */
  bool operator==(const LongInteger& other) const;

  /**
   * @brief Проверка на неравенство.
   *
   * @param other Число для сравнения.
   * @return `true`, если числа не равны; иначе `false`.
   */
  bool operator!=(const LongInteger& other) const;

  /**
   * @brief Сравнение "больше".
   *
   * @param other Число для сравнения.
   * @return `true`, если текущее число больше; иначе `false`.
   */
  bool operator>(const LongInteger& other) const;

  /**
   * @brief Сравнение "меньше".
   *
   * @param other Число для сравнения.
   * @return `true`, если текущее число меньше; иначе `false`.
   */
  bool operator<(const LongInteger& other) const;

  /**
   * @brief Сравнение "больше или равно".
   *
   * @param other Число для сравнения.
   * @return `true`, если текущее число >= other; иначе `false`.
   */
  bool operator>=(const LongInteger& other) const;

  /**
   * @brief Сравнение "меньше или равно".
   *
   * @param other Число для сравнения.
   * @return `true`, если текущее число <= other; иначе `false`.
   */
  bool operator<=(const LongInteger& other) const;

  // --- Ввод/вывод ---

  /**
   * @brief Оператор ввода из потока.
   *
   * Считывает строковое представление числа из входного потока
   * и конструирует `LongInteger`. Поддерживает тот же формат,
   * что и конструктор из строки.
   *
   * @param is Входной поток (например, `std::cin`).
   * @param num Объект для записи результата.
   * @return Ссылка на входной поток.
   * @throws std::invalid_argument при некорректном формате (устанавливает failbit).
   */
  friend std::istream& operator>>(std::istream& is, LongInteger& num);

  /**
   * @brief Оператор вывода в поток.
   *
   * Выводит строковое представление числа в выходной поток.
   * Отрицательные числа выводятся с префиксом `'-'`.
   *
   * @param os Выходной поток (например, `std::cout`).
   * @param num Объект для вывода.
   * @return Ссылка на выходной поток.
   */
  friend std::ostream& operator<<(std::ostream& os, const LongInteger& num);

 private:
  std::vector<int> digits_;  ///< Цифры числа в обратном порядке (младшая — первая)
  bool is_negative_;         ///< Флаг отрицательного числа

  /**
   * @brief Удаляет ведущие нули из внутреннего представления.
   *
   * После удаления, если число становится пустым, устанавливает его в `0`
   * и сбрасывает флаг отрицательности.
   */
  void RemoveLeadingZeros();

  /**
   * @brief Сравнивает абсолютные значения двух чисел.
   *
   * @param other Число для сравнения (должно быть без знака).
   * @return 1, если |this| > |other|; -1, если |this| < |other|; 0, если равны.
   */
  int CompareAbsolute(const LongInteger& other) const;

  /**
   * @brief Складывает два положительных числа.
   *
   * @param other Второе слагаемое (должно быть положительным).
   * @return Результат сложения (положительное число).
   */
  LongInteger AddPositive(const LongInteger& other) const;

  /**
   * @brief Вычитает из текущего положительного числа другое положительное.
   *
   * Предусловие: |this| >= |other|.
   *
   * @param other Вычитаемое (положительное, не больше текущего).
   * @return Результат вычитания (неотрицательное число).
   */
  LongInteger SubtractPositive(const LongInteger& other) const;

  /**
   * @brief Умножает два положительных числа.
   *
   * @param other Множитель (должен быть положительным).
   * @return Результат умножения (положительное число).
   */
  LongInteger MultiplyPositive(const LongInteger& other) const;

  /**
   * @brief Делит текущее положительное число на другое положительное.
   *
   * Возвращает **частное** (целую часть от деления).
   *
   * @param other Делитель (положительное, не ноль).
   * @return Частное (неотрицательное число).
   */
  LongInteger DividePositive(const LongInteger& other) const;

  /**
   * @brief Возвращает остаток от деления двух положительных чисел.
   *
   * @param other Делитель (положительное, не ноль).
   * @return Остаток (неотрицательное число).
   */
  LongInteger ModuloPositive(const LongInteger& other) const;
};

#endif  // LONG_INTEGER_H_