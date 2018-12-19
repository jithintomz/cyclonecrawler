##database models########

from sqlalchemy import Column, String, Integer, BigInteger, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .connection import Base


class Cyclone(Base):
    
    __tablename__ = 'cyclone'

    id = Column(Integer, primary_key=True)
    identifier = Column(String(200))
    name = Column(String(200))
    url = Column(String(500))
    date = Column(DateTime,default = datetime.now)
    is_active = Column(Integer,default = 1) #{ 1:active,2:inactive }
    forecasts = relationship("Forecast",cascade="all,delete",backref="cyclone")
    history = relationship("History",cascade="all,delete",backref="cyclone")


    def __init__(self, id=None, name=None, url=None, date=None,identifier = None):
        self.id = id
        self.name = name
        self.url = url
        self.date = date
        self.identifier = identifier

    def __repr__(self):
        return "<Cyclone: id='%d', name='%s', url='%s', date='%s'>" % (self.identifier, self.name, self.url, self.date)


class Forecast(Base):
    
    __tablename__ = 'forecast'
    
    id = Column(Integer, primary_key=True)
    forecast_time = Column(DateTime)
    latitude = Column(String(50))
    longitude = Column(String(50))
    intensity = Column(Integer)
    forecast_hour = Column(BigInteger)
    cyclone_id = Column(Integer, ForeignKey("cyclone.id",ondelete='CASCADE'))

    def __init__(self, id=None, latitude=None, longitude=None, forecast_time=None,intensity = None,cyclone_id = None,forecast_hour = None):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.forecast_time = forecast_time
        self.intensity = intensity
        self.forecast_hour = forecast_hour
        self.cyclone_id = cyclone_id

    def __repr__(self):
        return "<Cyclone: id='%d', latitude='%s', longitude='%s', time='%s'>" % (self.id, self.latitude, self.longitude, self.time)



class History(Base):
    
    __tablename__ = 'history'
    
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    latitude = Column(String(50))
    longitude = Column(String(50))
    intensity = Column(Integer)
    cyclone_id = Column(Integer, ForeignKey("cyclone.id",ondelete='CASCADE'))

    def __init__(self, id=None, latitude=None, longitude=None, time=None,intensity = None,cyclone_id = None):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.time = time
        self.intensity = intensity
        self.cyclone_id = cyclone_id

    def __repr__(self):
        return "<Cyclone: id='%d', latitude='%s', longitude='%s', time='%s'>" % (self.id, self.latitude, self.longitude, self.time)