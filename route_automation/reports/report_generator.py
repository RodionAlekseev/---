from typing import List, Dict, Any
from datetime import datetime
from models.route import Route
import json

class ReportGenerator:
    """Генератор отчетов"""
    
    @staticmethod
    def generate_route_report(route: Route) -> str:
        """Сгенерировать текстовый отчет о маршруте"""
        route_dict = route.to_dict()
        
        report = f"""
ОТЧЕТ О МАРШРУТНОМ ЛИСТЕ
{'='*60}

Основная информация:
-------------------
Изделие: {route_dict['product_code']} - {route_dict['product_name']}
Количество: {route_dict['quantity']} шт.
Общее время: {route_dict['total_time']} ч.
Дата создания: {route_dict['created_at']}

Последовательность цехов:
-------------------
{ ' -> '.join(route_dict['workshops_sequence']) }

Детали операций:
-------------------
"""
        for op in route_dict['operations']:
            report += f"""
{op['sequence']}. {op['operation_name']}
   Цех: {op['workshop']}
   Оборудование: {op['equipment'] or 'Не указано'}
   Время: {op['total_time']} ч.
   Контроль качества: {'Да' if op['requires_quality_check'] else 'Нет'}
"""
        
        report += "\nЗагрузка оборудования:\n-------------------\n"
        for equip, hours in route_dict['equipment_load'].items():
            report += f"{equip}: {hours} ч.\n"
        
        return report
    
    @staticmethod
    def generate_summary_report(routes: List[Route]) -> str:
        """Сгенерировать сводный отчет по нескольким маршрутам"""
        total_time = sum(r.get_total_time() for r in routes)
        avg_time = total_time / len(routes) if routes else 0
        
        report = f"""
СВОДНЫЙ ОТЧЕТ ПО МАРШРУТАМ
{'='*60}

Всего маршрутов: {len(routes)}
Общее время: {total_time} ч.
Среднее время: {avg_time:.2f} ч.

Детали по каждому маршруту:
-------------------
"""
        for route in routes:
            report += f"\n{route.product_code} - {route.product_name}: {route.get_total_time()} ч."
        
        return report
    
    @staticmethod
    def generate_equipment_utilization_report(equipment_data: Dict[str, float]) -> str:
        """Отчет по загрузке оборудования"""
        report = f"""
ОТЧЕТ ПО ЗАГРУЗКЕ ОБОРУДОВАНИЯ
{'='*50}

{'Оборудование':<20} {'Время, ч':<10}
{'-'*50}
"""
        for equip, hours in sorted(equipment_data.items(), key=lambda x: x[1], reverse=True):
            report += f"{equip:<20} {hours:<10.2f}\n"
        
        return report