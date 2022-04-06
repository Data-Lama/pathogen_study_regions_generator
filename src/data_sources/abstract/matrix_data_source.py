# Abstract class for implementing a single matrix data source
import abc
from abc import ABC, abstractmethod
import pandas as pd

from data_sources.abstract.data_source import DataSource


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
    def createData(self, df_geo, time_resolution):
        '''
        Method that creates the corresponding matrix data. Final data should have the geographical resolution in
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
        pandas.DataFrame (vector data)
            Returns a pandas Dataframe with the timeseries of the geographical regions. Must include the columns:
                - ID_1 : identifier of the corresponding first polygon.
                - ID_2 : identifier of the corresponding second polygon.
                - date : date for the values (corresponds to the last day of the periodicity)
                .... rest of columns of the data source (can be as many as desired)

        '''
        pass

    @abstractmethod
    def createDataFromCachedSubGeography(self, time_resolution, sub_geography,
                                         df_map):
        '''
        Method that creates the corresponding matrix data, based on a sub_geography. 
        This method is intended to save excecution time by using cached files.
        Final data should have the geographical resolution in the df_geo paramter and the periodicity of expressed in time_resolution.

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
