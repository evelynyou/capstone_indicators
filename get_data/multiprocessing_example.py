__author__ = 'saeedamen'  # Saeed Amen

#
# Copyright 2016 Cuemacro
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and limitations under the License.
#
import pandas as pd
from findatapy.market import Market, MarketDataRequest, MarketDataGenerator
from findatapy.util import DataConstants, LoggerManager

START_DATE = "01 Jan 2019"

def load_tickers():
    logger = LoggerManager.getLogger(__name__)

    market = Market(market_data_generator=MarketDataGenerator())

    DataConstants.market_thread_technique = 'thread'

    # load S&P 500 ticker via wikipedia
    snp = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    tickers = snp[0]['Symbol'].to_list()

    # download equities data from Yahoo
    md_request = MarketDataRequest(
        start_date=START_DATE,
        data_source='yahoo',  # use Bloomberg as data source
        tickers=tickers,  # ticker (findatapy)
        fields=['close', 'open', 'high', 'low', 'volume'],  # which fields to download
        vendor_tickers=tickers,  # ticker (Yahoo)
        vendor_fields=['Close', 'Open', 'High', 'Low', 'Volume'])  # which Bloomberg fields to download)


    logger.info("Loading data with threading")

    df = market.fetch_market(md_request)

    logger.info("Loading data with multiprocessing")

    DataConstants.market_thread_technique = 'multiprocessing'

    df = market.fetch_market(md_request)

    logger.info("Loaded data with multiprocessing")

    df.to_csv("temp_downloads/snp.csv")

if __name__ == "__main__":

    ###### below line CRUCIAL when running Windows, otherwise multiprocessing doesn't work! (not necessary on Linux)
    from findatapy.util import SwimPool; SwimPool()

    load_tickers()
