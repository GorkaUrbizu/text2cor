import sys

join_file = sys.argv[1]
src_file = sys.argv[2]
trg_file = sys.argv[3]

with open(join_file, "r") as join_f:
	with open(src_file, "w") as src_f:
		with open(trg_file, "w") as trg_f:

			for j in join_f:
				join = j.strip("\n").split("\t")
				src, trg = join[0], join[1]
				src_f.write(src+"\n")
				trg_f.write(trg+"\n")
