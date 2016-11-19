
import os
from readGraphXml import readGraphInfo
from HED import *
from test.test_math import test_file
import sys
from genericpath import exists
# from HED.global_values import p_norm_type_list

def compute_performance(thr, recognition_pair_value, key):
    
    score_pairs = recognition_pair_value.get(key, [])
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

def do_train(p_train_keywords_dict, p_valid_keywords_dict, p_graph_path, p_Ce, p_Cn,
              p_alpha,p_ED_type, p_out_dir, norm_type_list):
    print 'train started'
    
    cost_param = {'Tn':p_Cn, 'Te':p_Ce, 'A':p_alpha}
    #print type(cost_param)
    #print cost_param.get('Tn')
    print cost_param
    
    unsorted_scores = {}
    recognition_pair_value = {}
    
#     p_valid_keywords_dict = p_valid_keywords_dict.items()[1:2]
#     p_train_keywords_dict = p_train_keywords_dict.items()[:2]
#     print p_valid_keywords_dict
#     print p_train_keywords_dict
    print len(p_valid_keywords_dict) 
    print len(p_train_keywords_dict)
    
    valid_id = 0
    train_id = 0
    
    for key_valid, file_valid_list in p_valid_keywords_dict.items():
        
        print 'valid number'
        print valid_id 
        print len(p_valid_keywords_dict) 
        valid_id += 1
        
        for file_vaild in file_valid_list:
            file_valid_path = os.path.join(p_graph_path, file_vaild + '.gxl')
            if not os.path.exists(file_valid_path):
                print 'invalid file:' + file_valid_path
                continue
            g_valid = readGraphInfo(file_valid_path)
                        
            
            for key_train,file_train_list in  p_train_keywords_dict.items():
                print 'train id'
                print train_id 
                print len(p_train_keywords_dict)
                train_id += 1 
                
                scores_dict ={}
                for file_train in file_train_list:
                    file_train_path = os.path.join(p_graph_path, file_train+ '.gxl')
                    if not os.path.exists(file_train_path):
                        print 'invalid file:' + file_train_path
                        continue
                    g_train = readGraphInfo(file_train_path)
                    # TODO select base on algo type
                    distance = HED(g_train, g_valid, cost_param)
                    normalization_score = get_normalization(g_train, g_valid, norm_type_list, cost_param)
                    
                    #normalizing                              
                    for norm_type in norm_type_list:  
                        normal_d = distance / normalization_score.get(norm_type)
                 
                        new_list = scores_dict.get(norm_type, []) 
                        new_list.append(normal_d)
                        scores_dict[norm_type]  = new_list
                        
                    
            
                #print '++++++++++++'
                #print scores_dict
                for key, value in scores_dict.items():
                    min_score= reduce(min, value)
                    #print min_score
                    min_score_pair = [min_score, key_train, key_valid]
                    
                    
                    new_list = unsorted_scores.get(key, [])
                    new_list.append(min_score)
                    unsorted_scores[key] = new_list
                    
                    new_list = recognition_pair_value.get(key, [])
                    new_list.append(min_score_pair)
                    recognition_pair_value[key] = new_list
                
#                 print unsorted_scores
#                 print recognition_pair_value
                
    print 'evaluating the performance'   
#     print unsorted_scores
#     print recognition_pair_value
#     
    performance = {}        
    for key, unsorted_score in unsorted_scores.items():
        #print 'key, unsorted score'
        #print key
        #print unsorted_score
        unsorted_score.sort()
        sorted_score = unsorted_score
        #print sorted_score
        
        for thr in sorted_score:
            new_pr = compute_performance(thr, recognition_pair_value, key)
            new_list = performance.get(key, [])
            new_list.append(new_pr)
            performance[key] = new_list
                
  
    #print performance
    print 'train Finished '
    
    #return the performance
    return performance

def do_test(p_CV_dir, p_graph_path, p_Ce, p_Cn, p_alpha,p_ED_type, p_out_dir):
    print 'test'

