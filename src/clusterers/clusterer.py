# Abstract class for implementing an embedder
from abc import ABC, abstractmethod

class Clusterer(ABC):

    @abstractmethod
    def cluster(self, df):
        '''
        Method that clusters the embedded metric space parameters.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame with a single row per geographical region. Must include the columns:
                - ID : identifier of the corresponding polygon.
                .... rest of columns of embedding (can be as many as desired)


        Return
        ------
        pandas.DataFrame
            Returns a pandas Dataframe with a single row per geographical region. Must include the columns:
                - ID : identifier of the corresponding polygon.
                - cluster_id : cluster identifier to which each geographical region belongs to.

        '''

    pass