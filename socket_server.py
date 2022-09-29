import socket
import csv
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Float, Integer, Column, DateTime
import datetime

# HOST = "192.168.137.1"
# HOST = '192.168.0.101'
HOST = "127.0.0.1"
PORT = 65432 

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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
c, address = s.accept()
print(f"Connection from {address} has been established.")

def float_to_str(element):
    try:
        float(element)
        return float(element)
    except ValueError:
        return None

while True:
    client_message_encoded = c.recv(2048)
    if not client_message_encoded:
        break
    client_message = client_message_encoded.decode("utf-8")
    sensors = client_message.split(",")
    print(sensors)
    new_record = SensorModel(
        timestamp=str(datetime.datetime.now()),
        wind=float_to_str(sensors[0]),
        temperature=float_to_str(sensors[1]),
        humidity=float_to_str(sensors[2]),
        uv=float_to_str(sensors[3]))
    print(new_record)
    session.add(new_record)
    session.commit()





print('Socket closed.')