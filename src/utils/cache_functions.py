# Cache Functions


def build_cache_name(data_source, geography, time_resolution):
    '''
    Method that builds the cache name
    '''

    if geography.is_stable:
        return (f"{data_source.ID}-{geography.ID}-{time_resolution}.csv")
    else:
        return (
            f"TEMPORAL-{geography.get_uuid()}-{data_source.ID}-{geography.ID}-{time_resolution}.csv"
        )
