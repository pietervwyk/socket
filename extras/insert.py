from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Float, Integer, Column, DateTime
import datetime

engine = create_engine("postgresql://zlqcntsofqygzm:e59a3a6cf6a27c504fe282183ada49b1686e36ff7afacb77c854386a5bd66ac5@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/db7dqloivpuvco", echo=True)
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

new_row = SensorModel(timestamp=str(datetime.datetime.now()), wind=1.0, temperature=5.0, humidity=0, uv=2.0)
session.add(new_row)
session.commit()
