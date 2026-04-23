import sqlite3
import json
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "production.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для работы с БД"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def init_database(self):
        """Инициализация базы данных из schema.sql"""
        schema_path = Path(__file__).parent / "schema.sql"
        if schema_path.exists():
            try:
                with self.get_connection() as conn:
                    with open(schema_path, 'r', encoding='utf-8') as f:
                        conn.executescript(f.read())
                logger.info("Database initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize database: {e}")
        else:
            logger.warning(f"Schema file not found: {schema_path}")
    
    # Работа с цехами
    def get_all_workshops(self) -> List[Dict]:
        """Получить список всех цехов"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM workshops ORDER BY code")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_workshop_by_code(self, code: str) -> Optional[Dict]:
        """Получить цех по коду"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM workshops WHERE code = ?", (code,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    # Работа с операциями
    def get_all_operations(self) -> List[Dict]:
        """Получить список всех операций"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT o.*, w.name as workshop_name, e.name as equipment_name
                FROM operations o
                LEFT JOIN workshops w ON o.workshop_id = w.id
                LEFT JOIN equipment e ON o.equipment_id = e.id
                ORDER BY o.code
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_operation_by_code(self, code: str) -> Optional[Dict]:
        """Получить операцию по коду"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT o.*, w.name as workshop_name, e.name as equipment_name
                FROM operations o
                LEFT JOIN workshops w ON o.workshop_id = w.id
                LEFT JOIN equipment e ON o.equipment_id = e.id
                WHERE o.code = ?
            """, (code,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def add_operation(self, operation_data: Dict) -> int:
        """Добавить новую операцию"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO operations (code, name, description, default_time, setup_time, 
                                       time_unit, equipment_id, workshop_id, requires_quality_check)
                VALUES (:code, :name, :description, :default_time, :setup_time,
                       :time_unit, :equipment_id, :workshop_id, :requires_quality_check)
            """, operation_data)
            return cursor.lastrowid
    
    # Работа с маршрутами
    def get_route_for_product(self, product_code: str) -> Optional[Dict]:
        """Получить сохраненный маршрут для изделия"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM product_routes 
                WHERE product_code = ? AND is_active = 1
                ORDER BY version DESC LIMIT 1
            """, (product_code,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'product_code': row['product_code'],
                    'product_name': row['product_name'],
                    'operations': json.loads(row['operation_sequence']) if row['operation_sequence'] else [],
                    'total_time': row['total_time'],
                    'version': row['version']
                }
            return None
    
    def save_route(self, product_code: str, product_name: str, 
                   operations: List[Dict], total_time: float) -> int:
        """Сохранить рассчитанный маршрут"""
        with self.get_connection() as conn:
            # Получаем текущую версию
            cursor = conn.execute(
                "SELECT MAX(version) as max_version FROM product_routes WHERE product_code = ?",
                (product_code,)
            )
            row = cursor.fetchone()
            new_version = (row['max_version'] or 0) + 1
            
            # Деактивируем старую версию
            conn.execute(
                "UPDATE product_routes SET is_active = 0 WHERE product_code = ?",
                (product_code,)
            )
            
            # Сохраняем новую версию
            cursor = conn.execute("""
                INSERT INTO product_routes 
                (product_code, product_name, operation_sequence, total_time, version, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (product_code, product_name, json.dumps(operations, ensure_ascii=False), 
                  total_time, new_version))
            
            return cursor.lastrowid
    
    # Работа со спецификациями
    def get_specification(self, product_code: str) -> List[Dict]:
        """Получить спецификацию изделия"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT s.*, o.code as operation_code, o.name as operation_name,
                       o.default_time, o.setup_time
                FROM specifications s
                LEFT JOIN operations o ON s.operation_id = o.id
                WHERE s.product_code = ?
                ORDER BY s.priority
            """, (product_code,))
            return [dict(row) for row in cursor.fetchall()]
    
    def add_specification_item(self, spec_data: Dict) -> int:
        """Добавить элемент в спецификацию"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO specifications 
                (product_code, component_code, component_name, quantity, unit, 
                 operation_id, time_coefficient, priority)
                VALUES (:product_code, :component_code, :component_name, :quantity, 
                       :unit, :operation_id, :time_coefficient, :priority)
            """, spec_data)
            return cursor.lastrowid
    
    # Работа с заказами
    def create_production_order(self, order_number: str, product_code: str, 
                                 quantity: int, deadline: str = None) -> int:
        """Создать производственный заказ"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO production_orders (order_number, product_code, quantity, deadline)
                VALUES (?, ?, ?, ?)
            """, (order_number, product_code, quantity, deadline))
            return cursor.lastrowid
    
    def get_production_orders(self, status: str = None) -> List[Dict]:
        """Получить список заказов"""
        with self.get_connection() as conn:
            if status:
                cursor = conn.execute(
                    "SELECT * FROM production_orders WHERE status = ? ORDER BY created_at DESC",
                    (status,)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM production_orders ORDER BY created_at DESC"
                )
            return [dict(row) for row in cursor.fetchall()]
    
    def update_order_status(self, order_id: int, status: str) -> bool:
        """Обновить статус заказа"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "UPDATE production_orders SET status = ? WHERE id = ?",
                (status, order_id)
            )
            return cursor.rowcount > 0
    
    # Логирование маршрутов
    def log_route(self, order_id: int, product_code: str, route_data: Dict, created_by: str = "system"):
        """Сохранить сгенерированный маршрут в лог"""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO route_logs (order_id, product_code, route_data, total_time, created_by)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, product_code, json.dumps(route_data, ensure_ascii=False),
                  route_data.get('total_time', 0), created_by))
            return cursor.lastrowid