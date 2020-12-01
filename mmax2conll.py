import sys
import string
from bs4 import BeautifulSoup as Soup
import os
import unicodedata

def removeAccents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii


def parseWords(file):
	handler = open(file, 'rb').read()
	soup = Soup(handler, "html5lib")
	words = []
	for word in soup.findAll('word'):
		#w = removeAccents(word.get_text())
		w = word.get_text()
		id = "_".join(word['id'].split("_")[1:])
		words.append([w, id])
	return(words)


def parseSentences(file):
	handler = open(file).read()
	soup = Soup(handler, "html5lib")
	sentences = []
	for sentence in soup.findAll('markable'):
		n = sentence['orderid']
		span = sentence['span'].split("..")
		spanA = "_".join(span[0].split("_")[1:])
		spanB = "_".join(span[-1].split("_")[1:])
		sentences.append([n, spanA, spanB])
	return(sentences)


def parseCoreferences(file):
	handler = open(file).read()
	soup = Soup(handler, "html5lib")
	coreferences = []
	for coreference in soup.findAll('markable'):
		try:
			cor = coreference['coref_set'].split("_")[-1]
			span = coreference['span'].split("..")
			spanA = "_".join(span[0].split("_")[1:])
			spanB = "_".join(span[-1].split("_")[1:])
			coreferences.append([cor, spanA, spanB])
		except:
			pass
	return(coreferences)




path = "ARRAU/data/"
all =  ["Pear_Stories/", "RST_DTreeBank/train/", "Trains_91/", "Trains_93/", "VPC/train/", "RST_DTreeBank/dev/", "RST_DTreeBank/test/", "VPC/test/"]
train = ["Pear_Stories/", "RST_DTreeBank/train/", "Trains_91/", "Trains_93/", "VPC/train/"]
dev = ["RST_DTreeBank/dev/"]
test = ["RST_DTreeBank/test/", "VPC/test/"]


fout = "data/train_ARRAU.conll" #/ "data/train_ARRAU_sen.conll": word \t sen \t cor \n 
folders = train

with open (fout, "w") as out:
	for folder in folders:
		maxW = 0
		print("### "+folder+" ###")
		pathFolder = path+folder+"MMAX/"
		for file in os.listdir(pathFolder):
			if file.endswith(".mmax"):
				try:
					file = file.split(".mmax")[0]
					#print(file)
					words = parseWords(pathFolder+"/Basedata/"+file+"_words.xml")
					sentences = parseSentences(pathFolder+"/markables/"+file+"_sentence_level.xml")
					coreferences = parseCoreferences(pathFolder+"/markables/"+file+"_coref_level.xml")
					sen = 0
					conll = []
					for word in words:
						cor = []
						w, i = word
						for sentence in sentences:
							if sentence[1] == i:
								sen+=1
						for coreference in coreferences:
							if coreference[1] == i and coreference[2] == i:
								cor.append("("+coreference[0]+")")
							elif coreference[1] == i:
								cor.append("("+coreference[0])
							elif coreference[2] == i:
								cor.append(coreference[0]+")")
						if cor:
							c = "|".join(cor)
						else:
							c = "_"
						conll.append([w,sen,c])
					out.write("#begin document "+file+"\n")
					if len(conll) > maxW:
						maxW = max(maxW,len(conll))
						print(maxW)
					for conl in conll:
						if "_" in conl[0]:
							for w in conl[0].split("_"):
								#out.write(w+"\t"+str(conl[1])+"\t"+conl[2]+"\n")
								out.write(w+"\t"+conl[2]+"\n")
						else:
							#out.write(conl[0]+"\t"+str(conl[1])+"\t"+conl[2]+"\n")
							out.write(conl[0]+"\t"+conl[2]+"\n")

					out.write("#end document "+file+"\n")
				except Exception as e: 
					print("Errorea fitxategi honekin: "+file)
					print(e)
