# Sistema de Gestión de Inventario — Laboratorio de Electrónica

Proyecto en Python (POO) para administrar el inventario de un laboratorio de
electrónica: componentes electrónicos, herramientas e instrumentos de medición.
La información persiste en un archivo de texto plano (`inventario.txt`).

## Archivos

| Archivo               | Contenido                                                         |
|------------------------|--------------------------------------------------------------------|
| `uml_diagramas.md`     | Diagrama de casos de uso, de clases y de secuencia (Mermaid)       |
| `modelos.py`           | Clases `Componente`, `ComponenteElectronico`, `Herramienta`, `InstrumentoMedicion` |
| `persistencia.py`      | Clase `GestorPersistencia` (lectura/escritura del `.txt`)          |
| `inventario.py`        | Clase `Inventario` (lógica de negocio: CRUD, búsquedas, reportes)  |
| `main.py`              | Interfaz de consola (CLI)                                          |
| `gui.py`               | Interfaz gráfica opcional (Tkinter)                                |
| `inventario.txt`       | Se genera automáticamente al guardar el primer elemento            |

## Requisitos

Solo Python 3 (no se necesitan librerías externas; Tkinter viene incluido en
la instalación estándar de Python en Windows/Mac; en Linux puede requerir
`sudo apt install python3-tk`).

## Ejecutar

**Modo consola:**
```bash
python main.py
```

**Modo gráfico:**
```bash
python gui.py
```

## Formato de persistencia (`inventario.txt`)

Cada línea representa un elemento, con campos separados por `|`. El primer
campo indica el tipo (`ELECTRONICO`, `HERRAMIENTA`, `INSTRUMENTO`), lo que
permite reconstruir la subclase correcta al cargar el archivo (patrón
"fábrica" en `Componente.from_linea`).

Ejemplo:
```
ELECTRONICO|R001|Resistencia 220ohm|Resistencias|150|Gaveta A1|1/4W|Resistencia|5.0|2026-09-24 10:00:00
HERRAMIENTA|H001|Cautín 40W|Eléctrica|3|Estante B||Bueno|2026-09-24 10:01:00
INSTRUMENTO|I001|Multímetro Fluke 115|Medición|2|Gabinete C||True|2026-01-10|2026-09-24 10:02:00
```

## Diseño orientado a objetos

- **Herencia:** `ComponenteElectronico`, `Herramienta` e `InstrumentoMedicion`
  heredan de `Componente`.
- **Polimorfismo:** cada subclase sobreescribe `to_linea()` y `__str__()`.
- **Composición:** `Inventario` usa un `GestorPersistencia` en lugar de
  heredar de él, separando la lógica de negocio del almacenamiento.
- **Encapsulamiento:** las validaciones (p. ej. cantidad no negativa) están
  dentro de los métodos de la propia clase.
