import sys
import os
import logging

# =========================================================
# CONFIGURACIÓN DE RUTAS
# =========================================================

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# =========================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# =========================================================

logging.basicConfig(
    filename='registro_errores.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# =========================================================
# LISTAS EN MEMORIA
# =========================================================

clientes = []
servicios = []
reservas = []

# =========================================================
# CLASE CLIENTE
# =========================================================

class Cliente:

    def __init__(self, identificacion, nombre, correo):

        if not identificacion.isdigit():
            raise ValueError(
                "La identificación debe ser numérica."
            )

        if "@" not in correo:
            raise ValueError(
                "Correo inválido."
            )

        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    def obtener_informacion(self):

        return (
            f"Cliente: {self.nombre} "
            f"| ID: {self.identificacion}"
        )

# =========================================================
# CLASE SERVICIO BASE
# =========================================================

class Servicio:

    def __init__(self, codigo, nombre, precio):

        if precio <= 0:
            raise ValueError(
                "El precio debe ser mayor a cero."
            )

        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

    def obtener_informacion(self):

        return (
            f"{self.nombre} "
            f"| Precio: ${self.precio}"
        )

# =========================================================
# CLASE RESERVA SALA
# =========================================================

class ReservaSala(Servicio):

    def __init__(
        self,
        codigo,
        nombre,
        precio,
        capacidad
    ):

        super().__init__(
            codigo,
            nombre,
            precio
        )

        self.capacidad = capacidad

# =========================================================
# CLASE ALQUILER EQUIPO
# =========================================================

class AlquilerEquipo(Servicio):

    def __init__(
        self,
        codigo,
        nombre,
        precio,
        seguro
    ):

        super().__init__(
            codigo,
            nombre,
            precio
        )

        self.seguro = seguro

# =========================================================
# CLASE ASESORIA
# =========================================================

class Asesoria(Servicio):

    def __init__(
        self,
        codigo,
        nombre,
        precio,
        nivel
    ):

        super().__init__(
            codigo,
            nombre,
            precio
        )

        self.nivel = nivel

# =========================================================
# CLASE RESERVA
# =========================================================

class Reserva:

    def __init__(
        self,
        id_reserva,
        cliente,
        servicio,
        tiempo
    ):

        if tiempo <= 0:
            raise ValueError(
                "El tiempo debe ser mayor a cero."
            )

        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.tiempo = tiempo
        self.estado = "Pendiente"

    def confirmar(self):

        self.estado = "Confirmada"

    def cancelar(self):

        self.estado = "Cancelada"

    def obtener_informacion(self):

        return (
            f"Reserva {self.id_reserva} "
            f"| Cliente: {self.cliente.nombre} "
            f"| Servicio: {self.servicio.nombre} "
            f"| Estado: {self.estado}"
        )

# =========================================================
# MENÚ PRINCIPAL
# =========================================================

def mostrar_menu():

    print("\n")
    print("===================================")
    print("         SOFTWARE FJ")
    print("===================================")
    print("1. Registrar cliente")
    print("2. Crear servicio")
    print("3. Crear reserva")
    print("4. Confirmar reserva")
    print("5. Cancelar reserva")
    print("6. Ver registros")
    print("7. Salir")
    print("===================================")

# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================

if __name__ == "__main__":

    while True:

        mostrar_menu()

        opcion = input(
            "\nSeleccione una opción: "
        )

        try:

            # =================================================
            # OPCIÓN 1
            # =================================================

            if opcion == "1":

                print("\n--- REGISTRO CLIENTE ---")

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

                clientes.append(cliente)

                print(
                    "\nCliente registrado correctamente."
                )

            # =================================================
            # OPCIÓN 2
            # =================================================

            elif opcion == "2":

                print("\n--- CREAR SERVICIO ---")

                print("1. Reserva Sala")
                print("2. Alquiler Equipo")
                print("3. Asesoría")

                tipo = input(
                    "Seleccione tipo: "
                )

                codigo = input(
                    "Código: "
                )

                nombre = input(
                    "Nombre: "
                )

                precio = float(
                    input("Precio: ")
                )

                if tipo == "1":

                    capacidad = int(
                        input("Capacidad: ")
                    )

                    servicio = ReservaSala(
                        codigo,
                        nombre,
                        precio,
                        capacidad
                    )

                elif tipo == "2":

                    seguro = input(
                        "¿Seguro? (s/n): "
                    )

                    servicio = AlquilerEquipo(
                        codigo,
                        nombre,
                        precio,
                        seguro.lower() == "s"
                    )

                elif tipo == "3":

                    nivel = input(
                        "Nivel: "
                    )

                    servicio = Asesoria(
                        codigo,
                        nombre,
                        precio,
                        nivel
                    )

                else:

                    raise ValueError(
                        "Tipo inválido."
                    )

                servicios.append(servicio)

                print(
                    "\nServicio creado correctamente."
                )

            # =================================================
            # OPCIÓN 3
            # =================================================

            elif opcion == "3":

                print("\n--- CREAR RESERVA ---")

                if len(clientes) == 0:

                    raise ValueError(
                        "No hay clientes."
                    )

                if len(servicios) == 0:

                    raise ValueError(
                        "No hay servicios."
                    )

                id_reserva = input(
                    "ID reserva: "
                )

                print("\nCLIENTES:")

                for i, cliente in enumerate(clientes):

                    print(
                        f"{i + 1}. "
                        f"{cliente.obtener_informacion()}"
                    )

                cliente_index = int(
                    input(
                        "Seleccione cliente: "
                    )
                ) - 1

                print("\nSERVICIOS:")

                for i, servicio in enumerate(servicios):

                    print(
                        f"{i + 1}. "
                        f"{servicio.obtener_informacion()}"
                    )

                servicio_index = int(
                    input(
                        "Seleccione servicio: "
                    )
                ) - 1

                tiempo = int(
                    input(
                        "Tiempo: "
                    )
                )

                reserva = Reserva(
                    id_reserva,
                    clientes[cliente_index],
                    servicios[servicio_index],
                    tiempo
                )

                reservas.append(reserva)

                print(
                    "\nReserva creada correctamente."
                )

            # =================================================
            # OPCIÓN 4
            # =================================================

            elif opcion == "4":

                for i, reserva in enumerate(reservas):

                    print(
                        f"{i + 1}. "
                        f"{reserva.obtener_informacion()}"
                    )

                indice = int(
                    input(
                        "Seleccione reserva: "
                    )
                ) - 1

                reservas[indice].confirmar()

                print(
                    "\nReserva confirmada."
                )

            # =================================================
            # OPCIÓN 5
            # =================================================

            elif opcion == "5":

                for i, reserva in enumerate(reservas):

                    print(
                        f"{i + 1}. "
                        f"{reserva.obtener_informacion()}"
                    )

                indice = int(
                    input(
                        "Seleccione reserva: "
                    )
                ) - 1

                reservas[indice].cancelar()

                print(
                    "\nReserva cancelada."
                )

            # =================================================
            # OPCIÓN 6
            # =================================================

            elif opcion == "6":

                print("\n===== CLIENTES =====")

                for cliente in clientes:

                    print(
                        cliente.obtener_informacion()
                    )

                print("\n===== SERVICIOS =====")

                for servicio in servicios:

                    print(
                        servicio.obtener_informacion()
                    )

                print("\n===== RESERVAS =====")

                for reserva in reservas:

                    print(
                        reserva.obtener_informacion()
                    )

            # =================================================
            # OPCIÓN 7
            # =================================================

            elif opcion == "7":

                print(
                    "\nPrograma finalizado."
                )

                break

            else:

                print(
                    "\nOpción inválida."
                )

        # =====================================================
        # MANEJO DE ERRORES
        # =====================================================

        except (
            ValueError,
            IndexError
        ) as e:

            print(f"\nERROR: {e}")

            logging.error(e)

        finally:

            print(
                "\nEl sistema continúa funcionando."
            )