
import logging

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("SoftwareFJ")


def registrar_evento(mensaje):
    """Registra operaciones exitosas."""
    logger.info(mensaje)


def registrar_error(mensaje):
    """Registra errores del sistema."""
    logger.error(mensaje)
