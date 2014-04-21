import math
import os
from xml.dom import minidom
import xml.etree.ElementTree as ET
import logging
import string
import os
import sys
import time
import zmq
import codecs
from collections import defaultdict
from nltk.corpus import wordnet as wn
import jsonrpclib
from simplejson import loads
from sms_query_1 import input_from_xml
from svm_test import main_function
threshold_score = 0.5
'''
		tree = ET.parse("/home/rohspeed/Faq_retrieval/FIRE_TRAINING_DATA/FIRE2013_TRAINING_DATA/FAQs/English/eng.xml")
		root = tree.getroot()
		questions = defaultdict(list)
		data = []

				for i in range(0,len(root)):
			domain   = ""
			question = ""
			for j in range(0,4):
				if root[i][j].tag == "DOMAIN":
					domain = root[i][j].text
				if root[i][j].tag == "QUESTION":
					question = root[i][j].text
			data.append((domain,question))

		for domain,question in data:
			questions[domain].append(question)

				fname = codecs.open('kernel_trees.txt','w+', encoding='utf-8')
		fname.seek(0,0)
'''

class convert_training_data():
	def convert_to_parse_tree(self,question):
		server = jsonrpclib.Server("http://localhost:8080")
		try:
			question = question.strip()
			question = question.encode('ascii','ignore')
			result = loads(server.parse(question))
			if result:
				res = result['sentences'][0]['parsetree']
#				print res
				return res
				print "#################"
		except UnicodeEncodeError:
			print "Error in question format"

class kernel_function():
	def data_from_svm(self):
		questions,predict,classes,scores, domains = main_function()
		context = zmq.Context()
		socket = context.socket(zmq.REQ)
		socket.connect("tcp://127.0.0.1:5000")
		
		for i in range(0,len(questions)):
			quest = questions[i]
			train_questions_indices = []
			fname = open("kernel_trees.txt","r")
			max_score = -4.0
			for score in scores[i]:
				max_score = max(score,max_score)	
			if max_score >= threshold_score:
				print "iam here in one"
				domain = domains[predict[i]]
				temp = input_from_xml()
				dmns,quests = temp.fetch_input_from_xml_questions()
				
				cnt = 1
				indices = []
				for k,v in quests.items():
					temp_questions = quests[k]
					for i in range(0,len(temp_questions)):
						if(k == domain):
							indices.append(cnt)
						cnt = cnt + 1

				for i in range(0,len(indices)):
					train_questions_indices.append(indices[i])

			else:
				print "iam here in two"
				line_cnt = 1
				for line in fname.readlines():
					train_questions_indices.append(line_cnt)
					line_cnt = line_cnt + 1

			temp2 = convert_training_data()

			parse_quest = temp2.convert_to_parse_tree(quest)
			print len(parse_quest)
			msg = str(parse_quest)

			msg2 = ""
			for i in range(0,len(train_questions_indices)):
				msg2 = msg2 + str(train_questions_indices[i])
				msg2 = msg2 + "$"
			msg2 = str(msg2)

			main_msg = msg + "\n" + msg2
			socket.send(main_msg)
			time.sleep(1000)

if __name__ == "__main__":
	obj = kernel_function()
	obj.data_from_svm()