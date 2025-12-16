import pandas as pd #type: ignore
from pathlib import Path

from .utils import empty_daily_df


def load_daily_reporting(participant_id, data_raw_path):
    """
    Charge et agrège les données de reporting (nutrition / hydratation).
    """

    path = data_raw_path / participant_id / "googledocs" / "reporting.csv"

    # Fichier manquant
    if not path.exists():
        return empty_daily_df(
            participant_id,
            [
                "weight",
                "glasses_of_fluid",
                "alcohol_consumed",
                "n_meals",
                "n_reports",
            ],
        )

    df = pd.read_csv(path)

    # Dates
    df["date"] = pd.to_datetime(df["date"], dayfirst=True).dt.date
    df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=True)

    df["alcohol_consumed"] = df["alcohol_consumed"].map(
        {"Yes": 1, "No": 0}
    )

    df["n_meals"] = df["meals"].fillna("").apply(
        lambda x: len([m for m in x.split(",") if m.strip() != ""])
    )

    daily_df = (
        df.groupby("date")
        .agg(
            weight=("weight", "mean"),
            glasses_of_fluid=("glasses_of_fluid", "mean"),
            alcohol_consumed=("alcohol_consumed", "max"),
            n_meals=("n_meals", "max"),
                    )
        .reset_index()
    )

    daily_df.insert(0, "participant_id", participant_id)
    return daily_df
