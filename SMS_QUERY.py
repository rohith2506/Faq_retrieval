# First step involves inputting an SMS query through XML
# Second step involves cleaning it and retreive best possibilties as a list

import math
import os
from xml.dom import minidom
import xml.etree.ElementTree as ET
import logging
import string
from collections import defaultdict

class input_from_xml():
	# fetch questions input from eng.xml
	def fetch_input_from_xml_questions(self):
		tree = ET.parse("/home/infinity/Algo/Project/FIRE_TRAINING_DATA/FIRE2013_TRAINING_DATA/FAQs/English/eng.xml")
		root = tree.getroot()
		# Get questions from mono_training_data
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

		return questions

	# Build dictionary from given questions in training data
	def build_dictionary(self,questions):
		dictionary = []
		for domain,question in questions.items():
			for quest in question: 
				# Replace punctuations with null character
				for c in string.punctuation:
					quest = quest.replace(c,"")
				words = quest.split()
				for i in range(0,len(words)):
					words[i] = words[i].lower()
					if words[i] not in dictionary:
						dictionary.append(words[i])
		return dictionary

	def fetch_sms_queries():
		tree = ET.parse("/home/infinity/Algo/Project/FIRE_TRAINING_DATA/FIRE2013_TRAINING_DATA/SMS_Queries/Monolingual Task/English/_ENG_2013_MONO_TRAINING_DATA.xml")
		root = tree.getroot()

		# Get sms questions from mono_training_data
		questions = []
		for i in range(0,len(root)):
			for j in range(0,4):
				if(root[i][j].tag == 'QUESTION'):
					questions.append(root[i][j].text)
		return questions


if __name__=="__main__":
	c = input_from_xml()
	questions = c.fetch_input_from_xml_questions()
	dictionary = c.build_dictionary(questions)
	print len(dictionary)
	dictionary.sort()
	print dictionary[10000:10500]
	sms_queries = fetch_sms_queries()








