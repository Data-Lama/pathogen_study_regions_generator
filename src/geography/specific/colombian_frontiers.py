# Colombian Departments
from constants import GEO_DATA_FOLDER, ID
from geography.abstract.abstact_geography import Geography
import geopandas
import os


class ColombianFrontiers(Geography):
    '''
    Geography for the froniers of Colombia
    
    '''
    # Stable Geometry
    is_stable = True

    @property
    def ID(self):
        return ("colombian_frontiers")

    @property
    def name(self):
        return ("Colombian Frontiers")

    def build_geometry(self):
        df = geopandas.read_file(
            os.path.join(GEO_DATA_FOLDER, "frontiers/frontiers.shp"))
        df = df.rename(columns={"id": ID})

        return (df)
