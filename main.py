'''
Created on Oct 10, 2018

@author: Ryan
'''
from numpy import poly1d
from numpy.polynomial.polynomial import polypow
from numpy import polydiv
import random

def GF(res):
    return poly1d([abs(res[i]%2) for i in range(res.order,-1,-1)])

def main():
    #hard-coded constants (you can change these if you want)
    primPoly = poly1d([1,0,0,0,0,0,1,1])
    G = 100
    
    #randomly choose A and B -> construct polynomials
    #Arand = random.randint(1,G); Brand = random.randint(1,G)
    Arand = 56
    Brand = 18
    A = poly1d([1]+[0]*Arand)
    B = poly1d([1]+[0]*Brand)
    
    #apply modulo -> map to Galois field GF(2)
    Ya = GF((A/primPoly)[1])
    Yb = GF((B/primPoly)[1])
    
    print(Ya,'\n',Yb)
    
    #exchange Ya and Yb : apply modulo -> map to Galois field GF(2)
    Yba = GF(polydiv(GF(poly1d(Yb**Arand)),primPoly)[1])
    Yab = GF(polydiv(GF(poly1d(Ya**Brand)),primPoly)[1])
    
    print(Yba,'\n',Yab)
    
if __name__ == "__main__":
    main()