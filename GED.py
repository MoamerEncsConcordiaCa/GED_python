'''
Created on Apr 2, 2014

@author: mo_amer
'''
import networkx as nx
#from costCommon import *
from costWordGraphs import *

def mapNodeToNode(Node1,Node2):
    return [Node1, Node2]

def addToMapS(mapNew, maps):
    allMaps = []
    allMaps.extend(maps)
    allMaps.append(mapNew)    
    return allMaps

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
#     if edgesMaped[0] == 'E' or edgesMaped[1] == 'E':
#         return (1-a)* Te 
#     else: 
#         
#         if len(edgesMaped[0][0]) == 3 and len(edgesMaped[1][0] )== 3:
#             dist1 = edgesMaped[0][0][2]['weight']
#             dist2 = edgesMaped[1][0][2]['weight']
#     
#         else:
#             dist1 = 0 
#             dist2 = 0
#         return (1-a)*(abs(dist1 - dist2))
#     

def EPC(cPath, G1, G2):
    cost = 0;
    
    G1Nodes = G1.nodes()
    G2Nodes = G2.nodes()
    
    G1NodesData = G1.nodes(data = True)
    G2NodesData = G2.nodes(data = True)
 
    
    G1Degree = nx.degree(G1).values()
    G2Degree = nx.degree(G2).values()
    
    for cMap in cPath:
        
        if cMap[0] == 'E' and cMap[1] == 'E':
            continue
        
        if cMap[0] == 'E':
            #insertion
            cost = cost + bigCNodes(cMap)
            
            i = G2Nodes.index(cMap[1])
            cost = cost + G2Degree[i] * bigCEdges(['E','E']) / 2

        elif cMap[1] == 'E':
            # deletion
            cost = cost + bigCNodes(cMap)
            
            i = G1Nodes.index(cMap[0])
            cost = cost + G1Degree[i] * bigCEdges(['E','E']) /2
            #print 'f'
        else:
            i = G1Nodes.index(cMap[0])
            j = G2Nodes.index(cMap[1])
            
            nodeMap  = (G1NodesData[i], G2NodesData[j])
        
            cost = cost + bigCNodes(nodeMap)
            # substitution for an edge is when both nodes are mapped 
            # first node of edge is in cMap which is here
            # it needs to just test the second node of each adjacent edge  
            insertedEdges = []
            deletedEdges = []
            substitutedEdges = [] 
            
            insertedEdges.extend(list(G2.edges(cMap[1])))
            deletedEdges.extend(list(G1.edges(cMap[0])))            
            
            
            #G1SourceNeighbors = G1.neighbors(cMap[0])
            #G2TargetNeighbors = G2.neighbors(cMap[1])
             
            # to see which edges are substituted. Remove them form insert and 
            # delete list      
            U1 = cMap[0]
            V1 = cMap[1]
                  
            G1UEdgesData = G1.edges(U1, data = True)
            G2VEdgesData = G2.edges(V1, data = True)
            
            G1UEdges = G1.edges(U1)
            G2VEdges = G2.edges(V1)
            
            for i in range(0, len(G1UEdges)):
                for j in range(0, len(G2VEdges)):
                    p = G1UEdges[i]
                    q = G2VEdges[j]
                    
                    U2 = p[0]
                    if U2 == cMap[0]:
                        U2 = p[1]
                        
                    V2 = q[0]    
                    if V2 == cMap[1]:
                        V2 = q[1]
                    
                    if [U2, V2] in cPath:
                        deletedEdges.remove((U1, U2))
                        insertedEdges.remove((V1, V2))
                        substitutedEdges.append((G1UEdgesData[i], G2VEdgesData[j]))
                           
                        
   
