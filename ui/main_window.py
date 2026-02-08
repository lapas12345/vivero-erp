import customtkinter as ctk
from tkinter import messagebox
from database import get_insumos_con_stock_bajo, init_database, get_insumos
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🌱 Sistema ERP - Vivero de Cacao ULEAM")
        self.geometry("1200x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Crear sidebar
        self.crear_sidebar()
        
        # Frame principal de contenido
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Variable para el frame actual
        self.current_content = None
        
        # Mostrar dashboard al inicio
        self.mostrar_dashboard()
    
    def crear_sidebar(self):
        """Crea el menú lateral"""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)
        self.sidebar.grid_propagate(False)
        
        # Logo/Título
        logo = ctk.CTkLabel(
            self.sidebar,
            text="🌱 Vivero ERP",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        logo.grid(row=0, column=0, padx=20, pady=(30, 5))
        
        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Logística de\nAprovisionamiento",
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        )
        subtitle.grid(row=1, column=0, padx=20, pady=(0, 30))
        
        # Botones del menú
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar,
            text="📊 Dashboard",
            command=self.mostrar_dashboard,
            font=ctk.CTkFont(size=14),
            height=40,
            anchor="w"
        )
        self.btn_dashboard.grid(row=2, column=0, padx=15, pady=8, sticky="ew")
        
        self.btn_inventario = ctk.CTkButton(
            self.sidebar,
            text="📦 Inventario",
            command=self.mostrar_inventario,
            font=ctk.CTkFont(size=14),
            height=40,
            anchor="w"
        )
        self.btn_inventario.grid(row=3, column=0, padx=15, pady=8, sticky="ew")
        
        self.btn_proyecciones = ctk.CTkButton(
            self.sidebar,
            text="📋 Proyecciones",
            command=self.mostrar_proyecciones,
            font=ctk.CTkFont(size=14),
            height=40,
            anchor="w"
        )
        self.btn_proyecciones.grid(row=4, column=0, padx=15, pady=8, sticky="ew")
        
        self.btn_ordenes = ctk.CTkButton(
            self.sidebar,
            text="🛒 Órdenes",
            command=self.mostrar_ordenes,
            font=ctk.CTkFont(size=14),
            height=40,
            anchor="w"
        )
        self.btn_ordenes.grid(row=5, column=0, padx=15, pady=8, sticky="ew")
        
        # Botón de configuración al final
        self.btn_config = ctk.CTkButton(
            self.sidebar,
            text="⚙️ Configuración",
            command=self.mostrar_config,
            font=ctk.CTkFont(size=14),
            height=40,
            anchor="w",
            fg_color="gray40",
            hover_color="gray30"
        )
        self.btn_config.grid(row=8, column=0, padx=15, pady=(8, 30), sticky="ew")
    
    def limpiar_main_frame(self):
        """Limpia el contenido del frame principal"""
        if self.current_content:
            self.current_content.destroy()
            self.current_content = None
    
    def mostrar_dashboard(self):
        """Muestra el dashboard principal"""
        self.limpiar_main_frame()
        
        # Frame para el dashboard
        dashboard = ctk.CTkFrame(self.main_frame)
        dashboard.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_content = dashboard
        
        # Título
        ctk.CTkLabel(
            dashboard,
            text="📊 Dashboard",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w", pady=(0, 20))
        
        # Métricas principales
        metricas_frame = ctk.CTkFrame(dashboard)
        metricas_frame.pack(fill="x", pady=10)
        
        insumos = get_insumos()
        insumos_bajos = get_insumos_con_stock_bajo()
        
        metricas = [
            ("Total Insumos", len(insumos), "📦"),
            ("Alertas Stock", len(insumos_bajos), "⚠️"),
            ("Órdenes Pendientes", "3", "📋"),
            ("Lotes Activos", "2", "🌱")
        ]
        
        for titulo, valor, icono in metricas:
            card = ctk.CTkFrame(metricas_frame)
            card.pack(side="left", expand=True, fill="both", padx=10, pady=10)
            
            ctk.CTkLabel(
                card,
                text=icono,
                font=ctk.CTkFont(size=36)
            ).pack(pady=(20, 5))
            
            ctk.CTkLabel(
                card,
                text=str(valor),
                font=ctk.CTkFont(size=32, weight="bold")
            ).pack()
            
            ctk.CTkLabel(
                card,
                text=titulo,
                font=ctk.CTkFont(size=12),
                text_color="gray70"
            ).pack(pady=(0, 20))
        
        # Alertas de stock
        alertas_frame = ctk.CTkFrame(dashboard)
        alertas_frame.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(
            alertas_frame,
            text="⚠️ Alertas de Stock Crítico",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="orange"
        ).pack(anchor="w", padx=20, pady=15)
        
        if insumos_bajos:
            scroll = ctk.CTkScrollableFrame(alertas_frame, height=200)
            scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            for insumo in insumos_bajos:
                alerta = ctk.CTkFrame(scroll, fg_color="gray25")
                alerta.pack(fill="x", pady=5)
                
                texto = f"🔴 {insumo['nombre']}: {insumo['stock_actual']} {insumo['unidad_medida']} (mínimo: {insumo['stock_minimo']})"
                ctk.CTkLabel(
                    alerta,
                    text=texto,
                    text_color="red",
                    font=ctk.CTkFont(size=13)
                ).pack(anchor="w", padx=15, pady=10)
        else:
            ctk.CTkLabel(
                alertas_frame,
                text="✅ No hay alertas de stock. Todo está en orden.",
                text_color="green",
                font=ctk.CTkFont(size=14)
            ).pack(anchor="w", padx=20, pady=10)
    
    def mostrar_inventario(self):
        """Muestra el módulo de inventario"""
        self.limpiar_main_frame()
        
        # Importar dinámicamente el módulo de inventario
        try:
            from inventario import InventarioFrame
            inventario = InventarioFrame(self.main_frame)
            inventario.pack(fill="both", expand=True)
            self.current_content = inventario
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo cargar el módulo de inventario:\n{str(e)}")
            self.mostrar_dashboard()
    
    def mostrar_proyecciones(self):
        """Muestra el módulo de proyecciones"""
        self.limpiar_main_frame()
        
        proyecciones = ctk.CTkFrame(self.main_frame)
        proyecciones.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_content = proyecciones
        
        ctk.CTkLabel(
            proyecciones,
            text="📋 Proyección de Necesidades",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            proyecciones,
            text="Módulo en desarrollo...\n\nAquí se calculará la demanda derivada basada en lotes programados",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        ).pack(pady=50)
    
    def mostrar_ordenes(self):
        """Muestra el módulo de órdenes de compra"""
        self.limpiar_main_frame()
        
        ordenes = ctk.CTkFrame(self.main_frame)
        ordenes.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_content = ordenes
        
        ctk.CTkLabel(
            ordenes,
            text="🛒 Órdenes de Compra",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        ctk.CTkLabel(
            ordenes,
            text="Módulo en desarrollo...\n\nAquí se generarán y gestionarán las órdenes a proveedores",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        ).pack(pady=50)
    
    def mostrar_config(self):
        """Muestra el módulo de configuración"""
        self.limpiar_main_frame()
        
        config = ctk.CTkFrame(self.main_frame)
        config.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_content = config
        
        ctk.CTkLabel(
            config,
            text="⚙️ Configuración",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        # Backup
        backup_frame = ctk.CTkFrame(config)
        backup_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            backup_frame,
            text="💾 Respaldo de Datos",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=15)
        
        ctk.CTkButton(
            backup_frame,
            text="📥 Exportar Backup (.db)",
            command=self.exportar_backup,
            width=200
        ).pack(padx=20, pady=(0, 20))
    
    def exportar_backup(self):
        """Exporta la base de datos"""
        import shutil
        from datetime import datetime
        
        try:
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"vivero_backup_{fecha}.db"
            
            shutil.copy("vivero.db", backup_name)
            
            messagebox.showinfo(
                "Éxito",
                f"✅ Backup creado correctamente:\n\n{backup_name}"
            )
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo crear el backup:\n{str(e)}"
            )
