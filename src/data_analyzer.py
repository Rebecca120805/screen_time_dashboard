import pandas as pd
from logging_config import setup_logger

logger = setup_logger(__name__)


def get_daily_total(df: pd.DataFrame) -> pd.Series:
    """Gibt die gesamte Bildschirmzeit pro Tag zurück.

    Die Funktion gruppiert die übergebenen Screentime-Daten nach Datum und summiert die Nutzungsdauer aller Apps für jeden einzelnen Tag.

    :param df: Pandas DataFrame mit den Spalten
      - 'date' (Datum in Format YYYY-MM-DD)
      - 'usage_minutes' (Nutzungsdauer in Minuten)

    :return: Pandas Series mit dem Datum als INdex und der gesamten Nutzungszeit pro tag als Wert"""

    logger.info("Starte Berechnung der täglichen Gesamtnutzungszeit")

    if df.empty:
        logger.warning("Leeres DataFrame übergeben - keine Tagesauswertung möglich")
        raise ValueError("Keine Daten für Tagesauswertung vorhanden")

    try:
        daily_total = df.groupby("date")["usage_minutes"].sum()

        logger.info("Tägliche Gesamtnutzungszeit erfolgreich berechnet")
        return daily_total

    except KeyError:
        logger.error(
            "Erforderliche Spalten ('date', 'usage_minutes') fehlen im DataFrame",
            exc_info=True,
        )
        raise

    except Exception:
        logger.exception("Unerwarteter Fehler bei der Tagesauswertung")
        raise


def get_top_5_apps_per_day(df: pd.DataFrame) -> dict[str, pd.Series]:
    """Gibt für jeden Tag die Top 5 meistgenutzten Apps zurück.

    :param df: Pandas DataFrame mit ScreenTime-Daten
        (Spalten: 'date', 'app', 'usage_minutes')
    :return: Dictionary mit Datum als Key und einer Pandas Series (Top-5-Apps pro Tag) als Value"""

    logger.info("Starte Berechnung der Top-5-Apps pro Tag")

    if df.empty:
        logger.warning("Leeres DataFrame übergeben - keine Top-5-Berechnung möglich")
        raise ValueError("Keine Daten zur Analyse vorhanden")

    try:
        result = {}

        for date, group in df.groupby("date"):  # Daten werden nach Tagen getrennt
            top5 = (
                group.groupby("app")["usage_minutes"]
                .sum()  # Nutzungszeit pro App pro Tag
                .sort_values(ascending=False)
                .  # Sortierung absteigend
                head(5)  # Top 5 Apps
            )

            result[date] = top5
            logger.debug(f"Top-5-Apps für {date} berechnet")

        logger.info("Top-5-Berechnung erfolgreich abgeschlossen")
        return result

    except KeyError:
        logger.error("Erwartete Spalte fehlt im DataFrame", exc_info=True)
        raise

    except Exception:
        logger.exception("Unerwarteter Fehler bei der Top-5-Berechnung")
        raise


def get_top_5_total_time(top5_dict: dict[str, pd.Series]) -> dict[str, int]:
    """Berechnet für jeden Tag die Summe der Nutzungszeit der jeweiligen Top 5 Apps.

    :param top5_dict: Dictionary mit Datum als Key und Pandas Series (Top-5-Apps) als Value
    :return: Dictionary mit Datum und Gesamtzeit der Top-5-Apps"""

    logger.info("Berechne Gesamtzeit der Top-5-Apps")

    if not top5_dict:
        logger.warning("Leeres Top-5-Dictionary - keine Summen berechenbar")
        return {}

    totals = {}

    try:
        for date, series in top5_dict.items():
            totals[date] = int(series.sum())
            logger.debug(f"Gesamtzeit für {date} berechnen")

        logger.info("Gesamtzeiten erfolgreich berechnet")
        return totals

    except Exception:
        logger.exception("Fehler bei der Berechnung der Gesamtzeiten")
        raise
