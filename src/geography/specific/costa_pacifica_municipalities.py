# Choco Municipalities
from constants import GEO_DATA_FOLDER, ID
from utils.logger import Logger
from geography.abstract.abstact_geography import Geography
import geopandas
import os
import constants as con


class CostaPacificaMunicipalities(Geography):
    '''
    Geography for the municipalities of Costa_pacifica
    
    '''
    # Stable Geometry
    is_stable = True

    @property
    def ID(self):
        return ("costa_pacifica_municipalities")

    @property
    def name(self):
        return ("Costa Pacifica Municipalities")

    @property
    def index(self):
        return self.__index


    def build_geometry(self):
        df = geopandas.read_file(
            os.path.join(GEO_DATA_FOLDER, "costa_pacifica_munis/costa_pacifica_munis.shp"))
        df = df.rename(columns={"muni_id": ID})

        return (df)
