#!/usr/bin/python3
from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('asr.yandex.net', 80))
sock.send(b'GET /asr_partial HTTP/1.1\r\nUser-Agent: KeepAliveClient\r\nHost: asr.yandex.net:80\r\nUpgrade: dictation\r\n\r\n')
print(sock.recv(1024))
with open('connection_request.proto', 'rb') as request_protobuf:
    message = request_protobuf.read()

sock.send(hex(len(message))[2:].encode())
sock.send('\r\n'.encode())
sock.send(message)
print(sock.recv(1024))
sock.close()