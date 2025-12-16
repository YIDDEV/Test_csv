import pandas as pd  # type: ignore
from functools import reduce


def merge_daily_dfs(dfs):
    """
    Fusionne une liste de DataFrames journaliers
    sur les clés (participant_id, date).

    - jointure externe (outer)
    - conserve toutes les dates disponibles
    """

    if not dfs:
        raise ValueError("La liste de DataFrames est vide")

    merged_df = reduce(
        lambda left, right: pd.merge(
            left,
            right,
            on=["participant_id", "date"],
            how="outer",
        ),
        dfs,
    )

    # Ordonner proprement
    merged_df = merged_df.sort_values(
        ["participant_id", "date"]
    ).reset_index(drop=True)

    return merged_df
