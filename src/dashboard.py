import streamlit as st
import pandas as pd
from data_loader import load_data
from data_analyzer import (
  get_top_5_app_per_day,
  get_top_5_total_time
)

#Titel
st.title("Bildschirmzeit Dashboard")

#Daten laden
df = load_data()

#Wenn CSV noch leer ist
if df.empty:
  st.warning("Die Datei 'screentime.csv' ist noch leer. Bitte füge Daten hinzu.")
  st.stop()

#Übersicht pro Tag
st.header("Tagesübersicht der Bildschrimzeit")

#Gesamtnutzung pro Tag(einfaches Diagramm)
daily_total = df.groupby("date")["usage_minutes"].sum()
st.subheader("Gesamte Nutzung pro Tag in Minuten")
st.bar_chart(daily_total)

#Top 5 Apps pro Tag berechnen
top5_dict = get_top_5_apps_per_day(df)
top5_totals = get_top_5_totaltime(top5_dict)

st.header("Top 5 Apps pro Tag")

for date, apps in top5_dict.items():
  st.subheader(f"{date} - Top 5 Apps")

  #Tabelle der 5 Apps
  st.table(apps)

  #Gesamtzeit der Top 5
  st.write(f"Gesamtnutzungszeit der Top-5-Apps: {top5_totals[date]} Minuten")
