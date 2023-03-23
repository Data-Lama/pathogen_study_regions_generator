# Abstract class for implementing a single matrix data source
import abc
from abc import ABC, abstractmethod
import pandas as pd

from data_sources.abstract.data_source import DataSource

from geography.abstract.abstact_geography import Geography


class MatrixDataSource(DataSource, ABC):

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
    def createData(self, geography : Geography, time_resolution : str) -> pd.DataFrame:
        '''
        Method that creates the corresponding matrix data. Final data should have the geographical resolution in
        the geography parameter and the periodicity of expressed in time_resolution.

        Parameters
        ----------
        geography : Geography
            The geography that will be used to create the data
        time_resolution : string
            Available time resolutions. Check the constants module for available options.

        Return
        ------
        pandas.DataFrame (vector data)
            Returns a pandas Dataframe with the timeseries of the geographical regions. Must include the columns:
                - ID_1 : identifier of the corresponding first polygon.
                - ID_2 : identifier of the corresponding second polygon.
                - date : date for the values (corresponds to the last day of the periodicity)
                .... rest of columns of the data source (can be as many as desired)

        '''
        pass

    @abstractmethod
    def createDataFromCachedSubGeography(self, time_resolution : str, sub_geography : Geography,
                                         df_map : pd.DataFrame) -> pd.DataFrame:
        '''
        Method that creates the corresponding matrix data, based on a sub_geography. 
        This method is intended to save execution time by using cached files.
        Final data should have the geographical resolution in the geography paramter and the periodicity of expressed in time_resolution.

        Parameters
        ----------
        time_resolution : string
            Available time resolutions. Check the constants module for available options.
        sub_geography : Geography
            Sub geography. The current df_geo should be an aggloeration of this geography's geometry
        df_map : pandas.DataFrame
            Data frame with the ID map. Should have the following columns
                - SUB_ID: ID in the sub_geograpy
                - ID: current ID

        Return
        ------
        pandas.DataFrame (vector data)
            Returns a pandas Dataframe with the timeseries of the geographical regions. Must include the columns:
                - ID_1 : identifier of the corresponding first polygon.
                - ID_2 : identifier of the corresponding second polygon.
                - date : date for the values (corresponds to the last day of the periodicity)
                .... rest of columns of the data source (can be as many as desired)

        '''
        pass
