import pandas as pd #type: ignore

def load_daily_wellness(participant_id, data_raw_path):
    """
    Charge et agrège les données de bien-être (wellness) à l'échelle journalière.

    Chaque ligne correspond à un questionnaire subjectif.
    L’agrégation journalière se fait par moyenne.
    """

    path = data_raw_path / participant_id / "pmsys" / "wellness.csv"

    if not path.exists():
        return pd.DataFrame(
            columns=[
                "participant_id", "date",
                "fatigue", "mood", "readiness",
                "sleep_duration_h", "sleep_quality",
                "soreness", "stress",
            ]
        )

    df = pd.read_csv(path)

    # parsing date
    df["date"] = pd.to_datetime(df["effective_time_frame"]).dt.date

    daily_df = (
        df
        .groupby("date")
        .agg(
            fatigue=("fatigue", "mean"),
            mood=("mood", "mean"),
            readiness=("readiness", "mean"),
            sleep_duration_h=("sleep_duration_h", "mean"),
            sleep_quality=("sleep_quality", "mean"),
            soreness=("soreness", "mean"),
            stress=("stress", "mean"),
        )
        .reset_index()
    )

    daily_df.insert(0, "participant_id", participant_id)

    return daily_df
