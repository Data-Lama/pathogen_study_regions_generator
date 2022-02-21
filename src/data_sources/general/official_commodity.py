# Data source from an official commodity.
# Uses Yahoo finance API
from constants import DATA_SOURCE_IDENT, DATE, ID, VALUE, isTimeResolutionValid

from data_sources.abstract.vector_data_source import VectorDataSource

import yfinance as yf
import pandas as pd

from utils.date_functions import get_period_representative_function

IDENT = DATA_SOURCE_IDENT

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
        self.__ID = ID
        self.__name = name
        self.symbol = symbol
        self.min_year = min_year
        self.max_year = max_year

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    # Override
    def createData(self, df_geo, time_resolution):

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

        # Maps the date
        df[date_col] = df[date_col].apply(
            get_period_representative_function(time_resolution))

        # Groupsby
        df = df.groupby(date_col).mean().reset_index()

        # Renames
        df = df.rename(columns={date_col: DATE, target_col: VALUE})

        # Cross product with geo id
        df = df_geo[[ID]].merge(df, how='cross')

        return (df)
