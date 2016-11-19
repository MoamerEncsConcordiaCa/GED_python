#!/usr/bin/env python

import os, sys
import subprocess
import platform

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)
#os.chdir('..')

from global_codes.global_values import *
#os.chdir('cluster')

def all_job_submitter_to_cluster(argv):
    print "function: all_job_submitter_to_cluster()"
    for arg in argv:
        print arg
    print "++++++++++++++++++++++++++++++++++++++++"
    #print platform.system()

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
     
    out_dir_path = os.path.abspath(os.path.join(SRC, '../../out_dir'))
    print os.path.exists(out_dir_path), out_dir_path 
    
    cv_list = [cv_item for cv_item in  os.listdir(out_dir_path) if os.path.isdir(os.path.join(out_dir_path, cv_item)) and cv_item[0:2] == 'cv']
#     cv_path = [os.path.join(out_dir_path, cv) for cv in cv_list]
    
    task_list =[]
#     print 'in each cv '
    for cv_item in cv_list:
        
        train_id_path = os.path.join(out_dir_path, cv_item, experiment_set_path, 'train')
        valid_id_path = os.path.join(out_dir_path, cv_item, experiment_set_path, 'valid')
             
        train_list = [train_item for train_item in  os.listdir(train_id_path) if os.path.isdir(os.path.join(train_id_path, train_item))]

        valid_list = [valid_item for valid_item in  os.listdir(valid_id_path) if os.path.isdir(os.path.join(valid_id_path, valid_item))]
        del valid_list
        
                 
        param_path = os.path.join(out_dir_path, cv_item, experiment_parameters)
        
        # i.e. HED
        alg_type_list = [alg_item for alg_item in  os.listdir(param_path) if os.path.isdir(os.path.join(param_path, alg_item))]
        for alg_type in alg_type_list:
            alg_path = os.path.join(param_path, alg_type)
#             print os.path.exists(alg_path), alg_path
            
            graph_param_list = [graph_param_item for graph_param_item in  os.listdir(alg_path) 
                                if os.path.isdir(os.path.join(alg_path, graph_param_item))]
            
            for graph_param in graph_param_list:
                graph_param_path = os.path.join(alg_path, graph_param)
#                 print os.path.exists(graph_param_path), graph_param
                norm_type_list = [norm_item for norm_item in  os.listdir(graph_param_path) 
                                if os.path.isdir(os.path.join(graph_param_path, norm_item))]
                                    
                
                
                for train_item in train_list:
                    one_job_params = {}
                    one_job_params['cv_list'] = [cv_item]
                    one_job_params['alg_type'] = [alg_item]
                    one_job_params['graph_param_list'] = [graph_param]
                    one_job_params['norm_type_list'] = norm_type_list
                    one_job_params['target_list'] = ['valid']
                    
                    one_job_params['train_list'] = [train_item] 
                    task_list.append(one_job_params)
            
                                
      
#     qsub -v argv=['test_val'],arg2=['val2']  job.py
    job_dir_path = os.path.join(out_dir_path, task_list_path)
    if not os.path.exists(job_dir_path):
        os.mkdir(job_dir_path)
        
    task_count = 0 
    for task in task_list:
        

        job_file_param = job_dir_path+'/job.' + str(task['train_list'][0]) + str(task_count) + '.txt'
        file_h  = open(job_file_param, 'w')


        file_h.write('cv_list:')
        for cv in task['cv_list']:
                file_h.write(str(cv))
                file_h.write(';')
        
        file_h.write('\nalg_type:')
        for alg in task['alg_type']:
                file_h.write(str(alg))
                file_h.write(';')
                
        file_h.write('\ngraph_param:')
        for g_p in task['graph_param_list']:
                file_h.write(str(g_p))
                file_h.write(';')

        file_h.write('\nnorm_type_list:')
        for norm_type in task['norm_type_list']:
                file_h.write(str(norm_type))
                file_h.write(';')
                
        file_h.write('\ntarget_list:')
        for target in task['target_list']:
                file_h.write(str(target))
                file_h.write(';')
        
        file_h.write('\ntrain_list:')
        for train_item in task['train_list']:
                file_h.write(str(train_item))
                file_h.write(';')
                
        file_h.close()
#      __cluster__
#         cmd_qsub = 'qsub -v argv=[{0}],  ./job.py'.format(job_file_param) 
        cmd_qsub = 'python  ./job.py {0}'.format(job_file_param) 
        
#         print cmd_qsub 
        if job_file_param.find('W-a-s-h-i-n-g-t-o-n-s_cm') > 0:
            
            print 'starting job : '
            
            print cmd_qsub 
            
            subprocess.call(cmd_qsub, shell = True)
            
            task_count += 1
        if task_count > 0 :
            break
        
        
        
    print 'total jobs are',  len(task_list)   
 
#     write all task to one files
#     all_task_file = job_dir_path+'job.' + str('all_task')  + '.txt'
#     file_h  = open(all_task_file, 'w')
#     for task in task_list:
#         file_h.write(str(task) + '\n')
#     file_h.close()
        
    
    
        



if __name__ == '__main__':
    argv = sys.argv[1:]
    all_job_submitter_to_cluster(argv)


