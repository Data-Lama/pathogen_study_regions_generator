# Abstract class for implementing an embedder
from abc import ABC, abstractmethod


class Clusterer(ABC):

    @abstractmethod
    def cluster(self, df_vector=None, df_matrix=None):
        '''
        Method that clusters the embedded metric space parameters.

        Parameters
        ----------
        df_vector : pandas.DataFrame
            DataFrame with a single row per geographical region (vector). Must include the columns:
                - ID : identifier of the corresponding polygon.
                .... rest of columns of embedding (can be as many as desired)
        df_matrix : pandas.DataFrame
            DataFrame with a single row per pair of geographical region (matrix). Must include the columns:
                - ID_1 : identifier of the first polygon.
                - ID_2 : identifier of the second polygon.
                .... rest of columns of embedding (can be as many as desired)

        Return
        ------
        pandas.DataFrame
            Returns a pandas Dataframe with a single row per geographical region. Must include the columns:
                - ID : identifier of the corresponding polygon.
                - cluster_id : cluster identifier to which each geographical region belongs to.

        '''

    pass