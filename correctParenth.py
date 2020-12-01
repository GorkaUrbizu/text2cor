def rremove(alist, x): #reversed remove: remove last apareance of x in list
    alist.pop(len(alist) - alist[::-1].index(x) - 1)


def correctParen(cors):
	clusList = [] #to keep cluster of the incorrect coref
	indList = [] #to keep index of the incorrect coref 
	i = 0
	while i in range(len(cors)):
		cor = cors[i]
		j=0
		found = 0
		aux = []
		cor = cor.split("|")
		while j in range(len(cor)): 
			c = cor[j]
			aux.append(c)
			if "(" in c and ")" not in c: # if (1
				clusList.append(c.strip("("))
				indList.append([i,j])
			elif ")" in c and "(" not in c:  # 1)
				if c.strip(")") not in clusList: # no (1 in list
					found = 1
					del aux[-1]
				else:
					indList.pop((-clusList[::-1].index(c.strip(")")))-1)
					rremove(clusList, c.strip(")"))
			if found:
				if "|" in cors[i]:
					cors[i] = "|".join(aux)
				else:	
					cors[i] = "_"
			j += 1	
		i += 1
	for i in reversed(indList):
		if isinstance(i, list):
			i,j = i[0],i[1]
			c = cors[i].split("|")
			if len(c) > 1:
				print(c)
				del c[j]
			else:
				c[j] = "_"
			cors[i] = "|".join(c)
		else:
			cors[i] = ("_")
	return cors

cor = "(1 _ 1) _ _ _ (2 (3) _ _ 4) _ (5 _ 5) _ (6) _ (7 | (8 8) _ (9) | 10) _ (4 | (5 | (6)"

print(cor)
cor = " ".join(correctParen(cor.split()))
print(cor)