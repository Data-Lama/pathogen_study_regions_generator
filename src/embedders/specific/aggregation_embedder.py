# Agreggation Embedder (does not alter the received inputs)

from embedders.abstract.embedder import AbstractEmbbeder
import constants as con


class AggregationEmbedder(AbstractEmbbeder):

    def __init__(self, aggregation_function='sum'):
        super().__init__()

        self.aggregation_function = aggregation_function

    def aggregation_function(self):
        return (self.aggregation_function)

    def set_aggregation_function(self, aggregation_function):
        self.aggregation_function = aggregation_function

    ID = "aggregation_embedder"
    name = "Aggregation Embedder"

    def embeddData(self, current_geography, df_vector=None, df_matrix=None):
        '''
        Aggregate based on provided function. Default behavior is sum
        '''

        df_vector = df_vector.groupby(con.ID).apply(
            self.aggregation_function).reset_index()

        return (df_vector, df_matrix)
