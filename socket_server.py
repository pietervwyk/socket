import socket

HOST = "192.168.137.1"
# HOST = "127.0.0.1"
PORT = 65432 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
c, address = s.accept()
print(f"Connection from {address} has been established.")

while True:
    # Keep reading while the client is writing.
    data = c.recv(2048)
    if not data:
        # Client is done with sending.
        break
    print(data.decode("utf-8"))

