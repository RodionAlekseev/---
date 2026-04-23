# route_app.py - Исправленная версия

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import threading

# Настройка внешнего вида CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ==================== КЛАССЫ ПРИЛОЖЕНИЯ ====================

class DatabaseManager:
    """Управление базой данных"""

    def __init__(self, db_path="production.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Инициализация БД"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Цеха
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workshops (
                id INTEGER PRIMARY KEY,
                code TEXT UNIQUE,
                name TEXT,
                description TEXT
            )
        ''')

        # Оборудование
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY,
                code TEXT UNIQUE,
                name TEXT,
                workshop_id INTEGER
            )
        ''')

        # Операции
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY,
                code TEXT UNIQUE,
                name TEXT,
                default_time REAL,
                setup_time REAL,
                workshop_id INTEGER,
                equipment_id INTEGER
            )
        ''')

        # Маршруты
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_code TEXT,
                product_name TEXT,
                quantity INTEGER,
                route_data TEXT,
                total_time REAL,
                created_at TIMESTAMP
            )
        ''')

        # Заказы
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number TEXT,
                product_code TEXT,
                quantity INTEGER,
                status TEXT,
                created_at TIMESTAMP
            )
        ''')

        # Заполняем тестовыми данными
        self._insert_test_data(conn)

        conn.commit()
        conn.close()

    def _insert_test_data(self, conn):
        """Тестовые данные"""
        cursor = conn.cursor()

        # Проверяем, есть ли данные
        cursor.execute("SELECT COUNT(*) FROM workshops")
        if cursor.fetchone()[0] == 0:
            # Добавляем цеха
            workshops = [
                (1, 'WS001', 'Заготовительный цех', 'Раскрой и подготовка материалов'),
                (2, 'WS002', 'Механообрабатывающий цех', 'Токарные и фрезерные работы'),
                (3, 'WS003', 'Сварочный цех', 'Сварка и соединение деталей'),
                (4, 'WS004', 'Окрасочный цех', 'Покраска и покрытие'),
                (5, 'WS005', 'Сборочный цех', 'Финальная сборка'),
                (6, 'WS006', 'Контроль качества', 'Проверка и испытания')
            ]
            cursor.executemany("INSERT INTO workshops VALUES (?,?,?,?)", workshops)

            # Добавляем оборудование
            equipment = [
                (1, 'EQ001', 'Лазерный станок', 1),
                (2, 'EQ002', 'Токарный станок', 2),
                (3, 'EQ003', 'Фрезерный станок', 2),
                (4, 'EQ004', 'Сварочный аппарат', 3),
                (5, 'EQ005', 'Окрасочная камера', 4),
                (6, 'EQ006', 'Сборочный стол', 5),
                (7, 'EQ007', 'Испытательный стенд', 6)
            ]
            cursor.executemany("INSERT INTO equipment VALUES (?,?,?,?)", equipment)

            # Добавляем операции
            operations = [
                ('CUT', 'Раскрой материала', 0.5, 0.2, 1, 1),
                ('TURN', 'Токарная обработка', 1.0, 0.3, 2, 2),
                ('MILL', 'Фрезерная обработка', 1.5, 0.3, 2, 3),
                ('WELD', 'Сварка', 0.8, 0.2, 3, 4),
                ('PAINT', 'Покраска', 0.6, 0.4, 4, 5),
                ('ASSEMBLE', 'Сборка', 1.2, 0.1, 5, 6),
                ('TEST', 'Испытания', 0.5, 0.1, 6, 7)
            ]
            cursor.executemany(
                "INSERT INTO operations (code, name, default_time, setup_time, workshop_id, equipment_id) VALUES (?,?,?,?,?,?)",
                operations)

    def get_all_operations(self) -> List[Dict]:
        """Получить все операции"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.*, w.name as workshop_name, e.name as equipment_name
            FROM operations o
            JOIN workshops w ON o.workshop_id = w.id
            LEFT JOIN equipment e ON o.equipment_id = e.id
        ''')
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result

    def get_all_workshops(self) -> List[Dict]:
        """Получить все цеха"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workshops")
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result

    def save_route(self, product_code: str, product_name: str, operations: List, total_time: float):
        """Сохранить маршрут"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        route_data = json.dumps(operations, ensure_ascii=False, default=str)
        cursor.execute('''
            INSERT INTO routes (product_code, product_name, route_data, total_time, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_code, product_name, route_data, total_time, datetime.now()))

        route_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return route_id

    def get_all_routes(self) -> List[Dict]:
        """Получить все сохраненные маршруты"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM routes ORDER BY created_at DESC")
        result = []
        for row in cursor.fetchall():
            item = dict(row)
            if item['route_data']:
                try:
                    item['route_data'] = json.loads(item['route_data'])
                except:
                    item['route_data'] = []
            result.append(item)
        conn.close()
        return result

    def delete_route(self, route_id: int):
        """Удалить маршрут"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM routes WHERE id = ?", (route_id,))
        conn.commit()
        conn.close()

    def create_order(self, order_number: str, product_code: str, quantity: int) -> int:
        """Создать производственный заказ"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO production_orders (order_number, product_code, quantity, status, created_at)
            VALUES (?, ?, ?, 'pending', ?)
        ''', (order_number, product_code, quantity, datetime.now()))
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return order_id

    def get_all_orders(self) -> List[Dict]:
        """Получить все заказы"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM production_orders ORDER BY created_at DESC")
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result


class RouteCalculator:
    """Калькулятор маршрута"""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def calculate_route(self, product_code: str, quantity: int, selected_operations: List[str] = None) -> Dict:
        """Расчет маршрута"""
        operations = self.db.get_all_operations()

        # Если выбраны конкретные операции
        if selected_operations:
            operations = [op for op in operations if op['code'] in selected_operations]

        route_ops = []
        total_time = 0

        for idx, op in enumerate(operations, 1):
            op_time = (op['default_time'] * quantity) + op['setup_time']
            total_time += op_time

            route_ops.append({
                'sequence': idx,
                'code': op['code'],
                'name': op['name'],
                'workshop': op['workshop_name'],
                'equipment': op.get('equipment_name', 'Не указано'),
                'time_per_unit': op['default_time'],
                'total_time': round(op_time, 2),
                'setup_time': op['setup_time']
            })

        # Определяем последовательность цехов
        workshops = []
        for op in route_ops:
            if op['workshop'] not in workshops:
                workshops.append(op['workshop'])

        return {
            'product_code': product_code,
            'product_name': f'Изделие {product_code}',
            'quantity': quantity,
            'operations': route_ops,
            'total_time': round(total_time, 2),
            'workshops_sequence': workshops,
            'created_at': datetime.now().isoformat()
        }


# ==================== ГЛАВНОЕ ПРИЛОЖЕНИЕ ====================

class RouteApp:
    def __init__(self):
        # Инициализация базы данных
        self.db = DatabaseManager()
        self.calculator = RouteCalculator(self.db)
        self.current_route = None

        # Создание главного окна
        self.window = ctk.CTk()
        self.window.title("Автоматизация маршрутных листов")
        self.window.geometry("1200x700")

        # Сначала создаем статус бар
        self.create_status_bar()

        # Затем создаем вкладки
        self.create_tabview()

        # Создаем содержимое вкладок
        self.create_route_tab()
        self.create_routes_tab()
        self.create_orders_tab()
        self.create_settings_tab()

    def create_status_bar(self):
        """Создание статус бара"""
        self.status_bar = ctk.CTkLabel(
            self.window,
            text="✅ Готов к работе",
            anchor="w",
            fg_color="gray20",
            height=30
        )
        self.status_bar.pack(fill="x", side="bottom")

    def create_tabview(self):
        """Создание вкладок"""
        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Добавление вкладок
        self.tabview.add("📋 Создание маршрута")
        self.tabview.add("📊 Сохраненные маршруты")
        self.tabview.add("📦 Заказы")
        self.tabview.add("⚙️ Настройки")

    def create_route_tab(self):
        """Вкладка создания маршрута"""
        tab = self.tabview.tab("📋 Создание маршрута")

        # Левая панель - настройки
        left_frame = ctk.CTkFrame(tab)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Заголовок
        ctk.CTkLabel(
            left_frame,
            text="Параметры маршрута",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Код изделия
        ctk.CTkLabel(left_frame, text="Код изделия:").pack(anchor="w", padx=20)
        self.product_code_entry = ctk.CTkEntry(left_frame, placeholder_text="Например: PROD-100")
        self.product_code_entry.pack(fill="x", padx=20, pady=5)

        # Количество
        ctk.CTkLabel(left_frame, text="Количество:").pack(anchor="w", padx=20, pady=(10, 0))
        self.quantity_entry = ctk.CTkEntry(left_frame, placeholder_text="10")
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.pack(fill="x", padx=20, pady=5)

        # Выбор операций
        ctk.CTkLabel(left_frame, text="Выберите операции:", font=("Arial", 14, "bold")).pack(anchor="w", padx=20,
                                                                                             pady=(20, 10))

        # Фрейм с чекбоксами
        self.operations_frame = ctk.CTkScrollableFrame(left_frame, height=300)
        self.operations_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # Загрузка операций из БД
        self.operation_vars = {}
        operations = self.db.get_all_operations()
        for op in operations:
            var = ctk.BooleanVar(value=True)
            self.operation_vars[op['code']] = var
            cb = ctk.CTkCheckBox(
                self.operations_frame,
                text=f"{op['code']} - {op['name']} (цех: {op['workshop_name']}, время: {op['default_time']} ч)",
                variable=var
            )
            cb.pack(anchor="w", pady=2)

        # Кнопки
        button_frame = ctk.CTkFrame(left_frame)
        button_frame.pack(fill="x", padx=20, pady=10)

        calculate_btn = ctk.CTkButton(
            button_frame,
            text="Рассчитать маршрут",
            command=self.calculate_route,
            height=40,
            font=("Arial", 14, "bold")
        )
        calculate_btn.pack(side="left", expand=True, padx=5)

        clear_btn = ctk.CTkButton(
            button_frame,
            text="Очистить",
            command=self.clear_form,
            fg_color="gray30",
            height=40
        )
        clear_btn.pack(side="left", expand=True, padx=5)

        # Правая панель - результат
        right_frame = ctk.CTkFrame(tab)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            right_frame,
            text="Результат расчета",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Текстовое поле для результатов
        self.result_text = ctk.CTkTextbox(right_frame, font=("Courier", 11))
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Кнопки экспорта
        export_frame = ctk.CTkFrame(right_frame)
        export_frame.pack(fill="x", padx=10, pady=10)

        export_csv_btn = ctk.CTkButton(
            export_frame,
            text="📄 Экспорт в CSV",
            command=self.export_to_csv,
            fg_color="green"
        )
        export_csv_btn.pack(side="left", expand=True, padx=5)

        export_json_btn = ctk.CTkButton(
            export_frame,
            text="📋 Экспорт в JSON",
            command=self.export_to_json,
            fg_color="blue"
        )
        export_json_btn.pack(side="left", expand=True, padx=5)

        save_btn = ctk.CTkButton(
            export_frame,
            text="💾 Сохранить в БД",
            command=self.save_route_to_db,
            fg_color="orange"
        )
        save_btn.pack(side="left", expand=True, padx=5)

    def create_routes_tab(self):
        """Вкладка сохраненных маршрутов"""
        tab = self.tabview.tab("📊 Сохраненные маршруты")

        # Фрейм для списка
        list_frame = ctk.CTkFrame(tab)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Заголовок
        ctk.CTkLabel(
            list_frame,
            text="Сохраненные маршрутные листы",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Создаем фрейм для таблицы
        tree_frame = ctk.CTkFrame(list_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Таблица с маршрутами
        columns = ("ID", "Код изделия", "Название", "Кол-во", "Время, ч", "Дата")
        self.routes_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # Настройка колонок
        column_widths = {"ID": 50, "Код изделия": 120, "Название": 200, "Кол-во": 80, "Время, ч": 100, "Дата": 150}
        for col in columns:
            self.routes_tree.heading(col, text=col)
            self.routes_tree.column(col, width=column_widths.get(col, 100))

        # Скроллбар
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.routes_tree.yview)
        self.routes_tree.configure(yscrollcommand=scrollbar.set)

        self.routes_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(fill="x", padx=10, pady=10)

        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Обновить",
            command=self.load_routes,
            fg_color="blue"
        )
        refresh_btn.pack(side="left", padx=5)

        view_btn = ctk.CTkButton(
            btn_frame,
            text="👁️ Просмотреть",
            command=self.view_route,
            fg_color="green"
        )
        view_btn.pack(side="left", padx=5)

        delete_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Удалить",
            command=self.delete_route,
            fg_color="red"
        )
        delete_btn.pack(side="left", padx=5)

        # Загрузка данных после создания всех виджетов
        self.load_routes()

    def create_orders_tab(self):
        """Вкладка заказов"""
        tab = self.tabview.tab("📦 Заказы")

        # Верхняя панель - создание заказа
        create_frame = ctk.CTkFrame(tab)
        create_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(create_frame, text="Создание заказа", font=("Arial", 16, "bold")).pack(pady=5)

        input_frame = ctk.CTkFrame(create_frame)
        input_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="Код изделия:").pack(side="left", padx=5)
        self.order_product_entry = ctk.CTkEntry(input_frame, width=150)
        self.order_product_entry.pack(side="left", padx=5)

        ctk.CTkLabel(input_frame, text="Количество:").pack(side="left", padx=5)
        self.order_quantity_entry = ctk.CTkEntry(input_frame, width=100)
        self.order_quantity_entry.insert(0, "1")
        self.order_quantity_entry.pack(side="left", padx=5)

        create_order_btn = ctk.CTkButton(
            input_frame,
            text="Создать заказ",
            command=self.create_order,
            fg_color="green"
        )
        create_order_btn.pack(side="left", padx=10)

        # Нижняя панель - список заказов
        list_frame = ctk.CTkFrame(tab)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            list_frame,
            text="Список заказов",
            font=("Arial", 16, "bold")
        ).pack(pady=5)

        # Фрейм для таблицы заказов
        orders_tree_frame = ctk.CTkFrame(list_frame)
        orders_tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Таблица заказов
        columns = ("ID", "Номер заказа", "Изделие", "Кол-во", "Статус", "Дата")
        self.orders_tree = ttk.Treeview(orders_tree_frame, columns=columns, show="headings", height=12)

        column_widths = {"ID": 50, "Номер заказа": 150, "Изделие": 120, "Кол-во": 80, "Статус": 120, "Дата": 150}
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=column_widths.get(col, 100))

        scrollbar = ttk.Scrollbar(orders_tree_frame, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)

        self.orders_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления заказами
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(fill="x", padx=10, pady=10)

        refresh_orders_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 Обновить",
            command=self.load_orders,
            fg_color="blue"
        )
        refresh_orders_btn.pack(side="left", padx=5)

        # Загрузка заказов
        self.load_orders()

    def create_settings_tab(self):
        """Вкладка настроек"""
        tab = self.tabview.tab("⚙️ Настройки")

        # Тема оформления
        theme_frame = ctk.CTkFrame(tab)
        theme_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(theme_frame, text="Оформление", font=("Arial", 16, "bold")).pack(pady=10)

        ctk.CTkLabel(theme_frame, text="Тема:").pack(anchor="w", padx=20)
        self.theme_var = ctk.StringVar(value="dark")
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["dark", "light", "system"],
            variable=self.theme_var,
            command=self.change_theme
        )
        theme_menu.pack(anchor="w", padx=20, pady=5)

        # Информация
        info_frame = ctk.CTkFrame(tab)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(info_frame, text="Информация", font=("Arial", 16, "bold")).pack(pady=10)

        info_text = """
        📋 Автоматизация маршрутных листов
        Версия: 1.0.0

        Описание:
        Приложение для автоматического расчета 
        маршрутных листов производства.

        Функции:
        • Расчет времени операций
        • Оптимизация последовательности цехов
        • Экспорт в CSV/JSON
        • Хранение маршрутов в БД
        • Управление заказами

        Разработчик: Система автоматизации производства
        """

        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            justify="left",
            font=("Arial", 12)
        )
        info_label.pack(anchor="w", padx=20)

    # ==================== МЕТОДЫ ПРИЛОЖЕНИЯ ====================

    def calculate_route(self):
        """Расчет маршрута"""
        product_code = self.product_code_entry.get()
        quantity = self.quantity_entry.get()

        if not product_code:
            messagebox.showerror("Ошибка", "Введите код изделия!")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть числом!")
            return

        # Получаем выбранные операции
        selected_ops = [code for code, var in self.operation_vars.items() if var.get()]

        if not selected_ops:
            messagebox.showerror("Ошибка", "Выберите хотя бы одну операцию!")
            return

        # Расчет с индикацией загрузки
        self.status_bar.configure(text="🔄 Расчет маршрута...")
        self.window.update()

        try:
            # Выполняем расчет
            route = self.calculator.calculate_route(product_code, quantity, selected_ops)
            self.current_route = route

            # Отображаем результат
            self.result_text.delete("1.0", "end")

            result_str = f"""
{'=' * 70}
МАРШРУТНЫЙ ЛИСТ
{'=' * 70}
📦 Изделие: {route['product_code']}
📝 Название: {route['product_name']}
🔢 Количество: {route['quantity']} шт
📅 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
{'=' * 70}

