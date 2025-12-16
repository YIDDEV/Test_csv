import pandas as pd #type: ignore

from .utils import empty_daily_df


def load_daily_srpe(participant_id, data_raw_path):
    """
    Charge et agrège les données sRPE (charge interne subjective).
    """

    path = data_raw_path / participant_id / "pmsys" / "srpe.csv"

    if not path.exists():
        return empty_daily_df(
            participant_id,
            [
                "srpe_load",
                "srpe_duration",
                "srpe_mean_rpe",
                "n_srpe_sessions",
            ],
        )

    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(
        df["end_date_time"]
    ).dt.date

    df["srpe_load"] = (
        df["perceived_exertion"] * df["duration_min"]
    )

    daily_df = (
        df.groupby("date")
        .agg(
        srpe_load=("srpe_load", "sum"),
        srpe_duration=("duration_min", "sum"),
        srpe_mean_rpe=("perceived_exertion", "mean"),
        n_srpe_sessions=("activity_names", "count"),
    )
        .reset_index()
    )

    daily_df.insert(0, "participant_id", participant_id)
    return daily_df
