# Abstract class for implementing a Geography
import abc
from abc import ABC, abstractmethod
import uuid
from constants import GEOMETRY, ID
from utils.geographic_functions import get_enclosing_geoemtry


class AbstractGeography(ABC):

    # Local Geometry (read only)
    __geometry = None
    # Unique identifier (read only)
    # This attribute is used in conjuction with is stable to prevent missreading cache files
    __uuid = None

    # Stable Variable
    # Determines if the geoemtry is stable across time or depends upon excecution
    is_stable = False

    # Sub Geography (From previuos flow excecutions for example)
    sub_geography = None
    df_map = None

    # ---------------------------
    # -- Abstract Properties ----
    # ---------------------------
    @abc.abstractproperty
    def ID(self):
        '''
        Unique identifier for the flow
        '''
        pass

    @abc.abstractproperty
    def name(self):
        '''
        Human readable name for the flow
        '''
        pass

    # Abstract Method
    @abstractmethod
    def build_geometry(self):
        '''
        Method that build geometry for the geography. This method is only called once.
        '''
        pass

    # ------------------
    # ---- Methods -----
    # ------------------
    def get_geometry(self):
        '''
        Method that gets geometry for the geography.
        This method calls build geometry only if the geometry object has not been called.
        '''
        if self.__geometry is None:
            self.__geometry = self.build_geometry()

        return (self.__geometry)

    def get_uuid(self):
        '''
        Return uuid. This uuid is unique for the lifecycle of the component
        '''
        if self.__uuid is None:
            self.__uuid = uuid.uuid4()

        return (self.__uuid)

    def get_enclosing_geometry(self):
        '''
        Gets the enclosing geometry as a geopandas
        '''
        geometry = self.get_geometry()
        return (get_enclosing_geoemtry(geometry))
