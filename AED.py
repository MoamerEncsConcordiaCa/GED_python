'''
Created on Jun 15, 2014

@author: ameriPC
'''

import numpy as np
import networkx as nx
from hungarian import *

#from costCommon import *
from costWordGraphs import *


def mapNodeToNode(Node1,Node2):
    return [Node1, Node2]

# def addToMapS(mapNew, maps):
#     allMaps = []
#     allMaps.extend(maps)
#     allMaps.append(mapNew)    
#     return allMaps

# def bigCNodes(cMap):
#     a = 0.2
#     Tn = 1
#     Te = 0.5
#     
#     if cMap[0] == 'E' or cMap[1] == 'E':
#         return a* Tn 
#     else: 
#         return a*(abs(cMap[0] - cMap[1]))
#         
# def bigCEdges(edgesMaped):
#     a = 0.2
#     Tn = 1
#     Te = 0.5
#     
#     edge1 = edgesMaped[0]
#     edge2 = edgesMaped[1]
#     
#     
#     if edge1 == 'E' or edge2 == 'E':
#         return (1-a)* Te 
#     else:      
#         
#         if len(edge1) == 3 and len(edge2 )== 3:
#             dist1 = edge1[2]['weight']
#             dist2 = edge2[2]['weight']
#     
#         else:
#             # compute weight to be distance of nodes connecting them
#             dist1 = abs(edge1[0] - edge1[1]) 
#             dist2 = abs(edge2[0] - edge2[1])
#             
#         return (1-a)*(abs(dist1 - dist2))
#     
# def EPC(cPath, G1, G2):
#     cost = 0;
#     
#     G1Nodes = G1.nodes()
#     G2Nodes = G2.nodes()
#     
#     G1Degree = nx.degree(G1).values()
#     G2Degree = nx.degree(G2).values()
#     
#     for cMap in cPath:
#         
#         if cMap[0] == 'E' and cMap[1] == 'E':
#             continue
#         
#         if cMap[0] == 'E':
#             #insertion
#             cost = cost + bigCNodes(cMap)
#             
#             i = G2Nodes.index(cMap[1])
#             cost = cost + G2Degree[i] * bigCEdges(['E','E'])
# 
#         elif cMap[1] == 'E':
#             # deletion
#             cost = cost + bigCNodes(cMap)
#             
#             i = G1Nodes.index(cMap[0])
#             cost = cost + G1Degree[i] * bigCEdges(['E','E'])
#             #print 'f'
#         else:
#             cost = cost + bigCNodes(cMap)
#             # substitution for an edge is when both nodes are mapped 
#             # first node of edge is in cMap which is here
#             # it needs to just test the second node of each adjacent edge  
#             insertedEdges = []
#             deletedEdges = []
#             substitutedEdges = [] 
#             
#             insertedEdges.extend(list(G2.edges(cMap[1])))
#             deletedEdges.extend(list(G1.edges(cMap[0])))            
#             
#             
#             G1SourceNeighbors = G1.neighbors(cMap[0])
#             G2TargetNeighbors = G2.neighbors(cMap[1])
#              
#             # to see which edges are substituted. Remove them form insert and 
#             # delete list            
#             for G1U in G1SourceNeighbors:
#                 for G2V in G2TargetNeighbors:
#                     
#                     if [G1U, G2V] in cPath:
#                         substitutedEdges.append([(cMap[0], G1U),(cMap[1], G2V)])
#                         deletedEdges.remove((cMap[0], G1U))
#                         #deletedEdges.remove((G1U, cMap[0]))
#                         
#                         insertedEdges.remove((cMap[1],G2V))
#                         #insertedEdges.remove([G2V,cMap[1]])
#             for substEdge in substitutedEdges:
#                 
#                 
#                 # to do : this line returnes all edges must be only the substituted edges
#                 
#                 edge1 = G1.edges(substEdge[0], True)
#                 edge2 = G2.edges(substEdge[1], True)
#                 cost = cost + bigCEdges([edge1, edge2])
#                 
#             for deleEdges in deletedEdges:
#                 cost = cost + bigCEdges([deleEdges, 'E'])
#             for insEdge in insertedEdges:
#                 cost  = cost + bigCEdges(['E', insEdge])
#           
#         
#     return cost    



