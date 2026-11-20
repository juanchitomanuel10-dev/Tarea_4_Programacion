
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reservas import Reserva
from excepciones import SoftwareFJError, DatosInvalidosError
from logging_config import registrar_evento, registrar_error
  
class SistemaSoftwareFJ:
    """Clase principal que administra el sistema."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, identificacion, nombre, correo, telefono):
        cliente = Cliente(identificacion, nombre, correo, telefono)

        if any(c.identificacion == cliente.identificacion for c in self.clientes):
            raise DatosInvalidosError("La identificacion ya existe.")

        self.clientes.append(cliente)
        registrar_evento(f"Cliente registrado: {nombre}")
        print("Cliente registrado correctamente.")
        return cliente

    def registrar_servicio(self, servicio):
        if any(s.codigo == servicio.codigo for s in self.servicios):
            raise DatosInvalidosError("El codigo del servicio ya existe.")

        self.servicios.append(servicio)
        registrar_evento(f"Servicio registrado: {servicio.nombre}")
        print("Servicio registrado correctamente.")

    def buscar_cliente(self, identificacion):
        for cliente in self.clientes:
            if cliente.identificacion == identificacion:
                return cliente

        raise DatosInvalidosError("Cliente no encontrado.")

    def buscar_servicio(self, codigo):
        for servicio in self.servicios:
            if servicio.codigo == codigo:
                return servicio

        raise DatosInvalidosError("Servicio no encontrado.")

    def buscar_reserva(self, codigo):
        for reserva in self.reservas:
            if reserva.codigo == codigo:
                return reserva

        raise DatosInvalidosError("Reserva no encontrada.")

    def crear_reserva(self, identificacion, codigo_servicio, duracion):
        cliente = self.buscar_cliente(identificacion)
        servicio = self.buscar_servicio(codigo_servicio)

        reserva = Reserva(cliente, servicio, duracion)
        reserva.procesar(impuesto=19)

        self.reservas.append(reserva)
        print(reserva.mostrar_info())
        return reserva

    def confirmar_reserva(self, codigo):
        reserva = self.buscar_reserva(codigo)
        reserva.confirmar()
        print("Reserva confirmada.")

    def cancelar_reserva(self, codigo):
        reserva = self.buscar_reserva(codigo)
        reserva.cancelar()
        print("Reserva cancelada.")

    def mostrar_clientes(self):
        print("\n--- CLIENTES ---")
        for cliente in self.clientes:
            print(cliente.mostrar_info())
            print("----------------")

    def mostrar_servicios(self):
        print("\n--- SERVICIOS ---")
        for servicio in self.servicios:
            print(servicio.describir_servicio())
            print(f"Precio: ${servicio.precio_base:,.2f}")
            print(f"Disponible: {servicio.disponible}")
            print("----------------")

    def mostrar_reservas(self):
        print("\n--- RESERVAS ---")
        for reserva in self.reservas:
            print(reserva.mostrar_info())
            print("----------------")

    def ejecutar_pruebas(self):
        """Ejecuta doce escenarios de prueba."""

        print("\n========== PRUEBAS SOFTWARE FJ ==========")

        # Prueba 1: registro correcto de cliente.
        try:
            self.registrar_cliente(
                "1001", "Carlos Perez", "carlos@gmail.com", "3001234567"
            )
        except Exception as error:
            registrar_error(f"Prueba 1: {error}")
            print(error)

        # Prueba 2: registro de otro cliente.
        try:
            self.registrar_cliente(
                "1002", "Laura Gomez", "laura@gmail.com", "3101234567"
            )
        except Exception as error:
            registrar_error(f"Prueba 2: {error}")
            print(error)

        # Prueba 3: cliente con nombre vacio.
        try:
            self.registrar_cliente(
                "1003", "", "error@gmail.com", "3001234567"
            )
        except Exception as error:
            registrar_error(f"Prueba 3: {error}")
            print("Error controlado:", error)

        # Prueba 4: registro de sala.
        try:
            sala = ReservaSala(
                "S01", "Sala de reuniones", 50000, 10
            )
            self.registrar_servicio(sala)
        except Exception as error:
            registrar_error(f"Prueba 4: {error}")
            print(error)

        # Prueba 5: registro de equipo.
        try:
            equipo = AlquilerEquipo(
                "E01", "Computador portatil", 30000, "Portatil"
            )
            self.registrar_servicio(equipo)
        except Exception as error:
            registrar_error(f"Prueba 5: {error}")
            print(error)

        # Prueba 6: registro de asesoria.
        try:
            asesoria = Asesoria(
                "A01", "Asesoria de software", 80000, "Programacion"
            )
            self.registrar_servicio(asesoria)
        except Exception as error:
            registrar_error(f"Prueba 6: {error}")
            print(error)

        # Prueba 7: precio incorrecto.
        try:
            sala_invalida = ReservaSala(
                "S02", "Sala invalida", -1000, 10
            )
            self.registrar_servicio(sala_invalida)
        except Exception as error:
            registrar_error(f"Prueba 7: {error}")
            print("Error controlado:", error)

        # Prueba 8: reserva correcta.
        reserva1 = None
        try:
            reserva1 = self.crear_reserva("1001", "S01", 2)
        except Exception as error:
            registrar_error(f"Prueba 8: {error}")
            print(error)

        # Prueba 9: confirmacion.
        try:
            if reserva1 is not None:
                self.confirmar_reserva(reserva1.codigo)
        except Exception as error:
            registrar_error(f"Prueba 9: {error}")
            print(error)

        # Prueba 10: reserva y cancelacion.
        try:
            reserva2 = self.crear_reserva("1002", "E01", 3)
            self.cancelar_reserva(reserva2.codigo)
        except Exception as error:
            registrar_error(f"Prueba 10: {error}")
            print(error)

        # Prueba 11: servicio no disponible.
        try:
            asesoria.cambiar_disponibilidad(False)
            self.crear_reserva("1001", "A01", 1)
        except Exception as error:
            registrar_error(f"Prueba 11: {error}")
            print("Error controlado:", error)

        # Prueba 12: reserva inexistente.
        try:
            self.buscar_reserva("R-999")
        except Exception as error:
            registrar_error(f"Prueba 12: {error}")
            print("Error controlado:", error)

        print("\nSe ejecutaron 12 escenarios de prueba.")
        print("Consulte logs.txt para revisar los registros.")

    def menu(self):
        """Muestra las opciones disponibles al usuario."""

        while True:
            print("\n========== SOFTWARE FJ ==========")
            print("1. Registrar cliente")
            print("2. Mostrar clientes")
            print("3. Mostrar servicios")
            print("4. Crear reserva")
            print("5. Confirmar reserva")
            print("6. Cancelar reserva")
            print("7. Mostrar reservas")
            print("8. Salir")

            opcion = input("Seleccione una opcion: ").strip()

            try:
                if opcion == "1":
                    identificacion = input("Identificacion: ")
                    nombre = input("Nombre: ")
                    correo = input("Correo: ")
                    telefono = input("Telefono: ")
                    self.registrar_cliente(
                        identificacion, nombre, correo, telefono
                    )

                elif opcion == "2":
                    self.mostrar_clientes()

                elif opcion == "3":
                    self.mostrar_servicios()

                elif opcion == "4":
                    identificacion = input("Identificacion del cliente: ")
                    codigo = input("Codigo del servicio: ")
                    duracion = float(input("Duracion: "))
                    self.crear_reserva(identificacion, codigo, duracion)

                elif opcion == "5":
                    codigo = input("Codigo de reserva: ")
                    self.confirmar_reserva(codigo)

                elif opcion == "6":
                    codigo = input("Codigo de reserva: ")
                    self.cancelar_reserva(codigo)

                elif opcion == "7":
                    self.mostrar_reservas()

                elif opcion == "8":
                    print("Gracias por utilizar Software FJ.")
                    registrar_evento("Cierre del sistema.")
                    break

                else:
                    print("Opcion no valida.")

            except (SoftwareFJError, ValueError) as error:
                registrar_error(f"Error en el menu: {error}")
                print("No se pudo completar:", error)

            except Exception as error:
                registrar_error(f"Error inesperado: {error}")
                print("Error inesperado:", error)


if __name__ == "__main__":
    sistema = SistemaSoftwareFJ()
    sistema.ejecutar_pruebas()
    sistema.menu()
