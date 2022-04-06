# Linear Regression coefficient embedder
from constants import DATE, ID
from embedders.abstract.embedder import AbstractEmbbeder

# Linear Regression
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


class LinearRegressionCoefficientEmbedder(AbstractEmbbeder):

    ID = "linear_regression_coefficient_embedder"
    name = "Linear Regression Coefficient Embeder"

    def __init__(self, target_col):
        super().__init__()

        self.target_col = target_col

    def embeddData(self, current_geography, df_vector=None, df_matrix=None):

        df_vector = df_vector.dropna()
        # Extract observed variable columns
        variable_cols = df_vector.columns.difference(
            [ID, DATE, self.target_col])

        imnersion = []
        for geo_id in df_vector[ID].unique():

            df_temp = df_vector[df_vector[ID] == geo_id]

            # Data
            X = df_temp[variable_cols]

            # Target
            y = df_temp[self.target_col]

            # Scaler
            scaler = StandardScaler()
            X = scaler.fit_transform(X)

            if np.std(y) != 0:
                y = (y - np.mean(y)) / np.std(y)
            else:
                y = (y - np.mean(y))

            # Regression
            reg = LinearRegression().fit(X, y)

            resp_dic = {ID: geo_id}
            for i in range(len(variable_cols)):
                resp_dic[variable_cols[i]] = reg.coef_[i]

            imnersion.append(resp_dic)

        df_emdedded = pd.DataFrame(imnersion)

        return (df_emdedded, df_matrix)
