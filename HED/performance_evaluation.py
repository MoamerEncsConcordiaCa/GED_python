'''
Created on Nov 26, 2014

@author: ameriPC
'''
import sys, getopt, os
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt

def main(argv):
    
    precision =[]
    recall = []
    
    performance_file_h = open(argv[0], 'r')
    lines = performance_file_h.readlines()
    for line in lines:
        parts =  line.split('\t')
        print parts
        
        tp = float( parts[1].split('TP:')[1])
        tn = float( parts[2].split('TN:')[1])
        fp = float( parts[3].split('FP:')[1])
        fn = float( parts[4].split('FN:')[1])
        
        new_pr = 0.0
        if tp + fp > 0:
            new_pr = tp / (tp + fp)
            
        print new_pr
        new_reca = 0.0
        if tp + fn > 0:
            new_reca = tp / (tp + fn)
            
        print new_reca
            
        precision.append(new_pr)
        recall.append(new_reca)
        
    print precision
    print recall
    
    precision_array = np.array(precision)   
    recall_array = np.array(recall)
    performance = metrics.auc(recall_array, precision_array)
    print performance
    
    plt.plot(recall_array, precision_array, lw=1, label='auc precision/recall (area = %0.2f)' % ( performance))
    plt.savefig("precision_Recall.png")
    plt.show()

if __name__ == '__main__':
    argv = sys.argv[1:]
    main(argv)
        
        
        