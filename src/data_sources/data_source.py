# Abstract class for implementing a single data source
import abc
from abc import ABC, abstractmethod


class DataSource(ABC):

    @abc.abstractproperty
    def ID(self):
        '''
        Unique identifier for the data source
        '''
        pass

    @abc.abstractproperty
    def name(self):
        '''
        Human readable name for the data source
        '''
        pass

    @abstractmethod
    def createData(self, df_geo, time_resolution):
        '''
        Method that creates the corresponding data. Final data should have the geographical resolution in
        the df_geo paramter and the periodicity of expressed in time_resolution.

        Parameters
        ----------
        df_geo : Geopandas.DataFrame
            DataFrame with the desired geographical resolution. The df must include columns:
                - geometry
                - ID : column with the unique ID
        time_resolution : string
            Available time resolutions. Check the constants module for available options.

        Return
        ------
        pandas.DataFrame
            Returns a pandas Dataframe with the timeseries of the geographical regions. Must include the columns:
                - ID : identifier of the corresponding polygon.
                - date : date for the values (corresponds to the last day of the periodicity)
                .... rest of columns of the data source (can be as many as desired)

        '''
        pass
