import streamlit as st
import pandas as pd
from data_loader import load_data
from data_analyzer import (
  get_top_5_apps_per_day,
  get_top_5_total_time,
  get_daily_total
)
from logging_config import setup_logger

logger = setup_logger(__name__)

#Titel
st.title("Bildschirmzeit Dashboard")
logger.info("Dashboard gestartet")

#Daten laden
df = load_data()
logger.info("Daten aus CSV geladen")

#Wenn CSV noch leer ist
if df.empty:
  logger.warning("CSV-Datei leer oder keine gültigen Daten vorhanden")
  #signalisiert fachliches Problem, ohne den Programmablauf zu unterbrechen
  st.warning("Die Datei 'screentime.csv' ist noch leer. Bitte füge Daten hinzu.")
  st.stop()

#Übersicht pro Tag
st.header("Tagesübersicht der Bildschirmzeit")
logger.info("Berechne KPI-Werte")

#Gesamtnutzung pro Tag(einfaches Diagramm)
logger.info("Starte Berechnung der täglichen Gesamtnutzungszeit")

try:
  daily_total = get_daily_total(df)

except ValueError:
  logger.warning("Keine gültigen Tagesdaten vorhanden")
  st.warning("Keine Tagesdaten zur Anzeige verfügbar.")
  st.stop()

except Exception:
  logger.critical("Kritischer Fehler bei der Berechnung der Tagesnutzung", exc_info = True)
  st.error("Ein interner Fehler ist bei der Tagesauswertung aufgetreten.")
  st.stop()

st.subheader("Gesamte Nutzung pro Tag in Minuten")
logger.info("Zeige Diagramm: Gesamte Bildschirmzeit pro Tag")
st.bar_chart(daily_total)

#Top 5 Apps pro Tag berechnen
logger.info("Starte Berechnung Top-5-Apps pro Tag")

try:
  top5_dict = get_top_5_apps_per_day(df)
  top5_totals = get_top_5_total_time(top5_dict)

except ValueError:
  logger.warning("Top-5-Berechnung nicht möglich  keine gültigen Daten")
  st.warning("Top-5-Apps können nicht berechnet werden.")
  st.stop()

except Exception:
  logger.critical("Kritischer Fehler bei der Top-5-Berechnung", exc_info = True)
  st.error("Ein interner Fehler ist bei der Top-5-Auswertung aufgetreten.")
  st.stop()

st.header("Top 5 Apps pro Tag")

for date, apps in top5_dict.items():
  logger.debug(f"Zeige Top-5-Apps für {date}")

  st.subheader(f"{date} - Top 5 Apps")

  #Tabelle der 5 Apps
  st.table(apps)

  #Gesamtzeit der Top 5
  st.write(f"Gesamtnutzungszeit der Top-5-Apps: {top5_totals[date]} Minuten")
