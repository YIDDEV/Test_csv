import json
import pandas as pd #type: ignore

def load_daily_steps(participant_id, data_raw_path):
    path = data_raw_path / participant_id / "fitbit" / "steps.json"

    with open(path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["dateTime"]).dt.date
    df["steps"] = df["value"].astype(int)

    daily_df = (
        df.groupby("date")["steps"]
        .sum()
        .reset_index()
        .rename(columns={"steps": "steps_day"})
    )

    daily_df.insert(0, "participant_id", participant_id)
    return daily_df
