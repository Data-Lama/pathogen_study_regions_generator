# Data source from a time series of shapefiles
from abc import ABC, abstractmethod
from constants import PIPELINE_DATA_FOLDER, RAW, SUPPLEMENTARY, DATA_SOURCE_IDENT, DATE, AVERAGE, ID, MAX, MIN, TOTAL, isTimeResolutionValid

import os
import pandas as pd
import geopandas as gpd

from data_sources.abstract.vector_data_source import VectorDataSource       
from utils.date_functions import compare_time_resolutions, get_dates_between_years_by_resolution, get_period_representative_function
from utils.geographic_functions import overlay_over_geo
from utils.preprocessing_functions import one_hot_encoding

IDENT = DATA_SOURCE_IDENT

class DataFromTimeSeriesOfCSV(VectorDataSource, ABC):
    '''
    Main class for extraction from a time series of csv. Given that the csv doesn't imply geography,
    a suplementary filename with geographic info should be provided to be used when building the datasource. 
    This abstract class is ment to handle data sources where a time series of csv 
    can be constructed from any source. This class expects the methods loadTimeSeriesCSV to be
    implemented, to later overlay it over the received geography and take it to the time resolution.
    '''

    def __init__(self,
                 id,
                 name,
                 folder_name, 
                 file_name,
                 suplementary_gdf,
                 data_time_resolution,
                 included_groupings=[TOTAL, AVERAGE, MAX, MIN]):
        '''
        Assings the included groupiings for the overlay stage
        '''
        super().__init__()
        self.__id = id
        self.__name = name
        self.folder_name = folder_name
        self.file_name = file_name
        self.data_time_resolution = data_time_resolution
        self.included_groupings = included_groupings
        self.suplementary_geo = suplementary_gdf
        self.encoding_dict = {}

    @property
    def ID(self):
        return self.__id

    @property
    def name(self):
        return self.__name
    
    def set_encoding_dict(self, encoding_dict):
        self.encoding_dict = encoding_dict
    

    def loadTimeSeriesCSV(self, index_name):
        '''
        Method that builds data source geography by merging with a supplementary geoPandas.
        This method assumes that the indicated file has only two columns, an index column
        (name is not important) and a geometry column.

        Parameters
        ----------
        index_name: column name on which to apply merge

        Returns
        -------
        Geopandas.DataFrame
                Geopandas Dataframe with the columns:
                    - geometry : geometry
                    ... columns with the values of the data

        '''
        # Loads supplementary file
        folder_location = os.path.join(PIPELINE_DATA_FOLDER, RAW)

        supplementary_file_location = os.path.join(folder_location, SUPPLEMENTARY, self.suplementary_gdf)
        try:
            supl_gdf = gpd.read_file(supplementary_file_location)
        except FileNotFoundError as e:
            print("Supplementary geographic file for loading csv not found.")
            raise e

        if len(supl_gdf.columns) > 2:
            raise("Supplementary geographic file must have only two columns. A 'geometry' column and any other desired\
                identifier column.")

        # Extract identifier column name from geoPandas     
        supl_index = list(supl_gdf.columns).remove('geometry')[0]

        # Loads csv
        folder_location = os.path.join(PIPELINE_DATA_FOLDER, RAW, self.folder_name)
        file_location = os.path.join(folder_location, self.file_name)

        df = pd.read_csv(file_location)

        # Perform one-hot-encoding
        df, encoding_dict = one_hot_encoding(df, columns_to_exclude=[index_name])
        self.set_encoding_dict(encoding_dict)

        # merge df with geometry
        gdf = supl_gdf.merge(df, left_on=supl_index, right_on=index_name)

        return gdf

    # Override Methods
    # -----------------
    def createData(self, df_geo, time_resolution):

        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        # Reads the time series 
        print(f"{IDENT}Loads Data")
        gdf_values = self.loadTimeSeriesShapefile()

        print(f"{IDENT}Builds Overlay")
        # Overlays over the given geography
        df = overlay_over_geo(
            gdf_values,
            df_geo,
            grouping_columns=[ID, DATE],
            included_groupings=self.included_groupings,
        )

        print(f"{IDENT}Changes Time Resolution")
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

