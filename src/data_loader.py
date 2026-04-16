import pandas as pd

def load_data (path="data/screentime.csv"):
  """Lädt die screentime Daten aus der CSV-Datei und gibt ein DataFrame zurück.
      :param: path: Pfad zur CSV-Datei
      :return: Pandas DataFrame mit Screentime-Daten"""
  return pd.read_csv(path)
