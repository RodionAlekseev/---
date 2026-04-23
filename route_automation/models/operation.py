from dataclasses import dataclass
from typing import Optional

@dataclass
class Operation:
    """Технологическая операция"""
    code: str
    name: str
    description: Optional[str] = None
    default_time: float = 0.0
    setup_time: float = 0.0
    time_unit: str = "hour"
    equipment_id: Optional[int] = None
    equipment_name: Optional[str] = None
    workshop_id: Optional[int] = None
    workshop_name: Optional[str] = None
    requires_quality_check: bool = False
    
    def calculate_time(self, quantity: int = 1, coefficient: float = 1.0) -> float:
        """Рассчитать время выполнения операции"""
        return (self.default_time * coefficient + self.setup_time) * quantity
    
    def to_dict(self) -> dict:
        return {
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'default_time': self.default_time,
            'setup_time': self.setup_time,
            'time_unit': self.time_unit,
            'equipment': self.equipment_name,
            'workshop': self.workshop_name,
            'requires_quality_check': self.requires_quality_check
        }