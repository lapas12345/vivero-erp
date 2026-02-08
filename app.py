import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Vivero ERP", layout="wide")

st.title("🌱 Sistema ERP - Logística de Aprovisionamiento")
st.markdown("**Vivero de Cacao - ULEAM**")

# Sidebar
menu = st.sidebar.radio("Menú", ["Dashboard", "Inventario", "Configuración"])

if menu == "Dashboard":
    st.header("📊 Dashboard")
    
    # Conectar a BD
    try:
        conn = sqlite3.connect("vivero.db")
        cursor = conn.cursor()
        
        # Verificar si existe tabla insumos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='insumos'")
        if cursor.fetchone():
            # Contar insumos
            cursor.execute("SELECT COUNT(*) FROM insumos")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM insumos WHERE stock_actual <= stock_minimo")
            alertas = cursor.fetchone()[0]
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Insumos", total)
            col2.metric("Alertas Stock", alertas, "Crítico" if alertas > 0 else "OK")
            col3.metric("Estado", "Online")
            
            # Mostrar tabla
            df = pd.read_sql_query("SELECT * FROM insumos", conn)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("Base de datos no inicializada")
            
        conn.close()
        
    except Exception as e:
        st.error(f"Error: {e}")

elif menu == "Inventario":
    st.header("📦 Inventario")
    st.info("Módulo en desarrollo")

elif menu == "Configuración":
    st.header("⚙️ Configuración")
    st.info("Sistema Offline - SQLite")