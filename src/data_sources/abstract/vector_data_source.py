# Abstract class for implementing a single vector data source
import abc
from abc import ABC, abstractmethod
from os.path import exists, join
import pandas as pd

from constants import CACHED, DATE, PIPELINE_DATA_FOLDER
from utils.cache_functions import build_cache_name


class VectorDataSource(ABC):

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
        pandas.DataFrame (vector data)
            Returns a pandas Dataframe with the timeseries of the geographical regions. Must include the columns:
                - ID : identifier of the corresponding polygon.
                - date : date for the values (corresponds to the last day of the periodicity)
                .... rest of columns of the data source (can be as many as desired)

        '''
        pass

    def get_data(self, geography, time_resolution):
        '''
        Method that gets the corresponding data. This method calls the method createData if no data is found.
        in cache       

        Parameters
        ----------
        geography : Geography
            Geography object with the desired geometry
        time_resolution : string
            Available time resolutions. Check the constants module for available options.

        Return
        ------
        pandas.DataFrame (vector data)
            Returns a pandas Dataframe with the timeseries of the geographical regions. Must include the columns:
                - ID : identifier of the corresponding polygon.
                - date : date for the values (corresponds to the last day of the periodicity)
                .... rest of columns of the data source (can be as many as desired)

        '''

        cached_file = join(
            PIPELINE_DATA_FOLDER, CACHED,
            build_cache_name(data_source_id=self.ID,
                             geography_id=geography.ID,
                             time_resolution=time_resolution))
        if exists(cached_file):
            return pd.read_csv(cached_file, parse_dates=[DATE])

        df = self.createData(df_geo=geography.get_geometry(),
                             time_resolution=time_resolution)
        df.to_csv(cached_file, index=False)

        return (df)
