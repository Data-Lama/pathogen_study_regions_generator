# Distance functions
import numpy as np
import pandas as pd

from constants import ID_2, ID_1, DATE


def hausdorff(df):
    # Build matrix 
    df["pivot_index_1"] = df.apply(lambda x: x.name, axis=1)
    df["pivot_index_2"] = df.apply(lambda x: x.name, axis=1)
    
    distance_matrix = df.pivot(index="pivot_index_1", columns="pivot_index_2", values='ibd')

    # Get pairs to filter
    ids = np.array(list(set(df[ID_1].unique()).union(set(df[ID_2].unique()))))
    pairs = np.array(np.meshgrid(ids, ids)).T.reshape(-1,2)

    # filter by muni
    data = []
    for pair in pairs:
        index_values_rows = df[df[ID_1] == pair[0]].index.values
        index_values_cols = df[df[ID_2] == pair[1]].index.values

        if (index_values_rows.size == 0) or (index_values_cols.size == 0):
            continue

        # filter columns
        distance_matrix_tmp = distance_matrix[index_values_cols]
    
        # filter rows
        distance_matrix_tmp = distance_matrix_tmp.loc[index_values_rows]

        if distance_matrix_tmp.empty:
            continue
        
        min_rows = distance_matrix_tmp.min(axis=1).dropna()
        min_cols = distance_matrix_tmp.min(axis=0).dropna()

        hausdorff = (min_rows.mean() + min_cols.min()) / 2

        data.append({ID_1: pair[0], ID_2: pair[1], "hausdorff": hausdorff})
    
    
    return pd.DataFrame(data)