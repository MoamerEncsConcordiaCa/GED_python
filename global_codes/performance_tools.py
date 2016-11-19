'''
Created on Dec 11, 2014

@author: ameriPC
'''
import sys, os




import sys, getopt, os
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from Edit_Distance_Algorithm.global_codes.global_values import *

def write_validation_item_id_to_file (list_word_scores, performance_path, normalizing_param):
    
    performance_dir = os.path.join(performance_path, normalizing_param)
    
    if not os.path.exists(performance_dir):
        os.mkdir(performance_dir)
        
    performace_file_name = os.path.join(performance_dir, "validation_id.txt")
      

    file_h = open(performace_file_name, 'w')
    
    for word_score_item in list_word_scores:
        
        item_id = word_score_item[3]
        
        file_h.write(str(item_id))
        
        
        file_h.write('\n\r')
    
    
    file_h.close()
    

def write_performace_to_file(performance_list, performance_path, normalizing_param):
     
     
    performance_dir = os.path.join(performance_path, normalizing_param)
    
    if not os.path.exists(performance_dir):
        os.mkdir(performance_dir)
        
    performace_file_name = os.path.join(performance_dir, "performance_by_threshold.txt")
    
    

    file_h = open(performace_file_name, 'w')
    
    for performance_item in performance_list:
        
                
        tp = float( performance_item['TP'])
        tn = float( performance_item['TN'])
        fp = float( performance_item['FP'])
        fn = float( performance_item['FN'])
        
        new_pr = 0.0
        if tp + fp > 0:
            new_pr = tp / (tp + fp)
            
#         print new_pr
        new_reca = 0.0
        if tp + fn > 0:
            new_reca = tp / (tp + fn)
            
        performance_item['PR'] = new_pr
        performance_item['RE'] = new_reca
        
        file_h.write('thr: '+ str(performance_item['thr']))
        file_h.write(', TP: '+ str(performance_item['TP']))
        file_h.write(', TN: '+ str(performance_item['TN']))
        file_h.write(', FP: '+ str(performance_item['FP']))
        file_h.write(', FN: '+ str(performance_item['FN']))
        file_h.write(', PR: '+ str(performance_item['PR']))
        file_h.write(', RE: '+ str(performance_item['RE']))
        
        
        file_h.write('\n\r')
        
        
    file_h.close()
    
    

def compute_curve(argv, score_path, normalizing_param):
    
    precision =[]
    recall = []
    
    tp_list = []
    fp_list = []
    
    for performance_item in argv:
        
                
        tp = float( performance_item['TP'])
        tn = float( performance_item['TN'])
        fp = float( performance_item['FP'])
        fn = float( performance_item['FN'])
        
        tp_list.append(tp)
        fp_list.append(fp)
        
        new_pr = 0.0
        if tp + fp > 0:
            new_pr = tp / (tp + fp)
            
#         print new_pr
        new_reca = 0.0
        if tp + fn > 0:
            new_reca = tp / (tp + fn)
            
#         print new_reca
            
        precision.append(new_pr)
        recall.append(new_reca)
        
#     print precision
#     print recall
    
    print 'precision'
    print precision
    
    print 'recall'
    print recall
    
    
    precision_array = np.array(precision)   
    recall_array = np.array(recall)
    performance = metrics.auc(recall_array, precision_array)
    print performance
    
    plt.plot( recall_array, precision_array, 'xb-', 
              lw=1)
    plt.ylabel('precision')
    plt.xlabel('recall')
    
    score_dir = os.path.join(score_path, normalizing_param)
    
    if not os.path.exists(score_dir):
        os.mkdir(score_dir)
        
    score_diagram_file = os.path.join(score_dir, "precision_Recall.png")
    plt.savefig(score_diagram_file)
#     plt.show()

    tp_array = np.array(tp_list)   
    fp_array = np.array(fp_list)
    
    plt.clf()
    plt.plot(fp_array, tp_array, 'xb-', lw=1)
    plt.xlabel('false positive')
    plt.ylabel('true positive')
    score_diagram_file = os.path.join(score_dir, "ROC.png")
    plt.savefig(score_diagram_file)
    
    roc = metrics.auc(fp_array, tp_array )
    
    print 'ROC=' + str(roc)

