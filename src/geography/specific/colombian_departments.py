# Colombian Departments
from constants import GEO_DATA_FOLDER, ID
from geography.abstract.abstact_geography import Geography
import geopandas
import os
import constants as con


class ColombianDepartments(Geography):
    '''
    Geography for the departments of Colombia
    
    '''
    # Stable Geometry
    is_stable = True

    @property
    def ID(self):
        return ("colombian_departments")

    @property
    def name(self):
        return ("Colombian Departments")

    def build_geometry(self):
        df = geopandas.read_file(
            os.path.join(GEO_DATA_FOLDER, "departments/departments.shp"))
        df = df.rename(columns={"depto_id": ID})

        return (df)
