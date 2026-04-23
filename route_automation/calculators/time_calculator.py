from typing import List, Dict, Any
from models.route import Route
import logging

logger = logging.getLogger(__name__)

class TimeCalculator:
    """Калькулятор времени операций"""
    
    def __init__(self):
        self.coefficients = {
            'preparation': 0.15,     # 15% на подготовку
            'finalization': 0.10,    # 10% на завершающие операции
            'transport': 0.05,       # 5% на транспортировку
            'quality_control': 0.08  # 8% на контроль качества
        }
    
    def calculate_operation_time(self, base_time: float, 
                                  quantity: int = 1,
                                  coefficient: float = 1.0,
                                  include_setup: bool = True,
                                  setup_time: float = 0.0) -> float:
        """Рассчитать время операции"""
        time_with_coefficient = base_time * coefficient
        if include_setup:
            time_with_coefficient += setup_time
        return time_with_coefficient * quantity
    
    def calculate_route_time(self, route: Route) -> float:
        """Рассчитать общее время маршрута"""
        return route.get_total_time()
    
    def calculate_production_time(self, route: Route, 
                                    work_hours_per_day: float = 8.0) -> Dict[str, Any]:
        """Рассчитать производственное время в днях/сменах"""
        total_hours = route.get_total_time()
        
        return {
            'total_hours': total_hours,
            'work_days': round(total_hours / work_hours_per_day, 1),
            'shifts': round(total_hours / work_hours_per_day, 1),
            'calendar_days': round(total_hours / work_hours_per_day * 1.2, 1)  # с учетом выходных
        }
    
    def calculate_equipment_load(self, route: Route, 
                                  shift_hours: float = 8.0) -> Dict[str, float]:
        """Рассчитать загрузку оборудования в сменах"""
        equipment_load = route.get_equipment_load()
        
        result = {}
        for equipment, hours in equipment_load.items():
            result[equipment] = {
                'hours': hours,
                'shifts': round(hours / shift_hours, 2),
                'utilization': round(hours / shift_hours * 100, 1) if hours <= shift_hours else 100.0
            }
        
        return result
    
    def calculate_bottlenecks(self, route: Route, 
                               shift_hours: float = 8.0) -> List[Dict[str, Any]]:
        """Определить узкие места в производстве"""
        equipment_load = self.calculate_equipment_load(route, shift_hours)
        
        bottlenecks = []
        for equipment, load_data in equipment_load.items():
            if load_data['shifts'] > 1.0:  # Загрузка более одной смены
                bottlenecks.append({
                    'equipment': equipment,
                    'required_shifts': load_data['shifts'],
                    'severity': 'high' if load_data['shifts'] > 2 else 'medium'
                })
        
        return bottlenecks
    
    def apply_coefficients(self, base_time: float, 
                            coefficients: Dict[str, float] = None) -> float:
        """Применить нормативные коэффициенты ко времени"""
        if coefficients is None:
            coefficients = self.coefficients
        
        total_coefficient = 1 + sum(coefficients.values())
        return base_time * total_coefficient
    
    def optimize_parallel_operations(self, operations: List[Dict]) -> float:
        """Оптимизация времени при параллельном выполнении"""
        if not operations:
            return 0
        
        # Группировка операций, которые могут выполняться параллельно
        # (например, в разных цехах)
        workshops = {}
        for op in operations:
            workshop = op.get('workshop', 'unknown')
            if workshop not in workshops:
                workshops[workshop] = 0
            workshops[workshop] += op.get('actual_time', 0) * op.get('quantity', 1)
        
        # Время определяется самым загруженным цехом
        return max(workshops.values()) if workshops else 0