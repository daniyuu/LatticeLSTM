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


@gen.coroutine
def parse(sentence,model_dir_new,dset_dir,gpu,model_dir,data,model):
    result_output=""
    seg = True
    if model_dir_new == model_dir:
        
        data.generate_instance_with_gaz(sentence, 'sentence')
        decode_results = main.parse_text(model,data, 'raw', gpu, seg)
        result = data.write_decoded_results_back(decode_results, 'raw')
        result_output=js.dumps(result)

    else:

        model_dir = model_dir_new
        dset_dir = "/app/data/" + model_dir + "/" + model_dir + ".train.dset"
        one_model_dir = "/app/data/" + model_dir + "/" + model_dir + ".train.0.model"
        data = main.load_data_setting(dset_dir)
        model = main.load_model(one_model_dir, data, gpu)

        data.generate_instance_with_gaz(sentence, 'sentence')
        decode_results = main.parse_text(model,data, 'raw', gpu, seg)
        result = data.write_decoded_results_back(decode_results, 'raw')
        result_output=js.dumps(result)

    return model_dir_new,dset_dir,data,model,result_output



@gen.coroutine
def train(dataInput,train_file,gaz_file,dev_file,test_file,char_emb,bichar_emb,gpu,save_model_dir,seg):
    data = main.Data()
    data.write_http_data(train_file, dataInput)
    data.write_http_data(test_file, dataInput)
    data.write_http_data(dev_file, dataInput)

    data.HP_gpu = gpu
    data.HP_use_char = False
    data.HP_batch_size = 1
    data.use_bigram = False
    data.gaz_dropout = 0.5
    data.norm_gaz_emb = False
    data.HP_fix_gaz_emb = False

    main.data_initialization(data, gaz_file, train_file,dev_file,test_file)
    data.generate_instance_with_gaz(train_file, 'train')
    data.generate_instance_with_gaz(dev_file, 'dev')
    data.generate_instance_with_gaz(test_file, 'test')
    data.build_word_pretrain_emb(char_emb)
    data.build_biword_pretrain_emb(bichar_emb)
    data.build_gaz_pretrain_emb(gaz_file)
    main.train(data, save_model_dir, seg)
    return "save over"


@gen.coroutine
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print "---  new folder...  ---"
		print "---  OK  ---"
    else:
		print "---  There is this folder!  ---"



   