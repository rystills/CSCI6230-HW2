'''
Created on Oct 10, 2018

@author: Ryan
'''
import numpy
def main():
    #select polynomials
    #a = numpy.poly1d([1,0,0,0,0,0,0])
    a = numpy.poly1d([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    b = numpy.poly1d([1,0,0,1,1])
    
    #initial result
    res = numpy.polydiv(a,b)[1]
    print(res)
    
    #apply Galois field GF(2)
    for i in range(len(res),-1,-1):
        res[i] = abs(res[i]%2)
    print(res)
    
if __name__ == "__main__":
    main()