import socket
import csv
import datetime
from os.path import exists

HOST = "192.168.137.1"
# HOST = "127.0.0.1"
PORT = 65432 

csv_file_name = 'sensor_data.csv'
csv_header = ['time', 'uv', 'temperature', 'humidity']

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
c, address = s.accept()
print(f"Connection from {address} has been established.")

# ensure CSV is configured
csv_exists = exists(f'./{csv_file_name}')
if (not csv_exists):
    with open(csv_file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)

# append to end of the CSV file
with open(csv_file_name, 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    while True:
        # keep reading while client is writing
        client_message_encoded = c.recv(2048)
        if not client_message_encoded:
            # when client is done writing
            break
        client_message = client_message_encoded.decode("utf-8")
        csv_data = [str(datetime.datetime.now()), int(client_message), 0, 0]
        print(csv_data)
        writer.writerow(csv_data)


print('Socket closed.')