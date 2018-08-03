# -*- coding: utf-8 -*-
# @Author: Jie
# @Date:   2017-06-15 14:11:08
# @Last Modified by:   Jie Yang,     Contact: jieynlp@gmail.com
# @Last Modified time: 2018-07-06 11:08:27
from tornado import gen
import main
import json as js
import os
import time
import shutil

@gen.coroutine
def parse(sentence,model_dir_new,dset_dir,gpu,model_dir,data,model,seg):
    result_output=""
    
    if model_dir_new == model_dir:
        
        data.generate_instance_with_gaz(sentence, 'sentence')
        decode_results = main.parse_text(model,data, 'raw', gpu, seg)
        result = data.write_decoded_results_back(decode_results, 'raw')
        result_output=js.dumps(result)

    else:
        dset_dir_new = "/app/data/" + model_dir_new + "/" + model_dir_new + ".train.dset"

        haveModel = os.path.exists("/app/data/" + model_dir_new)
        haveDset = os.path.exists(dset_dir_new)

        if haveModel and haveDset:
            #处理文件路径
            dirs = os.listdir("/app/data/" + model_dir_new + "/")
            maxValue = 0
            for file in dirs:
                strArray = file.split('.')
                strArrayLen = len(strArray)
                if strArrayLen > 1 and strArray[strArrayLen-1]=='model':
                    index_int = int(strArray[strArrayLen-2])
                    if maxValue < index_int:
                        maxValue = index_int

            one_model_dir_new = "/app/data/" + model_dir_new + "/" + model_dir_new + ".train." + str(maxValue) +".model"
            print one_model_dir_new
            haveModel = os.path.exists(one_model_dir_new)

            if haveModel:

                model_dir = model_dir_new
                dset_dir = dset_dir_new 
                one_model_dir = one_model_dir_new
                #初始化
                data = main.load_data_setting(dset_dir)
                model = main.load_model(one_model_dir, data, gpu)

                #处理sentence
                data.generate_instance_with_gaz(sentence, 'sentence')
                decode_results = main.parse_text(model,data, 'raw', gpu, seg)
                result = data.write_decoded_results_back(decode_results, 'raw')
                result_output=js.dumps(result)
            else:
                print "can not fine the model"
                print "use default model"
                model_dir,dset_dir,data,model,result_output = parseCommon(sentence,model_dir_new,dset_dir,gpu,model_dir,data,model,seg)
 
        else:
            print "can not fine the model"
            print "use default model"
            model_dir,dset_dir,data,model,result_output = parseCommon(sentence,model_dir_new,dset_dir,gpu,model_dir,data,model,seg)
            
        
    return model_dir,dset_dir,data,model,result_output

def parseCommon(sentence,model_dir_new,dset_dir,gpu,model_dir,data,model,seg):

    if "common" == model_dir:
        data.generate_instance_with_gaz(sentence, 'sentence')
        decode_results = main.parse_text(model,data, 'raw', gpu, seg)
        result = data.write_decoded_results_back(decode_results, 'raw')
        result_output=js.dumps(result)

    else:
        model_dir = "common"
        haveDset = os.path.exists("/app/data/CommonNER/common.dset")
        haveModel = os.path.exists("/app/data/CommonNER/common.35.model")

        if haveDset and haveModel:
            dset_dir = "/app/data/CommonNER/common.dset"
            one_model_dir = "/app/data/CommonNER/common.35.model"
            #初始化
            data = main.load_data_setting(dset_dir)
            model = main.load_model(one_model_dir, data, gpu)

            #处理sentence
            data.generate_instance_with_gaz(sentence, 'sentence')
            decode_results = main.parse_text(model,data, 'raw', gpu, seg)
            result = data.write_decoded_results_back(decode_results, 'raw')
            result_output = js.dumps(result)
        else:
            print "have not predefine model"

    return model_dir,dset_dir,data,model,result_output


def train(dataInput,train_file,gaz_file,dev_file,test_file,char_emb,bichar_emb,gpu,save_model_dir,seg):
    get_num = len(dataInput)

    if get_num>=3:

        data = main.Data()
        data.write_http_data(train_file, dataInput,'train')
        data.write_http_data(test_file, dataInput,'test')
        data.write_http_data(dev_file, dataInput,'dev')

        data.HP_gpu = gpu
        data.HP_use_char = True
        data.HP_batch_size = 1
        data.use_bigram = False
        data.gaz_dropout = 0.5
        data.norm_gaz_emb = False
        data.HP_fix_gaz_emb = True


        main.data_initialization(data, gaz_file, train_file,dev_file,test_file)
        data.generate_instance_with_gaz(train_file, 'train')
        data.generate_instance_with_gaz(dev_file, 'dev')
        data.generate_instance_with_gaz(test_file, 'test')
        data.build_word_pretrain_emb(char_emb)
        data.build_biword_pretrain_emb(bichar_emb)
        data.build_gaz_pretrain_emb(gaz_file)
        main.train(data, save_model_dir, seg)
        
        return "train over"
    else:
        return "train fail: the sentence_num must over 3"


@gen.coroutine
def getModel():
    print("model")
    dirs = os.listdir("/app/data/")
    maxValue = 0
    result =[]
    for file in dirs:
        haveModelFile = os.path.exists("/app/data/" + file + "/")
        print("/app/data/" + file + "/")
        if haveModelFile:
            havedset = os.path.exists("/app/data/" + file + "/" + file + ".train.dset")
            
            dirsModel = os.listdir("/app/data/" + file + "/")

            maxValue = 0
            for files in dirsModel:
                strArray = files.split('.')
                strArrayLen = len(strArray)
                if strArrayLen > 1 and strArray[strArrayLen-1]=='model':
                    index_int = int(strArray[strArrayLen-2])
                    if maxValue < index_int:
                        maxValue = index_int
            
            haveModel = os.path.exists("/app/data/" + file + "/" + file + ".train." + str(maxValue) +".model")

            if havedset and haveModel:
                result.append(file)
    
    result_output = js.dumps(result)
    print(result_output)

    return result_output


@gen.coroutine
def deleteModel(delete_model_dir):

    folder = os.path.exists("/app/data/" + delete_model_dir)
    if folder:
        shutil.rmtree("/app/data/" + delete_model_dir)




   