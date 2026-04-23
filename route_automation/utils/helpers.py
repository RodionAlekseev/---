import csv
import json
from typing import List, Dict, Any
from datetime import datetime
import re

def format_time(hours: float) -> str:
    """Форматирование времени в часы и минуты"""
    h = int(hours)
    m = int((hours - h) * 60)
    if h > 0:
        return f"{h} ч {m} мин"
    return f"{m} мин"

def generate_route_number(product_code: str) -> str:
    """Генерация номера маршрутного листа"""
    date_str = datetime.now().strftime("%Y%m%d")
    time_str = datetime.now().strftime("%H%M%S")
    return f"RL-{product_code}-{date_str}-{time_str}"

def validate_product_code(code: str) -> bool:
    """Валидация кода изделия"""
    pattern = r'^[A-Z0-9]{3,10}-[0-9]{3}$'
    return bool(re.match(pattern, code))

def export_to_csv(route_data: Dict, filename: str = None) -> str:
    """Экспорт маршрутного листа в CSV"""
    if filename is None:
        filename = f"route_{route_data.get('product_code', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')
        
        # Заголовок
        writer.writerow(['МАРШРУТНЫЙ ЛИСТ'])
        writer.writerow([f'Изделие: {route_data.get("product_code")} - {route_data.get("product_name")}'])
        writer.writerow([f'Дата: {route_data.get("created_at", datetime.now().isoformat())}'])
        writer.writerow([])
        
        # Шапка таблицы операций
        writer.writerow(['№', 'Операция', 'Цех', 'Оборудование', 'Норма времени, ч', 
                        'Факт. время, ч', 'Подготовка, ч', 'Кол-во', 'Итого, ч'])
        
        # Операции
        for op in route_data.get('operations', []):
            writer.writerow([
                op.get('sequence', ''),
                op.get('operation_name', ''),
                op.get('workshop', ''),
                op.get('equipment', ''),
                op.get('standard_time', ''),
                op.get('actual_time', ''),
                op.get('setup_time', ''),
                op.get('quantity', ''),
                op.get('total_time', '')
            ])
        
        writer.writerow([])
        writer.writerow(['ИТОГО ВРЕМЕНИ:', '', '', '', '', '', '', '', route_data.get('total_time', 0)])
        
        # Последовательность цехов
        writer.writerow([])
        writer.writerow(['ПОСЛЕДОВАТЕЛЬНОСТЬ ЦЕХОВ:'])
        workshops = route_data.get('workshops_sequence', [])
        for i, workshop in enumerate(workshops, 1):
            writer.writerow([f'{i}. {workshop}'])
        
        # Загрузка оборудования
        writer.writerow([])
        writer.writerow(['ЗАГРУЗКА ОБОРУДОВАНИЯ:'])
        writer.writerow(['Оборудование', 'Время, ч'])
        for equip, hours in route_data.get('equipment_load', {}).items():
            writer.writerow([equip, hours])
    
    return filename

def export_to_json(route_data: Dict, filename: str = None) -> str:
    """Экспорт маршрутного листа в JSON"""
    if filename is None:
        filename = f"route_{route_data.get('product_code', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(route_data, f, ensure_ascii=False, indent=2)
    
    return filename

def calculate_production_schedule(route_data: Dict, start_date: datetime) -> List[Dict]:
    """Расчет графика производства"""
    schedule = []
    current_date = start_date
    current_shift = 1
    
    for op in route_data.get('operations', []):
        operation_time = op.get('total_time', 0)
        
        schedule.append({
            'operation': op.get('operation_name'),
            'workshop': op.get('workshop'),
            'start_date': current_date.strftime('%Y-%m-%d'),
            'start_shift': current_shift,
            'duration_hours': operation_time,
            'end_date': current_date.strftime('%Y-%m-%d'),
            'end_shift': current_shift
        })
        
        # Простое добавление времени (без учета смен)
        # В реальной системе нужна сложная логика
    
    return schedule