📋 ОПЕРАЦИИ:
{'-' * 70}
"""
            for op in route['operations']:
                result_str += f"{op['sequence']:>2}. {op['name']:<25} {op['workshop']:<20} {op['total_time']:>8.2f} ч\n"

            result_str += f"{'-' * 70}\n"
            result_str += f"{'ИТОГО:':<57} {route['total_time']:>8.2f} ч\n\n"

            result_str += f"🏭 ПОСЛЕДОВАТЕЛЬНОСТЬ ЦЕХОВ:\n"
            for i, workshop in enumerate(route['workshops_sequence'], 1):
                result_str += f"   {i}. {workshop}\n"

            result_str += f"\n{'=' * 70}\n"

            self.result_text.insert("1.0", result_str)
            self.status_bar.configure(text=f"✅ Расчет завершен. Общее время: {route['total_time']} часов")

            messagebox.showinfo("Успех",
                                f"Маршрут рассчитан!\n\nОбщее время: {route['total_time']} часов\nКоличество операций: {len(route['operations'])}")

        except Exception as e:
            self.status_bar.configure(text=f"❌ Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", f"При расчете произошла ошибка:\n{str(e)}")

    def save_route_to_db(self):
        """Сохранение маршрута в БД"""
        if not hasattr(self, 'current_route') or self.current_route is None:
            messagebox.showerror("Ошибка", "Сначала рассчитайте маршрут!")
            return

        try:
            route_id = self.db.save_route(
                self.current_route['product_code'],
                self.current_route['product_name'],
                self.current_route['operations'],
                self.current_route['total_time']
            )

            messagebox.showinfo("Успех", f"Маршрут сохранен в БД!\nID: {route_id}")
            self.load_routes()
            self.status_bar.configure(text=f"✅ Маршрут сохранен в БД (ID: {route_id})")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить маршрут:\n{str(e)}")

    def export_to_csv(self):
        """Экспорт в CSV"""
        if not hasattr(self, 'current_route') or self.current_route is None:
            messagebox.showerror("Ошибка", "Сначала рассчитайте маршрут!")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"route_{self.current_route['product_code']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        if filename:
            try:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow(['МАРШРУТНЫЙ ЛИСТ'])
                    writer.writerow([f'Изделие: {self.current_route["product_code"]}'])
                    writer.writerow([f'Количество: {self.current_route["quantity"]} шт'])
                    writer.writerow([f'Дата: {datetime.now().strftime("%d.%m.%Y")}'])
                    writer.writerow([])
                    writer.writerow(['№', 'Операция', 'Цех', 'Оборудование', 'Время, ч'])

                    for op in self.current_route['operations']:
                        writer.writerow([
                            op['sequence'],
                            op['name'],
                            op['workshop'],
                            op.get('equipment', '-'),
                            f"{op['total_time']:.2f}"
                        ])

                    writer.writerow([])
                    writer.writerow(['ИТОГО:', '', '', '', f"{self.current_route['total_time']:.2f}"])

                messagebox.showinfo("Успех", f"Файл сохранен:\n{filename}")
                self.status_bar.configure(text=f"📄 Экспортирован в CSV: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def export_to_json(self):
        """Экспорт в JSON"""
        if not hasattr(self, 'current_route') or self.current_route is None:
            messagebox.showerror("Ошибка", "Сначала рассчитайте маршрут!")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"route_{self.current_route['product_code']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.current_route, f, ensure_ascii=False, indent=2, default=str)

                messagebox.showinfo("Успех", f"Файл сохранен:\n{filename}")
                self.status_bar.configure(text=f"📋 Экспортирован в JSON: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def clear_form(self):
        """Очистка формы"""
        self.product_code_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        self.quantity_entry.insert(0, "1")
        self.result_text.delete("1.0", "end")

        for var in self.operation_vars.values():
            var.set(True)

        self.current_route = None
        self.status_bar.configure(text="🗑️ Форма очищена")

    def load_routes(self):
        """Загрузка сохраненных маршрутов"""
        # Очищаем таблицу
        for item in self.routes_tree.get_children():
            self.routes_tree.delete(item)

        routes = self.db.get_all_routes()
        for route in routes:
            self.routes_tree.insert("", "end", values=(
                route['id'],
                route['product_code'],
                (route['product_name'][:27] + '...') if len(route['product_name']) > 30 else route['product_name'],
                route['quantity'],
                route['total_time'],
                route['created_at'][:19] if route['created_at'] else ""
            ))

        self.status_bar.configure(text=f"📊 Загружено {len(routes)} маршрутов")

    def view_route(self):
        """Просмотр выбранного маршрута"""
        selected = self.routes_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите маршрут для просмотра!")
            return

        # Получаем ID выбранного маршрута
        values = self.routes_tree.item(selected[0])['values']
        route_id = values[0]

        # Получаем данные маршрута
        routes = self.db.get_all_routes()
        route = next((r for r in routes if r['id'] == route_id), None)

        if route:
            # Переключаемся на вкладку создания и показываем маршрут
            self.tabview.set("📋 Создание маршрута")

            # Заполняем поля
            self.product_code_entry.delete(0, "end")
            self.product_code_entry.insert(0, route['product_code'])
            self.quantity_entry.delete(0, "end")
            self.quantity_entry.insert(0, str(route['quantity']))

            # Отображаем результат
            self.result_text.delete("1.0", "end")

            result_str = f"""
{'=' * 70}
МАРШРУТНЫЙ ЛИСТ (Сохраненный)
{'=' * 70}
📦 Изделие: {route['product_code']}
📝 Название: {route['product_name']}
🔢 Количество: {route['quantity']} шт
📅 Дата: {route['created_at']}
{'=' * 70}

