# Average precipitation data source
from constants import AVERAGE, WEEK
from data_sources.general.data_from_gee_export import DataFromGeeExport

# Constants
id = "precipitation_average"
name = "Precipitation Average"
file_name = "total_precipitation_2000_2020.shp"
data_columns_dictionary = {"total_prec": "precipitation"}


class PrecipitationAverage(DataFromGeeExport):
    '''
    Average Precipitation Data Source
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
                         default_values=0,
                         data_time_resolution=WEEK)
