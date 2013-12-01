import os
f = open("sms_dictionary.txt","rb")
line = f.read()
f.close()
new_lines = line.split('<li>')
words = {}	

for k in range(1,len(new_lines)):
	Line = new_lines[k]
#	print Line
	temp = ""
	index = 0
	for i in range(0,len(Line)-3):
		temp = Line[i]+Line[i+1]+Line[i+2]
		if temp == "php":
			index = i+3
			break
#	print index
#	print "hello"
	sms_word = ""
	temp = ""
	for j in range(index,len(Line)-3):
		temp = Line[j] + Line[j+1] + Line[j+2]
		if temp!="</a":
			sms_word+=Line[j]
		else:
			index = j
			break
	index = index + 11
	sms_word = sms_word[2:len(sms_word)]
	
	temp = ""
	normal_word = ""
	for i in range(index,len(Line)-5):
		temp = temp + Line[i]+Line[i+1]+Line[i+2]+Line[i+3]+Line[i+4]
		if temp!="</li>":
			normal_word = normal_word+Line[i]
		else:
			break
	print sms_word,normal_word
	words[sms_word] = normal_word

print len(words)
f = open("sms_words.txt","wb")
for k,v in words.items():
	line = k+"[]"+words[k]
	f.write(line)
	f.write("\n")
print len(new_lines)