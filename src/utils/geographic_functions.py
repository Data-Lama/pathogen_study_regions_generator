# Geographic functions
import geopandas
import pandas as pd

from constants import DATE, AVERAGE, GEOMETRY, ID, MANIPULATION_PROJECTION, MAX, MIN, TOTAL


def overlay_over_geo(
    df_values,
    df_geo,
    grouping_columns=[ID, DATE],
    included_groupings=[TOTAL, AVERAGE, MAX, MIN],
):
    '''
    Method that overlays the given df over the geographic dataframe

    Parameters
    ----------
    df_values : Geopandas.DataFrame
        Geopandas dataframe with the values to overlay. This method assumes that anything other than
        than the grouping columns and geomtry is a value that must be overlayed.
    df_geo : Geopandas.DataFrame
        Geopandas dataframe with the gemotry to be overlayed. Will only use the columns ID and geometry
    grouping_columns : array
        Columns that must be grouped over
    included_groupings : array
        Grouping functions to be applied 
    '''

    df_geo = df_geo[[ID, GEOMETRY]]

    # Constructs function for overlay
    def extract_values(df):

        geo_id = df.iloc[0][ID]
        area = df_geo[df_geo[ID] == geo_id].geometry.to_crs(
            MANIPULATION_PROJECTION).area.values[0]

        response = {}
        for col in df.columns:
            if col in [ID, 'geometry']:
                continue

            if MAX in included_groupings:
                response[f"{col}_{MAX}"] = df[col].max()
            if MIN in included_groupings:
                response[f"{col}_{MIN}"] = df[col].min()
            if TOTAL in included_groupings:
                response[f"{col}_{TOTAL}"] = (
                    df[col] *
                    df.geometry.to_crs(MANIPULATION_PROJECTION).area).sum()
            if AVERAGE in included_groupings:
                response[f"{col}_{AVERAGE}"] = (df[col] * df.geometry.to_crs(
                    MANIPULATION_PROJECTION).area).sum() / area

            return (pd.DataFrame([response]))

    df_overlayed = geopandas.overlay(df_geo, df_values, how='intersection')

    df_overlayed = df_overlayed.groupby(grouping_columns).apply(
        extract_values).reset_index().drop(f'level_{len(grouping_columns)}',
                                           axis=1)

    return (df_overlayed)
