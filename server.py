# -*- coding: UTF-8 -*-
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver 
import tornado.gen 

import argparse
import torch
import os

import main
import time
import serverCall
import json as js
import copy
from tornado.options import define, options
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

model_dir = "hsjaklhjsbvxsabvdsbgahdjscdsakfdg"
dset_dir = ""
data = ""
model= ""
gpu = ""


tornado.options.define("port", default=5006, help="变量保存端口，默认5006",type = int)

class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin","*")
        self.set_header("Access-Control-Allow-Headers","*")
        self.set_header('Access-Control-Allow-Methods','POST,GET,OPTIONS')
        self.set_header("Content-Type","application/json;charset=utf-8")
       

    def get(self):
        self.write("Hello, world")

class ParseHandler(tornado.web.RequestHandler):

    def initialize(self, data):
        self.data = data
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin","*")
        self.set_header("Access-Control-Allow-Headers","*")
        self.set_header('Access-Control-Allow-Methods','POST,GET,OPTIONS')
        self.set_header("Content-Type","application/json;charset=utf-8")
        
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.write("parse data")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        global dset_dir
        global gpu
        global model_dir
        global data
        global model
        getData = js.loads(self.request.body.decode('utf-8'))  
        sentence = getData["q"]
        model_dir_new = getData["model_dir"]

        seg = True
        model_dir,dset_dir,data,model,result_output = yield serverCall.parse(sentence,model_dir_new,dset_dir,gpu,model_dir,data,model,seg)
        self.set_status(200)
        self.finish(result_output)
    




class trainHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(1)
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin","*")
        self.set_header("Access-Control-Allow-Headers","*")
        self.set_header('Access-Control-Allow-Methods','POST,GET,OPTIONS')
        self.set_header("Content-Type","application/json;charset=utf-8")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.write("train data")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        getData = js.loads(self.request.body.decode('utf-8')) 

        doTrain = getData["doTrain"]

        if doTrain == 1:
            data = getData["data"]
            save_model_dir = "/app/data/" + getData["save_model_dir"] + "/" + getData["save_model_dir"] + ".train"
            train_file = "/app/data/" + getData["save_model_dir"]  + "/" + getData["save_model_dir"] + ".train.char"
            test_file = "/app/data/" + getData["save_model_dir"]  + "/" + getData["save_model_dir"] + ".test.char"
            dev_file = "/app/data/" + getData["save_model_dir"]  + "/" + getData["save_model_dir"] + ".dev.char"
            char_emb = "/app/data/gigaword_chn.all.a2b.uni.ite50.vec"
            bichar_emb = None
            gaz_file = "/app/data/ctb.50d.vec"

            seg = True
            global gpu

            folder = os.path.exists("/app/data/" + getData["save_model_dir"])

            if not folder:
                os.makedirs("/app/data/" + getData["save_model_dir"])#makedirs 创建文件时如果路径不存在会创建这个路径
                print "---  new folder...  ---"
                print "---  OK  ---"
                result_output = yield self.trainServer(data,train_file,gaz_file,dev_file,test_file,char_emb,bichar_emb,gpu,save_model_dir,seg)
            else:
                result_output = "This model already exists! "
        else:
            result_output = "no train"

        self.set_status(200)
        self.write(result_output)
    
    @run_on_executor
    def trainServer(self, data,train_file,gaz_file,dev_file,test_file,char_emb,bichar_emb,gpu,save_model_dir,seg):
        result_output = serverCall.train(data,train_file,gaz_file,dev_file,test_file,char_emb,bichar_emb,gpu,save_model_dir,seg)
        return result_output

class ModelHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin","*")
        self.set_header("Access-Control-Allow-Headers","*")
        self.set_header('Access-Control-Allow-Methods','POST,GET,OPTIONS')
        self.set_header("Content-Type","application/json;charset=utf-8")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        result_output = yield serverCall.getModel()
        self.write(result_output)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def delete(self):
        getData = js.loads(self.request.body.decode('utf-8')) 

        delete_dir = getData["save_model_dir"]
        yield serverCall.deleteModel(delete_dir)
        
        self.write("delete model")


def make_app():
    global data 
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/parse", ParseHandler,dict(data=data)),
        (r"/train", trainHandler),
        (r"/model",ModelHandler)
    ], autoreload=True)

def initialize():
    
    global gpu
    gpu = torch.cuda.is_available()

    return

if __name__ == "__main__":
    print("model initialize... please wait")
    initialize()
    print("Success model initialize!")
    app = make_app()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()