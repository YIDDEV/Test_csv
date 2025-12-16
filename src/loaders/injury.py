import pandas as pd #type: ignore
import ast

from .utils import empty_daily_df


def load_daily_injury(participant_id, data_raw_path):
    """
    Charge et agrège les données de blessures.
    """

    path = data_raw_path / participant_id / "pmsys" / "injury.csv"

    if not path.exists():
        return empty_daily_df(
            participant_id,
            ["injured", "injury_minor", "injury_major", "n_injuries"],
        )

    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(
        df["effective_time_frame"]
    ).dt.date

    df["injuries_dict"] = df["injuries"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else {}
    )

    df["n_injuries"] = df["injuries_dict"].apply(len)
    df["injured"] = (df["n_injuries"] > 0).astype(int)

    df["injury_minor"] = df["injuries_dict"].apply(
        lambda d: int(any(v == "minor" for v in d.values()))
    )

    df["injury_major"] = df["injuries_dict"].apply(
        lambda d: int(any(v == "major" for v in d.values()))
    )

    daily_df = (
        df.groupby("date")
        .agg(
            injured=("injured", "max"),
            injury_minor=("injury_minor", "max"),
            injury_major=("injury_major", "max"),
            n_injuries=("n_injuries", "sum"),
        )
        .reset_index()
    )

    daily_df.insert(0, "participant_id", participant_id)
    return daily_df
