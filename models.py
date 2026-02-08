from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Insumo:
    """Clase para representar un insumo del inventario"""
    id: Optional[int] = None
    codigo: str = ""
    nombre: str = ""
    categoria: str = "otro"
    stock_actual: float = 0.0
    stock_minimo: float = 0.0
    unidad_medida: str = "unidades"
    proveedor_habitual_id: Optional[int] = None
    fecha_caducidad: Optional[str] = None
    activo: bool = True
    
    def tiene_stock_bajo(self) -> bool:
        """Verifica si el stock está por debajo del mínimo"""
        return self.stock_actual <= self.stock_minimo
    
    def porcentaje_stock(self) -> float:
        """Calcula el porcentaje de stock respecto al mínimo"""
        if self.stock_minimo == 0:
            return 100.0
        return (self.stock_actual / self.stock_minimo) * 100
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'stock_actual': self.stock_actual,
            'stock_minimo': self.stock_minimo,
            'unidad_medida': self.unidad_medida,
            'proveedor_habitual_id': self.proveedor_habitual_id,
            'fecha_caducidad': self.fecha_caducidad,
            'activo': self.activo
        }

@dataclass
class Proveedor:
    """Clase para representar un proveedor"""
    id: Optional[int] = None
    nombre: str = ""
    contacto: str = ""
    telefono: str = ""
    email: str = ""
    categoria: str = ""
    calificacion: float = 0.0
