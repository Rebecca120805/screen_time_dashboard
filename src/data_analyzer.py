import pandas as pd

def get_daily_total(df):
  """Gibt die gesamte Bildschirmzeit pro Tag zurück"""
  return df.groupby("date")["usage_minutes"].sum()

def get_top_5_apps_per_day(df):
  """Gibt für jeden Tag die Top 5 meistgenutzten Apps zurück."""
  result = {}
  for date, group in df.groupby("date"):
    top5 = group.groupby("app")["usage_minutes"].sum().sort_values(ascending=False).head(5)
    result[date] = top5

  return result

def get_top_5_total_time(top5_dict):
  """Berechnet für jeden Tag die Summe der Nutzungszeit der jeweiligen Top 5 Apps"""
  totals= {}
  for date, series in top5_dict.items():
    totals[date] = series.sum()

  return totals
