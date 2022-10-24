from gramformer import Gramformer
import csv

gf = Gramformer(models=1)

f = open('inputs/outputs/word_delete_output.csv', 'r', encoding='utf-8')
example = []
rdr = csv.reader(f)
for line in rdr:
    if line[0] == "text":
        continue
    else:
        example.append(line[0])
f.close()

print(example)

for item in example:
    print(gf.correct(item, max_candidates=1))
