# Cache Functions


def build_cache_name(data_source_id, geography_id, time_resolution):
    '''
    Method that builds the cache name
    '''

    return (f"{data_source_id}-{geography_id}-{time_resolution}.csv")
