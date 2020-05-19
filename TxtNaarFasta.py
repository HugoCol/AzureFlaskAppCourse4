txt = open("dataset.txt", "r")
fasta = open("FastaDataset.fasta", "w+")

gegevens = []
for regel in txt:
    gegevens.append(regel.replace("\n", "").split("\t"))

# Gaf "ï»¿" bij eerste regel dus word hieronder weg gehaald.
gegevens[0][0] = gegevens[0][0].replace("ï»¿", "")

for i in range(len(gegevens)):
    gegevens[i][0] = gegevens[i][0].replace("@", ">")
    gegevens[i][3] = gegevens[i][3].replace("@", ">")

i = 0
while i < 100:
    fasta.write(gegevens[i][0] + "\n")
    fasta.write(gegevens[i][1] + "\n")
    fasta.write(gegevens[i][3] + "\n")
    fasta.write(gegevens[i][4] + "\n")
    i += 1