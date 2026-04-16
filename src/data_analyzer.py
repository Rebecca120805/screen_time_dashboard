import pandas as pd

def get_daily_total(df):
  """Gibt die gesamte Bildschirmzeit pro Tag zurück.

    Die Funktion gruppiert die übergebenen Screentime-Daten nach Datum und summiert die Nutzungsdauer aller Apps für jeden einzelnen Tag.

    :param df: Pandas DataFrame mit den Spalten
      - 'date' (Datum in Format YYYY-MM-DD)
      - 'usage_minutes' (Nutzungsdauer in Minuten)

    :return: Pandas Series mit dem Datum als INdex und der gesamten Nutzungszeit pro tag als Wert"""
  return df.groupby("date")["usage_minutes"].sum()


def get_top_5_apps_per_day(df):
  """Gibt für jeden Tag die Top 5 meistgenutzten Apps zurück.

    :param df: Pandas DataFrame mit ScreenTime-Daten
        (Spalten: 'date', 'app', 'usage_minutes')
    :return: Dictionary mit Datum als Key und einer Pandas Series (Top-5-Apps pro Tag) als Value"""
  result = {}
  for date, group in df.groupby("date"): #Daten werden nach Tagen getrennt
    top5 = (
      group.groupby("app")["usage_minutes"]
      .sum() #Nutzungszeit pro App pro Tag
      .sort_values(ascending=False). #Sortierung absteigend
      head(5) #Top 5 Apps
    )
    result[date] = top5

  return result


def get_top_5_total_time(top5_dict):
  """Berechnet für jeden Tag die Summe der Nutzungszeit der jeweiligen Top 5 Apps.

      :param top5_dict: Dictionary mit Datum als Key und Pandas Series (Top-5-Apps) als Value
      :return: Dictionary mit Datum und Gesamtzeit der Top-5-Apps"""
  totals= {}
  for date, series in top5_dict.items():
    totals[date] = series.sum()

  return totals
