import json
import pandas as pd #type: ignore

def extract_activity_minutes(levels, names):
    if not isinstance(levels, list):
        return 0
    return sum(l["minutes"] for l in levels if l["name"] in names)

def extract_hr_minutes(zones, zone_names):
    if not isinstance(zones, list):
        return 0
    return sum(z["minutes"] for z in zones if z["name"] in zone_names)

def load_daily_exercise(participant_id, data_raw_path):
    path = data_raw_path / participant_id / "fitbit" / "exercise.json"

    with open(path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    df["startTime"] = pd.to_datetime(df["startTime"])
    df["date"] = df["startTime"].dt.date
    df["duration_min"] = df["duration"] / 1000 / 60

    df["high_intensity_minutes"] = df["activityLevel"].apply(
        lambda x: extract_activity_minutes(x, ["fairly", "very"])
    )

    df["hrz_fat_burn_minutes"] = df["heartRateZones"].apply(
        lambda x: extract_hr_minutes(x, ["Fat Burn"])
    )
    df["hrz_cardio_minutes"] = df["heartRateZones"].apply(
        lambda x: extract_hr_minutes(x, ["Cardio"])
    )
    df["hrz_peak_minutes"] = df["heartRateZones"].apply(
        lambda x: extract_hr_minutes(x, ["Peak"])
    )

    df["distance"] = df["distance"].fillna(0)
    df["steps"] = df["steps"].fillna(0)

    daily_df = (
        df.groupby("date")
        .agg(
            exercise_duration_min_day=("duration_min", "sum"),
            exercise_calories_day=("calories", "sum"),
            exercise_steps_day=("steps", "sum"),
            exercise_distance_km_day=("distance", "sum"),
            exercise_avg_hr=("averageHeartRate", "mean"),
            high_intensity_minutes=("high_intensity_minutes", "sum"),
            hrz_fat_burn_minutes=("hrz_fat_burn_minutes", "sum"),
            hrz_cardio_minutes=("hrz_cardio_minutes", "sum"),
            hrz_peak_minutes=("hrz_peak_minutes", "sum"),
            n_exercise_sessions=("activityName", "count"),
        )
        .reset_index()
    )

    daily_df.insert(0, "participant_id", participant_id)
    return daily_df
