import socket
import csv
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine, Float, Integer, Column, DateTime
import datetime
from os.path import exists
import pandas as pd

# SOCKET VARIABLES
# HOST = "192.168.137.1"
HOST = '192.168.0.102'
# HOST = "127.0.0.1"
PORT = 65432 

# ONLINE DATABASE
db_string = "postgresql://hslkxfirbemaoq:01f860338dfa67d43867ed24c0a609e446d635e6ec347cf1d1d101380bfb681a@ec2-52-31-77-218.eu-west-1.compute.amazonaws.com:5432/db58657qkakm5p"
engine = create_engine(db_string, echo=False, poolclass=NullPool)
#  pool_pre_ping=True
Base = declarative_base()
table_name = 'sensor_table'

# LOCALLY STORED DATA, FOR LOADSHEDDING
csv_file_name = 'sensor_data_local.csv'
csv_header = ['timestamp', 'wind', 'temperature', 'humidity', 'uv']

# ONLINE DATABASE SCHEMA
class SensorModel(Base):
    __tablename__ = table_name
    
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

# CREATE SOCKET CONNECTION
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
c, address = s.accept()
print(f"Connection from {address} has been established.")

# ONLINE DATABASE SESSION
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# AUXILLIARY FUNCTIONS
def init_csv():
    csv_exists = exists(f'./{csv_file_name}')
    if (not csv_exists):
        with open(csv_file_name, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)

def float_to_str(element):
    try:
        float(element)
        return float(element)
    except ValueError:
        return None

def is_connected():
    try:
        test_socket = socket.create_connection(("www.google.com", 80))
        if test_socket is not None:
            test_socket.close
        return True
    except OSError:
        pass
    return False

# MAIN LOOP
disconnected_flag = False
while True:
    client_message_encoded = c.recv(2048)
    if not client_message_encoded:
        break
    client_message = client_message_encoded.decode("utf-8")
    
    sensors = client_message.split(",")

    if is_connected():
        print('CONNECTION SUCCESFUL')
        
        if disconnected_flag and exists(f'./{csv_file_name}'):
            df_local_data = pd.read_csv(csv_file_name)
            print(df_local_data.to_string())
            conn = engine.connect()
            sensor_data_list = df_local_data.to_dict(orient='records')
            metadata = sqlalchemy.schema.MetaData(bind=engine)
            table = sqlalchemy.Table(table_name, metadata, autoload=True)
            print(table)
            conn.execute(table.insert(), sensor_data_list)
            session.commit()
            
            f = open(csv_file_name, "w+")
            writer = csv.writer(f)
            writer.writerow(csv_header)
            f.close()
            disconnected_flag = False
        
        new_record = SensorModel(
            timestamp=str(datetime.datetime.now()),
            wind=float_to_str(sensors[0]),
            temperature=float_to_str(sensors[1]),
            humidity=float_to_str(sensors[2]),
            uv=float_to_str(sensors[3])
        )
        
        session.add(new_record)
        session.commit()
    else:
        session.close()
        disconnected_flag = True
        print('FAILED TO CONNECT')
        init_csv()
        with open(csv_file_name, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            csv_data = [
                str(datetime.datetime.now()),
                float_to_str(sensors[0]),
                float_to_str(sensors[1]),
                float_to_str(sensors[2]),
                float_to_str(sensors[3])
            ]
            
            print(csv_data)
            writer.writerow(csv_data)

print('Socket closed.')


































