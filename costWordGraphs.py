'''
Created on Jul 1, 2014

@author: ameriPC
'''
from math import *

  
def bigCNodes(cMap):
    
    if cMap[0] == 'E' or cMap[1] == 'E':
        return 0.2
    else: 
        u = cMap[0]
        v = cMap[1]
        #print '\n'
        x1, y1 =  u[1]['pos']
        x2, y2 =  v[1]['pos']
        
        
        val =  0.5*(sqrt( (x1-x2)**2 + (y1-y2)**2 ))
        #print val
        #print x1, y1, x2, y2, val
        #print cMap[0]
        #print cMap[1]
        
        return val
        
def bigCEdges(edgesMaped):
    
    edge1 = edgesMaped[0]
    edge2 = edgesMaped[1]
    
   
    if edge1 == 'E' or edge2 == 'E':
        return 0.05
    else:      
        return 0