# Malaria data source

from constants import SUM, TOTAL, DAY, WEEK, MONTH, YEAR
from data_sources.general.data_from_time_series_csv import DataFromTimeSeriesOfCSV
from geography.specific.colombian_municipalities import ColombianMunicipalities

# Constants
id = "gold_exports"
name = "Gold Exports"


class GoldExport(DataFromTimeSeriesOfCSV):
    '''
    gold exports data source
    '''

    def __init__(self):
        super().__init__(id=id,
                         name=name,
                         folder_name="gold_exports",
                         file_name="gold_exports.csv",
                         min_year=2012,
                         max_year=2020,
                         suplementary_geography=ColombianMunicipalities(),
                         min_time_resolution=MONTH,
                         index_id="muni_id",
                         included_groupings=[SUM],
                         columns_of_interest=["grams"],
                         default_values={"grams": 0})
