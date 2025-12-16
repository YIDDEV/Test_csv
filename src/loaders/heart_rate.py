import json
import pandas as pd  # type: ignore
from pathlib import Path
from .utils import empty_daily_df


def load_daily_heart_rate(participant_id, data_raw_path):
    """
    Charge la fréquence cardiaque minute par minute
    et calcule des statistiques journalières.
    """

    path = data_raw_path / participant_id / "fitbit" / "heart_rate.json"

    # FICHIER MANQUANT
    if not path.exists():
        return empty_daily_df(
            participant_id,
            ["hr_mean", "hr_max", "hr_std", "hr_p90", "hr_p10"],
        )

    with open(path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Extraction bpm
    df["dateTime"] = pd.to_datetime(df["dateTime"])
    df["date"] = df["dateTime"].dt.date
    df["heart_rate"] = df["value"].apply(lambda x: x["bpm"])

    daily_df = (
        df.groupby("date")
        .agg(
            hr_mean=("heart_rate", "mean"),
            hr_max=("heart_rate", "max"),
            hr_std=("heart_rate", "std"),
            hr_p90=("heart_rate", lambda x: x.quantile(0.90)),
            hr_p10=("heart_rate", lambda x: x.quantile(0.10)),
        )
        .reset_index()
    )

    daily_df.insert(0, "participant_id", participant_id)
    return daily_df

