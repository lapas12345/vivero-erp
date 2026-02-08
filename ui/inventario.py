import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from database import get_connection, get_insumos

class InventarioFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Título
        titulo = ctk.CTkLabel(
            self,
            text="📦 Gestión de Inventario",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Frame de botones y filtros
        self.crear_barra_herramientas()
        
        # Frame para la tabla
        self.crear_tabla_insumos()
        
        # Cargar datos
        self.cargar_datos()
    
    def crear_barra_herramientas(self):
        """Crea la barra de herramientas con botones y filtros"""
        toolbar = ctk.CTkFrame(self)
        toolbar.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Botones
        btn_nuevo = ctk.CTkButton(
            toolbar,
            text="➕ Nuevo Insumo",
            command=self.abrir_formulario_nuevo,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        btn_nuevo.pack(side="left", padx=5)
        
        btn_refrescar = ctk.CTkButton(
            toolbar,
            text="🔄 Refrescar",
            command=self.cargar_datos,
            fg_color="gray50"
        )
        btn_refrescar.pack(side="left", padx=5)
        
        # Filtro por categoría
        ctk.CTkLabel(toolbar, text="Categoría:").pack(side="left", padx=(20, 5))
        
        self.filtro_categoria = ctk.CTkComboBox(
            toolbar,
            values=["Todas", "sustrato", "fertilizante", "fundas", "herramienta", "otro"],
            command=self.aplicar_filtros,
            width=150
        )
        self.filtro_categoria.set("Todas")
        self.filtro_categoria.pack(side="left", padx=5)
        
        # Filtro por estado
        ctk.CTkLabel(toolbar, text="Estado:").pack(side="left", padx=(20, 5))
        
        self.filtro_estado = ctk.CTkComboBox(
            toolbar,
            values=["Todos", "Stock OK", "Stock Bajo"],
            command=self.aplicar_filtros,
            width=150
        )
        self.filtro_estado.set("Todos")
        self.filtro_estado.pack(side="left", padx=5)
    
    def crear_tabla_insumos(self):
        """Crea la tabla scrollable de insumos"""
        # Frame contenedor
        tabla_container = ctk.CTkFrame(self)
        tabla_container.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        tabla_container.grid_columnconfigure(0, weight=1)
        tabla_container.grid_rowconfigure(1, weight=1)
        
        # Encabezados
        headers_frame = ctk.CTkFrame(tabla_container, fg_color="gray30")
        headers_frame.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        
        headers = [
            ("Código", 0.10),
            ("Nombre", 0.25),
            ("Categoría", 0.15),
            ("Stock", 0.10),
            ("Mínimo", 0.10),
            ("Unidad", 0.10),
            ("Estado", 0.10),
            ("Acciones", 0.10)
        ]
        
        for i, (header, weight) in enumerate(headers):
            label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            label.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        
        # Scrollable frame para los datos
        self.scroll_frame = ctk.CTkScrollableFrame(tabla_container)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
    
    def cargar_datos(self, filtro_categoria=None, filtro_estado=None):
        """Carga los datos de insumos en la tabla"""
        # Limpiar tabla actual
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Obtener insumos
        insumos = get_insumos()
        
        # Aplicar filtros
        if filtro_categoria and filtro_categoria != "Todas":
            insumos = [i for i in insumos if i['categoria'] == filtro_categoria]
        
        if filtro_estado:
            if filtro_estado == "Stock Bajo":
                insumos = [i for i in insumos if i['stock_actual'] <= i['stock_minimo']]
            elif filtro_estado == "Stock OK":
                insumos = [i for i in insumos if i['stock_actual'] > i['stock_minimo']]
        
        # Mostrar insumos
        for idx, insumo in enumerate(insumos):
            self.crear_fila_insumo(insumo, idx)
    
    def crear_fila_insumo(self, insumo, idx):
        """Crea una fila en la tabla con los datos del insumo"""
        # Color alternado
        bg_color = "gray20" if idx % 2 == 0 else "gray25"
        
        fila = ctk.CTkFrame(self.scroll_frame, fg_color=bg_color)
        fila.grid(row=idx, column=0, sticky="ew", pady=1)
        fila.grid_columnconfigure(tuple(range(8)), weight=1)
        
        # Determinar estado
        tiene_stock_bajo = insumo['stock_actual'] <= insumo['stock_minimo']
        estado_texto = "🔴 BAJO" if tiene_stock_bajo else "✅ OK"
        estado_color = "red" if tiene_stock_bajo else "green"
        
        # Columnas
        ctk.CTkLabel(fila, text=insumo['codigo']).grid(row=0, column=0, padx=5, pady=8)
        ctk.CTkLabel(fila, text=insumo['nombre']).grid(row=0, column=1, padx=5, pady=8)
        ctk.CTkLabel(fila, text=insumo['categoria']).grid(row=0, column=2, padx=5, pady=8)
        ctk.CTkLabel(fila, text=str(insumo['stock_actual'])).grid(row=0, column=3, padx=5, pady=8)
        ctk.CTkLabel(fila, text=str(insumo['stock_minimo'])).grid(row=0, column=4, padx=5, pady=8)
        ctk.CTkLabel(fila, text=insumo['unidad_medida']).grid(row=0, column=5, padx=5, pady=8)
        ctk.CTkLabel(fila, text=estado_texto, text_color=estado_color).grid(row=0, column=6, padx=5, pady=8)
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(fila, fg_color="transparent")
        btn_frame.grid(row=0, column=7, padx=5, pady=5)
        
        btn_editar = ctk.CTkButton(
            btn_frame,
            text="✏️",
            width=30,
            command=lambda: self.editar_insumo(insumo),
            fg_color="orange",
            hover_color="darkorange"
        )
        btn_editar.pack(side="left", padx=2)
        
        btn_eliminar = ctk.CTkButton(
            btn_frame,
            text="🗑️",
            width=30,
            command=lambda: self.eliminar_insumo(insumo),
            fg_color="red",
            hover_color="darkred"
        )
        btn_eliminar.pack(side="left", padx=2)
    
    def aplicar_filtros(self, *args):
        """Aplica los filtros seleccionados"""
        categoria = self.filtro_categoria.get()
        estado = self.filtro_estado.get()
        self.cargar_datos(categoria, estado)
    
    def abrir_formulario_nuevo(self):
        """Abre ventana para crear nuevo insumo"""
        FormularioInsumo(self, modo="nuevo")
    
    def editar_insumo(self, insumo):
        """Abre ventana para editar insumo"""
        FormularioInsumo(self, modo="editar", insumo=insumo)
    
    def eliminar_insumo(self, insumo):
        """Elimina un insumo (desactivación lógica)"""
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el insumo '{insumo['nombre']}'?\n\nEsta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Desactivación lógica
                cursor.execute("""
                    UPDATE insumos SET activo = 0 WHERE id = ?
                """, (insumo['id'],))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Éxito", "Insumo eliminado correctamente")
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el insumo:\n{str(e)}")


class FormularioInsumo(ctk.CTkToplevel):
    """Ventana modal para crear o editar insumos"""
    
    def __init__(self, parent, modo="nuevo", insumo=None):
        super().__init__(parent)
        
        self.parent = parent
        self.modo = modo
        self.insumo = insumo
        
        # Configuración de la ventana
        titulo = "Nuevo Insumo" if modo == "nuevo" else "Editar Insumo"
        self.title(titulo)
        self.geometry("500x600")
        
        # Centrar ventana
        self.transient(parent)
        self.grab_set()
        
        self.crear_formulario()
        
        # Si es edición, cargar datos
        if modo == "editar" and insumo:
            self.cargar_datos_insumo()
    
    def crear_formulario(self):
        """Crea el formulario de insumo"""
        # Título
        titulo = ctk.CTkLabel(
            self,
            text="📝 Datos del Insumo",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=20)
        
        # Frame del formulario
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Código
        ctk.CTkLabel(form_frame, text="Código:").pack(anchor="w", padx=20, pady=(10, 0))
        self.entry_codigo = ctk.CTkEntry(form_frame, placeholder_text="Ej: SUS-001")
        self.entry_codigo.pack(fill="x", padx=20, pady=5)
        
        # Nombre
        ctk.CTkLabel(form_frame, text="Nombre:").pack(anchor="w", padx=20, pady=(10, 0))
        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Ej: Sustrato Premium")
        self.entry_nombre.pack(fill="x", padx=20, pady=5)
        
        # Categoría
        ctk.CTkLabel(form_frame, text="Categoría:").pack(anchor="w", padx=20, pady=(10, 0))
        self.combo_categoria = ctk.CTkComboBox(
            form_frame,
            values=["sustrato", "fertilizante", "fundas", "herramienta", "otro"]
        )
        self.combo_categoria.pack(fill="x", padx=20, pady=5)
        
        # Stock actual
        ctk.CTkLabel(form_frame, text="Stock Actual:").pack(anchor="w", padx=20, pady=(10, 0))
        self.entry_stock = ctk.CTkEntry(form_frame, placeholder_text="0.0")
        self.entry_stock.pack(fill="x", padx=20, pady=5)
        
        # Stock mínimo
        ctk.CTkLabel(form_frame, text="Stock Mínimo:").pack(anchor="w", padx=20, pady=(10, 0))
        self.entry_minimo = ctk.CTkEntry(form_frame, placeholder_text="0.0")
        self.entry_minimo.pack(fill="x", padx=20, pady=5)
        
        # Unidad de medida
        ctk.CTkLabel(form_frame, text="Unidad de Medida:").pack(anchor="w", padx=20, pady=(10, 0))
        self.combo_unidad = ctk.CTkComboBox(
            form_frame,
            values=["kg", "unidades", "litros", "sacos", "cajas", "metros"]
        )
        self.combo_unidad.pack(fill="x", padx=20, pady=5)
        
        # Fecha de caducidad (opcional)
        ctk.CTkLabel(form_frame, text="Fecha Caducidad (opcional):").pack(anchor="w", padx=20, pady=(10, 0))
        self.entry_caducidad = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD")
        self.entry_caducidad.pack(fill="x", padx=20, pady=5)
        
        # Botones
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        btn_guardar = ctk.CTkButton(
            btn_frame,
            text="💾 Guardar",
            command=self.guardar,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            width=150
        )
        btn_guardar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=self.destroy,
            fg_color="gray50",
            width=150
        )
        btn_cancelar.pack(side="left", padx=10)
    
    def cargar_datos_insumo(self):
        """Carga los datos del insumo en el formulario"""
        self.entry_codigo.insert(0, self.insumo['codigo'])
        self.entry_nombre.insert(0, self.insumo['nombre'])
        self.combo_categoria.set(self.insumo['categoria'])
        self.entry_stock.insert(0, str(self.insumo['stock_actual']))
        self.entry_minimo.insert(0, str(self.insumo['stock_minimo']))
        self.combo_unidad.set(self.insumo['unidad_medida'])
        
        if self.insumo['fecha_caducidad']:
            self.entry_caducidad.insert(0, self.insumo['fecha_caducidad'])
    
    def validar_formulario(self):
        """Valida los datos del formulario"""
        if not self.entry_codigo.get().strip():
            messagebox.showerror("Error", "El código es obligatorio")
            return False
        
        if not self.entry_nombre.get().strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return False
        
        try:
            float(self.entry_stock.get())
            float(self.entry_minimo.get())
        except ValueError:
            messagebox.showerror("Error", "Stock actual y mínimo deben ser números")
            return False
        
        return True
    
    def guardar(self):
        """Guarda el insumo en la base de datos"""
        if not self.validar_formulario():
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            datos = (
                self.entry_codigo.get().strip(),
                self.entry_nombre.get().strip(),
                self.combo_categoria.get(),
                float(self.entry_stock.get()),
                float(self.entry_minimo.get()),
                self.combo_unidad.get(),
                self.entry_caducidad.get().strip() or None
            )
            
            if self.modo == "nuevo":
                cursor.execute("""
                    INSERT INTO insumos (codigo, nombre, categoria, stock_actual, stock_minimo, unidad_medida, fecha_caducidad)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, datos)
                mensaje = "Insumo creado correctamente"
            else:
                cursor.execute("""
                    UPDATE insumos 
                    SET codigo=?, nombre=?, categoria=?, stock_actual=?, stock_minimo=?, unidad_medida=?, fecha_caducidad=?
                    WHERE id=?
                """, datos + (self.insumo['id'],))
                mensaje = "Insumo actualizado correctamente"
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Éxito", mensaje)
            self.parent.cargar_datos()
            self.destroy()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe un insumo con ese código")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el insumo:\n{str(e)}")
