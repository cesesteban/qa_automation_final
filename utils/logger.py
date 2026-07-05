import logging
import pathlib

# Crea el directorio de logs si no existe
pathlib.Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    filename="logs/suite.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s – %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("qa_final")
