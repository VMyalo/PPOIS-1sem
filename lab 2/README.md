# Система Аренды Предметов

Учебный проект демонстрирующий принципы объектно-ориентированного программирования на Python.

## Обзор

Система представляет собой полнофункциональную платформу для аренды различных предметов (оборудование, инструменты, транспорт, одежда). Проект разработан с соблюдением принципов SOLID, DRY, KISS, BDUF и лучших практик ООП.

## Архитектура

### Основные Компоненты

- **81 класс** с иерархией наследования (35 основных, 20 Enum, 10 Protocol/Interface, 16 исключений)
- **349 методов** включая методы экземпляров, класс-методы, статические методы и свойства
- **30+ ассоциаций** между классами (наследование, композиция, агрегация, зависимости)
- **16 исключений** (1 базовое + 15 персональных)

## Структура Проекта

```
src/
├── core/                    # Базовые классы и интерфейсы
│   ├── base.py             # BaseEntity, BaseService, Repository
│   ├── identifiable.py     # Интерфейс Identifiable
│   ├── validatable.py      # Интерфейс Validatable
│   ├── serializable.py     # Интерфейс Serializable
│   ├── calculable.py       # Протокол Calculable
│   ├── reservable.py       # Протокол Reservable
│   ├── payable.py          # Протокол Payable
│   ├── notifiable.py       # Протокол Notifiable
│   ├── trackable.py        # Протокол Trackable
│   ├── interfaces.py       # Интерфейсы
│   ├── protocols.py        # Протоколы
│   └── exceptions/         # Исключения системы
│       ├── __init__.py
│       ├── base_exception.py
│       ├── auth_exceptions.py  # Исключения аутентификации (дубликаты)
│       ├── auth/           # Исключения аутентификации
│       ├── inventory/      # Исключения инвентаря
│       ├── payment/        # Исключения платежей
│       ├── rental/         # Исключения аренды
│       └── other/          # Прочие исключения
├── entities/               # Сущности предметной области
│   ├── people/            # Люди в системе
│   │   ├── base_person.py
│   │   ├── customer.py
│   │   ├── employee/      # Сотрудники
│   │   │   ├── base_employee.py
│   │   │   ├── manager.py
│   │   │   ├── administrator.py
│   │   │   └── enums/
│   │   └── enums/
│   ├── items/             # Предметы аренды
│   │   ├── base_item.py
│   │   ├── equipment/     # Оборудование
│   │   │   ├── base_equipment.py
│   │   │   ├── camera.py
│   │   │   ├── drone.py
│   │   │   ├── sport_equipment.py
│   │   │   └── enums/
│   │   ├── tools/         # Инструменты
│   │   │   ├── base_tool.py
│   │   │   ├── hand_tool.py
│   │   │   ├── power_tool.py
│   │   │   └── enums/
│   │   ├── vehicles/      # Транспорт
│   │   │   ├── base_vehicle.py
│   │   │   ├── car.py
│   │   │   ├── bicycle.py
│   │   │   ├── motorcycle.py
│   │   │   ├── scooter.py
│   │   │   └── enums/
│   │   ├── clothing/      # Одежда
│   │   │   ├── clothing_item.py
│   │   │   └── enums/
│   │   └── enums/
│   ├── payments/          # Платежи
│   │   ├── base_payment.py
│   │   ├── cash.py
│   │   ├── credit_card.py
│   │   ├── wallet.py
│   │   └── enums/
│   └── rentals/           # Аренда и резервы
│       └── reservation.py
├── services/              # Бизнес-логика
│   ├── auth_service.py
│   └── rental_service.py
├── utils/                 # Утилиты и константы
│   └── constants.py
└── tests/                 # Тесты
    └── test_basic_functionality.py
```

## Классы Системы

### 1. Базовые Классы и Интерфейсы

#### `BaseEntity`
```python
@dataclass
class BaseEntity(Identifiable, Validatable, Serializable):
    entity_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
```

**Поля:**
- `entity_id: str` - Уникальный идентификатор
- `created_at: datetime` - Время создания
- `updated_at: datetime` - Время последнего обновления
- `is_active: bool` - Активность сущности

**Методы:**
- `id: str` - Уникальный идентификатор (свойство)
- `generate_id() -> str` - Генерация нового ID
- `validate() -> bool` - Валидация состояния
- `get_validation_errors() -> List[str]` - Получение ошибок валидации
- `update_timestamp() -> None` - Обновление временной метки
- `to_dict() -> Dict[str, Any]` - Сериализация в словарь
- `from_dict(data: Dict[str, Any]) -> BaseEntity` - Десериализация из словаря (classmethod)

#### `BaseService[T]`
```python
class BaseService(Generic[T], ABC):
    repository: Optional[Repository[T]]
```

**Поля:**
- `repository: Optional[Repository[T]]` - Репозиторий для операций с данными

**Методы:**
- `create(entity: T) -> T` - Создание сущности
- `get_by_id(entity_id: str) -> Optional[T]` - Получение по ID
- `update(entity: T) -> T` - Обновление сущности
- `delete(entity_id: str) -> bool` - Удаление сущности
- `get_all() -> List[T]` - Получение всех сущностей

#### `Repository[T]`
```python
class Repository(Generic[T], ABC):
```

