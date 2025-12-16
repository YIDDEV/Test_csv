import pandas as pd  # type: ignore


def load_daily_sleep(participant_id, data_raw_path):
    """
    Charge les scores de sommeil journaliers.
    """

    path = data_raw_path / participant_id / "fitbit" / "sleep_score.csv"

    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(df["timestamp"]).dt.date

    daily_df = df[
        [
            "date",
            "overall_score",
            "composition_score",
            "revitalization_score",
            "duration_score",
            "deep_sleep_in_minutes",
            "resting_heart_rate",
            "restlessness",
        ]
    ].copy()

    # Renommage explicite
    daily_df = daily_df.rename(
        columns={
            "overall_score": "sleep_overall_score",
            "composition_score": "sleep_composition_score",
            "revitalization_score": "sleep_revitalization_score",
            "duration_score": "sleep_duration_score",
            "deep_sleep_in_minutes": "deep_sleep_min",
            "resting_heart_rate": "sleep_resting_hr",
            "restlessness": "sleep_restlessness",
        }
    )

    daily_df.insert(0, "participant_id", participant_id)
    return daily_df
