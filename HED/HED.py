'''
Created on Jun 19, 2014

@author: mo_amer
'''
#from costCommon import *
import os, sys
from costWordGraphs import *
import numpy as np
import networkx as nx

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)

from global_codes.readGraphXml import readGraphInfo

 
def HEC(G1, G2, u, v, p_cost):
   
    
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
         
        c1[G1Edges[i]] = bigCEdges(edgeMapped, p_cost)
        
        c1Path[G1Edges[i]] = 'E'
     
#      
#     print c1
#     print c1Path
#     
    for i in range(0, len(G2Edges)):
        
        edgeMapped = (G2EdgesData[i], 'E')
        
        c2[ G2Edges[i] ] = bigCEdges(edgeMapped, p_cost)
        
        c2Path[ G2Edges[i] ] = 'E'
    


    for i in range(0, len(G1Edges)):
        for j in range(0, len(G2Edges)):
            
            edgeMapped = (G1EdgesData[i] , G2EdgesData[j])
            newCost = bigCEdges(edgeMapped, p_cost) / 2
            
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

def get_normalization(G1, G2, norm_type_list, p_cost):
    
    #normalization_score = []
    score_dict = {}
    for norm_type in norm_type_list:
        if norm_type == 'nodes_number_method':
            #print 'node number'
            norm_score = G1.number_of_nodes() + G2.number_of_nodes()
            #normalization_score.append(norm_score)
            score_dict[norm_type ] = norm_score
            
        if norm_type == 'ins_del_method':
            #print 'ins del method'
            norm_score = Lall(G1, G2, p_cost)
            for u in G1:
                for v in G2:
                    edge_rem_cost = LNodes(G1, G2, u, v, p_cost)
                    norm_score += edge_rem_cost
            #normalization_score.append(norm_score)
            score_dict[norm_type ] = norm_score
            
    #print score_dict
    
            
    return score_dict
    
              
def Lall(G1, G2, p_cost):
    usize = len(G1.nodes())
    vsize = len(G2.nodes())     
    cost = 0
    
    uMapped = map(lambda x : (x, 'E'), G1.nodes())
    vMapped = map(lambda x : ('E', x), G2.nodes())
    
    costu = [bigCNodes(x, p_cost) for x in uMapped]
    costv = [bigCNodes(x, p_cost) for x in vMapped]
    #costu = map(bigCNodes, uMapped, p_cost)
    #costv = map(bigCNodes, vMapped, p_cost)
    
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
        
def LNodes(G1, G2, u, v, p_costs):
    cost = 0
    usize = G1.degree(u)
    vsize = G2.degree(v)
    
    uEdges = G1.edges(u, data = True)
    vEdges = G2.edges(v, data = True)
    
    uMapped = map(lambda x : (x, 'E'), uEdges)
    vMapped = map(lambda x : ('E', x), vEdges)
    cost_u = []
    cost_v = []
    
   
    costu = [bigCEdges(x, p_costs) for x in uMapped]
    costv = [bigCEdges(x, p_costs) for x in vMapped]
    
    #costu = map(bigCEdges, uMapped, p_costs)
    #costv = map(bigCEdges, vMapped, p_costs)
    
    
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


def HED(G1,G2,p_costs, p_path = False):
   
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
        cost = bigCNodes([u,'E'], p_costs)
       
        uEdges = G1.edges(u, data = True)
        for e in uEdges:
            cost += bigCEdges([e, 'E'], p_costs) / 2
        
        d1[u]=(cost) 
        d1Path[u]  = 'E'
        
    for v in G2Nodes:
        cost = bigCNodes([v,'E'], p_costs)
       
        vEdges = G2.edges(v, data = True)
        for e in vEdges:
            cost += bigCEdges([e, 'E'], p_costs) / 2
        
        d2[v] = (cost) 
        d2Path[v]  = 'E' 

    for u in G1Nodes:
        for v in G2Nodes:
            Ce = []
            
            [Ce, CePath] = HEC(G1, G2, u, v, p_costs )
            #CePath is the map for edges not used yet
           
            Ce = max(Ce, LNodes(G1, G2, u, v, p_costs))
            i = G1Nodes.index(u)
            j = G2Nodes.index(v)
            mapNode = [G1NodesData[i], G2NodesData[j]]
            newCostu = (bigCNodes(mapNode, p_costs) + Ce /2) / 2
            newCostv = (bigCNodes(mapNode, p_costs) + Ce /2) / 2
            
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
    
    d = max(d, Lall(G1, G2, p_costs))   
          
#     print 'd1 and d2 :'
#     print d1
#     print d1Path
#     print d2
#     print d2Path
#     print d
#     print 'path cost is :'
#     print 'nothingh yet!'
#     
    if p_path :
        return [d, [d1Path, d2Path]]
    return d
    

