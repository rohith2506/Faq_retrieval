# First step involves inputting an SMS query through XML
# Second step involves cleaning it and retreive best possibilties as a list

import math
import os
from xml.dom import minidom
import xml.etree.ElementTree as ET
import logging
import string
from collections import defaultdict
phi = 1

class input_from_xml():
	# fetch questions input from eng.xml
	def fetch_input_from_xml_questions(self):
		tree = ET.parse("/home/rohit/Dropbox/Project/Faq/Faq_retrieval/FIRE_TRAINING_DATA/FIRE2013_TRAINING_DATA/FAQs/English/eng.xml")
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

	def fetch_sms_queries(self):
		tree = ET.parse("/home/rohit/Dropbox/Project/Faq/Faq_retrieval/FIRE_TRAINING_DATA/FIRE2013_TRAINING_DATA/SMS_Queries/Monolingual Task/English/_ENG_2013_MONO_TRAINING_DATA.xml")
		root = tree.getroot()
		# Get sms questions from mono_training_data
		questions = []
		for i in range(0,len(root)):
			for j in range(0,3):
				if(root[i][j].tag == 'SMS_TEXT'):
					questions.append(root[i][j].text)
		return questions

def min(a,b,c):
	if a > b:
		if b > c:
			return c
		else:
			return b
	else:
		if a > c:
			return c
		else:
			return a

def LevenshteinDistance(s,len_s,t,len_t):
	if len_s == 0:
			 return len_t
	if len_t == 0:
		 return len_s
	if s[len_s-1] == t[len_t-1]: 
		cost = 0
	else:
		cost = 1
	return min(LevenshteinDistance(s,len_s-1,t,len_t) + 1,LevenshteinDistance(s,len_s,t,len_t-1)+1,LevenshteinDistance(s,len_s-1,t,len_t-1) + cost)

def lcs(s1,s2,m,n):
	if m==0 or n==0:
		return 0
	if s1[m-1]==s2[n-1]:
		return 1+lcs(s1,s2,m-1,n-1)
	else:
		return max(lcs(s1,s2,m,n-1),lcs(s1,s2,m-1,n))

def cs(word):
	pruned_word = ""
	pruned_word+=word[0]
	for i in range(1,len(word)):
		if word[i] != word[i-1]:
			pruned_word+=word[i]

	new_word = ""
	vowels = ['a','e','i','o','u']
	for ch in pruned_word:
		if ch not in vowels:
			new_word+=ch

	return new_word

def edit_distance(w,word):
	w1 = cs(w)
	w2 = cs(word)
	return LevenshteinDistance(w1,len(w1),w2,len(w2))+1

def similarity_measure(word,dictionary):
	first_letter = word[0]
#	print word
	set_of_words = []
	for d in dictionary:
		if d[0] == first_letter:
			set_of_words.append(d)

	dict_list = {}
	if not set_of_words:
		return None
	else:
		for w in set_of_words:
			lcs_value = lcs(w,word,len(w),len(word))
			MAX_LEN = max(len(w),len(word))
			lcs_ratio = lcs_value/(MAX_LEN*1.0)
			edit_distance_value = edit_distance(w,word)
			if lcs_value/(edit_distance_value*1.0) > phi:
				dict_list[w] = (lcs_value/(edit_distance_value*1.0))

	dict_list = sorted(dict_list, key=dict_list.__getitem__)
#	print dict_list
	return dict_list[::-1]


if __name__=="__main__":
	c = input_from_xml()
	questions = c.fetch_input_from_xml_questions()
	dictionary = c.build_dictionary(questions)
#	print len(dictionary)
	dictionary.sort()
#	print dictionary[10000:10500]
	sms_queries = c.fetch_sms_queries()

	for query in sms_queries:
		pruned_word_list = []
		for ch in string.punctuation:
			query = query.replace(ch,"")
		sms_query_words = query.split()
		for i in range(0,len(sms_query_words)):
			print sms_query_words[i]
			sms_query_words[i] = sms_query_words[i].lower()
			pruned_word_list.append(similarity_measure(sms_query_words[i],dictionary))
#		print pruned_word_list
		break