**Методы:**
- `save(entity: T) -> T` - Сохранение сущности
- `find_by_id(entity_id: str) -> Optional[T]` - Поиск по ID
- `find_all() -> List[T]` - Поиск всех сущностей
- `delete(entity_id: str) -> bool` - Удаление сущности
- `exists(entity_id: str) -> bool` - Проверка существования

#### Интерфейсы и Протоколы

##### `Identifiable`
```python
class Identifiable(ABC):
```

**Методы:**
- `id: str` - Уникальный идентификатор (свойство)
- `generate_id() -> str` - Генерация нового ID

##### `Validatable`
```python
class Validatable(ABC):
```

**Методы:**
- `validate() -> bool` - Валидация состояния
- `get_validation_errors() -> List[str]` - Получение ошибок валидации

##### `Serializable`
```python
class Serializable(ABC):
```

**Методы:**
- `to_dict() -> Dict[str, Any]` - Преобразование в словарь
- `from_dict(data: Dict[str, Any]) -> Serializable` - Создание из словаря

##### `Calculable` (Protocol)
```python
class Calculable(Protocol):
```

**Методы:**
- `calculate_total() -> Decimal` - Расчет общей стоимости

##### `Reservable` (Protocol)
```python
class Reservable(Protocol):
```

**Методы:**
- `reserve(user_id: str, start_date: datetime, end_date: datetime) -> bool` - Резервирование
- `cancel_reservation(reservation_id: str) -> bool` - Отмена резервирования

##### `Payable` (Protocol)
```python
class Payable(Protocol):
```

**Методы:**
- `process_payment(amount: Decimal, payment_method: str) -> bool` - Обработка платежа
- `get_payment_status() -> str` - Получение статуса оплаты

### 2. Люди в Системе

#### `BasePerson`
```python
@dataclass
class BasePerson(BaseEntity):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    date_of_birth: Optional[datetime]
    gender: Gender
    address: Optional[str]
    contact_preference: ContactPreference
    is_active: bool
    last_login: Optional[datetime]
    profile_image_url: Optional[str]
```

**Поля:**
- `first_name: str` - Имя
- `last_name: str` - Фамилия
- `email: str` - Email
- `phone: Optional[str]` - Телефон
- `date_of_birth: Optional[datetime]` - Дата рождения
- `gender: Gender` - Пол
- `address: Optional[str]` - Адрес
- `contact_preference: ContactPreference` - Предпочтения контактов

**Методы:**
- `full_name: str` - Полное имя (свойство)
- `age: Optional[int]` - Возраст (свойство)
- `update_last_login() -> None` - Обновление времени последнего входа
- `deactivate_account() -> None` - Деактивация аккаунта
- `activate_account() -> None` - Активация аккаунта
- `update_contact_info(email: Optional[str] = None, phone: Optional[str] = None, address: Optional[str] = None) -> None` - Обновление контактной информации
- `update_personal_info(first_name: Optional[str] = None, last_name: Optional[str] = None, date_of_birth: Optional[datetime] = None, gender: Optional[Gender] = None) -> None` - Обновление личной информации
- `set_contact_preference(preference: ContactPreference) -> None` - Установка предпочтительного способа связи
- `get_preferred_contact_method() -> str` - Получение предпочтительного метода связи
- `to_dict() -> Dict[str, Any]` - Сериализация в словарь
- `from_dict(data: Dict[str, Any]) -> BasePerson` - Десериализация из словаря (classmethod)

#### `Customer` (Клиент)
```python
@dataclass
class Customer(BasePerson):
    loyalty_points: int
    total_spent: Decimal
    rental_count: int
    average_rating: float
    preferred_categories: Set[str]
    payment_methods: List[str]
    is_vip: bool
    referral_code: Optional[str]
    membership_level: str
```

**Поля:**
- `loyalty_points: int` - Количество баллов лояльности
- `total_spent: Decimal` - Общая сумма потраченная на аренду
- `rental_count: int` - Количество совершенных аренд
- `average_rating: float` - Средний рейтинг клиента
- `preferred_categories: Set[str]` - Предпочитаемые категории предметов
- `payment_methods: List[str]` - Сохраненные методы оплаты
- `is_vip: bool` - VIP статус клиента
- `referral_code: Optional[str]` - Реферальный код для приглашения друзей
- `referred_by: Optional[str]` - Кто пригласил этого клиента
- `last_rental_date: Optional[datetime]` - Дата последней аренды
- `membership_level: str` - Уровень членства (standard, premium, vip)

**Методы:**
- `add_rental(amount: Decimal, rating: Optional[float] = None) -> None` - Добавление информации об аренде
- `redeem_loyalty_points(points_to_redeem: int) -> Decimal` - Использование баллов лояльности
- `get_membership_discount() -> Decimal` - Получение скидки по уровню членства
- `add_preferred_category(category: str) -> None` - Добавление предпочтительной категории
- `remove_preferred_category(category: str) -> None` - Удаление предпочтительной категории
- `add_payment_method(payment_method_id: str) -> None` - Добавление метода оплаты
- `remove_payment_method(payment_method_id: str) -> None` - Удаление метода оплаты
- `generate_referral_code() -> str` - Генерация реферального кода
- `apply_referral_bonus(referrer: Customer) -> None` - Применение бонуса за приглашение друга
- `upgrade_membership(new_level: str) -> None` - Обновление уровня членства
- `can_redeem_points(points: int) -> bool` - Проверка возможности использования баллов
- `get_customer_summary() -> Dict[str, Any]` - Получение сводной информации о клиенте
- `to_dict() -> Dict[str, Any]` - Сериализация в словарь
- `from_dict(data: Dict[str, Any]) -> Customer` - Десериализация из словаря (classmethod)

