import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("37.139.14.163", 9999))
s.send("Малахов Михаил".encode())
s.send(s.recv(1024))

