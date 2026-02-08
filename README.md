# 🌱 Sistema ERP - Vivero de Cacao ULEAM

Sistema de gestión de logística de aprovisionamiento para viveros de cacao.

## 📋 Características Implementadas

### ✅ Módulo de Inventario (COMPLETO)
- Visualización de todos los insumos en tabla interactiva
- Agregar nuevos insumos con validación
- Editar insumos existentes
- Eliminar insumos (desactivación lógica)
- Filtros por categoría y estado de stock
- Alertas visuales de stock bajo
- Interfaz moderna con CustomTkinter

### 🔄 Dashboard
- Métricas principales (total insumos, alertas, órdenes, lotes)
- Panel de alertas de stock crítico
- Vista rápida del estado del sistema

### 🚧 En Desarrollo
- Módulo de Proyecciones (demanda derivada)
- Módulo de Órdenes de Compra
- Gestión de Proveedores
- Gestión de Lotes

## 🛠️ Instalación

### 1. Instalar dependencias

```bash
pip install customtkinter
```

### 2. Estructura de archivos

Asegúrate de tener esta estructura:

```
vivero-erp/
├── main.py              # Punto de entrada
├── database.py          # Conexión y operaciones con SQLite
├── models.py            # Clases de datos (Insumo, Orden, etc.)
├── ui/
│   ├── __init__.py
│   ├── main_window.py   # Ventana principal
│   └── inventario.py    # Pantalla de inventario
└── vivero.db           # Base de datos (se crea automáticamente)
```

### 3. Configurar archivos

#### Coloca los archivos descargados así:

- `models.py` → Raíz del proyecto
- `main_window.py` → Dentro de la carpeta `ui/`
- `inventario.py` → Dentro de la carpeta `ui/`

#### Crea un archivo `ui/__init__.py` vacío:

```bash
type nul > ui\__init__.py
```

(En Linux/Mac: `touch ui/__init__.py`)

## 🚀 Ejecutar el Sistema

```bash
python main.py
```

O si tienes Python 3:

```bash
py main.py
```

## 📦 Uso del Módulo de Inventario

### Agregar Insumo
1. Click en "📦 Inventario" en el menú lateral
2. Click en "➕ Nuevo Insumo"
3. Llenar el formulario:
   - **Código**: Identificador único (Ej: SUS-001)
   - **Nombre**: Nombre del insumo
   - **Categoría**: sustrato, fertilizante, fundas, herramienta, otro
   - **Stock Actual**: Cantidad disponible
   - **Stock Mínimo**: Nivel de alerta
   - **Unidad**: kg, unidades, litros, etc.
   - **Fecha Caducidad**: (Opcional) YYYY-MM-DD
4. Click en "💾 Guardar"

### Editar Insumo
1. En la tabla de inventario, click en el botón "✏️" del insumo
2. Modificar los datos necesarios
3. Click en "💾 Guardar"

### Eliminar Insumo
1. En la tabla de inventario, click en el botón "🗑️" del insumo
2. Confirmar la eliminación
3. El insumo se desactiva (no se borra físicamente)

### Filtros
- **Por Categoría**: Filtra por tipo de insumo
- **Por Estado**: 
  - "Stock OK" → Insumos con stock suficiente
  - "Stock Bajo" → Insumos en alerta (stock ≤ mínimo)

## 🎨 Interfaz

- **Tema oscuro** por defecto (moderno y profesional)
- **Colores de estado**:
  - 🟢 Verde: Stock OK
  - 🔴 Rojo: Stock bajo
  - 🟠 Naranja: Alertas
- **Tabla responsive** con scroll automático
- **Formularios modales** para operaciones

## 🔧 Configuración

### Cambiar a tema claro

En `main_window.py`, línea 14:
```python
ctk.set_appearance_mode("light")  # Cambiar de "dark" a "light"
```

### Backup de Base de Datos

1. Click en "⚙️ Configuración"
2. Click en "📥 Exportar Backup (.db)"
3. Se creará un archivo `vivero_backup_YYYYMMDD_HHMMSS.db`

## 📊 Base de Datos

El sistema usa SQLite con las siguientes tablas principales:

- **insumos**: Inventario de materiales
- **fases**: Fases del proceso de cultivo
- **lotes**: Grupos de plantas en producción
- **proveedores**: Datos de proveedores
- **ordenes_compra**: Órdenes de aprovisionamiento

## 🐛 Solución de Problemas

### Error: "No module named 'customtkinter'"
```bash
pip install customtkinter
```

### Error: "No se pudo cargar el módulo de inventario"
Verifica que:
1. La carpeta `ui/` existe
2. Dentro de `ui/` están los archivos:
   - `__init__.py` (puede estar vacío)
   - `main_window.py`
   - `inventario.py`

### La base de datos no se crea
Asegúrate de ejecutar desde la raíz del proyecto donde está `main.py`

## 📝 Próximas Funcionalidades

- [ ] Módulo de Proyecciones (demanda derivada)
- [ ] Gestión de Lotes y Cronogramas
- [ ] Generación automática de órdenes de compra
- [ ] Reportes en PDF/Excel
- [ ] Gráficos de tendencias
- [ ] Sistema de alertas por email
- [ ] Gestión de usuarios y permisos

## 👨‍💻 Desarrollado por

ULEAM - Universidad Laica Eloy Alfaro de Manabí  
Facultad de Ingeniería

---

**Versión**: 1.0.0  
**Fecha**: Febrero 2026
