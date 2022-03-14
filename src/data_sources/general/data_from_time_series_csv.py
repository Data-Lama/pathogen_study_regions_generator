# Data source from a time series of shapefiles
from abc import ABC, abstractmethod
from constants import PIPELINE_DATA_FOLDER, RAW, SUPPLEMENTARY, IDENT, DATE, AVERAGE, ID, MAX, MIN, TOTAL, isTimeResolutionValid, DAY, WEEK, MONTH, YEAR

import os
import numpy as np
import pandas as pd
import geopandas as gpd

from data_sources.abstract.vector_data_source import VectorDataSource
from utils.date_functions import compare_time_resolutions, get_dates_between_years_by_resolution, get_period_representative_function, take_to_period_representative
from utils.geographic_functions import overlay_over_geo_malaria_tmp
from utils.logger import Logger
from utils.preprocessing_functions import one_hot_encoding



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
                 min_year,
                 max_year,
                 suplementary_gdf,
                 index_id=ID,
                 min_time_resolution=DAY,
                 included_groupings=[TOTAL, AVERAGE, MAX, MIN],
                 columns_of_interest=[],
                 default_values=np.nan
                 ):
        '''
        Assings the included groupings for the overlay stage
        '''
        super().__init__()
        self.__id = id
        self.__name = name
        self.folder_name = folder_name
        self.file_name = file_name
        self.min_year = min_year
        self.max_year = max_year
        self.index_id = index_id
        self.included_groupings = included_groupings
        self.min_time_resolution = min_time_resolution
        self.encoding_dict = {}
        self.columns_of_interest = columns_of_interest
        self.suplementary_gdf = suplementary_gdf
        self.default_values = default_values

    @property
    def ID(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    def set_encoding_dict(self, encoding_dict):
        self.encoding_dict = encoding_dict

    # Override Methods
    # -----------------

    def loadTimeSeriesCSV(self):
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
        supplementary_file_location = os.path.join(folder_location,
                                                   SUPPLEMENTARY,
                                                   self.suplementary_gdf)

                                               
        try:
            supl_gdf = gpd.read_file(supplementary_file_location)
        except FileNotFoundError as e:
            Logger.print_error(
                "Supplementary geographic file for loading csv not found.")
            raise e

        if len(supl_gdf.columns) > 2:
            raise (
                "Supplementary geographic file must have only two columns. A 'geometry' column and any other desired\
                identifier column.")

        # Extract identifier column name from geoPandas
        supl_idx = [i for i in list(supl_gdf.columns) if i != 'geometry'][0]
        supl_gdf.rename(columns={supl_idx: self.index_id}, inplace=True)

        # Loads csv
        folder_location = os.path.join(PIPELINE_DATA_FOLDER, RAW,
                                       self.folder_name)
        file_location = os.path.join(folder_location, self.file_name)

        df = pd.read_csv(file_location, parse_dates=["date"])

        # Take to min allowed resolution
        df["min_time_resolution"] = df.apply(lambda x: take_to_period_representative(x["date"], self.min_time_resolution), axis=1)
        df.drop(columns=["date"], inplace=True)
        df.rename(columns={"min_time_resolution": "date"}, inplace=True)
        self.data_time_resolution = self.min_time_resolution

        # Drop unecessary columns 
        columns_to_exclude = list(set(df.columns) - set(self.columns_of_interest))
        columns_to_exclude.remove(self.index_id)
        columns_to_exclude.remove("date")
        df.drop(columns=columns_to_exclude, inplace=True)

        # Drop nans on merging columns
        df.dropna(subset=[self.index_id], inplace=True)
        supl_gdf.dropna(subset=[self.index_id], inplace=True)

        # Perform one-hot-encoding
        df, encoding_dict = one_hot_encoding(df, [self.index_id])
        self.set_encoding_dict(encoding_dict)
    
        # merge df with geometry
        df[self.index_id] = df[self.index_id].astype('int')
        supl_gdf[self.index_id] = supl_gdf[self.index_id].astype('int')

        # group by minimun resolution to speed things up
        df = df.groupby(["date", self.index_id]).sum().reset_index()

        # merge
        gdf = supl_gdf.merge(df, on=self.index_id)
  
        # Drop index_id
        gdf.drop(columns=[self.index_id], inplace=True)

        return gdf

    def createData(self, df_geo, time_resolution, **kwargs):

        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        # Reads the time series
        Logger.print_progress(f"Loads Data")
        gdf_values = self.loadTimeSeriesCSV()

        Logger.print_progress(f"Builds Overlay")
        # Overlays over the given geography
        df = overlay_over_geo_malaria_tmp(
            gdf_values,
            df_geo,
            grouping_columns=[ID, DATE],
            included_groupings=self.included_groupings,
            default_values=self.default_values
        )

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
