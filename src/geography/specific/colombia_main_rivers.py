# Colombian Rivers
from constants import GEO_DATA_FOLDER, ID
from geography.abstract.abstact_geography import Geography
import geopandas as gpd
import os
import constants as con


class ColombianMainRivers(Geography):
    '''
    Geography for the rivers of Colombia
    
    '''
    # Stable Geometry
    is_stable = True

    @property
    def ID(self):
        return ("colombian_main_rivers")

    @property
    def name(self):
        return ("Colombian Main rivers")

    @property
    def index(self):
        return self.__index

    def build_geometry(self):
        gdf = gpd.read_file(
            os.path.join(GEO_DATA_FOLDER, f"main_rivers/main_rivers.shp"))
        gdf = gdf.rename(columns={"id": ID})

        return (gdf)