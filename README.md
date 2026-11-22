# Software FJ – Management System

## Descripción del proyecto

Software FJ – Management System es una aplicación de escritorio desarrollada en Python para gestionar clientes, servicios y reservas. El sistema cuenta con una interfaz gráfica construida con Tkinter y aplica conceptos de programación orientada a objetos (POO).

El proyecto fue desarrollado colaborativamente, integrando diferentes módulos para ampliar las funcionalidades del sistema y facilitar la administración de la información.

## Objetivo general

Desarrollar un sistema de gestión que permita administrar clientes, servicios y reservas, incorporando validaciones, manejo de excepciones, registro de eventos y herramientas de consulta para facilitar el control de las operaciones.

## Funcionalidades principales

- Registro y administración de clientes.
- Creación y gestión de servicios.
- Administración de reservas.
- Cálculo automático de costos.
- Validación de datos ingresados.
- Manejo de excepciones personalizadas.
- Registro de eventos mediante logging.
- Inicio de sesión para el acceso al sistema.
- Consulta de estadísticas y resumen financiero.
- Gestión de disponibilidad de recursos.

## Tecnologías utilizadas

- **Python 3**
- **Tkinter:** desarrollo de la interfaz gráfica.
- **Logging:** registro de eventos y errores.
- **Programación orientada a objetos:** organización del código mediante clases, métodos y herencia.
- **Git y GitHub:** control de versiones y trabajo colaborativo.

## Integrantes y aportes

### 1. Edisson Alejandro Castaneda Bermudez

- Desarrolló y estableció la estructura inicial del proyecto.
- Implementó la base principal del código y la organización de sus componentes.
- Desarrolló las clases principales para la gestión de clientes, servicios y reservas.
- Implementó los cálculos de costos y las validaciones correspondientes.
- Incorporó el manejo de excepciones y el registro de eventos.
- Desarrolló la interfaz gráfica principal utilizando Tkinter.
- Implementó pruebas para verificar el funcionamiento de las funcionalidades iniciales.

### 2. Jhon Jairo Rodriguez Herrera

- Desarrolló el módulo de inicio de sesión (Login).
- Implementó la ventana de acceso mediante Tkinter.
- Creó las funciones `open_login_window` y `validate_login`.
- Incorporó la validación de credenciales para controlar el acceso al sistema.
- Integró el manejo de excepciones y el registro de eventos mediante logging.
- Realizó pruebas de funcionamiento y revisión de errores durante la integración del módulo.

### 3. Sara Valeria Valenzuela Cantor

- Desarrolló el módulo de estadísticas del sistema.
- Implementó la función `open_stats_window`.
- Incorporó una ventana para consultar el resumen general y financiero.
- Agregó indicadores como el total de clientes, total de servicios, reservas confirmadas e ingresos generados por las reservas confirmadas.
- Integró el acceso a las estadísticas mediante un botón en el menú principal.

### 4. Juan Diego Rodriguez Jacome

- Desarrolló un módulo independiente para la gestión de disponibilidad de recursos.
- Implementó las clases `ReservaRecurso` y `GestorDisponibilidad`.
- Incorporó validaciones para fechas, duración y códigos de reserva.
- Implementó la detección de cruces o superposiciones de reservas para un mismo recurso.
- Agregó funcionalidades para registrar y cancelar reservas.
- Incorporó excepciones personalizadas y registro de eventos mediante logging.
- Desarrolló una demostración con diferentes escenarios para comprobar el funcionamiento del módulo.

## Estructura del proyecto

```text
software-fj-management-system/
│
├── software_fj_management_system.py
│
├── aporte_rama_disponibilidad/
│   └── disponibilidad_recursos.py
│
├── system.log
│
└── README.md
```

*La estructura puede variar dependiendo de la integración final de las ramas y los archivos del proyecto.*

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/EACBDEV/software-fj-management-system.git
```

### 2. Ingresar a la carpeta del proyecto

```bash
cd software-fj-management-system
```

### 3. Ejecutar el sistema principal

```bash
python software_fj_management_system.py
```

### 4. Ejecutar el módulo independiente de disponibilidad

```bash
python aporte_rama_disponibilidad/disponibilidad_recursos.py
```

## Conceptos de programación aplicados

Durante el desarrollo se aplicaron diferentes conceptos de programación:

- **Clases y objetos:** para representar clientes, servicios, reservas y recursos.
- **Herencia:** para organizar los diferentes tipos de servicios.
- **Encapsulamiento:** para estructurar y controlar los datos y comportamientos de los componentes.
- **Manejo de excepciones:** para controlar errores y situaciones inesperadas.
- **Validaciones:** para garantizar que los datos ingresados cumplan las condiciones establecidas.
- **Logging:** para registrar eventos y facilitar la identificación de errores.
- **Interfaces gráficas:** para permitir la interacción del usuario con el sistema.

## Pruebas

El proyecto incorpora pruebas para verificar el funcionamiento de sus componentes, incluyendo la gestión de clientes, servicios, reservas, validaciones y manejo de errores.

También se desarrollaron pruebas para los módulos adicionales de inicio de sesión, estadísticas y disponibilidad de recursos.

## Repositorio

GitHub: https://github.com/EACBDEV/software-fj-management-system

## Conclusión

El desarrollo de Software FJ – Management System permitió aplicar conocimientos de Python, programación orientada a objetos, interfaces gráficas, validaciones y manejo de excepciones. Además, el trabajo colaborativo permitió dividir las responsabilidades entre los integrantes e integrar diferentes funcionalidades para construir un sistema de gestión más completo.
