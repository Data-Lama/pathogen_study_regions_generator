# Quantile clusterer
import numpy as np
import pandas as pd
from clusterers.abstract.clusterer import AbstractClusterer
import constants as con


class QuantileClusterer(AbstractClusterer):
    '''
    Clusterer that clusters by quantile
    '''

    def __init__(self, ID, name, quantiles=[0.25, 0.5, 0.75]):
        super().__init__()

        # Abstarct Properties
        self.__ID = ID
        self.__name = name
        self.quantiles = quantiles

    @property
    def ID(self):
        return (self.__ID)

    @property
    def name(self):
        return (self.__name)


    def clusterData(self, df_vector=None, df_matrix=None):

        if df_vector[con.ID].value_counts().iloc[0] > 1:
            raise Exception(
                "The df_vector data cannot have duplicate values for any of the ids"
            )

        if len(df_vector.columns) > 2:
            raise Exception(
                "This implementation only suports clutering over one column. Combine columns first"
            )
        
        col = [x for x in df_vector.columns if x != con.ID][0]
            
        quantiles_values = np.quantile(df_vector[col], self.quantiles)

        df_response = pd.DataFrame(columns=[con.ID, con.CLUSTER_ID])
        for idx, q in enumerate(quantiles_values):
            
            df_tmp = pd.DataFrame({con.ID: df_vector[df_vector[col].lt(q)][con.ID].values})
            df_tmp[con.CLUSTER_ID] = idx

            df_response = pd.concat([df_response, df_tmp], ignore_index=True)

            # Keep only unclustered IDs
            df_vector = df_vector[df_vector[col].ge(q)].copy()
                
        # Concat last cluster
        df_tmp = pd.DataFrame({con.ID: df_vector[con.ID].values})
        df_tmp[con.CLUSTER_ID] = idx + 1

        df_response = pd.concat([df_response, df_tmp], ignore_index=True)
        
        return df_response

    