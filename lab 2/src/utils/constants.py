"""
Константы и конфигурационные значения для системы аренды.

Этот модуль содержит все постоянные значения, используемые в приложении,
чтобы избежать магических чисел и жестко закодированных значений.
"""

from decimal import Decimal


# Конфигурация системы
DEFAULT_CURRENCY = "USD"
SYSTEM_TIMEZONE = "UTC"

# Конфигурация аренды
MINIMUM_RENTAL_DURATION_HOURS = 1
MAXIMUM_RENTAL_DURATION_DAYS = 30
DEFAULT_RENTAL_DURATION_HOURS = 24

# Конфигурация ценообразования
BASE_RENTAL_RATE_PER_HOUR = Decimal("5.00")
LATE_RETURN_PENALTY_MULTIPLIER = Decimal("1.5")
DISCOUNT_THRESHOLD_DAYS = 7
DISCOUNT_PERCENTAGE = Decimal("0.10")

# Конфигурация платежей
MINIMUM_PAYMENT_AMOUNT = Decimal("1.00")
MAXIMUM_PAYMENT_AMOUNT = Decimal("10000.00")
PAYMENT_PROCESSING_FEE_PERCENTAGE = Decimal("0.029")  # 2.9%
PAYMENT_PROCESSING_FIXED_FEE = Decimal("0.30")

# Конфигурация инвентаря
MINIMUM_STOCK_LEVEL = 1
LOW_STOCK_THRESHOLD = 5
MAXIMUM_STOCK_LEVEL = 1000

# Конфигурация пользователей
MINIMUM_PASSWORD_LENGTH = 8
MAXIMUM_PASSWORD_LENGTH = 128
MAXIMUM_LOGIN_ATTEMPTS = 5
ACCOUNT_LOCKOUT_DURATION_MINUTES = 30

# Конфигурация уведомлений
EMAIL_NOTIFICATION_DELAY_MINUTES = 15
SMS_NOTIFICATION_DELAY_MINUTES = 5
PUSH_NOTIFICATION_DELAY_MINUTES = 1

# Конфигурация обслуживания
MAINTENANCE_CHECK_INTERVAL_DAYS = 30
MAXIMUM_USAGE_HOURS_BEFORE_MAINTENANCE = 100

# Конфигурация программы лояльности
LOYALTY_POINTS_PER_DOLLAR = 1
LOYALTY_POINTS_REDEMPTION_RATE = Decimal("0.01")  # 1 балл = $0.01
MINIMUM_POINTS_FOR_REDEMPTION = 100

# Конфигурация страхования
BASE_INSURANCE_RATE_PER_DAY = Decimal("2.00")
INSURANCE_DEDUCTIBLE = Decimal("50.00")
MAXIMUM_INSURANCE_COVERAGE = Decimal("1000.00")

# Конфигурация местоположения
DEFAULT_SEARCH_RADIUS_KM = 10
MAXIMUM_SEARCH_RADIUS_KM = 100

# Конфигурация отчетов
DEFAULT_REPORT_PERIOD_DAYS = 30
MAXIMUM_REPORT_PERIOD_DAYS = 365

# Конфигурация API
DEFAULT_PAGE_SIZE = 20
MAXIMUM_PAGE_SIZE = 100
API_REQUEST_TIMEOUT_SECONDS = 30

# Конфигурация валидации
MAXIMUM_STRING_LENGTH = 255
MAXIMUM_TEXT_LENGTH = 1000
MAXIMUM_FILE_SIZE_MB = 10

# Коды статусов
STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"
STATUS_PENDING = "pending"
STATUS_COMPLETED = "completed"
STATUS_CANCELLED = "cancelled"
STATUS_OVERDUE = "overdue"

# Категории предметов
CATEGORY_CLOTHING = "clothing"
CATEGORY_EQUIPMENT = "equipment"
CATEGORY_TOOLS = "tools"
CATEGORY_VEHICLES = "vehicles"

# Типы оборудования
EQUIPMENT_CAMERA = "camera"
EQUIPMENT_DRONE = "drone"
EQUIPMENT_SPORT = "sport_equipment"

# Типы инструментов
TOOL_HAND = "hand_tool"
TOOL_POWER = "power_tool"

# Типы транспортных средств
VEHICLE_BICYCLE = "bicycle"
VEHICLE_CAR = "car"
VEHICLE_MOTORCYCLE = "motorcycle"
VEHICLE_SCOOTER = "scooter"

# Способы оплаты
PAYMENT_CASH = "cash"
PAYMENT_CREDIT_CARD = "credit_card"
PAYMENT_WALLET = "wallet"

# Типы уведомлений
NOTIFICATION_EMAIL = "email"
NOTIFICATION_SMS = "sms"
NOTIFICATION_PUSH = "push"

# Роли пользователей
ROLE_CUSTOMER = "customer"
ROLE_EMPLOYEE = "employee"
ROLE_MANAGER = "manager"
ROLE_ADMINISTRATOR = "administrator"

# Уровни повреждений
DAMAGE_NONE = "none"
DAMAGE_MINOR = "minor"
DAMAGE_MODERATE = "moderate"
DAMAGE_SEVERE = "severe"

# Статусы резервирования
RESERVATION_PENDING = "pending"
RESERVATION_CONFIRMED = "confirmed"
RESERVATION_ACTIVE = "active"
RESERVATION_COMPLETED = "completed"
RESERVATION_CANCELLED = "cancelled"

# Коды ошибок
ERROR_INVALID_INPUT = "INVALID_INPUT"
ERROR_NOT_FOUND = "NOT_FOUND"
ERROR_UNAUTHORIZED = "UNAUTHORIZED"
ERROR_INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
ERROR_ITEM_UNAVAILABLE = "ITEM_UNAVAILABLE"
ERROR_PAYMENT_FAILED = "PAYMENT_FAILED"