#### `BaseEmployee` (Базовый Сотрудник)
```python
@dataclass
class BaseEmployee(BasePerson):
    employee_id: str
    department: Department
    position: str
    salary: Decimal
    hire_date: Optional[datetime]
    status: EmployeeStatus
    performance_rating: float
    completed_tasks: int
```

**Поля:**
- `employee_id: str` - Внутренний ID сотрудника
- `department: Department` - Отдел сотрудника
- `position: str` - Должность
- `salary: Decimal` - Зарплата
- `hire_date: Optional[datetime]` - Дата приема на работу
- `status: EmployeeStatus` - Статус сотрудника
- `manager_id: Optional[str]` - ID менеджера
- `performance_rating: float` - Рейтинг производительности
- `completed_tasks: int` - Количество выполненных задач
- `location_id: Optional[str]` - ID места работы
- `work_schedule: Optional[str]` - График работы
- `emergency_contact: Optional[str]` - Контакт для экстренных случаев
- `certifications: List[str]` - Сертификаты и квалификации

**Методы:**
- `years_of_service: float` - Стаж работы в годах (свойство)
- `is_manager: bool` - Проверка является ли менеджером (свойство)
- `update_performance_rating(rating: float) -> None` - Обновление рейтинга производительности
- `increment_completed_tasks() -> None` - Увеличение счетчика выполненных задач
- `update_salary(new_salary: Decimal) -> None` - Обновление зарплаты
- `change_department(new_department: Department) -> None` - Смена отдела
- `change_position(new_position: str) -> None` - Смена должности
- `set_manager(manager_id: str) -> None` - Установка менеджера
- `update_work_schedule(schedule: str) -> None` - Обновление графика работы
- `add_certification(certification: str) -> None` - Добавление сертификата
- `remove_certification(certification: str) -> None` - Удаление сертификата
- `update_emergency_contact(contact: str) -> None` - Обновление контакта для экстренных случаев
- `terminate_employment() -> None` - Увольнение сотрудника
- `put_on_leave() -> None` - Отправка сотрудника в отпуск
- `reactivate_employee() -> None` - Возврат сотрудника к работе
- `can_manage_employees() -> bool` - Проверка возможности управления сотрудниками
- `get_employee_summary() -> Dict[str, Any]` - Получение сводной информации о сотруднике
- `to_dict() -> Dict[str, Any]` - Сериализация в словарь
- `from_dict(data: Dict[str, Any]) -> BaseEmployee` - Десериализация из словаря (classmethod)

#### `Manager` (Менеджер)
```python
@dataclass
class Manager(BaseEmployee):
    subordinates: Set[str]
    managed_departments: Set[str]
    budget_limit: Decimal
    approval_limit: Decimal
    team_performance_rating: float
```

**Поля:**
- `subordinates: Set[str]` - Подчиненные
- `managed_departments: Set[str]` - Управляемые отделы
- `budget_limit: Decimal` - Лимит бюджета
- `approval_limit: Decimal` - Лимит одобрения
- `team_performance_rating: float` - Рейтинг производительности команды
- `monthly_goals: List[str]` - Месячные цели
- `achieved_goals: List[str]` - Достигнутые цели

**Методы:**
- `add_subordinate(employee_id: str) -> None` - Добавление подчиненного
- `remove_subordinate(employee_id: str) -> None` - Удаление подчиненного
- `add_managed_department(department: str) -> None` - Добавление управляемого отдела
- `remove_managed_department(department: str) -> None` - Удаление управляемого отдела
- `can_approve_expense(amount: Decimal) -> bool` - Проверка возможности одобрения расходов
- `approve_expense(expense_id: str, amount: Decimal) -> bool` - Одобрение расходов
- `update_budget_limit(new_limit: Decimal) -> None` - Обновление лимита бюджета
- `update_approval_limit(new_limit: Decimal) -> None` - Обновление лимита одобрения
- `update_team_performance_rating(rating: float) -> None` - Обновление рейтинга команды
- `add_monthly_goal(goal: str) -> None` - Добавление месячной цели
- `mark_goal_achieved(goal: str) -> None` - Отметка цели как достигнутой
- `get_management_summary() -> Dict[str, Any]` - Получение сводки управления
- `can_manage_employee(employee_id: str) -> bool` - Проверка возможности управления сотрудником
- `get_subordinates_list() -> List[str]` - Получение списка подчиненных
- `get_managed_departments_list() -> List[str]` - Получение списка управляемых отделов
- `to_dict() -> Dict[str, Any]` - Сериализация в словарь
- `from_dict(data: Dict[str, Any]) -> Manager` - Десериализация из словаря (classmethod)

#### `Administrator` (Администратор)
```python
@dataclass
class Administrator(Manager):
    system_access_level: str
    configurations_changed: int
    users_created: int
    emergency_access_enabled: bool
```

**Поля:**
- `system_access_level: str` - Уровень доступа к системе
- `configurations_changed: int` - Количество измененных конфигураций
- `users_created: int` - Количество созданных пользователей
- `emergency_access_enabled: bool` - Экстренный доступ включен

