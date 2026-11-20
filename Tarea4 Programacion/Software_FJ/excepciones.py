
class SoftwareFJError(Exception):
    """Excepcion principal del sistema."""


class DatosInvalidosError(SoftwareFJError):
    """Error cuando los datos ingresados no son validos."""


class ClienteNoEncontradoError(SoftwareFJError):
    """Error cuando no se encuentra un cliente."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Error cuando un servicio no esta disponible."""


class ReservaError(SoftwareFJError):
    """Error relacionado con las reservas."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Error cuando se intenta realizar una operacion no permitida."""
