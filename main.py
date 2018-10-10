'''
Created on Oct 10, 2018

@author: Ryan
'''
import numpy,random

def main():
    #hard-coded constants (you can change these if you want)
    primPoly = numpy.poly1d([1,0,0,0,0,0,1,1])
    
    #randomly choose A and B -> construct polynomials
    Arand = random.randint(10,80); Brand = random.randint(10,60)
    A = numpy.poly1d([1]+[0]*Arand); B = numpy.poly1d([1]+[0]*Brand)
    
    #apply modulo -> map to Galois field GF(2)
    GF = lambda res: numpy.poly1d([abs(res[i]%2) for i in range(len(res),-1,-1)]) 
    Ya = GF(numpy.polydiv(A,primPoly)[1]); Yb = GF(numpy.polydiv(B,primPoly)[1]);
    print(Ya)
    
if __name__ == "__main__":
    main()