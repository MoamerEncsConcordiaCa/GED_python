'''
Created on Jul 1, 2014

@author: ameriPC
'''
a = 0.2
Tn = 1
Te = 0.5
  
  
def bigCNodes(cMap):
    
    if cMap[0] == 'E' or cMap[1] == 'E':
        return a* Tn 
    else: 
        return a*(abs(cMap[0] - cMap[1]))
        
def bigCEdges(edgesMaped):
    
    edge1 = edgesMaped[0]
    edge2 = edgesMaped[1]
    
   
    if edge1 == 'E' or edge2 == 'E':
        return (1-a)* Te 
    else:      
   
        if len(edge1) == 3 and len(edge2 )== 3:
            dist1 = edge1[2]['weight']
            dist2 = edge2[2]['weight']
    
        else:
            # compute weight to be distance of nodes connecting them
            dist1 = abs(edge1[0] - edge1[1]) 
            dist2 = abs(edge2[0] - edge2[1])
            
        return (1-a)*(abs(dist1 - dist2))
   