def list_best_score_images(list_scores,  list_word_scores, best_count_num, performance_path,
                           normalizing_param ):
    SRC = os.getcwd()
    out_dir_path = os.path.abspath(os.path.join(SRC, '../../out_dir'))
    
    
    path_images = os.path.abspath( os.path.join(out_dir_path, '../', DATA_SET_PATH, DATA_SET_PATH_IMAGES))
    
    best_scores = list_scores[0:best_count_num -1]
    
    for score in list_word_scores:
        s_value = score[0]
        first_str = score[1]
        second_str = score[2]
        item_id = score[3]
        
             
        
        if s_value in best_scores or first_str == second_str:
            s_position = list_scores.index(s_value)
            
            image_file_name = os.path.join(path_images, item_id+'.png')
            
            img=mpimg.imread(image_file_name)
            imgplot = plt.imshow(img)
            imgplot.set_cmap('spectral')
            title_fig =  '\n score= ' + str(s_value) + \
                    '\n rank = ' + str(s_position)+ '/' + str(len(list_scores))
            
            plt.xlabel(first_str+ ' <-> '+ second_str )
            plt.title(title_fig)
            
            imgplot.axes.get_xaxis().set_ticks([])
            
            performance_dir = os.path.join(performance_path, normalizing_param)
    
            if not os.path.exists(performance_dir):
                os.mkdir(performance_dir)
            
            if first_str == second_str: 
                
                file_name_out = str(s_position).zfill(5) + '_same_keyword_' + item_id + '.png'
            
            else:
                file_name_out = str(s_position).zfill(5) + '_' + item_id + '.png'
            
            
            
            image_file_out = os.path.join(performance_dir, file_name_out)
            plt.savefig(image_file_out)
            plt.clf()
            
            
            
        
        
        
        
            
 
    


def global_threshold_performace(p_keyword):
    
    
    return

def get_performance_root(p_keyword, p_cv):
    SRC = os.getcwd()
    out_dir_path = os.path.abspath(os.path.join(SRC, '../../out_dir'))
  
    performance_path = os.path.join(out_dir_path, PERFORMANCE_PATH)
    if not os.path.exists(performance_path):
        os.mkdir(performance_path)
    performance_local_threshold_path = os.path.join(performance_path, LOCAL_TRESHOLD_PATH)
    if not os.path.exists(performance_local_threshold_path):
        os.mkdir(performance_local_threshold_path)
        
    performance_cv_path = os.path.join(performance_local_threshold_path, p_cv)
    if not os.path.exists(performance_cv_path):
        os.mkdir(performance_cv_path)
    
    performance_keyword_path = os.path.join(performance_cv_path, p_keyword)
    if not os.path.exists(performance_keyword_path):
        os.mkdir(performance_keyword_path)

    
    return performance_keyword_path

def get_score_root(p_cv, p_experiment):
    SRC = os.getcwd()
    out_dir_path = os.path.abspath(os.path.join(SRC, '../../out_dir'))
    
    score_path = os.path.join(out_dir_path, experiment_scores, p_cv, p_experiment)
    return score_path

def  get_scores_list_0(valid_path, experiments_path, keyword_str):
    
    score_list =  [ ]
    score_id_list = []
    
#     experiments_path_list = ['HED/Cn=1, Ce=0, a=0.5/ins_del_method', 'HED/Cn=1, Ce=0, a=0.5/nodes_number_method']
    
#     print experiments_path_list
#     print type(experiments_path_list[0][0])
#     print experiments_path_list[0][0]
    
    valid_word_items = [valid_word for valid_word in  os.listdir(valid_path) 
                        if os.path.isdir(os.path.join(valid_path, valid_word))]
    
    for valid_word in valid_word_items:
        
        valid_word_dir = os.path.join(valid_path, valid_word)
        if not os.path.exists(valid_word_dir):
            print valid_word_dir , ' not exitst '
# ids for each word

        valid_word_item_ids = [valid_id for valid_id in  os.listdir(valid_word_dir) 
                        if os.path.isdir(os.path.join(valid_word_dir, valid_id))]
        
        for valid_id in valid_word_item_ids:
            
            ins_del_path = os.path.join(valid_word_dir, valid_id, experiments_path, 'score.txt')
#             print ins_del_path
#             print os.path.exists(ins_del_path)
            
            file_score = open(ins_del_path, 'r')
            score = float(file_score.read())
            file_score.close()
            
            score_list.append(score)
#             print float(score)
            
            score_id_list.append([score, valid_word, keyword_str])
            
        
    
        
#     print valid_word_items
    return [score_id_list, score_list]     

def  get_scores_list(valid_path, keyword_path, keyword_str):
    
    score_list =  [ ]
    score_id_list = []
    
    
    valid_word_items = [valid_word for valid_word in  os.listdir(valid_path) 
                        if os.path.isdir(os.path.join(valid_path, valid_word))]
    
    for valid_word in valid_word_items:
        
        valid_word_dir = os.path.join(valid_path, valid_word)
        
        if not os.path.exists(valid_word_dir):
            print valid_word_dir , ' not exitst '


        # ids for each valid 
        valid_word_item_ids = [valid_id for valid_id in  os.listdir(valid_word_dir) 
                        if os.path.isdir(os.path.join(valid_word_dir, valid_id))]
        
        for valid_id in valid_word_item_ids:
            
            ins_del_path = os.path.join(valid_word_dir, valid_id, keyword_path, 'score.txt')
