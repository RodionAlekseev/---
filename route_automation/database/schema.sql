-- Цеха
CREATE TABLE IF NOT EXISTS workshops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Оборудование
CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    model TEXT,
    workshop_id INTEGER,
    power_kw FLOAT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE SET NULL
);

-- Технологические операции
CREATE TABLE IF NOT EXISTS operations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    default_time FLOAT,
    setup_time FLOAT DEFAULT 0,
    time_unit TEXT DEFAULT 'hour',
    equipment_id INTEGER,
    workshop_id INTEGER,
    requires_quality_check BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE SET NULL,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE SET NULL
);

-- Маршруты для типов изделий
CREATE TABLE IF NOT EXISTS product_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code TEXT NOT NULL,
    product_name TEXT,
    operation_sequence TEXT,
    total_time FLOAT,
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Спецификации изделий
CREATE TABLE IF NOT EXISTS specifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code TEXT NOT NULL,
    component_code TEXT NOT NULL,
    component_name TEXT,
    quantity INTEGER DEFAULT 1,
    unit TEXT DEFAULT 'шт',
    operation_id INTEGER,
    time_coefficient FLOAT DEFAULT 1.0,
    priority INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (operation_id) REFERENCES operations(id) ON DELETE SET NULL
);

-- Производственные заказы
CREATE TABLE IF NOT EXISTS production_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    product_code TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    deadline DATE,
    status TEXT DEFAULT 'planned',
    route_snapshot TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Журнал маршрутных листов
CREATE TABLE IF NOT EXISTS route_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_code TEXT,
    route_data TEXT,
    total_time FLOAT,
    created_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES production_orders(id) ON DELETE CASCADE
);

-- Индексы
CREATE INDEX idx_product_routes_product_code ON product_routes(product_code);
CREATE INDEX idx_specifications_product_code ON specifications(product_code);
CREATE INDEX idx_production_orders_status ON production_orders(status);
CREATE INDEX idx_operations_workshop ON operations(workshop_id);
CREATE INDEX idx_equipment_workshop ON equipment(workshop_id);

-- Начальные данные
INSERT OR IGNORE INTO workshops (code, name, description) VALUES 
('WS001', 'Заготовительный цех', 'Раскрой и подготовка материалов'),
('WS002', 'Механообрабатывающий цех', 'Токарные, фрезерные работы'),
('WS003', 'Сварочный цех', 'Сварка и сборка'),
('WS004', 'Окрасочный цех', 'Покраска и сушка'),
('WS005', 'Сборочный цех', 'Финальная сборка'),
('WS006', 'Контроль качества', 'Проверка и испытания');

INSERT OR IGNORE INTO equipment (code, name, model, workshop_id) VALUES 
('EQ001', 'Лазерный станок', 'LASER-2000', 1),
('EQ002', 'Токарный станок', 'CK6163', 2),
('EQ003', 'Фрезерный станок', 'XK7145', 2),
('EQ004', 'Сварочный аппарат', 'MIG-350', 3),
('EQ005', 'Окрасочная камера', 'PAINT-1000', 4),
('EQ006', 'Сборочный стол', 'ASSY-500', 5),
('EQ007', 'Испытательный стенд', 'TEST-100', 6);

INSERT OR IGNORE INTO operations (code, name, description, default_time, setup_time, equipment_id, workshop_id, requires_quality_check) VALUES 
('CUT', 'Раскрой', 'Раскрой материала', 0.5, 0.2, 1, 1, 1),
('TURN', 'Токарная обработка', 'Токарные работы', 1.0, 0.3, 2, 2, 1),
('MILL', 'Фрезерная обработка', 'Фрезерные работы', 1.5, 0.3, 3, 2, 1),
('WELD', 'Сварка', 'Сварочные работы', 0.8, 0.2, 4, 3, 1),
('PAINT', 'Покраска', 'Окраска изделия', 0.6, 0.4, 5, 4, 0),
('ASSEMBLE', 'Сборка', 'Сборка узлов', 1.2, 0.1, 6, 5, 0),
('TEST', 'Испытания', 'Проверка качества', 0.5, 0.1, 7, 6, 1);