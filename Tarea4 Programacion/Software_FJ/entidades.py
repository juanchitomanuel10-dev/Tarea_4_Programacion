# Se importan ABC y abstractmethod para definir clases abstractas que sirven como plantilla
from abc import ABC, abstractmethod
# Se importa la excepción personalizada para notificar datos inválidos o vacíos
from excepciones import DatosInvalidosError


class Entidad(ABC):
    """Clase abstracta base para las entidades del sistema."""

    def __init__(self, identificacion):
        # Verifica que la identificación sea un texto y que no esté vacía tras quitar espacios
        if not isinstance(identificacion, str) or not identificacion.strip():
            # Lanza error si la identificación no cumple con el formato requerido
            raise DatosInvalidosError("La identificacion es obligatoria.")

        # Guarda la identificación limpia de espacios en un atributo protegido
        self._identificacion = identificacion.strip()

    @property
    def identificacion(self):
        # Expone el atributo protegido de identificación de forma controlada (solo lectura)
        return self._identificacion

    @abstractmethod
    def mostrar_info(self):
        # Método abstracto que obliga a las subclases a definir cómo mostrar su información
        pass


class Cliente(Entidad):
    """Clase que representa a los clientes y hereda de Entidad."""

    def __init__(self, identificacion, nombre, correo, telefono):
        # Llama al constructor de Entidad para validar y asignar la identificación
        super().__init__(identificacion)

        # Verifica que el nombre sea una cadena de texto y no quede vacío
        if not isinstance(nombre, str) or not nombre.strip():
            # Lanza error si falta el nombre del cliente
            raise DatosInvalidosError("El nombre es obligatorio.")

        # Verifica que el correo sea texto y contenga '@' y '.' como validación básica
        if not isinstance(correo, str) or "@" not in correo or "." not in correo:
            # Lanza error si el correo no tiene un formato válido
            raise DatosInvalidosError("El correo no es valido.")

        # Verifica que el teléfono sea numérico y tenga mínimo 7 dígitos
        if not isinstance(telefono, str) or not telefono.isdigit() or len(telefono) < 7:
            # Lanza error si el teléfono no cumple con los dígitos requeridos
            raise DatosInvalidosError("El telefono debe tener al menos 7 digitos.")

        # Almacena los datos ya validados y sin espacios extra en atributos protegidos
        self._nombre = nombre.strip()
        self._correo = correo.strip()
        self._telefono = telefono.strip()

    @property
    def nombre(self):
        # Retorna el nombre del cliente
        return self._nombre

    @property
    def correo(self):
        # Retorna el correo electrónico del cliente
        return self._correo

    @property
    def telefono(self):
        # Retorna el número de teléfono del cliente
        return self._telefono

    def mostrar_info(self):
        # Implementa el método abstracto devolviendo los datos del cliente formateados
        return (
            f"Identificacion: {self.identificacion}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}\n"
            f"Telefono: {self.telefono}"
        )
