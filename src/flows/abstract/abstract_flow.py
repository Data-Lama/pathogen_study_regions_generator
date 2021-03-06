# Abstract class for implementing a flow
import abc
from abc import ABC, abstractmethod
from asyncio.log import logger
from clusterers.specific.identity_clusterer import IdentityClusterer
from constants import CLUSTER_ID, DATE, GEOMETRY, ID, ID_1, ID_2, SUPPLEMENTARY_ARGS

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
    final_geometry = None

    # State
    has_ranned = False
    data_loaded = False
    data_embedded = False
    data_clustered = False

    # Vector and Matrix Data Names
    vector_data_sources_names = []
    matrix_data_sources_names = []

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
        Embedder or array of embedders of the flow. 
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

    @abc.abstractproperty
    def geography(self):
        '''
        Geography for the flow
        '''
        pass

    # ------------------
    # ---- Methods -----
    # ------------------
    def run(self, warnings_as_errors=False):
        '''
        Method that runs the entire flow with the designated elements.
        At each point the pipeline assignes the corresponding element.
        The usual excecution of the pipeline is:
        1. Loads the data (both vector and matrix)
        3. Embbeds the data sources
        4. Clusteres the embedded sources.
        '''

        # Sets the warning parameter
        self.warnings_as_errors = warnings_as_errors

        # Resets attributes
        self.df_vector = None
        self.df_embedded_vector = None
        self.df_matrix = None
        self.df_embedded_matrix = None
        self.clustered_ids = None
        self.final_geometry = None
        self.has_ranned = False
        self.data_loaded = False
        self.data_embedded = False
        self.data_clustered = False

        Logger.print_progress(f"Starts Flow: {self.name}")
        Logger.enter_level()
        # Assigns initial geography
        # ----------------------
        Logger.print_progress(f"Loads Initial Geography")
        self.initial_geometry = self.geography.get_geometry()

        # Loads Data
        # ----------------------
        Logger.print_progress("Loads Data")
        Logger.enter_level()
        # Assigns
        self.df_vector, self.df_matrix = self.loadData(self.geography)
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
        Logger.print_progress("Builds Final Geometry")
        Logger.enter_level()
        self.buildFinalGeography()
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
        geography : Geography
            Geography with the desired geometry.
            The geometry is a DataFrame with the desired geographical resolution. The df must include columns:
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
        for data_source in self.vector_data_sources:
            ds = data_source()

            # Adds Name
            self.vector_data_sources_names.append(ds.name)

            Logger.print_progress(
                f"Extracts {i} of {len(self.vector_data_sources)}: {ds.name} ({ds.ID}) "
            )

            # Extracts the data source
            df_data = ds.get_data(geography, self.time_resolution)
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
        if df_vector is not None:
            df_vector = df_vector.sort_values('date').reset_index(drop=True)

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
        for data_source in self.matrix_data_sources:

            ds = data_source()

            # Adds Name
            self.matrix_data_sources_names.append(ds.name)

            Logger.print_progress(
                f"Extracts {i} of {len(self.matrix_data_sources)}: {ds.name} ({ds.ID}) "
            )
            # Extracts the data source
            df_data = ds.get_data(geography, self.time_resolution)
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
        if df_matrix is not None:
            df_matrix = df_matrix.sort_values('date').reset_index(drop=True)

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
            raise ValueError('''Data has not been loaded. 
                Please load data before embedding''')

        embedders = self.embedder
        if not isinstance(self.embedder, list):
            embedders = [self.embedder]

        Logger.print_progress(f"Found {len(embedders)} embedders")
        Logger.enter_level()

        self.df_embedded_vector, self.df_embedded_matrix = self.df_vector, self.df_matrix

        for emb in embedders:

            Logger.print_progress(emb.name)
            self.df_embedded_vector, self.df_embedded_matrix = emb.embeddData(
                current_geography=self.geography,
                df_vector=self.df_embedded_vector,
                df_matrix=self.df_embedded_matrix)

        Logger.exit_level()

    def clusterData(self):
        '''
        Method that embedds the data with the given embedder.
        After this method both df_embedded_vector and df_embedded_martrix will be assigned (if configured)
        '''
        if not self.data_embedded:
            raise ValueError('''Data has not been embedded. 
                Please embedd data before clustering. 
                If you need access to the entire time series, please use an the IdentityEmbedder.'''
                             )
        self.clustered_ids = self.clusterer.clusterData(
            current_geography=self.geography,
            df_vector=self.df_embedded_vector,
            df_matrix=self.df_embedded_matrix)

    def buildFinalGeography(self):
        '''
        Builds the final geography from the initial clustering.
        After this method, the attribute final_geography will be set
        '''

        if not self.data_clustered:
            raise ('''Data has not been clustered. 
                Please cluster data before merging geography''')

        # Cleans the clusterd ids
        self.clustered_ids = self.clustered_ids.drop_duplicates(subset=[ID])

        # Checks Integrity
        clust_ids = set(self.clustered_ids[ID].unique())
        clust_geo = set(self.initial_geometry[ID].unique())

        diff = clust_geo.difference(clust_ids)
        if len(diff) > 0:
            text = f'''Error in building final geography. The geography ids: {diff} are missing in the clustered ids'''
            if self.warnings_as_errors:
                raise ValueError(text)
            else:
                Logger.print_warning(text)

        diff = clust_ids.difference(clust_geo)
        if len(diff) > 0:

            text = f'''Error in building final geography. The clusterd ids: {diff} are missing in the geography ids'''
            if self.warnings_as_errors:
                raise ValueError(text)
            else:
                Logger.print_warning(text)

        # Dissolves
        final_geometry = self.initial_geometry[[ID, GEOMETRY
                                                ]].merge(self.clustered_ids,
                                                         on=[ID])
        final_geometry = final_geometry.drop([ID], axis=1)
        final_geometry = final_geometry.dissolve(by=CLUSTER_ID).reset_index()

        # Renames
        final_geometry = final_geometry.rename(columns={CLUSTER_ID: ID})

        # Assigns
        self.final_geometry = final_geometry
