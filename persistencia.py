"""
persistencia.py
Responsable exclusivamente de leer y escribir el inventario en un archivo .txt.
Separar esta responsabilidad de Inventario sigue el principio de responsabilidad
única (S de SOLID) y facilita cambiar el mecanismo de persistencia en el futuro
(por ejemplo a JSON o a una base de datos) sin tocar la lógica de negocio.
"""

import os
from modelos import Componente


class GestorPersistencia:
    def __init__(self, ruta_archivo="inventario.txt"):
        self.ruta_archivo = ruta_archivo

    def guardar_componentes(self, componentes):
        """Escribe todos los componentes en el archivo, uno por línea."""
        with open(self.ruta_archivo, "w", encoding="utf-8") as f:
            for componente in componentes:
                f.write(componente.to_linea() + "\n")

    def cargar_componentes(self):
        """Lee el archivo y reconstruye la lista de objetos Componente."""
        componentes = []
        if not os.path.exists(self.ruta_archivo):
            return componentes

        with open(self.ruta_archivo, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    componentes.append(Componente.from_linea(linea))
                except (IndexError, ValueError):
                    # Línea corrupta o con formato inválido: se ignora
                    continue
        return componentes