#             for G1U in G1SourceNeighbors:
#                 for G2V in G2TargetNeighbors:
#                     
#                     if [G1U, G2V] in cPath:
#                         
#                         substitutedEdges.append([(cMap[0], G1U),(cMap[1], G2V)])
#                        
#                         deletedEdges.remove((cMap[0], G1U))
#                         #deletedEdges.remove((G1U, cMap[0]))
#                         
#                         insertedEdges.remove((cMap[1],G2V))
#                         #insertedEdges.remove([G2V,cMap[1]])
#           
#             print 'substitude edge : '
#             print substitutedEdges              
            for substEdge in substitutedEdges:
                
                
                # to do : this line returnes all edges must be only the substituted edges
                
#                 edge1 = G1.edges((substEdge[0][0],substEdge[0][1]), data = True)
#                 edge2 = G2.edges((substEdge[1][0],substEdge[1][1]), data = True)
#                 
#                 cost = cost + bigCEdges([edge1, edge2])
                
                cost += bigCEdges(substEdge) / 2

                
            for deleEdges in deletedEdges:
                cost = cost + bigCEdges([deleEdges, 'E']) / 2
            for insEdge in insertedEdges:
                cost  = cost + bigCEdges(['E', insEdge]) /2
          
        
    return cost    

# def hurstic(cPath, G1, G2):
#     '''
#     hurstic is buggy so we are using the trivial case 0 now 
#     
#     '''
#     
#     cost  = 0
#     return cost
# 
#     G1NodesRemained = []
#     G2NodesRemained = []
#     G1NodesRemained.extend(G1.nodes())
#     G2NodesRemained.extend(G2.nodes())
#     
#     for cMap in cPath:
#         
#         if cMap[0] != 'E':
#             G1NodesRemained.remove(cMap[0]) 
#         if cMap[1] != 'E':
#             G2NodesRemained.remove(cMap[1])
#     minVal = []
#     
#     for u in G1NodesRemained:
#         for v in G2NodesRemained:
#             cVal1 = bigCNodes([u, v])
#             cVal2 = bigCNodes([u, 'E']) + bigCNodes(['E', v])
#             cVal = min(cVal1, cVal2)
#             if minVal == []:
#                 minVal = cVal
#                   
#             if cVal < minVal:
#                 minVal = cVal      
#     
#     #substitution with minVal of all
#     if minVal == []:
#         minVal = 0
#     cost = cost + minVal* min(len(G1NodesRemained), len(G2NodesRemained))
#     cost = cost + max(0, len(G1NodesRemained) - len(G2NodesRemained)) * bigCNodes([u, 'E'])  
#     cost = cost + max(0, len(G2NodesRemained) - len(G1NodesRemained)) * bigCNodes(['E', v])
#     
#     ########################  For Edges
#     G1EdgesRemained = []
#     G2EdgesRemained = []
#     for u in G1NodesRemained:
#         G1EdgesRemained.extend(G1.edges(u, True))
#         
#     for v in G2NodesRemained:
#         G2EdgesRemained.extend(G2.edges(v, True))  
#         
#     minVal = []    
#     for u in G1EdgesRemained:
#         for v in G2EdgesRemained:
#             #cVal1 = bigCEdges([u, v])
#             cVal2 = bigCEdges([u, 'E']) + bigCEdges(['E', v])
#             cVal = min(cVal1, cVal2)
#             if minVal == []:
#                 minVal = cVal
#                   
#             if cVal < minVal:
#                 minVal = cVal      
#     
#     #substitution with minVal of all
#     if minVal == []:
#         minVal = 0
#     cost = cost + minVal* min(len(G1EdgesRemained), len(G2EdgesRemained))
#     cost = cost + max(0, len(G1EdgesRemained) - len(G2EdgesRemained)) * bigCEdges([u, 'E'])  
#     cost = cost + max(0, len(G1EdgesRemained) - len(G2EdgesRemained)) * bigCEdges(['E', v])
#         
#      
#     
#     
#     #return cost
#     return 0

