# Abstract class for implementing a flow
import abc
from abc import ABC, abstractmethod
from clusterers.specific.identity_clusterer import IdentityClusterer
from constants import CLUSTER_ID, DATE, ID, ID_1, ID_2

from embedders.specific.identity_embedder import IdentityEmbbeder
from utils.logger import Logger

ident = "   "


class AbstractFlow(ABC):

    # Properties that will be assigned after ranned
    # Consolidated data vector source
    df_vector = None
    df_embedded_vector = None
    # Consolidated matrix source
    df_matrix = None
    df_embedded_matrix = None
    # Clusterer
    clustered_ids = None
    # Final geography
    final_geography = None

    # State
    has_ranned = False
    data_loaded = False
    data_embedded = False
    data_clustered = False

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

    @abc.abstractproperty
    def time_resolution(self):
        '''
        Time resolution of the flow
        '''
        pass

    @abc.abstractproperty
    def vector_data_sources(self):
        '''
        Collections of vector data sources
        '''
        return []

    @abc.abstractproperty
    def matrix_data_sources(self):
        '''
        Collections of matrix data sources
        '''
        return []

    @abc.abstractproperty
    def embedder(self):
        '''
        Embedder of the flow. 
        Default: identity
        '''
        return IdentityEmbbeder()

    @abc.abstractproperty
    def clusterer(self):
        '''
        Embedder of the flow. 
        Default: identity
        '''
        return IdentityClusterer()

    # ------------------
    # ---- Methods -----
    # ------------------

    @abstractmethod
    def get_initial_geography(self):
        '''
        Initial geography for the flow.
        This is set as a method, not a property since it might be expensive to execute.
        It will only be excecuted once in the run() procedure.
        '''
        pass

    # ------------------
    # ---- Methods -----
    # ------------------
    def run(self):
        '''
        Method that runs the entire flow with the designated elements.
        At each point the pipeline assignes the corresponding element.
        The usual excecution of the pipeline is:
        1. Loads the data (both vector and matrix)
        3. Embbeds the data sources
        4. Clusteres the embedded sources.
        '''

        # Resets attributes
        self.df_vector = None
        self.df_embedded_vector = None
        self.df_matrix = None
        self.df_embedded_matrix = None
        self.clustered_ids = None
        self.final_geography = None
        self.has_ranned = False
        self.data_loaded = False
        self.data_embedded = False
        self.data_clustered = False

        Logger.print_progress(f"Starts Flow: {self.name}")
        Logger.enter_level()
        # Assigns initial geography
        # ----------------------
        Logger.print_progress(f"Loads Initial Geography")
        self.initial_geography = self.get_initial_geography()

        # Loads Data
        # ----------------------
        Logger.print_progress("Loads Data")
        Logger.enter_level()
        # Assigns
        self.df_vector, self.df_matrix = self.loadData(self.initial_geography)
        self.data_loaded = True
        Logger.exit_level()

        # Embbeds Data
        # ----------------------
        Logger.print_progress("Embedds Data")
        Logger.enter_level()
        self.embeddData()
        self.data_embedded = True
        Logger.exit_level()

        # Clusters Data
        # ----------------------
        Logger.print_progress("Clusters Data")
        Logger.enter_level()
        self.clusterData()
        self.data_clustered = True
        Logger.exit_level()

        # Builds final geography
        # ----------------------
        Logger.print_progress("Builds Final Geography")
        Logger.enter_level()
        self.buildFinalGeography()
        self.data_clustered = True
        Logger.exit_level()

        self.has_ranned = True
        Logger.exit_level()
        Logger.print_progress(f"Flow Ended")
        Logger.print_progress("Done")
        Logger.print_progress("-----------------")

    def loadData(self, geography):
        '''
        Method that creates the data sources. 
        After this method both df_vector and df_martrix will be assigned (if configured)

        Parameters
        ----------
        df_geo : Geopandas.DataFrame
            DataFrame with the desired geographical resolution. The df must include columns:
                - geometry
                - ID : column with the unique ID
        '''

        # Vector
        Logger.print_progress(f"Loads Vector Data")
        Logger.print_progress(
            f"Found {len(self.vector_data_sources)} elements")
        Logger.enter_level()
        df_vector = None
        i = 1
        for ds in self.vector_data_sources:
            Logger.print_progress(
                f"Extracts {i} of {len(self.vector_data_sources)}: {ds.name} ({ds.ID}) "
            )
            # Extracts the data source
            df_data = ds.createData(geography, self.time_resolution)
            # To ensure uniqueness, adds the id to each column
            col_dict = dict([(col, f"{ds.ID}_{col}") for col in df_data.columns
                             if col not in [ID, DATE]])
            df_data = df_data.rename(columns=col_dict)

            if df_vector is None:
                df_vector = df_data
            else:
                df_vector = df_vector.merge(df_data,
                                            on=[ID, DATE],
                                            how="outer")
            i += 1

        Logger.exit_level()
        Logger.print_progress(f"Done")
        Logger.print_progress(f"")
        Logger.print_progress(f"Loads Matrix Data")
        Logger.print_progress(
            f"Found {len(self.matrix_data_sources)} elements")
        Logger.enter_level()

        # Matrix
        df_matrix = None
        i = 1
        for ds in self.matrix_data_sources:
            Logger.print_progress(
                f"Extracts {i} of {len(self.matrix_data_sources)}: {ds.name} ({ds.ID}) "
            )
            # Extracts the data source
            df_data = ds.createData(geography, self.time_resolution)
            # To ensure uniqueness, adds the id to each column
            col_dict = dict([(col, f"{ds.ID}_{col}") for col in df_data.columns
                             if col not in [ID_1, ID_2, DATE]])
            df_data = df_data.rename(columns=col_dict)

            if df_matrix is None:
                df_matrix = df_data
            else:
                df_matrix = df_vector.merge(df_data,
                                            on=[ID_1, ID_2, DATE],
                                            how="outer")

        Logger.exit_level()
        Logger.print_progress(f"Done")
        Logger.print_progress(f"------------------")

        return (df_vector, df_matrix)

    def embeddData(self):
        '''
        Method that embedds the data with the given embedder.
        After this method both df_embedded_vector and df_embedded_martrix will be assigned (if configured)
        '''
        if not self.data_loaded:
            raise ('''Data has not been loaded. 
                Please load data before embedding''')
        self.df_embedded_vector, self.df_embedded_matrix = self.embedder.embeddData(
            df_vector=self.df_vector, df_matrix=self.df_matrix)

    def clusterData(self):
        '''
        Method that embedds the data with the given embedder.
        After this method both df_embedded_vector and df_embedded_martrix will be assigned (if configured)
        '''
        if not self.data_embedded:
            raise ('''Data has not been embedded. 
                Please embedd data before clustering. 
                If you need access to the entire time series, please use an the IdentityEmbedder.'''
                   )
        self.clustered_ids = self.clusterer.clusterData(
            df_vector=self.df_vector, df_matrix=self.df_matrix)

    def buildFinalGeography(self):
        '''
        Builds the final geography from the initial clustering.
        After this method, the attribute final_geography will be set
        '''

        if not self.data_loaded:
            raise ('''Data has not been clustered. 
                Please cluster data before merging geography''')

        # Cleans the clusterd ids
        self.clustered_ids = self.clustered_ids.drop_duplicates(subset=[ID])

        # Checks Integrity
        clust_ids = set(self.clustered_ids[ID].unique())
        clust_geo = set(self.initial_geography[ID].unique())

        diff = clust_geo.difference(clust_ids)
        if len(diff) > 0:
            raise ('''Error in building final geography.
                    The geography ids: {diff} are missing in the clustered ids'''
                   )

        diff = clust_ids.difference(clust_geo)
        if len(diff) > 0:
            raise ('''Error in building final geography.
                    The clusterd ids: {diff} are missing in the geography ids'''
                   )

        # Dissolves
        final_geography = self.initial_geography.merge(self.clustered_ids,
                                                       on=[ID])
        final_geography = final_geography.dissolve(by=CLUSTER_ID).reset_index()

        # Renames
        final_geography = final_geography.rename(columns={CLUSTER_ID: ID})

        # Assigns
        self.final_geography = final_geography
