from typing import List, Dict, Any, Optional
from database.db_manager import DatabaseManager
from models.product import Product, Component
from models.route import Route, RouteOperation, OperationStatus
import logging

logger = logging.getLogger(__name__)

class RouteCalculator:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def calculate_route_from_product(self, product: Product, quantity: int = 1) -> Route:
        """Рассчитать маршрут на основе модели изделия"""
        
        route = Route(
            product_code=product.code,
            product_name=product.name,
            quantity=quantity
        )
        
        # Собираем все операции из компонентов
        all_operations = []
        
        for component in product.components:
            component_ops = self._get_component_operations(component, quantity)
            all_operations.extend(component_ops)
        
        # Оптимизируем маршрут (группируем по цехам)
        optimized_ops = self._optimize_route(all_operations)
        
        # Добавляем операции в маршрут
        for op_data in optimized_ops:
            route.add_operation(RouteOperation(**op_data))
        
        logger.info(f"Route calculated for product {product.code}, total time: {route.get_total_time()}h")
        
        return route
    
    def calculate_route_from_specification(self, product_code: str, quantity: int = 1) -> Optional[Route]:
        """Рассчитать маршрут на основе спецификации из БД"""
        
        # Получаем спецификацию
        specification = self.db.get_specification(product_code)
        if not specification:
            logger.warning(f"No specification found for product {product_code}")
            return None
        
        # Получаем информацию о продукте
        product_name = self._get_product_name(product_code)
        
        route = Route(
            product_code=product_code,
            product_name=product_name,
            quantity=quantity
        )
        
        all_operations = []
        
        for spec_item in specification:
            # Получаем операцию
            operation = self.db.get_operation_by_code(spec_item['operation_code'])
            if not operation:
                continue
            
            # Создаем операцию для маршрута
            actual_time = operation['default_time'] * spec_item.get('time_coefficient', 1.0)
            
            for _ in range(spec_item.get('quantity', 1)):
                all_operations.append({
                    'operation_code': operation['code'],
                    'operation_name': operation['name'],
                    'workshop': operation['workshop_name'],
                    'equipment': operation['equipment_name'],
                    'standard_time': operation['default_time'],
                    'actual_time': actual_time,
                    'setup_time': operation.get('setup_time', 0),
                    'quantity': quantity,
                    'requires_quality_check': operation.get('requires_quality_check', False)
                })
        
        # Оптимизируем
        optimized_ops = self._optimize_route(all_operations)
        
        for i, op_data in enumerate(optimized_ops, 1):
            op_data['sequence'] = i
            route.add_operation(RouteOperation(**op_data))
        
        return route
    
    def _get_component_operations(self, component: Component, quantity: int) -> List[Dict]:
        """Получить операции для компонента"""
        operations = []
        
        for op_code in component.operations:
            operation = self.db.get_operation_by_code(op_code)
            if operation:
                actual_time = operation['default_time'] * component.time_coefficient
                
                # Умножаем на количество компонентов
                for _ in range(component.quantity):
                    operations.append({
                        'operation_code': operation['code'],
                        'operation_name': operation['name'],
                        'workshop': operation['workshop_name'],
                        'equipment': operation['equipment_name'],
                        'standard_time': operation['default_time'],
                        'actual_time': actual_time,
                        'setup_time': operation.get('setup_time', 0),
                        'quantity': quantity,
                        'requires_quality_check': operation.get('requires_quality_check', False)
                    })
        
        return operations
    
    def _optimize_route(self, operations: List[Dict]) -> List[Dict]:
        """Оптимизация маршрута - группировка по цехам"""
        if not operations:
            return []
        
        # Группируем операции по цехам
        workshops_order = {}
        for op in operations:
            workshop = op['workshop']
            if workshop not in workshops_order:
                workshops_order[workshop] = []
            workshops_order[workshop].append(op)
        
        # Формируем оптимизированный маршрут
        optimized = []
        for workshop, ops in workshops_order.items():
            # Внутри цеха операции можно дополнительно оптимизировать
            optimized.extend(self._optimize_within_workshop(ops))
        
        return optimized
    
    def _optimize_within_workshop(self, operations: List[Dict]) -> List[Dict]:
        """Оптимизация внутри цеха"""
        # Здесь можно добавить логику оптимизации внутри цеха
        # Например, группировка по оборудованию или приоритетам
        return operations
    
    def _get_product_name(self, product_code: str) -> str:
        """Получить название продукта"""
        # В реальной системе здесь был бы запрос к БД
        product_names = {
            'PROD-001': 'Корпусное изделие',
            'PROD-002': 'Электронный блок',
            'PROD-100': 'Сборка финальная'
        }
        return product_names.get(product_code, product_code)