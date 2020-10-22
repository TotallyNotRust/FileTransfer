import socket
import tqdm
import os
from listbox import *


if input("yes?: ") in "yes":
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 4096 

    host, port = input("Give ip adress and port (0.0.0.0:0000): ").split(":")
    filenames = init()
    filesizes = [os.path.getsize(filename) for filename in filenames]
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, int(port)))
    print("[+] Connected.")
    for filename, filesize in [filenames, filesizes]:
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            for _ in progress:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))
    s.close()
else:
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5001
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    while True:
            s.listen(5)
            print(f"[*] Listening as {socket.gethostbyname(socket.gethostname())}:{SERVER_PORT}")
            client_socket, address = s.accept() 
            print(f"[+] {address} is connected.")
            received = client_socket.recv(BUFFER_SIZE).decode()
            filename, filesize = received.split(SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open('5.txt', "wb") as f:
                for _ in progress:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:    
                        break
                    f.write(bytes_read)
                    progress.update(len(bytes_read))

    client_socket.close()
    s.close()