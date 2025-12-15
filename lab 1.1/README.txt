# Активировать виртуальное окружение
source ./venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
# (В действительности проект зависит только от typing, тесты зависят от pytest - но это встроенные библиотеки)

# Запустить тесты
pytest test_cantorian_set_pytest.py -v

# Генерация отчёта о покрытии
pytest --cov=cantorian_set test_cantorian_set_pytest.py --cov-report=term-missing --cov-report=html:htmlcov -v

# Сгенерировать документацию
doxygen Doxyfile