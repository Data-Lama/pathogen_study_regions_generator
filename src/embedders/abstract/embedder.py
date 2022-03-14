# Abstract class for implementing an embedder
from abc import ABC, abstractmethod
import abc


class AbstractEmbbeder(ABC):

    @abc.abstractproperty
    def ID(self):
        '''
        Unique identifier for the embedder
        '''
        pass

    @abc.abstractproperty
    def name(self):
        '''
        Human readable name for the embedder
        '''
        pass

    @abstractmethod
    def embeddData(self, df_vector=None, df_matrix=None, **kwargs):
        '''
        Method that embbeds the given geographical timeseries into a vector metric space.

        Parameters
        ----------
        df_vector : pandas.DataFrame
            DataFrame with the geographical timeseries as vector. Must have the following columns:
                - ID : identifier of the corresponding polygon.
                - date : date for the values (corresponds to the last day of the periodicity)
                .... rest of columns of the (can be as many as desired)

        df_matrix : pandas.DataFrame
            DataFrame with the geographical timeseries as matrix. Must have the following columns:
                - ID_1 : identifier of the first polygon.
                - ID_2 : identifier of the second polygon.
                - date : date for the values (corresponds to the last day of the periodicity)
                .... rest of columns of data (can be as many as desired)


        Return
        ------
        vector : pandas.DataFrame
            Returns a pandas Dataframe with a single row per geographical region. Must include the columns:
                - ID : identifier of the corresponding polygon.
                .... rest of columns of embedding (can be as many as desired)
        matrix : pandas.DataFrame
            Returns a pandas Dataframe with a single row per geographical region. Must include the columns:
                - ID_1 : identifier of the first polygon.
                - ID_2 : identifier of the second polygon.
                .... rest of columns of embedding (can be as many as desired)

        '''
        pass
