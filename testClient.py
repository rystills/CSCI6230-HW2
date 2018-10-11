import socket

def main():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    MESSAGE = "Hello, World!"
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE.encode('utf-8'))
    data = s.recv(BUFFER_SIZE).decode('utf-8')
    s.close()
    
    print("client received data:", data)
    
if __name__ == "__main__":
    main()