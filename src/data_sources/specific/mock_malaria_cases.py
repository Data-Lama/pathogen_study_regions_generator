# Mock Malaria data source
import numpy as np
import pandas as pd
from constants import DATE, ID, TOTAL, DAY, WEEK, MONTH, YEAR
from data_sources.abstract.vector_data_source import VectorDataSource
from data_sources.general.data_from_time_series_csv import DataFromTimeSeriesOfCSV
from utils.date_functions import get_dates_between_years_by_resolution

from geography.abstract.abstact_geography import Geography

# Constants
id = "malaria"
name = "Malaria"


class MockMalaria(VectorDataSource):
    '''
    Mock Malaria data source
    '''

    @property
    def ID(self):
        return ("mock_malaria")

    @property
    def name(self):
        return ("Mock Malaria")

    def createData(self, geography: Geography, time_resolution: str) -> pd.DataFrame:
        
        # Extracts geopandas
        df_geo = geography.get_geometry()
        
        all_dates = get_dates_between_years_by_resolution(
            min_year=2006, max_year=2019, time_resolution=time_resolution)

        df_dates = pd.DataFrame({DATE: all_dates})

        df_data = df_geo[[ID]].merge(df_dates, how="cross")

        # Adds mock
        df_data['num_cases'] = np.random.uniform(0,
                                                 1000,
                                                 size=df_data.shape[0])

        # Orders columns
        return (df_data)

    def createDataFromCachedSubGeography(self, time_resolution, sub_geography,
                                         df_map):

        # Mock Geometry

        all_dates = get_dates_between_years_by_resolution(
        min_year=2006, max_year=2019, time_resolution=time_resolution)

        df_dates = pd.DataFrame({DATE: all_dates})

        df_data = df_map[[ID]].drop_duplicates().merge(df_dates, how="cross")

        # Adds mock
        df_data['num_cases'] = np.random.uniform(0,
                                                 1000,
                                                 size=df_data.shape[0])

        # Orders columns
        return (df_data)

