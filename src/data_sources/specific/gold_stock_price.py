# Gold stock price data source

# Constants
from data_sources.general.official_commodity import OfficialCommodity

id = "gold_stock_price"
name = "Gold Stock Price"
symbol = "GC=F"


class GoldStockPrice(OfficialCommodity):
    '''
    Gold stock price
    '''

    def __init__(self):
        super().__init__(ID=id,
                         name=name,
                         symbol=symbol,
                         min_year=2008,
                         max_year=2021)
