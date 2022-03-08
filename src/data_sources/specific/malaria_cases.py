# Malaria data source

from constants import TOTAL
from data_sources.general.data_from_time_series_csv import DataFromTimeSeriesOfCSV

# Constants
id = "malaria"
name = "Malaria"


class Malaria(DataFromTimeSeriesOfCSV):
    '''
    malaria data source
    '''

    def __init__(self):
        super().__init__(id=id,
                         name=name,
                         folder_name="malaria_cases",
                         file_name="anonymized_individual_data.csv",
                         min_year=2006,
                         max_year=2019,
                         included_groupings=[TOTAL],
                         columns_to_exclude=["notification_muni_id", "residence_muni_id"])

                         