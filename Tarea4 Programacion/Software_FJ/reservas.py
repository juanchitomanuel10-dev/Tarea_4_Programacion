
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    ReservaError,
    OperacionNoPermitidaError
)
from logging_config import registrar_evento, registrar_error


class Reserva:
    """Clase encargada de administrar las reservas."""

    contador = 0

    def __init__(self, cliente, servicio, duracion):
        if cliente is None:
            raise DatosInvalidosError("Debe seleccionar un cliente.")

        if servicio is None:
            raise DatosInvalidosError("Debe seleccionar un servicio.")

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser positiva.")

        Reserva.contador += 1
        self._codigo = f"R-{Reserva.contador:03d}"
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "Pendiente"
        self._total = 0.0

    @property
    def codigo(self):
        return self._codigo

    @property
    def estado(self):
        return self._estado

    @property
    def total(self):
        return self._total

    def procesar(self, impuesto=0, descuento=0):
        """Procesa la reserva y calcula su costo."""

        try:
            if self._estado != "Pendiente":
                raise OperacionNoPermitidaError(
                    "La reserva no esta pendiente."
                )

            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    "El servicio no esta disponible."
                )

            self._total = self._servicio.calcular_costo(
                self._duracion, impuesto, descuento
            )

        except Exception as error:
            registrar_error(f"Error procesando {self.codigo}: {error}")
            raise ReservaError(
                f"No se pudo procesar la reserva: {error}"
            ) from error

        else:
            registrar_evento(
                f"Reserva {self.codigo} procesada. Total: {self.total}"
            )
            return self._total

        finally:
            registrar_evento(
                f"Finalizo el procesamiento de {self.codigo}."
            )

    def confirmar(self):
        """Confirma una reserva procesada."""

        if self._estado != "Pendiente" or self._total <= 0:
            error = OperacionNoPermitidaError(
                "La reserva no puede confirmarse."
            )
            registrar_error(str(error))
            raise error

        self._estado = "Confirmada"
        registrar_evento(f"Reserva {self.codigo} confirmada.")

    def cancelar(self):
        """Cancela una reserva."""

        if self._estado == "Cancelada":
            error = OperacionNoPermitidaError(
                "La reserva ya esta cancelada."
            )
            registrar_error(str(error))
            raise error

        self._estado = "Cancelada"
        registrar_evento(f"Reserva {self.codigo} cancelada.")

    def mostrar_info(self):
        return (
            f"\nCodigo: {self.codigo}\n"
            f"Cliente: {self._cliente.nombre}\n"
            f"Servicio: {self._servicio.nombre}\n"
            f"Duracion: {self._duracion}\n"
            f"Estado: {self.estado}\n"
            f"Total: ${self.total:,.2f}"
        )
