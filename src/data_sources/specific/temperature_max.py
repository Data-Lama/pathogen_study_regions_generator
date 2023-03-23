# Max temperature data source
from constants import MAX
from data_sources.general.data_from_gee_export import DataFromGeeExport

# Constants
id = "temperature_max"
name = "Max Temperature"
file_name = "maximum_2m_air_temperature_2000_2020.shp"
data_columns_dictionary = {"maximum_2m": "temperature"}


class TemperatureMax(DataFromGeeExport):
    '''
    Max Temprerature Data Source
    '''

    def __init__(self):
        super().__init__(id=id,
                         name=name,
                         folder_name="weather_shapefiles",
                         file_name=file_name,
                         data_columns_dictionary=data_columns_dictionary,
                         min_year=2000,
                         max_year=2020,
                         included_groupings=[MAX],
                         time_resolution_aggregation_function = MAX,
                         default_values=None)
