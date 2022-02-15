# Abstract class for implementing an embedder
from abc import ABC, abstractmethod


class Embbeder(ABC):

    @abstractmethod
    def embedd(self, df):
        '''
        Method that embbeds the given geographical timeseries into a metric space.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame with the geographical timeseries. Must have the following columns:
                - ID : identifier of the corresponding polygon.
                - date : date for the values (corresponds to the last day of the periodicity)
                .... rest of columns of the data


        Return
        ------
        pandas.DataFrame
            Returns a pandas Dataframe with a single row per geographical region. Must include the columns:
                - ID : identifier of the corresponding polygon.
                .... rest of columns of embedding (can be as many as desired)

        '''
        pass