### Sider that runs the app###
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from cyclonecrawler.items import CyclonecrawlerItem
from cyclonecrawler import utils
from datetime import datetime

class CycloneSpider(CrawlSpider):
    
    name = "active_cyclones"
    start_urls = ['http://rammb.cira.colostate.edu/products/tc_realtime/index.asp']
    rules = (
        Rule(LinkExtractor(allow=(r'http://rammb.cira.colostate.edu/products/tc_realtime/storm.asp\?storm_identifier*')), 
            callback='parse_item'),
        )

    def __init__(self, *args, **kwargs):
        super(CycloneSpider, self).__init__(*args, **kwargs)
        self.log = utils.get_logger("base")

    def parse_item(self,response):
        self.log.info("parsing {}".format(response.url))
        item = CyclonecrawlerItem()
        item['url'] = response.url
        item['identifier'] = response.url.split('storm_identifier=')[1]
        item['name'] = response.css('h2::text').extract_first()
        item['forecasts'] = []
        item['history'] = []
        reference_time = response.css('div.text_product_wrapper > h4::text').extract_first()
        if reference_time:
            item["forecast_time"] = reference_time.split(":")[1][1:]
            item["forecast_time"] = datetime.strptime(item["forecast_time"],'%Y%m%d%H%M')
        else:
            item["forecast_time"] = datetime.now()
        for index,row in enumerate(response.css('div.text_product_wrapper > table:nth-of-type(1) > tr')):
            if index!=0:
                forecast = []
                for col in row.css('td::text'):
                    forecast.append(col.extract())
                item['forecasts'].append(forecast)
        for index,row in enumerate(response.css('div.text_product_wrapper > table:nth-of-type(2) > tr')):
            if index!=0:
                history = []
                for col in row.css('td::text'):
                    history.append(col.extract())
                item['history'].append(history)
        return item