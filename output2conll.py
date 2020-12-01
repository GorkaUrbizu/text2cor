import sys


src_file = sys.argv[1]
trg_file = sys.argv[2]
hyp_file = sys.argv[3]
out_name = sys.argv[4]


def correct_len2(L, n):
	if len(L) < n:
		return L + (["_"] * (n - len(L)))
	else:
		return L[:n]

def correct_len1(L, n):
	L2 = []
	i = 0

	for l in L:
		L2.append(l)

		if l == "|":
			i -= 1
		else:
			i += 1

		if i == n:
			break
	return L2	

def merge_label(trg):
	L = []
	label = ""
	for t in trg:
		if t == "|":
			if label[-1] == "_":
				label = label[:-1]
			else:
				label += t
		elif label and label[-1] == "|":
			if t == "_":
				label = label[:-1]
			else:
				label += t
		else:
			if label:
				L.append(label)
			label = t
	L.append(label)
	'''for i in L: 
		if "|" in i:
			print(i)'''
	return L

def rremove(alist, x): #reversed remove: remove last apareance of x in list
    alist.pop(len(alist) - alist[::-1].index(x) - 1)

def correct_paren(cors):
	#print(cors)
	clusList = [] #to keep cluster of the incorrect coref
	indList = [] #to keep index of the incorrect coref 

	for i in range(len(cors)):
		c = cors[i]

		if "(" in c and ")" not in c: # if (1
			clusList.append(c.strip("("))
			indList.append(i)

		elif ")" in c and "(" not in c:  # if 1)

			if c.strip(")") not in clusList: # no (1 in list
				cors[i] = "_"
				#cors[i] = "("+c.strip(")")+")"

			else: # (1 in list
				n = c.strip(")")
				indList.pop(-clusList[::-1].index(n)-1)
				rremove(clusList, n)

		'''if c not in ["_", "|"] and not ("(" in c and ")" in c):
			print(c)
			print(clusList)

	print(clusList)
	print(indList)'''
	for i in reversed(indList):
		cors[i] = "_"
		#cors[i] = "("+cors[i].strip("(")+")"

	return cors

def correct_trg(trg):
	#print(len(trg))
	#print(trg)
	hyp = correct_paren(trg)
	#print(len(hyp))
	#print(hyp)
	hyp = merge_label(hyp)
	#print(len(hyp))
	#print(hyp)
	return hyp

def correct_hyp(hyp, l):
	hyp = correct_len1(hyp, l)
	#print(len(hyp))
	#print(hyp)
	hyp = correct_paren(hyp)
	#print(len(hyp))
	#print(hyp)
	hyp = merge_label(hyp)
	#print(len(hyp))
	#print(hyp)
	hyp = correct_len2(hyp, l)
	#print(len(hyp))
	#print(hyp)
	return hyp
	#return correct_len(merge_label(correct_paren(hyp)), l)

def write_out(f, src, trg, i):
	f.write(f"#begin document test_{i}\n")
	for s, t in zip(src, trg):
		f.write(f"{s}\t{t}\n")
	f.write(f"#end document test_{i}\n")

def write_out2(f, src, trg, hyp, i):
	f.write(f"#begin document test_{i}\n")
	#print(f"#### len: {len(src)} {len(trg)} {len(hyp)}")
	for s, t, h in zip(src, trg, hyp):
		f.write(f"{s}\t\t{t}\t\t{h}\n")
	f.write(f"#end document test_{i}\n")

with open(src_file, "r") as src_f:
	with open(trg_file, "r") as trg_f:
		with open(hyp_file, "r") as hyp_f:
			with open(out_name+".pred", "w") as pred_f:
				with open(out_name+".gold", "w") as gold_f:
					with open(out_name+".txt", "w") as both_f:

						i = 0
						for s, t, h in zip(src_f, trg_f, hyp_f):
							#print(f"#### len: {len(s.split())} {len(t.split())} {len(h.split())}")

							if 1: # i == 40:

								print(f"TEST_{i}:")
								src = s.strip("\n").split()
								#print("_________trg_________")
								trg = correct_trg(t.strip("\n").split())
								#print("_________hyp_________")
								hyp = correct_hyp(h.strip("\n").split(), len(src))
								
								write_out(gold_f, src, trg, i)
								write_out(pred_f, src, hyp, i)
								write_out2(both_f, src, trg, hyp, i)
								#break
							i += 1
							#break
