# Average temperature data source
from constants import AVERAGE
from data_sources.general.data_from_weekly_gee_export import DataFromWeeklyGeeExport

# Constants
id = "temperature_mean"
name = "Mean Temperature"
file_name = "mean_2m_air_temperature_2000_2020"
data_columns_dictionary = {"mean_2m_ai": "temperature"}


class TemperatureAverage(DataFromWeeklyGeeExport):
    '''
    Average Temperature Data Source
    '''

    def __init__(self):
        super().__init__(id=id,
                         name=name,
                         folder_name="weather_shapefiles",
                         file_name=file_name,
                         data_columns_dictionary=data_columns_dictionary,
                         min_year=2000,
                         max_year=2020,
                         included_groupings=[AVERAGE],
                         default_values=None)
