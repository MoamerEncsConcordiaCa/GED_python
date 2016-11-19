'''
Created on Jul 3, 2014

@author: ameriPC
'''
import xml.etree.ElementTree as ET
import networkx as nx

from math import *

def getFileList(directory , fileName):
    tree = ET.parse(directory + fileName)
    root = tree.getroot()
    
    file_list = []
    
    
    for fileInfo in root[0]:
        name =  fileInfo.get('file')
        
        file_list.append(directory + name)
    return file_list


def readGraphInfo(fileName):
     
    graphXml = ET.parse(fileName)
    
    graphXmlRoot = graphXml.getroot()
    #print graphXmlRoot.attrib
    G = nx.Graph()
    for GElement in graphXmlRoot[0]:
        if GElement.tag == 'node' :
            #print 'node'
            node_name =  GElement.get('id')
            G.add_node(node_name)
            x = 0 
            y = 0
            for cord in GElement:
                nodeAttrib =  cord.get('name')
                if nodeAttrib == 'x' :
                    x = float (cord[0].text)
                if nodeAttrib == 'y':
                    y  = float (cord[0].text)
                
            G.add_node(node_name, pos= [x,y])
            #print [x, y]
                
            
        if GElement.tag == 'edge' :
            #print 'edge'
            #print GElement.attrib
            edgeTo =  GElement.get('to')
            edgeFrom =  GElement.get('from')
            G.add_edge(edgeFrom, edgeTo)
            
    
    return G

def readWordGraphs(directory, fileName):
    fileList = getFileList(directory, fileName)
    G = []
    for graphFileName in fileList:
        G.append(readGraphInfo(graphFileName))
    
    return G





if __name__ == '__main__':
    #print 'main'
    tree = ET.parse('letters/train.cxl')
    root = tree.getroot()
   
    file_list = []
    
    dir = 'letters/'
    for l1 in root:
        for file in l1:
            name =  file.get('file')
            
            file_list.append(dir + name)

    #print file_list
    print 'file list :'
    for f in file_list:
        print f
        #tree = ET.parse('letters/train.cxl')
        
    graph1 = ET.parse('letters/AP1_0000.gxl')
    graph1Root = graph1.getroot()
    print graph1Root[0].tag
    print graph1Root[0].attrib
    
    for n in graph1Root[0]:
        print n.tag
        print n.attrib
        
    x1 = 1
    x2 = 5
    y1 = 1
    y2 = 1    
    print 'value of sqrt'
    print pow((x1-x2), 2)
    print (x1-x2)**2
    
    val  = 0.5*(sqrt( pow(x1-x2, 2) + (y1-y2)**2 ))
    print val
