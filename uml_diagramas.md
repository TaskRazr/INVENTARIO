# Diagramas UML — Sistema de Gestión de Inventario de Laboratorio de Electrónica

Los diagramas están en sintaxis **Mermaid**. Se pueden visualizar en GitHub, VS Code (extensión Mermaid), o en https://mermaid.live/

---

## 1. Diagrama de Casos de Uso

```mermaid
flowchart TB
    Actor((Encargado del<br/>Laboratorio))

    subgraph Sistema["Sistema de Gestión de Inventario"]
        UC1[Registrar componente]
        UC2[Consultar componente]
        UC3[Actualizar cantidad]
        UC4[Eliminar componente]
        UC5[Buscar por categoría]
        UC6[Generar reporte de<br/>bajo stock]
        UC7[Listar todo el<br/>inventario]
        UC8[Guardar inventario<br/>en archivo .txt]
        UC9[Cargar inventario<br/>desde archivo .txt]
    end

    Actor --> UC1
    Actor --> UC2
    Actor --> UC3
    Actor --> UC4
    Actor --> UC5
    Actor --> UC6
    Actor --> UC7

    UC1 -.include.-> UC8
    UC3 -.include.-> UC8
    UC4 -.include.-> UC8
    UC2 -.include.-> UC9
    UC5 -.include.-> UC9
    UC7 -.include.-> UC9
```

**Descripción de actores:** el único actor es el *Encargado del Laboratorio*, responsable de mantener actualizado el inventario de componentes electrónicos, herramientas e instrumentos de medición.

---

## 2. Diagrama de Clases

```mermaid
classDiagram
    class Componente {
        <<abstract>>
        -id_componente: str
        -nombre: str
        -categoria: str
        -cantidad: int
        -ubicacion: str
        -descripcion: str
        -fecha_registro: str
        +actualizar_cantidad(cantidad: int)
        +to_linea() str
        +from_linea(linea: str)$
        +__str__() str
    }

    class ComponenteElectronico {
        -tipo: str
        -voltaje_operacion: float
        +to_linea() str
        +__str__() str
    }

    class Herramienta {
        -estado: str
        +to_linea() str
        +__str__() str
    }

    class InstrumentoMedicion {
        -calibrado: bool
        -fecha_calibracion: str
        +to_linea() str
        +__str__() str
    }

    class Inventario {
        -componentes: List~Componente~
        -persistencia: GestorPersistencia
        +agregar_componente(c: Componente) bool
        +eliminar_componente(id: str) bool
        +buscar_por_id(id: str) Componente
        +buscar_por_categoria(categoria: str) List~Componente~
        +actualizar_cantidad(id: str, cantidad: int) bool
        +listar_todos() List~Componente~
        +reporte_bajo_stock(umbral: int) List~Componente~
        +guardar()
        +cargar()
    }

    class GestorPersistencia {
        -ruta_archivo: str
        +guardar_componentes(componentes: List~Componente~)
        +cargar_componentes() List~Componente~
    }

    Componente <|-- ComponenteElectronico
    Componente <|-- Herramienta
    Componente <|-- InstrumentoMedicion
    Inventario "1" o-- "*" Componente : contiene
    Inventario "1" *-- "1" GestorPersistencia : usa
```

**Notas de diseño:**
- `Componente` es la clase base (herencia) que define atributos y comportamiento comunes.
- Las subclases (`ComponenteElectronico`, `Herramienta`, `InstrumentoMedicion`) demuestran **polimorfismo**: cada una serializa (`to_linea`) y se representa (`__str__`) de forma distinta.
- `Inventario` usa **composición** con `GestorPersistencia` para delegar la lectura/escritura del archivo `.txt`, separando responsabilidades (principio de responsabilidad única).

---

## 3. Diagrama de Secuencia — Registrar un nuevo componente

```mermaid
sequenceDiagram
    actor U as Encargado
    participant GUI as Interfaz (CLI/GUI)
    participant INV as Inventario
    participant COMP as Componente (subclase)
    participant PER as GestorPersistencia
    participant TXT as inventario.txt

    U->>GUI: Ingresa datos del nuevo componente
    GUI->>COMP: new ComponenteElectronico(...)
    COMP-->>GUI: objeto creado
    GUI->>INV: agregar_componente(componente)
    INV->>INV: valida que el id no exista
    alt id ya existe
        INV-->>GUI: retorna False
        GUI-->>U: muestra error "ID duplicado"
    else id disponible
        INV->>INV: componentes.append(componente)
        INV->>PER: guardar_componentes(componentes)
        loop por cada componente
            PER->>COMP: to_linea()
            COMP-->>PER: línea serializada
        end
        PER->>TXT: escribe todas las líneas
        TXT-->>PER: escritura confirmada
        PER-->>INV: guardado exitoso
        INV-->>GUI: retorna True
        GUI-->>U: muestra "Componente registrado"
    end
```

---

## 4. Diagrama de Secuencia — Consultar / Buscar por categoría

```mermaid
sequenceDiagram
    actor U as Encargado
    participant GUI as Interfaz (CLI/GUI)
    participant INV as Inventario
    participant TXT as inventario.txt

    U->>GUI: Solicita ver componentes de una categoría
    GUI->>INV: buscar_por_categoria("Resistencias")
    INV->>INV: filtra self.componentes
    INV-->>GUI: lista de Componente
    GUI-->>U: muestra resultados en tabla/consola
    Note over INV,TXT: El inventario ya está cargado en memoria<br/>(se leyó de inventario.txt al iniciar la app)
```
