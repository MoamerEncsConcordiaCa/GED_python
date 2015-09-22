'''
Created on Mar 19, 2014

@author: mo_amer
'''

from readGraphXml import readWordGraphs
import networkx as nx
from GED import *
from AED import *
from HED import *

try:
    import matplotlib.pyplot as plt
except:
    raise

if __name__ == '__main__':
    
    G1 = nx.Graph()
    G2 = nx.Graph()
    
    
    G1.add_node(1)
    G1.add_node(2)
    G1.add_node(3)
    G1.add_node(4)
    
    G1.add_edge(1,2, weight  = 1)
    G1.add_edge(2,3, weight  = 10)
    
    
    G2.add_node(1)
    G2.add_node(2)
    G2.add_node(3)
    G2.add_node(4)
    
        
    #G2.add_edge(2,3, weight  = 10)
    G2.add_edge(1,2, weight  = 9.9)
    G2.add_edge(1,4, weight  = 1)
  
    
    #pos = nx.spring_layout(G2, iterations=100)
    #plt.subplot(111)
    #nx.draw(G2, pos, font_size=8)
    #nx.draw_networkx_edges(G2,pos, width=1)
    #nx.draw_networkx_edge_labels(G2,pos,font_size=10,font_family='sans-serif')

    #plt.savefig('G2_init.png')
    #plt.show()
    #plt.close()
    
    #pos = nx.spring_layout(G1, iterations=100)
    #plt.subplot(111)
    #nx.draw(G1, pos, font_size=8)
    #nx.draw_networkx_edge_labels(G1,pos,font_size=10,font_family='sans-serif')
    #plt.savefig("G1_init.png")
    #plt.show()
    
    #x = G1.edges([1], True)
    #print x
    
#     GEDpath =  GED(G1, G2)
#       
#     assignmnetPath = AED(G1, G2)
#     
#     hausorfftPath = HED(G1, G2)
#     
#     print '\nGED ----------------------'
#     
#     print GEDpath
#     print type(GEDpath)
#     
#     print 'assignment ----------------------'
#     
#     print assignmnetPath
#     
#     print 'hausdorff----------------------'
#     
#     print hausorfftPath
#      
#      
    g = readWordGraphs('letters/','train.cxl')
        
    for gi in g:
        print gi.nodes(data = True)
        print gi.edges()
        
        print '\n'
    
    print '\n cost \n'
    costGED = []
    costAED = []
    costHED = []
    for G1 in g:
        costGED.append([])
        costAED.append([])
        costHED.append([])
        for G2 in g:
            GEDpath =  GED(G1, G2)
       
            assignmnetPath = AED(G1, G2)
     
            hausorfftPath = HED(G1, G2)
            
            costGED.append(GEDpath)
            costAED.append(assignmnetPath)
            costHED.append(hausorfftPath)
            
            #print assignmnetPath
#           print 'next graph'
            #print GEDpath
            
        
            
        
    f = open("HED_cost.txt", "w")
    for row in costHED:
        for c in row:
            f.write(str(c))
            f.write('\n')
            
        f.write('\n________________________\n')
        
    f = open("AED_cost.txt", "w")
    for row in costAED:
        for c in row:
            f.write(str(c))
            f.write('\n')
            
        f.write('\n________________________\n')
  
    f = open("Ged_cost.txt", "w")
    for row in costGED:
        for c in row:
            f.write(str(c))
            f.write('\n')
            
        f.write('\n________________________\n')
      

    #print costGED
    
    #print costAED
    
    #print costHED
    
    exit()


    G = g[9]
    # position is stored as node attribute data for random_geometric_graph
    pos=nx.get_node_attributes(G,'pos')
    
    print G.nodes(data = True)
    print pos
    # find node near center (0.5,0.5)
    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d
    
    # color by path length from node near center
    p=G.nodes()
    
    plt.figure(figsize=(8,8))
    nx.draw_networkx_edges(G,pos,G.edges(),alpha=0.4)
    nx.draw_networkx_nodes(G,pos,nodelist=p,
                           node_size=80,
                           )
    
   # plt.xlim(-0.05,1.05)
    #plt.ylim(-0.05,1.05)
    plt.axis('off')
    plt.savefig('wordGraph.png')
    plt.show()
    
    
    
    
        
#     G = nx.grid_2d_graph(4, 4)  # 4x4 grid
# 
#     pos = nx.spring_layout(G, iterations=100)
# 
#     plt.subplot(221)
#     nx.draw(G, pos, font_size=8)
# 
#     plt.subplot(222)
#     nx.draw(G, pos, node_color='k', node_size=0, with_labels=False)
# 
#     plt.subplot(223)
#     nx.draw(G, pos, node_color='g', node_size=250, with_labels=False, width=6)
# 
#     plt.subplot(224)
#     H = G.to_directed()
#     nx.draw(H, pos, node_color='b', node_size=20, with_labels=False)
# 
#     plt.savefig("four_grids.png")
#     plt.show()
    
    print '_______END________'
