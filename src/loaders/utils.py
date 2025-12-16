from pathlib import Path
import pandas as pd # type: ignore

def empty_daily_df(participant_id: str, columns: list[str]) -> pd.DataFrame:
    """
    Retourne un DataFrame journalier vide avec participant_id et date.
    """
    df = pd.DataFrame(columns=["participant_id", "date"] + columns)
    df["participant_id"] = df["participant_id"].astype("object")
    return df
