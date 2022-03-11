# Min temperature data source
from constants import MIN
from data_sources.general.data_from_weekly_gee_export import DataFromWeeklyGeeExport

# Constants
id = "temperature_min"
name = "Min Temperature"
file_name = "minimum_2m_air_temperature_2000_2020"
data_columns_dictionary = {"minimum_2m": "temperature"}


class TemperatureMin(DataFromWeeklyGeeExport):
    '''
    Min temperature Data Source
    '''

    def __init__(self):
        super().__init__(id=id,
                         name=name,
                         folder_name="weather_shapefiles",
                         file_name=file_name,
                         data_columns_dictionary=data_columns_dictionary,
                         min_year=2000,
                         max_year=2020,
                         included_groupings=[MIN],
                         default_values=None)
