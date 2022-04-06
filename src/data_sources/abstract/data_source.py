# Abstract class for implementing a single data source
import abc
from abc import ABC, abstractmethod
from os.path import exists, join
import pandas as pd

from constants import CACHED, DATE, PIPELINE_DATA_FOLDER
from utils.cache_functions import build_cache_name


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

    def get_data(self, geography, time_resolution):
        '''
        Method that gets the corresponding data. 
        This method first checks for cached data will return it if found.         
        Then will check if the geography has a sub_geography and if it does, it will load that datasource
        and then agglomerate it to the current geography. On all other cases, it will call createData
        and return its output

        Parameters
        ----------
        geography : Geography
            Geography object with the desired geometry
        time_resolution : string
            Available time resolutions. Check the constants module for available options.

        Return
        ------
        return from createData method

        '''

        cached_file = join(
            PIPELINE_DATA_FOLDER, CACHED,
            build_cache_name(data_source=self,
                             geography=geography,
                             time_resolution=time_resolution))

        if exists(cached_file):
            return pd.read_csv(cached_file, parse_dates=[DATE])

        if geography.sub_geography is not None:

            df = self.createDataFromCachedSubGeography(
                time_resolution=time_resolution,
                sub_geography=geography.sub_geography,
                df_map=geography.df_map)
        else:
            df = self.createData(df_geo=geography.get_geometry(),
                                 time_resolution=time_resolution)

        # Saves
        df.to_csv(cached_file, index=False)
        return (df)
