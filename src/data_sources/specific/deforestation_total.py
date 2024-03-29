# Average deforestation data source
from constants import AVERAGE, TOTAL, YEAR, SUM
from data_sources.general.data_from_gee_export import DataFromGeeExport

# Constants
id = "deforestation_total"
name = "Deforestation Average"
file_name = "deforestation_2000_2020.shp"
data_columns_dictionary = {"deforestat": "deforestation"}


class DeforestationTotal(DataFromGeeExport):
    '''
    Total Deforestation Data Source
    '''

    def __init__(self):
        super().__init__(id=id,
                         name=name,
                         folder_name="deforestation",
                         file_name=file_name,
                         data_columns_dictionary=data_columns_dictionary,
                         min_year=2001,
                         max_year=2020,
                         included_groupings=[TOTAL],
                         time_resolution_aggregation_function = SUM,
                         default_values=0,
                         data_time_resolution=YEAR,
                         drop_zeros=True,
                         complete_source=False)
