# Coca data source

from constants import TOTAL
from data_sources.general.data_from_yearly_shapefiles import DataFromYearlyShapefiles

# Constants
id = "coca"
name = "Coca"


class Coca(DataFromYearlyShapefiles):
    '''
    Coca data source
    '''

    def __init__(self):
        super().__init__(id=id,
                         name=name,
                         folder_name="coca_fields_shapes",
                         file_format="coca_fields_{year}.shp",
                         data_columns=['coca'],
                         min_year=2000,
                         max_year=2019,
                         included_groupings=[TOTAL],
                         default_values=0)
