# Total precipitation data source
from constants import TOTAL, WEEK, SUM
from data_sources.general.data_from_gee_export import DataFromGeeExport

# Constants
id = "precipitation_total"
name = "Precipitation Total"
file_name = "total_precipitation_2000_2020.shp"
data_columns_dictionary = {"total_prec": "precipitation"}


class PrecipitationTotal(DataFromGeeExport):
    '''
    Total Precipitation Data Source
    '''

    def __init__(self):
        super().__init__(id=id,
                         name=name,
                         folder_name="weather_shapefiles",
                         file_name=file_name,
                         data_columns_dictionary=data_columns_dictionary,
                         min_year=2000,
                         max_year=2020,
                         included_groupings=[TOTAL],
                         time_resolution_aggregation_function=SUM,
                         default_values=0,
                         data_time_resolution=WEEK)
