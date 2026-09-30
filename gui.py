"""
gui.py
Interfaz gráfica opcional (Tkinter, incluido en la librería estándar de Python,
no requiere instalación adicional) para el sistema de inventario.

Ejecutar con:
    python gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from inventario import Inventario
from modelos import ComponenteElectronico, Herramienta, InstrumentoMedicion


class VentanaNuevoComponente(tk.Toplevel):
    """Ventana emergente para registrar un nuevo elemento, según el tipo elegido."""

    def __init__(self, master, inventario, al_guardar):
        super().__init__(master)
        self.inventario = inventario
        self.al_guardar = al_guardar
        self.title("Registrar nuevo elemento")
        self.resizable(False, False)
        self.campos_extra = {}

        self.tipo_var = tk.StringVar(value="Electrónico")
        tk.Label(self, text="Tipo de elemento:").grid(row=0, column=0, sticky="w", padx=8, pady=(10, 2))
        combo = ttk.Combobox(self, textvariable=self.tipo_var, state="readonly",
                              values=["Electrónico", "Herramienta", "Instrumento"])
        combo.grid(row=0, column=1, padx=8, pady=(10, 2))
        combo.bind("<<ComboboxSelected>>", lambda e: self._render_extra())

        self.comunes = {}
        etiquetas = ["ID", "Nombre", "Categoría", "Cantidad", "Ubicación", "Descripción"]
        for i, etiqueta in enumerate(etiquetas, start=1):
            tk.Label(self, text=etiqueta + ":").grid(row=i, column=0, sticky="w", padx=8, pady=2)
            entrada = tk.Entry(self, width=30)
            entrada.grid(row=i, column=1, padx=8, pady=2)
            self.comunes[etiqueta] = entrada

        self.frame_extra = tk.Frame(self)
        self.frame_extra.grid(row=len(etiquetas) + 1, column=0, columnspan=2, pady=4)
        self._render_extra()

        tk.Button(self, text="Guardar", command=self._guardar, bg="#2e7d32", fg="white")\
            .grid(row=len(etiquetas) + 2, column=0, columnspan=2, pady=10)

    def _render_extra(self):
        for widget in self.frame_extra.winfo_children():
            widget.destroy()
        self.campos_extra = {}

        tipo = self.tipo_var.get()
        if tipo == "Electrónico":
            etiquetas = ["Tipo (Resistencia/IC/...)", "Voltaje de operación"]
        elif tipo == "Herramienta":
            etiquetas = ["Estado (Bueno/Regular/Malo)"]
        else:
            etiquetas = ["Calibrado (si/no)", "Fecha última calibración"]

        for i, etiqueta in enumerate(etiquetas):
            tk.Label(self.frame_extra, text=etiqueta + ":").grid(row=i, column=0, sticky="w", padx=4, pady=2)
            entrada = tk.Entry(self.frame_extra, width=28)
            entrada.grid(row=i, column=1, padx=4, pady=2)
            self.campos_extra[etiqueta] = entrada

    def _guardar(self):
        try:
            id_c = self.comunes["ID"].get().strip()
            nombre = self.comunes["Nombre"].get().strip()
            categoria = self.comunes["Categoría"].get().strip()
            cantidad = int(self.comunes["Cantidad"].get() or 0)
            ubicacion = self.comunes["Ubicación"].get().strip()
            descripcion = self.comunes["Descripción"].get().strip()

            if not id_c or not nombre:
                messagebox.showwarning("Datos incompletos", "El ID y el nombre son obligatorios.")
                return

            tipo = self.tipo_var.get()
            if tipo == "Electrónico":
                tipo_e = self.campos_extra["Tipo (Resistencia/IC/...)"].get().strip() or "N/A"
                voltaje = float(self.campos_extra["Voltaje de operación"].get() or 0.0)
                comp = ComponenteElectronico(id_c, nombre, categoria, cantidad,
                                              ubicacion, descripcion, tipo_e, voltaje)
            elif tipo == "Herramienta":
                estado = self.campos_extra["Estado (Bueno/Regular/Malo)"].get().strip() or "Bueno"
                comp = Herramienta(id_c, nombre, categoria, cantidad, ubicacion,
                                    descripcion, estado)
            else:
                calibrado = self.campos_extra["Calibrado (si/no)"].get().strip().lower() in ("si", "sí", "s", "true")
                fecha_cal = self.campos_extra["Fecha última calibración"].get().strip() or "N/A"
                comp = InstrumentoMedicion(id_c, nombre, categoria, cantidad, ubicacion,
                                            descripcion, calibrado, fecha_cal)

            if self.inventario.agregar_componente(comp):
                messagebox.showinfo("Éxito", "Elemento registrado y guardado en inventario.txt")
                self.al_guardar()
                self.destroy()
            else:
                messagebox.showerror("Error", f"Ya existe un elemento con el ID '{id_c}'.")
        except ValueError as e:
            messagebox.showerror("Error de datos", f"Revisa los campos numéricos.\n{e}")


class AppInventario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventario - Laboratorio de Electrónica")
        self.geometry("880x480")
        self.inventario = Inventario("inventario.txt")

        self._construir_barra_superior()
        self._construir_tabla()
        self._refrescar_tabla()

    def _construir_barra_superior(self):
        barra = tk.Frame(self)
        barra.pack(fill="x", padx=8, pady=8)

        tk.Button(barra, text="+ Nuevo elemento", command=self._abrir_nuevo,
                  bg="#1565c0", fg="white").pack(side="left")
        tk.Button(barra, text="Eliminar seleccionado", command=self._eliminar_seleccionado,
                  bg="#c62828", fg="white").pack(side="left", padx=6)
        tk.Button(barra, text="Actualizar cantidad", command=self._actualizar_cantidad_seleccionada)\
            .pack(side="left", padx=6)
        tk.Button(barra, text="Bajo stock (≤5)", command=self._mostrar_bajo_stock)\
            .pack(side="left", padx=6)

        tk.Label(barra, text="Buscar:").pack(side="left", padx=(20, 2))
        self.busqueda_var = tk.StringVar()
        entrada_busqueda = tk.Entry(barra, textvariable=self.busqueda_var, width=20)
        entrada_busqueda.pack(side="left")
        entrada_busqueda.bind("<KeyRelease>", lambda e: self._refrescar_tabla())

    def _construir_tabla(self):
        columnas = ("id", "tipo", "nombre", "categoria", "cantidad", "ubicacion", "detalle")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=16)
        encabezados = {"id": "ID", "tipo": "Tipo", "nombre": "Nombre",
                        "categoria": "Categoría", "cantidad": "Cant.",
                        "ubicacion": "Ubicación", "detalle": "Detalle"}
        anchos = {"id": 70, "tipo": 90, "nombre": 140, "categoria": 110,
                  "cantidad": 60, "ubicacion": 100, "detalle": 220}
        for col in columnas:
            self.tabla.heading(col, text=encabezados[col])
            self.tabla.column(col, width=anchos[col])
        self.tabla.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def _refrescar_tabla(self, lista=None):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        if lista is None:
            texto = self.busqueda_var.get().strip()
            lista = self.inventario.buscar_por_nombre(texto) if texto else self.inventario.listar_todos()

        for c in lista:
            detalle = ""
            if isinstance(c, ComponenteElectronico):
                detalle = f"{c.tipo_electronico}, {c.voltaje_operacion}V"
            elif isinstance(c, Herramienta):
                detalle = f"Estado: {c.estado}"
            elif isinstance(c, InstrumentoMedicion):
                detalle = f"{'Calibrado' if c.calibrado else 'Sin calibrar'} ({c.fecha_calibracion})"
            self.tabla.insert("", "end", values=(c.id_componente, c.TIPO, c.nombre,
                                                  c.categoria, c.cantidad, c.ubicacion, detalle))

    def _fila_seleccionada_id(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un elemento de la tabla primero.")
            return None
        return self.tabla.item(seleccion[0])["values"][0]

    def _abrir_nuevo(self):
        VentanaNuevoComponente(self, self.inventario, self._refrescar_tabla)

    def _eliminar_seleccionado(self):
        id_c = self._fila_seleccionada_id()
        if id_c is None:
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar el elemento con ID '{id_c}'?"):
            self.inventario.eliminar_componente(str(id_c))
            self._refrescar_tabla()

    def _actualizar_cantidad_seleccionada(self):
        id_c = self._fila_seleccionada_id()
        if id_c is None:
            return
        nueva = tk.simpledialog.askinteger("Actualizar cantidad", "Nueva cantidad:", minvalue=0) \
            if hasattr(tk, "simpledialog") else None
        if nueva is None:
            import tkinter.simpledialog as simpledialog
            nueva = simpledialog.askinteger("Actualizar cantidad", "Nueva cantidad:", minvalue=0)
        if nueva is not None:
            self.inventario.actualizar_cantidad(str(id_c), nueva)
            self._refrescar_tabla()

    def _mostrar_bajo_stock(self):
        self._refrescar_tabla(self.inventario.reporte_bajo_stock(5))


if __name__ == "__main__":
    app = AppInventario()
    app.mainloop()
