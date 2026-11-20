class SoftwareFJError(Exception):
    """Excepcion base principal del sistema Software FJ; hereda de Exception."""


class DatosInvalidosError(SoftwareFJError):
    """Excepcion lanzada cuando los datos ingresados no cumplen las reglas de validacion."""


class ClienteNoEncontradoError(SoftwareFJError):
    """Excepcion lanzada cuando no se encuentra un cliente registrado en el sistema."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Excepcion lanzada cuando un servicio no esta disponible para ser reservado."""


class ReservaError(SoftwareFJError):
    """Excepcion lanzada ante fallos relacionados con la creacion o gestion de reservas."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Excepcion lanzada cuando se intenta realizar una operacion no permitida."""




