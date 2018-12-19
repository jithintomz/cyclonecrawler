###run this file to start crawling#########

from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from cyclonecrawler.spiders.cyclone_spider import CycloneSpider

settings = Settings()
settings.set("ITEM_PIPELINES", {'cyclonecrawler.pipelines.CyclonecrawlerPipeline': 100})
process = CrawlerProcess(settings)
process.crawl(CycloneSpider)
process.start()


