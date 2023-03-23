# Bogota Localities
from constants import GEO_DATA_FOLDER, ID
from geography.abstract.abstact_geography import Geography
import geopandas
import os


class BogotaLocalities(Geography):
    '''
    Geography for the municipalities of Colombia
    
    '''
    # Stable Geometry
    is_stable = True

    @property
    def ID(self):
        return ("bogota_localities")

    @property
    def name(self):
        return ("Bogota Localities")

    @property
    def index(self):
        return self.__index

    def build_geometry(self):
        df = geopandas.read_file(
            os.path.join(GEO_DATA_FOLDER, "bogota/localities.shp"))
        df = df.rename(columns={"index": ID})

        return (df)
