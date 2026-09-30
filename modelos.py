"""
modelos.py
Clases del dominio para el sistema de inventario del laboratorio de electrónica.

Jerarquía de clases (herencia):
    Componente (clase base)
        ├── ComponenteElectronico
        ├── Herramienta
        └── InstrumentoMedicion

Cada subclase sobreescribe to_linea() y __str__() (polimorfismo) para
serializarse y mostrarse de forma distinta según su naturaleza.
"""

from datetime import datetime

SEPARADOR = "|"  # separador de campos usado en el archivo .txt


class Componente:
    """Clase base para cualquier elemento del inventario."""

    TIPO = "COMPONENTE"

    def __init__(self, id_componente, nombre, categoria, cantidad,
                 ubicacion, descripcion="", fecha_registro=None):
        self.id_componente = str(id_componente)
        self.nombre = nombre
        self.categoria = categoria
        self.cantidad = int(cantidad)
        self.ubicacion = ubicacion
        self.descripcion = descripcion
        self.fecha_registro = fecha_registro or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def actualizar_cantidad(self, nueva_cantidad):
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.cantidad = int(nueva_cantidad)

    def to_linea(self):
        """Serializa el objeto a una línea de texto plano."""
        campos = [self.TIPO, self.id_componente, self.nombre, self.categoria,
                  str(self.cantidad), self.ubicacion, self.descripcion,
                  self.fecha_registro]
        return SEPARADOR.join(campos)

    @staticmethod
    def from_linea(linea):
        """
        Fábrica: reconstruye el objeto correcto (subclase) a partir de una
        línea de texto, según el prefijo de tipo guardado al inicio.
        """
        campos = linea.rstrip("\n").split(SEPARADOR)
        tipo = campos[0]

        if tipo == ComponenteElectronico.TIPO:
            return ComponenteElectronico(
                id_componente=campos[1], nombre=campos[2], categoria=campos[3],
                cantidad=campos[4], ubicacion=campos[5], descripcion=campos[6],
                tipo_electronico=campos[7], voltaje_operacion=campos[8],
                fecha_registro=campos[9],
            )
        elif tipo == Herramienta.TIPO:
            return Herramienta(
                id_componente=campos[1], nombre=campos[2], categoria=campos[3],
                cantidad=campos[4], ubicacion=campos[5], descripcion=campos[6],
                estado=campos[7], fecha_registro=campos[8],
            )
        elif tipo == InstrumentoMedicion.TIPO:
            return InstrumentoMedicion(
                id_componente=campos[1], nombre=campos[2], categoria=campos[3],
                cantidad=campos[4], ubicacion=campos[5], descripcion=campos[6],
                calibrado=campos[7], fecha_calibracion=campos[8],
                fecha_registro=campos[9],
            )
        else:
            return Componente(
                id_componente=campos[1], nombre=campos[2], categoria=campos[3],
                cantidad=campos[4], ubicacion=campos[5], descripcion=campos[6],
                fecha_registro=campos[7],
            )

    def __str__(self):
        return (f"[{self.TIPO}] ID: {self.id_componente} | {self.nombre} "
                f"| Categoría: {self.categoria} | Cant.: {self.cantidad} "
                f"| Ubicación: {self.ubicacion}")


class ComponenteElectronico(Componente):
    """Ej: resistencias, capacitores, circuitos integrados, transistores."""

    TIPO = "ELECTRONICO"

    def __init__(self, id_componente, nombre, categoria, cantidad, ubicacion,
                 descripcion="", tipo_electronico="N/A", voltaje_operacion=0.0,
                 fecha_registro=None):
        super().__init__(id_componente, nombre, categoria, cantidad,
                          ubicacion, descripcion, fecha_registro)
        self.tipo_electronico = tipo_electronico  # p.ej. "Resistencia", "IC"
        self.voltaje_operacion = float(voltaje_operacion)

    def to_linea(self):
        campos = [self.TIPO, self.id_componente, self.nombre, self.categoria,
                  str(self.cantidad), self.ubicacion, self.descripcion,
                  self.tipo_electronico, str(self.voltaje_operacion),
                  self.fecha_registro]
        return SEPARADOR.join(campos)

    def __str__(self):
        return (super().__str__() +
                f" | Tipo: {self.tipo_electronico} | Voltaje: {self.voltaje_operacion}V")


class Herramienta(Componente):
    """Ej: destornilladores, cautines, pinzas, pistolas de aire caliente."""

    TIPO = "HERRAMIENTA"

    def __init__(self, id_componente, nombre, categoria, cantidad, ubicacion,
                 descripcion="", estado="Bueno", fecha_registro=None):
        super().__init__(id_componente, nombre, categoria, cantidad,
                          ubicacion, descripcion, fecha_registro)
        self.estado = estado  # "Bueno", "Regular", "Malo"

    def to_linea(self):
        campos = [self.TIPO, self.id_componente, self.nombre, self.categoria,
                  str(self.cantidad), self.ubicacion, self.descripcion,
                  self.estado, self.fecha_registro]
        return SEPARADOR.join(campos)

    def __str__(self):
        return super().__str__() + f" | Estado: {self.estado}"


class InstrumentoMedicion(Componente):
    """Ej: multímetros, osciloscopios, fuentes de voltaje, generadores."""

    TIPO = "INSTRUMENTO"

    def __init__(self, id_componente, nombre, categoria, cantidad, ubicacion,
                 descripcion="", calibrado=True, fecha_calibracion=None,
                 fecha_registro=None):
        super().__init__(id_componente, nombre, categoria, cantidad,
                          ubicacion, descripcion, fecha_registro)
        if isinstance(calibrado, str):
            calibrado = calibrado.strip().lower() in ("true", "1", "si", "sí")
        self.calibrado = bool(calibrado)
        self.fecha_calibracion = fecha_calibracion or "N/A"

    def to_linea(self):
        campos = [self.TIPO, self.id_componente, self.nombre, self.categoria,
                  str(self.cantidad), self.ubicacion, self.descripcion,
                  str(self.calibrado), self.fecha_calibracion, self.fecha_registro]
        return SEPARADOR.join(campos)

    def __str__(self):
        estado_cal = "Calibrado" if self.calibrado else "Sin calibrar"
        return super().__str__() + f" | {estado_cal} (últ.: {self.fecha_calibracion})"
