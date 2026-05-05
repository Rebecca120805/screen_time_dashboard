import pandas as pd
from logging_config import setup_logger

logger = setup_logger(__name__)

def load_data (path: str = "data/screentime.csv") -> pd.DataFrame:
  """Lädt die screentime Daten aus der CSV-Datei und gibt ein DataFrame zurück.
      :param: path: Pfad zur CSV-Datei
      :return: Pandas DataFrame mit Screentime-Daten"""

  try:
    df = pd.read_csv(path)
    logger.info("CSV-Datei erfolgreich geladen")
    return df

  except FileNotFoundError:
    logger.critical(f"CSV-Datei nicht gefunden: {path}")
    return pd.DataFrame()

  except Exception:
    logger.exception("Unerwarteter Fehler beim Laden der CSV")
    return pd.DataFrame()

