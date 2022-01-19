from django.test import TestCase
from django.conf import settings
from django.test.runner import DiscoverRunner

class NoSQLTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass
    def teardown_databases(self, old_config, **kwargs):
        pass

class NoSQLTestCase(TestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass

# Create your tests here.
from mongoengine import connect, disconnect
from mongoengine.queryset.visitor import Q
import urllib

from feed.models import NiftyFifty

class NSETestCase(NoSQLTestCase):
    scraped_live_nse_data = []

    @classmethod
    def setUpClass(self):
        connect(settings.DBNAME, host=settings.MONGODB_DATABASE_HOST, alias='testdb')
        with urllib.request.urlopen('https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json') as response:
            jsonresponse = response.read()
        # print(jsonresponse)
        self.scraped_live_nse_data = json.loads(jsonresponse)
        # self.scraped_live_nse_data = {}

    @classmethod
    def tearDownClass(self):
       disconnect(alias='testdb')

    def test_scraped_data_upto_date(self):
        """Scraped data in mongo is matching with live"""
        
        queryset = list(NiftyFifty.objects.all())

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

        self.assertEqual(len(queryset), len(self.scraped_live_nse_data.get("data", [])))

        for stock, row in self.scraped_live_nse_data["data"], queryset:
            for key in stock.keys():
                if remote_local_key_map.get(key):
                    self.assertEqual(str(row[remote_local_key_map[key]]), str(stock[key].replace(',', '')))
    
    def test_api_response_with_filters(self):
        """API response with filters is correct"""
        
        queryset = NiftyFifty.objects.all()
        search_keyword = 'tata'
        columns = 'symbol,high,low'.split(',')
        order = '-high'
        
        queryset = queryset.filter(Q(symbol__icontains=search_keyword))
        queryset = queryset.only(*columns)
        queryset = queryset.order_by(order)

        self.assertEqual(list(queryset), [{
                "id": "61e17c043d994d77ddb85dd4",
                "symbol": "TATASTEEL",
                "open": None,
                "high": "1226.3",
                "low": "1206.1",
                "ltp": None,
                "chng": None,
                "pcnt_chng": None,
                "volume": None,
                "turnover": None,
                "ftwh": None,
                "ftwl": None,
                "tsfd_pcnt_chng": None,
                "td_pcnt_chng": None
            },
            {
                "id": "61e17c043d994d77ddb85db4",
                "symbol": "TATACONSUM",
                "open": None,
                "high": "777.0",
                "low": "727.0",
                "ltp": None,
                "chng": None,
                "pcnt_chng": None,
                "volume": None,
                "turnover": None,
                "ftwh": None,
                "ftwl": None,
                "tsfd_pcnt_chng": None,
                "td_pcnt_chng": None
            },
            {
                "id": "61e7f97a80397d4117425c3d",
                "symbol": "TATAMOTORS",
                "open": None,
                "high": "522.2",
                "low": "504.8",
                "ltp": None,
                "chng": None,
                "pcnt_chng": None,
                "volume": None,
                "turnover": None,
                "ftwh": None,
                "ftwl": None,
                "tsfd_pcnt_chng": None,
                "td_pcnt_chng": None
            }
        ]) # or lambda filter scraped_live_nse_data based on search_keyword, columns, order