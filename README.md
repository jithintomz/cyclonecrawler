# cyclonecrawler
Crawl realtime cyclone data from http://rammb.cira.colostate.edu/products/tc_realtime/index.asp

BasicUsage
------------

    docker compose up -d

    docker run -i -t {image_name} /bin/bash

    python -m unittest cyclonercrawler/tests.py ##runs tests

    python core.py ##starts crawling
    
Access Crawled data with sqlalchmey
    
    python

    >>> from cyclonecrawler.database.connection import *
    
    >>> from cyclonecrawler.database.models import *
    
    >>>>  db.query(Cyclone).filter_by(id = 1).one().forecasts
    
    >>>> db.query(Cyclone).filter_by(id = 1).one().history