def argMin(openSet, G1, G2):
    if len(openSet) == 0:
        return []
       
    minIndex = -1
    minCost = 0
    for cPath in openSet:
        if minIndex == -1 :
            minCost = EPC(cPath, G1, G2) + 0 #hurstic(cPath, G1, G2)
            minIndex = openSet.index(cPath)
            continue
        
        cCost = EPC(cPath, G1, G2) + 0 #hurstic(cPath, G1, G2)
        if minCost > cCost:
            minCost = cCost
            minIndex = openSet.index(cPath)
        
        
    if minIndex == -1:
        return []   
    #print minCost
    #print openSet[minIndex]   
    return openSet[minIndex]


def isCompletePath(pMin, G1Nodes, G2Nodes):
    '''
    a path is complete if it contains all the nodes from both g1 and g2 graph
    mapped. 
    '''
    G1Mapped = []
    G2Mapped = [] 
    for m in pMin:
        if m[0] != 'E':
            G1Mapped.append(m[0])
        if m[1] != 'E':
            G2Mapped.append(m[1])
    
    for n in G1Nodes:
        if not(n in G1Mapped):
            return False
    for n in G2Nodes:
        if not(n in G2Mapped):
            return False     
       
    return True
        


def GED(G1, G2):
   
    '''
    elements in openSet are path and defined like p_i = [[1,3],[2,2], [3,E]]
    it is mapping of node 1 to 3 and node 2 to 2 and 3 to empty
    and openSet contains openSet = [p_1, p_2, ..., p_n] 
    '''
    G1Nodes = G1.nodes()
    G2Nodes = G2.nodes()
    
    openSet = []
    for i in range(0, G2.number_of_nodes()):         
        openSet.append(addToMapS(mapNodeToNode(G1Nodes[0], G2Nodes[i]), []))
        
    openSet.append(addToMapS(mapNodeToNode(G1Nodes[0], 'E'),[]))
    
    #print openSet
    pMin = []
    while True:
        pMin = argMin(openSet, G1, G2)
        # return first element by now
        
        if isCompletePath(pMin, G1Nodes, G2Nodes):
            #print 'found complete map'
            
            #print pMin
            
            break
        else:

            k = len(pMin)
            openSet.remove(pMin)
            
            if k < len(G1Nodes):
                pNew = addToMapS(mapNodeToNode(G1Nodes[k], 'E'), pMin)
                openSet.append(pNew)
                
                G2Mapped = []
                for m in pMin:
                    if m[1] != 'E':
                        G2Mapped.append(m[1])

                G2UnMapped = []
                G2UnMapped.extend(G2Nodes)
                for m in G2Mapped:
                    G2UnMapped.remove(m)
                    
                for m in G2UnMapped:                
                    pNew = addToMapS(mapNodeToNode(G1Nodes[k], m), pMin)
                    openSet.append(pNew)                     
                              
                
            else:
                G2Mapped = []
                for m in pMin:
                    if m[1] != 'E':
                        G2Mapped.append(m[1])
                pNew = []
                pNew.extend(pMin)
                
                G2UnMapped = []
                G2UnMapped.extend(G2Nodes)
                for m in G2Mapped:
                    G2UnMapped.remove(m)
                    
                for m in G2UnMapped:
                    pNew = addToMapS(mapNodeToNode('E', m), pNew)
                openSet.append(pNew)
                
                #print 'a new complete map'
                #print pNew
                #print '##################'
                
    
         
    
    
    pMin = argMin(openSet, G1, G2)
        
    costMin = EPC(pMin, G1, G2)   
    
    mapSubstitude ={}
    mapInsert = {}
    mapDelete ={}
    
    for p in pMin:
        if p[0] != 'E' and p[1] !='E':
            mapSubstitude[p[0]] = p[1]
            
        elif p[0] =='E' and p[1] != 'E':
            mapInsert[p[1]] = 'E'
            
        elif p[0] != 'E'  and p[1] == 'E':
            mapDelete[p[0]] = 'E'
            
    # fix path before sendin them
    
    return[costMin, [mapSubstitude, mapDelete, mapInsert]]

        
    
#   print 'GED finished'
    return [costMin, pMin]
    #for p in openSet:
        #print p
        #print EPC(p, G1, G2) 
        
    
    
    return pMin