def do_one_train_experiment(p_CV_dir, word_dir,p_graph_path, p_Ce,p_Cn,p_alpha,p_ED_type,p_norm_type_list,  p_out_dir):
    print p_Ce
    print p_alpha
    print p_Cn
    print p_CV_dir
    print p_graph_path
    print p_ED_type
    print p_out_dir
    
    #preparing the out put path
    # path + ED type + Cn, Ce value
    if not os.path.exists(p_out_dir):
        os.mkdir(p_out_dir)
        print 'path created:' + p_out_dir
    local_out_dir = os.path.join(p_out_dir, p_ED_type)
    
    if not os.path.exists(local_out_dir):
        os.mkdir(local_out_dir)
        
    local_param_str = 'Cn='+ str(p_Cn)+ ',Ce= ' + str(p_Ce) + ',a='+ str(p_alpha)
    
    local_out_dir = os.path.join(local_out_dir, local_param_str)
    if not os.path.exists(local_out_dir):
        os.mkdir(local_out_dir)
    
    # reading the list of files
    all_word_file = os.path.join(word_dir, 'words.txt')    
    train_file = os.path.join(p_CV_dir, 'train.txt')
    valid_file = os.path.join(p_CV_dir, 'valid.txt')
    keyword_file = os.path.join(p_CV_dir, 'keywords.txt')

    h_all_word_file = open(all_word_file, "r")
    read_lines_buff = h_all_word_file.readlines()
    all_word_list =[]
    for line in read_lines_buff:
        all_word_list.append(line.splitlines()[0])
    #print all_word_list[0]
    
    
    h_train_file = open(train_file, "r")
    read_lines_buff = h_train_file.readlines()   
    train_list =[]
    for line in read_lines_buff:
        train_list.append(line.splitlines()[0])
    #print train_list[0]
    
    h_valid_file = open(valid_file, 'r')
    read_lines_buff = h_valid_file.readlines()
    valid_list =[]
    for line in read_lines_buff:
        valid_list.append(line.splitlines()[0])
    #print valid_list[0]
    
    h_keyword_file = open(keyword_file, 'r')
    read_lines_buff = h_keyword_file.readlines()
    keyword_list =[]
    for line in read_lines_buff:
        keyword_list.append(line.splitlines()[0])
    #print keyword_list[0]
    
#     print all_word_list
#     print train_list
#     print valid_list
#     print keyword_list
#     
    #all word dict
    all_word_dict ={}
    for word in all_word_list:
        #parts = word.splitlines()
        parts = word.split(' ')
        
        if len(parts) < 2:
            continue
        
        key = parts[1]
        value = parts[0]
        new_value = all_word_dict.get(key, [])
        new_value.append(value)
        all_word_dict[key] = new_value
    #print all_word_dict    
    #print 'all word finished'
    
    #print train_list
       
    train_keywords_dict ={}
    for keyword in keyword_list:
        #train_keywords_dict[keyword] = [] 
        #keyword = keyword.splitlines()[0]
        selected_values = []
        
        candidates_from_all_words = all_word_dict.get(keyword, [])
        for candidate_word in candidates_from_all_words:
            #print candidate_word[:6]
            if candidate_word[:6] in train_list:
                selected_values.append(candidate_word)
                
