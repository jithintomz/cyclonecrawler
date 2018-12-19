from .database.connection import db
from .database.models import *
from datetime import datetime,timedelta
import time
import logging


def save_crawled_items(items):
	identifiers = [item['identifier'] for item in items]
	mark_as_active = db.query(Cyclone).filter(Cyclone.identifier.in_(identifiers),
		Cyclone.is_active == 2).update({"is_active" : 1},synchronize_session=False) # mark previously inactive cyclones as active
	marked_as_inactive = db.query(Cyclone).filter(~Cyclone.identifier.in_(identifiers),
		Cyclone.is_active == 1).update({"is_active" : 2},synchronize_session=False)
	current = [r for r, in db.query(Cyclone.identifier).filter_by(is_active = 1)] #mark previously active cyclones as inactive
	to_be_created = set(identifiers)- set(current)
	to_be_updated = set(identifiers).intersection(set(current)) #identifies the forecasts and history data to be replaced
	cyclones_to_be_updated = [id for id, in db.query(Cyclone.id).filter(Cyclone.identifier.in_(to_be_updated))]
	db.query(Forecast).filter(Forecast.cyclone_id.in_(cyclones_to_be_updated)).delete(synchronize_session=False)
	db.query(History).filter(History.cyclone_id.in_(cyclones_to_be_updated)).delete(synchronize_session=False)
	for item in items:
		if item['identifier'] in to_be_created:
			cyclone_obj = Cyclone(url = item['url'],identifier = item['identifier'],name = item['name'])
			db.add(cyclone_obj)
		else:
			cyclone_obj = db.query(Cyclone).filter_by(identifier = item['identifier'],is_active = 1).scalar()
		for forecast in item['forecasts']:
			cyclone_obj.forecasts.append(Forecast(forecast_time = item["forecast_time"],
				forecast_hour = forecast[0],latitude = forecast[1],longitude = forecast[2],intensity = forecast[3],
				cyclone_id = cyclone_obj.identifier))
		for history in item['history']:
			cyclone_obj.history.append(History(time = datetime.strptime(history[0],'%Y%m%d%H%M'),latitude = history[1],
				longitude = history[2],intensity = history[3],
				cyclone_id = cyclone_obj.identifier))
	db.commit()
	return cyclone_obj


def get_logger(name):
    log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        filename='dev.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)