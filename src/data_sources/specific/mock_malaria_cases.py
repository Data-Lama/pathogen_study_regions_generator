# Mock Malaria data source
import numpy as np
import pandas as pd
from constants import DATE, ID, TOTAL, DAY, WEEK, MONTH, YEAR
from data_sources.general.data_from_time_series_csv import DataFromTimeSeriesOfCSV
from utils.date_functions import get_dates_between_years_by_resolution

# Constants
id = "malaria"
name = "Malaria"


class Malaria():
    '''
    Mock Malaria data source
    '''

    ID = "malaria"
    name = "Mock Malaria"

    def createData(self, df_geo, time_resolution, **kwargs):

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