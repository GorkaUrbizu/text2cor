import sys

src_file = sys.argv[1]
trg_file = sys.argv[2]
outFile = sys.argv[3]

with open(src_file, "r") as src_f:
	with open(trg_file, "r") as trg_f:
		with open(outFile, "w") as out:

			for s, t in zip(src_f, trg_f):
				src = s.strip("\n")
				trg = t.strip("\n")
				out.write(src+"\t"+trg+"\n")
