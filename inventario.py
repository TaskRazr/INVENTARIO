

from persistencia 
import GestorPersistencia


class Inventario:
    def __init__(self, ruta_archivo="inventario.txt"):
        self.persistencia = GestorPersistencia(ruta_archivo)
        self.componentes = self.persistencia.cargar_componentes()

 

    def agregar_componente(self, componente):
        if self.buscar_por_id(componente.id_componente) is not None:
            return False  # ID duplicado
        self.componentes.append(componente)
        self.guardar()
        return True

    def eliminar_componente(self, id_componente):
        componente = self.buscar_por_id(id_componente)
        if componente is None:
            return False
        self.componentes.remove(componente)
        self.guardar()
        return True

    def actualizar_cantidad(self, id_componente, nueva_cantidad):
        componente = self.buscar_por_id(id_componente)
        if componente is None:
            return False
        componente.actualizar_cantidad(nueva_cantidad)
        self.guardar()
        return True



    def buscar_por_id(self, id_componente):
        for c in self.componentes:
            if c.id_componente == str(id_componente):
                return c
        return None

    def buscar_por_categoria(self, categoria):
        categoria = categoria.strip().lower()
        return [c for c in self.componentes if c.categoria.strip().lower() == categoria]

    def buscar_por_nombre(self, texto):
        texto = texto.strip().lower()
        return [c for c in self.componentes if texto in c.nombre.lower()]

    def listar_todos(self):
        return list(self.componentes)


    def reporte_bajo_stock(self, umbral=5):
        return [c for c in self.componentes if c.cantidad <= umbral]



    def guardar(self):
        self.persistencia.guardar_componentes(self.componentes)

    def cargar(self):
        self.componentes = self.persistencia.cargar_componentes()
