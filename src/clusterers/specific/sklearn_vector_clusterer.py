# Sklearn clusterer
import pandas as pd
from clusterers.abstract.clusterer import AbstractClusterer
import constants as con


class SklearnVectorClusterer(AbstractClusterer):
    '''
    Clusterer that recevices an initiated sklearn cluster object to use 
    for clustering 
    '''

    def __init__(self, ID, name, sklearn_clusterer):
        super().__init__()

        # Abstarct Properties
        self.__ID = ID
        self.__name = name

        # Clusterer
        self.sklearn_clusterer = sklearn_clusterer

    @property
    def ID(self):
        return (self.__ID)

    @property
    def name(self):
        return (self.__name)

    def clusterData(self, current_geography, df_vector=None, df_matrix=None):

        if df_vector[con.ID].value_counts().iloc[0] > 1:
            raise Exception(
                "The df_vector data cannot have duplicate values for any of the ids"
            )

        # Ignores the matrix data
        X = df_vector[df_vector.columns.difference([con.ID])]

        self.sklearn_clusterer = self.sklearn_clusterer.fit(X)

        # Builds return object
        results = pd.DataFrame({
            con.ID: df_vector[con.ID],
            con.CLUSTER_ID: self.sklearn_clusterer.labels_
        })

        return (results)
