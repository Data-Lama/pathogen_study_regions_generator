# Identity cluster (For testing)
import pandas as pd
import numpy as np
from clusterers.abstract.clusterer import AbstractClusterer
import constants as con


class IdentityClusterer(AbstractClusterer):

    ID = "identity_clusterer"
    name = "Identity Clusterer"

    def clusterData(self, df_vector=None, df_matrix=None):

        # If both vector and matrix are providedm it gives priority to
        # to the vector

        if df_vector is not None:
            ids = df_vector[con.ID].unique()
            return (pd.DataFrame({
                con.ID: ids,
                con.CLUSTER_ID: range(len(ids))
            }))

        if df_matrix is not None:
            ids = np.unique(
                np.concatenate(df_vector[con.ID_1].unique(),
                               df_vector[con.ID_2].unique()))
            return (pd.DataFrame({
                con.ID: ids,
                con.CLUSTER_ID: range(len(ids))
            }))

        # Both vector and matrix are None
        raise ValueError(
            "Error in cluster. Both df_vector and df_matrix cannot be None")
