# Mobility to similarity embedder
from constants import ID, ID_1, ID_2
from embedders.abstract.embedder import AbstractEmbbeder
import pandas as pd


class MobilityToSimilarityEmbeder(AbstractEmbbeder):

    ID = "mobility_to_similarity_embedder"
    name = "Mobility to Similarity Embeder"

    def __init__(self, mobility_col):
        '''
        Embedder that turns a mobility matrix across time and outputs a similarity matrix based on it.

        Parameters
        ----------
        mobility_col : string
            The column that will be interpreted as mobility
        '''
        super().__init__()

        self.mobility_col = mobility_col

    def embeddData(self, current_geography, df_vector=None, df_matrix=None):

        # Computes the average mobility
        df_mobility = df_matrix[[ID_1, ID_2, self.mobility_col
                                 ]].groupby([ID_1, ID_2]).mean().reset_index()

        # Gets Ids
        ids = current_geography.get_geometry()[ID].values

        df_ids = pd.DataFrame({ID: ids})
        df_complete_matrix = df_ids[[ID]].merge(
            df_ids[[ID]], how='cross').rename(columns={
                f"{ID}_x": ID_1,
                f"{ID}_y": ID_2
            })

        df_mobility = df_complete_matrix.merge(df_mobility,
                                               how='left').fillna(0)

        return (df_vector, df_mobility)
