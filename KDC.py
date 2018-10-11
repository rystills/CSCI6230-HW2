from main import generate_nonce, nonceSubtract, diffieHellman, encoder, decoder, sendMessage, receiveMessage
import sympy, random, sys
try: import simplejson as json
except ImportError: import json
sys.path.insert(0, 'DES/'); import DES
import socket

def main():
    TCP_IP = '127.0.0.1'
    SERV_PORT = 5005
    BUFFER_SIZE = 4096
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, SERV_PORT))
    s.listen(1)
    names = []
    keys = []
    for i in range(2):   
        print("Awaiting {0} connection to establish diffie-hellman key".format("first" if i == 0 else "second"))
        conn, addr = s.accept()
        names.append(conn.recv(BUFFER_SIZE).decode("utf-8"))
        print("Connected to {0}. Running diffieHellman for initial key.".format(names[i]))
        keys.append(diffieHellman(conn, True))
        print("server key for {0}: {1}".format(names[i],keys[i]))
        if (i == 0):
            #close Bob's connection, but keep Alice open for a bit longer
            conn.close()
    bobKey = keys[0]
    aliceKey = keys[1]

    #generate random session key on the server for alice and bob to communicate
    Kab = [random.randint(0, 9) for _ in range(10)]
    
    #4. The server generates K_AB and sends back to Alice a copy encrypted under K_BS for Alice to forward to Bob and also a copy for Alice. 
    #Since Alice may be requesting keys for several different people, the nonce assures Alice that the message is fresh and that 
    #the server is replying to that particular message and the inclusion of Bob's name tells Alice who she is to share this key with.
    #Note the inclusion of the nonce.
    msg = receiveMessage(conn)
    decryptedBobMsg = DES.frombits(DES.decrypt(msg[3],bobKey))
    decryptedBob = decoder.decode(decryptedBobMsg)
    decryptedBob.append(Kab)
    
    reEncryptedBob = DES.encrypt(DES.tobits(encoder.encode(decryptedBob)),bobKey)
    newMsg = [msg[1],msg[2],Kab,reEncryptedBob]
    encryptedNewMsg = DES.encrypt(DES.tobits(encoder.encode(newMsg)),aliceKey)
    sendMessage(conn, encryptedNewMsg)
    conn.close()
    
if __name__ == "__main__":
    main()