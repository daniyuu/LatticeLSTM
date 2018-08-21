Chinese NER Using Lattice LSTM
====

Lattice LSTM for Chinese NER. Character based LSTM with Lattice embeddings as input.

Models and results can be found at our ACL 2018 paper [Chinese NER Using Lattice LSTM](https://arxiv.org/pdf/1805.02023.pdf). It achieves 93.18% F1-value on MSRA dataset, which is the state-of-the-art result on Chinese NER task.

Details will be updated soon.

Requirement:
======
	Python: 2.7   
	PyTorch: 0.3

Input format:
======
CoNLL format (prefer BIOES tag scheme), with each character its label for one line. Sentences are splited with a null line.

	美	B-LOC
	国	E-LOC
	的	O
	华	B-PER
	莱	I-PER
	士	E-PER

	我	O
	跟	O
	他	O
	谈	O
	笑	O
	风	O
	生	O 

Pretrained Embeddings:
====
The pretrained character and word embeddings are the same with the embeddings in the baseline of [RichWordSegmentor](https://github.com/jiesutd/RichWordSegmentor)

Character embeddings: [gigaword_chn.all.a2b.uni.ite50.vec](https://pan.baidu.com/s/1pLO6T9D)

Word(Lattice) embeddings: [ctb.50d.vec](https://pan.baidu.com/s/1pLO6T9D)

Predefined Model:
====
The CommonNER Model: 

How to run the code?
====
1. Download the character embeddings and word embeddings and put them in the `data` folder.
2. Modify the `run_main.py` or `run_demo.py` by adding your train/dev/test file directory.
3. `sh run_main.py` or `sh run_demo.py`

How to run the server?
====
1. Download the predefined Model and put them in the `data` folder, 'CommonNER' model is a default model.
2. Run `python server.py --port=5002`.
3. Now you can access the Lattice server, example:

	parse_example:if there are not "model_dir" model, the server will use the default model.
	url:http://localhost:5002/parse;
	Hearder: Content-Type:application/x-www-form-urlencoded;
	raw:
	{
		"model_dir":"",
		"q":"我想从南京到上海"
	}

	train_example:if "doTrain" equal to 1, the server will start a train.
	url:http://localhost:5002/train;
	Hearder: Content-Type:application/x-www-form-urlencoded;
	raw:
	{
		"save_model_dir" : "mytest",
		"doTrain":1,
		"data":[
					{	"text" : "我想去北京",
						"entities":[{
							"start":3,
							"end":5,
							"value":"北京",
							"entity":"目的地",
							"entity_id":1}]
					},
					{
						"text" : "从澳洲去云南的票还有吗",
						"entities":[{
							"start":1,
							"end":3,
							"value":"澳洲",
							"entity":"出发地",
							"entity_id":1},
							{
							"start":4,
							"end":6,
							"value":"云南",
							"entity":"目的地",
							"entity_id":1}]
					},
					{
						"text" : "我想前往上海",
						"entities":[{
							"start":4,
							"end":6,
							"value":"上海",
							"entity":"目的地",
							"entity_id":1}]
					}
				]
	}

Resume NER data 
====
Crawled from the Sina Finance, it includes the resumes of senior executives from listed companies in the Chinese stock market. Details can be found in our paper.


Cite: 
========
Please cite our ACL 2018 paper:

    @article{zhang2018chinese,  
     title={Chinese NER Using Lattice LSTM},  
     author={Yue Zhang and Jie Yang},  
     booktitle={Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (ACL)},
     year={2018}  
    }
    
Code
========

Pre-progress
1. Alphabet

        self.word_alphabet, one word one item
        self.biword_alphabet, every two close words are one item
        self.char_alphabet, it same with word_alphabet when the language is Chinese
        self.label_alphabet, memory the laebl
        
        char_emb = "data/gigaword_chn.all.a2b.uni.ite50.vec", character-level embedding
        
2. Gaz file and gaz alphabet 

        gaz_file = "data/ctb.50d.vec", lattice dictionary
        gaz_alphabet, create a alphabel for training dataset by using lattice dictionary 