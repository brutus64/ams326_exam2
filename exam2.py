import numpy as np
import random
def naive(A,B,n):
    C = np.zeros((n,n)) #n by n 0 matrix
    #loop through row of array * col of b
    flops = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                #i,j represent the element position and we are using k to loop through the row values of A and col values of B
                C[i][j] += A[i][k] * B[k][j]
                flops += 2
                # print("added ", k)
    
    # print(C)
    return C, flops
def strassen():
    pass
def matrix_mult(n):
    #Set up A matrix NxN uniform random -1,1
    A = []
    B = []
    for _ in range(n):
        subarr, subarr2 = [], []
        #generates uniform value between -2 and 2 for both A and B
        for _ in range(n):
            subarr.append(random.uniform(-2,2))
            subarr2.append(random.uniform(-2,2))
        A.append(subarr)
        B.append(subarr2)
    A = np.array(A)
    B = np.array(B) 
    
    print("original matrix A:")
    print(A)
    print("original matrix B:")
    print(B)
    
    #get the results and print them out
    res, flop1 = naive(A,B,n)
    print("NAIVE FLOP:", flop1)
    print("NAIVE RESULT:", res)
    res2, flop2 = strassen(A,B,2)
    print("STRASSEN FLOP:", flop2)
    print("STRASSEN RESULT:",res2)
    
def split_quadrant(matrix):    
    n = len(matrix)
    mid = n // 2
    #1st quadrant, 2nd quadrant, 3rd quadrant, 4th quadrant
    #:mid = 1st half (end at midpoint) mid: = 2nd half (starting from midpoint)
    return matrix[:mid, :mid],  matrix[:mid, mid:], matrix[mid:, :mid], matrix[mid:, mid:]

def strassen(A,B,level):
    #need to split quadrant twice
    n = len(A)
    #just naive way of matrix multiplication once level is done
    if level == 0:
        return naive(A,B,n)
    
    #function splits into q1,q2,q3,q4
    #since we are using 2 levels, when strassen is called again at level 1, it splits it again
    a11, a12, a21, a22 = split_quadrant(A)
    b11, b12, b21, b22 = split_quadrant(B)
    
    #recursively split until level = 0 to then calculate it the naive way, so we subtract 1 from the level each time, only comes back when both levels are done
    M1, flop1 = strassen(a11 + a22, b11 + b22, level - 1)
    M2, flop2 = strassen(a21 + a22, b11, level - 1)
    M3, flop3 = strassen(a11, b12 - b22, level - 1)
    M4, flop4 = strassen(a22, b21 - b11, level - 1)
    M5, flop5 = strassen(a11 + a12, b22, level - 1)
    M6, flop6 = strassen(a21 - a11, b11 + b12, level - 1)
    M7, flop7 = strassen(a12 - a22, b21 + b22, level - 1)
    
    #results are all returned from recursive calls, so we can start creating the matrix quadrants
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6
    #3,1,1,3 for c11,c12,c21,c22
    flops = flop1+flop2+flop3+flop4+flop5+flop6+flop7+3+1+1+3
    #C11 and C12 are horizontally combined since its q1 and q2
    top_half = np.hstack((C11, C12))
    #C21 C22 horizontally combined since its q3 and q4
    bottom_half = np.hstack((C21,C22))
    #then finally they are vertically combined
    return np.vstack((top_half, bottom_half)), flops
    
if __name__ == '__main__':
    matrix_mult(2**10)
