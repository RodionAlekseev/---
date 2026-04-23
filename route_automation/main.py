#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Автоматизация маршрутных листов
Главный модуль приложения
"""

import sys
import json
import logging
import os
from pathlib import Path
from datetime import datetime

# СОЗДАЕМ НЕОБХОДИМЫЕ ПАПКИ
os.makedirs("logs", exist_ok=True)
os.makedirs("data/specifications", exist_ok=True)
os.makedirs("data/reports", exist_ok=True)

from database.db_manager import DatabaseManager
from calculators.route_calculator import RouteCalculator
from calculators.time_calculator import TimeCalculator
from models.product import Product, Component
from models.route import Route, RouteOperation, OperationStatus
from reports.report_generator import ReportGenerator
from utils.helpers import export_to_csv, export_to_json, format_time, generate_route_number


# Настройка конфига (временная)
class Config:
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/route_automation.log'
    DATABASE_PATH = 'production.db'
    SPECIFICATIONS_DIR = Path('data/specifications')
    DATA_DIR = Path('data')
    REPORTS_DIR = Path('data/reports')


config = Config()

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RouteAutomationSystem:
    """Основной класс системы автоматизации маршрутных листов"""

    def __init__(self):
        self.db = DatabaseManager(config.DATABASE_PATH)
        self.route_calculator = RouteCalculator(self.db)
        self.time_calculator = TimeCalculator()
        self.report_generator = ReportGenerator()

    def create_product_from_specification(self, spec_file_path: str) -> Product:
        """Создать изделие из файла спецификации"""
        with open(spec_file_path, 'r', encoding='utf-8') as f:
            spec_data = json.load(f)

        components = []
        for comp_data in spec_data.get('components', []):
            component = Component(
                code=comp_data['code'],
                name=comp_data['name'],
                quantity=comp_data.get('quantity', 1),
                unit=comp_data.get('unit', 'шт'),
                time_coefficient=comp_data.get('time_coefficient', 1.0),
                operations=comp_data.get('operations', [])
            )
            components.append(component)

        product = Product(
            code=spec_data['product_code'],
            name=spec_data['product_name'],
            description=spec_data.get('description'),
            components=components,
            version=spec_data.get('version', 1)
        )

        # Сохраняем спецификацию в БД
        for comp in components:
            for op_code in comp.operations:
                op = self.db.get_operation_by_code(op_code)
                if op:
                    self.db.add_specification_item({
                        'product_code': product.code,
                        'component_code': comp.code,
                        'component_name': comp.name,
                        'quantity': comp.quantity,
                        'unit': comp.unit,
                        'operation_id': op['id'],
                        'time_coefficient': comp.time_coefficient,
                        'priority': 1
                    })

        logger.info(f"Product {product.code} created from specification")
        return product

    def generate_route(self, product_code: str, quantity: int = 1,
                       order_number: str = None) -> Route:
        """Сгенерировать маршрутный лист для изделия"""

        # Пытаемся получить сохраненный маршрут
        saved_route = self.db.get_route_for_product(product_code)

        if saved_route:
            # Восстанавливаем маршрут из БД
            route = Route(
                product_code=product_code,
                product_name=saved_route['product_name'],
                quantity=quantity,
                version=saved_route['version']
            )

            for op_data in saved_route['operations']:
                route.add_operation(RouteOperation(**op_data))

            logger.info(f"Loaded existing route for {product_code} (v{saved_route['version']})")
        else:
            # Рассчитываем новый маршрут
            route = self.route_calculator.calculate_route_from_specification(product_code, quantity)

            if route is None:
                logger.error(f"Cannot generate route for {product_code}")
                return None

            # Сохраняем в БД
            self.db.save_route(
                product_code,
                route.product_name,
                [op.to_dict() for op in route.operations],
                route.get_total_time()
            )

            logger.info(f"Generated new route for {product_code}")

        route.order_number = order_number or generate_route_number(product_code)

        # Логируем генерацию маршрута
        self.db.log_route(None, product_code, route.to_dict())

        return route

    def create_production_order(self, product_code: str, quantity: int,
                                deadline: str = None) -> int:
        """Создать производственный заказ"""
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{product_code}"

        order_id = self.db.create_production_order(
            order_number=order_number,
            product_code=product_code,
            quantity=quantity,
            deadline=deadline
        )

        logger.info(f"Production order created: {order_number}")
        return order_id

    def print_route_sheet(self, route: Route):
        """Вывести маршрутный лист в консоль"""
        route.print_route_sheet()

        # Дополнительная информация по загрузке
        equipment_load = self.time_calculator.calculate_equipment_load(route)
        if equipment_load:
            print(f"\nЗАГРУЗКА ОБОРУДОВАНИЯ:")
            for equip, load in equipment_load.items():
                print(f"  {equip}: {load['hours']:.2f} ч ({load['utilization']:.0f}%)")

        # Узкие места
        bottlenecks = self.time_calculator.calculate_bottlenecks(route)
        if bottlenecks:
            print(f"\nУЗКИЕ МЕСТА:")
            for b in bottlenecks:
                print(f"  {b['equipment']}: требуется {b['required_shifts']:.1f} смен")

        # Производственное время
        prod_time = self.time_calculator.calculate_production_time(route)
        print(f"\nПРОИЗВОДСТВЕННОЕ ВРЕМЯ:")
        print(f"  Всего часов: {prod_time['total_hours']:.2f}")
        print(f"  Рабочих дней: {prod_time['work_days']}")

    def export_route(self, route: Route, format: str = 'csv') -> str:
        """Экспорт маршрутного листа в файл"""
        route_dict = route.to_dict()

        if format == 'csv':
            return export_to_csv(route_dict)
        elif format == 'json':
            return export_to_json(route_dict)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def run_demo(self):
        """Демонстрационный режим работы"""
        print("\n" + "=" * 70)
        print("АВТОМАТИЗАЦИЯ МАРШРУТНЫХ ЛИСТОВ - ДЕМОНСТРАЦИЯ")
        print("=" * 70)

        # 1. Создаем изделие из спецификации
        spec_file = config.SPECIFICATIONS_DIR / "spec_example.json"

        # Создаем пример спецификации если ее нет
        if not spec_file.exists():
            example_spec = {
                "product_code": "PROD-100",
                "product_name": "Сборка финальная",
                "components": [
                    {
                        "code": "COMP-001",
                        "name": "Корпус металлический",
                        "quantity": 1,
                        "operations": ["CUT", "WELD", "PAINT"]
                    },
                    {
                        "code": "COMP-002",
                        "name": "Плата управления",
                        "quantity": 2,
                        "time_coefficient": 1.2,
                        "operations": ["ASSEMBLE", "TEST"]
                    }
                ]
            }
            with open(spec_file, 'w', encoding='utf-8') as f:
                json.dump(example_spec, f, ensure_ascii=False, indent=2)
            print(f"\nСоздан пример спецификации: {spec_file}")

        # 2. Создаем изделие
        print("\n1. Загрузка спецификации...")
        try:
            product = self.create_product_from_specification(str(spec_file))
            print(f"   Изделие: {product.code} - {product.name}")
            print(f"   Компонентов: {len(product.components)}")
        except Exception as e:
            print(f"   Ошибка загрузки спецификации: {e}")
            print("   Продолжаем с демонстрационными данными...")
            product = None

        # 3. Генерируем маршрут
        print("\n2. Расчет маршрута...")
        route = self.generate_route("PROD-100", quantity=10, order_number="DEMO-001")

        if route:
            # 4. Выводим маршрутный лист
            print("\n3. Маршрутный лист:")
            self.print_route_sheet(route)

            # 5. Экспортируем
            print("\n4. Экспорт...")
            csv_file = self.export_route(route, 'csv')
            print(f"   Экспорт в CSV: {csv_file}")

            json_file = self.export_route(route, 'json')
            print(f"   Экспорт в JSON: {json_file}")

            # 6. Генерируем отчет
            print("\n5. Генерация отчета...")
            report = self.report_generator.generate_route_report(route)
            print(report)
        else:
            print("Ошибка: не удалось сгенерировать маршрут")

        print("\n" + "=" * 70)
        print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
        print("=" * 70)


def main():
    """Главная функция"""
    system = RouteAutomationSystem()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'demo':
            system.run_demo()
        elif command == 'generate' and len(sys.argv) > 2:
            product_code = sys.argv[2]
            quantity = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            route = system.generate_route(product_code, quantity)
            if route:
                system.print_route_sheet(route)
        elif command == 'order' and len(sys.argv) > 3:
            product_code = sys.argv[2]
            quantity = int(sys.argv[3])
            order_id = system.create_production_order(product_code, quantity)
            print(f"Создан заказ ID: {order_id}")
        else:
            print("Использование:")
            print("  python main.py demo                 - Демонстрация")
            print("  python main.py generate PROD-100 10 - Генерация маршрута")
            print("  python main.py order PROD-100 5     - Создание заказа")
    else:
        system.run_demo()


if __name__ == "__main__":
    main()