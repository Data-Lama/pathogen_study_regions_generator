# Data source from a geopandas (abstract)
from abc import ABC, abstractmethod
from utils.logger import Logger
from constants import AREA_COL, GEOMETRY, DATE, AVERAGE, ID, LINEAR, MANIPULATION_PROJECTION, MAX, MEAN, MIN, SUB_ID, TOTAL, YEAR, isTimeResolutionValid
import pandas as pd
import numpy as np
import geopandas

from data_sources.abstract.vector_data_source import VectorDataSource
from utils.date_functions import compare_time_resolutions, increase_time_resolution, lower_time_resolution
from utils.geographic_functions import agglomerate_data_frame, get_enclosing_geoemtry, overlay_over_geo


class DataFromGeoPandas(VectorDataSource, ABC):
    '''
    Main class for extraction from any file representation that endsup being a geopandas
    implemented, to later overlay it over the received geography and take it to the time resolution.
    '''

    def __init__(self,
                 id,
                 name,
                 data_time_resolution,
                 included_groupings=[TOTAL, AVERAGE, MAX, MIN],
                 time_resolution_aggregation_function=MEAN,
                 time_resolution_extrapolation_function= LINEAR,
                 default_values=None,
                 fill_missing_space=False):
        '''
        Parameters
        ----------
        id : string
            ID of the data source
        name : string
            Name of the data source
        data_time_resolution : string
            Resolution in which the data source is in.
        included_groupings : array
            Grouping functions to be applied. See: utils.geographic_functions.overlay_over_geo for more info
        time_resolution_aggregation_function : str
            How to lower the time resolution of the data source. See utils.date_functions.lower_time_resolution for more info.
        time_resolution_extrapolation_function : str
            How to increase the time resolution of the data source. See utils.date_functions.increase_time_resolution for more info.
        default_values : value or dict
            Value or dict indicating the default values for geometries where no value could be extracted. See: utils.geographic_functions.overlay_over_geo for more info
        complete_source : boolean
            Determines if the given geopandas fills the entire space (no geographical holes). In case it has holes, they will be filled with 
            polygons with the default value.
        fill_missing_space : boolean
            If the missing geographical space should be filled with default values or not
        '''
        super().__init__()
        self.__id = id
        self.__name = name
        self.data_time_resolution = data_time_resolution
        self.included_groupings = included_groupings
        self.default_values = default_values
        self.time_resolution_aggregation_function = time_resolution_aggregation_function
        self.time_resolution_extrapolation_function = time_resolution_extrapolation_function
        self.fill_missing_space = fill_missing_space


    @property
    def ID(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def loadGeopandasDataFrame(self):
        '''
        Method that loads the dataframe

        Returns
        -------
        Geopandas.DataFrame
            Geopandas Dataframe with the columns:
                - date : date for the given values. Should be in the format of the periods
                - geometry : geomtry
                ... columns with the values of the data
        '''
        pass

    # Override Methods
    # -----------------
    def createData(self, df_geo, time_resolution, **kwargs):

        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        # Loads inclosing geometry
        if self.fill_missing_space:
            enclosing_geo = get_enclosing_geoemtry(df_geo)

        # Reads the time series shapefile
        Logger.print_progress(f"Loads Data")
        Logger.enter_level()
        df_values = self.loadGeopandasDataFrame()
        Logger.exit_level()

        Logger.print_progress(f"Builds Overlay")

        # Iterates over every date
        all_dfs = []
        dates = np.unique(df_values[DATE])
        Logger.print_progress(
            f"By Dates. From {np.min(df_values[DATE].dt.year)} to {np.max(df_values[DATE].dt.year)}"
        )
        Logger.enter_level()
        for date in dates:
            Logger.print_progress(f"{date}")
            df_temp = df_values[df_values[DATE] == date]

            # If incomplete. Adds difference polygon
            if self.fill_missing_space:
                geo_diff = enclosing_geo[GEOMETRY].difference(
                    df_temp[[GEOMETRY]].dissolve())

                df_temp = pd.concat(
                    (df_temp,
                     geopandas.GeoDataFrame(pd.DataFrame({DATE: [date]}),
                                            geometry=geo_diff)),
                    ignore_index=True)

                df_temp = df_temp.fillna(self.default_values)

            # Overlays over the given geography
            df_ovelayed = overlay_over_geo(
                df_temp,
                df_geo,
                grouping_columns=[ID, DATE],
                included_groupings=self.included_groupings,
                default_values=self.default_values)

            all_dfs.append(df_ovelayed)

        df = pd.concat(all_dfs, ignore_index=True)
        Logger.exit_level()

        Logger.print_progress(f"Changes Time Resolution")
        # Takes the time series to the desired time resolution
        # --------------
        # Compares time resolutions
        comp = compare_time_resolutions(self.data_time_resolution,
                                        time_resolution)

        if comp > 0:
            # Target resolution is lower

            df = lower_time_resolution(df=df, 
                                       initial_time_resolution=self.data_time_resolution,
                                       target_time_resolution=time_resolution,
                                       aggregation_function=self.time_resolution_aggregation_function)

        elif comp < 0:
            # Target resolution is higher
            df = increase_time_resolution(df = df,
                                        initial_time_resolution = self.data_time_resolution,
                                        target_time_resolution = time_resolution,
                                        extrapolation_function = self.time_resolution_extrapolation_function)

        return df

    def createDataFromCachedSubGeography(self, time_resolution, sub_geography,
                                         df_map):

        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        # Gets the data from the sub_geography
        df = self.get_data(sub_geography, time_resolution)

        # Attaches Areas
        df_area = sub_geography.get_geometry()[[ID, GEOMETRY]].copy()
        df_area[AREA_COL] = df_area[GEOMETRY].to_crs(
            MANIPULATION_PROJECTION).area

        df = df.merge(df_area)
        #df.drop(GEOMETRY, index=1, inplace=True)

        # Maps the ids
        df.rename(columns={ID: SUB_ID}, inplace=True)
        df = df.merge(df_map)
        df.drop(SUB_ID, axis=1, inplace=True)

        # Agglomerates
        df_final = agglomerate_data_frame(df, [ID, DATE],
                                          included_groupings=[])

        return (df_final)
