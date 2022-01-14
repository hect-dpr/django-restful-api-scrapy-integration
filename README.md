# scrape-nse

NiftyFifty List

Scrapy script to scrape data from NSE India, store in mongodb.
e.g. http://127.0.0.1:8000/api/nse/?q=TATA&c=symbol,high&o=+high
Q parameter is used to search icontains for specific stock symbols(names),
C parameter is comma separated(optional) columns whose value to be shown
O parameter is + ascending / - descending and column name for ordering
Based on the parameter values stated on the url will scan the mongodb table

Rest API: http://127.0.0.1:8000/api/nse/
Basic Frontend UI: http://127.0.0.1:8000/

Brief Instructions:
Install mongodb (credentials in settings point to niftyfifty DB, niftyfifty table), python, run `pip install -r requirements.txt`.
Run `python manage.py runserver` - django server for API, basic UI.
Scrape by `cd scrape_portal`, running `scrapy crawl nse`, can make a daemon for periodicity
