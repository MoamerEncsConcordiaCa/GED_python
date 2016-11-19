#!/usr/bin/env python
#PBS -l walltime=00:01:00
#PBS -l nodes=16:ppn=4


import os, platform, sys
import subprocess
from compute_scores import call_compute_score

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)

from global_codes.global_values import *



def job(p_file_name, p_task_param):

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
    print SRC
    
    out_dir_path = os.path.abspath(os.path.join(SRC, '../../out_dir'))
    print os.path.exists(out_dir_path), out_dir_path 
    
    cv_list = [cv_item for cv_item in  os.listdir(out_dir_path) if os.path.isdir(os.path.join(out_dir_path, cv_item)) and cv_item[0:2] == 'cv']
    

#     print ' cv is '
    cv_item = p_task_param['cv_list'][0]
    
#     print cv_item
    
#     /out_dir/cv*/train
    source_id_path = os.path.join(out_dir_path, cv_item, experiment_set_path, 'train')
#     /out_dir/cv*/valid
    target_id_path = os.path.join(out_dir_path, cv_item, experiment_set_path, p_task_param['target_list'][0])
      
         
    keyword_item = [train_item for train_item in  p_task_param['train_list'] if os.path.isdir(os.path.join(source_id_path, train_item))][0]
    keyword_item_dir  = os.path.join(source_id_path, keyword_item)
    keyword_item_file_ids  = [file_id for file_id in  os.listdir(keyword_item_dir) if os.path.isfile(os.path.join(keyword_item_dir, file_id))]
    
      
    target_list = [valid_item for valid_item in  os.listdir(target_id_path) if os.path.isdir(os.path.join(target_id_path, valid_item))]
  
    target_item_len = len(target_list)
    target_item_index = 0
    for target_item in target_list:
        target_item_index += 1
        target_item_dir = os.path.join(target_id_path, target_item)
        target_item_file_ids  = [file_id for file_id in  os.listdir(target_item_dir) if os.path.isfile(os.path.join(target_item_dir, file_id))]
#         print target_item_file_ids
        target_id_len = len(target_item_file_ids)
        target_id_index = 0
        for target_item_file_id in target_item_file_ids:
            target_id_index += 1
            if target_item_file_id[0] == '.':
                continue
            for keyword_item_file_id in keyword_item_file_ids:
                
                if keyword_item_file_id[0] == '.':
                    continue
                
#                 cmd_txt = "./compute_scores.py  {0} {1} {2} {3}".format( 
#                             keyword_item_file_id, target_item_file_id, target_item, p_file_name)
#                 print cmd_txt

#                 subprocess.call(cmd_txt, shell = True)
                call_compute_score(keyword_item_file_id, target_item_file_id, target_item, p_task_param)
                
            print 'item({0}/{1}) id({2}/{3})'.format(
                    target_item_index, target_item_len, target_id_index, target_id_len 
                    )
            
#             target_id_index += 1
        
#         target_item_index += 1
        

                
    print 'summary'
    print 'item({0}/{1}) id({2}/{3})'.format(
                    target_item_index, target_item_len, target_id_index, target_id_len 
                    )     
#     subprocess.call('wait', shell = True)
    print 'job finished'
    exit()
 

   

if __name__ == '__main__':
    print 'job.py started +++++++++++++++++++++++++++'
#      __cluster__
#     argv = os.environ.get('argv', None)
#     p_file_name = argv[1:-1]

#    comment 
    argv = sys.argv[1:]
    p_file_name = argv[0]

    
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
    
    print task_param
    
    job(p_file_name, task_param)
    

