import scrapy
import re
import time
import json
from datetime import datetime as dt
from scrape_portal.items import NSEItem

class NSESpider(scrapy.Spider):
    name = "nse"
    allowed_domains = ['www1.nseindia.com']
    news_urls = [
        # 'live_market/dynaContent/live_watch/equities_stock_watch.htm', 
        'live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json'
    ]

    def __init__(self, scrape_date=None, *args, **kwargs):
        super(NSESpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www1.nseindia.com/%s' % (path) for path in self.news_urls]

    def parse(self, response):
        # parse thru each of the element
        # for element in response.css('table#dataTable>.tbody>tr'):
        #     item = NSEItem()
            
        #     cols = ['symbol', '', '', 'open', 'high', 'low', 'ltp', 'chng', 'pcnt_chng', 'volume', 'turnover', 'ftwh', 'ftwl', '', 'tsfd_pcnt_chng', '', 'td_pcnt_chng']

        #     for i, td in enumerate(element.css('td')):
        #         if cols[i]:
        #             if cols[i] == 'volume':
        #                 item[cols[i]] = td.css('.lacvol::text').extract_first()
        #             if cols[i] == 'turnover':
        #                 item[cols[i]] = td.css('.lacValue::text').extract_first()
        #             else:
        #                 item[cols[i]] = td.css('::text').extract_first()

        #     yield item

        remote_local_key_map = {
            "symbol": "symbol",
            "open": "open",
            "high": "high",
            "low": "low",
            "ltP": "ltp",
            "ptsC": "chng",
            "per": "pcnt_chng",
            "trdVol": "volume",
            "ntP": "turnover",
            "wkhi": "ftwh",
            "wklo": "ftwl",
            "yPC": "tsfd_pcnt_chng",
            "mPC": "td_pcnt_chng"
        }

        jsonresponse = json.loads(response.text)
        for stock in jsonresponse["data"]:
            item = NSEItem()
            
            for key in stock.keys():
                if remote_local_key_map.get(key):
                    if key == 'symbol':
                        item[remote_local_key_map[key]] = stock[key].replace(',', '')
                    else:
                        item[remote_local_key_map[key]] = float(stock[key].replace(',', ''))
            
            yield item
