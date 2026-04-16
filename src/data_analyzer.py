import pandas as pd

def get_daily_total(df):
  """Gibt die gesamte Bildschirmzeit pro Tag zurück"""
  return df.groupby("date")["usage_minutes"].sum()

def get_top_5_apps_per_day(df):
  """Gibt für jeden Tag die Top 5 meistgenutzten Apps zurück."""
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
  """Berechnet für jeden Tag die Summe der Nutzungszeit der jeweiligen Top 5 Apps
      :param top5_dict: Dictionary mit Datum als Key und Pandas Series (Top-5-Apps) als Value
      :return: Dictionary mit Datum und Gesamtzeit der Top-5-Apps"""
  totals= {}
  for date, series in top5_dict.items():
    totals[date] = series.sum()

  return totals
