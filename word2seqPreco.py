import sys
import random

file = sys.argv[1]
outFile = sys.argv[2]

def split_coref(coref):
	coref = " ".join(coref)
	coref = " | ".join(coref.split("|"))
	return coref

def reduce_numbers(coref):
	coref = coref.split()
	n_map = []
	reduced_coref = []

	for cor in coref:
		p1, p2 = "", ""

		if cor in ["|", "_"] :
			reduced_coref.append(cor)
		else:
			n = cor.strip("()")
			if "(" in cor: p1 = "("
			if ")" in cor: p2 = ")"

			if n not in n_map:
				n_map.append(n)
			reduced_coref.append(f"{p1}{n_map.index(n)}{p2}")
	return reduced_coref

doc, sentence, coref, cor = [], [], [], []

with open(file, "r") as f:
	with open(outFile+".src", "w") as out1:
		with open(outFile+".trg", "w") as out2:	

			for line in f:

				if "#begin document" in line:
					doc, sentence, coref, cor = [], [], [], []
					current_sentence = 1

				elif "#end document" in line:

					for i in range(len(doc)):
						for j in range(i+1, len(doc)):
							#r = random.random()

							if 1: #j == i+4 or j >= len(doc)-1 or r <= 0.1:

								text = [k for l in doc[i:j] for k in l]
								c = [k for l in coref[i:j] for k in l]

								if len(text) >= 10: #Write only +10 len seq
									
									c_split_reduced = reduce_numbers((split_coref(c)))
									out1.write(" ".join(text)+"\n")
									out2.write(" ".join(c_split_reduced)+"\n")
					break

				else:
					tab = line.strip("\n").split("\t")

					if sentence and tab[0] in [".","!","?"]:
						doc.append(sentence)
						coref.append(cor)
						sentence, cor = [], []

					sentence.append(tab[0])
					cor.append(tab[1])