"""
Sistema de Reservas - Proyecto Mejorado
"""

from abc import ABC, abstractmethod
from datetime import datetime


# =========================================================
# EXCEPCIONES PERSONALIZADAS
# =========================================================

class ErrorCliente(Exception):
    pass


class ErrorServicio(Exception):
    pass


class ErrorReserva(Exception):
    pass


# =========================================================
# CLASE ABSTRACTA BASE
# =========================================================

class EntidadGeneral(ABC):

    @abstractmethod
    def obtener_informacion(self):
        pass


# =========================================================
# CLASE CLIENTE
# =========================================================

class Cliente(EntidadGeneral):

    def __init__(self, identificacion, nombre, correo):

        self.__identificacion = identificacion
        self.__nombre = nombre
        self.__correo = correo

        self.__validar_datos()

    def __validar_datos(self):

        if not self.__nombre.strip():

            raise ErrorCliente(
                "El nombre no puede estar vacío."
            )

        if not self.__identificacion.isdigit():

            raise ErrorCliente(
                "La identificación debe ser numérica."
            )

        if len(self.__identificacion) < 5:

            raise ErrorCliente(
                "La identificación debe tener mínimo 5 dígitos."
            )

        if "@" not in self.__correo or "." not in self.__correo:

            raise ErrorCliente(
                "Correo inválido."
            )

    def obtener_informacion(self):

        return (
            f"Cliente: {self.__nombre} | "
            f"ID: {self.__identificacion}"
        )


# =========================================================
# CLASE ABSTRACTA SERVICIO
# =========================================================

class Servicio(EntidadGeneral):

    def __init__(
        self,
        id_servicio,
        nombre,
        precio_base
    ):

        if precio_base <= 0:

            raise ErrorServicio(
                "El precio debe ser mayor a cero."
            )

        self.id_servicio = id_servicio
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, tiempo):
        pass

    def obtener_informacion(self):

        return (
            f"Servicio: {self.nombre} | "
            f"Precio Base: ${self.precio_base}"
        )


# =========================================================
# RESERVA SALA
# =========================================================

class ReservaSala(Servicio):

    def __init__(
        self,
        id_servicio,
        nombre,
        precio_base,
        capacidad
    ):

        super().__init__(
            id_servicio,
            nombre,
            precio_base
        )

        self.capacidad = capacidad

    def calcular_costo(self, horas):

        if horas <= 0:

            raise ErrorServicio(
                "Las horas deben ser mayores a cero."
            )

        return self.precio_base * horas


# =========================================================
# ALQUILER EQUIPO
# =========================================================

class AlquilerEquipo(Servicio):

    def __init__(
        self,
        id_servicio,
        nombre,
        precio_base,
        requiere_seguro=True
    ):

        super().__init__(
            id_servicio,
            nombre,
            precio_base
        )

        self.requiere_seguro = requiere_seguro

    def calcular_costo(self, dias):

        if dias <= 0:

            raise ErrorServicio(
                "Los días deben ser mayores a cero."
            )

        costo = self.precio_base * dias

        if self.requiere_seguro:

            costo += 50000

        return costo


# =========================================================
# ASESORÍA
# =========================================================

class Asesoria(Servicio):

    def __init__(
        self,
        id_servicio,
        nombre,
        precio_base,
        nivel="Senior"
    ):

        super().__init__(
            id_servicio,
            nombre,
            precio_base
        )

        self.nivel = nivel

    def calcular_costo(self, sesiones):

        if sesiones <= 0:

            raise ErrorServicio(
                "Las sesiones deben ser mayores a cero."
            )

        recargo = 1.5 if self.nivel == "Senior" else 1.0

        return (
            self.precio_base *
            sesiones *
            recargo
        )


# =========================================================
# CLASE RESERVA
# =========================================================

