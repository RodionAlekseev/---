import os
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SPECIFICATIONS_DIR = DATA_DIR / "specifications"
REPORTS_DIR = DATA_DIR / "reports"

# Создаем директории если их нет
for dir_path in [DATA_DIR, SPECIFICATIONS_DIR, REPORTS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Настройки БД
DATABASE_PATH = BASE_DIR / "production.db"

# Производственные параметры
WORK_HOURS_PER_DAY = 8
WORK_DAYS_PER_WEEK = 5
SHIFT_START_HOUR = 8
SHIFT_END_HOUR = 17
BREAK_HOURS = 1.0

# Коэффициенты времени
TIME_COEFFICIENTS = {
    'preparation': 0.15,
    'finalization': 0.10,
    'transport': 0.05,
    'quality_control': 0.08,
    'waiting': 0.12
}

# Приоритеты заказов
ORDER_PRIORITIES = {
    'urgent': 1,
    'high': 2,
    'normal': 3,
    'low': 4
}

# Статусы заказов
ORDER_STATUSES = {
    'planned': 'Запланирован',
    'in_progress': 'В работе',
    'quality_check': 'Контроль качества',
    'completed': 'Завершен',
    'cancelled': 'Отменен'
}

# Форматы экспорта
EXPORT_FORMATS = ['csv', 'json', 'excel', 'pdf']

# Логирование
LOG_LEVEL = 'INFO'
LOG_FILE = BASE_DIR / 'logs' / 'route_automation.log'

# Настройки отображения
DECIMAL_PLACES = 2
DATE_FORMAT = '%d.%m.%Y'
DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'

def get_config():
    """Получить конфигурацию в виде словаря"""
    return {
        'work_hours_per_day': WORK_HOURS_PER_DAY,
        'work_days_per_week': WORK_DAYS_PER_WEEK,
        'time_coefficients': TIME_COEFFICIENTS,
        'export_formats': EXPORT_FORMATS,
        'decimal_places': DECIMAL_PLACES
    }