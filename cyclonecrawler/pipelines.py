# -*- coding: utf-8 -*-
### Processes items parsed by spider ###
from . import utils

class CyclonecrawlerPipeline(object):
    
    def __init__(self):
        self.items = []
    
    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self,spider):
        utils.save_crawled_items(self.items)

