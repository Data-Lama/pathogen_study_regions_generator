# Abstract class for implementing a Geography
import abc
from abc import ABC, abstractmethod


class AbstractGeography(ABC):

    __geometry = None

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

    # ------------------
    # ---- Methods -----
    # ------------------
    @abstractmethod
    def build_geometry(self):
        '''
        Method that build geometry for the geography. This method is only called once.
        '''
        pass

    def get_geometry(self):
        '''
        Method that gets geometry for the geography.
        This method calls build geometry only if the geometry object has not been called.
        '''
        if self.__geometry is None:
            self.__geometry = self.build_geometry()

        return (self.__geometry)