📋 ОПЕРАЦИИ:
{'-' * 70}
"""
            total_time = 0
            for op in route['route_data']:
                result_str += f"{op['sequence']:>2}. {op['name']:<25} {op['workshop']:<20} {op['total_time']:>8.2f} ч\n"
                total_time += op['total_time']

            result_str += f"{'-' * 70}\n"
            result_str += f"{'ИТОГО:':<57} {total_time:>8.2f} ч\n"

            self.result_text.insert("1.0", result_str)
            self.current_route = route['route_data']

            messagebox.showinfo("Загружено", f"Маршрут {route['product_code']} загружен\nДата: {route['created_at']}")
            self.status_bar.configure(text=f"👁️ Просмотр маршрута {route['product_code']}")

    def delete_route(self):
        """Удаление маршрута"""
        selected = self.routes_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите маршрут для удаления!")
            return

        values = self.routes_tree.item(selected[0])['values']
        route_id = values[0]
        product_code = values[1]

        if messagebox.askyesno("Подтверждение", f"Удалить маршрут {product_code} (ID: {route_id})?"):
            try:
                self.db.delete_route(route_id)
                self.load_routes()
                messagebox.showinfo("Успех", "Маршрут удален")
                self.status_bar.configure(text=f"🗑️ Маршрут {product_code} удален")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить маршрут:\n{str(e)}")

    def create_order(self):
        """Создание заказа"""
        product_code = self.order_product_entry.get()
        quantity = self.order_quantity_entry.get()

        if not product_code:
            messagebox.showerror("Ошибка", "Введите код изделия!")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть положительным числом!")
            return

        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{product_code}"

        try:
            order_id = self.db.create_order(order_number, product_code, quantity)

            messagebox.showinfo("Успех",
                                f"Заказ создан!\n\nНомер: {order_number}\nID: {order_id}\nИзделие: {product_code}\nКоличество: {quantity}")
            self.load_orders()

            # Очищаем поля
            self.order_product_entry.delete(0, "end")
            self.order_quantity_entry.delete(0, "end")
            self.order_quantity_entry.insert(0, "1")

            self.status_bar.configure(text=f"✅ Создан заказ {order_number}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать заказ:\n{str(e)}")

    def load_orders(self):
        """Загрузка заказов"""
        # Очищаем таблицу
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        orders = self.db.get_all_orders()
        status_icons = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅',
            'cancelled': '❌'
        }

        for order in orders:
            status_icon = status_icons.get(order['status'], '📋')
            status_text = f"{status_icon} {order['status']}"

            self.orders_tree.insert("", "end", values=(
                order['id'],
                order['order_number'],
                order['product_code'],
                order['quantity'],
                status_text,
                order['created_at'][:19] if order['created_at'] else ""
            ))

        self.status_bar.configure(text=f"📦 Загружено {len(orders)} заказов")

    def change_theme(self, theme):
        """Смена темы"""
        ctk.set_appearance_mode(theme)
        self.status_bar.configure(text=f"🎨 Тема изменена на {theme}")

    def run(self):
        """Запуск приложения"""
        self.window.mainloop()


# ==================== ЗАПУСК ====================

if __name__ == "__main__":
    print("Запуск приложения...")
    app = RouteApp()
    app.run()