#             for prefix_file in train_list:
#                 if candidate_word.startswith( prefix_file ):
#                     selected_values.append(candidate_word)
        train_keywords_dict[keyword] = selected_values
        
    valid_keywords_dict ={}
    for key, candidate_values in all_word_dict.items():
        selected_values =[]
        
        for candidate in candidate_values:
            if candidate[:6] in valid_list:
                selected_values.append(candidate)
        valid_keywords_dict[key] = selected_values
              
        
      
     
    print len(all_word_list)
    print len(train_keywords_dict)
    print len(valid_keywords_dict)   
    
    sum = 0
    for key, val in train_keywords_dict.items():
        print key, 'values are'
        sum += len(val)
        for value in val:
            print value
            
    print len(train_keywords_dict.items())
    print sum
     
    return 

    performance = do_train(train_keywords_dict, valid_keywords_dict, p_graph_path, p_Ce, p_Cn, p_alpha, 
                           p_ED_type, p_out_dir, p_norm_type_list)
    local_out_dir_norm_type = local_out_dir
    
    for norm_type in p_norm_type_list:
        local_out_dir_norm_type = local_out_dir
        local_out_dir_norm_type = os.path.join(local_out_dir_norm_type, norm_type)
        
        if not os.path.exists(local_out_dir_norm_type):
            os.mkdir(local_out_dir_norm_type)
            print 'path created:' + local_out_dir_norm_type
            
        performance_file_name = local_out_dir_norm_type + '/performance.txt'
        
        performance_file_h = open(performance_file_name, 'w')
        performance_list = performance.get(norm_type)
        for performance_item in performance_list:
            
            #{'thr': thr, 'acc': acuracy, 'TP':TP, 'TN':TN, 'FP':FP, 'FN':FN}
            
            performance_file_h.write('acc:' + str(performance_item.get('acc')) + '\t')  
            performance_file_h.write('TP:' + str(performance_item.get('TP')) + '\t')  
            performance_file_h.write('TN:' + str(performance_item.get('TN')) + '\t')  
            performance_file_h.write('FP:' + str(performance_item.get('FP')) + '\t')  
            performance_file_h.write('FN:' + str(performance_item.get('FN')) + '\t')  
            
            performance_file_h.write('TH:' + str(performance_item.get('thr')) + '\n')
            # Dict
            #performance_file_h.write(str(performance_item))
            
                
            
            
            
            
        
    
    
    #print performance
def make_experiment_set_files(p_keywords_dict, p_set_path, p_root_path):
    
    if not os.path.exists(p_root_path):
        os.mkdir(p_root_path)
    local_path = os.path.join(p_root_path, p_set_path)
    
    if not os.path.exists(local_path):
        os.mkdir(local_path)
        
    for key, val in p_keywords_dict.items():
        local_key_path = os.path.join(local_path, key)
        if not os.path.exists(local_key_path):
            os.mkdir(local_key_path)
        
        for file_id in val:
            local_file_id_name = os.path.join(local_key_path, file_id)
            h_file = open(local_file_id_name, 'w')
            h_file.close()

   
def make_experiment_sets(p_CV_dir, word_dir,p_out_dir, p_experiment_set_path):
    
    print 'start of make '
    
    #preparing the out put path
    if not os.path.exists(p_out_dir):
        os.mkdir(p_out_dir)
        print 'path created:' + p_out_dir
        
        
    # reading the list of files
    all_word_file = os.path.join(word_dir, 'words.txt')    
    train_file = os.path.join(p_CV_dir, 'train.txt')
    valid_file = os.path.join(p_CV_dir, 'valid.txt')
    keyword_file = os.path.join(p_CV_dir, 'keywords.txt')
    test_file  = os.path.join(p_CV_dir, 'test.txt')

    
    h_all_word_file = open(all_word_file, "r")
    read_lines_buff = h_all_word_file.readlines()
    all_word_list =[]
    for line in read_lines_buff:
        all_word_list.append(line.splitlines()[0])
#     print all_word_list[0]
#     print 'all words', len(all_word_list)
    h_all_word_file.close()
    
    
    h_train_file = open(train_file, "r")
    read_lines_buff = h_train_file.readlines()   
    train_list =[]
    for line in read_lines_buff:
        train_list.append(line.splitlines()[0])
#     print train_list[0]
#     print 'train words', len(train_list)
    h_train_file.close()
    
    
    h_valid_file = open(valid_file, 'r')
    read_lines_buff = h_valid_file.readlines()
    valid_list =[]
    for line in read_lines_buff:
        valid_list.append(line.splitlines()[0])
#     print valid_list[0]
#     print 'valid list', len(valid_list)
    h_valid_file.close()
    
    h_test_file = open(test_file, 'r')
    read_lines_buff = h_test_file.readlines()
    test_list =[]
    for line in read_lines_buff:
        test_list.append(line.splitlines()[0])
