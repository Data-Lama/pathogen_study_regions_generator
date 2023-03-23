# Bogota Sectors
from constants import GEO_DATA_FOLDER, ID
from geography.abstract.abstact_geography import Geography
import geopandas
import os


class BogotaSectors(Geography):
    '''
    Geography for the municipalities of Colombia
    
    '''
    # Stable Geometry
    is_stable = True

    @property
    def ID(self):
        return ("bogota_sectors")

    @property
    def name(self):
        return ("Bogota Sectors")

    @property
    def index(self):
        return self.__index

    def build_geometry(self):
        df = geopandas.read_file(
            os.path.join(GEO_DATA_FOLDER, "bogota/sectors.shp"))
        df = df.rename(columns={"COD_SECTOR": ID})

        return (df)
