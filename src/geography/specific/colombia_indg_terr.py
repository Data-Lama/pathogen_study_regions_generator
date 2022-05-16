# Colombian indigenous communities
import this
from constants import GEO_DATA_FOLDER, ID
from geography.abstract.abstact_geography import AbstractGeography
import geopandas as gpd
import os
import constants as con


class ColombianIndgTerr(AbstractGeography):
    '''
    Geography for the indigenous territories of Colombia
    
    '''
    # Stable Geometry
    is_stable = True

    @property
    def ID(self):
        return ("colombian_indg_terr")

    @property
    def name(self):
        return ("Colombian Indigenous Territories")

    @property
    def index(self):
        return self.__index

    def build_geometry(self):
              
        gdf = gpd.read_file(
            os.path.join(GEO_DATA_FOLDER, f"indigenous_territories/territorios_indigenas.shp"))
        gdf = gdf.rename(columns={"id": ID})

        return (gdf)