**Методы:**
- `increment_configurations_changed() -> None` - Увеличение счетчика измененных конфигураций
- `increment_users_created() -> None` - Увеличение счетчика созданных пользователей
- `toggle_emergency_access() -> None` - Переключение экстренного доступа
- `can_access_system_settings() -> bool` - Проверка доступа к настройкам системы
- `can_manage_users() -> bool` - Проверка возможности управления пользователями
- `reset_user_password(user_id: str) -> bool` - Сброс пароля пользователя
- `disable_user_account(user_id: str, reason: str) -> bool` - Отключение учетной записи пользователя
- `enable_user_account(user_id: str) -> bool` - Включение учетной записи пользователя
- `change_system_access_level(new_level: str) -> None` - Изменение уровня доступа к системе
- `perform_system_backup() -> bool` - Выполнение резервного копирования системы
- `get_admin_summary() -> Dict[str, Any]` - Получение сводной информации об администраторе
- `has_emergency_access() -> bool` - Проверка включен ли экстренный доступ
- `to_dict() -> Dict[str, Any]` - Сериализация в словарь
- `from_dict(data: Dict[str, Any]) -> Administrator` - Десериализация из словаря (classmethod)

### 3. Предметы Аренды

#### `BaseItem` (Базовый Предмет)
```python
@dataclass
class BaseItem(BaseEntity, Calculable, Reservable):
    name: str
    description: str
    category: str
    daily_rate: Decimal
    status: ItemStatus
    condition: ItemCondition
    location_id: Optional[str]
    serial_number: Optional[str]
    rental_count: int
    total_revenue: Decimal
```

**Поля:**
- `name: str` - Название предмета
- `description: str` - Описание предмета
- `category: str` - Категория предмета
- `daily_rate: Decimal` - Стоимость аренды за день
- `status: ItemStatus` - Текущий статус предмета
- `condition: ItemCondition` - Состояние предмета
- `location_id: Optional[str]` - ID места хранения
- `serial_number: Optional[str]` - Серийный номер
- `purchase_date: Optional[datetime]` - Дата покупки
- `last_maintenance_date: Optional[datetime]` - Дата последнего обслуживания
- `rental_count: int` - Количество аренд
- `total_revenue: Decimal` - Общий доход от аренды

**Методы:**
- `calculate_total(days: int = 1) -> Decimal` - Расчет стоимости аренды
- `reserve(user_id: str, start_date: datetime, end_date: datetime) -> bool` - Резервирование предмета
- `cancel_reservation(reservation_id: str) -> bool` - Отмена резервирования
- `mark_as_rented() -> None` - Отметка как арендованный
- `mark_as_returned(revenue: Decimal) -> None` - Отметка как возвращенный
- `mark_for_maintenance() -> None` - Отметка как требующий обслуживания
- `mark_as_damaged() -> None` - Отметка как поврежденный
- `mark_as_lost() -> None` - Отметка как утерянный
- `update_condition(new_condition: ItemCondition) -> None` - Обновление состояния
- `is_available_for_rental() -> bool` - Проверка доступности
- `needs_maintenance() -> bool` - Проверка необходимости обслуживания
- `get_age_in_days() -> int` - Возраст предмета в днях
- `to_dict() -> Dict[str, Any]` - Сериализация в словарь
- `from_dict(data: Dict[str, Any]) -> BaseItem` - Десериализация из словаря (classmethod)

#### `BaseEquipment` (Оборудование)
```python
@dataclass
class BaseEquipment(BaseItem):
    equipment_type: EquipmentType
    brand: str
    model: str
    power_source: PowerSource
    battery_life_hours: Optional[float]
    weight_kg: Optional[float]
    technical_specs: Dict[str, Any]
```

**Поля:**
- `equipment_type: EquipmentType` - Тип оборудования
- `brand: str` - Бренд производителя
- `model: str` - Модель оборудования
- `power_source: PowerSource` - Источник питания
- `battery_life_hours: Optional[float]` - Время работы от батареи в часах
- `weight_kg: Optional[float]` - Вес в килограммах
- `dimensions_cm: Optional[str]` - Размеры в сантиметрах (Д x Ш x В)
- `requires_assembly: bool` - Требуется сборка
- `assembly_instructions: Optional[str]` - Инструкции по сборке
- `technical_specs: Dict[str, Any]` - Технические характеристики
- `compatible_accessories: List[str]` - Совместимые аксессуары

**Методы:**
- `requires_power_source() -> bool` - Требуется ли источник питания
- `get_battery_status() -> Optional[str]` - Получение статуса батареи
- `add_technical_spec(key, value)` - Добавление технической характеристики
- `remove_technical_spec(key)` - Удаление технической характеристики
- `add_compatible_accessory(accessory)` - Добавление совместимого аксессуара
- `remove_compatible_accessory(accessory)` - Удаление совместимого аксессуара
- `get_equipment_info() -> Dict` - Получение информации об оборудовании
- `calculate_transport_cost(distance_km) -> Decimal` - Расчет стоимости транспортировки
- `requires_special_transport() -> bool` - Требуется ли специальный транспорт
- `get_maintenance_schedule() -> Dict` - Получение графика обслуживания

#### `Camera` (Камера)
```python
@dataclass
class Camera(BaseEquipment):
    camera_type: CameraType
    sensor_size: SensorSize
    megapixels: float
    max_iso: int
    has_video: bool
    max_video_resolution: Optional[str]
    lens_mount: Optional[str]
```

