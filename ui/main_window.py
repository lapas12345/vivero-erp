import customtkinter as ctk
from database import get_insumos_con_stock_bajo, init_database

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema ERP - Logística de Aprovisionamiento")
        self.geometry("1000x700")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Frame lateral (menú)
        self.menu_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.pack_propagate(False)
        
        ctk.CTkLabel(self.menu_frame, text="VIVERO ERP", 
                    font=("Arial", 20, "bold")).pack(pady=30)
        
        # Botones de menú
        self.crear_boton_menu("📊 Dashboard", self.mostrar_dashboard)
        self.crear_boton_menu("📦 Inventario", self.mostrar_inventario)
        self.crear_boton_menu("📋 Proyecciones", self.mostrar_proyecciones)
        self.crear_boton_menu("📝 Órdenes de Compra", self.mostrar_ordenes)
        self.crear_boton_menu("⚙️ Configuración", self.mostrar_config)
        
        # Frame principal (contenido dinámico)
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Mostrar dashboard al inicio
        self.mostrar_dashboard()
    
    def crear_boton_menu(self, texto, comando):
        btn = ctk.CTkButton(self.menu_frame, text=texto, 
                           command=comando, width=180, height=40,
                           fg_color="transparent", text_color=("gray10", "gray90"),
                           hover_color=("gray70", "gray30"), anchor="w")
        btn.pack(pady=5, padx=10)
    
    def limpiar_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def mostrar_dashboard(self):
        self.limpiar_main_frame()
        
        ctk.CTkLabel(self.main_frame, text="Dashboard", 
                    font=("Arial", 24, "bold")).pack(pady=20)
        
        # Frame de alertas críticas
        alertas_frame = ctk.CTkFrame(self.main_frame)
        alertas_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(alertas_frame, text="⚠️ Alertas de Stock Crítico", 
                    font=("Arial", 16, "bold"), text_color="red").pack(pady=10)
        
        insumos_bajos = get_insumos_con_stock_bajo()
        
        if insumos_bajos:
            for insumo in insumos_bajos:
                texto = f"• {insumo['nombre']}: {insumo['stock_actual']} {insumo['unidad_medida']} (mín: {insumo['stock_minimo']})"
                ctk.CTkLabel(alertas_frame, text=texto, text_color="red").pack(anchor="w", padx=20)
        else:
            ctk.CTkLabel(alertas_frame, text="✅ No hay alertas de stock", 
                        text_color="green").pack()
        
        # Resumen rápido
        resumen_frame = ctk.CTkFrame(self.main_frame)
        resumen_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(resumen_frame, text="📈 Resumen", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        datos = [
            ("Total de insumos:", "12"),
            ("Órdenes pendientes:", "3"),
            ("Lotes activos:", "2"),
            ("Alertas:", str(len(insumos_bajos)))
        ]
        
        for label, valor in datos:
            fila = ctk.CTkFrame(resumen_frame, fg_color="transparent")
            fila.pack(fill="x", padx=20, pady=2)
            ctk.CTkLabel(fila, text=label).pack(side="left")
            ctk.CTkLabel(fila, text=valor, font=("Arial", 14, "bold")).pack(side="right")
    
    def mostrar_inventario(self):
        self.limpiar_main_frame()
        
        ctk.CTkLabel(self.main_frame, text="Inventario de Insumos", 
                    font=("Arial", 24, "bold")).pack(pady=20)
        
        # Tabla simple
        from database import get_insumos
        insumos = get_insumos()
        
        # Encabezados
        headers = ctk.CTkFrame(self.main_frame)
        headers.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(headers, text="Código", width=100, font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkLabel(headers, text="Nombre", width=200, font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkLabel(headers, text="Stock", width=100, font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkLabel(headers, text="Mínimo", width=100, font=("Arial", 12, "bold")).pack(side="left")
        ctk.CTkLabel(headers, text="Estado", width=100, font=("Arial", 12, "bold")).pack(side="left")
        
        # Scrollable frame para la lista
        scroll = ctk.CTkScrollableFrame(self.main_frame, height=400)
        scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        for insumo in insumos:
            fila = ctk.CTkFrame(scroll)
            fila.pack(fill="x", pady=2)
            
            # Color de estado
            estado_color = "green" if insumo['stock_actual'] > insumo['stock_minimo'] else "red"
            estado_texto = "OK" if insumo['stock_actual'] > insumo['stock_minimo'] else "BAJO"
            
            ctk.CTkLabel(fila, text=insumo['codigo'], width=100).pack(side="left")
            ctk.CTkLabel(fila, text=insumo['nombre'], width=200).pack(side="left")
            ctk.CTkLabel(fila, text=f"{insumo['stock_actual']} {insumo['unidad_medida']}", width=100).pack(side="left")
            ctk.CTkLabel(fila, text=str(insumo['stock_minimo']), width=100).pack(side="left")
            ctk.CTkLabel(fila, text=estado_texto, width=100, text_color=estado_color).pack(side="left")
    
    def mostrar_proyecciones(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="Proyección de Necesidades", 
                    font=("Arial", 24, "bold")).pack(pady=20)
        
        ctk.CTkLabel(self.main_frame, text="Aquí irá el cálculo de compras basado en lotes programados").pack()
        
        # Placeholder para fechas
        fechas_frame = ctk.CTkFrame(self.main_frame)
        fechas_frame.pack(pady=20)
        
        ctk.CTkLabel(fechas_frame, text="Período de proyección:").pack(side="left", padx=5)
        ctk.CTkEntry(fechas_frame, placeholder_text="Desde (YYYY-MM-DD)", width=150).pack(side="left", padx=5)
        ctk.CTkEntry(fechas_frame, placeholder_text="Hasta (YYYY-MM-DD)", width=150).pack(side="left", padx=5)
        ctk.CTkButton(fechas_frame, text="Calcular").pack(side="left", padx=5)
    
    def mostrar_ordenes(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="Órdenes de Compra", 
                    font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self.main_frame, text="Aquí se generarán y gestionarán las órdenes a proveedores").pack()
    
    def mostrar_config(self):
        self.limpiar_main_frame()
        ctk.CTkLabel(self.main_frame, text="Configuración", 
                    font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkButton(self.main_frame, text="Exportar Base de Datos (Backup)", 
                     command=self.exportar_backup).pack(pady=10)
    
    def exportar_backup(self):
        import shutil
        from datetime import datetime
        import os
        
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"vivero_backup_{fecha}.db"
        
        try:
            shutil.copy("vivero.db", backup_name)
            ctk.CTkLabel(self.main_frame, text=f"✅ Backup creado: {backup_name}", 
                        text_color="green").pack(pady=10)
        except Exception as e:
            ctk.CTkLabel(self.main_frame, text=f"❌ Error: {str(e)}", 
                        text_color="red").pack(pady=10)