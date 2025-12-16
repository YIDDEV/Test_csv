import json
import pandas as pd #type: ignore

def load_daily_calories(participant_id, data_raw_path):
    path = data_raw_path / participant_id / "fitbit" / "calories.json"

    with open(path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["dateTime"]).dt.date
    df["calories"] = df["value"].astype(float)

    daily_df = (
        df.groupby("date")["calories"]
        .sum()
        .reset_index()
        .rename(columns={"calories": "calories_burned_day"})
    )

    daily_df.insert(0, "participant_id", participant_id)
    return daily_df
