'''
Created on Jun 20, 2014

@author: ameriPC
'''
from __builtin__ import range
#from aetypes import Range
import copy
from scipy.linalg.decomp_schur import eps
epsilon  = 0.000000001
import math

def minRow(listMatrix, rowIndex):
    
    L = len(listMatrix)
    if L < 1:
        return 0
    
    m = listMatrix[rowIndex][0]
    
    for i in range(1, L):
        if m > listMatrix[rowIndex][i]:
            m = listMatrix[rowIndex][i]
    return m
    

def minCol(listMatrix, colIndex):
    
    L = len(listMatrix)
    if L < 1:
        return 0
    m = listMatrix[0][colIndex]
    
    for i in range(1, L):
        if m > listMatrix[i][colIndex]:
            m = listMatrix[i][colIndex]
    return m
    

def computeMunkerCost(costMatrix):
    #print 'start munker'
    path = Munker(costMatrix)
    #print 'end munker now path'
    cost = 0
    for p in path:
        cost += costMatrix[p[0]][p[1]]
    
    # return path and cost
    return [cost, path] 

def noZeroIn(costMatrix, i,j, stared):
    L = len(costMatrix)
    ret = True
    
    for k in range(0, L):
        if abs(costMatrix[i][k]) <= epsilon:
            if [i,k] in stared: 
                return False
        if abs(costMatrix[k][j]) <= epsilon:
            if [k, j] in stared:
                return False
    
    return ret    

def prime(primed, i,j):
    if not([i,j] in primed):
        primed.append([i, j])    

def unPrime(primed, p):
    if p in primed:
        primed.remove(p)
        
def star(stared, i,j):
    if not([i,j] in stared):
        stared.append([i, j])    

def unStar(stared, s):
    if s in stared:
        stared.remove(s)
              
def cover(covered, col):
    if not col in covered:
        covered.append(col)
        
def unCover(covered, j):
    if j in covered:
        covered.remove(j)
    
def do_step1(costMatrix, stared, coveredCol):
    #coveredCol = []
    for s in stared:
        #print 's=' ,s
        cover(coveredCol, s[1])
        #print 'coverd now ' ,coveredCol
#     print coveredCol
#     print 'end step 1 ------'
#     return coveredCol
#  
def isRowStared(stared, row):
    for s in stared:
        if s[0] == row:
            return [True, s[1]]
    return [False]

def isColStared(stared, col):
    for s in stared:
        if s[1] == col:
            return [True, s[0]]
    return [False]

def isPrimedRow(primed, row):
    for p in primed:
        if p[0] == row:
            return [ True, p[1]]
    return [False]
               
def do_step2(costMatrix, coveredCol, coveredRow, primed, stared):
    L = len (costMatrix)
    unCoveredZero = False
    
#     print coveredCol
#     print coveredRow
#     print primed
#     print stared
#     
    for row in costMatrix:
        nrow = []
        for c in row:
            if c == 0 :
                nrow.append(0)
            else:
                nrow.append(1)
#         print nrow
     
    for i in range(0, L):
        for j in range(0, L):
            if abs(costMatrix[i][j]) <= epsilon:
                if not(j in coveredCol) and not(i in coveredRow):
                    unCoveredZero = True
                    prime(primed, i, j)
                    
                    isStared = isRowStared(stared, i)
                    if isStared[0] == False:
                        # step 3
                        return [3, [i,j]]
                    else: 
                        cover(coveredRow, i)
                        unCover(coveredCol, j)
                        return [2]
    #print unCoveredZero    
          
                    
    if not unCoveredZero:
        # find smallest un covered goto step 4
        eMin = []
        for i in range(0, L):
            if i in coveredRow:
                continue
            for j in range(0, L):
                if j in coveredCol:
                    continue
#                 print i, j, costMatrix[i][j]
#                 print eMin
                if len(eMin) == 0:
                    eMin = [costMatrix[i][j]]
                    
                elif eMin[0] > costMatrix[i][j]:
                    eMin = [costMatrix[i][j]]
#                 print eMin 
                            
    return [4, eMin]                  
                    

