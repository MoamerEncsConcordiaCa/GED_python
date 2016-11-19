'''
Created on Nov 30, 2014

@author: ameriPC
'''

import sys, getopt, os

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)

from global_codes.global_values import *
from experiment import *


def main(argv):
    
    in_path = data_set_path
    out_dir = out_dir_path
    
    try:
        opts, args = getopt.getopt(argv,"d:o:", ["dir=","OutDir="])
    except: 
        print 'mainHED.py -d <dir> -o <dir>'
        sys.exit(2)
    
    for opt, arg in opts:
 
        if opt == '-h':
            print 'mainHED.py -d <dir> -v <cv_Dir> -n <Cn_val> -e <Ce_val>'
            sys.exit()
            
        elif '-d' in opt:
            in_path = str(arg)
       
        elif '-o' in opt:
            out_dir = str(arg)
            
    word_dir = os.path.join(os.path.abspath(in_path), gt)
            
    for cv in cv_list:
        
        cv_path = os.path.join(os.path.abspath(in_path), gt, cv)
#         print cv_path
        out_cv_dir = os.path.join(out_dir, cv)
        make_experiment_sets(cv_path, word_dir,out_cv_dir, experiment_set_path)
    
    
    
    
    
if __name__ == '__main__':
    argv = sys.argv[1:]
    print argv
    main(argv)
    
