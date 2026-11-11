##### IMPORTS #####
import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod
import logging
import math
import re
##### FINAL IMPORTS #####


##### VARIABLES Y DICCIONARIOS #####
# Informacion general de la aplicacion #
APP_INFO = {
    "name": "CLIENT, SERVICE AND RESERVATION MANAGEMENT SYSTEM",
    "company_name": "SOFTWARE FJ",
    "version": "1.0"
}
# Final Informacion general de la aplicacion #

# Configuracion del archivo de eventos y errores #
logging.basicConfig(
    filename="system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
# Final Configuracion del archivo de eventos y errores #
##### FINAL VARIABLES Y DICCIONARIOS #####


##### EXCEPCIONES #####
# Errores personalizados del sistema #
class SystemErrorFJ(Exception):
    pass


class InvalidDataError(SystemErrorFJ):
    pass


class ServiceUnavailableError(SystemErrorFJ):
    pass


class ReservationError(SystemErrorFJ):
    pass
# Final Errores personalizados del sistema #
##### FINAL EXCEPCIONES #####


##### CLASES #####
# Clase abstracta para las entidades del sistema #
class Entity(ABC):
    @abstractmethod
    def describe(self):
        pass
# Final Clase abstracta para las entidades del sistema #


# Clase cliente con datos privados #
class Client(Entity):
    def __init__(self, name, identification, email):
        name = name.strip()
        identification = identification.strip()
        email = email.strip()
        if not name or not all(part.isalpha() for part in name.split()):
            raise InvalidDataError("Client name must contain letters only.")
        if not identification.isdigit():
            raise InvalidDataError("Identification must contain digits only.")
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            raise InvalidDataError("Enter a valid email address.")
        self.__name = name
        self.__identification = identification
        self.__email = email

    @property
    def name(self):
        return self.__name

    @property
    def identification(self):
        return self.__identification

    def describe(self):
        return f"{self.__name} | ID: {self.__identification} | {self.__email}"
# Final Clase cliente con datos privados #


# Clase abstracta para los servicios #
class Service(Entity, ABC):
    def __init__(self, name, hourly_rate):
        if not name.strip():
            raise InvalidDataError("Service name is required.")
        try:
            rate = float(hourly_rate)
        except (ValueError, TypeError) as error:
            raise InvalidDataError("Hourly rate must be numeric.") from error
        if not math.isfinite(rate) or rate <= 0:
            raise InvalidDataError("Hourly rate must be greater than zero.")
        self.name = name.strip()
        self.hourly_rate = rate
        self.available = True

    @abstractmethod
    def validate_parameters(self, duration):
        pass

    @abstractmethod
    def calculate_cost(self, duration, tax=0, discount=0):
        pass

    def _calculate_total(self, duration, tax=0, discount=0):
        try:
            hours = float(duration)
            tax = float(tax)
            discount = float(discount)
        except (ValueError, TypeError) as error:
            raise InvalidDataError("Duration, tax and discount must be numeric.") from error
        if not all(math.isfinite(value) for value in (hours, tax, discount)):
            raise InvalidDataError("Only finite numbers are allowed.")
        self.validate_parameters(hours)
        if not 0 <= tax <= 100 or not 0 <= discount <= 100:
            raise InvalidDataError("Tax and discount must be between 0 and 100.")
        subtotal = self.hourly_rate * hours
        total = subtotal * (1 - discount / 100) * (1 + tax / 100)
        if not math.isfinite(total) or total < 0:
            raise InvalidDataError("The calculated cost is invalid.")
        return total
# Final Clase abstracta para los servicios #


# Clases de los tres tipos de servicios #
class RoomRental(Service):
    def validate_parameters(self, duration):
        if not 0 < duration <= 8:
            raise InvalidDataError("Room rental duration must be between 0 and 8 hours.")

    def calculate_cost(self, duration, tax=0, discount=0):
        return self._calculate_total(duration, tax, discount)

    def describe(self):
        return f"Room | {self.name} | ${self.hourly_rate:,.2f}/hour"


class EquipmentRental(Service):
    def validate_parameters(self, duration):
        if not 0 < duration <= 24:
            raise InvalidDataError("Equipment rental duration must be between 0 and 24 hours.")

    def calculate_cost(self, duration, tax=0, discount=0):
        return self._calculate_total(duration, tax, discount)

    def describe(self):
        return f"Equipment | {self.name} | ${self.hourly_rate:,.2f}/hour"


class ConsultingService(Service):
    def validate_parameters(self, duration):
        if not 0 < duration <= 4:
            raise InvalidDataError("Consulting duration must be between 0 and 4 hours.")

    def calculate_cost(self, duration, tax=0, discount=0):
        return self._calculate_total(duration, tax, discount)

    def describe(self):
        return f"Consulting | {self.name} | ${self.hourly_rate:,.2f}/hour"
# Final Clases de los tres tipos de servicios #


# Clase para procesar confirmar y cancelar reservas #
class Reservation(Entity):
    def __init__(self, client, service, duration, tax=0, discount=0):
        if not isinstance(client, Client) or not isinstance(service, Service):
            raise ReservationError("A valid client and service are required.")
        self.client = client
        self.service = service
        self.duration = duration
        self.tax = tax
        self.discount = discount
        self.status = "Pending"
        self.total = 0

    def process(self):
        if self.status != "Pending":
            raise ReservationError("Only pending reservations can be processed.")
        if not self.service.available:
            raise ServiceUnavailableError("This service is not available.")
        self.total = self.service.calculate_cost(self.duration, self.tax, self.discount)
        return self.total

    def confirm(self):
        if self.status != "Pending":
            raise ReservationError("Only pending reservations can be confirmed.")
        self.process()
        self.service.available = False
        self.status = "Confirmed"
        logging.info("Reservation confirmed: %s / %s", self.client.name, self.service.name)

    def cancel(self):
        if self.status == "Cancelled":
            raise ReservationError("This reservation is already cancelled.")
        if self.status == "Confirmed":
            self.service.available = True
        self.status = "Cancelled"
        logging.info("Reservation cancelled: %s / %s", self.client.name, self.service.name)

    def describe(self):
        return (f"{self.client.name} | {self.service.name} | "
                f"{self.status} | ${self.total:,.2f}")
# Final Clase para procesar confirmar y cancelar reservas #


# Clase para administrar las listas sin base de datos #
class ManagementSystem:
    def __init__(self):
        self.clients = []
        self.services = []
        self.reservations = []

    def add_client(self, name, identification, email):
        if any(client.identification == identification.strip() for client in self.clients):
            raise InvalidDataError("A client with this ID already exists.")
        client = Client(name, identification, email)
        self.clients.append(client)
        logging.info("Client registered: %s", client.identification)
        return client

    def add_service(self, service_type, name, hourly_rate):
        types = {
            "Room": RoomRental,
            "Equipment": EquipmentRental,
            "Consulting": ConsultingService
        }
        if service_type not in types:
            raise InvalidDataError("Invalid service type.")
        if any(service.name.lower() == name.strip().lower() for service in self.services):
            raise InvalidDataError("A service with this name already exists.")
        service = types[service_type](name, hourly_rate)
        self.services.append(service)
        logging.info("Service created: %s", service.name)
        return service

    def add_reservation(self, client, service, duration, tax=0, discount=0):
        if client not in self.clients or service not in self.services:
            raise ReservationError("Select a registered client and service.")
        reservation = Reservation(client, service, duration, tax, discount)
        reservation.confirm()
        self.reservations.append(reservation)
        return reservation
# Final Clase para administrar las listas sin base de datos #
##### FINAL CLASES #####


##### FUNCIONES #####
# Funcion para mostrar y registrar errores sin cerrar la aplicacion #
def show_error(error):
    logging.error("%s: %s", type(error).__name__, error)
    messagebox.showerror("Error", str(error))
# Final Funcion para mostrar y registrar errores sin cerrar la aplicacion #


# Ventana de registro de clientes #
def open_client_window():
    window = tk.Toplevel(main_window)
    window.title("Software FJ - Clients")
    window.geometry("610x480")

    frame = tk.Frame(window)
    frame.pack(pady=15)
    entries = {}
    for row, field in enumerate(("Name", "Identification", "Email")):
        tk.Label(frame, text=field + ":").grid(row=row, column=0, padx=8, pady=7, sticky="e")
        entries[field] = tk.Entry(frame, width=34)
        entries[field].grid(row=row, column=1, padx=8, pady=7)

    client_list = tk.Listbox(window, width=75, height=10)
    client_list.pack(pady=10)

    def refresh():
        client_list.delete(0, tk.END)
        for client in system.clients:
            client_list.insert(tk.END, client.describe())

    def register():
        try:
            system.add_client(entries["Name"].get(), entries["Identification"].get(), entries["Email"].get())
        except (SystemErrorFJ, ValueError, TypeError) as error:
            show_error(error)
        else:
            refresh()
            for entry in entries.values():
                entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Client registered successfully.")
        finally:
            logging.info("Client registration attempt finished.")

    tk.Button(window, text="Register Client", width=24, command=register).pack(pady=7)
    tk.Label(window, text="Registered Clients", font=("Arial", 11, "bold")).pack(pady=5)
    refresh()
# Final Ventana de registro de clientes #


# Ventana de registro de servicios #
def open_service_window():
    window = tk.Toplevel(main_window)
    window.title("Software FJ - Services")
    window.geometry("630x490")
    frame = tk.Frame(window)
    frame.pack(pady=15)

    tk.Label(frame, text="Service Type:").grid(row=0, column=0, padx=8, pady=7)
    service_type = tk.StringVar(value="Room")
    ttk.Combobox(frame, textvariable=service_type, values=("Room", "Equipment", "Consulting"),
                 state="readonly", width=31).grid(row=0, column=1, padx=8, pady=7)

    tk.Label(frame, text="Service Name:").grid(row=1, column=0, padx=8, pady=7)
    name_entry = tk.Entry(frame, width=34)
    name_entry.grid(row=1, column=1, padx=8, pady=7)
    tk.Label(frame, text="Hourly Rate:").grid(row=2, column=0, padx=8, pady=7)
    rate_entry = tk.Entry(frame, width=34)
    rate_entry.grid(row=2, column=1, padx=8, pady=7)

    service_list = tk.Listbox(window, width=76, height=10)
    service_list.pack(pady=10)

    def refresh():
        service_list.delete(0, tk.END)
        for service in system.services:
            status = "Available" if service.available else "Unavailable"
            service_list.insert(tk.END, f"{service.describe()} | {status}")

    def register():
        try:
            system.add_service(service_type.get(), name_entry.get(), rate_entry.get())
        except (SystemErrorFJ, ValueError, TypeError) as error:
            show_error(error)
        else:
            refresh()
            name_entry.delete(0, tk.END)
            rate_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Service created successfully.")
        finally:
            logging.info("Service creation attempt finished.")

    tk.Button(window, text="Create Service", width=24, command=register).pack(pady=7)
    tk.Label(window, text="Registered Services", font=("Arial", 11, "bold")).pack(pady=5)
    refresh()
# Final Ventana de registro de servicios #


# Ventana de reservas y calculo de costos #
def open_reservation_window():
    window = tk.Toplevel(main_window)
    window.title("Software FJ - Reservations")
    window.geometry("770x650")
    frame = tk.Frame(window)
    frame.pack(pady=12)

    tk.Label(frame, text="Client:").grid(row=0, column=0, padx=8, pady=6, sticky="e")
    client_box = ttk.Combobox(frame, width=43, state="readonly")
    client_box.grid(row=0, column=1, padx=8, pady=6)
    tk.Label(frame, text="Service:").grid(row=1, column=0, padx=8, pady=6, sticky="e")
    service_box = ttk.Combobox(frame, width=43, state="readonly")
    service_box.grid(row=1, column=1, padx=8, pady=6)

    entries = {}
    for row, field in enumerate(("Duration (hours)", "Tax (%)", "Discount (%)"), start=2):
        tk.Label(frame, text=field + ":").grid(row=row, column=0, padx=8, pady=6, sticky="e")
        entries[field] = tk.Entry(frame, width=46)
        entries[field].grid(row=row, column=1, padx=8, pady=6)
    entries["Tax (%)"].insert(0, "0")
    entries["Discount (%)"].insert(0, "0")

    reservation_list = tk.Listbox(window, width=93, height=10)
    reservation_list.pack(pady=10)

    def refresh():
        client_box["values"] = [client.describe() for client in system.clients]
        service_box["values"] = [service.describe() for service in system.services]
        reservation_list.delete(0, tk.END)
        for reservation in system.reservations:
            reservation_list.insert(tk.END, reservation.describe())

    def selected_objects():
        client_index = client_box.current()
        service_index = service_box.current()
        if client_index < 0 or service_index < 0:
            raise ReservationError("Please select a client and a service.")
        return system.clients[client_index], system.services[service_index]

    def calculate():
        try:
            client, service = selected_objects()
            total = service.calculate_cost(entries["Duration (hours)"].get(),
                                           entries["Tax (%)"].get(), entries["Discount (%)"].get())
        except (SystemErrorFJ, ValueError, TypeError, IndexError) as error:
            show_error(error)
        else:
            messagebox.showinfo("Cost", f"Client: {client.name}\nTotal cost: ${total:,.2f}")

    def book():
        try:
            client, service = selected_objects()
            reservation = system.add_reservation(client, service, entries["Duration (hours)"].get(),
                                                 entries["Tax (%)"].get(), entries["Discount (%)"].get())
        except (SystemErrorFJ, ValueError, TypeError, IndexError) as error:
            show_error(error)
        else:
            refresh()
            messagebox.showinfo("Success", f"Reservation confirmed.\nTotal: ${reservation.total:,.2f}")
        finally:
            logging.info("Reservation creation attempt finished.")

    def cancel():
        try:
            selection = reservation_list.curselection()
            if not selection:
                raise ReservationError("Please select a reservation.")
            system.reservations[selection[0]].cancel()
        except (SystemErrorFJ, IndexError) as error:
            show_error(error)
        else:
            refresh()
            messagebox.showinfo("Success", "Reservation cancelled successfully.")

    buttons = tk.Frame(window)
    buttons.pack(pady=7)
    tk.Button(buttons, text="Calculate Cost", width=17, command=calculate).grid(row=0, column=0, padx=6)
    tk.Button(buttons, text="Confirm Reservation", width=19, command=book).grid(row=0, column=1, padx=6)
    tk.Button(buttons, text="Cancel Selected", width=17, command=cancel).grid(row=0, column=2, padx=6)
    tk.Label(window, text="Reservations", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Button(window, text="Refresh Lists", width=20, command=refresh).pack(pady=9)
    tk.Label(window, text="One confirmed reservation per service at a time.", fg="gray").pack()
    refresh()
# Final Ventana de reservas y calculo de costos #


# Pruebas de operaciones correctas e incorrectas #
def run_tests():
    test_system = ManagementSystem()
    results = []

    def check(label, action, should_fail=False):
        try:
            action()
        except Exception as error:
            logging.error("Test %s - %s: %s", label, type(error).__name__, error)
            if should_fail and isinstance(error, SystemErrorFJ):
                results.append(f"PASS - {label} (error handled)")
            else:
                results.append(f"FAIL - {label} ({error})")
        else:
            if should_fail:
                results.append(f"FAIL - {label} (error was expected)")
            else:
                results.append(f"PASS - {label}")
        finally:
            logging.info("Test finished: %s", label)

    check("1. Valid client", lambda: test_system.add_client("Edisson Alejandro Castañeda Bermúdez", "1111111111", "eacb@eacb.com"))
    check("2. Invalid email", lambda: test_system.add_client("Mathias Castañeda Martínez", "1111111112", "eacb.com"), True)
    check("3. Duplicate client", lambda: test_system.add_client("Edisson Castañeda", "1111111111", "edissoncastaneda@dominio.com"), True)
    check("4. Valid room", lambda: test_system.add_service("Room", "Espacio 1", 50000))
    check("5. Invalid rate", lambda: test_system.add_service("Equipment", "Camera", -50), True)
    check("6. Valid equipment", lambda: test_system.add_service("Equipment", "Projector", 20000))
    check("7. Valid consulting", lambda: test_system.add_service("Consulting", "Python Help", 70000))
    client = test_system.clients[0]
    room = test_system.services[0]
    equipment = test_system.services[1]
    consulting = test_system.services[2]
    check("8. Valid room reservation", lambda: test_system.add_reservation(client, room, 2))
    check("9. Unavailable room", lambda: test_system.add_reservation(client, room, 1), True)
    check("10. Invalid duration", lambda: test_system.add_reservation(client, equipment, -1), True)
    check("11. Invalid tax", lambda: test_system.add_reservation(client, equipment, 1, 150), True)
    check("12. Valid equipment reservation", lambda: test_system.add_reservation(client, equipment, 3, 10, 5))
    check("13. Cancel reservation", lambda: test_system.reservations[0].cancel())
    check("14. Book available room again", lambda: test_system.add_reservation(client, room, 1))
    check("15. Valid consulting reservation", lambda: test_system.add_reservation(client, consulting, 2))
    check("16. Double cancellation", lambda: test_system.reservations[0].cancel(), True)

    window = tk.Toplevel(main_window)
    window.title("Software FJ - Test Results")
    window.geometry("650x560")
    tk.Label(window, text="SYSTEM TEST RESULTS", font=("Arial", 15, "bold")).pack(pady=12)
    output = tk.Text(window, width=75, height=23)
    output.pack(padx=10, pady=5)
    output.insert(tk.END, "\n".join(results))
    output.insert(tk.END, f"\n\nPassed: {sum(line.startswith('PASS') for line in results)}/{len(results)}")
    output.insert(tk.END, "\nTests use temporary lists and do not change your data.")
    output.config(state="disabled")
    logging.info("Test run completed: %s", results[-1])
# Final Pruebas de operaciones correctas e incorrectas #


# Ventana principal de la aplicacion #
def open_main_menu():
    global main_window
    main_window = tk.Tk()
    main_window.title("Software FJ - Main Menu")
    main_window.geometry("540x510")
    main_window.resizable(False, False)

    tk.Label(main_window, text=APP_INFO["company_name"], font=("Arial", 19, "bold")).pack(pady=(28, 10))
    tk.Label(main_window, text=APP_INFO["name"], font=("Arial", 10), wraplength=460).pack(pady=6)
    tk.Button(main_window, text="Client Management", width=30, command=open_client_window).pack(pady=12)
    tk.Button(main_window, text="Service Management", width=30, command=open_service_window).pack(pady=12)
    tk.Button(main_window, text="Reservation Management", width=30, command=open_reservation_window).pack(pady=12)
    tk.Button(main_window, text="Run Tests", width=30, command=run_tests).pack(pady=12)
    tk.Button(main_window, text="Exit", width=30, command=main_window.destroy).pack(pady=12)
    main_window.mainloop()
# Final Ventana principal de la aplicacion #
##### FINAL FUNCIONES #####


##### CODIGO PRINCIPAL #####
# Creacion del sistema e inicio de la interfaz #
if __name__ == "__main__":
    system = ManagementSystem()
    logging.info("Software FJ application started.")
    open_main_menu()
# Final Creacion del sistema e inicio de la interfaz #
##### FINAL CODIGO PRINCIPAL #####
