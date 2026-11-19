"""
APORTE INDIVIDUAL PARA SOFTWARE FJ
Tema: Verificación básica de disponibilidad de recursos antes de reservar.

Este módulo es independiente: no modifica cliente.py, servicio.py, reserva.py
ni main.py. Puede incorporarse en una rama nueva y revisarse mediante Pull Request.
"""

from datetime import datetime, timedelta
import logging
from pathlib import Path

# Los eventos se guardan en un log propio para no interferir con el log del equipo.
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logger = logging.getLogger("disponibilidad_recursos")
logger.setLevel(logging.INFO)

if not logger.handlers:
    archivo = logging.FileHandler(LOG_DIR / "disponibilidad.log", encoding="utf-8")
    archivo.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    ))
    logger.addHandler(archivo)


# Excepciones específicas del módulo.
class ErrorDisponibilidad(Exception):
    """Error general al consultar o registrar disponibilidad."""


class FechaReservaInvalida(ErrorDisponibilidad):
    """La fecha ingresada no tiene el formato correcto."""


class DuracionReservaInvalida(ErrorDisponibilidad):
    """La duración debe ser un número positivo."""


class ConflictoHorario(ErrorDisponibilidad):
    """El recurso ya está ocupado durante el intervalo solicitado."""


class ReservaRecurso:
    """Representa el uso de un recurso en un intervalo de tiempo."""

    FORMATO = "%Y-%m-%d %H:%M"

    def __init__(self, codigo, recurso, fecha_inicio, horas):
        if not codigo.strip() or not recurso.strip():
            raise ErrorDisponibilidad("El código y el recurso son obligatorios.")

        try:
            inicio = datetime.strptime(fecha_inicio, self.FORMATO)
        except (TypeError, ValueError) as error:
            raise FechaReservaInvalida(
                "Formato requerido: AAAA-MM-DD HH:MM."
            ) from error

        if not isinstance(horas, (int, float)) or isinstance(horas, bool) or horas <= 0:
            raise DuracionReservaInvalida("Las horas deben ser un número mayor que cero.")

        self.__codigo = codigo.strip()
        self.__recurso = recurso.strip()
        self.__inicio = inicio
        self.__fin = inicio + timedelta(hours=float(horas))
        self.__estado = "Activa"

    @property
    def codigo(self):
        return self.__codigo

    @property
    def recurso(self):
        return self.__recurso

    @property
    def inicio(self):
        return self.__inicio

    @property
    def fin(self):
        return self.__fin

    @property
    def estado(self):
        return self.__estado

    def cancelar(self):
        if self.__estado != "Activa":
            raise ErrorDisponibilidad("La reserva ya se encuentra cancelada.")
        self.__estado = "Cancelada"
        logger.info("Reserva %s cancelada.", self.__codigo)

    def se_superpone(self, otra):
        """Comprueba si dos reservas activas del mismo recurso se cruzan."""
        if not isinstance(otra, ReservaRecurso):
            raise ErrorDisponibilidad("Se esperaba un objeto ReservaRecurso.")
        if self.__estado == "Cancelada" or otra.estado == "Cancelada":
            return False
        if self.__recurso.casefold() != otra.recurso.casefold():
            return False
        return self.__inicio < otra.fin and otra.inicio < self.__fin

    def descripcion(self):
        return (
            f"{self.__codigo} | {self.__recurso} | "
            f"{self.__inicio:%Y-%m-%d %H:%M} - "
            f"{self.__fin:%Y-%m-%d %H:%M} | {self.__estado}"
        )


class GestorDisponibilidad:
    """Administra las reservas en una lista interna, sin base de datos."""

    def __init__(self):
        self.__reservas = []

    def registrar(self, reserva):
        if not isinstance(reserva, ReservaRecurso):
            raise ErrorDisponibilidad("Debe registrar un objeto ReservaRecurso.")

        if any(item.codigo == reserva.codigo for item in self.__reservas):
            raise ErrorDisponibilidad("El código de reserva ya existe.")

        for existente in self.__reservas:
            if reserva.se_superpone(existente):
                raise ConflictoHorario(
                    f"{reserva.recurso} ya está ocupado en ese horario."
                )

        self.__reservas.append(reserva)
        logger.info("Reserva %s registrada.", reserva.codigo)
        return reserva

    def listar(self):
        return [reserva.descripcion() for reserva in self.__reservas]


def demostracion():
    """Ejecuta diez pruebas sencillas, válidas e inválidas."""
    gestor = GestorDisponibilidad()
    pruebas = [
        ("Reserva inicial", lambda: gestor.registrar(
            ReservaRecurso("A01", "Sala 1", "2026-11-20 09:00", 2))),
        ("Cruce de horario", lambda: gestor.registrar(
            ReservaRecurso("A02", "Sala 1", "2026-11-20 10:00", 1))),
        ("Otro recurso a la misma hora", lambda: gestor.registrar(
            ReservaRecurso("A03", "Proyector", "2026-11-20 10:00", 1))),
        ("Duración cero", lambda: ReservaRecurso(
            "A04", "Sala 2", "2026-11-20 12:00", 0)),
        ("Duración negativa", lambda: ReservaRecurso(
            "A05", "Sala 2", "2026-11-20 12:00", -2)),
        ("Fecha con formato incorrecto", lambda: ReservaRecurso(
            "A06", "Sala 2", "20/11/2026 12:00", 1)),
        ("Código vacío", lambda: ReservaRecurso(
            " ", "Sala 2", "2026-11-20 12:00", 1)),
        ("Cancelar reserva A01", lambda: gestor.registrar(
            ReservaRecurso("A07", "Sala 3", "2026-11-20 14:00", 1))),
        ("Intentar registrar código repetido", lambda: gestor.registrar(
            ReservaRecurso("A01", "Sala 4", "2026-11-20 16:00", 1))),
        ("Registrar reserva en otro horario", lambda: gestor.registrar(
            ReservaRecurso("A08", "Sala 1", "2026-11-20 12:00", 1))),
    ]

    print("\n=== PRUEBAS: DISPONIBILIDAD DE RECURSOS ===")
    for numero, (nombre, accion) in enumerate(pruebas, start=1):
        try:
            resultado = accion()
        except ErrorDisponibilidad as error:
            print(f"[{numero}] Validación correcta: {nombre} -> {error}")
            logger.exception("Prueba %s: %s", numero, nombre)
        else:
            print(f"[{numero}] Operación correcta: {nombre}")
            if isinstance(resultado, ReservaRecurso):
                print("   ", resultado.descripcion())
        finally:
            print("    Fin de la prueba.")

    print("\nReservas registradas:")
    for linea in gestor.listar():
        print(" -", linea)
    print("\nRegistro guardado en logs/disponibilidad.log")


if __name__ == "__main__":
    demostracion()
