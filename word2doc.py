import sys

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

doc, coref = [], []

with open(file, "r") as f:
	with open(outFile+".src", "w") as out1:
		with open(outFile+".trg", "w") as out2:	
			voc = []

			for line in f:

				if "#begin document" in line:
					doc, coref = [], []

				elif "#end document" in line:
					out1.write(" ".join(doc)+"\n")
					coref_split_reduced = reduce_numbers((split_coref(coref)))
					out2.write(" ".join(coref_split_reduced)+"\n")
				else:
					tab = line.strip("\n").split("\t")
					doc.append(tab[0])
					coref.append(tab[1])