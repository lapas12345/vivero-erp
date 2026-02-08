import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Vivero ERP - Logística de Aprovisionamiento",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ FUNCIONES DE BASE DE DATOS ============

def get_connection():
    return sqlite3.connect("vivero.db")

def init_database():
    """Crea tablas si no existen"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insumos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            categoria TEXT,
            stock_actual REAL DEFAULT 0,
            stock_minimo REAL DEFAULT 0,
            unidad_medida TEXT,
            proveedor_habitual_id INTEGER,
            fecha_caducidad DATE
        )
    """)
    
    # Fases
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            orden INTEGER NOT NULL,
            duracion_dias INTEGER NOT NULL
        )
    """)
    
    # Proveedores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contacto TEXT,
            telefono TEXT,
            email TEXT,
            categoria TEXT
        )
    """)
    
    # Lotes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            cantidad_plantas INTEGER NOT NULL,
            fecha_inicio DATE,
            fase_actual_id INTEGER,
            estado TEXT DEFAULT 'activo'
        )
    """)
    
    # Insumos por fase
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insumos_por_fase (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fase_id INTEGER,
            insumo_id INTEGER,
            cantidad_por_planta REAL
        )
    """)
    
    # Órdenes de compra
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordenes_compra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            fecha_emision DATE DEFAULT CURRENT_DATE,
            fecha_entrega_esperada DATE,
            proveedor_id INTEGER,
            estado TEXT DEFAULT 'borrador',
            total_estimado REAL
        )
    """)
    
    # Insertar datos de prueba
    cursor.execute("SELECT COUNT(*) FROM insumos")
    if cursor.fetchone()[0] == 0:
        insertar_datos_prueba(cursor)
    
    conn.commit()
    conn.close()

def insertar_datos_prueba(cursor):
    """Datos iniciales"""
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
    
    fases = [
        ('Preparación de sustrato', 1, 7),
        ('Siembra', 2, 1),
        ('Desarrollo/Germinación', 3, 45),
        ('Injerto', 4, 30),
        ('Aclimatación', 5, 60),
    ]
    cursor.executemany("INSERT INTO fases (nombre, orden, duracion_dias) VALUES (?, ?, ?)", fases)
    
    proveedores = [
        ('AgroInsumos S.A.', 'Juan Pérez', '0991234567', 'ventas@agro.com', 'sustratos'),
        ('Fertilizantes del Norte', 'María López', '0987654321', 'contacto@fnorte.com', 'fertilizante'),
    ]
    cursor.executemany("""
        INSERT INTO proveedores (nombre, contacto, telefono, email, categoria)
        VALUES (?, ?, ?, ?, ?)
    """, proveedores)

def get_insumos():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM insumos ORDER BY nombre", conn)
    conn.close()
    return df

def get_insumos_stock_bajo():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT * FROM insumos 
        WHERE stock_actual <= stock_minimo
        ORDER BY (stock_actual / stock_minimo)
    """, conn)
    conn.close()
    return df

# ============ INICIALIZACIÓN ============
init_database()

# ============ SIDEBAR ============
st.sidebar.title("🌱 Vivero ERP")
st.sidebar.markdown("**Logística de Aprovisionamiento**")

menu = st.sidebar.radio(
    "Navegación",
    ["📊 Dashboard", "📦 Inventario", "📋 Proyecciones", "📝 Órdenes de Compra", "⚙️ Configuración"]
)

# ============ PÁGINAS ============

if menu == "📊 Dashboard":
    st.title("Dashboard")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    df_insumos = get_insumos()
    df_alertas = get_insumos_stock_bajo()
    
    col1.metric("Total Insumos", len(df_insumos))
    col2.metric("Alertas Stock", len(df_alertas), "Crítico" if len(df_alertas) > 0 else "OK")
    col3.metric("Órdenes Pendientes", "3")
    col4.metric("Lotes Activos", "2")
    
    st.divider()
    
    # Alertas
    st.subheader("⚠️ Alertas de Stock Crítico")
    
    if len(df_alertas) > 0:
        for _, row in df_alertas.iterrows():
            with st.container():
                cols = st.columns([3, 1, 1])
                cols[0].error(f"🔴 **{row['nombre']}**")
                cols[1].write(f"Stock: **{row['stock_actual']}** {row['unidad_medida']}")
                cols[2].write(f"Mínimo: {row['stock_minimo']} {row['unidad_medida']}")
    else:
        st.success("✅ No hay alertas de stock. Todo está en orden.")
    
    # Gráfico simple de stock
    st.divider()
    st.subheader("📊 Niveles de Stock")
    
    df_chart = df_insumos[['nombre', 'stock_actual', 'stock_minimo']].copy()
    df_chart = df_chart.set_index('nombre')
    st.bar_chart(df_chart)

