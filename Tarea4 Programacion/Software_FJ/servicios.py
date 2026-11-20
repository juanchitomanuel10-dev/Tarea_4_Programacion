# Se importan ABC y abstractmethod para definir la clase abstracta base Servicio
from abc import ABC, abstractmethod
# Se importa DatosInvalidosError para reportar parámetros inválidos en validaciones
from excepciones import DatosInvalidosError


class Servicio(ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, codigo, nombre, precio_base, disponible=True):
        # Valida que el código sea un texto no vacío
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatosInvalidosError("El codigo es obligatorio.")

        # Valida que el nombre sea un texto no vacío
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre es obligatorio.")

        # Valida que precio_base sea numérico (no booleano) y mayor que cero
        if isinstance(precio_base, bool) or not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise DatosInvalidosError("El precio debe ser mayor que cero.")

        # Valida que disponible sea un valor booleano (True o False)
        if not isinstance(disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser booleana.")

        # Asigna los atributos protegidos limpios y normalizados
        self._codigo = codigo.strip()
        self._nombre = nombre.strip()
        self._precio_base = float(precio_base)
        self._disponible = disponible

    @property
    def codigo(self):
        # Retorna el código del servicio
        return self._codigo

    @property
    def nombre(self):
        # Retorna el nombre del servicio
        return self._nombre

    @property
    def precio_base(self):
        # Retorna el precio base por unidad de duración
        return self._precio_base

    @property
    def disponible(self):
        # Indica si el servicio está disponible actualmente
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        # Valida que el nuevo estado sea booleano y actualiza la disponibilidad del servicio
        if not isinstance(estado, bool):
            raise DatosInvalidosError("Estado de disponibilidad incorrecto.")
        self._disponible = estado

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Calcula el costo total según duración, impuesto y descuento opcionales (en porcentaje)."""

        # Valida que la duración sea un número positivo y no un booleano
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duracion debe ser positiva.")

        # Valida que el impuesto sea numérico y esté entre 0 y 100 (%)
        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 100:
            raise DatosInvalidosError("Impuesto no valido.")

        # Valida que el descuento sea numérico y esté entre 0 y 100 (%)
        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not 0 <= descuento <= 100:
            raise DatosInvalidosError("Descuento no valido.")

        # Calcula el subtotal multiplicando precio base por duración
        subtotal = self._precio_base * duracion
        # Calcula el monto del impuesto y el monto del descuento sobre el subtotal
        valor_impuesto = subtotal * impuesto / 100
        valor_descuento = subtotal * descuento / 100

        # Retorna el total neto redondeado a 2 decimales
        return round(subtotal + valor_impuesto - valor_descuento, 2)

    @abstractmethod
    def describir_servicio(self):
        # Método abstracto: cada subclase debe entregar su propia descripción
        pass


class ReservaSala(Servicio):
    """Subclase que representa el servicio de reserva de salas."""

    def __init__(self, codigo, nombre, precio_base, capacidad, disponible=True):
        # Inicializa los atributos comunes desde la clase padre Servicio
        super().__init__(codigo, nombre, precio_base, disponible)

        # Valida que la capacidad sea un entero positivo (excluyendo booleanos)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad debe ser positiva.")

        # Guarda la capacidad máxima de personas de la sala
        self.capacidad = capacidad

    def describir_servicio(self):
        # Implementación polimórfica de describir_servicio para salas
        return f"Sala: {self.nombre}. Capacidad: {self.capacidad} personas."


class AlquilerEquipo(Servicio):
    """Subclase que representa el servicio de alquiler de equipos."""

    def __init__(self, codigo, nombre, precio_base, tipo_equipo, disponible=True):
        # Inicializa los atributos comunes desde Servicio
        super().__init__(codigo, nombre, precio_base, disponible)

        # Valida que el tipo de equipo sea un texto no vacío
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise DatosInvalidosError("El tipo de equipo es obligatorio.")

        # Guarda el tipo de equipo limpio de espacios
        self.tipo_equipo = tipo_equipo.strip()

    def describir_servicio(self):
        # Implementación polimórfica de describir_servicio para equipos
        return f"Equipo: {self.nombre}. Tipo: {self.tipo_equipo}."


class Asesoria(Servicio):
    """Subclase que representa el servicio de asesorías especializadas."""

    def __init__(self, codigo, nombre, precio_base, especialidad, disponible=True):
        # Inicializa los atributos comunes desde Servicio
        super().__init__(codigo, nombre, precio_base, disponible)

        # Valida que la especialidad sea un texto no vacío
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError("La especialidad es obligatoria.")

        # Guarda la especialidad limpia de espacios
        self.especialidad = especialidad.strip()

    def describir_servicio(self):
        # Implementación polimórfica de describir_servicio para asesorías
        return f"Asesoria: {self.nombre}. Especialidad: {self.especialidad}."