#     print test_list[0]
#     print 'test list', len(test_list)
    h_test_file.close()
        
    
    
    h_keyword_file = open(keyword_file, 'r')
    read_lines_buff = h_keyword_file.readlines()
    keyword_list =[]
    for line in read_lines_buff:
        keyword_list.append(line.splitlines()[0])
#     print keyword_list[0]
#     print 'keyword list', len(keyword_list)
    h_keyword_file.close()
    
   
    
#     print all_word_list
#     print train_list
#     print valid_list
#     print keyword_list
#     
    
    #all word dict
    all_word_dict ={}
    for word in all_word_list:
        parts = word.split(' ')
        
        if len(parts) < 2:
            print 'invalid data', parts
            continue
        
        key = parts[1]
        value = parts[0]
        new_value = all_word_dict.get(key, [])
        new_value.append(value)
        all_word_dict[key] = new_value
        
        
#     sum = 0
#     for key, val in all_word_dict.items():
#         print key, 'values are'
#         sum += len(val)
#         for value in val:
#             print value
#             
#     print len(all_word_dict.items())
#     print sum


    train_keywords_dict ={}
    for keyword in keyword_list:
        selected_values = []
        
        candidates_from_all_words = all_word_dict.get(keyword, [])
        for candidate_word in candidates_from_all_words:
            if candidate_word[:6] in train_list:
                selected_values.append(candidate_word)
                
        train_keywords_dict[keyword] = selected_values



       
    valid_keywords_dict ={}
    for key, candidate_values in all_word_dict.items():
        selected_values =[]
        
        for candidate in candidate_values:
            if candidate[:6] in valid_list:
                selected_values.append(candidate)
        valid_keywords_dict[key] = selected_values
              
    test_keywords_dict ={}
    for key, candidate_values in all_word_dict.items():
        selected_values =[]
        
        for candidate in candidate_values:
            if candidate[:6] in test_list:
                selected_values.append(candidate)
        test_keywords_dict[key] = selected_values
        
      
#     print 'size of items' 
#     print len(all_word_list)
#     print len(train_keywords_dict)
#     print len(valid_keywords_dict)  
#     print len(test_keywords_dict)
#     

    
#     print p_experiment_set_path
#     print p_out_dir
#     
    experiment_path =  os.path.join(p_out_dir,  p_experiment_set_path)
    
    make_experiment_set_files(train_keywords_dict, 'train', experiment_path)
    make_experiment_set_files(test_keywords_dict, 'test', experiment_path)
    make_experiment_set_files(valid_keywords_dict, 'valid', experiment_path)
    
    
    
    print 'end of make'
    return    
  
def make_parameters(p_out_dir, p_parameter_path, p_Ed_type, p_Cn, p_Ce, p_alpha, p_norm_type_list):
    print p_Ed_type
    print p_Ce
    print p_Cn
    print p_out_dir
    print p_parameter_path
    
    print 'start of parameters'   
    if not os.path.exists(p_out_dir):
        os.mkdir(p_out_dir)
    local_root = os.path.join(p_out_dir, p_parameter_path)
    
    if not os.path.exists(local_root):
        os.mkdir(local_root) 
    
    for ed_alg in p_Ed_type:
        ed_path = os.path.join(local_root, ed_alg)
        if not exists(ed_path):
            os.mkdir(ed_path)
        for cn in p_Cn:
            for ce in p_Ce:
                for alpha in p_alpha:
#                     param_str = "Cn:%s Ce:%s a:%s", cn, ce, alpha
                    param_str = 'Cn='+ str(cn)+ ', Ce=' + str(ce) + ', a='+ str(alpha)
                    param_path = os.path.join(ed_path, param_str)
#                     print param_path
                    if not exists(param_path):
                        os.mkdir(param_path)
                        
                    for norm_type in p_norm_type_list:
                        norm_path = os.path.join(param_path, norm_type)
                        if not exists(norm_path):
                            os.mkdir(norm_path)
  