elif menu == "📦 Inventario":
    st.title("Inventario de Insumos")
    
    df = get_insumos()
    
    # Filtros
    col1, col2 = st.columns(2)
    filtro_categoria = col1.selectbox("Filtrar por categoría", ["Todas"] + df['categoria'].unique().tolist())
    filtro_estado = col2.selectbox("Estado", ["Todos", "Stock Bajo", "OK"])
    
    # Aplicar filtros
    if filtro_categoria != "Todas":
        df = df[df['categoria'] == filtro_categoria]
    
    if filtro_estado == "Stock Bajo":
        df = df[df['stock_actual'] <= df['stock_minimo']]
    elif filtro_estado == "OK":
        df = df[df['stock_actual'] > df['stock_minimo']]
    
    # Mostrar tabla
    st.dataframe(
        df[['codigo', 'nombre', 'categoria', 'stock_actual', 'stock_minimo', 'unidad_medida']],
        use_container_width=True,
        hide_index=True
    )
    
    # Botón para agregar insumo
    st.divider()
    with st.expander("➕ Agregar Nuevo Insumo"):
        with st.form("nuevo_insumo"):
            col1, col2 = st.columns(2)
            codigo = col1.text_input("Código")
            nombre = col2.text_input("Nombre")
            categoria = st.selectbox("Categoría", ["sustrato", "fertilizante", "herramienta", "fundas", "otro"])
            
            col3, col4, col5 = st.columns(3)
            stock = col3.number_input("Stock Inicial", min_value=0.0)
            minimo = col4.number_input("Stock Mínimo", min_value=0.0)
            unidad = col5.text_input("Unidad (kg, unidades, etc.)")
            
            if st.form_submit_button("Guardar Insumo"):
                conn = get_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO insumos (codigo, nombre, categoria, stock_actual, stock_minimo, unidad_medida)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (codigo, nombre, categoria, stock, minimo, unidad))
                    conn.commit()
                    st.success("✅ Insumo agregado correctamente")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    conn.close()

elif menu == "📋 Proyecciones":
    st.title("Proyección de Necesidades")
    
    st.info("📅 Calcula qué insumos necesitas comprar basado en los lotes programados")
    
    col1, col2 = st.columns(2)
    fecha_inicio = col1.date_input("Desde", datetime.now())
    fecha_fin = col2.date_input("Hasta", datetime.now() + timedelta(days=30))
    
    if st.button("🔍 Calcular Proyección", type="primary"):
        st.warning("⚠️ Función en desarrollo: Aquí se conectará con la tabla de lotes para calcular demanda derivada")
        
        # Placeholder de ejemplo
        datos_ejemplo = {
            'Insumo': ['Sustrato Premium', 'Fundas de polietileno', 'Fertilizante NPK'],
            'Cantidad Necesaria': [500, 1000, 50],
            'Stock Actual': [25.5, 200, 15],
            'A Comprar': [474.5, 800, 35],
            'Prioridad': ['🔴 Alta', '🔴 Alta', '🟡 Media']
        }
        df_proy = pd.DataFrame(datos_ejemplo)
        st.dataframe(df_proy, use_container_width=True, hide_index=True)

elif menu == "📝 Órdenes de Compra":
    st.title("Órdenes de Compra")
    
    tab1, tab2 = st.tabs(["📋 Ver Órdenes", "➕ Nueva Orden"])
    
    with tab1:
        st.subheader("Órdenes Existentes")
        
        # Datos de ejemplo
        ordenes_ejemplo = {
            'Código': ['OC-2025-001', 'OC-2025-002', 'OC-2025-003'],
            'Fecha': ['2025-01-15', '2025-01-20', '2025-01-25'],
            'Proveedor': ['AgroInsumos S.A.', 'Fertilizantes del Norte', 'AgroInsumos S.A.'],
            'Total': [1250.00, 890.50, 2340.00],
            'Estado': ['Recibida', 'Pendiente', 'Enviada']
        }
        df_ordenes = pd.DataFrame(ordenes_ejemplo)
        st.dataframe(df_ordenes, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Generar Nueva Orden de Compra")
        
        with st.form("nueva_orden"):
            proveedor = st.selectbox("Proveedor", ["AgroInsumos S.A.", "Fertilizantes del Norte"])
            fecha_entrega = st.date_input("Fecha de entrega esperada", datetime.now() + timedelta(days=7))
            
            st.divider()
            st.write("**Insumos a solicitar:**")
            
            col1, col2, col3 = st.columns(3)
            insumo = col1.selectbox("Insumo", ["Sustrato Premium", "Sustrato Estándar", "Fertilizante NPK"])
            cantidad = col2.number_input("Cantidad", min_value=1.0)
            precio = col3.number_input("Precio unitario", min_value=0.0)
            
            if st.form_submit_button("Generar Orden"):
                st.success("✅ Orden de compra generada correctamente")

elif menu == "⚙️ Configuración":
    st.title("Configuración del Sistema")
    
    st.subheader("💾 Respaldo de Datos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Exportar Base de Datos**")
        if st.button("📥 Descargar Backup (.db)"):
            with open("vivero.db", "rb") as file:
                st.download_button(
                    label="Haz clic para descargar",
                    data=file,
                    file_name=f"vivero_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
                    mime="application/octet-stream"
                )
    
    with col2:
        st.write("**Importar Backup**")
        archivo = st.file_uploader("Selecciona archivo .db", type=['db'])
        if archivo is not None:
            st.warning("⚠️ Esta función sobrescribirá los datos actuales")
            if st.button("Restaurar Backup"):
                st.success("Backup restaurado (simulado)")
    
    st.divider()
    
    st.subheader("📊 Información del Sistema")
    st.info(f"""
    **Versión:** 1.0.0  
    **Última actualización:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  
    **Base de datos:** vivero.db  
    **Modo:** Offline (SQLite)
    """)