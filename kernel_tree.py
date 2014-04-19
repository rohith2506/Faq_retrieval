'''
Parse the Xml and retrrieve XMl
@Author: Rohit
'''
import math
import os
from xml.dom import minidom
import xml.etree.ElementTree as ET
import logging
import string
import os
import sys
import time
import codecs
from collections import defaultdict
from nltk.corpus import wordnet as wn
import jsonrpclib
from simplejson import loads


class convert_training_data():
	def input_from_xml(self):
		tree = ET.parse("/home/rohspeed/Faq_retrieval/FIRE_TRAINING_DATA/FIRE2013_TRAINING_DATA/FAQs/English/eng.xml")
		root = tree.getroot()
		questions = defaultdict(list)
		data = []
		server = jsonrpclib.Server("http://localhost:8080")
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
		for k,v in questions.items():
			temp_questions = questions[k]
			for question in temp_questions:
				print k,question
				try:
					question = question.strip()
					question = question.encode('ascii','ignore')
					result = loads(server.parse(question))
					if result:
						res = result['sentences'][0]['parsetree']
						print res
						fname.write(res+"\n")
						print "#################"
				except UnicodeEncodeError:
					print "Error in question format"
		return questions

if __name__ == "__main__":
	obj = convert_training_data()
	questions = obj.input_from_xml()
