
from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError


class Servicio(ABC):
    """Clase abstracta para los servicios de Software FJ."""

    def __init__(self, codigo, nombre, precio_base, disponible=True):
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatosInvalidosError("El codigo es obligatorio.")

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre es obligatorio.")

        if isinstance(precio_base, bool) or not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise DatosInvalidosError("El precio debe ser mayor que cero.")

        if not isinstance(disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser booleana.")

        self._codigo = codigo.strip()
        self._nombre = nombre.strip()
        self._precio_base = float(precio_base)
        self._disponible = disponible

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio_base(self):
        return self._precio_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise DatosInvalidosError("Estado de disponibilidad incorrecto.")
        self._disponible = estado

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Calcula costos con impuestos y descuentos opcionales."""

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser positiva.")

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 100:
            raise DatosInvalidosError("Impuesto no valido.")

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not 0 <= descuento <= 100:
            raise DatosInvalidosError("Descuento no valido.")

        subtotal = self._precio_base * duracion
        valor_impuesto = subtotal * impuesto / 100
        valor_descuento = subtotal * descuento / 100

        return round(subtotal + valor_impuesto - valor_descuento, 2)

    @abstractmethod
    def describir_servicio(self):
        pass


class ReservaSala(Servicio):
    """Servicio de reserva de salas."""

    def __init__(self, codigo, nombre, precio_base, capacidad, disponible=True):
        super().__init__(codigo, nombre, precio_base, disponible)

        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser positiva.")

        self.capacidad = capacidad

    def describir_servicio(self):
        return f"Sala: {self.nombre}. Capacidad: {self.capacidad} personas."


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos."""

    def __init__(self, codigo, nombre, precio_base, tipo_equipo, disponible=True):
        super().__init__(codigo, nombre, precio_base, disponible)

        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise DatosInvalidosError("El tipo de equipo es obligatorio.")

        self.tipo_equipo = tipo_equipo.strip()

    def describir_servicio(self):
        return f"Equipo: {self.nombre}. Tipo: {self.tipo_equipo}."


class Asesoria(Servicio):
    """Servicio de asesorias especializadas."""

    def __init__(self, codigo, nombre, precio_base, especialidad, disponible=True):
        super().__init__(codigo, nombre, precio_base, disponible)

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError("La especialidad es obligatoria.")

        self.especialidad = especialidad.strip()

    def describir_servicio(self):
        return f"Asesoria: {self.nombre}. Especialidad: {self.especialidad}."
