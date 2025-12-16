import json
import pandas as pd #type: ignore

def load_daily_distance(participant_id, data_raw_path):
    path = data_raw_path / participant_id / "fitbit" / "distance.json"

    with open(path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["dateTime"]).dt.date
    df["distance_km"] = df["value"].astype(float) / 100_000  # cm to km

    daily_df = (
        df.groupby("date")["distance_km"]
        .sum()
        .reset_index()
        .rename(columns={"distance_km": "distance_km_day"})
    )

    daily_df.insert(0, "participant_id", participant_id)
    return daily_df
