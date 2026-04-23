from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class OperationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"

@dataclass
class RouteOperation:
    """Операция в маршрутном листе"""
    sequence: int
    operation_code: str
    operation_name: str
    workshop: str
    equipment: Optional[str]
    standard_time: float  # норма времени
    actual_time: float    # фактическое время с учетом коэффициентов
    setup_time: float = 0.0
    quantity: int = 1
    status: OperationStatus = OperationStatus.PENDING
    requires_quality_check: bool = False
    
    def get_total_time(self) -> float:
        """Получить общее время операции"""
        return (self.actual_time + self.setup_time) * self.quantity
    
    def to_dict(self) -> Dict:
        return {
            'sequence': self.sequence,
            'operation_code': self.operation_code,
            'operation_name': self.operation_name,
            'workshop': self.workshop,
            'equipment': self.equipment,
            'standard_time': self.standard_time,
            'actual_time': self.actual_time,
            'setup_time': self.setup_time,
            'quantity': self.quantity,
            'total_time': self.get_total_time(),
            'status': self.status.value,
            'requires_quality_check': self.requires_quality_check
        }

@dataclass
class Route:
    """Маршрутный лист"""
    product_code: str
    product_name: str
    operations: List[RouteOperation] = field(default_factory=list)
    order_id: Optional[int] = None
    order_number: Optional[str] = None
    quantity: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    version: int = 1
    
    def add_operation(self, operation: RouteOperation):
        """Добавить операцию в маршрут"""
        operation.sequence = len(self.operations) + 1
        self.operations.append(operation)
    
    def get_total_time(self) -> float:
        """Получить общее время маршрута"""
        return sum(op.get_total_time() for op in self.operations)
    
    def get_workshops_sequence(self) -> List[str]:
        """Получить последовательность цехов"""
        workshops = []
        for op in self.operations:
            if op.workshop not in workshops:
                workshops.append(op.workshop)
        return workshops
    
    def get_equipment_load(self) -> Dict[str, float]:
        """Получить загрузку оборудования"""
        load = {}
        for op in self.operations:
            if op.equipment:
                load[op.equipment] = load.get(op.equipment, 0) + op.get_total_time()
        return load
    
    def update_operation_status(self, sequence: int, status: OperationStatus):
        """Обновить статус операции"""
        for op in self.operations:
            if op.sequence == sequence:
                op.status = status
                break
    
    def is_completed(self) -> bool:
        """Проверка, завершен ли маршрут"""
        return all(op.status == OperationStatus.COMPLETED for op in self.operations)
    
    def to_dict(self) -> Dict:
        """Преобразовать в словарь"""
        return {
            'product_code': self.product_code,
            'product_name': self.product_name,
            'order_id': self.order_id,
            'order_number': self.order_number,
            'quantity': self.quantity,
            'operations': [op.to_dict() for op in self.operations],
            'total_time': self.get_total_time(),
            'workshops_sequence': self.get_workshops_sequence(),
            'equipment_load': self.get_equipment_load(),
            'created_at': self.created_at.isoformat(),
            'version': self.version
        }
    
    def print_route_sheet(self):
        """Вывести маршрутный лист в консоль"""
        print(f"\n{'='*80}")
        print(f"МАРШРУТНЫЙ ЛИСТ")
        print(f"Изделие: {self.product_code} - {self.product_name}")
        if self.order_number:
            print(f"Заказ: {self.order_number}")
        print(f"Количество: {self.quantity} шт")
        print(f"Дата: {self.created_at.strftime('%d.%m.%Y %H:%M')}")
        print(f"{'='*80}\n")
        
        print(f"{'№':<4} {'Операция':<25} {'Цех':<20} {'Оборудование':<20} {'Время, ч':<10}")
        print("-" * 80)
        
        for op in self.operations:
            print(f"{op.sequence:<4} {op.operation_name[:24]:<25} {op.workshop[:19]:<20} "
                  f"{op.equipment[:19] if op.equipment else '-':<20} {op.get_total_time():<10.2f}")
        
        print("-" * 80)
        print(f"{'ИТОГО:':<69} {self.get_total_time():<10.2f}")
        
        if self.get_workshops_sequence():
            print(f"\nПоследовательность цехов: {' -> '.join(self.get_workshops_sequence())}")