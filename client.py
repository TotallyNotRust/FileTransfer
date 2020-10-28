import socket
import tqdm
import os
import time
from clientErrors import *
from listbox import *

if (x:= input("Send or receive?: ").lower()) in "send":
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 

    host, port = input("Give ip adress and port (0.0.0.0:0000): ").split(":")
    filenames = init("Choose files >:(")
    filesizes = [os.path.getsize(filename) for filename in filenames if filename]
    print(f"[+] Connecting to {host}:{port}")
    try:
        for filename, filesize in zip(filenames, filesizes):
            s = socket.socket()
            s.connect((host, int(port)))
            print("[+] Connected.")
            print(filename)
            filetype = "." + filename.split(".")[-1]
            s.send(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{filetype}".encode())

            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            try:
                f = open(filename, "rb")
            except Exception as e:
                print(e)
            for _ in progress:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))
            s.close()
    except Exception as e:
        print("Server decided so close... :)")
        print(e)

elif x in "receive":
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5001
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    while True: 
        try:
            s.listen(5)
            print(f"[*] Listening as {socket.gethostbyname(socket.gethostname())}:{SERVER_PORT}")
            client_socket, address = s.accept() 
            print(f"[+] {address} is connected.")
            received = client_socket.recv(BUFFER_SIZE).decode()
            client_socket.send(b"l")
            filename, filesize, filetype = received.split(SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}.{filetype}", unit="B", unit_scale=True, unit_divisor=1024)
            p1 = filename.split(".")[0]
            with open(f"{p1} (TRANSFERED){filetype}", "wb") as f:
                for _ in progress:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:  
                        break
                    f.write(bytes_read)
                    progress.update(len(bytes_read))
            
            client_socket.close()
        except Exception as e:
            print("Client did something")
            print(e)
    s.close()
else:
    try:
        raise InputError("Uknown input")
    except Exception as e:
        print(e)