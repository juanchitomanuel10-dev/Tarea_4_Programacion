# Se importan las entidades y servicios del sistema
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
# Se importa la clase Reserva para gestionar el ciclo de reservas
from reservas import Reserva
# Se importan las excepciones propias del sistema para capturar y controlar errores
from excepciones import SoftwareFJError, DatosInvalidosError
# Se importan las funciones para registrar eventos y errores en logs.txt
from logging_config import registrar_evento, registrar_error


class SistemaSoftwareFJ:
    """Clase principal que coordina clientes, servicios, reservas, pruebas y menú."""

    def __init__(self):
        # Inicializa las colecciones en memoria (el sistema opera sin base de datos)
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, identificacion, nombre, correo, telefono):
        # Crea y valida una nueva instancia de Cliente
        cliente = Cliente(identificacion, nombre, correo, telefono)

        # Evita registrar dos clientes con la misma identificación
        if any(c.identificacion == cliente.identificacion for c in self.clientes):
            raise DatosInvalidosError("La identificacion ya existe.")

        # Agrega el cliente a la lista, registra el evento en el log y notifica en consola
        self.clientes.append(cliente)
        registrar_evento(f"Cliente registrado: {nombre}")
        print("Cliente registrado correctamente.")
        return cliente

    def registrar_servicio(self, servicio):
        # Impide registrar servicios duplicados con el mismo código
        if any(s.codigo == servicio.codigo for s in self.servicios):
            raise DatosInvalidosError("El codigo del servicio ya existe.")

        # Guarda el servicio, registra el evento en el log y confirma en consola
        self.servicios.append(servicio)
        registrar_evento(f"Servicio registrado: {servicio.nombre}")
        print("Servicio registrado correctamente.")

    def buscar_cliente(self, identificacion):
        # Busca el cliente por su identificación y lo retorna si existe
        for cliente in self.clientes:
            if cliente.identificacion == identificacion:
                return cliente

        # Si no se encuentra, lanza error de datos inválidos
        raise DatosInvalidosError("Cliente no encontrado.")

    def buscar_servicio(self, codigo):
        # Busca el servicio por su código y lo retorna si existe
        for servicio in self.servicios:
            if servicio.codigo == codigo:
                return servicio

        # Si no existe, lanza error
        raise DatosInvalidosError("Servicio no encontrado.")

    def buscar_reserva(self, codigo):
        # Busca la reserva por su código y la retorna si existe
        for reserva in self.reservas:
            if reserva.codigo == codigo:
                return reserva

        # Si no existe, lanza error
        raise DatosInvalidosError("Reserva no encontrada.")

    def crear_reserva(self, identificacion, codigo_servicio, duracion):
        # Localiza el cliente y el servicio solicitados
        cliente = self.buscar_cliente(identificacion)
        servicio = self.buscar_servicio(codigo_servicio)

        # Instancia la reserva y calcula su total aplicando un 19% de impuesto
        reserva = Reserva(cliente, servicio, duracion)
        reserva.procesar(impuesto=19)

        # Almacena la reserva, muestra su información y la retorna
        self.reservas.append(reserva)
        print(reserva.mostrar_info())
        return reserva

    def confirmar_reserva(self, codigo):
        # Busca la reserva, la confirma y muestra mensaje de éxito
        reserva = self.buscar_reserva(codigo)
        reserva.confirmar()
        print("Reserva confirmada.")

    def cancelar_reserva(self, codigo):
        # Busca la reserva, la cancela y muestra mensaje de éxito
        reserva = self.buscar_reserva(codigo)
        reserva.cancelar()
        print("Reserva cancelada.")

    def mostrar_clientes(self):
        # Imprime el listado de clientes registrados usando polimorfismo en mostrar_info()
        print("\n--- CLIENTES ---")
        for cliente in self.clientes:
            print(cliente.mostrar_info())
            print("----------------")

    def mostrar_servicios(self):
        # Imprime la descripción polimórfica, precio base y disponibilidad de cada servicio
        print("\n--- SERVICIOS ---")
        for servicio in self.servicios:
            print(servicio.describir_servicio())
            print(f"Precio: ${servicio.precio_base:,.2f}")
            print(f"Disponible: {servicio.disponible}")
            print("----------------")

    def mostrar_reservas(self):
        # Imprime el detalle de todas las reservas registradas
        print("\n--- RESERVAS ---")
        for reserva in self.reservas:
            print(reserva.mostrar_info())
            print("----------------")

    def ejecutar_pruebas(self):
        """Ejecuta doce escenarios de prueba automatizados para validar el sistema."""

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

        # Prueba 3: cliente con nombre vacio (debe lanzar excepción controlada).
        try:
            self.registrar_cliente(
                "1003", "", "error@gmail.com", "3001234567"
            )
        except Exception as error:
            registrar_error(f"Prueba 3: {error}")
            print("Error controlado:", error)

        # Prueba 4: registro de servicio de sala.
        try:
            sala = ReservaSala(
                "S01", "Sala de reuniones", 50000, 10
            )
            self.registrar_servicio(sala)
        except Exception as error:
            registrar_error(f"Prueba 4: {error}")
            print(error)

        # Prueba 5: registro de servicio de alquiler de equipo.
        try:
            equipo = AlquilerEquipo(
                "E01", "Computador portatil", 30000, "Portatil"
            )
            self.registrar_servicio(equipo)
        except Exception as error:
            registrar_error(f"Prueba 5: {error}")
            print(error)

        # Prueba 6: registro de servicio de asesoría.
        try:
            asesoria = Asesoria(
                "A01", "Asesoria de software", 80000, "Programacion"
            )
            self.registrar_servicio(asesoria)
        except Exception as error:
            registrar_error(f"Prueba 6: {error}")
            print(error)

        # Prueba 7: precio negativo o cero (debe lanzar excepción controlada).
        try:
            sala_invalida = ReservaSala(
                "S02", "Sala invalida", -1000, 10
            )
            self.registrar_servicio(sala_invalida)
        except Exception as error:
            registrar_error(f"Prueba 7: {error}")
            print("Error controlado:", error)

        # Prueba 8: creación y procesamiento de reserva válida.
        reserva1 = None
        try:
            reserva1 = self.crear_reserva("1001", "S01", 2)
        except Exception as error:
            registrar_error(f"Prueba 8: {error}")
            print(error)

        # Prueba 9: confirmación de la reserva creada en la prueba 8.
        try:
            if reserva1 is not None:
                self.confirmar_reserva(reserva1.codigo)
        except Exception as error:
            registrar_error(f"Prueba 9: {error}")
            print(error)

        # Prueba 10: creación y posterior cancelación de una segunda reserva.
        try:
            reserva2 = self.crear_reserva("1002", "E01", 3)
            self.cancelar_reserva(reserva2.codigo)
        except Exception as error:
            registrar_error(f"Prueba 10: {error}")
            print(error)

        # Prueba 11: intento de reservar un servicio marcado como no disponible.
        try:
            asesoria.cambiar_disponibilidad(False)
            self.crear_reserva("1001", "A01", 1)
        except Exception as error:
            registrar_error(f"Prueba 11: {error}")
            print("Error controlado:", error)

        # Prueba 12: búsqueda de un código de reserva inexistente.
        try:
            self.buscar_reserva("R-999")
        except Exception as error:
            registrar_error(f"Prueba 12: {error}")
            print("Error controlado:", error)

        # Informa el cierre de las pruebas y dónde consultar el log
        print("\nSe ejecutaron 12 escenarios de prueba.")
        print("Consulte logs.txt para revisar los registros.")

    def menu(self):
        """Muestra el menú interactivo en consola para operar el sistema."""

        # Bucle principal hasta que el usuario elija la opción 8 (Salir)
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

            # Lee y limpia la opción seleccionada por el usuario
            opcion = input("Seleccione una opcion: ").strip()

            try:
                if opcion == "1":
                    # Solicita datos del cliente y llama a registrar_cliente
                    identificacion = input("Identificacion: ")
                    nombre = input("Nombre: ")
                    correo = input("Correo: ")
                    telefono = input("Telefono: ")
                    self.registrar_cliente(
                        identificacion, nombre, correo, telefono
                    )

                elif opcion == "2":
                    # Muestra los clientes registrados
                    self.mostrar_clientes()

                elif opcion == "3":
                    # Muestra los servicios disponibles y no disponibles
                    self.mostrar_servicios()

                elif opcion == "4":
                    # Solicita datos y convierte la duración a flotante
                    identificacion = input("Identificacion del cliente: ")
                    codigo = input("Codigo del servicio: ")
                    duracion = float(input("Duracion: "))
                    self.crear_reserva(identificacion, codigo, duracion)

                elif opcion == "5":
                    # Confirma una reserva existente por su código
                    codigo = input("Codigo de reserva: ")
                    self.confirmar_reserva(codigo)

                elif opcion == "6":
                    # Cancela una reserva existente por su código
                    codigo = input("Codigo de reserva: ")
                    self.cancelar_reserva(codigo)

                elif opcion == "7":
                    # Muestra todas las reservas registradas
                    self.mostrar_reservas()

                elif opcion == "8":
                    # Registra el cierre del sistema y termina el ciclo
                    print("Gracias por utilizar Software FJ.")
                    registrar_evento("Cierre del sistema.")
                    break

                else:
                    # Avisa si el número o texto ingresado no corresponde a ninguna opción
                    print("Opcion no valida.")

            except (SoftwareFJError, ValueError) as error:
                # Controla errores del dominio (SoftwareFJError) o conversiones inválidas (ValueError)
                registrar_error(f"Error en el menu: {error}")
                print("No se pudo completar:", error)

            except Exception as error:
                # Respaldo para cualquier excepción no prevista manteniendo el programa estable
                registrar_error(f"Error inesperado: {error}")
                print("Error inesperado:", error)


# Punto de entrada: solo se ejecuta si main.py es el archivo principal ejecutado
if __name__ == "__main__":
    sistema = SistemaSoftwareFJ()
    sistema.ejecutar_pruebas()
    sistema.menu()