**Поля:**
- `camera_type: CameraType` - Тип камеры
- `sensor_size: SensorSize` - Размер сенсора
- `megapixels: float` - Мегапиксели
- `max_iso: int` - Максимальный ISO
- `has_video: bool` - Поддержка видео

**Методы:**
- `supports_4k_video() -> bool` - Поддержка 4K
- `requires_lens() -> bool` - Требуется ли объектив
- `is_professional_grade() -> bool` - Профессиональный уровень
- `estimate_storage_needs(recording_time) -> Dict` - Расчет хранилища

#### `Drone` (Дрон)
```python
@dataclass
class Drone(BaseEquipment):
    drone_category: DroneCategory
    max_flight_time_minutes: int
    max_altitude_meters: int
    max_speed_kmh: int
    camera_resolution: Optional[str]
    gps_enabled: bool
```

**Поля:**
- `drone_category: DroneCategory` - Категория дрона
- `max_flight_time_minutes: int` - Время полета
- `max_altitude_meters: int` - Максимальная высота
- `max_speed_kmh: int` - Максимальная скорость

**Методы:**
- `can_fly_in_weather(wind, visibility) -> bool` - Проверка погоды
- `calculate_flight_range() -> Dict` - Расчет дальности
- `requires_pilot_license() -> bool` - Требуется ли лицензия
- `estimate_battery_usage(flight_time) -> Dict` - Расчет батареи

#### `SportEquipment` (Спортивное Оборудование)
```python
@dataclass
class SportEquipment(BaseEquipment):
    sport_type: SportType
    skill_level: str
    age_range: str
    max_weight_kg: Optional[float]
    requires_supervision: bool
    safety_rating: int
    maintenance_interval_hours: int
```

**Поля:**
- `sport_type: SportType` - Тип спорта
- `skill_level: str` - Уровень сложности (beginner, intermediate, advanced)
- `age_range: str` - Возрастной диапазон
- `max_weight_kg: Optional[float]` - Максимальный вес пользователя
- `requires_supervision: bool` - Требуется ли надзор
- `safety_rating: int` - Рейтинг безопасности (1-5)

**Методы:**
- `is_suitable_for_user(user_age, user_weight, user_skill) -> bool` - Проверка подходящности
- `get_sport_equipment_info() -> Dict` - Информация об оборудовании

#### `BaseTool` (Инструмент)
```python
@dataclass
class BaseTool(BaseItem):
    tool_type: ToolType
    material: MaterialType
    weight_grams: Optional[int]
    requires_power: bool
    power_rating_watts: Optional[int]
    safety_features: List[str]
```

**Поля:**
- `tool_type: ToolType` - Тип инструмента
- `material: MaterialType` - Материал
- `requires_power: bool` - Требуется ли питание
- `safety_features: List[str]` - Функции безопасности

**Методы:**
- `is_power_tool() -> bool` - Электроинструмент ли
- `requires_training() -> bool` - Требуется ли обучение
- `get_power_requirements() -> Optional[Dict]` - Требования к питанию

#### `HandTool` (Ручной Инструмент)
```python
@dataclass
class HandTool(BaseTool):
    grip_type: str
    blade_material: Optional[str]
    handle_material: Optional[str]
    adjustable: bool
```

**Методы:**
- `get_tool_specs() -> Dict` - Спецификации инструмента

#### `PowerTool` (Электроинструмент)
```python
@dataclass
class PowerTool(BaseTool):
    voltage: int
    motor_type: str
    rpm: Optional[int]
    battery_type: Optional[str]
    charging_time_hours: Optional[float]
```

**Методы:**
- `get_power_specs() -> Dict` - Спецификации питания

#### `BaseVehicle` (Транспорт)
```python
@dataclass
class BaseVehicle(BaseItem):
    vehicle_type: VehicleType
    fuel_type: FuelType
    fuel_capacity_liters: Optional[float]
    fuel_efficiency_kml: Optional[float]
    max_speed_kmh: int
    passenger_capacity: int
    license_required: bool
```

**Поля:**
- `vehicle_type: VehicleType` - Тип транспорта
- `fuel_type: FuelType` - Тип топлива
- `passenger_capacity: int` - Вместимость пассажиров
- `license_required: bool` - Требуется ли лицензия

**Методы:**
- `requires_drivers_license() -> bool` - Требуется ли права
- `calculate_fuel_cost(distance, fuel_price) -> float` - Расчет топлива

#### `Car` (Автомобиль)
```python
@dataclass
class Car(BaseVehicle):
    transmission: str
    drive_type: str
    engine_size: Optional[float]
    doors_count: int
    has_gps: bool
    has_ac: bool
```

**Методы:**
- `get_car_specs() -> Dict` - Спецификации автомобиля

#### `Bicycle` (Велосипед)
```python
@dataclass
class Bicycle(BaseVehicle):
    frame_size: str
    gear_count: int
    has_basket: bool
    has_lights: bool
    tire_size: str
    brake_type: str
```

**Методы:**
- `get_bike_specs() -> Dict` - Спецификации велосипеда

#### `Motorcycle` (Мотоцикл)
```python
@dataclass
class Motorcycle(BaseVehicle):
    engine_cc: int
    has_sidecar: bool
    helmet_required: bool
    bike_type: str
```

