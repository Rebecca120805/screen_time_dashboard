import pandas as pd

def load_data (path="data/screentime.csv"):
  """Lädt die Screentime CSV-Datei und gibt ein DataFrame zurück."""
  return pd.read_csv(path)
