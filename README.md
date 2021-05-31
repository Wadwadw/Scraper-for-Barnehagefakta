# Scraper-for-Barnehagefakta
This scraper get information from site https://www.barnehagefakta.no with help framework Scrapy
## Running all the stuff
1. Clone repo: `git clone https://github.com/Wadwadw/Scraper-for-Barnehagefakta.git`
2. Create virtualenv, for example: `python3 -m venv venv` or `virtualenv -p python3 venv`
3. Activate it `source venv/bin/activate`
4. Install all the packages `pip install -r requirements.txt`
5. Start scraper script `scrapy crawl scrape -o results.csv`
