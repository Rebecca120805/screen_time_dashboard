import streamlit as st
import pandas as pd

from data_loader import (
  list_week_files,
  load_week_data
)
from data_analyzer import (
  get_top_5_apps_per_day,
  get_top_5_total_time,
  get_daily_total
)
from logging_config import setup_logger

#Logger
logger = setup_logger(__name__)

#Titel
st.title("📊Bildschirmzeit Dashboard")
logger.info("Dashboard gestartet")

#Auswahl der lokalen Wochen-Datei
st.header("📂 Datenauswahl")
week_files = list_week_files()

#Wenn keine Files vorhanden sind
if not week_files:
  logger.critical("Keine lokalen Wochen-CSV-Dateien gefunden")
  st.error("Keine lokalen Screentime-Daten gefunden.")
  st.stop()

selected_week = st.selectbox(
  "Wähle eine Kalenderwoche",
  week_files
)

logger.info(f"Ausgewählte Wochendatei: {selected_week}")

#Wochendaten laden
df = load_week_data(selected_week)

if df.empty:
  logger.warning("Ausgewählte Wochendatei enthält keine Daten")
  st.warning("Die ausgewählte Woche enthält keine Daten.")
  st.stop()

#Wochenübersicht der täglichen Bildschirmzeit - Barchart
st.header("📅 Gesamte Bildschirmzeit der Woche")
logger.info("Starte Berechnung der wöchentlichen Gesamtnutzung")

try:
  daily_total = get_daily_total(df)

except ValueError:
  logger.warning("Keine gültigen Tagesdaten für Wochenübersicht vorhanden")
  st.warning("Keine Tagesdaten zur Anzeige verfügbar.")
  st.stop()

except Exception:
  logger.critical("Kritischer Fehler bei der Berechnung der WOchennutzung", exc_info = True)
  st.error("Ein interner Fehler ist bei der Wochenauswertung aufgetreten.")
  st.stop()

st.subheader("Gesamte Nutzung pro Tag in Minuten")
logger.info("Zeige Diagramm: Gesamte Bildschirmzeit pro Tag")
st.bar_chart(daily_total)

#Tag auswählen für Detaildaten
st.header("🔎 Detailansicht für einen Tag")

available_dates = sorted(df["date"].unique())

selected_date = st.selectbox(
  "Wähle einen Tag für die Detailanalyse",
  available_dates
)

logger.info(f"Ausgewählter Tag für Detailansicht: {selected_date}")

filtered_df = df[df["date"] == selected_date] #Nur Daten für den gewählten Tag

#Top 5 Apps für Tag berechnen
st.header("🏆 Top 5 Apps am ausgewählten Tag")
logger.info("Starte Berechnung Top-5-Apps für Detailtag")

try:
  top5_dict = get_top_5_apps_per_day(filtered_df)
  top5_apps = top5_dict[selected_date]
  top5_total_time = int(top5_apps.sum())

except ValueError:
  logger.warning("Top-5-Berechnung nicht möglich  keine gültigen Daten")
  st.warning("Top-5-Apps können nicht berechnet werden.")
  st.stop()

except Exception:
  logger.critical("Kritischer Fehler bei der Top-5-Berechnung", exc_info = True)
  st.error("Ein interner Fehler ist bei der Top-5-Auswertung aufgetreten.")
  st.stop()

logger.debug(f"Zeige Top-5-Apps für {selected_date}")

st.subheader(f"{selected_date} - Top 5 Apps")
st.table(top5_apps)


#Gesamtzeit der Top 5
st.write(f"Gesamtnutzungszeit der Top-5-Apps:** {top5_total_time} Minuten")