def getEdgeCost_Ce(G1, G2, u, v):
    '''
    this part return a matrix of cost for (insert delete substitute )
    of EDGES.
    
        substitute             del
        |---------------------------------------
        |c1,1 c1,2 ... c1,m  | c1,e inf ... inf
        |c2,1                | inf  c2,e ... inf
        |c3,1                |
        |                    |
        |cn,1     ...  cn,m  |inf inf ...  cn,e
   C=   |_______________________________________
        | ce,1 inf ... inf   | 0 0 ... 0
        |inf  ce,2 ... inf   | 0 0 ... 0
        |inf  inf ...        | ...
        |inf  inf ...  ce,m  | 0 0 ... 0
        _________________________________________
    size is     
        NxM | NxN
        MxM | MxN
        
        
    '''
    INFINITY = np.Inf
    uEdges = G1.edges(u, data = True)
    vEdges = G2.edges(v, data = True)
    N = len (uEdges)
    M = len (vEdges)
    
    #print N 
    #print M
    #print uEdges
    #print vEdges
    #print '_________________________________________________'
    
    #substitution
    substituteCost = [] 
    for i in range(0,N):
        substituteCost.append([])
        for j in range(0, M):
            edgeMapped  = (uEdges[i], vEdges[j])            
            substituteCost[i].append(bigCEdges(edgeMapped))
    
    deletionCost = []
    for i in range(0 ,N):
        deletionCost.append([])
        for j in range(0, N):
            deletionCost[i].append(INFINITY)
            if i == j:
                edgeMapped  = (uEdges[i], 'E')       
                deletionCost[i][j] = (bigCEdges(edgeMapped))
            
    insertionCost = []
    for i in range(0, M):
        insertionCost.append([])
        for j in range(0, M):
            insertionCost[i].append(INFINITY)
            if i == j:
                edgeMapped  = ('E' , vEdges[i]) 
                insertionCost[i][j] = (bigCEdges(edgeMapped))
            
        
    
    edgeCost = []
    for i in range(0, M + N):
        edgeCost.append([])
        for j in range(0, M + N):
            edgeCost[i].append(0.0)
            
    for i in range(0, N):
        for j in range(0, M):
            edgeCost[i][j] = substituteCost[i][j]
            
    for i in range(0, N):
        for j in range(0, N):
            edgeCost[i][j + M] = deletionCost[i][j]
            
    for i in range(0, M):
        for j in range(0, M):
            edgeCost[i + N][j] = insertionCost[i][j]
                   
    #for i in edgeCost:
     #   print i
    #print edgeCost    
    #print len(edgeCost)
    #print '-----------------------------------\n---------------------------------'
    
    pathCost =  computeMunkerCost(edgeCost)
    return pathCost[0]
     
    
def getNodeCost(G1,G2):
    '''
    this part return a matrix of cost for (insert delete substitute )
    of nodes. in substitution par we are using munker for implied edge costs
    
        substitute             del
        |---------------------------------------
        |c1,1 c1,2 ... c1,m  | c1,e inf ... inf
        |c2,1                | inf  c2,e ... inf
        |c3,1                |
        |                    |
        |cn,1     ...  cn,m  |inf inf ...  cn,e
   C=   |_______________________________________
        | ce,1 inf ... inf   | 0 0 ... 0
        |inf  ce,2 ... inf   | 0 0 ... 0
        |inf  inf ...        | ...
        |inf  inf ...  ce,m  | 0 0 ... 0
        _________________________________________
         ins
    
    
    TODO : first fix insert and delete, then substitude part then add all together
    '''
    INFINITY = np.Inf
    
    G1Nodes = G1.nodes()
    G2Nodes = G2.nodes()
    
    G1NodesData = G1.nodes(data  = True)
    G2NodesData = G2.nodes(data  = True)
    
    G1Edges = G1.edges()
    G2Edges = G2.edges()
    
    
    
    N = len(G1Nodes)
    M = len(G2Nodes)
    
    #print 'compute edge costs Ce'
    #print getEdgeCost_Ce(G1, G2, G1Nodes[1], G2Nodes[0])
    Ce = []
    for i in range(0,N):
        Ce.append([])
        for j in range(0, M):
            
            Ce[i].append( getEdgeCost_Ce( G1, G2, G1Nodes[i], G2Nodes[j])  )
     
    
    #print 'Ce finished'
    # substitute cost
    substituteCost = []
    for i in range(0,N):
        substituteCost.append([])
        for j in range(0, M):
            substituteCost[i].append(0)
  
    for i in range(0,N):
        for j in range(0, M):
            nodeMap  = mapNodeToNode(G1NodesData[i], G2NodesData[j])
        
            substituteCost[i][j] = bigCNodes(nodeMap) + Ce[i][j] / 2
              
    #print substituteCost
    
    
    # delete nodes
    deleteCost = []
    for i in range(0,N):
        deleteCost.append([])
        for j in range(0, N):
            deleteCost[i].append(INFINITY)
            
    for i in range(0,N):
        nodeMap  = mapNodeToNode(G1Nodes[i], 'E')        
        deleteCost[i][i] = bigCNodes(nodeMap)
        
    #adding edge costs
    
    
    for e in G1Edges:
        edgeDeleteCost = bigCEdges([e,'E'])/2
