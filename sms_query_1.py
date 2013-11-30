# First step involves inputting an SMS query through XML
# Second step involves cleaning it and retreive best possibilties as a list
# 21195
import math
import os
from xml.dom import minidom
import xml.etree.ElementTree as ET
import logging
import string
import os
import sys
from collections import defaultdict
phi = 1
sms_dictionary = {}
eng_faq = defaultdict(list)
sms_vowels = ["a","e","i","o"]
numbers = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",0:"zero"}

def preprocess_sms_dictionary():
	f  = open("sms_words.txt","rw+")
	lines = f.readlines()
	for line in lines:
		sword,nword = line.split("[]")
#		print sword,nword
		sms_dictionary[sword] = nword

#	for k,v in sms_dictionary.items():
#		print k,sms_dictionary[k]
#	print len(sms_dictionary)


def check_in_corpus(word):
	for k,v in sms_dictionary.items():
#		if word == "2" and k == "to":
#			print word,k
		if word == k.lower():
#			print word,sms_dictionary[k]
			wrd = sms_dictionary[k]
			return wrd[0:len(wrd)-1]
	return None

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
			domain = ""
			question = ""
			indomain = 0
			
			if root[i][1].tag == 'SMS_TEXT':
				question = root[i][1].text

			if root[i][2][0].tag == 'ENGLISH':
				if root[i][2][0].text == 'NONE':
					indomain = 0
					domain = ""
				else:
					domain = root[i][2][0].text
					index = len(domain) -1 

					while index>=0:
						if domain[index] == '_':
							break
						index = index - 1

					domain = domain[0:index]
					indomain = 1
			questions.append((domain,question,indomain))
#		print questions[0:5]
		return questions

	def build_eng_faq_dictionary(self):
		tree = ET.parse("/home/rohit/Dropbox/Project/Faq/Faq_retrieval/FIRE_TRAINING_DATA/FIRE2013_TRAINING_DATA/FAQs/English/eng.xml")
		root = tree.getroot()		
		domains = []
		for i in range(0,len(root)):
			for j in range(0,4):
				if root[i][j].tag == 'FAQID':
					wrd = root[i][j].text
					index = len(wrd)-1
					while index>=0:
						if wrd[index] == '_':
							break
						index = index - 1
					wrd = wrd[0:index]
					if wrd not in domains:
						domains.append(wrd)
		print domains
		data = []
		for i in range(0,len(root)):
			domain = ""
			question = ""
			for j in range(0,4):
				if root[i][j].tag == 'FAQID':
					domain = root[i][j].text
					index = len(domain)-1
					while index>=0:
						if domain[index] == '_':
							break
						index = index - 1
					domain = domain[0:index]
				if root[i][j].tag == 'QUESTION':
					question = root[i][j].text	
			data.append((domain,question))

		print data[0:10]
		for domain,question in data:
			eng_faq[domain].append(question)
		print eng_faq['ENG_CAREER']
		return eng_faq

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
	newword = ""

	for i in range(0,len(word)):
		if word[i].isdigit():
#			print "inside" + " "+ word[i]
			n = int(word[i])
			newword = newword + numbers[n]
		else:
			newword = newword + word[i]

#	print newword
	word = newword
#	print word
	set_of_words = []
	if word in sms_vowels:
		set_of_words.append(word)
		return set_of_words

	for d in dictionary:
		if d[0] == first_letter:
			set_of_words.append(d)

	dict_list = {}
	if not set_of_words:
		temp_list = []
		set_of_words.append(word)
		return set_of_words

	else:
		for w in set_of_words:
			lcs_value = lcs(w,word,len(w),len(word))
			MAX_LEN = max(len(w),len(word))
			lcs_ratio = lcs_value/(MAX_LEN*1.0)
			edit_distance_value = edit_distance(w,word)
			if lcs_value/(edit_distance_value*1.0) > phi:
				dict_list[w] = (lcs_value/(edit_distance_value*1.0))

	dict_list = sorted(dict_list, key=dict_list.__getitem__)
#   dictionary to list conversion
	temp_list = []
	for wrd in dict_list:
		if wrd == word:
			temp_list.append(word)
			return temp_list
	dict_list = dict_list[::-1]
#	print dict_list[0:5]
	return dict_list[0:5]

if __name__=="__main__":
	c = input_from_xml()
	questions = c.fetch_input_from_xml_questions()
	dictionary = c.build_dictionary(questions)
#	print len(dictionary)
	dictionary.sort()
#	print dictionary[10000:10500]
	sms_queries = c.fetch_sms_queries()
	preprocess_sms_dictionary()
	c.build_eng_faq_dictionary()
#	for k,v in sms_dictionary.items():
#		print k,sms_dictionary[k]
	
	print len(sms_dictionary)

	for domain,query,indomain in sms_queries[0:4]:
		pruned_word_list = []
		for ch in string.punctuation:
			if ch!= '#':
				query = query.replace(ch,"")
		print query
		sms_query_words = query.split(" ")
		for i in range(0,len(sms_query_words)):
			print sms_query_words[i]
			sms_query_words[i] = sms_query_words[i].lower()
			corpus_word = check_in_corpus(sms_query_words[i])
			if corpus_word:
				temp_list = []
				temp_list.append(corpus_word)
	#			print temp_list
				pruned_word_list.append(temp_list)
			else:
				wrdlist = similarity_measure(sms_query_words[i],dictionary)
				if not wrdlist:
					wrdlist.append(sms_query_words[i])
				pruned_word_list.append(wrdlist)

		for i in range(0,len(pruned_word_list)):
			print sms_query_words[i],pruned_word_list[i]

		cleaned_sms_sentence = ""
		for i in range(0,len(pruned_word_list)):
			cleaned_sms_sentence = cleaned_sms_sentence + pruned_word_list[i][0]
			cleaned_sms_sentence = cleaned_sms_sentence + " "

		# English faq has been constructed 
		


		