**Поля:**
- `engine_cc: int` - Объем двигателя в куб.см
- `has_sidecar: bool` - Есть ли коляска
- `helmet_required: bool` - Требуется ли шлем
- `bike_type: str` - Тип мотоцикла

**Методы:**
- `get_motorcycle_specs() -> Dict` - Спецификации мотоцикла

#### `Scooter` (Скутер)
```python
@dataclass
class Scooter(BaseVehicle):
    engine_cc: int
    foldable: bool
    max_load_kg: float
    battery_range_km: Optional[float]
```

**Поля:**
- `engine_cc: int` - Объем двигателя в куб.см
- `foldable: bool` - Складной
- `max_load_kg: float` - Максимальная нагрузка
- `battery_range_km: Optional[float]` - Запас хода на батарее

**Методы:**
- `get_scooter_specs() -> Dict` - Спецификации скутера

#### `ClothingItem` (Одежда)
```python
@dataclass
class ClothingItem(BaseItem):
    clothing_type: ClothingType
    size: ClothingSize
    color: str
    material: str
    gender: str
    season: str
    waterproof: bool
    brand: str
    style: str
```

**Поля:**
- `clothing_type: ClothingType` - Тип одежды
- `size: ClothingSize` - Размер
- `color: str` - Цвет
- `material: str` - Материал
- `waterproof: bool` - Водонепроницаемость

**Методы:**
- `is_suitable_for_weather(temp, rain) -> bool` - Подходит ли погода
- `get_clothing_specs() -> Dict` - Спецификации одежды

### 4. Платежи

#### `BasePayment` (Базовый Платеж)
```python
@dataclass
class BasePayment(BaseEntity, Payable):
    amount: Decimal
    currency: str
    payment_method: PaymentMethod
    status: PaymentStatus
    transaction_id: Optional[str]
    fees: Decimal
    refund_amount: Decimal
```

**Поля:**
- `amount: Decimal` - Сумма платежа
- `currency: str` - Валюта
- `payment_method: PaymentMethod` - Метод оплаты
- `status: PaymentStatus` - Статус платежа
- `transaction_id: Optional[str]` - ID транзакции
- `payment_date: Optional[datetime]` - Дата платежа
- `description: Optional[str]` - Описание платежа
- `customer_id: Optional[str]` - ID клиента
- `rental_id: Optional[str]` - ID аренды
- `fees: Decimal` - Сборы и комиссии
- `refund_amount: Decimal` - Сумма возврата
- `refund_reason: Optional[str]` - Причина возврата

**Методы:**
- `process_payment(amount: Decimal, payment_method: str) -> bool` - Обработка платежа
- `get_payment_status() -> str` - Получение статуса оплаты
- `calculate_total_amount() -> Decimal` - Расчет общей суммы с учетом сборов
- `refund_payment(amount: Decimal, reason: str) -> bool` - Возврат платежа
- `cancel_payment() -> None` - Отмена платежа
- `get_payment_summary() -> Dict[str, Any]` - Получение сводки платежа
- `to_dict() -> Dict[str, Any]` - Сериализация в словарь
- `from_dict(data: Dict[str, Any]) -> BasePayment` - Десериализация из словаря (classmethod)

#### `CashPayment` (Оплата Наличными)
```python
@dataclass
class CashPayment(BasePayment):
    received_amount: float
    change_amount: float
    received_by: Optional[str]
    payment_location: Optional[str]
```

**Методы:**
- `get_cash_details() -> Dict` - Детали оплаты наличными

#### `CreditCardPayment` (Оплата Картой)
```python
@dataclass
class CreditCardPayment(BasePayment):
    card_number_masked: Optional[str]
    card_holder_name: Optional[str]
    expiry_month: Optional[int]
    expiry_year: Optional[int]
    authorization_code: Optional[str]
```

**Методы:**
- `mask_card_number(full_number) -> str` - Маскировка номера
- `validate_card() -> bool` - Валидация карты

#### `WalletPayment` (Оплата Кошельком)
```python
@dataclass
class WalletPayment(BasePayment):
    wallet_id: Optional[str]
    wallet_provider: str
    user_wallet_balance: float
    transaction_fee: float
```

**Методы:**
- `check_sufficient_balance() -> bool` - Проверка баланса
- `deduct_from_wallet() -> bool` - Списание с кошелька

### 5. Аренда и Резервы

#### `Reservation` (Резервирование)
```python
@dataclass
class Reservation(BaseEntity):
    customer_id: str
    item_id: str
    start_date: datetime
    end_date: datetime
    status: str
    total_cost: float
    deposit_amount: float
    confirmed_at: Optional[datetime]
```

**Поля:**
- `customer_id: str` - ID клиента
- `item_id: str` - ID предмета
- `start_date: datetime` - Дата начала резерва
- `end_date: datetime` - Дата окончания резерва
- `status: str` - Статус резерва (pending, confirmed, cancelled, expired)
- `total_cost: float` - Общая стоимость
- `deposit_amount: float` - Сумма залога
- `special_requests: Optional[str]` - Особые запросы
- `confirmed_at: Optional[datetime]` - Время подтверждения
- `expires_at: Optional[datetime]` - Время истечения резерва

**Методы:**
- `confirm_reservation() -> None` - Подтверждение резервирования
- `cancel_reservation() -> None` - Отмена резервирования
- `expire_reservation() -> None` - Истечение резервирования
- `is_active() -> bool` - Проверка активности резервирования
- `get_duration_days() -> int` - Получение длительности резервирования в днях
- `to_dict() -> Dict[str, Any]` - Сериализация в словарь

