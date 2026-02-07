import sqlite3
import customtkinter as ctk
from datetime import datetime, timedelta

# ============ BASE DE DATOS ============
def crear_base_datos():
    conn = sqlite3.connect("vivero.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insumos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nombre TEXT NOT NULL,
            categoria TEXT,
            stock_actual REAL DEFAULT 0,
            stock_minimo REAL,
            unidad TEXT,
            fecha_caducidad DATE
        )
    """)
    
    # Insertar datos de prueba
    cursor.execute("""
        INSERT OR IGNORE INTO insumos (codigo, nombre, categoria, stock_actual, stock_minimo, unidad)
        VALUES ('SUS-001', 'Sustrato Premium', 'sustrato', 25.5, 50.0, 'kg')
    """)
    
    conn.commit()
    conn.close()

# ============ APLICACIÓN ============
class ViveroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Aprovisionamiento - Vivero de Cacao")
        self.geometry("900x600")
        
        # Título
        ctk.CTkLabel(self, text="Logística de Aprovisionamiento", 
                    font=("Arial", 24, "bold")).pack(pady=20)
        
        # Frame de alertas
        self.frame_alertas = ctk.CTkFrame(self)
        self.frame_alertas.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(self.frame_alertas, text="⚠️ Alertas de Stock", 
                    font=("Arial", 16, "bold"), text_color="orange").pack(pady=5)
        
        self.mostrar_alertas()
        
        # Botones principales
        ctk.CTkButton(self, text="📦 Ver Inventario", 
                     command=self.ver_inventario).pack(pady=10)
        ctk.CTkButton(self, text="📋 Proyección de Compras", 
                     command=self.ver_proyeccion).pack(pady=10)
        ctk.CTkButton(self, text="📝 Nueva Orden de Compra", 
                     command=self.nueva_orden).pack(pady=10)
    
    def mostrar_alertas(self):
        conn = sqlite3.connect("vivero.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT nombre, stock_actual, stock_minimo, unidad 
            FROM insumos 
            WHERE stock_actual <= stock_minimo
        """)
        
        alertas = cursor.fetchall()
        conn.close()
        
        if alertas:
            for nombre, actual, minimo, unidad in alertas:
                texto = f"• {nombre}: {actual} {unidad} (mínimo: {minimo} {unidad})"
                ctk.CTkLabel(self.frame_alertas, text=texto, 
                           text_color="red").pack(anchor="w", padx=10)
        else:
            ctk.CTkLabel(self.frame_alertas, text="✅ No hay alertas de stock", 
                       text_color="green").pack()
    
    def ver_inventario(self):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Inventario")
        ventana.geometry("600x400")
        
        # Tabla simple
        conn = sqlite3.connect("vivero.db")
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, nombre, stock_actual, unidad FROM insumos")
        datos = cursor.fetchall()
        conn.close()
        
        for i, (codigo, nombre, stock, unidad) in enumerate(datos):
            texto = f"{codigo} | {nombre} | Stock: {stock} {unidad}"
            ctk.CTkLabel(ventana, text=texto).pack(pady=2)
    
    def ver_proyeccion(self):
        # Aquí iría tu lógica de proyección de compras
        pass
    
    def nueva_orden(self):
        # Aquí iría el formulario de órdenes de compra
        pass

# ============ EJECUCIÓN ============
if __name__ == "__main__":
    crear_base_datos()
    app = ViveroApp()
    app.mainloop()