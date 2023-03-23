# Data source from an official commodity.
# Uses Yahoo finance API
from constants import DAY, IDENT, DATE, ID, LINEAR, MEAN, SUB_ID, VALUE, YEAR, isTimeResolutionValid

from data_sources.abstract.vector_data_source import VectorDataSource

import yfinance as yf
import pandas as pd

from utils.date_functions import lower_time_resolution

from geography.abstract.abstact_geography import Geography


IDENT = IDENT

# Constants
target_col = "Adj Close"
date_col = "Date"


class OfficialCommodity(VectorDataSource):
    '''
    Main class for extraction of an official commodity
    This class is agnostic to the given geography.
    Assumes prices are global.
    '''

    def __init__(self, ID, name, symbol, min_year, max_year):
        '''
        '''
        super().__init__()
        self.__id = ID
        self.__name = name
        self.symbol = symbol
        self.min_year = min_year
        self.max_year = max_year

    @property
    def ID(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    # Override
    def createData(self, geography: Geography, time_resolution: str) -> pd.DataFrame:

        # Extracts geopandas
        df_geo = geography.get_geometry()
        
        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        # Downloads all the data
        df = yf.download(self.symbol, period="max")
        # Sets column
        df = df.reset_index()
        df = df[[date_col, target_col]]

        # Filters
        df = df[(df[date_col] >= pd.to_datetime(f"{self.min_year}-01-31")) & (
            df[date_col] <= pd.to_datetime(f"{self.max_year}-12-31"))].copy()

        # Renames
        df = df.rename(columns={date_col: DATE, target_col: VALUE})

        # Cross product with geo id
        df = df_geo[[ID]].merge(df, how='cross')

        df = lower_time_resolution(df=df,
                    initial_time_resolution=DAY,
                    target_time_resolution=time_resolution,
                    aggregation_function=MEAN)

        
        return (df)

    def createDataFromCachedSubGeography(self, time_resolution, sub_geography,
                                         df_map):

        # Checks time resolution
        isTimeResolutionValid(time_resolution)

        # Gets the data from the sub_geography
        df = self.get_data(sub_geography, time_resolution)

        # Maps the ids
        df.rename(columns={ID: SUB_ID}, inplace=True)
        df = df.merge(df_map)
        df.drop(SUB_ID, axis=1, inplace=True)

        # Agglomerates
        # Non geographic datasource. Simply drops duplicates
        # Groups and excecutes
        df_final = df.drop_duplicates(subset=[ID, DATE])

        return (df_final)
