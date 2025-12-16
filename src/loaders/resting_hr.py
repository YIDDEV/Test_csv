import json
import pandas as pd  # type: ignore


def load_daily_resting_hr(participant_id, data_raw_path):
    """
    Charge la fréquence cardiaque au repos journalière.
    """

    path = data_raw_path / participant_id / "fitbit" / "resting_heart_rate.json"

    with open(path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    df["dateTime"] = pd.to_datetime(df["dateTime"])
    df["date"] = df["dateTime"].dt.date


    df["resting_hr"] = df["value"].apply(lambda x: x.get("value"))

    daily_df = (
        df.groupby("date")["resting_hr"]
        .mean()
        .reset_index()
        .rename(columns={"resting_hr": "resting_hr_day"})
    )

    daily_df.insert(0, "participant_id", participant_id)
    return daily_df
