
# Se importa el módulo estándar logging para registrar eventos y errores en archivo
import logging

# Configura el sistema de registro (logging) de forma global
logging.basicConfig(
    # Archivo de destino donde se guardarán los registros
    filename="logs.txt",
    # Nivel mínimo de registro: INFO captura info, advertencias y errores
    level=logging.INFO,
    # Formato de cada línea: fecha/hora - nivel del mensaje - contenido del mensaje
    format="%(asctime)s - %(levelname)s - %(message)s",
    # Codificación UTF-8 para soportar tildes y caracteres especiales sin fallos
    encoding="utf-8"
)

# Crea o recupera un logger con nombre "SoftwareFJ" para identificar los mensajes del sistema
logger = logging.getLogger("SoftwareFJ")


def registrar_evento(mensaje):
    """Registra operaciones exitosas o eventos normales en el archivo de logs."""
    # Escribe el mensaje con nivel INFO en logs.txt
    logger.info(mensaje)


def registrar_error(mensaje):
    """Registra errores o excepciones controladas en el archivo de logs."""
    # Escribe el mensaje con nivel ERROR en logs.txt
    logger.error(mensaje)
