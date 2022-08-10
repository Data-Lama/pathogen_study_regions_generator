# Facebook functions
import os
import pandas as pd
import geopandas

from constants import PIPELINE_DATA_FOLDER, RAW

# Data location constans
FB_MOVEMENT = "fb_mobility"
MOVEMENT_BETWEEN_TILES_RECENT = 'movement_between_tiles_recent'
MOVEMENT_BETWEEN_TILES_ALL = 'movement_between_tiles_all'


def build_movement(directory):
    '''
	Method that build the movement database from single downloaded files
	'''

    # Builds the dataset
    df = build_dataset_in_directory(directory)

    # Adds the geometry
    df['start_movement_lon'] = df.geometry.apply(
        lambda g: extract_lon(g, pos=1))
    df['start_movement_lat'] = df.geometry.apply(
        lambda g: extract_lat(g, pos=1))
    df['end_movement_lon'] = df.geometry.apply(lambda g: extract_lon(g, pos=2))
    df['end_movement_lat'] = df.geometry.apply(lambda g: extract_lat(g, pos=2))
    return (df)


def build_dataset_in_directory(directory, dropna=False):
    '''
    Loads all the file sinto a single dataframe.
    This method is designed for the facebook files
    '''

    datasets = []
    for file in os.listdir(directory):
        file_name = os.path.join(directory, file)
        if file_name.endswith('.csv') and os.stat(file_name).st_size > 0:

            df_temp = read_single_file(file_name, dropna=dropna)
            if df_temp is not None:
                datasets.append(df_temp)

    df = pd.concat(datasets, ignore_index=True)
    return (df)


def extract_lon(poly, pos=1):
    '''
	Extracts the longitud from the polygon string
	'''
    try:
        poly = poly[12:-1]
        poly = poly.replace(', ', ',')
        poly = poly.split(',')[pos - 1]
        resp = poly.split(' ')[0]
    except IndexError:
        return None

    return (float(resp))


def extract_lat(poly, pos=1):
    '''
	Extracts the latitude from the polygon string
	'''
    try:
        poly = poly[12:-1]
        poly = poly.replace(', ', ',')
        poly = poly.split(',')[pos - 1]
        resp = poly.split(' ')[1]
    except IndexError:
        return None

    return (float(resp))


def read_single_file(file_name, dropna=False, parse_dates=False):
    '''
	Reads a single file and returns it as a pandas data frame.
	This method is designed for the facebook files
	'''

    try:
        if parse_dates:
            df = pd.read_csv(file_name,
                             parse_dates=["date_time"],
                             date_parser=lambda x: pd.to_datetime(
                                 x, format="%Y-%m-%d %H%M"))
        else:
            df = pd.read_csv(file_name)

        if dropna:
            df.dropna(inplace=True)

        return (df)

    except pd.errors.EmptyDataError:
        print(f'File {file_name} is empty, please download it again.')

    except pd.errors.ParserError:
        print(f"File: {file_name} is corrupt, please download again")

    return None
