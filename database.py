import sqlite3
from datetime import datetime, timedelta

def get_connection():
    return sqlite3.connect("vivero.db")

def init_database():
    """Crea todas las tablas necesarias"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabla de insumos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            categoria TEXT CHECK(categoria IN ('sustrato', 'fertilizante', 'herramienta', 'fundas', 'otro')),
            stock_actual REAL DEFAULT 0,
            stock_minimo REAL DEFAULT 0,
            unidad_medida TEXT,
            proveedor_habitual_id INTEGER,
            fecha_caducidad DATE,
            activo BOOLEAN DEFAULT 1
        )
    """)
    
    # Tabla de fases (para calcular proyecciones)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            orden INTEGER NOT NULL,
            duracion_dias INTEGER NOT NULL
        )
    """)
    
    # Tabla de insumos por fase (cuánto necesita cada fase)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insumos_por_fase (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fase_id INTEGER,
            insumo_id INTEGER,
            cantidad_por_planta REAL,
            FOREIGN KEY (fase_id) REFERENCES fases(id),
            FOREIGN KEY (insumo_id) REFERENCES insumos(id)
        )
    """)
    
    # Tabla de lotes (cronograma que viene del encargado)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            cantidad_plantas INTEGER NOT NULL,
            fecha_inicio DATE,
            fase_actual_id INTEGER,
            estado TEXT DEFAULT 'activo',
            FOREIGN KEY (fase_actual_id) REFERENCES fases(id)
        )
    """)
    
    # Tabla de proveedores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contacto TEXT,
            telefono TEXT,
            email TEXT,
            categoria TEXT,
            calificacion REAL DEFAULT 0
        )
    """)
    
    # Tabla de órdenes de compra
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordenes_compra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            fecha_emision DATE DEFAULT CURRENT_DATE,
            fecha_entrega_esperada DATE,
            proveedor_id INTEGER,
            estado TEXT DEFAULT 'borrador',
            total_estimado REAL,
            FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
        )
    """)
    
    # Tabla de detalle de órdenes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordenes_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orden_id INTEGER,
            insumo_id INTEGER,
            cantidad_solicitada REAL,
            cantidad_recibida REAL DEFAULT 0,
            precio_unitario REAL,
            FOREIGN KEY (orden_id) REFERENCES ordenes_compra(id),
            FOREIGN KEY (insumo_id) REFERENCES insumos(id)
        )
    """)
    
    # Insertar datos de prueba si no existen
    cursor.execute("SELECT COUNT(*) FROM insumos")
    if cursor.fetchone()[0] == 0:
        insertar_datos_prueba(cursor)
    
    conn.commit()
    conn.close()

def insertar_datos_prueba(cursor):
    """Inserta datos iniciales para pruebas"""
    
    # Insumos
    insumos = [
        ('SUS-001', 'Sustrato Premium', 'sustrato', 25.5, 50.0, 'kg', '2025-06-15'),
        ('SUS-002', 'Sustrato Estándar', 'sustrato', 80.0, 100.0, 'kg', None),
        ('FER-001', 'Fertilizante NPK 20-20-20', 'fertilizante', 15.0, 20.0, 'kg', None),
        ('FUN-001', 'Fundas de polietileno', 'fundas', 200.0, 500.0, 'unidades', None),
        ('HER-001', 'Machete', 'herramienta', 5.0, 10.0, 'unidades', None),
    ]
    cursor.executemany("""
        INSERT INTO insumos (codigo, nombre, categoria, stock_actual, stock_minimo, unidad_medida, fecha_caducidad)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, insumos)
    
    # Fases del cacao (las 5 que mencionó el Ing. Nivela)
    fases = [
        ('Preparación de sustrato', 1, 7),
        ('Siembra', 2, 1),
        ('Desarrollo/Germinación', 3, 45),
        ('Injerto', 4, 30),
        ('Aclimatación', 5, 60),
    ]
    cursor.executemany("""
        INSERT INTO fases (nombre, orden, duracion_dias) VALUES (?, ?, ?)
    """, fases)
    
    # Proveedores
    proveedores = [
        ('AgroInsumos S.A.', 'Juan Pérez', '0991234567', 'ventas@agro.com', 'sustratos'),
        ('Fertilizantes del Norte', 'María López', '0987654321', 'contacto@fnorte.com', 'fertilizante'),
    ]
    cursor.executemany("""
        INSERT INTO proveedores (nombre, contacto, telefono, email, categoria)
        VALUES (?, ?, ?, ?, ?)
    """, proveedores)
    
    print("✅ Datos de prueba insertados")

# Funciones de consulta
def get_insumos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM insumos WHERE activo = 1 ORDER BY nombre")
    columnas = [desc[0] for desc in cursor.description]
    resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    conn.close()
    return resultados

def get_insumos_con_stock_bajo():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM insumos 
        WHERE stock_actual <= stock_minimo AND activo = 1
        ORDER BY (stock_actual / stock_minimo)
    """)
    columnas = [desc[0] for desc in cursor.description]
    resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    conn.close()
    return resultados

def get_proyeccion_necesidades(fecha_inicio, fecha_fin):
    """Calcula insumos necesarios basado en lotes programados"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Consulta que une lotes con sus insumos por fase
    cursor.execute("""
        SELECT 
            i.id,
            i.nombre,
            i.unidad_medida,
            SUM(ipf.cantidad_por_planta * l.cantidad_plantas) as total_necesario,
            i.stock_actual,
            (SUM(ipf.cantidad_por_planta * l.cantidad_plantas) - i.stock_actual) as deficit
        FROM lotes l
        JOIN fases f ON l.fase_actual_id = f.id
        JOIN insumos_por_fase ipf ON f.id = ipf.fase_id
        JOIN insumos i ON ipf.insumo_id = i.id
        WHERE l.fecha_inicio BETWEEN ? AND ?
        AND l.estado = 'activo'
        GROUP BY i.id
        HAVING deficit > 0
    """, (fecha_inicio, fecha_fin))
    
    resultados = cursor.fetchall()
    conn.close()
    return resultados