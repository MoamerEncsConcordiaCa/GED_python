#!/usr/bin/env python

import os, sys
import subprocess
import platform

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)

from global_codes.global_values import *
from global_codes.readGraphXml import *
from HED.HED import *

def get_path_upto_param(p_out_dir, p_task):
    '''
     scores go to the out_dir/scores/cv*/train_keyword/train_id/valid or test/valid_id/alg_tpe/para/norm_tpe/score.txt
   
     scores go to the out_dir/scores/cv*/alg_tpe/para/valid or test/valid_id/train_keyword/train_id/norm_tpe/score.txt
   
    '''
    path_scores = os.path.join(p_out_dir, experiment_scores)
    if not os.path.exists(path_scores):
        os.mkdir(path_scores)
    
    path_cv = os.path.join(path_scores, str(p_task['cv_list'][0]))
    if not os.path.exists(path_cv):
        os.mkdir(path_cv)
 
    path_alg = os.path.join(path_cv, str(p_task['alg_type'][0]))
    if not os.path.exists(path_alg):
        os.mkdir(path_alg)
 
    path_param = os.path.join(path_alg, str(p_task['graph_param'][0]))
    if not os.path.exists(path_param):
        os.mkdir(path_param)
        
    path_target = os.path.join(path_param, str(p_task['target_list'][0]))
    if not os.path.exists(path_target):
        os.mkdir(path_target)
        
    path_target_name = os.path.join(path_target, str(p_task['target_name']))
    if not os.path.exists(path_target_name):
        os.mkdir(path_target_name)    
    
    path_target_id = os.path.join(path_target_name, str(p_task['target_id']))
    if not os.path.exists(path_target_id):
        os.mkdir(path_target_id)
    
    path_train_keywrod = os.path.join(path_target_id, str(p_task['train_list'][0]))
    if not os.path.exists(path_train_keywrod):
        os.mkdir(path_train_keywrod)

    path_train_id = os.path.join(path_train_keywrod, str(p_task['keyword_id']))
    if not os.path.exists(path_train_id):
        os.mkdir(path_train_id)
     
     
     
#     change to last path   
    return path_train_id
       
    
    
def get_cost_param(p_task):
    
    '''
    cost_param = {'Tn':p_Cn, 'Te':p_Ce, 'A':p_alpha}
    p_task['graph_param'] =  ['Cn=1, Ce=0, a=0.5'],
    '''
    cost_string =  p_task['graph_param'][0].split(',')
    
#     print cost_string
    cost_param = {}        
    cost_param['Tn'] = float (cost_string[0].split('=')[1])
    cost_param['Te'] = float (cost_string[1].split('=')[1])
    cost_param['A'] = float (cost_string[2].split('=')[1])
    
#     print cost_param  
         
    return cost_param

def compute_score(p_task):
    print 'compute_score_ started'
    
    '''
    scores go to the out_dir/scores/cv*/train_keyword/train_id/valid or test/valid_id/alg_tpe/para/norm_tpe/score.txt
    
    1) make path for score
    1.5)make graph path
    2) read source and target graphs
    3) call alg with paramteres
    4) store param in score.txt
    '''
   
#     print p_task
    
    if platform.system() == 'Linux':

        home = os.environ['HOME']
        
        SRC=home +'/sourcecode/Graph_Based_Word_Spotting/Edit_Distance_Algorithms/cluster/' 
        if not os.path.exists(SRC):
            print 'source directory does not exist'
            return
    
    elif platform.system() == 'Darwin':
        SRC = os.getcwd()
        if not os.path.exists(SRC):
            print 'source directory does not exist'
            return


    os.chdir(SRC)
    #print SRC
    
    out_dir_path = os.path.abspath(os.path.join(SRC, '../../out_dir'))
    #print os.path.exists(out_dir_path), out_dir_path 
    
    path_param = get_path_upto_param(out_dir_path,  p_task)
#     print path_param
#    check if the score is computed yet
    
    local_exist = False
    norm_type_list = p_task['norm_type_list']
    for norm_type in norm_type_list:  
        
        path_score = os.path.join(path_param, norm_type)
        if not os.path.exists(path_score):
            os.mkdir(path_score)
             
        score_file_name = path_score + '/score.txt'
        
        if  os.path.exists(score_file_name):
            local_exist = True
        break

    if local_exist:
        return
    
    file_score = open(score_file_name, 'w')
    file_score.close()
    
    path_graphs = os.path.abspath( os.path.join(out_dir_path, '../', DATA_SET_PATH, DATA_SET_PATH_GRAPHS))
#     print path_graphs
    
    file_name_source = os.path.join(path_graphs, p_task['keyword_id'] + '.gxl')
    if not os.path.exists(file_name_source):
        print 'invalid file path {0}'.format(file_name_source)
        return
    

    file_name_target = os.path.join(path_graphs, p_task['target_id'] + '.gxl')
    if not os.path.exists(file_name_target):
        print 'invalid file path {0}'.format(file_name_target)
        return
   
    

    graph_source = readGraphInfo(file_name_source)
    graph_target = readGraphInfo(file_name_target)
    
    
    
    cost_param = get_cost_param(p_task)       
    norm_type_list = p_task['norm_type_list'] 
    scores_dict ={}
    
    
    distance = HED(graph_source, graph_target, cost_param)
    normalization_score = get_normalization(graph_source, graph_target, norm_type_list, cost_param)
                    
    #normalizing                              
    for norm_type in norm_type_list:  
        normal_d = distance / normalization_score.get(norm_type) 
        new_list = scores_dict.get(norm_type, []) 
        new_list.append(normal_d)
        scores_dict[norm_type]  = new_list
        
        path_score = os.path.join(path_param, norm_type)
        if not os.path.exists(path_score):
            os.mkdir(path_score)
             
        score_file_name = path_score + '/score.txt'
        
        file_score = open(score_file_name, 'w')
        file_score.write(str(normal_d))
        file_score.close()
        
            
    print scores_dict            
    

def call_compute_score(p_source_id, p_target_id, p_target_name, task_param):
    
    print 'call compute score'
    task_param['keyword_id'] = p_source_id
    task_param['target_id'] = p_target_id
    task_param['target_name'] = p_target_name

    print task_param
    compute_score(task_param)
    print '++++++++++++++++++++++++++++++++++++++++++++++++++++'

    

if __name__ == '__main__':
#      __cluster__
#     argv = os.environ.get('argv', None)
#     p_file_name = argv[1:-1]

#    comment 
    argv = sys.argv[1:]
#     print argv
    
    p_target_id = argv[1]
    p_source_id = argv[0]
    p_target_name = argv[2] 
    p_file_name = argv[3]
    
    
    if not os.path.exists(p_file_name):
        print 'file {0} does not exists'.format(p_file_name)
        
    task_param = {}
    if os.path.exists(p_file_name):
        file_h = open(p_file_name, 'r')
        buf  = file_h.readlines()
        for line in buf:
            part0 = line.split('\n')
            part1 = part0[0][:-1].split(':')
            task_param[str(part1[0])] = part1[1].split(';')
        file_h.close()
    
    task_param['keyword_id'] = p_source_id
    task_param['target_id'] = p_target_id
    task_param['target_name'] = p_target_name
    
    
    print task_param
    
#     compute_score(task_param)