### 6. Сервисы

#### `AuthService` (Аутентификация)
```python
@dataclass
class AuthService(BaseService):
    session_timeout_minutes: int
    max_login_attempts: int
```

**Поля:**
- `user_repository: Optional[Any]` - Репозиторий пользователей
- `session_timeout_minutes: int` - Таймаут сессии в минутах
- `max_login_attempts: int` - Максимальное количество попыток входа

**Методы:**
- `authenticate_user(email: str, password: str) -> Tuple[bool, Optional[Any], str]` - Аутентификация пользователя
- `authorize_action(user: Any, required_role: str, action: str) -> bool` - Проверка прав пользователя
- `create_session(user: Any) -> str` - Создание сессии для пользователя
- `validate_session(session_id: str) -> Optional[Any]` - Валидация сессии
- `logout_user(user: Any) -> None` - Выход пользователя из системы
- `register_customer(customer_data: Dict[str, Any]) -> Customer` - Регистрация нового клиента
- `change_password(user: Any, old_password: str, new_password: str) -> bool` - Изменение пароля
- `reset_password(email: str) -> str` - Сброс пароля пользователя

#### `RentalService` (Аренда)
```python
@dataclass
class RentalService(BaseService):
    item_repository: Optional[Any]
    customer_repository: Optional[Any]
    payment_service: Optional[Any]
```

**Поля:**
- `item_repository: Optional[Any]` - Репозиторий предметов
- `customer_repository: Optional[Any]` - Репозиторий клиентов
- `payment_service: Optional[Any]` - Сервис платежей

**Методы:**
- `create_reservation(customer_id: str, item_id: str, start_date: datetime, end_date: datetime) -> Reservation` - Создание резервирования
- `start_rental(reservation_id: str) -> None` - Начало аренды на основе резервирования
- `end_rental(rental_id: str, return_condition: str) -> Decimal` - Завершение аренды
- `calculate_rental_cost(item_id: str, start_date: datetime, end_date: datetime, customer_id: Optional[str] = None) -> Dict[str, Any]` - Расчет стоимости аренды
- `get_available_items(category: Optional[str] = None, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> List[BaseItem]` - Получение доступных предметов

## Ассоциации Классов (30+ примеров)

### 1. Наследование (is-a) - 23 ассоциации

**Иерархия людей:**
- `Customer` **is-a** `BasePerson`
- `BaseEmployee` **is-a** `BasePerson`
- `Manager` **is-a** `BaseEmployee`
- `Administrator` **is-a** `Manager`

**Иерархия предметов:**
- `BaseItem` **is-a** `BaseEntity`
- `BaseEquipment` **is-a** `BaseItem`
- `Camera` **is-a** `BaseEquipment`
- `Drone` **is-a** `BaseEquipment`
- `SportEquipment` **is-a** `BaseEquipment`
- `BaseTool` **is-a** `BaseItem`
- `HandTool` **is-a** `BaseTool`
- `PowerTool` **is-a** `BaseTool`
- `BaseVehicle` **is-a** `BaseItem`
- `Car` **is-a** `BaseVehicle`
- `Bicycle` **is-a** `BaseVehicle`
- `Motorcycle` **is-a** `BaseVehicle`
- `Scooter` **is-a** `BaseVehicle`
- `ClothingItem` **is-a** `BaseItem`

**Иерархия платежей:**
- `BasePayment` **is-a** `BaseEntity`
- `CashPayment` **is-a** `BasePayment`
- `CreditCardPayment` **is-a** `BasePayment`
- `WalletPayment` **is-a** `BasePayment`

**Иерархия аренды:**
- `Reservation` **is-a** `BaseEntity`

**Иерархия исключений:**
- Все исключения **is-a** `RentalSystemException`

### 2. Реализация интерфейсов - 6 ассоциаций

- `BaseEntity` **implements** `Identifiable, Validatable, Serializable`
- `BaseItem` **implements** `Calculable, Reservable`
- `BasePayment` **implements** `Payable`

### 3. Композиция через ID (слабая связь) - 10 ассоциаций

- `Reservation.customer_id` → `Customer.entity_id` (Many-to-One)
- `Reservation.item_id` → `BaseItem.entity_id` (Many-to-One)
- `BasePayment.customer_id` → `Customer.entity_id` (Many-to-One)
- `BasePayment.rental_id` → `Reservation.entity_id` (Many-to-One)
- `BaseEmployee.manager_id` → `Manager.employee_id` (Many-to-One)
- `Manager.subordinates` → `BaseEmployee.employee_id` (One-to-Many)
- `Customer.referred_by` → `Customer.entity_id` (Many-to-One, реферальная программа)
- `BaseItem.location_id` → Location (Many-to-One, внешняя сущность)
- `BaseEmployee.location_id` → Location (Many-to-One, внешняя сущность)
- `WalletPayment.wallet_id` → Wallet (Many-to-One, внешняя сущность)

### 4. Композиция (has-a) - 7 ассоциаций

- `Customer` **has** `preferred_categories: Set[str]`
- `Customer` **has** `payment_methods: List[str]`
- `BaseEmployee` **has** `certifications: List[str]`
- `BaseEquipment` **has** `technical_specs: Dict[str, Any]`
- `BaseEquipment` **has** `compatible_accessories: List[str]`
- `BaseTool` **has** `safety_features: List[str]`
- `Manager` **has** `subordinates: Set[str]`

