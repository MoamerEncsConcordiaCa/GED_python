#!/usr/bin/python

'''
Created on Nov 19, 2014

@author: ameriPC
'''


#from Helper.readGraphXml import readWordGraphs
#import networkx as nx

import sys, getopt, os

from HED import *
from experiment import *


try:
    import matplotlib.pyplot as plt
except:
    raise

experiment_set_path = 'set_of_ids'
score_paths = 'scores'

def main(argv):


    gt = 'gt/'
    graphs = 'graphs/'
    dirPath =''
    
    
    cv = ''
    Ce=0
    Cn=0
    alpha = .5
    Ed_type = 'HED'
    
    word_dir =''
    out_dir = ''

    

    try:
        opts, args = getopt.getopt(argv,"d:v:n:e:o:", ["dir=","cv=", "Cn=", "Ce=","OutDir="])
    except: 
        print 'mainHED.py -d <dir> -v <cv_Dir> -n <Cn_val> -e <Ce_val>'
        sys.exit(2)
    
    for opt, arg in opts:
 
        if opt == '-h':
            print 'mainHED.py -d <dir> -v <cv_Dir> -n <Cn_val> -e <Ce_val>'
            sys.exit()
            
        elif '-d' in opt:
            dirPath = str(arg)
        elif '-v' in opt:
            cv = str(arg)
        elif '-n' in opt:
            Cn = float(arg)
        elif '-e' in opt:
            Ce = float(arg)
        elif '-o' in opt:
            out_dir = str(arg)
             
    
    #print dirPath, cv, Cn, Ce, out_dir
    
    print str(cv) , 'Cn' + str(Cn), 'Ce' + str(Ce)
 
    
    graphPaths = os.path.join(os.path.abspath(dirPath), graphs)
      
    cv_path = os.path.join(os.path.abspath(dirPath), gt, cv)
    word_dir = os.path.join(os.path.abspath(dirPath), gt)
    
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        print 'path created:' + out_dir
 
    out_dir = os.path.join(os.path.abspath(out_dir),cv)
    
#     print graphPaths
#     print cv_path
#     print out_dir
#     print 'call do experiments'
    p_norm_type_list = ['nodes_number_method','ins_del_method']
    
    #print 'not experiment'
    #return

    #do_one_train_experiment(cv_path,word_dir, graphPaths, Ce, Cn, alpha, 'HED', p_norm_type_list, out_dir)
#     make_experiment_sets(cv_path, word_dir,out_dir, experiment_set_path)
    #do_one_train_experiment(cv_path,word_dir, graphPaths, Ce+ .2, Cn - .2, alpha, 'HED', p_norm_type_list, out_dir)
    
    
if __name__ == '__main__':
    argv = sys.argv[1:]
    print argv
    main(argv)
        
    
    