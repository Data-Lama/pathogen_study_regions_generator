# Data source from a time series of shapefiles
from abc import ABC, abstractmethod
from utils.logger import Logger
from constants import IDENT, DATE, AVERAGE, ID, MAX, MIN, TOTAL, isTimeResolutionValid
import pandas as pd

from data_sources.abstract.vector_data_source import VectorDataSource
from utils.date_functions import compare_time_resolutions, get_dates_between_years_by_resolution, get_period_representative_function
from utils.geographic_functions import overlay_over_geo


class DataFromTimeSeriesOfShapefiles(VectorDataSource, ABC):
    '''
    Main class for extraction from a time series of shapefiles. 
    This abstract class is ment to handle data sources where a time series of shapefiles 
    can be constructed from any source. This class expects the methods loadTimeSeriesShapefile to be
    implemented, to later overlay it over the received geography and take it to the time resolution.
    '''

    def __init__(self,
                 id,
                 name,
                 data_time_resolution,
                 included_groupings=[TOTAL, AVERAGE, MAX, MIN],
                 default_values=None):
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
        default_values : value or dict
            Value or dict indicating the default values for geometries where no value could be extracted. See: utils.geographic_functions.overlay_over_geo for more info
        '''
        super().__init__()
        self.__id = id
        self.__name = name
        self.data_time_resolution = data_time_resolution
        self.included_groupings = included_groupings
        self.default_values = default_values

    @property
    def ID(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @abstractmethod
    def loadTimeSeriesShapefile(self):
        '''
        Method that loads the time series shapefile.

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

        # Reads the time series shapefile
        Logger.print_progress(f"Loads Data")
        Logger.enter_level()
        df_values = self.loadTimeSeriesShapefile()
        Logger.exit_level()

        Logger.print_progress(f"Builds Overlay")
        # Overlays over the given geography
        df = overlay_over_geo(df_values,
                              df_geo,
                              grouping_columns=[ID, DATE],
                              included_groupings=self.included_groupings,
                              default_values=self.default_values)

        Logger.print_progress(f"Changes Time Resolution")
        # Takes the time series to the desired time resolution
        # --------------
        # Compares time resolutions
        comp = compare_time_resolutions(self.data_time_resolution,
                                        time_resolution)

        if comp < 0:
            # Data resolution is lower

            # Takes the dates to their corresponding period
            df[DATE] = df[DATE].apply(
                get_period_representative_function(time_resolution), axis=1)

            df = df.groupby([ID, DATE]).mean().reset_index()

        elif comp > 0:
            # Data resolution is higher
            all_dates = get_dates_between_years_by_resolution(
                min_year=df[DATE].min().year,
                max_year=df[DATE].max().year,
                time_resolution=time_resolution)

            # Creates merging column
            df_all_dates = pd.DataFrame({"__final_date": all_dates})
            df_all_dates[DATE] = df_all_dates["__final_date"].apply(
                get_period_representative_function(time_resolution))

            # Merges
            df = df.merge(df_all_dates)
            df.drop(DATE, axis=1, inplace=True)
            df.rename(columns={"__final_date": DATE}, inplace=True)

        # Orders columns
        return (df[[ID, DATE] +
                   df.columns.difference([ID, DATE]).values.tolist()].copy())
