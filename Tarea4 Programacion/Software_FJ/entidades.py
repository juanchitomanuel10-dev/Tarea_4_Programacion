
from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError


class Entidad(ABC):
    """Clase abstracta para las entidades del sistema."""

    def __init__(self, identificacion):
        if not isinstance(identificacion, str) or not identificacion.strip():
            raise DatosInvalidosError("La identificacion es obligatoria.")

        self._identificacion = identificacion.strip()

    @property
    def identificacion(self):
        return self._identificacion

    @abstractmethod
    def mostrar_info(self):
        pass


class Cliente(Entidad):
    """Clase que representa a los clientes."""

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre es obligatorio.")

        if not isinstance(correo, str) or "@" not in correo or "." not in correo:
            raise DatosInvalidosError("El correo no es valido.")

        if not isinstance(telefono, str) or not telefono.isdigit() or len(telefono) < 7:
            raise DatosInvalidosError("El telefono debe tener al menos 7 digitos.")

        self._nombre = nombre.strip()
        self._correo = correo.strip()
        self._telefono = telefono.strip()

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono

    def mostrar_info(self):
        return (
            f"Identificacion: {self.identificacion}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}\n"
            f"Telefono: {self.telefono}"
        )
