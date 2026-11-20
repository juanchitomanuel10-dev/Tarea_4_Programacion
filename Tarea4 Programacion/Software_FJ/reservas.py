# Se importan las excepciones personalizadas necesarias para validar y controlar errores en reservas
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    ReservaError,
    OperacionNoPermitidaError
)
# Se importan las funciones de registro para guardar eventos y errores en logs.txt
from logging_config import registrar_evento, registrar_error


class Reserva:
    """Clase encargada de administrar el ciclo de vida y costo de las reservas."""

    # Contador de clase para generar códigos secuenciales únicos (R-001, R-002, etc.)
    contador = 0

    def __init__(self, cliente, servicio, duracion):
        # Verifica que se haya asignado un cliente válido
        if cliente is None:
            raise DatosInvalidosError("Debe seleccionar un cliente.")

        # Verifica que se haya asignado un servicio válido
        if servicio is None:
            raise DatosInvalidosError("Debe seleccionar un servicio.")

        # Verifica que la duración sea un número positivo (excluyendo booleanos, ya que en Python bool es subclase de int)
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser positiva.")

        # Incrementa el contador global y formatea el código de la reserva con ceros a la izquierda
        Reserva.contador += 1
        self._codigo = f"R-{Reserva.contador:03d}"
        # Guarda las referencias al cliente y servicio en atributos protegidos
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        # Toda reserva inicia en estado "Pendiente" y con total en 0.0 hasta procesarse
        self._estado = "Pendiente"
        self._total = 0.0

    @property
    def codigo(self):
        # Retorna el código único de la reserva
        return self._codigo

    @property
    def estado(self):
        # Retorna el estado actual de la reserva ("Pendiente", "Confirmada" o "Cancelada")
        return self._estado

    @property
    def total(self):
        # Retorna el monto total calculado para la reserva
        return self._total

    def procesar(self, impuesto=0, descuento=0):
        """Procesa la reserva, valida disponibilidad y calcula su costo total."""

        try:
            # Solo se pueden procesar reservas que estén en estado "Pendiente"
            if self._estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    "La reserva no esta pendiente."
                )

            # Verifica que el servicio asociado se encuentre disponible
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    "El servicio no esta disponible."
                )

            # Calcula el costo aplicando duración, impuesto y descuento según el tipo de servicio
            self._total = self._servicio.calcular_costo(
                self._duracion, impuesto, descuento
            )

        except Exception as error:
            # Registra el error en el log y relanza una ReservaError encadenada con el error original
            registrar_error(f"Error procesando {self.codigo}: {error}")
            raise ReservaError(
                f"No se pudo procesar la reserva: {error}"
            ) from error

        else:
            # Se ejecuta solo si el bloque try terminó sin excepciones: registra el éxito y retorna el total
            registrar_evento(
                f"Reserva {self.codigo} procesada. Total: {self.total}"
            )
            return self._total

        finally:
            # Se ejecuta siempre al terminar el procesamiento, haya habido error o no
            registrar_evento(
                f"Finalizo el procesamiento de {self.codigo}."
            )

    def confirmar(self):
        """Confirma una reserva que esté pendiente y tenga un total válido mayor que cero."""

        # Impide confirmar si no está pendiente o si aún no se ha calculado un total positivo
        if self._estado != "Pendiente" or self._total <= 0:
            error = OperacionNoPermitidaError(
                "La reserva no puede confirmarse."
            )
            registrar_error(str(error))
            raise error

        # Actual