class Reserva(EntidadGeneral):

    def __init__(
        self,
        id_reserva,
        cliente,
        servicio,
        cantidad_tiempo,
        fecha_reserva,
        hora_reserva
    ):

        if not isinstance(cliente, Cliente):

            raise ErrorReserva(
                "Cliente inválido."
            )

        if not isinstance(servicio, Servicio):

            raise ErrorReserva(
                "Servicio inválido."
            )

        if cantidad_tiempo <= 0:

            raise ErrorReserva(
                "El tiempo debe ser mayor a cero."
            )

        try:

            self.fecha_reserva = datetime.strptime(
                fecha_reserva,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            raise ErrorReserva(
                "Fecha inválida. Use YYYY-MM-DD."
            )

        try:

            self.hora_reserva = datetime.strptime(
                hora_reserva,
                "%H:%M"
            ).time()

        except ValueError:

            raise ErrorReserva(
                "Hora inválida. Use HH:MM."
            )

        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad_tiempo = cantidad_tiempo
        self.estado = "Pendiente"

    def confirmar(self):

        if self.estado == "Cancelada":

            raise ErrorReserva(
                "La reserva ya fue cancelada."
            )

        self.estado = "Confirmada"

    def cancelar(self):

        self.estado = "Cancelada"

    def obtener_informacion(self):

        total = self.servicio.calcular_costo(
            self.cantidad_tiempo
        )

        return (
            f"\nReserva #{self.id_reserva}\n"
            f"Cliente: {self.cliente.obtener_informacion()}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Fecha: {self.fecha_reserva}\n"
            f"Hora: {self.hora_reserva}\n"
            f"Estado: {self.estado}\n"
            f"Total: ${total}\n"
        )


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def solicitar_entero(mensaje):

    while True:

        try:

            valor = int(input(mensaje))

            if valor <= 0:

                print(
                    "Debe ingresar un número mayor a cero."
                )

                continue

            return valor

        except ValueError:

            print(
                "Debe ingresar un número válido."
            )


def pausar():

    input(
        "\nPresione ENTER para continuar..."
    )


# =========================================================
# MENÚ PRINCIPAL
# =========================================================

def menu_principal():

    reservas = []
    contador = 1

    while True:

        print("\n================================")
        print(" SISTEMA DE RESERVAS SOFTWARE FJ")
        print("================================")
        print("1. Crear reserva")
        print("2. Ver reservas")
        print("3. Confirmar reserva")
        print("4. Cancelar reserva")
        print("5. Salir")

        opcion = input(
            "\nSeleccione una opción: "
        )

        try:

            # =============================================
            # CREAR RESERVA
            # =============================================

            if opcion == "1":

                print("\n--- DATOS CLIENTE ---")

                identificacion = input(
                    "Identificación: "
                )

                nombre = input(
                    "Nombre: "
                )

                correo = input(
                    "Correo: "
                )

                cliente = Cliente(
                    identificacion,
                    nombre,
                    correo
                )

                print("\n--- SERVICIOS ---")
                print("1. Reserva Sala")
                print("2. Alquiler Equipo")
                print("3. Asesoría")

                tipo = input(
                    "Seleccione servicio: "
                )

                if tipo == "1":

                    servicio = ReservaSala(
                        "S1",
                        "Sala Empresarial",
                        100000,
                        30
                    )

                    cantidad = solicitar_entero(
                        "Cantidad de horas: "
                    )

                elif tipo == "2":

                    servicio = AlquilerEquipo(
                        "S2",
                        "Video Beam",
                        80000,
                        True
                    )

                    cantidad = solicitar_entero(
                        "Cantidad de días: "
                    )

                elif tipo == "3":

                    servicio = Asesoria(
                        "S3",
                        "Asesoría Profesional",
                        120000,
                        "Senior"
                    )

                    cantidad = solicitar_entero(
                        "Cantidad de sesiones: "
                    )

                else:

                    raise ErrorServicio(
                        "Servicio inválido."
                    )

                fecha = input(
                    "Fecha (YYYY-MM-DD): "
                )

                hora = input(
                    "Hora (HH:MM): "
                )

                reserva = Reserva(
                    contador,
                    cliente,
                    servicio,
                    cantidad,
                    fecha,
                    hora
                )

                reservas.append(reserva)

                contador += 1

                print(
                    "\nReserva creada correctamente."
                )

                print(
                    reserva.obtener_informacion()
                )

                pausar()

            # =============================================
            # VER RESERVAS
            # =============================================

            elif opcion == "2":

                if not reservas:

                    print(
                        "\nNo existen reservas."
                    )

                else:

                    for reserva in reservas:

                        print(
                            reserva.obtener_informacion()
                        )

                pausar()

            # =============================================
            # CONFIRMAR RESERVA
            # =============================================

            elif opcion == "3":

                codigo = solicitar_entero(
                    "ID reserva: "
                )

                encontrada = False

                for reserva in reservas:

                    if reserva.id_reserva == codigo:

                        reserva.confirmar()

                        encontrada = True

                        print(
                            "\nReserva confirmada."
                        )

                        break

                if not encontrada:

                    print(
                        "\nReserva no encontrada."
                    )

                pausar()

            # =============================================
            # CANCELAR RESERVA
            # =============================================

            elif opcion == "4":

                codigo = solicitar_entero(
                    "ID reserva: "
                )

                encontrada = False

                for reserva in reservas:

                    if reserva.id_reserva == codigo:

                        reserva.cancelar()

                        encontrada = True

                        print(
                            "\nReserva cancelada."
                        )

                        break

                if not encontrada:

                    print(
                        "\nReserva no encontrada."
                    )

                pausar()

            # =============================================
            # SALIR
            # =============================================

            elif opcion == "5":

                print(
                    "\nGracias por usar el sistema."
                )

                break

            else:

                print(
                    "\nOpción inválida."
                )

        # =============================================
        # MANEJO DE EXCEPCIONES
        # =============================================

        except ErrorCliente as error:

            print(
                f"\nError cliente: {error}"
            )

        except ErrorServicio as error:

            print(
                f"\nError servicio: {error}"
            )

        except ErrorReserva as error:

            print(
                f"\nError reserva: {error}"
            )

        except Exception as error:

            print(
                f"\nError inesperado: {error}"
            )


# =========================================================
# EJECUCIÓN PRINCIPAL
# =========================================================

if __name__ == "__main__":

    menu_principal()