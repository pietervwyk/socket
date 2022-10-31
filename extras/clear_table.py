from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Float, Integer, Column, DateTime
import datetime

engine = create_engine("INSERT_DB_STRING", echo=True)
Base = declarative_base()

class SensorModel(Base):
    __tablename__ = 'sensor_table'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=False), nullable=True)
    wind = Column(Float(), nullable=True)
    temperature = Column(Float(), nullable=True)
    humidity = Column(Float(), nullable=True)
    uv = Column(Float(), nullable=True)
    

    def __init__(self, timestamp, wind, temperature, humidity, uv):
        self.timestamp = timestamp
        self.wind = wind
        self.temperature = temperature
        self.humidity = humidity
        self.uv = uv

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

session.query(SensorModel).delete()
session.commit()