### 5. Агрегация (использование) - 2 ассоциации

- `RentalService` **uses** `item_repository: Repository[BaseItem]`
- `AuthService` **uses** `user_repository: Repository[BasePerson]`

### 6. Зависимости - 3 ассоциации

- `RentalService` **depends on** `AuthService` (для проверки прав)
- `BaseService` **depends on** `Repository[T]` (абстракция)
- Все сервисы **depend on** исключения для обработки ошибок

## Исключения (15 персональных + 1 базовое)

### Базовое исключение
1. `RentalSystemException` - Базовое исключение системы (родитель всех исключений)

### Аутентификация (3)
2. `InvalidCredentialsException` - Неверные учетные данные
3. `AccountLockedException` - Аккаунт заблокирован
4. `InsufficientPermissionsException` - Недостаточно прав

### Инвентарь (3)
5. `ItemNotAvailableException` - Предмет недоступен
6. `ItemAlreadyRentedException` - Предмет уже арендован
7. `InsufficientStockException` - Недостаточно запаса

### Платежи (3)
8. `PaymentFailedException` - Оплата не удалась
9. `InsufficientFundsException` - Недостаточно средств
10. `InvalidCardException` - Недействительная карта

### Аренда (3)
11. `RentalNotFoundException` - Аренда не найдена
12. `InvalidRentalPeriodException` - Недействительный период аренды
13. `OverdueReturnException` - Просрочен возврат

### Прочие (3)
14. `ValidationException` - Ошибка валидации данных
15. `BusinessRuleViolationException` - Нарушение бизнес-правил
16. `SystemUnavailableException` - Система недоступна

## Тестирование

```bash
# Запуск всех тестов
python -m pytest src/tests/test_basic_functionality.py

# С покрытием кода
python -m pytest src/tests/test_basic_functionality.py --cov=src --cov-report=html

# Конкретный тест
python -m pytest src/tests/test_basic_functionality.py::TestCustomer::test_customer_creation -v
```

## Покрытие Кода

- **Тестовое покрытие**: 81%
- **Количество тестов**: 20+ unit и integration тестов
- **Автоматизированное тестирование**: pytest + pytest-cov

## Принципы Проектирования

### SOLID
- **S** - Single Responsibility: Каждый класс имеет одну ответственность
- **O** - Open/Closed: Классы открыты для расширения, закрыты для модификации
- **L** - Liskov Substitution: Подклассы заменяют базовые классы
- **I** - Interface Segregation: Специфические интерфейсы для клиентов
- **D** - Dependency Inversion: Зависимости от абстракций

### DRY, KISS, BDUF
- **DRY**: Don't Repeat Yourself - избегание дублирования
- **KISS**: Keep It Simple Stupid - простота решений
- **BDUF**: Big Design Up Front - тщательное предварительное проектирование

## Документация

Весь код документирован на русском языке с использованием docstrings в формате Doxygen:

```python
def authenticate_user(self, email: str, password: str) -> Tuple[bool, Optional[Any], str]:
    """
    Аутентифицирует пользователя.

    Args:
        email: Email пользователя
        password: Пароль пользователя

    Returns:
        Tuple[bool, Optional[Any], str]: (успех, пользователь, сообщение)

    Raises:
        InvalidCredentialsException: При неверных учетных данных
    """
```

### Генерация Документации

Проект использует **Doxygen** для автоматической генерации полной HTML-документации из docstrings в коде.

#### Требования

- **Doxygen** 1.9.8+ (для поддержки Python)
- **Graphviz** (для диаграмм наследования)

#### Установка зависимостей

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install doxygen graphviz

# macOS
brew install doxygen graphviz

# Windows - скачать с официального сайта
# https://www.doxygen.nl/download.html
```

#### Генерация документации

```bash
# Из корневой директории проекта
doxygen

# Или явно указать конфигурационный файл
doxygen Doxyfile
```

#### Просмотр документации

После генерации откройте файл:
```
docs/doxygen/html/index.html
```

Документация включает:
- Полное описание всех классов и методов
- Диаграммы наследования (inheritance graphs)
- Диаграммы зависимостей (collaboration diagrams)
- Поиск по документации
- Навигация по модулям и пакетам

## Требования

- Python 3.8+
- pytest 9.0.2
- pytest-cov 7.0.0
- coverage 7.13.1
- dataclasses 0.6
- typing-extensions 4.15.0

Все зависимости указаны в файле `requirements.txt`. Для установки выполните:
```bash
pip install -r requirements.txt
```

## Статистика Проекта

- **Всего классов**: 81 (35 основных, 20 Enum, 10 Protocol/Interface, 16 исключений)
- **Всего методов**: 349 (методы экземпляров, класс-методы, статические методы, свойства)
- **Ассоциации между классами**: 30+
- **Исключений**: 16 (1 базовое + 15 персональных)
- **Тестов**: 20+
- **Покрытие**: 81%

---

## Образовательная Цель

Проект демонстрирует применение принципов объектно-ориентированного программирования:

- Инкапсуляция данных и поведения
- Наследование и полиморфизм
- Композиция и агрегация
- Абстракция и интерфейсы
- Обработка исключений
- Unit и интеграционное тестирование
- Принципы SOLID и другие best practices
