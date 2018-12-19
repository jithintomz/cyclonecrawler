### Unit tests ###
from . import utils
from .database.connection import db
from .database.models import *
import unittest
from cyclonecrawler.spiders.cyclone_spider import CycloneSpider
import os
from scrapy.http import Response, Request ,TextResponse
import datetime

logger = utils.get_logger("base")

class DbSaveTestCase(unittest.TestCase):

    def setUp(self):
        self.items = [{'forecasts': [['201812150000', '-9.4', '57.7', '20'],
               ['201812141800', '-8.3', '57', '20'],
               ['201812141200', '-8.5', '56.5', '15']],
             'history': [],
             'forecast_time' : datetime.datetime.now(),
             'identifier': 'SH022019',
             'name': 'SH922019 - INVEST',
             'url': 'http://rammb.cira.colostate.edu/products/tc_realtime/storm.asp?storm_identifier=SH022019'}]
        self.item_id = None

    def test_items_save(self):
        cyclone_obj = utils.save_crawled_items(self.items)
        try:
            assert cyclone_obj.id != None
            self.item_id = cyclone_obj.id
        except AssertionError:
            logger.error("Items not saved to db")
        except Exception as e:
            logger.error(e)

    def tearDown(self):
        if self.item_id != None:
            db.query(Cyclone).filter(Cyclone.id == self.item_id).delete(synchronize_session=False)
    

    """Test for parser of cyclone spider"""
        

def fake_response_from_file(file_name, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = 'http://rammb.cira.colostate.edu/products/tc_realtime/'

    request = Request(url=url)
    if not file_name[0] == '/':
        responses_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(responses_dir, file_name)
    else:
        file_path = file_name

    file_content = open(file_path, 'rb').read()

    response = TextResponse(url=url,
        request=request,
        body=file_content)
    #response.encoding = 'utf-8'
    return response


class SpiderParserTestCase(unittest.TestCase):
    
    """Test for parser of cyclone spider"""
    
    def setUp(self):
        self.spider = CycloneSpider()
        self.expected_item = {'forecasts': [['201812150000', '-9.4', '57.7', '20'],
               ['201812141800', '-8.3', '57', '20'],
               ['201812141200', '-8.5', '56.5', '15']],
             'history': [],
             'identifier': 'SH022019',
             'name': 'SH922019 - INVEST',
             'url': 'http://rammb.cira.colostate.edu/products/tc_realtime/storm.asp?storm_identifier=SH022019'}

    def test_parse(self):
        results = self.spider.parse_item(fake_response_from_file('testtemplates/sample.html',
            "http://rammb.cira.colostate.edu/products/tc_realtime/storm.asp?storm_identifier=SH022019"))
        del results['forecast_time']
        assert results['forecasts'] == self.expected_item['forecasts']