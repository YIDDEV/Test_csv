import json
import pandas as pd  # type: ignore


def load_daily_hr_zones(participant_id, data_raw_path):
    """
    Charge le temps passé dans les zones de fréquence cardiaque par jour.
    """

    path = data_raw_path / participant_id / "fitbit" / "time_in_heart_rate_zones.json"

    with open(path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(df["dateTime"]).dt.date

    # Extraction zones
    df["hr_below_zone"] = df["value"].apply(
        lambda x: x["valuesInZones"].get("BELOW_DEFAULT_ZONE_1", 0)
    )
    df["hr_fat_burn"] = df["value"].apply(
        lambda x: x["valuesInZones"].get("IN_DEFAULT_ZONE_1", 0)
    )
    df["hr_cardio"] = df["value"].apply(
        lambda x: x["valuesInZones"].get("IN_DEFAULT_ZONE_2", 0)
    )
    df["hr_peak"] = df["value"].apply(
        lambda x: x["valuesInZones"].get("IN_DEFAULT_ZONE_3", 0)
    )

    # Intensité élevée = cardio + peak
    df["hr_high_intensity"] = df["hr_cardio"] + df["hr_peak"]

    daily_df = df[
        [
            "date",
            "hr_below_zone",
            "hr_fat_burn",
            "hr_cardio",
            "hr_peak",
            "hr_high_intensity",
        ]
    ]

    daily_df.insert(0, "participant_id", participant_id)
    return daily_df
