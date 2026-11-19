# Aporte individual: disponibilidad de recursos

## Objetivo
Agregar una funcionalidad complementaria al sistema Software FJ: verificar que un recurso (por ejemplo, una sala o un equipo) no tenga otra reserva activa en el mismo intervalo horario.

## Archivos
- `disponibilidad_recursos.py`: clases, validaciones y demostración.
- `logs/`: carpeta para el archivo de eventos `disponibilidad.log`.

## Requisitos
Python 3.8 o superior. No utiliza librerías externas ni bases de datos.

## Ejecución en Visual Studio Code
```bash
python disponibilidad_recursos.py
```

## Pruebas
El programa presenta diez escenarios válidos e inválidos: reserva aceptada, cruce de horario, otro recurso, duración cero y negativa, fecha inválida, código vacío, registro de otra reserva, código duplicado y reserva en otro horario.

## Integración segura
Este aporte no modifica los archivos existentes del equipo (`cliente.py`, `servicio.py`, `reserva.py` o `main.py`). Se propone añadirlo como módulo independiente y solicitar revisión antes de integrarlo.

## Rama y publicación
Partiendo de la rama principal actualizada:
```bash
git switch main
git pull origin main
git switch -c feature/disponibilidad-recursos
```
Copiar estos archivos a una carpeta nueva, por ejemplo `aporte_disponibilidad/`, y luego:
```bash
git add aporte_disponibilidad/
git commit -m "feat: agrega validacion de disponibilidad de recursos"
git push -u origin feature/disponibilidad-recursos
```
Finalmente, abrir un Pull Request hacia la rama principal para revisión del equipo. No realizar merge directamente.
