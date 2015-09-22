'''
Created on Jun 19, 2014

@author: mo_amer
'''
#from costCommon import *
from costWordGraphs import *
import numpy as np
import networkx as nx


 
def HEC(G1, G2, u, v):
   
    
    c1 ={}
    c2 ={}
    c1Path = {}
    c2Path = {}
    
    G1Edges = G1.edges(u)
    G1EdgesData = G1.edges(u, data = True)
   
    G2Edges = G2.edges(v)
    G2EdgesData = G2.edges(v, data = True)
    
     
   
    #print G1Edges    
    for i in range(0, len(G1Edges)):
        edgeMapped = (G1EdgesData[i], 'E')
         
        c1[G1Edges[i]] = bigCEdges(edgeMapped)
        
        c1Path[G1Edges[i]] = 'E'
     
#      
#     print c1
#     print c1Path
#     
    for i in range(0, len(G2Edges)):
        
        edgeMapped = (G2EdgesData[i], 'E')
        
        c2[ G2Edges[i] ] = bigCEdges(edgeMapped)
        
        c2Path[ G2Edges[i] ] = 'E'
    


    for i in range(0, len(G1Edges)):
        for j in range(0, len(G2Edges)):
            
            edgeMapped = (G1EdgesData[i] , G2EdgesData[j])
            newCost = bigCEdges(edgeMapped) / 2
            
            if newCost < c1[ G1Edges[i]]:
                c1[ G1Edges[i] ] = newCost
                c1Path[ G1Edges[i] ] = G2Edges[j]
            
            if newCost < c2[ G2Edges[j]]:
                c2[ G2Edges[j]] = newCost
                c2Path[ G2Edges[j]] = G1Edges[i]
     
    cost = 0           

    for i in range(0, len(G1Edges)):
        cost += c1[ G1Edges[i]]
        
    for j in range(0, len(G2Edges)):
        cost += c2[ G2Edges[j]]    
        
   
    return [cost, [c1Path, c2Path]]
          
def Lall(G1, G2):
    usize = len(G1.nodes())
    vsize = len(G2.nodes())     
    cost = 0
    
    uMapped = map(lambda x : (x, 'E'), G1.nodes())
    vMapped = map(lambda x : ('E', x), G2.nodes())
    
   
    costu = map(bigCNodes, uMapped)
    costv = map(bigCNodes, vMapped)
    
    minCostu = 0
    minCostv = 0
    if len(costu) > 0:
        
        minCostu = reduce(min, costu)
        
    if len(costv) > 0:
        minCostv = reduce(min, costv)
    
    
    #costu = bigCNodes(cMap)
    if usize > vsize:
        cost = (usize - vsize) * minCostu
    
    else:
        cost = (vsize - usize) * minCostv   
 
    return cost        
        
def LNodes(G1, G2, u, v):
    cost = 0
    usize = G1.degree(u)
    vsize = G2.degree(v)
    
    uEdges = G1.edges(u, data = True)
    vEdges = G2.edges(v, data = True)
    
    uMapped = map(lambda x : (x, 'E'), uEdges)
    vMapped = map(lambda x : ('E', x), vEdges)
    
   
    costu = map(bigCEdges, uMapped)
    costv = map(bigCEdges, vMapped)
    
    
    minCostu = 0
    minCostv = 0
    
    if len(costu) > 0:
        
        minCostu = reduce(min, costu)
        
    if len(costv) > 0:
        minCostv = reduce(min, costv)
    
   
    if usize > vsize:
          
        cost = (usize - vsize) * minCostu
         
    else:
        cost = (vsize - usize) * minCostv
      
    return cost


def HED(G1,G2):
   
    '''
    compute the distance between two graph and also the path between which make the distance
    Hausdorff distance.
    return [d, [G1_dic_map, G2_dict_map]]
    '''
    G1Nodes = G1.nodes()
    G2Nodes = G2.nodes()
    G1NodesData = G1.nodes(data = True)
    G2NodesData = G2.nodes(data = True)
    
    G1Edges = G1.edges()
    G2Edges = G2.edges()
    
    d1 = {}
    d1Path = {}
    d2 = {}
    d2Path = {}
    
    for u in G1Nodes:
        cost = bigCNodes([u,'E'])
       
        uEdges = G1.edges(u, data = True)
        for e in uEdges:
            cost += bigCEdges([e, 'E']) / 2
        
        d1[u]=(cost) 
        d1Path[u]  = 'E'
        
    for v in G2Nodes:
        cost = bigCNodes([v,'E'])
       
        vEdges = G2.edges(v, data = True)
        for e in vEdges:
            cost += bigCEdges([e, 'E']) / 2
        
        d2[v] = (cost) 
        d2Path[v]  = 'E' 

    for u in G1Nodes:
        for v in G2Nodes:
            Ce = []
            
            [Ce, CePath] = HEC(G1, G2, u, v )
            #CePath is the map for edges not used yet
           
            Ce = max(Ce, LNodes(G1, G2, u, v))
            i = G1Nodes.index(u)
            j = G2Nodes.index(v)
            mapNode = [G1NodesData[i], G2NodesData[j]]
            newCostu = (bigCNodes(mapNode) + Ce /2) / 2
            newCostv = (bigCNodes(mapNode) + Ce /2) / 2
            
            if newCostu < d1[u]:
                d1[u] = newCostu
                d1Path[u] = v
            
            if newCostv < d2[v]:
                d2[v] = newCostv
                d2Path[v] = u
                
            
            
    d = 0
    for u in G1Nodes:
        d += d1[u]
        
    
    for v in G2Nodes:
        d += d2[v]
    
    d = max(d, Lall(G1, G2))   
          
#     print 'd1 and d2 :'
#     print d1
#     print d1Path
#     print d2
#     print d2Path
#     print d
#     print 'path cost is :'
#     print 'nothingh yet!'
#     
    
    return [d, [d1Path, d2Path]]
    

