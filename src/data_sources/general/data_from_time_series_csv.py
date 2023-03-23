# Data source from a time series of shapefiles
from abc import ABC, abstractmethod
from asyncio.log import logger
from constants import GEOMETRY, LINEAR, SUM, PIPELINE_DATA_FOLDER, RAW, DATE, AVERAGE, ID, MAX, MIN, TOTAL, isTimeResolutionValid, DAY, WEEK, MONTH, YEAR

import os
import numpy as np
import pandas as pd
import geopandas as gpd

from data_sources.abstract.vector_data_source import VectorDataSource
from data_sources.general.data_from_geopandas import DataFromGeoPandas
from utils.date_functions import take_to_resolution_representative
from utils.geographic_functions import overlay_over_geo
from utils.logger import Logger
from utils.preprocessing_functions import one_hot_encoding


class DataFromTimeSeriesOfCSV(DataFromGeoPandas):
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
                 reference_geography,
                 time_resolution_aggregation_function,
                 index_id=ID,
                 min_time_resolution=DAY,
                 included_groupings=[TOTAL, AVERAGE, MAX, MIN],
                 columns_of_interest=[],
                 default_values=np.nan,                 
                 time_resolution_extrapolation_function= LINEAR,
                 filter=None):
        '''
        Assings the included groupings for the overlay stage
        '''
        super().__init__(id=id,
                         name=name,
                         data_time_resolution=min_time_resolution,
                         included_groupings=included_groupings,
                         time_resolution_aggregation_function = time_resolution_aggregation_function,
                         time_resolution_extrapolation_function = time_resolution_extrapolation_function,
                         default_values=default_values,
                         reference_geography=reference_geography)

        self.folder_name = folder_name
        self.file_name = file_name
        self.min_year = min_year
        self.max_year = max_year
        self.index_id = index_id
        self.included_groupings = included_groupings
        self.min_time_resolution = min_time_resolution
        self.encoding_dict = {}
        self.columns_of_interest = columns_of_interest
        self.default_values = default_values
        self.filter = filter
        self.time_resolution_aggregation_function= time_resolution_aggregation_function
        self.time_resolution_extrapolation_function = time_resolution_extrapolation_function


    def set_encoding_dict(self, encoding_dict):
        self.encoding_dict = encoding_dict

    # Override Methods
    # -----------------

    def loadGeopandasDataFrame(self):
        '''
        Method that builds data source geography by merging with a supplementary geoPandas.
        This method assumes that the indicated file has only two columns, an index column
        (name is not important) and a geometry column.

        Returns
        -------
        Geopandas.DataFrame
                Geopandas Dataframe with the columns:
                    - geometry : geometry
                    - date : date
                    ... columns with the values of the data

        '''

        # Loads supplementary geography
        reference_gdf = self.reference_geography.get_geometry()
        reference_gdf = reference_gdf[[ID, GEOMETRY]].copy()
        reference_gdf.rename(columns={ID: self.index_id}, inplace=True)

        # Loads csv
        folder_location = os.path.join(PIPELINE_DATA_FOLDER, RAW,
                                       self.folder_name)
        file_location = os.path.join(folder_location, self.file_name)

        df = pd.read_csv(file_location, parse_dates=["date"])

        # Filters
        df = df[df[DATE].dt.year >= self.min_year]
        df = df[df[DATE].dt.year <= self.max_year].copy()

        # Apply filter function if necesary
        if self.filter:
            for key in self.filter.keys():
                values = self.filter[key]
                if not key in df.columns:
                    logger.error(f"Column {key} for filter, doesn't exist.")
                else:
                    df = df[df[key].isin(values)]
                    
        # Take to min allowed resolution
        df["min_time_resolution"] = df.apply(
            lambda x: take_to_resolution_representative(x["date"], self.
                                                    min_time_resolution),
            axis=1)
        df.drop(columns=["date"], inplace=True)
        df.rename(columns={"min_time_resolution": "date"}, inplace=True)
        self.data_time_resolution = self.min_time_resolution

        # Drop unnecessary columns
        columns_to_exclude = list(
            set(df.columns) - set(self.columns_of_interest))
        columns_to_exclude.remove(self.index_id)
        columns_to_exclude.remove("date")
        df.drop(columns=columns_to_exclude, inplace=True)

        # Drop nans on merging columns
        df.dropna(subset=[self.index_id], inplace=True)
        reference_gdf.dropna(subset=[self.index_id], inplace=True)

        # Perform one-hot-encoding
        df, encoding_dict = one_hot_encoding(df, [self.index_id])
        self.set_encoding_dict(encoding_dict)

        # merge df with geometry
        df[self.index_id] = df[self.index_id].astype('int')
        reference_gdf[self.index_id] = reference_gdf[
            self.index_id].astype('int')

        # group by minimun resolution to speed things up
        df = df.groupby(["date", self.index_id]).sum().reset_index()

        # merge
        gdf = reference_gdf.merge(df, on=self.index_id)

        # Returns Index to original name
        gdf.rename(columns={self.index_id : ID}, inplace=True)

        return gdf