def do_step4(costMatrix, coveredCol, coveredRow, primed, stared, eMin):
    L = len(costMatrix)
     
    for i in coveredRow:
        for j in range(0, L):
            costMatrix[i][j] += eMin[0]
            
    for j in range(0, L):
        if j in coveredCol:
            continue
        for i in range(0, L):
            costMatrix[i][j] -= eMin[0]
        
    
    return 2

def do_step3(costMatrix, coveredCol, coveredRow, primed, stared, Z0):
    S = [Z0]
    
    while(True):
        colStared = isColStared(stared, Z0[1])
        if colStared[0] == False:
            break
        
        Z1 = [colStared[1] ,Z0[1]]
        S.append(Z1)
        
        primedZ0 = isPrimedRow(primed, Z1[0])
        if primedZ0[0] == True:
            Z0 = [Z1[0], primedZ0[1]]
            S.append(Z0)
        else:
            break
     
    # un star each sttared zero
    for s in S:
        if s in stared:
            unStar(stared, s)
        if s in primed:
            star(stared, s[0], s[1])
     
    # erase alll primes
    for p in primed:
        unPrime(primed, p)       
    #uncover all
    for col in coveredCol:
        unCover(coveredCol, col)
    for row in coveredRow:
        unCover(coveredRow, row)
         
    return 1                        

def Munker(costMatrix_in):
    costMatrix =copy.deepcopy(costMatrix_in)
    
    L = len(costMatrix)
    path = []
    
    stared = []
    coveredCol = []
    coveredRow = []
    primed = []
    
    #print costMatrix
    
    for i in range( 0, L):
        minRowCost =  minRow(costMatrix, i)
        for j in range(0 , L):
            costMatrix[i][j] -= minRowCost 
       
    
   
    for i in range(0, L):
        minColCost =  minCol(costMatrix, i)
        for j in range(0 , L):
            costMatrix[j][i] -= minColCost
    
       
    
    #print costMatrix_in
        
    
    for i in range(0, L):
        for j in range(0 , L):
            if abs(costMatrix[i][j]) <= epsilon:
                if noZeroIn(costMatrix, i,j, stared):
                    star(stared, i,j)
#     print 'first stared ', stared
                   
    #print stared 
    step = 1
    eMin = 0
    Z0 = []
    while step != 'done':
        
#         print step, stared, primed, coveredRow, coveredCol
        #print primed
#         print '\n'
        
        break_in = False
        for row in costMatrix:
            for c in row:
                if math.isnan(c):
                    #print 'nan '
                    break_in = True
                    
        if break_in: 
            print 'invalid matrix:'
#             for row in costMatrix:
#                 print row
            return []
            break
        
        if step == 1:
            #coveredCol = []
#             print 'step 1' , stared , coveredCol
            coveredCol = []
            do_step1(costMatrix, stared, coveredCol)
#             print colREt
#             print coveredCol
#             print 'step 1 end' , stared , coveredCol
#             
#             print len(coveredCol), L
            if len(coveredCol) != L:
                step = 2
                primed = []
            else:
                step =  'done'
                
        elif step == 2:
            step = do_step2(costMatrix, coveredCol, coveredRow, primed, stared)
#             print step
            if len(step) > 1:
                if step[0] == 4:
                    eMin = step[1]
                    
                    step = 4
                elif step[0] == 3:
                    Z0 = step[1]
                    step = 3
            
            else:
                step = step[0]
                
        elif step == 3:
            step = do_step3(costMatrix, coveredCol, coveredRow, primed, stared, Z0)
            Z0 = []
            
        elif step == 4:
            
            step = do_step4(costMatrix, coveredCol, coveredRow, primed, stared, eMin)
            eMin = 0
            
           
            
    path  = stared
    #print stared
    return path



if __name__ == '__main__':
   
#     matrix = [[5, 9, 1], [10, 3, 2],[8, 7, 4]]
#     
    matrix = [[400, 150, 400],
              [400, 450, 600],
              [300, 225, 300]]
    path  = computeMunkerCost(matrix)
     
    print path 
#     
#     matrix = [[400, 150, 400, 1],
#               [400, 450, 600, 2],
#               [300, 225, 300, 3]]
#           
#     path  = computeMunkerCost(matrix)
#     
#     print path 
    
    
    matrix  = [[10, 10,  8],
               [9,  8,  1],
               [9,  7,  4]]
    path  = computeMunkerCost(matrix)
    
    print path 