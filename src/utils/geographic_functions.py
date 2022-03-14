# Geographic functions
from traceback import print_tb
import geopandas
import numpy as np
import pandas as pd
import geopandas as gpd

from constants import DATE, AVERAGE, GEOMETRY, ID, MANIPULATION_PROJECTION, MAX, MIN, TOTAL


def overlay_over_geo(df_values,
                     df_geo,
                     grouping_columns=[ID, DATE],
                     included_groupings=[TOTAL, AVERAGE, MAX, MIN],
                     default_values=np.nan):
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
    default_values : value or dict
        Value or dict indicating the default values for geometries where no value could be extracted
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

    # Fills Nas
    if DATE in grouping_columns:
        # Adds default by date
        # Builds total DF
        geo_ids = df_geo[ID].unique()
        dfs = []
        for date in df_values[DATE].unique():
            dfs.append(pd.DataFrame({ID: geo_ids, DATE: date}))

        df_global = pd.concat(dfs, ignore_index=True)
        df_overlayed = df_global.merge(df_overlayed,
                                       how='left').fillna(default_values)

    else:
        df_overlayed = df_geo[[ID]].merge(df_overlayed,
                                          how='left').fillna(default_values)

    return (df_overlayed)

def overlay_over_geo_malaria_tmp(df_values,
                     df_geo,
                     grouping_columns=[ID, DATE],
                     included_groupings=[TOTAL, AVERAGE, MAX, MIN],
                     default_values=np.nan):
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
    default_values : value or dict
        Value or dict indicating the default values for geometries where no value could be extracted
    '''

    df_geo = df_geo[[ID, GEOMETRY]]

    # Constructs function for overlay
    def extract_values(df):


        df["area"] = df.geometry.to_crs(
            MANIPULATION_PROJECTION).area


        cols_manipulate = list(set(df.columns) - set(grouping_columns))

        return (df[cols_manipulate] * df["area"]).sum()


    df_overlayed = geopandas.overlay(df_geo, df_values, how='intersection')

    # df_overlayed = df_overlayed.groupby(grouping_columns).apply(
    #     extract_values).reset_index()

    df_overlayed = df_overlayed.groupby(grouping_columns).sum().reset_index()

    rename_dict = {}
    for col in df_overlayed.columns:
        if col in grouping_columns:
            continue
        rename_dict[col] = f"{col}_{TOTAL}"

    df_overlayed.rename(columns=rename_dict, inplace=True)

    # Fills Nas
    if DATE in grouping_columns:
        # Adds default by date
        # Builds total DF
        geo_ids = df_geo[ID].unique()
        dfs = []
        for date in df_values[DATE].unique():
            dfs.append(pd.DataFrame({ID: geo_ids, DATE: date}))

        df_global = pd.concat(dfs, ignore_index=True)
        df_overlayed = df_global.merge(df_overlayed,
                                       how='left').fillna(default_values)

    else:
        df_overlayed = df_geo[[ID]].merge(df_overlayed,
                                          how='left').fillna(default_values)

    return (df_overlayed)