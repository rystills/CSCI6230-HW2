from main import generate_nonce, nonceSubtract, diffieHellman, encoder, decoder
import sympy, random, sys
try: import simplejson as json
except ImportError: import json
sys.path.insert(0, 'DES/'); import DES
import socket

def main():
    TCP_IP = '127.0.0.1'
    SERV_PORT = 5005
    BOB_PORT = 5004
    BUFFER_SIZE = 4096
    
    #connect to KDC to establish bobKey
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, SERV_PORT))
    bob = "Bob"
    s.send(bob.encode("utf-8"))
    bobKey = diffieHellman(s,BUFFER_SIZE, False)
    s.close()
    bobNonce = generate_nonce()
    bobNoncePrime = generate_nonce()
    
    #prepare for a connection from Alice
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, BOB_PORT))
    s.listen(1)
    conn, addr = s.accept()
    received = conn.recv(BUFFER_SIZE).decode("utf-8")
    while (True):
        print(received)
    
    '''
    #2. Bob responds with a nonce encrypted under his key with the Server
    msg = [alice,bobNoncePrime]
    encryptedMsg = DES.encrypt(DES.tobits(encoder.encode(msg)),bobKey)
    #send encryptedMsg to alice
    
    #6. Bob sends Alice a nonce encrypted under K_AB to show that he has the key.
    decryptedAliceMsg = DES.frombits(DES.decrypt(toBob,bobKey))
    decryptedAlice = decoder.decode(decryptedAliceMsg)
    bobKab = decryptedAlice[2]
    newMsg = [bobNonce]
    encryptedNewMsg = DES.encrypt(DES.tobits(encoder.encode(newMsg)),bobKab)
    #send encryptedNewMsg to Alice
    
    #8. Bob see's that Alice's computation was correct. Hurray, we're ready to chat!
    decryptedAliceMsg = DES.frombits(DES.decrypt(encryptedNewMsg,bobKab))
    decryptedAlice = decoder.decode(decryptedAliceMsg)
    if (decryptedAlice[0] == nonceSubtract(bobNonce)):
        print("Success!")
    else:
        print("Error: Did not receive Bob Nonce - 1 from Alice")'''

if __name__ == "__main__":
    main()