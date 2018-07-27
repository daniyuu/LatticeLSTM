# -*- coding: UTF-8 -*-
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver 
import tornado.gen 

import argparse
import torch
import main
import serverCall
import json as js
import copy
from tornado.options import define, options


model_dir = ""
dset_dir = ""
data = ""
model=""
gpu =""


tornado.options.define("port", default=5006, help="变量保存端口，默认8000",type = int)

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
        model_dir,dset_dir,data,model,result_output = yield serverCall.parse(sentence,model_dir_new,dset_dir,gpu,model_dir,data,model)
        self.set_status(200)
        self.finish(result_output)

class trainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin","*")
        self.set_header("Access-Control-Allow-Headers","*")
        self.set_header('Access-Control-Allow-Methods','POST,GET,OPTIONS')
        self.set_header("Content-Type","application/json;charset=utf-8")

    def get(self):
        self.write("train data")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        getData = js.loads(self.request.body.decode('utf-8')) 
        
        data = getData["data"]
        
        save_model_dir = "/app/data/" + getData["save_model_dir"] + "/" + getData["save_model_dir"] + ".train"
        train_file = "/app/data/" + getData["save_model_dir"]  + "/" + getData["save_model_dir"] + ".train.char"
        test_file = "/app/data/" + getData["save_model_dir"]  + "/" + getData["save_model_dir"] + ".test.char"
        dev_file = "/app/data/" + getData["save_model_dir"]  + "/" + getData["save_model_dir"] + ".dev.char"
        char_emb = None #getData["char_emb"]
        bichar_emb = None #getData["bichar_emb"]
        gaz_file = None #getData["gaz_file"]
        seg = True
        global gpu

        serverCall.mkdir("/app/data/" + getData["save_model_dir"])
        result_output = yield serverCall.train(data,train_file,gaz_file,dev_file,test_file,char_emb,bichar_emb,gpu,save_model_dir,seg)
        self.set_status(200)
        self.write(result_output)

def make_app():
    global data 
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/parse", ParseHandler,dict(data=data)),
        (r"/train", trainHandler)
    ])

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