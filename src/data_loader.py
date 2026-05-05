import pandas as pd
import os
from logging_config import setup_logger

logger = setup_logger(__name__)

#Fester lokaler basis-Pfad (Laptop)
DATA_DIR = os.path.expanduser("~/screentime_data")

def list_week_files() -> list[str]:
  """ Listet alle lokal vorhandenen Wochen-Csv-Dateien auf"""

  try:
    files = [
      f for f in os.listdir(DATA_DIR)
      if f.endswith(".csv")
    ]
    logger.info("Lokale Wochen-Dateien erfolgreich ausgelesen")
    return sorted(files)

  except FileNotFoundError:
    logger.critical("Lokaler Screentime-Datenordner nicht gefunden")
    return []

  except Exception:
    logger.exception("Fehler beim Lesen des lokalen Datenordners")
    return []

def load_week_data(filename: str) -> pd.DataFrame:
  """Lädt eine lokal gespeicherte Wochen-CSV-Datei"""

  path = os.path.join(DATA_DIR, filename)

  try:
    df = pd.read_csv(path)
    logger.info(f"Wochendatei geladen: {filename}")
    return df

  except FileNotFoundError:
    logger.error(f"Wochendatei nicht gefunden: {filename}")
    return pd.DataFrame()

  except Exception:
    logger.exception(f"Fehler beim laden der Datei: {filename}")
    return pd.DataFrame()

#Legacy-Funktion
#Wird nicht verwendet, weil Umstieg auf lokale wochenbasierte CSV-Dateien
#def load_data (path: str = "data/screentime.csv") -> pd.DataFrame:
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

