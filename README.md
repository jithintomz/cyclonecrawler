# cyclonecrawler
Crawl realtime cyclone data from http://rammb.cira.colostate.edu/products/tc_realtime/index.asp

BasicUsage
------------

docker compose up -d

docker run -i -t {image_name} /bin/bash

python -m unittest cyclonrcrawler/tests.py ##runs tests

python core.py ##starts crawling