#             print ins_del_path
#             print os.path.exists(ins_del_path)
            
            file_score = open(ins_del_path, 'r')
            score = float(file_score.read())
            file_score.close()
            
            score_list.append(score)
#             print float(score)
            
            score_id_list.append([score, valid_word, keyword_str, valid_id])
            
        
    
        
#     print valid_word_items
    return [score_id_list, score_list]   



def compute_performance(thr, recognition_pair_value):
    
    score_pairs = recognition_pair_value
    TP = 0.0 
    TN = 0.0
    FP = 0.0
    FN = 0.0
    
    for score in score_pairs:
        s_value = score[0]
        first_str = score[1]
        second_str = score[2]
        
        if first_str == second_str:
            if s_value <= thr:
                TP += 1
            else:
                FN +=1
            
        else:
            if s_value <= thr:
                FP +=1
            else:
                TN +=1
                
    acuracy = (TP + TN) / (TP + TN + FP + FN)
    
    
    prformance = {'thr': thr, 'acc': acuracy, 'TP':TP, 'TN':TN, 'FP':FP, 'FN':FN}            
#     precision = TP / (TP + FN)   
#     recall = TP / (TP + FP)           
            
    
    
    return  prformance  

def draw_precision_cuve(list_scores, list_word_scores, performance_path, normalizing_param):
    
    list_scores.sort()
    
    performance_list = []
    for thr in list_scores:
        new_pr = compute_performance(thr, list_word_scores)
        if new_pr['TP'] >= 0:
            performance_list.append(new_pr)
#             print new_pr
        
#     print 'two first'    
#     print (performance_list[0])
#     print (performance_list[1])
#     
    
    compute_curve(performance_list, performance_path, normalizing_param)
    
    list_best_score_images(list_scores,  list_word_scores, 20 , performance_path,
                            normalizing_param)
    write_performace_to_file(performance_list, performance_path, normalizing_param)
    
    write_validation_item_id_to_file (list_word_scores, performance_path, normalizing_param)
     
    
def local_threshold_performace(p_keyword, p_cv):
    
    print 'local threshold'
    p_experiment = 'HED/Cn=1, Ce=0, a=0.5'
    score_path = get_score_root(p_cv, p_experiment)
    performance_path = get_performance_root(p_keyword, p_cv)
    print score_path
    print performance_path
    print os.path.exists(score_path)
    print os.path.exists(performance_path)
    
    

#     keyword_items = [keyword_item for keyword_item in  os.listdir(score_path) if os.path.isdir(os.path.join(score_path, keyword_item))]

#     print keyword_items
    
    

    valid_path = os.path.join(score_path, 'valid')
    print valid_path
    print os.path.exists(valid_path)
    
    valid_word_items = [valid_word for valid_word in  os.listdir(valid_path) 
                        if os.path.isdir(os.path.join(valid_path, valid_word))]
    
    print len(valid_word_items)
#    get list of scores
    
    
    keyword_pathx= ['W-a-s-h-i-n-g-t-o-n-s_cm/270-18-01/ins_del_method'
        , 'W-a-s-h-i-n-g-t-o-n-s_cm/270-18-01/nodes_number_method']
    
#     experiments_path_list = ['HED/Cn=1, Ce=0, a=0.5/ins_del_method', 'HED/Cn=1, Ce=0, a=0.5/nodes_number_method']
    
    normalizing_param = ['ins_del_method', 'nodes_number_method']
    
    i = 0
    for keyword_path in keyword_pathx:   
  
        [list_word_scores, list_scores] = get_scores_list(valid_path, keyword_path, p_keyword)
        
        draw_precision_cuve(list_scores, list_word_scores,
                             performance_path, normalizing_param[i])
        i += 1
    
#     print len(list_scores)

        
    
    
       
    
    
#     performance = {}        
#     for key, unsorted_score in unsorted_scores.items():
#         
#         for thr in sorted_score:
#             new_pr = compute_performance(thr, recognition_pair_value, key)
#             new_list = performance.get(key, [])
#             new_list.append(new_pr)
#             performance[key] = new_list

    
#         valid_list = [valid_item for valid_item in  os.listdir(valid_id_path) if os.path.isdir(os.path.join(valid_id_path, valid_item))]
       
  
#     read the experiment file where the scores are sorted and evaluated 
    
    

        
    
#  
    

    return



if __name__ == '__main__':
    argv = sys.argv[1:]
    
    if len(argv) < 2:
        print 'not enough argument!'
        exit(2)
        
    local_keyword = argv[0]
    local_cv = argv[1]
    
    if argv[2] == 'local':
        local_threshold_performace(local_keyword, local_cv)
    else:
        global_threshold_performace(local_keyword)
        
    
    