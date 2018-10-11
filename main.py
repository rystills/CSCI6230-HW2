import sympy, random, sys
try: import simplejson as json
except ImportError: import json
sys.path.insert(0, 'DES/'); import DES

x = sympy.Symbol('x')
encoder = json.JSONEncoder()
decoder = json.JSONDecoder()

BUFFER_SIZE = 4096

"""
map the polynomial res to GF(2)
@param res: the polynomial to map to GF(2)
returns the polynomial res mapped to GF(2)
"""
def GF(res):
    coeffs = res.all_coeffs()
    return sympy.Poly.from_list([abs(coeffs[i]%2) for i in range(len(coeffs))],gens=x)

"""
Generate pseudorandom number.
"""
def generate_nonce(length=8):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

"""
subtract one from the specified nonce
@param nonce: the nonce to subtract from
"""
def nonceSubtract(nonce):
    smallestOne = nonce.rfind('1')
    if (smallestOne == -1):
        return "1" * len(nonce)
    return nonce[:smallestOne] + '0' + nonce[smallestOne+1:]

"""
receive a message from the specified connection, and strip byte encoding and stringification
@param conn: the connection on which to receive a message
"""
def receiveMessage(conn):
    received = conn.recv(BUFFER_SIZE)
    print("received data:",received)
    return decoder.decode(received.decode("utf-8"))

"""
send a message to the specified connection, adding byte encoding and stringification
@param conn: the connection on which to send a message
@param msg: the message to send
"""
def sendMessage(conn,msg):
    sent = encoder.encode(msg).encode("utf-8")
    print("sent data:",sent)
    conn.send(sent)

"""
diffie-hellman implementation
@param conn: the socket connection to use for Ya/Yb exchange
@param BUFFER_SIZE: the size of the network buffer to employ
@param meFirst: whether I should receive Yb before sending Ya during the exchange or vice versa
"""
def diffieHellman(conn, meFirst = True):
    #hard-coded constants (you can change these if you want, but primpoly should stay degree 10)
    primPoly = sympy.Poly.from_list([1,0,0,0,0,0,0,0,0,1,1],gens=x)
    G = 100
    
    #randomly choose A and B -> construct polynomials
    Arand = random.randint(1,G)
    A = sympy.Poly.from_list([1]+[0]*Arand,gens=x)
    
    #apply modulo -> map to Galois field GF(2)
    Ya = GF((sympy.div(A,primPoly,domain='QQ')[1]))
    
    #exchange Ya and Yb
    #JSON won't encode a coefficient list from sympy for some reason, so manually reconstruct Yb
    if (meFirst):
        Yb = conn.recv(BUFFER_SIZE).decode('utf-8')
        Yb = sympy.Poly.from_list([int(Yb[i]) for i in range(2,len(Yb)-2,3)],gens=x)
        conn.send(encoder.encode(Ya.all_coeffs().__str__()).encode("utf-8"))
    else:
        conn.send(encoder.encode(Ya.all_coeffs().__str__()).encode("utf-8"))
        Yb = conn.recv(BUFFER_SIZE).decode('utf-8')
        Yb = sympy.Poly.from_list([int(Yb[i]) for i in range(2,len(Yb)-2,3)],gens=x)
        
    #apply modulo -> map to Galois field GF(2)
    Yba = GF(sympy.div(GF(Yb**Arand),primPoly,domain='QQ')[1])
    
    #convert poly to key 
    key = Yba.all_coeffs()
    key = [0] * (10-len(key)) + key
    
    return key
    
def main():
    pass

    
if __name__ == "__main__":
    main()