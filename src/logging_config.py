import os
import logging
from logging import Logger


def setup_logger(name: str) -> Logger:
    """Erstellt und konfiguriert einen Logger mit zwei Handlern:
    - Console-Ausgabe für kritische Meldungen (ERROR/CRITICAL)
    - Datei-Ausgabe für alle Meldungen (DEBUG bis CRITICAL)"""

    # Verhindern doppelter Logs, falls der Logger mehrfach erstellt wird
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    os.makedirs("logs", exist_ok=True)

    # Formatter

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler (hohe Dringlichkeit)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)

    # File Handler (alle Logs)

    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler hinzufügen

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
