# Ryan Stillings Cryptography and Network Security I - Homework Assignment 2  
## Dependencies:  
-sympy (pip install sympy)  
## Assumptions:  
Although I mostly followed the Needham–Schroeder and Diffie–Hellman algorithms by the book, I did have to make a few assumptions. One major assumption was in my implementation of diffie-hellman. The output of my diffie-hellman was a polynomial mapped to GF(2). However, I needed to convert that output into a 10-bit key for my DES implementation. To achieve this, I made the primitive polynomial degree 10, and treated the coefficients (each 0 or 1 due to GF(2)) as a list of bits to serve as my 10-bit key.  
An additional assumption was made in my sample client code. I decided each client should know the name of the other client from the start, since otherwise they would not be trying to connect to each other to initiate a conversation in the first place.  
## Setup:  
As with the last hw, I chose to write this assignment in Python due to its ease of use, allowing me to focus on the algorithms at a high level. There are 4 new files this time; main.py, which contains the diffie-hellman function, a number of helper functions, and a main function which automatically starts the server and clients. Alice.py and Bob.py, who run Alice and Bob's code respectively. And finally KDC.py, who acts as the key distribution center.  
All networking this time is handled with TCP, with the first 4 bytes of each message containing the message length, allowing for arbitrarily large messages to be sent and received successfully.  Initially, Bob and Alice each connect to KDC, where both sides run diffie-hellman to obtain a key. Alice then communicates back and forth with Bob and the server to obtain Kab and distribute it to Bob via Needham-Schroeder. Once the keys are established and the nonce is verified, Alice and Bob are free to securely chat with each other as much as they like.  
## Algebraic Constructions / Implementation:  
An key component of diffie-hellman is performing polynomial math. At first I tried using numpy for this task, but it caused inconsistent errors due to floating point rounding during the exponentiation. Eventually, I settled on the external library sympy, which allowed me to perform polynomial math with arbitrary precision. Throughout this polynomial math I also needed to make sure I was staying with the Galois Field GF(2). To achieve this, I wrote a small method GF which maps each coefficient in a specified polynomial to GF(2), and ran that function after each polynomial operation.  
As before, DES takes in bit arrays for the data and key, each in the form of a list of ints. For passing messages via sockets, I used JSON to stringify and destringify the raw message data, and then encoded the result into a utf-8 bytestring so that it would be supported by Python. For nonces, I used a randomly generated 8-char array, with each char being either 0 or 1. Alice and Bob later test their encryption key by subtracting one from the smallest bit in Bob's nonce.  Finally, to ensure that my implementation of N-S is safe against replay attacks, I had Bob create a second nonce prime, and include that in his message to Alice.
