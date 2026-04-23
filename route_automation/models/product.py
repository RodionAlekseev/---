from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class Component:
    """Компонент изделия"""
    code: str
    name: str
    quantity: int = 1
    unit: str = "шт"
    time_coefficient: float = 1.0
    operations: List[str] = field(default_factory=list)

@dataclass
class Product:
    """Модель изделия"""
    code: str
    name: str
    description: Optional[str] = None
    components: List[Component] = field(default_factory=list)
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_component(self, component: Component):
        """Добавить компонент в изделие"""
        self.components.append(component)
    
    def remove_component(self, component_code: str):
        """Удалить компонент из изделия"""
        self.components = [c for c in self.components if c.code != component_code]
    
    def get_component(self, code: str) -> Optional[Component]:
        """Получить компонент по коду"""
        for component in self.components:
            if component.code == code:
                return component
        return None
    
    def get_total_components_count(self) -> int:
        """Получить общее количество компонентов"""
        return sum(c.quantity for c in self.components)
    
    def to_dict(self) -> Dict:
        """Преобразовать в словарь"""
        return {
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'components': [
                {
                    'code': c.code,
                    'name': c.name,
                    'quantity': c.quantity,
                    'unit': c.unit,
                    'time_coefficient': c.time_coefficient,
                    'operations': c.operations
                }
                for c in self.components
            ],
            'version': self.version,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Product':
        """Создать из словаря"""
        components = [
            Component(
                code=c['code'],
                name=c['name'],
                quantity=c.get('quantity', 1),
                unit=c.get('unit', 'шт'),
                time_coefficient=c.get('time_coefficient', 1.0),
                operations=c.get('operations', [])
            )
            for c in data.get('components', [])
        ]
        
        return cls(
            code=data['code'],
            name=data['name'],
            description=data.get('description'),
            components=components,
            version=data.get('version', 1),
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now()
        )