#         print e 
#         print G1Nodes.index(e[0])
#         print G1Nodes
#         print G1Edges
#         
        u1 = G1Nodes.index(e[0])
        u2 = G1Nodes.index(e[1])
        deleteCost[u1][u1] = deleteCost[u1][u1] + edgeDeleteCost
        deleteCost[u2][u2] = deleteCost[u2][u2] + edgeDeleteCost
        
    #print deleteCost
    
    
    
    #insert
    insertCost = []
    for i in range(0,M):
        insertCost.append([])
        for j in range(0, M):
            insertCost[i].append(INFINITY)
            
    for i in range(0,M):
        nodeMap  = mapNodeToNode('E', G2Nodes[i])        
        insertCost[i][i] = bigCNodes(nodeMap)
    
    #adding edge costs
    
    for e in G2Edges:
        edgeDeleteCost = bigCEdges(['E',e])/2
#         u1 = e[0] - 1
#         u2 = e[1] - 1
        u1 = G2Nodes.index(e[0])
        u2 = G2Nodes.index(e[1])
        insertCost[u1][u1] = insertCost[u1][u1] + edgeDeleteCost
        insertCost[u2][u2] = insertCost[u2][u2] + edgeDeleteCost
    #print insertCost
    
 
    #nodeCost all
    nodeCost = []
    # setting to zero
    for i in range(0,N + M):
        nodeCost.append([])
        for j in range(0, M + N):
            nodeCost[i].append(0.0)
 
#     for row in nodeCost:
#         print row 
#         print len(row)
#         
#     print 'total row' , len(nodeCost) , N, M
    #copy substitution        
    for i in range(0,N):
        for j in range(0, M):
            nodeCost[i][j] = substituteCost[i][j]
            
    # copy deletion
    for i in range(0 , N):
        for j in range(0 , N):
            nodeCost[i][j + M] = deleteCost[i][j]
            
    #copy insertion
    for i in range(0, M):
        for j in range(0, M):
            nodeCost[i + N][j] = insertCost[i][j]
             
            
#     print 'final cost is  \n\n\n'            
#     for i in range(0,N + M):
#         print nodeCost[i]
#         
#     print 'compute munker for  nodes'      
#     for row in nodeCost:
#         print row  
#         print len(row)
#     print 'total row' , len(nodeCost) , N, M         
    nodeCost = computeMunkerCost(nodeCost)  
#     print 'node compute finished'  
    cost = nodeCost[0]
    path = nodeCost[1]
    
    mapSubstitude = {}
    mapDelete = {}
    mapInsert = {}
    #print cost
    #print path    
    for p in path:
        if p[0] < N and p[1] < M:
            mapSubstitude[G1Nodes[p[0]]] = G2Nodes[p[1]]
            
        elif p[0] >= N and p[1] < M:
            mapInsert[G2Nodes[p[1]]] = 'E'
            
        elif p[0] < N  and p[1] >= M:
            mapDelete[G1Nodes[p[0]]] = 'E'
            
    # fix path before sendin them
    
    return[cost, [mapSubstitude, mapDelete, mapInsert]]


def AED(G1,G2):
   
    '''
    For two graphs first it must apply the cost function for the nodes.
    Then apply the munkers for the nodes.
    int First step we use munker to find implied cost for edges substitution.
    '''
    
    nodeCost = getNodeCost(G1,G2)
    return nodeCost
    #print 'path cost is :'
    #print nodeCost
    

    
   



