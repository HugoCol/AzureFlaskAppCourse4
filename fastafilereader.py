def fastafile_reader(file):
    open(file)
    linelist = []
    for line in file:
        linelist.append(line)

    print(linelist)
    return linelist

#
# if __name__ == '__main__':
#     file = open('fastatest.fasta')
#     fastafile_reader(file)
