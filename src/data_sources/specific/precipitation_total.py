# Total precipitation data source
from constants import TOTAL
from data_sources.general.data_from_weekly_gee_export import DataFromWeeklyGeeExport

# Constants
id = "precipitation_total"
name = "Precipitation Total"
file_name = "total_precipitation_2000_2020"
data_columns_dictionary = {"total_prec": "precipitation"}


class PrecipitationTotal(DataFromWeeklyGeeExport):
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
                         included_groupings=[TOTAL])
